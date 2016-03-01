import logging
import os
import sys
import shutil
import tempfile

logger = logging.getLogger(__name__)

class cd:
  """Context manager for changing the current working directory"""
  def __init__(self, newPath):
    self.newPath = newPath

  def __enter__(self):
    self.savedPath = os.getcwd()
    os.chdir(self.newPath)

  def __exit__(self, etype, value, traceback):
    os.chdir(self.savedPath)

def remove(filename):
  if (os.path.isfile (filename)):
    os.remove (filename)

def mkdirs(directory):
  if not os.path.exists(directory):
    os.makedirs(directory)

def fatal(message):
  logger.fatal('>>> ' + message + ' <<<')
  sys.exit(1)

def sed(original, replace_line, new_file=None, write_to_top=''):
  overwrite = new_file == None
  tmp_fh, tmp_file = tempfile.mkstemp()
  with open(tmp_file, 'w') as new_f:
    with open(original) as old_f:
      new_f.write(write_to_top)
      for line in old_f:
        new_f.write(replace_line(line))
  os.close(tmp_fh)
  if overwrite:
    target = original
  else:
    target = new_file
  remove(target)
  shutil.move(tmp_file, target)
