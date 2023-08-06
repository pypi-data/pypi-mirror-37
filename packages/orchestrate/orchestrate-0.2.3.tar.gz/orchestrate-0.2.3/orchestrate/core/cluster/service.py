import six


from orchestrate.common import safe_format
from orchestrate.core.exceptions import OrchestrateException
from orchestrate.core.services.base import Service


class ClusterError(OrchestrateException):
  pass


class MultipleClustersConnectionError(ClusterError):
  def __init__(self, connected_clusters):
    super(MultipleClustersConnectionError, self).__init__(
      safe_format(
        "You are currently connected to more than one cluster, all of which are listed below."
        "\nPlease disconnect from some of these clusters before re-running your command."
        "\nConnected clusters:"
        ":\n\t{}",
        "\n\t".join(connected_clusters),
      )
    )


class PleaseDisconnectError(ClusterError):
  def __init__(self, current_cluster_name):
    super(PleaseDisconnectError, self).__init__(
      safe_format("Please disconnect from this cluster before re-running your command: {}", current_cluster_name)
    )
    self.current_cluster_name = current_cluster_name


class NotConnectedError(ClusterError):
  def __init__(self):
    super(NotConnectedError, self).__init__("You are not currently connected to any cluster")

class ClusterService(Service):
  def connected_clusters(self):
    config_map = self.services.kubectl_service.get_config_map()
    return [] if not config_map else list(config_map.keys())

  def assert_is_connected(self):
    connected_clusters = self.connected_clusters()
    if not connected_clusters:
      raise NotConnectedError()
    elif len(connected_clusters) > 1:
      raise MultipleClustersConnectionError(connected_clusters)
    return connected_clusters[0]

  def assert_is_disconnected(self):
    connected_clusters = self.connected_clusters()
    if connected_clusters:
      if len(connected_clusters) == 1:
        raise PleaseDisconnectError(connected_clusters[0])
      else:
        raise MultipleClustersConnectionError(connected_clusters)

  def connect(self, cluster_name):
    try:
      self.assert_is_disconnected()
    except PleaseDisconnectError as e:
      if e.current_cluster_name != cluster_name:
        raise

    self.services.aws_service.connect_kubernetes_cluster(cluster_name=cluster_name)
    self.test()

  def create(self, options):
    try:
      self.assert_is_disconnected()
    except PleaseDisconnectError as e:
      if e.current_cluster_name != options['cluster_name']:
        raise

    self.services.options_validator_service.validate_cluster_options(**options)

    try:
      cluster = self.services.aws_service.create_kubernetes_cluster(options)
      self.services.kubectl_service.wait_until_nodes_are_ready()
      return cluster['name']
    except Exception as e:
      try:
        self.services.aws_service.disconnect_kubernetes_cluster(options['cluster_name'])
      except Exception:
        pass
      six.raise_from(
        ClusterError(safe_format(
          "Cluster create error: {}\n"
          "Resolve the issue and recreate your cluster.",
          str(e),
        )),
        e,
      )

  def destroy(self, cluster_name):
    self.services.aws_service.destroy_kubernetes_cluster(cluster_name=cluster_name)

  def disconnect(self, cluster_name, disconnect_all):
    if (cluster_name and disconnect_all) or (not cluster_name and not disconnect_all):
      raise ClusterError('Must provide exactly one of --cluster-name <cluster_name> and --all')

    try:
      current_cluster_name = self.assert_is_connected()
      if cluster_name is not None and current_cluster_name != cluster_name:
        raise PleaseDisconnectError(current_cluster_name)
    except MultipleClustersConnectionError:
      if not disconnect_all:
        raise

    for cname in self.connected_clusters():
      try:
        self.services.aws_service.disconnect_kubernetes_cluster(cluster_name=cname)
      except Exception as e:
        six.raise_from(ClusterError(safe_format(
          'Looks like an error occured while attempting to disconnect from cluster "{}".',
          cname,
        )), e)

  def test(self):
    cluster_name = self.assert_is_connected()
    self.services.aws_service.describe_cluster(cluster_name)
    self.services.aws_service.test_cluster_access_role(cluster_name)
    self.services.aws_service.test_kubernetes_cluster()
    return cluster_name
