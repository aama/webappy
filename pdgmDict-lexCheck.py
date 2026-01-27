#!/usr/local/bin/python3
'''
Make list of paradigm lexemeswith missing glosses (whose gloss is 
'[x]' or '[y]'). Can be generalized to other lexical properties.
'''
import json
import sys

# For CL argument
#language = sys.argv[1]

# For single lang:
#language = input('Type language name: ')

#languagenames = (language, )

# For corpus:
#languagenames = ('aari', 'afar', 'alaaba', 'alagwa', 'akkadian-ob', 'arabic', 'arbore', 'awngi', 'bayso', 'beja-alm', 'beja-hud', 'beja-rei', 'beja-rop', 'beja-van', 'beja-wed', 'berber-ghadames', 'bilin', 'boni-jara', 'boni-kijee-bala', 'boni-kilii', 'burji', 'burunge', 'coptic-sahidic', 'dahalo', 'dhaasanac', 'dizi', 'egyptian-middle', 'elmolo', 'gawwada', 'gedeo', 'geez', 'hadiyya', 'hausa', 'hdi', 'hebrew', 'iraqw', 'kambaata', 'kemant', 'khamtanga', 'koorete', 'maale', 'mubi', 'oromo', 'rendille', 'saho', 'shinassha', 'sidaama', 'somali', 'syriac', 'tsamakko', 'wolaytta', 'yaaku', 'yemsa')

# For coma corpus:
languagenames = ('aari', 'afar', 'alaaba', 'alagwa',  'arbore', 'awngi', 'bayso', 'beja-alm', 'beja-hud', 'beja-rei', 'beja-rop', 'beja-van', 'beja-wed',  'bilin', 'boni-jara', 'boni-kijee-bala', 'boni-kilii', 'burji-wed', 'burji-sas', 'burunge',  'dahalo', 'dhaasanac', 'dizi', 'elmolo', 'gawwada', 'gedeo', 'hadiyya', 'iraqw', 'kambaata', 'kemant', 'khamtanga', 'koorete', 'maale', 'oromo', 'rendille', 'saho', 'shinassha', 'sidaama', 'somali', 'tsamakko', 'wolaytta', 'yaaku', 'yemsa')

outfileGen = str('pvlists/AAMA-findGloss.txt')
#file = open(outfileGen, "w")
#file.write(str("PDGM LEXEMES WITHOUT GLOSS: \n\n"))


for lang in languagenames:
     print(str('LANG: ' + lang))
     lfile = str('../aama-data/data/' + lang + '/' + lang + '-pdgms.json')
     jdata = json.load(open(lfile))
     # edit and turn one of the 'lex' files into 'lexemes'
     outfile = str('pvlists/' + lang + '-findGloss.txt')

     # get number of pdgms
     tccount = len(jdata['termclusters'])
     print(tccount)
     # Get lexemes out of common
     pdgmLexemes = set()
     for i in range(tccount):
          # print(str("tccount: " + str(i)))
          common = jdata['termclusters'][i]['common']
          if "lexeme" in common:
               pdgmLex = jdata['termclusters'][i]['common']['lexeme']
               # print(str(pdgmLex))
               pdgmLexemes.add(pdgmLex)

     #print(str("pdgmLexemes = " + str(pdgmLexemes)))

     # See how many of pdgm lexemes have gloss "[y]" in lexemes section
     lexGlossMissing = []
     lexSection = jdata['lexemes']
     #print(str(lexSection))
     for lex in pdgmLexemes:
         if lexSection[lex]['gloss'] == "[y]" or lexSection[lex]['gloss'] =="[x]":
             lexGlossMissing.append(lex)
     print("plexemes without gloss:")
     print(lexGlossMissing)

     if len(lexGlossMissing) > 0:
         file1 = open(outfile, "w")
         file1.write(str(lexGlossMissing))
         file2 = open(outfileGen, "a")
         file2.write(str(lang + ": " + str(lexGlossMissing) + "\n\n\n"))

'''
NOTE [08/22/24]: after 'normalization' of lexemes section by inserting
dummy entry for missing lexemes which don't show up in schemata.lexeme,
and running lexCheck. need to replace all pv/LANG-lexemes.json by
LANG-pdgms.json lexemes section.

Dummy entry: 

"": {
    "pos": "Verb",
    "lemma": "[x]",
    "gloss": "[y]"
  },
  
'''

