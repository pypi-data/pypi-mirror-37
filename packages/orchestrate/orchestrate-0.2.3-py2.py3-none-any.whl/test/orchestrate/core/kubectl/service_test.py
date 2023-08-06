import pytest
from mock import Mock, patch

from orchestrate.core.kubectl.service import KubectlError, KubectlService
from orchestrate.core.exceptions import NodesNotReadyError

DUMMY_RETURN_VALUE = object()


class TestKubectlService(object):
  @pytest.fixture()
  def kubectl_service(self):
    services = Mock()
    return KubectlService(services)

  def mock_popen(self, return_code, out_msg, err_msg=None):

    def popen(*args, **kwargs):
      stdout = kwargs.pop('stdout')
      stdout.write(out_msg)
      if err_msg:
        stderr = kwargs.pop('stderr')
        stderr.write(err_msg)
      return Mock(wait=Mock(return_value=return_code))

    return Mock(side_effect=popen)

  def test_kubectl(self, kubectl_service):
    kubectl_service.kube_config = 'test_config'
    with patch('orchestrate.core.kubectl.service.subprocess') as mock_subprocess:
      mock_subprocess.Popen = self.mock_popen(0, 'DUMMY_RETURN_VALUE')
      assert kubectl_service.kubectl(['foo'], decode_json=False) == 'DUMMY_RETURN_VALUE'
      assert mock_subprocess.Popen.call_args[0][0] == ['kubectl', 'foo']

  def test_kubectl_json(self, kubectl_service):
    kubectl_service.kube_config = 'test_config'
    with patch('orchestrate.core.kubectl.service.subprocess') as mock_subprocess:
      mock_subprocess.Popen = self.mock_popen(0, '{"foo": "bar"}')
      assert kubectl_service.kubectl(['foo'], decode_json=True) == dict(foo='bar')
      assert mock_subprocess.Popen.call_args[0][0] == ['kubectl', 'foo', '-o', 'json']

  def test_kubectl_error(self, kubectl_service):
    kubectl_service.kube_config = 'test_config'
    with patch('orchestrate.core.kubectl.service.subprocess') as mock_subprocess:
      return_code = 1
      out_msg = "Test kubectl output"
      err_msg = "Test kubectl error"
      mock_subprocess.Popen = self.mock_popen(return_code, out_msg, err_msg)
      with pytest.raises(KubectlError) as excinfo:
        kubectl_service.kubectl(['foo'], decode_json=False)
      assert excinfo.value.return_code == return_code
      assert excinfo.value.stdout == out_msg
      assert excinfo.value.stderr == err_msg

  def test_kubectl_get(self, kubectl_service):
    kubectl_service.kube_config = 'test_config'
    kubectl_service.kubectl = Mock(return_value=DUMMY_RETURN_VALUE)
    assert kubectl_service.kubectl_get(['foo', 'bar']) == DUMMY_RETURN_VALUE
    kubectl_service.kubectl.assert_called_with(['get', 'foo', 'bar'], decode_json=True)

  def test_get_pods(self, kubectl_service):
    kubectl_service.kubectl_get = Mock(return_value=DUMMY_RETURN_VALUE)
    assert kubectl_service.get_pods() == DUMMY_RETURN_VALUE
    kubectl_service.kubectl_get.assert_called_with(['pods'])

  def test_get_pods_with_job_name(self, kubectl_service):
    kubectl_service.kubectl_get = Mock(return_value=DUMMY_RETURN_VALUE)
    assert kubectl_service.get_pods('foobar') == DUMMY_RETURN_VALUE
    kubectl_service.kubectl_get.assert_called_with(['pods', '--selector', 'job-name=foobar'])

  def test_get_nodes(self, kubectl_service):
    kubectl_service.kubectl_get = Mock(return_value=DUMMY_RETURN_VALUE)
    assert kubectl_service.get_nodes() == DUMMY_RETURN_VALUE
    kubectl_service.kubectl_get.assert_called_with(['nodes'])

  def test_logs(self, kubectl_service):
    kubectl_service.kubectl = Mock(return_value=DUMMY_RETURN_VALUE)
    assert kubectl_service.logs('foobar') == DUMMY_RETURN_VALUE
    kubectl_service.kubectl.assert_called_with(['logs', 'foobar'], decode_json=False)

  def test_pod_names(self, kubectl_service):
    kubectl_service.get_pods = Mock(return_value=dict(
      items=[
        dict(
          metadata=dict(
            name='foo',
          ),
        ),
        dict(
          metadata=dict(
            name='bar',
          ),
        ),
      ],
    ))

    assert sorted(kubectl_service.pod_names('baz')) == ['bar', 'foo']
    kubectl_service.get_pods.assert_called_with(job_name='baz')

  def test_start_job(self, kubectl_service):
    kubectl_service.kubectl = Mock(return_value=DUMMY_RETURN_VALUE)
    assert kubectl_service.start_job('foobar') == DUMMY_RETURN_VALUE
    kubectl_service.kubectl.assert_called_with(['create', '-f', 'foobar'], decode_json=False)

  def test_check_nodes_are_ready(self, kubectl_service):
    kubectl_service.get_nodes = Mock(return_value=dict(
      items=[
        dict(
          status=dict(
            conditions=[
              dict(type='Ready', status='True'),
              dict(type='foobar', status='True'),
            ],
          ),
        ),
        dict(
          status=dict(
            conditions=[
              dict(type='Ready', status='True'),
              dict(type='foobar', status='False'),
            ],
          ),
        ),
      ],
    ))
    kubectl_service.check_nodes_are_ready()

  def test_check_nodes_are_not_ready_status(self, kubectl_service):
    kubectl_service.get_nodes = Mock(return_value=dict(
      items=[
        dict(
          status=dict(
            conditions=[
              dict(type='Ready', status='True'),
              dict(type='foobar', status='True'),
            ],
          ),
        ),
        dict(
          status=dict(
            conditions=[
              dict(type='Ready', status='False'),
              dict(type='foobar', status='True'),
            ],
          ),
        ),
      ],
    ))
    with pytest.raises(NodesNotReadyError):
      kubectl_service.check_nodes_are_ready()

  def test_check_nodes_are_not_ready_no_nodes(self, kubectl_service):
    kubectl_service.get_nodes = Mock(return_value=dict(
      items=[],
    ))
    with pytest.raises(NodesNotReadyError):
      kubectl_service.check_nodes_are_ready()

  def test_wait_until_nodes_are_ready(self, kubectl_service):
    with patch('orchestrate.core.kubectl.service.time') as mock_time:
      kubectl_service.check_nodes_are_ready = Mock(side_effect=[
        NodesNotReadyError(),
        NodesNotReadyError(),
        NodesNotReadyError(),
        None,
        None,
      ])
      kubectl_service.wait_until_nodes_are_ready()
      assert kubectl_service.check_nodes_are_ready.call_count == 4
      assert mock_time.sleep.called
