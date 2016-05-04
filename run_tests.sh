#!/bin/sh
nosetests --with-coverage --with-timer --rednose --cover-erase \
  data_utils.py utils.py whizard_wizard.py --cover-package=data_utils,utils,whizard_wizard
