curve=$1
target=$1/$1/run.sin
mkdir -p $1/$1
cp template.sin $target

if [[ $curve == *expanded*p0* ]]; then
  sed -i 's/#FF/FF = 3/' $target
  sed -i 's/#nloop/nloop = 1/' $target
elif [[ $curve == *analytic*p0* ]]; then
  sed -i 's/#FF/FF = 6/' $target
elif [[ $curve == *p0* ]]; then
  sed -i 's/#FF/FF = 0/' $target
elif [[ $curve == *expanded* ]]; then
  sed -i 's/#FF/FF = 4/' $target
  sed -i 's/#nloop/nloop = 1/' $target
elif [[ $curve == *nloop* ]]; then
  sed -i 's/#FF/FF = 1/' $target
elif [[ $curve == *tree* ]]; then
  sed -i 's/#FF/FF = 10/' $target
fi

if [[ $curve == *sh_* ]]; then
  var=sh
  factor=`sed "s/.*sh_\([0-9]\.[0-9]*\).*/\1/" <<<$curve`
  sed -i "s/#$var/$var = $factor/" $target
fi
if [[ $curve == *sf_* ]]; then
  var="sf"
  factor=`sed "s/.*sf_\([0-9]\.[0-9]*\).*/\1/" <<<$curve`
  sed -i "s/#$var/$var = $factor/" $target
fi

if [[ $curve == *nloop_* ]]; then
  var="nloop"
  factor=`sed "s/.*nloop_\([0-9]\).*/\1/" <<<$curve`
  sed -i "s/#$var/$var = $factor/" $target
fi

if [[ $curve != *fixedorder* ]]; then
  proc='process ttbar = e1, E1 => Wp, Wm, b, B '
  proc+='{ $born_me_method = "threshold" $restrictions = "3+5~t \&\& 4+6~tbar" }'
  sed -i "s/#PROCESS/$proc/" $target
  sed -i "s/#MODEL/model = SM_tt_threshold/" $target
  sed -i "s/#GRIDS/sqrtsmin = sqrts\nsqrtsmax = sqrts/" $target
fi

if [[ $curve == *dm_* ]]; then
  factor=`sed "s/.*dm_\([0-9]*\).*/\1/" <<<$curve`
  cuts="cuts = all abs (M-mtpole) < $factor GeV [Wp,b]"
  cuts+=" and all abs (M-mtpole) < $factor GeV [Wm,B]"
  sed -i "s/#CUTS/$cuts/" $target
fi

if [[ $curve == *mpole* ]]; then
  sed -i 's/#MPOLEFIXED/mpole_fixed = 1/' $target
else
  sed -i 's/#MPOLEFIXED/mpole_fixed = -1/' $target
fi

if [[ $curve == *nopwave* ]]; then
  sed -i 's/#NOPWAVE/no_pwave = 1/' $target
else
  sed -i 's/#NOPWAVE/no_pwave = -1/' $target
fi

cat $target
