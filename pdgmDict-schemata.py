#!/usr/local/bin/python3
'''
Draws up the morphological property-values sdhemata used in the
current inventory of termclusters. It cretes three files:
1) 'pdgm-schemata-LANG.json': a full-formatted 'schemata'
   and 'pdgmPropOrder' which can be inserted in the 'pdgms-LANG.json'
   file;
2) a LANG-pdgms-newschemata.json file with the new schemata substitute
   for the old. (If content is correctly formatted, this file will
   replace the old LANG-pdgms.json file.
3) 'pdgm-PVN-LANG.txt': with the schemata information information, 
   but formatted for insertion in various pdgm and pname displays.
'''

import json
import re
from shutil import copy
import sys


#def pdgmidx(lang)

# For CL argument
language = sys.argv[1]

# For single lang:
#language = input('Type language name: ')

languagenames = (language, )

# For corpus:
#languagenames = ('aari', 'afar', 'alaaba', 'alagwa', 'akkadian-ob', 'arabic', 'arbore', 'awngi', 'bayso', 'beja-alm', 'beja-hud', 'beja-rei', 'beja-rop', 'beja-van', 'beja-wed', 'berber-ghadames', 'bilin', 'boni-jara', 'boni-kijee-bala', 'boni-kilii', 'burji', 'burunge', 'coptic-sahidic', 'dahalo', 'dhaasanac', 'dizi', 'egyptian-middle', 'elmolo', 'gawwada', 'gedeo', 'geez', 'hadiyya', 'hausa', 'hdi', 'hebrew', 'iraqw', 'kambaata', 'kemant', 'khamtanga', 'koorete', 'maale', 'mubi', 'oromo', 'rendille', 'saho', 'shinassha', 'sidaama', 'somali', 'syriac', 'tsamakko', 'wolaytta', 'yaaku', 'yemsa')

# For coma corpus:
#languagenames = ('aari', 'afar', 'alaaba', 'alagwa',  'arbore', 'awngi', 'bayso', 'beja-alm', 'beja-hud', 'beja-rei', 'beja-rop', 'beja-van', 'beja-wed',  'bilin', 'boni-jara', 'boni-kijee-bala', 'boni-kilii', 'burji', 'burunge', 'coptic-sahidic', 'dahalo', 'dhaasanac', 'dizi', 'elmolo', 'gawwada', 'gedeo', 'geez', 'hadiyya', 'iraqw', 'kambaata', 'kemant', 'khamtanga', 'koorete', 'maale', 'tsamakko', 'wolaytta', 'yaaku', 'yemsa')

