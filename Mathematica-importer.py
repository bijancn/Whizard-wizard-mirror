import ast
import numpy as np
from glob import glob


def convert_file(file_name):
  with open(file_name, 'r') as f:
    data = f.read().replace('\n', '')
  data = data.replace('{', '[').replace('}', ']')
  data = data.replace('*^', 'E')
  data = data.replace(' + 0.*I', '')
  mylist = ast.literal_eval(data)
  converted = []
  for x, y in mylist:
      converted.append((x, y * 1000))
  array = np.array(converted)
  np.savetxt(file_name.replace('.txt', '.dat'), array)


for file_name in glob('*.txt'):
  print 'Converting', file_name
  convert_file(file_name)
