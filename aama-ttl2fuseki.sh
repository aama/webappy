#!/bin/bash
# usage:  fuput "dir"
# examples:
#    aama/$ bin/fuput "data/*" --  puts everything
#    aama/$ bin/fuput "data/alaaba" -- puts only alaabe
#    aama/$ bin/fuput "data/alaaba data/burji data/coptic" -- puts all 3 datasets
#    aama/$ bin/fuput "schema" -- puts all 3 datasets
# cumulative logfile written to logs/fuput.log

# 07/13/13: cf. fupost-default.sh for loading data into single default graph
# rev. 10/30/20 -- insert .ttl into fuseki


#. bin/constants.sh

# echo "fuload.log" > logs/fuload.log;
# for f in `find $1 -name *.rdf`
for f in `find $1 -name *.ttl`
do
    # l=${f%.rdf}
    l=${f%.ttl}
    lang=${l#../aama-data/data/}
    graph="http://oi.uchicago.edu/aama/2013/graph/`dirname ${lang/\/\///}`"
    echo posting $f to $graph;
    ../jena/apache-jena-fuseki-3.16.0/bin/s-post -v http://localhost:3030/aama/data $graph  $f 2>&1 
    #../fuseki/apache-jena-fuseki-2.4.0/bin/s-post -v http://localhost:3030/aama/data $graph  $f 2>&1 >>logs/fuload.log
	#${FUSEKIDIR}/bin/s-post -v http://localhost:3030/aamaData/data 'default'   $f 2>&1 >>logs/fuload.log
done


# i.e.
#    ${FUSEKIDIR}/bin/s-post -v http://localhost:3030/aama/data \
#                          http://oi.uchicago.edu/aama/2013/graph/beja-arteiga  \
#			  data/beja-arteiga//beja-arteiga-pdgms.rdf \
#			  2>&1 \ #"redirect stderr to stdout"
#			  >>logs/fuload.log
