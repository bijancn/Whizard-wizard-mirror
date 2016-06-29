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

rm -f $target/overview.html
touch $target/overview.html
for i in plots/*.svg; do
  echo "<a href=\"$(basename ${i%%.*}).pdf\"><img src=\"$(basename $i)\" alt=\"$(basename $i)\"></a>" >> $target/overview.html
done
