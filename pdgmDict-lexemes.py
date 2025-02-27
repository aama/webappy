#!/usr/local/bin/python3
'''
Draws up the morphological property-values sdhemata used in the
current inventory of termclusters. It cretes two files:
1) 'pdgm-schemata-LANG.json': a full-formatted 'schemata'
   and 'pdgmPropOrder' which can be inserted in the 'pdgms-LANG.json'
   file;
2) 'pdgm-PVN-LANG.txt': with the same information, but formatted
   for insertion in various pdgm and pname displays
no. 3
'''

import json
import re
from shutil import copy
import sys

def value_getter(lexemes):
    return lexemes['label']

# For CL argument
language = sys.argv[1]

# For single lang:
#language = input('Type language name: ')

languagenames = (language, )


# For corpus:
#languagenames = ('aari', 'afar', 'alaaba', 'alagwa', 'akkadian-ob', 'arabic', 'arbore', 'awngi', 'bayso', 'beja-alm', 'beja-hud', 'beja-rei', 'beja-rop', 'beja-van', 'beja-wed', 'berber-ghadames', 'bilin', 'boni-jara', 'boni-kijee-bala', 'boni-kilii', 'burji', 'burunge', 'coptic-sahidic', 'dahalo', 'dhaasanac', 'dizi', 'egyptian-middle', 'elmolo', 'gawwada', 'gedeo', 'geez', 'hadiyya', 'hausa', 'hdi', 'hebrew', 'iraqw', 'kambaata', 'kemant', 'khamtanga', 'koorete', 'maale', 'mubi', 'oromo', 'rendille', 'saho', 'shinassha', 'sidaama', 'somali', 'syriac', 'tsamakko', 'wolaytta', 'yaaku', 'yemsa')

# NB: outfile 3 & 4, and lfilename2 are for definitive indices
# in pvlists/, outfile 1&2 and lfilename are for preliminary

for lang in languagenames:
     print(str('LANG: ' + lang))
     lfile = str('../aama-data/data/' + lang + '/' + lang + '-pdgms.json')
     lfilebck = str('../aama-data/data/' + lang + '/' + lang + '-pdgms-old.json')
     copy(lfile, lfilebck)
     jdata = json.load(open(lfile))
     # edit and turn one of the 'lex' files into 'lexemes'
     outfile1 = str('pvlists/' + lang + '-lex1.json')
     outfile2 = str('pvlists/' + lang + '-lex2.json')
     # list of lexeme labels
     pdgmLexemes = jdata['schemata']['lexeme']
     # output lexDict:what needs to be in lexeme file
     lexDict1 = {}
     for lex in pdgmLexemes:
          lexEntry = {}
          lexEntry["pos"] = "Verb"
          lexEntry["lemma"] = "[x]"
          lexEntry["gloss"] = "[y]"
          lexDict1[lex] = lexEntry
     print("pdgmLexemes:")
     print(lexDict1)
     # actual lexemex collection
     lexSection = jdata['lexemes']
     lexDict2 = {}
     lexSorted = sorted(lexSection)
     for lex in lexSorted:
         lexDict2[lex] = lexSection[lex]
     print("lexemes:")
     #print(lexSection)
     print("lexdict2")
     #print(lexDict2)
     # lexicalMaterial = lexDict | lexSection

     # Keep separate files of lex template (lex1) and current 'lexemes'
     json.dump(lexDict1, fp=open(outfile1, "w"), ensure_ascii=False, indent=2)
     json.dump(lexDict2, fp=open(outfile2, "w"), ensure_ascii=False, indent=2)

     # Replace 'lexemes' section in current updated lang file

     # First open the newly made lexemes file
     with open(outfile2) as f:
          ftext1 = f.read()

     # Prepare replacement text
     ftext1a = str('lexemes": ' + ftext1 + ',\n  "pdgmPropOrder": ')
     print("ftext1a:")
     # print(ftext1a)

     #Open 'matrix' text
     with open(lfile) as f:
          ftext = f.read()
     ftext2 = ftext.replace('\n','\\n')
     # print("ftext2")
     # print(ftext2)
    
     # Replace
     ftextnew1 = re.sub('lexemes":.*"pdgmPropOrder": ', ftext1a, ftext2)
     ftextnew2 = ftextnew1.replace('\\n','\n')
     print('ftextnew2')
     #print(ftextnew2)
     file = open(lfile, "w")
     file.write(ftextnew2)
     file.close