for lang in languagenames:
     print(str('\nLANG: ' + lang))
     lfile = str('../aama-data/data/' + lang + '/' + lang + '-pdgms.json')
     jdata = json.load(open(lfile))
     # The file which contains the new schema
     outfile1 = str('pvlists/' + lang + '-schemata.json')
     # A summarizing file for display in pdgm display app
     outfile2 = str('pvlists/' + lang + '-pdgm-PVN.txt')

     # The original lfile with new schemta section

     tccount = len(jdata['termclusters'])
     print(str('tccount:' + str(tccount)))
     # First, to get 'common' prop/val paiirs, 'harvest' pairs from 'common'
     # section of each termcluster into sorted set,  tcpsort.
     # a simple alphabetically ordered set of beja-hud common prop-val tups
     tcpset = set()
     for i in range(tccount):
          #print(str("tccount: " + str(i)))
          tccommon = jdata['termclusters'][i]['common']
          #cset = set()
          cset = set(tccommon.items())
          tcpset = tcpset | cset
     tcpsort = sorted(tcpset)
     # Then reduce tcpsort to 'prop': 'vals' dictionary of 'common' section.
     # This gives  commondict.dict, a dict of 'common' props keys, 
     # each with a set of vals as value.
     commondict = dict()
     # cprops is a list of all the props in 'common:' 
     cpropset = set()
     # Have to give each prop an initial val first. [08/23/22: see if can
     # combine the two 'for' clauses into a 'for' and an 'if']
     for tup in tcpsort:
          commondict[tup[0]] = {tup[1]}
          cpropset.add(tup[0])
     # [NEW] These are the props that occur in the 'common' section
     cprops = sorted(cpropset)
     # Then add the other vals. [Is there a more direct way to do this?]
     for tup in tcpsort:
          if tup[1] not in commondict[tup[0]]:
               val = {tup[1]}
               commondict[tup[0]] = commondict[tup[0]] | val
     # print(str('commondict: \n' + str(commondict)))

     # Then make 'terms' dictionary with pdgm props as keys 
     # and set of pdgm vals as values
     # The val-props dict for lang; starts out empty
     termsdict = {}
     tdsorted = {}
     for i in range(tccount):
          # print(str('termclusters: ' + str(i)))
          tcterm = jdata['termclusters'][i]['terms']
          # print(str('tcterm: ' + str(tcterm)))
          # tcterm is pdgm; tcterm[0] is row of pdgm props
          for j in range(len(tcterm [0])):
               valueset = set()
               tcdict = {}
               # Take all pdgm cols except those containing 'token' in the property-name
               # print(str(tcterm[0][j]))
               if 'token' not in tcterm[0][j]:
                    # want to get '1 to range . . .' to assemble value set for head-prop; but "__" cannot be a value
                    for k in range(1, len(tcterm)):
                         if tcterm[k][j] != "__":
                              valueset.add(tcterm[k][j])
                              # make the tcdict entry for that row
                              tcdict[tcterm[0][j]] = valueset
               # Then add tcdict entries to pvdict 
               for key in tcdict:
                    # If property already there, just add the values to the set of values
                    if key in termsdict.keys():
                         termsdict[key] = termsdict[key] | tcdict[key]
                    # Otherwise, add new enty to pvdict
                    else:
                         termsdict.setdefault(key, tcdict[key])
     for key in sorted(termsdict):
          tdsorted[key] = termsdict[key]
     # print(str('termsdict: \n' + str(tdsorted)))
     
     # Finally, combine 'commondict' and 'termsdict"
     # pvdict will be a union of commondict and termsdict
     pvdict = {}
     pvdsorted = {}
     for key in commondict.keys():
          if key in tdsorted.keys():
               combo = commondict[key] | tdsorted[key]
               pvdict.setdefault(key, combo)
          else:
               pvdict.setdefault(key, commondict[key])
     for key in tdsorted.keys():
          if key not in commondict.keys():
               pvdict.setdefault(key, tdsorted[key])
     for key in sorted(pvdict):
          pvdsorted[key] = sorted(pvdict[key])
     #jdata["schemata"] = pvdsorted
     #json.dump(jdata, fp=open(outfile3, 'w'), indent=2)     

     print(str('new ' + lang + ' schemata text: ' + outfile1))
     # print(pvdsorted)
     
     # Write 'schemata' to json file
     json.dump(pvdsorted, fp=open(outfile1, 'w'), ensure_ascii=False, indent=2) 
     
     # This subroutine yields a summarizing file pdgm-PVN-LANG.txt'
     # Given here as part of schemata since it uses both 
     # the pvdsorted str and cpropset.
     # Other possibility would be to put this in a separate file
     # "pdgmDict-PVN.py" and take pvdsorted from pdgm-schemata-LANG-file.
     # but not clear where cprops would come from
     pdgmProps = jdata['pdgmPropOrder']
     cprops = sorted(cpropset)
     pvdformat = str(pvdsorted)
     pvdf1 = pvdformat.replace('],', ']\n')
     pvdf1 = pvdf1.replace("'", "")
     pvdf1 = pvdf1.replace('{', "")
     pvdf1 = pvdf1.replace('}', "")
     pvdf1 = pvdf1.replace(' ', "")
     pdgmPropStr = ','.join(pdgmProps)
     # Have to make dict out of pvdsorted2
     cpropstr = ','.join(cprops) 
     #cpropstr = str('COMMON PROPS:\n' +  str(cprops))
     cpropstr = str(str(tccount) + '\ PDGMS:\ COMMON\ PROPS:\n ' + cpropstr)
     porderstr = str('\nPARADIGM-NAME\ PROP-ORDER:\n ' + pdgmPropStr)
     pvdsorted2 = str(str(pvdf1) + '\n------------------\n' + cpropstr + porderstr)
     file = open(outfile2, "w")
     file.write(str(pvdsorted2))
     file.close
     print('Schemata summary:')
     print(str(pvdsorted2))
     
     # Replace 'schemata' section in current updated lang file
     
     # First re-open the newly made schemata file
     with open(outfile1) as f:
          ftext1 = f.read()

     # Prepare replacement text
     ftext1a = str('schemata": ' + ftext1 + ',\n  "lexemes": ')
     # print("ftext1a:")
     # print(ftext1a)

     #Open 'matrix' text
     with open(lfile) as f:
          ftext = f.read()
     ftext2 = ftext.replace('\n','\\n')
     # print("ftext2")
     # print(ftext2)
     # subtitute the new shemata text for the old
     # NOTE: FOLLOWING DOES NOT WORK FOR INITIAL 'SCHEMATA'
     # (for an initial schemata, insert schemata file
     ftextnew1 = re.sub('schemata.*"lexemes": ', ftext1a, ftext2)
     ftextnew2 = ftextnew1.replace('\\n','\n')
     # print('ftextnew2')
     #print(ftextnew2)
     file = open(lfile, "w")
     file.write(ftextnew2)
     file.close

'''
07/22/23
above re.sub works for:
elmolo
07/20/23
This substitution of 'schemata' back into pdgms.json file will not be done
until the problem with re.sub is resolved.

     # Replace 'schemata' section in  json data file.
     # Will either have to use re.sub or substitiution
     # in json file with json.load/dump, with some
     # subsequent reformatting  'terms' (see below)
     # For the moment, will go with re.sub

     with open(lfile) as f:
          ftext = f.read()
     ftext2 = ftext.replace('\n','\\n')
     
     ftextnew1 = re.sub('schemata.*lexemes\"\:', ftext1a, ftext2)
     ftextnew2 = ftextnew1.replace('\\n','\n')
     file = open(lfile, "w")
     file.write(ftextnew2)
     file.close
'''
