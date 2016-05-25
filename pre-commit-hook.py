#!/usr/bin/env python
# Install me with `ln -s ../../pre-commit-hook.py .git/hooks/pre-commit`

import os
import re
import subprocess
import sys
from termcolor import colored

modified = re.compile('^(?:M|A)(\s+)(?P<name>.*)')

CHECKS = [
    {
        'output': 'Checking for debugging statements...',
        'command': 'grep -n -i \'# debugging$\' %s',
        'match_files': ['.*\.py$'],
        'ignore_files': ['pre-commit-hook.py'],
        'print_filename': True,
    },
    {
        'output': 'Checking for active processes in run.jsons...',
        'command': 'grep -n \'\"disabled\": false\' %s',
        'print_filename': True,
    },
    {
        'output': 'Running Pyflakes...',
        'command': 'pyflakes %s',
        'match_files': ['.*\.py$'],
        'ignore_files': ['ee_WbWb/rivet/site_init.py'],
        'print_filename': False,
    },
    {
        'output': 'Running pep8...',
        'command': 'pep8 --max-line-length=89 %s',
        'ignore_files': ['mpi4py_map.py'],
        'match_files': ['.*\.py$'],
        'print_filename': False,
    },
]


def matches_file(file_name, match_files):
  return any(re.compile(match_file).match(file_name) for
      match_file in match_files)


def check_files(files, check):
  result = 0
  print check['output']
  for file_name in files:
    if 'match_files' not in check or matches_file(file_name,
        check['match_files']):
      if 'ignore_files' not in check or not matches_file(file_name,
          check['ignore_files']):
        process = subprocess.Popen(check['command'] % file_name,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = process.communicate()
        if out or err:
          if check['print_filename']:
            prefix = '\t%s:' % file_name
          else:
            prefix = '\t'
          output_lines = ['%s%s' % (prefix, line) for line in out.splitlines()]
          if 'grep' not in check['command']:
            print '\n'.join(output_lines)
          else:
            print colored('\n'.join(output_lines), 'red')
          if err:
            print colored(err, 'red')
          result = 1
  return result


def main(all_files, syntax_only):
    # Stash any changes to the working tree that are not going to be committed
    subprocess.call(['git', 'stash', '-q', '--keep-index'],
        stdout=subprocess.PIPE)

    files = []
    if all_files:
        for root, dirs, file_names in os.walk('.'):
            for file_name in file_names:
                files.append(os.path.join(root, file_name))
    else:
        p = subprocess.Popen(['git', 'status', '--porcelain'],
            stdout=subprocess.PIPE)
        out, err = p.communicate()
        for line in out.splitlines():
            match = modified.match(line)
            if match:
                files.append(match.group('name'))

    result = 0

    print 'files to be checked =    ', files
    for check in CHECKS:
      result = check_files(files, check) or result

    if (not syntax_only):
      print 'Running Test Suite...'
      return_code = subprocess.call('./run_tests.sh', shell=True)
      result = return_code or result

    # Unstash changes to the working tree that we had stashed
    subprocess.call(['git', 'stash', 'pop', '-q'], stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    if result != 0:
      print colored('Commit cannot be accepted. See errors above.', 'red')
    sys.exit(result)

if __name__ == '__main__':
    all_files = False
    syntax_only = False
    if len(sys.argv) > 1 and sys.argv[1] == '--all-files':
        all_files = True
    if len(sys.argv) > 1 and sys.argv[1] == '--syntax-only':
        syntax_only = True
    main(all_files, syntax_only)
