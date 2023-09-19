#!/bin/bash
# usage:  ~/webappy/bin/aama-cpwebappy2langrepo.sh

# 08/03/23: adapted for webappy

echo "webapp ********************************************"
echo "copying ~/webappy  to aama/webappy"

cd ~/webappy
cp README.md ../aama/webapp/
cp bibliography/* ..aama/webappy/bibliography
cp bin/*  ../aama/webappy/bin/
cp *.py ../aama/webappy/
cd ../aama/webapp
git add README.md 
git add bibliography/* 
git add bin/* 
git add *.py 
git commit -am "revised webappy added to aama/webappy"
git push origin master
cd ../../webappy



