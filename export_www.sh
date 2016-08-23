target=~/www/$(basename $1)
echo "Writing to $target"
mkdir -p $target
cp $1/plots/*.pdf $target/
cp $1/plots/*.svg $target/

rm -f $target/md3overview.html
touch $target/md3overview.html
for i in plots/*.html; do
  if [ -f $i ]; then
    cat $i >> $target/md3overview.html
  fi
done

rm -f $target/index.html
touch $target/index.html
for i in plots/*.svg; do
  echo "<div style=\"display:inline-block; width:500px; text-align:center;font-size:5pt;\"><a href=\"$(basename ${i%%.*}).pdf\"><img src=\"$(basename $i)\" alt=\"$(basename $i)\" width=\"500px\" style=\"padding-bottom:0.5em;\"/></a>$(basename ${i%%.*})</div>" >> $target/index.html
done
