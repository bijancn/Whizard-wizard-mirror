trap 'echo ">> $BASH_COMMAND"' DEBUG
curves=''
#curves+='tree_dm_15_mpole172_nopwave '
#curves+='expanded_mpole172_dm_15_p0 '
#curves+='expanded_mpole172_dm_15 '
#curves+='expanded_onshell_mpole172_nopwave '
#curves+='expanded_onshell_mpole172 '
#curves+='fixedorder_onshell_NLO '
#curves+='nloop_0_dm_15_sh_1._sf_1._mpole172_p0 '
#curves+='nloop_0_dm_15_sh_1._sf_1._mpole172_nopwave '
#curves+='nloop_0_dm_15_sh_1._sf_1._mpole172_nopwave_p0 '

curves+='nloop_0_sh_1._sf_1._mpole172 '
curves+='resum_switchoff_nloop_0_sh_1._sf_1._mpole172 '
curves+='expanded_switchoff_nloop_0_sh_1._sf_1._mpole172 '
curves+='expanded_soft_nloop_0_sh_1._sf_1._mpole172 '
curves+='matched_nloop_0_sh_1._sf_1._mpole172 '
curves+='matched_nloop_1_sh_1._sf_1._mpole172 '
curves+='nloop_1_sh_1._sf_1._mpole172 '
curves+='resum_switchoff_nloop_1_sh_1._sf_1._mpole172 '
curves+='expanded_switchoff_nloop_1_sh_1._sf_1._mpole172 '
curves+='expanded_soft_nloop_1_sh_1._sf_1._mpole172 '

#curves+='nloop_0_sh_1._sf_1._mpole172_nopwave '
#curves+='nloop_0_sh_1._sf_1._mpole172_nopwave_p0 '
#curves+='nloop_1_sh_1._sf_1._mpole172_nopwave '
#curves+='nloop_1_sh_1._sf_1._mpole172_nopwave_p0 '
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
  if [ ! -f $curve/done ]; then
    ./create-sindarin.sh $curve
    #./parallelizer.py $curve/$curve sqrts 344.0 344.001 --stepsize 0.00001
    #./parallelizer.py $curve/$curve sqrts 344.0 344.25 --stepsize 0.001
    ./parallelizer.py $curve/$curve sqrts 340 350 --stepsize 0.25
    ./parallelizer.py $curve/$curve sqrts 350 400
    #./parallelizer.py $curve/$curve sqrts 400 600
    save-RES $curve/$curve
    touch $curve/done
  fi
done
