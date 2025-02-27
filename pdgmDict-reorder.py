#!/usr/local/bin/python3
'''
Provisional command-line program adapting current query code to reorder 
data ('terms') columns of LANG-pdgms.json file. Reordering is done
by simply (re)submitting pdgm-forming query with different order of output
preperties. Output is intended to be then manually subtituted for current 
paradigm 'terms' section. 
Working on code (using pandas?) to reorder data column display output on 
the fly and/or in json file refrence paradigm; similar approah also for 
variable  paradigm name order display.

'''

from SPARQLWrapper import SPARQLWrapper, JSON
import csv
from io import StringIO
from pdgmDispQuery import query   #import for pdgm-display query code
import shelve

l = input('Type language name: ')
# pdgm "name" contains old column order
pvals = input('Type current paradigm name (pval%old-valstring): ')

sfile = str('pvlists/' + l + '-pdgmdb')
pdgmdb = shelve.open(sfile) # open it
ppropval = pdgmdb[pvals] # get the full prop-val string
pdgmdb.close()  # close it right away
print(str('ppropval: ' + ppropval))

# WARNING! THIS VERSION PRESUPPOSES THAT NON-DEFAULT
# VALSTRING WILL BE SEPARATED BY SIMPLE '-', NOT '%'
# Back to '%' [101822]
if "%" in ppropval:
    propsel = ppropval.split("%")
    pvalue = propsel[0]
    valstring = propsel[1]
else:
    pvalue = ppropval
    valstring = "number,person,gender,token,token-note"
print(str("pvalue: " + pvalue))
# Now e=we stipulate new column order
valstring = input('Type new valstring order: ')
sparql = SPARQLWrapper("http://localhost:3030/aama/query")

res = query(pvalue,valstring,l)
print("\nSPARQL QUERY (by pdgmDispQuery.py from ppropval & valstring):")
print(res)
# else:
#pdisp.set(str('Problem with w: ' + w))
sparql.setQuery(res)
sparql.setReturnFormat(JSON)
result = sparql.query().convert() # JSON converted output
result2 = sparql.query() # raw outpuut
#print(str("SPARQLWrapper query URL:\n\n " + str(result2)))
#print("SPARQLWrapper JSON-formatted output: ")
#pprint(result)
select  = result["head"]["vars"]
select2 = []
header = []  # for both CSV and tabular output
paradigm = "" # this will be the CSV form output [not used at this point]
paradigm2 = []  # this will be the tabular output
results = result["results"]["bindings"]
for result in results:
#print(str('result:' + str(result)))
    pdgmrow = []
    pdgmrow2 = []
    for sel in select:
        #print(str('sel1: ' + sel))
        # See if 'optional' properties have yielded a value
        if sel in result:
            if sel not in header:
                header.append(sel)
            selval = result[sel]["value"]
            #print(str('selval: ' + selval))
            # pdgmrow = str(pdgmrow + sel + "      ") 
            pdgmrow.append(selval)
            pdgmrow2.append(selval)
            # i.e.
            # number = result["number"]["value"]
            # person = resnult["person"]["value"]
            # gender = result["gender"]["value"]
            # token  = result["tokenn"]["value"]
            # pdgmrow = (str(number +  "      " + person + "     " + gender + "     " + token + "\n"))
    pdgmrowstr = (",").join(pdgmrow)
    paradigm = str(paradigm + pdgmrowstr + "\n")
    paradigm2.append(pdgmrow2)
        
paradigm3 = paradigm2[:]
paradigm3.insert(0,header)
print("\nparadigm2:")
print(paradigm2)

# This gives the simple CSV
print("\nFROM WHICH . . .")
#print("\nCSV query output (from string-formatted output):\n")
#print(paradigm)
print("as list of lists:")
print(paradigm3)
#print("paradigm2: [for tabulate]")
#print(paradigm2)

