#!/bin/sh

# rev 02/13/15; rev. 10/30/20 -- insert .ttl into fuseki

# Script to delete current arg graphs from datastore, 
# regenerate ttl from corrected json, upload to fuseki, 
# generate pnames files necessary for pdgm "pname" display; 
# assumes fuseki has been launched by bin/fuseki.sh.
# Meant to be used when one or more lang json files have been updated.
# usage (from ~/webapp): 
# bin/aama-datastore-update.sh ../aama-data/data/[LANGDOMAIN]

echo "\n[01/05/22] NOTICE: For the moment the 'bin/aama-json2ttl.sh' component of this shell \nscript is not working correctly. Until this is corrected, before running this script, \nyou must run 'python3 json2ttl.py' [no args] independently."
echo " "
echo "[Enter] to continue or Ctl-C to exit"
read

#. bin/constants.sh
ldomain=${1//,/ }
ldomain=${ldomain//\"/}

# DOESN'T WORK ldomain="bayso beja-atmaan beja-hadendowa bilin boni-kilii boni-jara boni-kijee-bala burunge burji dahalo elmolo iraqw kambaata kemant saho shinassha wolaytta yemsa"

echo "ldomain is ${ldomain}"

for f in `find $ldomain -name "*pdgms.json"`
do
    f2=${f%/*-pdgms.json}
    echo "delete f = ${f2}"
    # Let's try it with the following not commented-out [01/05/22]
    bin/fudelete.sh $f2
    bin/fuqueries.sh
    echo " "
    #echo "[Enter] to continue or Ctl-C to exit"
    #read
    echo "json2ttl f = ${f2}"
    #bin/aama-json2ttl.sh $f2    
    echo "ttl2fuseki f = ${f2}"
    bin/aama-ttl2fuseki.sh $f2
    #bin/fuqueries.sh
    echo "======================="
    #bin/aama-cp2lngrepo.sh $f
done
