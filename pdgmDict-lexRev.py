#!/usr/local/bin/python3
'''
Presumes existence of (edited) LANG-lexemes.json. 
Subs it into lang=-pdgms.jsppn file
'''

import json
import re
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
     # Assume that thta L-lex1 (from 'lexeme' section of 'schemata') 
     # and L-lex2 from 'lfile/lexemes'have been combined and and completed
     # with lex data from the L source and rewritten as  L-lexemes
     lexfile = str('pvlists/' + lang + '-lexemes.json')
     # sort lexfile
     #ldict = {}
     ldict = json.load(open(lexfile))
     #with open(lexfile) as lf:
     #     ldict = dict(lf.read())
     print("ldict:")
     print(ldict)
     dlist = list(ldict)
     print("dlist:")
     print(dlist)
     #ldict = dict(lexemes)
     #lexSort will be a sorted list of lexID
     lexSort = sorted(ldict)
     print("lexSort:")
     print(lexSort)
     lexDict = {}
     for lex in lexSort:
         lexDict[lex] = ldict[lex]
     print(lexDict)
     # Prepare replacement text
     ftext1a = str('lexemes": ' + str(lexDict) + ',\n  "pdgmPropOrder": ')
     print("ftext1a:")
     print(ftext1a)
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
     file = open(lexfile, "w")
     file.write(str(lexDict))
     file.close




