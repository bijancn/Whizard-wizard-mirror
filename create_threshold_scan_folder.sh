#!/bin/sh
mkdir threshold_$1
cd threshold_$1
ln -s ../process_settings_threshold.sin process_settings_threshold.sin
ln -s ../process_settings_threshold_SM.sin process_settings_threshold_SM.sin
mkdir whizard
cp ../threshold_nlofull_cms/whizard/*template.sin whizard/
cp ../threshold_nlofull_cms/whizard/submit whizard/
cp ../threshold_nlofull_cms/whizard/.commonrc whizard/
cp ../threshold_nlofull_cms/run.json ./
source whizard/.commonrc
load-whizard-gfortran
../mpi_run_this.sh
