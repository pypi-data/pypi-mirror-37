import errno
import hashlib
import os
from six import raise_from
from six.moves import urllib
import subprocess

from orchestrate.common import get_for_platform, safe_format
from orchestrate.core.exceptions import CheckExecutableError

def get_root_dir():
  return os.path.expanduser('~/.orchestrate')

def get_root_subdir(dirname):
  return os.path.join(get_root_dir(), dirname)

def get_bin_dir():
  return get_root_subdir('bin')

def ensure_dir(path):
  try:
    os.makedirs(path)
  except os.error as oserr:
    if oserr.errno != errno.EEXIST:
      raise

def get_executable_path(command):
  return os.path.join(get_bin_dir(), command)

def check_executable(command, sha256, full_check):
  exec_path = get_executable_path(command)
  try:
    if full_check:
      with open(exec_path, 'rb') as exec_fp:
        contents = exec_fp.read()
      file_sha256 = hashlib.sha256(contents).hexdigest()
    else:
      with open(safe_format('{}.sha256', exec_path), 'r') as exec_sha256_fp:
        file_sha256 = exec_sha256_fp.read()
  except IOError as e:
    if e.errno == errno.ENOENT:
      raise_from(
        CheckExecutableError(safe_format('Error opening the hash files for: {}', command)),
        e,
      )
    raise

  if not sha256 == file_sha256:
    raise CheckExecutableError(safe_format(
      "the {} for '{}' does not have the expected hash",
      'executable' if full_check else 'hash file',
      command,
    ))

  if not os.access(exec_path, os.X_OK):
    raise CheckExecutableError(safe_format("the file for '{}' is not executable", command))

  if full_check:
    with open(os.devnull, 'w') as devnull:
      try:
        subprocess.check_call([exec_path], stdout=devnull, stderr=devnull)
        subprocess.check_call(
          [command],
          env={'PATH': get_bin_dir()},
          stdout=devnull,
          stderr=devnull,
        )
      except subprocess.CalledProcessError as e:
        raise_from(
          CheckExecutableError(safe_format('Exception checking the excecutable for {}: {}', command,  str(e))),
          e,
        )
      except OSError as e:
        if e.errno == errno.ENOENT:
          raise_from(
            CheckExecutableError(safe_format('System cannot find executable for {}', command)),
            e,
          )
        raise


KUBECTL_VERSION = 'v1.11.2'
KUBECTL_URL_FORMAT = 'https://storage.googleapis.com/kubernetes-release/release/{}/bin/{}/amd64/kubectl'
KUBECTL_SHA256_LINUX = 'b9f6bf64706a0ca5f1ebb9977fc7dd155b19881985a6b116a65db5f361fbc703'
KUBECTL_SHA256_MAC = '00982098dff8781b5837dcb15b6b1c5c8f8c3a3783ecb3f2d7300e176157e4d5'

AWS_IAM_AUTHENTICATOR_URL_FORMAT = (
  'https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-07-26/bin/{}/amd64/aws-iam-authenticator'
)
AWS_IAM_AUTHENTICATOR_SHA256_LINUX = '246f6d13b051bbfb12962edca074c8f67436930e84b2bec3a45a5d9242dc6f0c'
AWS_IAM_AUTHENTICATOR_SHA256_MAC = '1bc1dcd4afe33a4c0f5198b41aacd660623a43501e109f7ca85292258d8919d4'

def check_kubectl_executable(full_check=False):
  check_executable(
    command='kubectl',
    sha256=get_for_platform(
      linux_option=KUBECTL_SHA256_LINUX,
      mac_option=KUBECTL_SHA256_MAC,
    ),
    full_check=full_check,
  )

def check_iam_authenticator_executable(full_check=False):
  check_executable(
    command='aws-iam-authenticator',
    sha256=get_for_platform(
      linux_option=AWS_IAM_AUTHENTICATOR_SHA256_LINUX,
      mac_option=AWS_IAM_AUTHENTICATOR_SHA256_MAC,
    ),
    full_check=full_check,
  )

def download_executable(command, url):
  executable_path = get_executable_path(command)
  urllib.request.urlretrieve(url, executable_path)
  os.chmod(executable_path, 0o755)
  with \
    open(executable_path, 'rb') as exec_fp, \
    open(safe_format('{}.sha256', executable_path), 'w') as sha256_fp:
    sha256_fp.write(hashlib.sha256(exec_fp.read()).hexdigest())

def download_kubectl_executable():
  download_executable('kubectl', safe_format(
    KUBECTL_URL_FORMAT,
    KUBECTL_VERSION,
    get_for_platform(
      linux_option='linux',
      mac_option='darwin',
    ),
  ))

def download_iam_authenticator_executable():
  download_executable('aws-iam-authenticator', safe_format(
    AWS_IAM_AUTHENTICATOR_URL_FORMAT,
    get_for_platform(
      linux_option='linux',
      mac_option='darwin',
    ),
  ))
