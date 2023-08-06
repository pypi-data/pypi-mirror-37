from __future__ import print_function
import errno
import json
import os
import random
import subprocess
from tempfile import NamedTemporaryFile, TemporaryFile
import time

from orchestrate.common import safe_format
from orchestrate.core.exceptions import (
  MissingGpuNodesException,
  NodesNotReadyError,
  OrchestrateException,
)
from orchestrate.core.paths import ensure_dir, get_root_subdir
from orchestrate.core.services.base import Service


class NoNodesInClusterError(NodesNotReadyError):
  def __init__(self):
    super(NoNodesInClusterError, self).__init__(
      'Looks like your cluster does not have any nodes.'
      ' Please check that your cluster configuration file has defined either `cpu` or `gpu` nodes.'
      ' For AWS clusters, check that you see nodes on the EC2 console.'
    )


class NodeStatusNotReadyError(NodesNotReadyError):
  def __init__(self):
    super(NodeStatusNotReadyError, self).__init__(
      'Looks like some of your nodes have not reached the `Ready` status.'
      ' Run `sigopt kubectl get nodes` to see the status of your nodes.'
    )


class KubectlError(OrchestrateException):
  def __init__(self, args, return_code, stdout, stderr):
    super(KubectlError, self).__init__()
    self.args = args
    self.return_code = return_code
    self.stdout = stdout.read()
    self.stderr = stderr.read()

  def __str__(self):
    return safe_format(
      'kubectl command {} failed with exit status {}\n'
      'stdout:\n{}\nstderr:\n{}',
      self.args,
      self.return_code,
      self.stdout,
      self.stderr,
    )

