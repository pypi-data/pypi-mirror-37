import pytest

from kubernetes import client
from mock import Mock, MagicMock

from orchestrate.core.kubernetes.service import KubernetesService, ORCHESTRATE_NAMESPACE

# pylint: disable=protected-access
class TestKubernetesService(object):
  @pytest.fixture()
  def kubernetes_service(self):
    services = Mock()
    return KubernetesService(services)

  def test_delete_job(self, kubernetes_service):
    kubernetes_service._v1_batch = Mock()
    kubernetes_service.delete_job('test_job_name')

    kubernetes_service._v1_batch.delete_namespaced_job.assert_called_with(
      'test_job_name',
      'default',
      client.V1DeleteOptions()
    )

  def test_get_jobs(self, kubernetes_service):
    kubernetes_service._v1_batch = Mock()
    kubernetes_service.get_jobs()

    kubernetes_service._v1_batch.list_namespaced_job.assert_called_with(
      ORCHESTRATE_NAMESPACE,
      watch=False
    )

  def test_get_jobs_with_job_name(self, kubernetes_service):
    kubernetes_service._v1_batch = MagicMock()
    kubernetes_service.get_jobs('test_job_name')

    kubernetes_service._v1_batch.list_namespaced_job.assert_called_with(
      ORCHESTRATE_NAMESPACE,
      watch=False,
      label_selector='job-name=test_job_name'
    )
# pylint: enable=protected-access
