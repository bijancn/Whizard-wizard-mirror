import logging
import os
import re
import sys
import shutil
import tempfile
import json

def setup_logger():
  logPath = os.getcwd()
  logName = 'default'
  logFormatter = logging.Formatter('%(asctime)s ' + \
      '[%(levelname)-5.5s]  %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
  rootLogger = logging.getLogger()
  fileHandler = logging.FileHandler('{0}/{1}.log'.format(logPath, logName))
  fileHandler.setFormatter(logFormatter)
  rootLogger.addHandler(fileHandler)
  rootLogger.setLevel(logging.INFO)
  consoleHandler = logging.StreamHandler()
  consoleHandler.setFormatter(logFormatter)
  rootLogger.addHandler(consoleHandler)
  logger = logging.getLogger(__name__)
  return logger

# try:
  # logger = logging.getLogger(__name__)
# except:
logger = setup_logger()

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

def sed(original, replace_line=None, new_file=None, write_to_top='', write_to_bottom=''):
  overwrite = new_file == None
  tmp_fh, tmp_file = tempfile.mkstemp()
  with open(tmp_file, 'w') as new_f:
    with open(original) as old_f:
      new_f.write(write_to_top)
      for line in old_f:
        if replace_line is not None:
          new_f.write(replace_line(line))
        else:
          new_f.write(line)
      new_f.write(write_to_bottom)
  os.close(tmp_fh)
  if overwrite:
    target = original
  else:
    target = new_file
  remove(target)
  shutil.move(tmp_file, target)

def grep(pattern, filename):
  try:
   file = open(filename, "r")
  except IOError:
    return False
  for line in file:
    if re.search(pattern, line):
      return True
  return False

def load_json(json_file):
  try:
    with open(json_file) as f:
      return json.load(f)
  except IOError:
    fatal('json not found: ' + json_file )
  except ValueError:
    fatal('json seems invalid. Check it on http://jsonlint.com/')
