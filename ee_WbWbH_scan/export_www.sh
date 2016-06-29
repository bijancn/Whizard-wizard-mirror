target=~/www/$(basename `pwd`)
echo "Writing to $target"
mkdir -p $target
cp plots/*.pdf $target/
cp plots/*.svg $target/

rm -f $target/overview.html
touch $target/overview.html
for i in plots/*.svg; do
  echo "<a href=\"$(basename ${i%%.*}).pdf\"><img src=\"$(basename $i)\" alt=\"$(basename $i)\"></a>" >> $target/overview.html
done
