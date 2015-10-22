sindarin=$1
target=$1.sin
#mkdir -p $1/$1
cp template.sin $target

#if [[ $sindarin == *sh_* ]]; then
  #var=sh
  #factor=`sed "s/.*sh_\([0-9]\.[0-9]*\).*/\1/" <<<$sindarin`
  #sed -i "s/#$var/$var = $factor/" $target
#fi
#if [[ $sindarin == *sf_* ]]; then
  #var="sf"
  #factor=`sed "s/.*sf_\([0-9]\.[0-9]*\).*/\1/" <<<$sindarin`
  #sed -i "s/#$var/$var = $factor/" $target
#fi

#if [[ $sindarin == *nloop_* ]]; then
  #var="nloop"
  #factor=`sed "s/.*nloop_\([0-9]\).*/\1/" <<<$sindarin`
  #sed -i "s/#$var/$var = $factor/" $target
#fi

process=`echo $1 | sed 's/-.*//'`
echo "process $process"
sed -i "s/#PROCESS/$process/" $target
if [[ $sindarin == *nlo* ]]; then
  proc_def='E1, e1 => Wp, Wm, b, B {nlo_calculation="Full"}'
  sed -i "s/#PROC_DEF/$proc_def/" $target
fi

if [[ $sindarin == *E_* ]]; then
  factor=`sed "s/.*E_\([0-9]*\).*/\1/" <<<$sindarin`
  cuts="cuts = let @jets = cluster if E > $factor GeV [colored] in"
  cuts+="      count [@jets] == 2"
  sed -i "s/#cuts/$cuts/" $target
fi

if [[ $sindarin == *integrate* ]]; then
  sed -i 's/#integrate/integrate/' $target
fi

if [[ $sindarin == *simulate* ]]; then
  sed -i 's/#integrate/simulate/' $target
fi

cat $target
