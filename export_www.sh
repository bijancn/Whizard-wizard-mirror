target=~/www/$(basename `pwd`)
echo "Writing to $target"
mkdir -p $target
cp plots/*.pdf $target/
cp plots/*.svg $target/

rm -f $target/md3overview.html
touch $target/md3overview.html
for i in plots/*.html; do
  cat $i >> $target/md3overview.html
done

rm -f $target/index.html
touch $target/index.html
#echo "<font size=\"1\">" >> $target/index.html
for i in plots/*.svg; do
  echo "<div style=\"display:inline-block; width:500px; text-align:center;font-size:5pt;\"><a href=\"$(basename ${i%%.*}).pdf\"><img src=\"$(basename $i)\" alt=\"$(basename $i)\" width=\"500px\" style=\"padding-bottom:0.5em;\"/></a>$(basename ${i%%.*})</div>" >> $target/index.html
done
#echo "</font>" >> $target/index.html
