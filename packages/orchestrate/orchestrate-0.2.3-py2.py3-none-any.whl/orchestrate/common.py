from shutil import rmtree
import six
import sys
from tempfile import mkdtemp

class TemporaryDirectory(object):
  def __init__(self, *args, **kwargs):
    self.directory = mkdtemp(*args, **kwargs)

  def __enter__(self):
    return self.directory

  def __exit__(self, *args):
    rmtree(self.directory)

def safe_format(string, *args, **kwargs):
  return six.text_type(string).format(*args, **kwargs)

def get_for_platform(linux_option=None, mac_option=None):
  if sys.platform.startswith('linux'):
    return linux_option
  else:
    assert sys.platform == "darwin", "Only Mac and Linux systems are currently supported"
    return mac_option
