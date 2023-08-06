from __future__ import print_function
import os
from tempfile import NamedTemporaryFile

from orchestrate.common import safe_format
from orchestrate.core.services.base import Service


class JobRunnerService(Service):
  def env_vars(self, experiment_id):
    return {
      'ORCHESTRATE_EXPERIMENT_ID': experiment_id,
      'SIGOPT_API_TOKEN': self.services.sigopt_service.api_token,
    }

  def render_job_spec_file(self, experiment_id, optimization_options, image_name, resources):
    parallel_bandwidth = optimization_options.get('parallel_bandwidth', 1)
    template_args = dict(
      environment_variables=[
        {'name': key, 'value': value}
        for key, value in self.env_vars(experiment_id).items()
      ],
      image_name=image_name,
      job_name=self.job_name(experiment_id),
      parallel_bandwidth=parallel_bandwidth,
      resources=resources,
    )

    return self.services.template_service.render_template_from_file(
      'job_runner/job-spec.yml.ms',
      template_args,
    )

  def job_name(self, experiment_id):
    return safe_format('orchestrate-{}', experiment_id)

  def experiment_id(self, job_name):
    if job_name.startswith('orchestrate-'):
      return job_name[len('orchestrate-'):]
    return None

  def create_sigopt_experiment(self, name, optimization_options):
    data = optimization_options.copy()
    data.pop('sigopt', dict())

    try:
      metadata = data.pop('metadata')
    except KeyError:
      metadata = dict()

    # Note: We could concatenate this string with a uuid to further reduce the possibility of collision
    if 'orchestrate_experiment' not in metadata:
      metadata['orchestrate_experiment'] = "True"

    experiment = self.services.sigopt_service.create_experiment(name=name, metadata=metadata, **data)
    return experiment.id

  def run_job(self, image_name, name, optimization_options, resource_options):
    resource_options = resource_options or {}
    gpu_count = resource_options.get('gpus', 0)

    self.services.kubectl_service.check_nodes_are_ready()

    resources = {'gpu_count': gpu_count} if gpu_count > 0 else False
    experiment_id = self.create_sigopt_experiment(name, optimization_options)
    rendered_job_spec = self.render_job_spec_file(
      experiment_id,
      optimization_options,
      image_name,
      resources,
    )

    with NamedTemporaryFile(mode='w', delete=False) as job_spec_file:
      job_spec_file.write(rendered_job_spec)

    try:
      self.services.kubectl_service.start_job(job_spec_file.name)
      return experiment_id
    finally:
      os.remove(job_spec_file.name)

  def run_local_job(self, image_name, name, optimization_options):
    experiment_id = self.create_sigopt_experiment(name, optimization_options)

    self.services.docker_service.run(
      image_name,
      env=self.env_vars(experiment_id),
    )

    return experiment_id
