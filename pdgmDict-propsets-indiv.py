#!/usr/local/bin/python3
'''
Counts pdgms in LANG and returns list of property sets  used in each
of the paradigm's termcluster (common and terms sections).

'''

import json
import shelve
import sys
from operator import itemgetter
#def pdgmidx(lang)

# For CL argument
language = sys.argv[1]

# For single lang:
#language = input('Type language name: ')

languagenames = (language, )


# For corpus:
#languagenames = ('aari', 'afar', 'alaaba', 'alagwa', 'akkadian-ob', 'arabic', 'arbore', 'awngi', 'bayso', 'beja-alm', 'beja-hud', 'beja-rei', 'beja-rop', 'beja-van', 'beja-wed', 'berber-ghadames', 'bilin', 'boni-jara', 'boni-kijee-bala', 'boni-kilii', 'burji-sas', 'burji-wed', 'burunge', 'coptic-sahidic', 'dahalo', 'dhaasanac', 'dizi', 'egyptian-middle', 'elmolo', 'gawwada', 'gedeo', 'geez', 'hadiyya', 'hausa', 'hdi', 'hebrew', 'iraqw', 'kambaata', 'kemant', 'khamtanga', 'koorete', 'maale', 'mubi', 'oromo', 'rendille', 'saho', 'shinassha', 'sidaama', 'somali', 'syriac', 'tsamakko', 'wolaytta', 'yaaku', 'yemsa')

# Have decided to put all pdgm labels with full pdgm info in
# central db file. Other options:
#   1) make label->pdgm dict for each language
#   2) put label->pdgm in SQL database
for lang in languagenames:
     print(str('LANG: ' + lang))
     lfile = str('../aama-data/data/' + lang + '/' + lang + '-pdgms.json')
     jdata = json.load(open(lfile))
      # Lists 'pnames' for display in reference pdgm selection list.
     # Gives the 'common' values for each reference pdgm, and indicates the
     # pdgm's props hthat are not the 'default' 'number person gender'

     # File with pdgm 'names' for pdgm display pick list
     outfile1 = str('pvlists/' + lang + '-pdgm-values.txt')
     # NEW
     outfile2 = str('pvlists/' + lang + '-pdgm-props.txt')


     # 'tcprops' = ordered list of all properties, formal + morphosyntactic
     # occurring in termcluster.common section. Read in from json file
     tcprops = jdata['pdgmPropOrder']
 
    # NEW list of propsets
     psetslist = []

     print('tcprops:')
     print(str(tcprops))
     #pdgmdict = ''
     #pdgmlabels = ''
     #pprops = ''
     # These  will combine to form the outfile1 repo (for plabel display)
     pvallexlist = []
     pvalmphlist = []
     # get the number of pdgms in the file
     tccount = len(jdata['termclusters'])
     print(str('tccount:' + str(tccount))) 
     for i in range(tccount):
          tccommon = jdata['termclusters'][i]['common']
          sel =  jdata['termclusters'][i]['terms'][0]
          tpltcc = list(tccommon.items())
          #print(str('tpltcc: ' + str(tpltcc)))
          cpropset = set()
          tpropset = set()
          propsetlabel = ""
          for tup in tpltcc:
               #property = tup(0)
               #if property == 'pos':
                   
               propsetlabel = "property"
               cpropset.add(tup[0])
          for term in sel:
               if not "token" in term:
                    tpropset.add(term)
          ctpropset = cpropset | tpropset
          match = 0
          # Compare this propset with all the previous ones
          for i in range(len(psetslist)):
               if ctpropset == psetslist[i]:
                    match = 1  # seen this
                   # 'BREAK' [OR SET OF SETS???
          # If it hasn;t found a match, add it to the psetslist
          if match == 0:    # we've got a new proplist
               # Give it a label
               ctproplist = sorted(list(ctpropset))
               ctproplist.insert(0,propsetlabel)
               psetslist.append(ctproplist)
     # Now print psetslist using propset label as key
     print(str("\nProperty Sets in " + lang + ":"))
     #sorted_list = sorted(list_of_lists, key=itemgetter(1))
     sorted_psetslist = sorted(psetslist, key = itemgetter(1))
     #print(sorted_psetslist)
     for i in range(len(sorted_psetslist)):
          label = sorted_psetslist[i].pop(0)
          print(str(label + ': ' +  str(sorted_psetslist[i])))
               
     #genhead = "+++++++++++++++++\nPARADIGM-INFO\n+++++++++++++++++\n"
     #langinfo = "Language\nSource\nTranscription\n"
     #lexhead = "+++++++++++++++++\nPARADIGMS-LEXICAL\n+++++++++++++++++\n"
     #mphhead = "\n+++++++++++++++++++++++\nPARADIGMS-MORPHOTACTIC\n+++++++++++++++++++++++\n"
     #pvals = str(genhead + langinfo + lexhead + pvalslex + mphhead + pvalsmph)
     ##file = open(outfile2, "w")
     ##file.write(str(pvals))
     ##file.close()


'''
EDIT THIS FILE TO ELIMINATE VARS THAT ONLY CONTRIBUTE TO OUTFILES 2,3,4
     #PRINT(STR("PVALS: " + LANG))
     #PRINT(STR(PVALS))
     #PRINT(STR("PDGMDICT: " + LANG))
     #PRINT(STR(PDGMDICT))
     # PDGM-PROPS
     FILE = OPEN(OUTFILE2, "W")
     FILE.WRITE(STR(PPROPS))
     FILE.CLOSE
     # PDGM-PROPVALS
     FILE = OPEN(OUTFILE3, "W")
     FILE.WRITE(STR(PDGMDICT))
     FILE.CLOSE()
     # PDGM LABELS
     FILE = OPEN(OUTFILE4, "W")
     FILE.WRITE(STR(PDGMLABELS))
     FILE.CLOSE
NOTE: SCRIPT WHICH GENERATES THESE FILES SCRIPT-BCK/PDGMDICT-NEWLISTS.PY



VERB,MORPH-STEMFORMBASENASAL,BASE,NASEXT,SUFFIX
%TAM,POLARITY,PNGFORM ,TOKEN% 
= 
LANGUAGE:DHAASANAC,POS:VERB,MORPHCLASS:STEMFORMBASENASAL,DERIVEDSTEM:BASE,DERIVEDSTEMAUG:NASEXT,CONJCLASS:SUFFIX
%TAM,POLARITY,PNGFORM ,TOKEN%





BAD:

PVALS: VERB,MORPH-STEMFORMBASE_NASEXT,BASE_NASEXT,SUFFIX%TAM,POLARITY,PNGFORM

PPROPVAL = PDGMDB[PVALS] # GET THE FULL PROP-VAL STRING

'''
