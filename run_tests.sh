#!/bin/sh
nosetests --with-coverage --with-timer --rednose --cover-erase \
  utils.py whizard_wizard.py --cover-package=utils,whizard_wizard
