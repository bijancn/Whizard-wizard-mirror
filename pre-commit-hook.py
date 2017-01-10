#!/usr/bin/env python
# Install me with `ln -s ../../pre-commit-hook.py .git/hooks/pre-commit`
# Runs tests before each commit

import os
import re
import subprocess
import sys
import time
from termcolor import colored

modified = re.compile('^(?:M|A)(\s+)(?P<name>.*)')

EXTRA_COMMANDS = [
    "cp plot-schema.json ~/www/docson",
    "cp run-schema.json ~/www/docson"
]

CHECKS = [
    {
        'output': 'Checking for debugging statements...',
        'command': 'grep -n -i \'# debugging$\' %s',
        'match_files': ['.*\.py$'],
        'print_filename': True,
    },
    {
        'output': 'Checking for active processes in run.jsons...',
        'command': 'grep -n \'\"disabled\": false\' %s',
        'print_filename': True,
    },
    {
        'output': 'Running flake8...',
        'command': 'flake8 --max-line-length=89 %s',
        'match_files': ['.*\.py$'],
        'ignore_files': ['mpi4py_map.py'],
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


def stash_working_tree():
  new_stash = subprocess.Popen(['git', 'rev-parse', '-q', '--verify', 'refs/stash'],
    stdout=subprocess.PIPE).stdout.read()
  subprocess.call(['git', 'stash', 'save', '-q', '--keep-index'],
      stdout=subprocess.PIPE)
  old_stash = subprocess.Popen(['git', 'rev-parse', '-q', '--verify', 'refs/stash'],
    stdout=subprocess.PIPE).stdout.read()
  print 'old stash:', old_stash
  print 'new stash:', new_stash
  if new_stash == old_stash:
    print 'No changes to test'
    time.sleep(1)
    sys.exit(0)


def files_to_be_checked():
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
  print 'files to be checked =    ', files
  return files


def main(all_files, syntax_only):
  stash_working_tree()
  files = files_to_be_checked()
  result = 0
  for command in EXTRA_COMMANDS:
    process = subprocess.Popen(command,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = process.communicate()
  for check in CHECKS:
    result = check_files(files, check) or result
  if (not syntax_only):
    print 'Running Test Suite...'
    return_code = subprocess.call('./run_tests.sh', shell=True)
    result = return_code or result
  unstash_working_tree()
  if result != 0:
    print colored('Commit cannot be accepted. See errors above.', 'red')
  sys.exit(result)


def unstash_working_tree():
  subprocess.call(['git', 'reset', '--hard', '-q'], stdout=subprocess.PIPE,
      stderr=subprocess.PIPE)
  subprocess.call(['git', 'stash', 'apply', '--index', '-q'], stdout=subprocess.PIPE,
      stderr=subprocess.PIPE)
  subprocess.call(['git', 'stash', 'drop', '-q'], stdout=subprocess.PIPE,
      stderr=subprocess.PIPE)

if __name__ == '__main__':
    all_files = False
    syntax_only = False
    if len(sys.argv) > 1 and sys.argv[1] == '--all-files':
        all_files = True
    if len(sys.argv) > 1 and sys.argv[1] == '--syntax-only':
        syntax_only = True
    main(all_files, syntax_only)
