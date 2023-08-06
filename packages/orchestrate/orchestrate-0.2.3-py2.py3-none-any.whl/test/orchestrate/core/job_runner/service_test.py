import pytest
from mock import Mock

from orchestrate.core.job_runner.service import JobRunnerService

class TestJobRunnerService(object):
  @pytest.fixture
  def services(self):
    return Mock()

  @pytest.fixture
  def job_runner_service(self, services):
    return JobRunnerService(services)

  def test_job_name(self, job_runner_service):
    experiment_id = '234234'
    assert job_runner_service.experiment_id(job_runner_service.job_name(experiment_id)) == experiment_id

  def test_experiment_id(self, job_runner_service):
    job_name = 'orchestrate-o3u42-owskj'
    assert job_runner_service.job_name(job_runner_service.experiment_id(job_name)) == job_name

  def test_old_job_name(self, job_runner_service):
    job_name = 'galileo-o3u42-owskj'
    assert job_runner_service.experiment_id(job_name) is None
