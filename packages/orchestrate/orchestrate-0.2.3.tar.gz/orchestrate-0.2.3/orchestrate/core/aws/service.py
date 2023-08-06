import base64
import boto3
from botocore.exceptions import ClientError
import six
import time
import types

from orchestrate.common import safe_format
from orchestrate.core.exceptions import AwsClusterSharePermissionError, AwsPermissionsError, OrchestrateException
from orchestrate.core.paths import get_executable_path
from orchestrate.core.services.base import Service


def catch_aws_permissions_errors(func):
  def wrapper(*args, **kwargs):
    try:
      return func(*args, **kwargs)
    except ClientError as e:
      code = e.response['Error']['Code']
      http_status_code = e.response['ResponseMetadata']['HTTPStatusCode']
      if http_status_code == 403 or code in ('AccessDeniedException', 'UnauthorizedOperation'):
        six.raise_from(AwsPermissionsError(e), e)
      raise
  return wrapper

class AwsService(Service):
  def __getattribute__(self, name):
    attr = super(AwsService, self).__getattribute__(name)
    if isinstance(attr, types.MethodType):
      attr = catch_aws_permissions_errors(attr)
    return attr

  def get_region(self):
    return boto3.session.Session().region_name

  def describe_cluster(self, cluster_name):
    try:
      return self.services.eks_service.describe_cluster(cluster_name=cluster_name)['cluster']
    except self.services.eks_service.client.exceptions.ResourceNotFoundException as e:
      six.raise_from(
        OrchestrateException(safe_format(
          "We cannot find an EKS cluster named '{}' using your current AWS credentials."
          " Did someone delete this cluster?",
          cluster_name
        )),
        e
      )

  def create_kubernetes_cluster(self, options):
    cluster_name = options['cluster_name']
    cpu_nodes_config = options.get('cpu')
    gpu_nodes_config = options.get('gpu')
    assert cpu_nodes_config or gpu_nodes_config, "Looks like your cluster config file is not" \
      " asking us to spin up any CPU or GPU machines."

    role = self.services.iam_service.ensure_eks_role(cluster_name=cluster_name)
    eks_vpc_stack = self.services.cloudformation_service.ensure_eks_vpc_stack(cluster_name=cluster_name)
    eks_vpc_stack_outputs = dict((o['OutputKey'], o['OutputValue']) for o in eks_vpc_stack.outputs)
    security_groups = eks_vpc_stack_outputs.get('SecurityGroups', '').split(',')
    subnet_ids = eks_vpc_stack_outputs.get('SubnetIds', '').split(',')

    self.services.eks_service.ensure_cluster(
      cluster_name=cluster_name,
      eks_role=role,
      security_groups=security_groups,
      subnet_ids=subnet_ids,
    )

    key_name = self.services.ec2_service.ensure_key_pair_for_cluster(cluster_name).name

    worker_stacks = []
    if cpu_nodes_config:
      cpu_worker_stack = self.services.cloudformation_service.ensure_eks_worker_stack(
        cluster_name=cluster_name,
        security_groups=eks_vpc_stack_outputs.get('SecurityGroups', '').split(','),
        vpc_id=eks_vpc_stack_outputs.get('VpcId'),
        subnet_ids=eks_vpc_stack_outputs.get('SubnetIds', '').split(','),
        max_nodes=cpu_nodes_config['max_nodes'],
        min_nodes=cpu_nodes_config['min_nodes'],
        instance_type=cpu_nodes_config['instance_type'],
        key_name=key_name,
        gpu=False,
      )
      worker_stacks.append(cpu_worker_stack)

    if gpu_nodes_config:
      gpu_instance_type = gpu_nodes_config['instance_type']
      assert gpu_instance_type.startswith('p'), safe_format(
        "The gpu instance type ({}) does not support gpus",
        gpu_instance_type
      )
      gpu_worker_stack = self.services.cloudformation_service.ensure_eks_worker_stack(
        cluster_name=cluster_name,
        security_groups=eks_vpc_stack_outputs.get('SecurityGroups', '').split(','),
        vpc_id=eks_vpc_stack_outputs.get('VpcId'),
        subnet_ids=eks_vpc_stack_outputs.get('SubnetIds', '').split(','),
        max_nodes=gpu_nodes_config['max_nodes'],
        min_nodes=gpu_nodes_config['min_nodes'],
        instance_type=gpu_nodes_config['instance_type'],
        key_name=key_name,
        gpu=True,
      )
      worker_stacks.append(gpu_worker_stack)

    node_roles = []
    for worker_stack in worker_stacks:
      self.services.cloudformation_service.wait_for_eks_worker_stack(worker_stack)
      instance_role = next(o['OutputValue'] for o in worker_stack.outputs if o['OutputKey'] == 'NodeInstanceRole')
      node_roles.append(dict(arn=instance_role))

    self.connect_kubernetes_cluster(cluster_name=cluster_name, ignore_role=True)
    self.test_kubernetes_cluster()

    cluster_access_role = self.services.iam_service.ensure_cluster_access_role(cluster_name)
    text = self.services.template_service.render_template_from_file('eks/config_map.yml.ms', dict(
      node_roles=node_roles,
      cluster_access_role=dict(
        arn=cluster_access_role.arn,
        name=cluster_access_role.name,
      ),
    ))
    self.services.kubectl_service.apply(text)

    self.disconnect_kubernetes_cluster(cluster_name=cluster_name)
    self.connect_kubernetes_cluster(cluster_name=cluster_name)
    self.test_cluster_access_role(cluster_name=cluster_name, retries=3)
    self.test_kubernetes_cluster()

    self.services.kubectl_service.ensure_plugins()

    return self.describe_cluster(cluster_name)

  def test_cluster_access_role(self, cluster_name, retries=0, wait_time=5):
    sts_client = boto3.client('sts')
    cluster_access_role = self.services.iam_service.describe_cluster_access_role(cluster_name)
    for try_number in range(retries + 1):
      try:
        sts_client.assume_role(
          RoleArn=cluster_access_role.arn,
          RoleSessionName='cluster_access_test',
          DurationSeconds=900,
        )
      except ClientError as ce:
        if try_number >= retries:
          six.raise_from(
            AwsClusterSharePermissionError(safe_format(
              "You do not have permission to use the role '{}' for accessing this cluster.\n"
              "Please read the Orchestrate documentation for sharing clusters: {}",
              cluster_access_role.name,
              "https://app.sigopt.com/docs/orchestrate/deep_dive#cluster_sharing",
            )),
            ce,
          )
          raise
        else:
          time.sleep(wait_time)

  def test_kubernetes_cluster(self, **kwargs):
    self.services.kubectl_service.test_config(**kwargs)

  def connect_kubernetes_cluster(self, cluster_name, ignore_role=False):
    cluster = self.describe_cluster(cluster_name)

    if ignore_role:
      cluster_access_role_arn = None
    else:
      cluster_access_role_arn = self.services.iam_service.describe_cluster_access_role(cluster_name).arn

    # TODO(alexandra): optional role_arn is NOT the role ARN used to create the cluster
    # See Step 2 of https://docs.aws.amazon.com/eks/latest/userguide/getting-started.html
    template_args = dict(
      endpoint_url=cluster['endpoint'],
      base64_encoded_ca_cert=cluster['certificateAuthority']['data'],
      cluster_name=cluster_name,
      role_arn=cluster_access_role_arn,
      authenticator_binary_path=get_executable_path('aws-iam-authenticator')
    )

    self.services.kubectl_service.write_config(
      cluster_name=cluster_name,
      string=self.services.template_service.render_template_from_file('eks/kube_config.ms', template_args),
    )

  def disconnect_kubernetes_cluster(self, cluster_name):
    self.services.kubectl_service.ensure_config_deleted(cluster_name=cluster_name)

  def destroy_kubernetes_cluster(self, cluster_name):
    self.services.cloudformation_service.ensure_eks_worker_stack_deleted(cluster_name=cluster_name, gpu=True)
    self.services.cloudformation_service.ensure_eks_worker_stack_deleted(cluster_name=cluster_name, gpu=False)
    self.services.ec2_service.ensure_key_pair_for_cluster_deleted(cluster_name)
    self.disconnect_kubernetes_cluster(cluster_name=cluster_name)
    self.services.iam_service.ensure_cluster_access_role_deleted(cluster_name)
    self.services.eks_service.ensure_cluster_deleted(cluster_name=cluster_name)
    self.services.cloudformation_service.ensure_eks_vpc_stack_deleted(cluster_name=cluster_name)
    self.services.iam_service.ensure_eks_role_deleted(cluster_name=cluster_name)

  def login_to_container_registry(self, repository_name):
    repository = self.services.ecr_service.ensure_repositories([repository_name])['repositories'][0]
    registry_id = repository['registryId']
    authorization_data = self.services.ecr_service.get_authorization_token([registry_id])['authorizationData'][0]
    authorization_token = authorization_data['authorizationToken']
    decoded_bytes = base64.b64decode(authorization_token)
    (username, password) = decoded_bytes.decode('utf-8').split(':')
    proxy_endpoint = authorization_data['proxyEndpoint']
    return self.services.docker_service.login(
      server=proxy_endpoint,
      username=username,
      password=password,
    )

  def get_image_tag(self, repository_name):
    descriptions = self.services.ecr_service.describe_repositories([repository_name])
    return descriptions['repositories'][0]['repositoryUri']

  def node_access_instructions(self, cluster_name):
    filename = self.services.ec2_service.key_pair_location(cluster_name)
    return (safe_format(
      '*Optional:'
      '\n\tTo ssh into any ec2 node in your cluster, use the username `ec2-user` with the key pair located at:'
      '\n\t\t{filename}'
      '\n\tExample:'
      '\n\t\tssh -i {filename} ec2-user@<node_dns_name>'
      '\n\tYou may be required to change security groups on your ec2 instances'
      '\n\tInstructions: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AccessingInstancesLinux.html',
      filename=filename
    ))
