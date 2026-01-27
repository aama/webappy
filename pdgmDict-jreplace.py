#!/usr/local/bin/python3
'''
Script to be used as template for replacing one term in json file
with another. This script's present form replaces an old subfamily
term with another. Opens dict with 'oldfam: newfam'. Then for each 
languages file reads old fam and replaces it with newfam
AS OPPOSED TO pdgmDict-jreplace-old.py THIS VERSION GETS JSON INFO 
WITH json.load, BUT REPLACES OLD INFO USING ftext.replace(a,b), 
THUS PRESERVING JSON FORMAT
'''

import shutil
import json

# For single lang:
#language = input('Type language name: ')
#languagenames = (language, )

# For adhoc test set:
#languagenames = ('beja-alm', 'beja-hud', 'beja-rei', 'beja-rop', 'beja-van', 'beja-wed')
#sample = input('Type sample name: ')

# For corpus:
languagenames = ('aari', 'afar', 'alaaba', 'alagwa', 'akkadian-ob', 'arabic', 'arbore', 'awngi', 'bayso', 'beja-alm', 'beja-hud', 'beja-rei', 'beja-rop', 'beja-van', 'beja-wed', 'berber-ghadames', 'bilin', 'boni-jara', 'boni-kijee-bala', 'boni-kilii', 'burji', 'burunge', 'coptic-sahidic', 'dahalo', 'dhaasanac', 'dizi', 'egyptian-middle', 'elmolo', 'gawwada', 'gedeo', 'geez', 'hadiyya', 'hausa', 'hdi', 'hebrew', 'iraqw', 'kambaata', 'kemant', 'khamtanga', 'koorete', 'maale', 'mubi', 'oromo', 'rendille', 'saho', 'shinassha', 'sidaama', 'somali', 'syriac', 'tsamakko', 'wolaytta', 'yaaku', 'yemsa')

with open('AAMA-subfam.json') as f:
     subfams = f.read()    
repDict = json.loads(subfams)       

for lang in languagenames:
     print(str('LANG: ' + lang))
     lfile = str('../aama-data/data/' + lang + '/' + lang + '-pdgms.json')
     bckfile = str('../aama-data/data/' + lang + '/' + lang + '-pdgms-bck.json')
     shutil.copy(lfile, bckfile)

     jdata = json.load(open(lfile))
     oldfam = jdata['subfamily']
     print(str('old subfamily = ' + oldfam))
     #lfile.close

     newfam = repDict[oldfam]
     print(str('new subfamily = ' + newfam))

     with open(lfile) as f:
          ftext = f.read()
     ftext2 = ftext.replace(oldfam, newfam)
     #print(str(ftext2))

     file = open(lfile, "w")
     file.write(ftext2)
     file.close

     #f.write(str(ftext2))
     #f.close()








