curve=$1
target=$1/$1/run.sin
mkdir -p $1/$1
cp template.sin $target

if [[ $curve == *resum*switchoff* ]]; then
  sed -i 's/#FF/FF = -2/' $target
elif [[ $curve == *matched* ]]; then
  sed -i 's/#FF/FF = -1/' $target
elif [[ $curve == *p0* ]]; then
  sed -i 's/#FF/FF = 0/' $target
elif [[ $curve == *resum* ]]; then
  sed -i 's/#FF/FF = 1/' $target
elif [[ $curve == *expanded*hard*p0* ]]; then
  sed -i 's/#FF/FF = 3/' $target
elif [[ $curve == *expanded*hard* ]]; then
  sed -i 's/#FF/FF = 4/' $target
elif [[ $curve == *expanded*soft* ]]; then
  sed -i 's/#FF/FF = 5/' $target
elif [[ $curve == *expanded*switchoff* ]]; then
  sed -i 's/#FF/FF = 6/' $target
elif [[ $curve == *analytic*p0* ]]; then
  sed -i 's/#FF/FF = 7/' $target
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
  sed -i "s/#MODEL/model = SM_tt_threshold/" $target
  sed -i "s/#GRIDS/sqrtsmin = sqrts\nsqrtsmax = sqrts/" $target
  sed -i "s/#mass/m1S/" $target
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
  case $curve in
    *onshell*)
      proc='process ttbar = e1, E1 => t, T '
      proc+='{ $born_me_method = "threshold" }'
      sed -i "s/#PROCESS/$proc/" $target ;;
    *)
      proc='process ttbar = e1, E1 => Wp, Wm, b, B '
      proc+='{ $born_me_method = "threshold" $restrictions = "3+5~t \&\& 4+6~tbar" }'
      sed -i "s/#PROCESS/$proc/" $target ;;
  esac
  sed -i "s/#alpha/alpha_em_i = 125.924 ! (not running)/" $target
  sed -i 's/#printextra/printf "mtpole = %g" (mtpole) /' $target
else
  options='?combined_nlo_integration = false\n'
  options+='$loop_me_method = "openloops"\n'
  options+='alphas_power = 0\n'
  options+='?use_vamp_equivalences = false\n'
  case $curve in
    *onshell*)
      options+='alpha_power = 2'
      proc='process ttbar = e1, E1 => t, T ' ;;
    *)
      options+='alpha_power = 4'
      proc='process ttbar = e1, E1 => Wp, Wm, b, B ' ;;
  esac
  if [[ $curve == *NLO* ]]; then
    proc+='{nlo_calculation="Full"}'
  fi
  sed -i "s/#MODEL/model = SM\n$options/" $target
  sed -i "s/#mass/mtop/" $target
  sed -i "s/#alpha/GF = 1.2273E-005/" $target
  sed -i 's/#printextra/printf "alpha_em_i = %g" (alpha_em_i)/' $target
  sed -i "s/#GRIDS/mult_call_real = 10.0\nmult_call_virt = 0.5/" $target
  sed -i "s/#PROCESS/$proc/" $target
  if [[ $curve == *onshell* ]]; then
    sed -i "s/#wtop/wtop = 0.0/" $target
  fi
fi

if [[ $curve == *dm_* ]]; then
  factor=`sed "s/.*dm_\([0-9]*\).*/\1/" <<<$curve`
  cuts="cuts = all abs (M-mtpole) < $factor GeV [Wp,b]"
  cuts+=" and all abs (M-mtpole) < $factor GeV [Wm,B]"
  sed -i "s/#CUTS/$cuts/" $target
fi

cat $target
