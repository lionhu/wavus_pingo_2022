#!/bin/sh0
TARNAME="WavusPingo_SLIM_$1.tar.gz"

echo "finding exclude *.sock and *pid files"
find ./wavus_pingo -name \*.sock -o -name \*.pid -o -name \*.log -o -name \*.lock > tar_ignore
xargs rm -r <tar_ignore
rm tar_ignore

echo "taring ./wavus_pingo"
tar -czf  $TARNAME ./wavus_pingo
tar -czf  $TARNAME --exclude 'wavus_pingo/.git' --exclude 'wavus_pingo/nuxtjs_front/node_modules' --exclude 'wavus_pingo/nuxtjs_admin/node_modules' wavus_pingo


echo "=========COMPLETED=========="
