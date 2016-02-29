import os

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