class KubectlService(Service):
  kubectl_command = 'kubectl'

  def __init__(self, services):
    super(KubectlService, self).__init__(services)
    self.kube_config = None

  # Note: we leave the error handling for orchestrate cluster test. If we caught errors here,
  # then we would never be able to use the CLI to cleanup "invalid" states.
  def warmup(self):
    kube_configs = self.get_configs()
    if kube_configs:
      self.kube_config = os.path.join(self.kubectl_directory, kube_configs[0])

  def kubectl_pargs(self, args, decode_json):
    pargs = [self.kubectl_command] + args
    if decode_json:
      pargs += ['-o', 'json']
    return pargs

  def kubectl_env(self):
    assert self.kube_config, "The kubectl service has no kubernetes config"
    env = os.environ.copy()
    env.update(dict(
      KUBECONFIG=self.kube_config,
      PATH=safe_format(
        '{}:{}',
        os.path.expanduser('~/.orchestrate/bin'),
        env.get('PATH', ''),
      ).encode(),
    ))
    return env

  def kubectl(self, args, decode_json):
    pargs = self.kubectl_pargs(args, decode_json)
    env = self.kubectl_env()
    with TemporaryFile('w+') as stdout, TemporaryFile('w+') as stderr:
      ps = subprocess.Popen(pargs, env=env, stdout=stdout, stderr=stderr)
      exit_status = ps.wait()
      stdout.seek(0)
      stderr.seek(0)
      if exit_status != 0:
        raise KubectlError(args, exit_status, stdout, stderr)

      if decode_json:
        return json.load(stdout)
      else:
        return stdout.read()

  def kubectl_get(self, args):
    return self.kubectl(['get'] + args, decode_json=True)

  def _ensure_plugin(self, plugin):
    with self.services.resource_service.open('plugins', plugin) as plugin_fp:
      try:
        self.create(plugin_fp.name)
      except KubectlError:
        pass

  def ensure_plugins(self):
    self._ensure_plugin('nvidia-device-plugin.yml')

  def get_pods(self, job_name=None):
    if job_name:
      return self.kubectl_get(['pods', '--selector', safe_format('job-name={}', job_name)])
    else:
      return self.kubectl_get(['pods'])

  def get_nodes(self):
    return self.kubectl_get(['nodes'])

  # TODO(alexandra): https://kubernetes-v1-4.github.io/docs/user-guide/kubectl/kubectl_apply/
  # use `kubectl apply -f -` and stream the config from stdin
  def apply(self, yml_string):
    with NamedTemporaryFile(mode='w', delete=False) as f:
      f.write(yml_string)

    result = self.kubectl(['apply', '-f', f.name], decode_json=False)
    os.remove(f.name)
    return result

  def create(self, yml):
    return self.kubectl(['create', '-f', yml], decode_json=False)

  # TODO(alexandra): control how logs are displayed, should this be sent to stdout by subprocess or by the CLI?
  def logs(self, pod_name):
    return self.kubectl(['logs', pod_name], decode_json=False)

  def pod_names(self, job_name):
    data = self.get_pods(job_name=job_name)
    return [item['metadata']['name'] for item in data['items']]

  def start_job(self, yml):
    return self.create(yml)

  def check_nodes_are_ready(self):
    nodes = self.get_nodes()['items'] or []
    if not nodes:
      raise NoNodesInClusterError()

    for node in nodes:
      status = dict(((c['type'], (c['status'] == 'True')) for c in node['status']['conditions']))
      if not status['Ready']:
        raise NodeStatusNotReadyError()

  def wait_until_nodes_are_ready(self, retries=20):
    for try_number in range(retries + 1):
      try:
        self.check_nodes_are_ready()
        return
      except NodesNotReadyError:
        if try_number >= retries:
          raise
        else:
          time.sleep(random.uniform(20, 40))

  def check_gpu_nodes(self, num_gpus):
    nodes = self.get_nodes()['items']
    for node in nodes:
      gpus = int(node['status']['capacity'].get('nvidia.com/gpu', '0'))
      if gpus >= num_gpus:
        return
    raise MissingGpuNodesException(safe_format(
      "No nodes are available with {}, you might need to add some to your cluster",
      safe_format('{} GPUs', num_gpus) if num_gpus > 1 else 'GPUs',
    ))

  @property
  def kubectl_directory(self):
    return get_root_subdir('cluster')

  def ensure_kubectl_directory(self):
    ensure_dir(self.kubectl_directory)

  def kube_config_location(self, cluster_name):
    filename = safe_format('config-{}', cluster_name)
    return os.path.join(self.kubectl_directory, filename)

  def is_config_name(self, config_name):
    return config_name.startswith('config-')

  def cluster_name_from_config(self, config_name):
    basename = os.path.basename(config_name)
    if self.is_config_name(basename):
      return basename[len('config-'):]
    else:
      return None

  def get_configs(self):
    if os.path.exists(self.kubectl_directory):
      return [
        config
        for config
        in os.listdir(self.kubectl_directory)
        if self.is_config_name(config)
      ]
    return []

  def get_config_map(self):
    configs = self.get_configs()
    return dict((self.cluster_name_from_config(c), c) for c in configs)

  def write_config(self, cluster_name, string):
    self.ensure_kubectl_directory()
    filename = self.kube_config_location(cluster_name)
    if os.path.isfile(filename):
      raise Exception(safe_format(
        "Looks like the file: {filename} currently exists on your system,"
        " please delete this file or choose another cluster name",
        filename=filename
      ))

    with open(filename, 'w') as f:
      f.write(string)

    self.kube_config = filename

  def delete_config(self, cluster_name):
    self.kube_config = None
    os.remove(self.kube_config_location(cluster_name))

  def ensure_config_deleted(self, cluster_name):
    try:
      self.delete_config(cluster_name)
    except OSError as e:
      if e.errno != errno.ENOENT:
        raise

  def test_config(self, retries=0, wait_time=5):
    for try_number in range(retries + 1):
      try:
        return self.kubectl_get(['svc'])
      except KubectlError:
        if try_number >= retries:
          raise
        else:
          time.sleep(wait_time)
