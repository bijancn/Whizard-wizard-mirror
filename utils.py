import logging
import os
import re
import shutil
import tempfile
import json

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

# These are the sequences need to get colored ouput
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"


def formatter_message(message, use_color=True):
    if use_color:
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message

COLORS = {
    'WARNING': YELLOW,
    'INFO': BLACK,
    'DEBUG': BLUE,
    'CRITICAL': RED,
    'ERROR': RED
}


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            color = COLOR_SEQ % (30 + COLORS[levelname])
            levelname_color = color + levelname + RESET_SEQ
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)


def setup_logger(verbose=False):
  logPath = os.getcwd()
  logName = 'default'
  log_fmt = '[%(asctime)-20s][%(levelname)-10s] %(message)s '  # + \
  # '($BOLD%(filename)s$RESET:%(lineno)d)' # this always leads to utils
  date_fmt = '%Y-%m-%d %H:%M:%S'
  logFormatter = logging.Formatter(formatter_message(log_fmt, False),
      datefmt=date_fmt)
  rootLogger = logging.getLogger()
  fileHandler = logging.FileHandler('{0}/{1}.log'.format(logPath, logName))
  fileHandler.setFormatter(logFormatter)
  rootLogger.addHandler(fileHandler)
  rootLogger.setLevel(logging.INFO)
  consoleHandler = logging.StreamHandler()
  consoleHandler.setFormatter(ColoredFormatter(formatter_message(log_fmt)))
  if verbose:
    consoleHandler.setLevel(logging.INFO)
  else:
    consoleHandler.setLevel(logging.WARNING)
  rootLogger.addHandler(consoleHandler)
  logger = logging.getLogger(__name__)
  return logger


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
  if (os.path.isfile(filename)):
    os.remove(filename)


def mkdirs(directory):
  if not os.path.exists(directory):
    os.makedirs(directory)


def fatal(message):
  logger.fatal('>>> ' + message + ' <<<')


def sed(original, replace_line=None, new_file=None, write_to_top='', write_to_bottom=''):
  overwrite = new_file is None
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


def get_number(keyword, filename):
  return int(get_value("(" + keyword + ") *= *([0-9]*)" , filename))


def get_logical(keyword, filename):
  return get_value("(" + keyword + " *= *)(true|false)", filename)


def get_string(keyword, filename):
  return get_value("(" + keyword + " *= *)(.*$)", filename)


def get_process(filename):
  return get_value("(process +)(\w+)", filename)


def get_scale(filename):
  return get_value("(scale *= *)(.*$)", filename)


def test_get():
  from nose.tools import eq_
  filename = 'test'
  test = open(filename, "w")
  test.write("?combined_integration  =   true ")
  test.write("foo =  false ")
  test.write(" int bar =  123 ")
  test.close()
  eq_(get_logical("\?combined_integration", filename), 'true')
  eq_(get_logical("foo", filename), 'false')
  eq_(get_number("bar", filename), 123)
  os.remove(filename)


def get_value(pattern, filename):
  try:
   file = open(filename, "r")
  except IOError:
    return None
  for line in file:
    m = re.search(pattern, line)
    if m:
      return m.group(2)
  return None


def load_json(json_file):
  try:
    with open(json_file) as f:
      return json.load(f)
  except IOError:
    fatal('json not found: ' + json_file)
  except ValueError:
    fatal('json seems invalid. Check it on http://jsonlint.com/')
