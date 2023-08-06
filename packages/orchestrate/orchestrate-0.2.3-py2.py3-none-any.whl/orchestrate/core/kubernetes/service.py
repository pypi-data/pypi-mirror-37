from kubernetes import client, config
import os

from orchestrate.common import safe_format
from orchestrate.core.exceptions import OrchestrateException
from orchestrate.core.paths import get_root_subdir
from orchestrate.core.services.base import Service

ORCHESTRATE_NAMESPACE = 'default'

class KubernetesException(OrchestrateException):
  pass

class JobNotFoundException(KubernetesException):
  pass

class KubernetesService(Service):
  def __init__(self, services):
    super(KubernetesService, self).__init__(services)
    self._kube_config = None
    self._v1_core = None
    self._v1_batch = None

  def warmup(self):
    kube_configs = self._get_config_files()
    if kube_configs:
      self._kube_config = os.path.join(self._get_kubectl_directory(), kube_configs[0])
      config.load_kube_config(self._kube_config)
    self._v1_core = client.CoreV1Api()
    self._v1_batch = client.BatchV1Api()

  def delete_job(self, job_name):
    try:
      self._v1_batch.delete_namespaced_job(job_name, ORCHESTRATE_NAMESPACE, client.V1DeleteOptions())
    except client.rest.ApiException as e:
      if e.status == 404:
        raise JobNotFoundException(safe_format('Job with name {} not found', job_name))
      else:
        raise e

  def get_jobs(self, job_name=None):
    if job_name:
      return self._v1_batch.list_namespaced_job(
        ORCHESTRATE_NAMESPACE,
        watch=False,
        label_selector=safe_format('job-name={}', job_name)
      ).items[0]
    else:
      return self._v1_batch.list_namespaced_job(ORCHESTRATE_NAMESPACE, watch=False)

  def _get_kubectl_directory(self):
    return get_root_subdir('cluster')

  def _get_config_files(self):
    if os.path.exists(self._get_kubectl_directory()):
      return [
        config
        for config
        in os.listdir(self._get_kubectl_directory())
        if config.startswith('config-')
      ]
    return []
