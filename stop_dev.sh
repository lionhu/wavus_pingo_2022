#!/bin/sh
#echo "Removing exclude *.sock and *pid files"
#find . -name \*.sock -o -name \*.pid -o -name \*.log -o -name \*.lock > tar_ignore
#xargs rm -r <tar_ignore
#rm tar_ignore


docker-compose -f docker-compose.dev.yml down
