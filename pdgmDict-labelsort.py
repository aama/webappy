#!/usr/local/bin/python3
'''
File to be labeled and ordered is placed in dir webbapy/pdgmfiles
labrled as LANG-sort-pdgms.json. Program replaces each termcluster 
label with new label made from prop values of props entered with
'pdgmPropOrder' prompt. Pdgm file with new props is written out
to file LANG-labeled-sort-pdgms.json. After inspection, this file
can be ordered by pdgmSort.py.
[Temporary for dhaasanac trial:
 Desired orop order is:
 pos,conjClass,lexeme,derivedStem,derivedStemAug,extended,tam,polarity,morphClass,proClass
]
Required text transformations before, in order to preserve structure
of 'terms' as list of parallel lists (mimicking CSV output of query):

     ",_" => &

Required text transformations after sorting:
     ,_  => ,^J
     terms': => terms':^J
     ]]}  => ]]^J}
     &    => ', '
 
I.e.:
     ',_' => ',^J'
     },_  => },^J[
     ],_[ => ],^J[

'''

import json
from shutil import copy
import pprint
import re
import os
import sys

def value_getter(pdgm):
    return pdgm['label']
 
# For CL argument
lang = sys.argv[1]

# For single lang:
#lang = input('Type language name: ')
#xlang = 'elmolo'
print(str('LANG: ' + lang))
#lfile must have already been copied from aama-data
lfile = str('../aama-data/data/' + lang + '/' + lang + '-pdgms.json')
lfilebck = str('../aama-data/data/' + lang + '/' + lang + '-pdgms-old.json')
copy(lfile, lfilebck)
# 'exploded'[i.e.standard output] termcluster file (temporary)
# 'terms' section will need to be reformatted into AAMA 'pdgm' format
outfile0 = str('pvlists/' + lang + '-ordered-pdgms-0.json')
# formatted termcluster file
outfile1 = str('pvlists/' + lang + '-termclusters.json')
# Make new labels out of the 'common' values
pdgmfile = open(lfile, 'r')
#print(pdgmfile)
#pdgms = pdgmfile.read()
#print(pdgms)
# pdgmdict is the whloe language file
pdgmdict = json.load(pdgmfile)
#pdgmdict = dict(pdgms)
#print('pdgmdict in:')
#print(pdgmdict)
# The is the normative order of the pdgm props for this lang
# pdgm labels will be the values for these props in the normative
# order
tcprops = pdgmdict['pdgmPropOrder']
#tcpropstr = ','.join(tcprops)
#tcprops = pdgmdict[10]
lpref = pdgmdict['lgpref']
# This is the current prop order for pdgm names
print('PDGM name label props are:')
print(tcprops)
# this will be a list of pnames
plabels = ''
# get the number of pdgms in the file
tccount = len(pdgmdict['termclusters'])
print(str('tccount: ' + str(tccount)))

# New label string

# for each termcluster, make new label string out of the
# values of its props in its 'common' section, taken in the
# order of the props in 'refPdgmProops'
for i in range(tccount):
     # read-in 'common' section
     plabel1 = pdgmdict['termclusters'][i]['label']
     #print(str('plabel1 = ' + plabel1))
     tccommon = pdgmdict['termclusters'][i]['common']
     # 'common' section tupled
     tpltcc = list(tccommon.items())
     pdgmvals = []
     for prop in tcprops:
          for tup in tpltcc:
               if tup[0] == prop:
                    if tup[0] == 'morphClass':
                         #print(tup[0])
                         #print(tup[1])
                         # Make 'morph' first item in label
                         pdgmvals.insert(0,'morph')
                         pdgmvals.append(str('-' + tup[1])) 
                    elif tup[0] == 'lexeme':
                         # put '-' around lexeme'
                         pdgmvals.append(str('-' + tup[1] + '-')) 
                    else:
                         pdgmvals.append(str(tup[1]))
     pvalstr = ''.join(pdgmvals)
     plabel2 = str(lpref + '-' + pvalstr)
     #print(str('plabel2 = ' + plabel2))
     plabels += str(plabel2 + '\n')
     #print(plabels)
     pdgmdict['termclusters'][i]['label'] = plabel2
     plabel3 = pdgmdict['termclusters'][i]['label']
     #print(str('plabel3: ' + plabel3))

# Now sort termclusters by label     
pdgms = pdgmdict['termclusters']
#print('termclusters in:')
#print(pdgms)
# Now sort the paradigms using label as key
res = sorted(pdgms, key = value_getter)
# and replace the original pdgms by the pdgms sorted by the new label
pdgmdict['termclusters'] = res
print('termclusters out:')
#print(res)
# Write the reordered pdgms to a json file
fp0 = open(outfile0, 'w')
indent = 2
json.dump(res, fp0, ensure_ascii=False, indent=indent)
fp0.close()

# now open the newly made termclusters
f = open(outfile0, 'r')
tctext = f.read()

# outfle0 has served its purpose, and can now be removed
os.remove(outfile0)

print("tctext")
# print(tctext)

# re-format 'termclusters'section

# json.dump formulates output with one json constituent per line.
# However in our scheme the paradigm structure 'terms' is a 
# list of lists in whcih each  subllist represents a row of the pdgm.
# Thus in order to approxmate the familiar pdgm 'table' format 
# it is necessary to delete CR ('\n') and intervening spaces,  
# after each row-initial list bracket,  and between each row value.

# It can be seen that the number of spaces that need to be deleted 
# after '\n'  = 'width of indent' (as used in json.dump) times 'depth of json
# constituent' (= 4 for list members which constitute "paradigm rows" 
# and 3 for bracket which closes row). Thus in general 
# spdel = indent * depth; and in this case spdel1 = 8, and spdel2 =6

depth1 = 4
depth2 = 3
blank1 = depth1*indent  # i.e. '4*2'
blank2 = depth2*indent  # i.e. '3*2'
# The string of blank spaces to be eliminated
s1 = " " * blank1
s2 = " " * blank2

tctextx = str(tctext).replace(str('[\n' + s1 +'"'),'["')
# print("\nX\n")
# print(tctextx)
tctexty = tctextx.replace(str('",\n' + s1 + '"'), '" ,"')
# print("\nY\n")
# print(tctexty)
tctextnew = tctexty.replace(str('"\n' + s2 + ']'),'"]')
# print("\nNew Text\n")
# print(tctextnew)

# Keep a separate 'termclusters' file of sorted and ordered paradibms
with open(outfile1, 'w') as f:
    f.write(tctextnew )

# Replace 'termcluster' section in current updated lang file

# Prepare for replacement
ftext1a = str('termclusters": ' + tctextnew + '}')
# print("ftext1a:")
# print(ftext1a)
ftext1b = ftext1a.replace('\n', '\\n')

# Open 'matrix' text
with open(lfile) as f:
    ftext = f.read()
ftext2 = ftext.replace('\n','\\n')
#print("ftext2")
#print(ftext2)

# Replaace ew termclusters into lfile
# For re.sub, make VERY SURE that lfile ends exactly with ']}'
ftextnew1 = re.sub('termclusters.*]}', ftext1b, ftext2)
#ftextnew1 = re.sub('termclusters.*]}', ftext1a, ftext)
ftextnew2 = ftextnew1.replace('\\n','\n')
#print('ftextnew1')
#print(ftextnew1)
file = open(lfile, "w")
file.write(ftextnew2)
file.close

'''
DictList = {'a':'x','b':'y','c':'z','d':'w'}
