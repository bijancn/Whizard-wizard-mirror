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
elif [[ $curve == *expanded*soft*hard* ]]; then
  sed -i 's/#FF/FF = 8/' $target
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

if [[ $curve == *unrestricted* ]]; then
  restricted=''
  filter=''
else
  restricted='$restrictions = "3+5~t \&\& 4+6~tbar"'

  filter='\n$gosam_filter_nlo = "lambda d: d.vertices(T,Tbar,A) > 0 or d.vertices(T,Tbar,Z) > 0"\n'
  filter+='$gosam_filter_lo = "lambda d: d.vertices(T,Tbar,A) > 0 or d.vertices(T,Tbar,Z) > 0"\n'
  filter+='$gosam_symmetries="family,generation"\n'
  filter+='form_threads=16\n'
  filter+='form_workspace=1000\n'
  filter+='$gosam_fc="ifort"'
fi
if [[ $curve == *NLO* ]]; then
  nlo='nlo_calculation="Full"'
else
  nlo=''
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
      proc+='{ $born_me_method = "threshold" }' ;;
    *)
      proc='process ttbar = e1, E1 => Wp, Wm, b, B '
      proc+='{ \$born_me_method = "threshold"'
      proc+=" $restricted }" ;;
  esac
  sed -i "s/#alpha/alpha_em_i = 125.924 ! (not running)/" $target
  sed -i 's/#printextra/printf "mtpole = %g" (mtpole) /' $target
else
  # fixedorder
  options='?combined_nlo_integration = false\n'
  if [[ $curve == *NLO* ]]; then
    if [[ $curve == *unrestricted* ]] || [[ $curve == *onshell* ]]; then
      options+='$loop_me_method = "openloops"\n'
    else
      options+='$loop_me_method = "gosam"\n'
      options+='$born_me_method = "gosam"\n'
      options+='$correlation_me_method = "gosam"\n'
      options+='$real_tree_me_method = "gosam"\n'
    fi
  fi
  options+='alphas_power = 0\n'
  options+='?use_vamp_equivalences = false\n'
  case $curve in
    *onshell*)
      options+='alpha_power = 2'
      proc='process ttbar = e1, E1 => t, T '
      proc+="{ $nlo }" ;;
    *)
      options+='alpha_power = 4'
      proc='process ttbar = e1, E1 => Wp, Wm, b, B '
      proc+="{ $nlo "
      if [[ $curve != *NLO* ]]; then 
        proc+="$restricted "
      else
        proc+="$filter "
      fi
      proc+="}" ;;
  esac
  sed -i "s/#MODEL/model = SM\n$options/" $target
  sed -i "s/#mass/mtop/" $target
  sed -i "s/#alpha/GF = 1.2273E-005/" $target
  sed -i 's/#printextra/printf "alpha_em_i = %g" (alpha_em_i)/' $target
  if [[ $curve == 'fixedorder_offshell_NLO' ]]; then
    sed -i "s/#GRIDS/mult_call_real = 5.0\nmult_call_virt = 0.5/" $target
  else
    sed -i "s/#GRIDS/mult_call_real = 20.0\nmult_call_virt = 0.5/" $target
  fi
  if [[ $curve == *onshell* ]]; then
    sed -i "s/#wtop/wtop = 0.0/" $target
  else if [[ $curve == *NLO* ]]; then
    sed -i "s/#wtop/wtop = 1.4089709/" $target
  else
    sed -i "s/#wtop/wtop = 1.5386446/" $target
  fi
  fi
fi
sed -i "s/#PROCESS/$proc/" $target

if [[ $curve == *dm_* ]]; then
  factor=`sed "s/.*dm_\([0-9]*\).*/\1/" <<<$curve`
  cuts="cuts = all abs (M-mtpole) < $factor GeV [Wp,b]"
  cuts+=" and all abs (M-mtpole) < $factor GeV [Wm,B]"
  sed -i "s/#CUTS/$cuts/" $target
fi

cat $target
