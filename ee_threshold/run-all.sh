trap 'echo ">> $BASH_COMMAND"' DEBUG
curves=''
#curves+='tree_dm_15_mpole172_nopwave '
#curves+='nloop_0_dm_15_sh_1._sf_1._mpole172_nopwave '
#curves+='expanded_mpole172_dm_15_p0 '
#curves+='expanded_mpole172_dm_15 '
#curves+='nloop_0_dm_15_sh_1._sf_1._mpole172_p0 '
#curves+='nloop_0_dm_15_sh_1._sf_1._mpole172_nopwave_p0 '
#curves+='expanded_mpole172_dm_15_nopwave_p0 '
#curves+='expanded_mpole172_dm_15_nopwave '

function get-RES () {
  grep RES $1-*/whizard.log | sed 's/^.*RES //'
}
function save-RES () {
  file=/data/bcho/whizard_ttbar_threshold_project/Data/validation/$(basename $1)$2.dat
  get-RES $1 > $file && echo "Saved to $file"
}

echo "Producing $curves"
for curve in $curves; do
  ./create-sindarin.sh $curve
  ./parallelizer.py $curve/$curve sqrts 340 360 --stepsize 0.25
  ./parallelizer.py $curve/$curve sqrts 360 400
  save-RES $curve/$curve
done
