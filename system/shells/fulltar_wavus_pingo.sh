#!/bin/sh0
TARNAME="WavusPingo_FULL_$1.tar.gz"

echo "finding exclude *.sock and *pid files"
find ./wavus_pingo -name \*.sock -o -name \*.pid -o -name \*.log -o -name \*.lock > tar_ignore
xargs rm -r <tar_ignore
rm tar_ignore

echo "taring ./wavus_pingo"
tar -czf  $TARNAME ./wavus_pingo


echo "=========COMPLETED=========="
