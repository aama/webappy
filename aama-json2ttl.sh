#!/bin/bash
# usage:  ~/webapp/bin/aama-edn2ttl.sh "dir"

# 03/21/14; rev. 10/30/20 -- insert .ttl into fuseki 
# rev. 07/07/21 -- run it out of webappy, use python/json;
# fuseki no longer requires xml/rdf format

#. bin/constants.sh

 
#for d in burji dizi  hebrew kemant saho yaaku

#for d in `ls data`
#do
   echo "$d ********************************************"
	#fs=`find data/$d -name *json`
    fs=`find $1 -name *json`
    for f in $fs
	do
                echo "f is ${f}"
	       f3=${f%/*-pdgms.json}
               f4=${f3#../aama-data/data/}
	       echo "generating ${f%\.json}.ttl  for  $f4 "
		
               # python3 json2ttl.py $f > ${f%\.json}.ttl
               python3 json2ttl.py $f4
               #  python3 json2ttl.py beja-hud

	done
#done
