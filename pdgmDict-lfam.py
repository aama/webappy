#!/usr/local/bin/python3
'''
Makes sorted list of LANG-pdgms.json 'subfamily' (or other) entries
'''

import json


# For corpus:
languagenames = ('aari', 'afar', 'alaaba', 'alagwa', 'akkadian-ob', 'arabic', 'arbore', 'awngi', 'bayso', 'beja-alm', 'beja-hud', 'beja-rei', 'beja-rop', 'beja-van', 'beja-wed', 'berber-ghadames', 'bilin', 'boni-jara', 'boni-kijee-bala', 'boni-kilii', 'burji', 'burunge', 'coptic-sahidic', 'dahalo', 'dhaasanac', 'dizi', 'egyptian-middle', 'elmolo', 'gawwada', 'gedeo', 'geez', 'hadiyya', 'hausa', 'hdi', 'hebrew', 'iraqw', 'kambaata', 'kemant', 'khamtanga', 'koorete', 'maale', 'mubi', 'oromo', 'rendille', 'saho', 'shinassha', 'sidaama', 'somali', 'syriac', 'tsamakko', 'wolaytta', 'yaaku', 'yemsa')

outfile  = 'AAMA-subfam.json'


subfams = []

for lang in languagenames:
     #print(str('LANG: ' + lang))
     lfile = str('../aama-data/data/' + lang + '/' + lang + '-pdgms.json')
     jdata = json.load(open(lfile))
     family = jdata['subfamily']
     # add 'family' to subfams set
     if family not in subfams:
          subfams.append(family)
sortfams = sorted(subfams)
print(sortfams)
file = open(outfile, "w")
file.write(str(sortfams))

