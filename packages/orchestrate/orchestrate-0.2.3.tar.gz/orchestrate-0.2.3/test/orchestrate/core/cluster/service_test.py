import pytest
from mock import Mock

from orchestrate.core.cluster.service import (
  ClusterService,
  MultipleClustersConnectionError,
  NotConnectedError,
  PleaseDisconnectError,
)


class TestClusterService(object):
  @pytest.fixture
  def services(self):
    return Mock(
      aws_service=Mock(create_kubernetes_cluster=Mock(return_value=dict(name='foobar')))
    )

  @pytest.fixture
  def cluster_service(self, services):
    return ClusterService(services)

  def test_connected_clusters(self, cluster_service):
    cluster_service.services.kubectl_service.get_config_map.return_value = None
    assert cluster_service.connected_clusters() == []
    cluster_service.services.kubectl_service.get_config_map.return_value = []
    assert cluster_service.connected_clusters() == []
    cluster_service.services.kubectl_service.get_config_map.return_value = dict(foo=None)
    assert cluster_service.connected_clusters() == ['foo']
    cluster_service.services.kubectl_service.get_config_map.return_value = dict(foo=None, bar=None)
    assert sorted(cluster_service.connected_clusters()) == ['bar', 'foo']

  def test_multiple_clusters(self, cluster_service):
    cluster_service.connected_clusters = Mock(return_value=['bar', 'foo'])

    with pytest.raises(MultipleClustersConnectionError):
      cluster_service.assert_is_connected()
    with pytest.raises(MultipleClustersConnectionError):
      cluster_service.assert_is_disconnected()
    with pytest.raises(MultipleClustersConnectionError):
      cluster_service.connect(None)
    with pytest.raises(MultipleClustersConnectionError):
      cluster_service.create(None)
    with pytest.raises(MultipleClustersConnectionError):
      cluster_service.disconnect('bar', None)
    with pytest.raises(MultipleClustersConnectionError):
      cluster_service.test()

    cluster_service.disconnect(cluster_name=None, disconnect_all=True)

    # TODO(alexandra): decide which permissions to validate for cluster destroy
    cluster_service.destroy(None)

  def test_no_clusters(self, cluster_service):
    cluster_service.connected_clusters = Mock(return_value=[])

    with pytest.raises(NotConnectedError):
      cluster_service.assert_is_connected()
    with pytest.raises(NotConnectedError):
      cluster_service.disconnect('bar', None)
    with pytest.raises(NotConnectedError):
      cluster_service.disconnect(cluster_name=None, disconnect_all=True)
    with pytest.raises(NotConnectedError):
      cluster_service.test()

    cluster_service.assert_is_disconnected()
    cluster_service.test = Mock()
    cluster_service.connect('cluster_name')
    assert cluster_service.test.call_count == 1
    cluster_service.create(dict())

    # TODO(alexandra): decide which permissions to validate for cluster destroy
    cluster_service.destroy(None)

  def test_one_clusters(self, cluster_service):
    cluster_service.connected_clusters = Mock(return_value=['foo'])

    with pytest.raises(PleaseDisconnectError):
      cluster_service.assert_is_disconnected()
    with pytest.raises(PleaseDisconnectError):
      cluster_service.connect('bar')
    with pytest.raises(PleaseDisconnectError):
      cluster_service.create(dict(cluster_name='bar'))
    with pytest.raises(PleaseDisconnectError):
      cluster_service.disconnect('bar', None)

    cluster_service.assert_is_connected()
    cluster_service.connect('foo')
    cluster_service.create(dict(cluster_name='foo'))
    cluster_service.disconnect('foo', None)
    cluster_service.disconnect(cluster_name=None, disconnect_all=True)
    cluster_service.destroy('foo')
    cluster_service.test()

    # TODO(alexandra): decide which permissions to validate for cluster destroy
    cluster_service.destroy('bar')
