#!/bin/sh
mkdir threshold_nlofull_cms_$1
cd threshold_nlofull_cms_$1
ln -s ../process_settings_threshold.sin process_settings_threshold.sin
ln -s ../process_settings_threshold_SM.sin process_settings_threshold_SM.sin
mkdir rivet whizard
cp ../threshold_nlofull_cms_344/rivet/yodaenvelopes rivet/
cp ../threshold_nlofull_cms_344/rivet/yodamerge_noscale rivet/
cp ../threshold_nlofull_cms_344/rivet/*.cc rivet/
cp ../threshold_nlofull_cms_344/rivet/*.plot rivet/
cp ../threshold_nlofull_cms_344/rivet/*.info rivet/
cp ../threshold_nlofull_cms_344/rivet/SConstruct rivet/
cp ../threshold_nlofull_cms_344/whizard/*template.sin whizard/
cp ../threshold_nlofull_cms_344/whizard/submit whizard/
cp ../threshold_nlofull_cms_344/whizard/.commonrc whizard/
cp ../threshold_nlofull_cms_344/run.json ./
../copy_grids.sh $1
sed -i "s/sqrts = 344/sqrts = $1/" whizard/*sin
sed -i "s/344/$1/" rivet/*plot
cd rivet
scons --site-dir=../../
cd ../
source whizard/.commonrc
load-whizard-gfortran
../mpi_run_this.sh
