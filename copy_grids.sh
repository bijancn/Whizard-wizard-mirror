#!/bin/sh
energy=$1'.0-sqrts'
src='../threshold_nlofull_cms/whizard/nlofull_'
trgt='whizard/nlofull_'
types=(
Born
Real
Virtual
)
nums=(
1
2
3
)
declare -A scales
scales[low1]=0
scales[low2]=1
scales[high1]=2
scales[high2]=3

for index in ${!types[*]}; do
  grid=${types[$index]}_m${nums[$index]}.vg
  for s in "${!scales[@]}"; do
    cp ${src}${types[$index]}-${energy}--${scales[$s]}-scale_variations-0/nlofull_${grid} ${trgt}${s}_${grid}
  done
  cp ${src}${types[$index]}-${energy}-0/nlofull_${grid} ${trgt}central_${grid}
done

src='../threshold_matched_nlofull_nlodecay_newscalestar/whizard/matched_nlodecay_'
trgt='whizard/matched_nlodecay_'
scales[central]=4

for index in ${!types[*]}; do
  grid=${types[$index]}_m${nums[$index]}.vg
  for s in "${!scales[@]}"; do
    cp ${src}${types[$index]}-${energy}--${scales[$s]}-scale_variations--21-matched_variations-0/matched_nlodecay_${grid} ${trgt}${s}_${grid}
  done
done
