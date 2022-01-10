#!/bin/sh
echo "removing migrations files"


find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
#find . -path "*/migrations/*.py" -not -name "__init__.py" > rm_py.txt
#find . -path "*/migrations/*.pyc"   > rm_pyc.txt

