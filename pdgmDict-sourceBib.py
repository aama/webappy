#!/usr/local/bin/python3
'''
Makes csv file: ['fam', 'lang', 'source'] for each L.
List will then be edited by hand.

'''

import json

'''
# For corpus:
languagenames = ['aari', 'afar', 'alaaba', 'alagwa', 'akkadian-ob', 'arabic', 'arbore', 'awngi', 'bayso', 'beja-alm', 'beja-hud', 'beja-rei', 'beja-rop', 'beja-van', 'beja-wed', 'berber-ghadames', 'bilin', 'boni-jara', 'boni-kijee-bala', 'boni-kilii', 'burji-sas', 'burji-wed', 'burunge', 'coptic-sahidic', 'dahalo', 'dhaasanac', 'dizi', 'egyptian-middle', 'elmolo', 'gawwada', 'gedeo', 'geez', 'hadiyya', 'hausa', 'hdi', 'hebrew', 'iraqw', 'kambaata', 'kemant', 'khamtanga', 'koorete', 'maale', 'mubi', 'oromo', 'rendille', 'saho', 'shinassha', 'sidaama', 'somali', 'syriac', 'tsamakko', 'wolaytta', 'yaaku', 'yemsa']


# cushitic-motic
languagenames = ['aari', 'afar', 'alaaba', 'alagwa', 'arbore', 'awngi', 'bayso', 'beja-alm', 'beja-hud', 'beja-rei', 'beja-rop', 'beja-van', 'beja-wed', 'bilin', 'boni-jara', 'boni-kijee-bala', 'boni-kilii', 'burji-sas', 'burji-wed', 'burungi', 'dahalo', 'dhaasanac', 'dizi', 'elmolo', 'gawwada', 'gedeo', 'hadiyya', 'iraqw', 'kambaata', 'kemant', 'khamtanga', 'koorete', 'maale', 'oromo', 'rendille', 'saho', 'shinassha', 'sidaama', 'somali', 'tsamakko', 'wolaytta', 'yaaku', 'yemsa']
'''

#  For individual language(s)
lnames = input('Type comma-separated list of language names: ')
print(str("lnames: " + lnames))


outfile = str('AAMA Source Bibliography' + lnames + '.txt')
languagenames = lnames.split(',')
sourceColl = []
for lang in languagenames:
     print(str('LANG: ' + lang))
     lfile = str('../aama-data/data/' + lang + '/' + lang + '-pdgms.json')
     jdata = json.load(open(lfile))
     family = jdata['subfamily']
     source = jdata['datasource']
     entry = str(family + ' :: ' + lang + ':\n' + source + '\n[format:\n\n')
     sourceColl.append(entry)
sortedSource =  sorted(sourceColl)
sourcevals = '\n'.join(sortedSource)

file = open(outfile, "w")
file.write(str(sourcevals))
file.close()

'''
    {
      "label": "brn-Selector",
      "note": "K94s7.2.5.7 ::  [REV: :subjSel :nmbObj :prsObj :gndObj]",
      "common": {
        "pos": "Selector",
        "tenseSel": "Future2"
      },
      "terms": [
        ["subjSel" ,"nmbObj" ,"prsObj" ,"gndObj" ,"token"],
        ["P1_2Subj" ,"Singular" ,"Person1" ,"Common" ,"hanimaa"],
        ["P1_2Subj" ,"Singular" ,"Person2" ,"Masc" ,"hagumaa"],
        ["P1_2Subj" ,"Singular" ,"Person2" ,"Fem" ,"hagimaa"],
        ["P1_2Subj" ,"Singular" ,"Person3" ,"Masc" ,"hagumaa"],
        ["P1_2Subj" ,"Singular" ,"Person3" ,"Fem" ,"hagamaa"],
        ["P1_2Subj" ,"Plural" ,"Person1" ,"Common" ,"handimaa"],
        ["P1_2Subj" ,"Plural" ,"Person2" ,"Common" ,"hangumaa"],
        ["P1_2Subj" ,"Plural" ,"Person3" ,"Common" ,"hagimaa"],
        ["P3Subj" ,"Singular" ,"Person1" ,"Common" ,"hinimaa"],
        ["P3Subj" ,"Singular" ,"Person2" ,"Masc" ,"hugumaa"],
        ["P3Subj" ,"Singular" ,"Person2" ,"Fem" ,"higimaa"],
        ["P3Subj" ,"Singular" ,"Person3" ,"Masc" ,"higumaa"],
        ["P3Subj" ,"Singular" ,"Person3" ,"Fem" ,"higamaa"],
        ["P3Subj" ,"Plural" ,"Person1" ,"Common" ,"hindimaa"],
        ["P3Subj" ,"Plural" ,"Person2" ,"Common" ,"hungumaa"],
        ["P3Subj" ,"Plural" ,"Person3" ,"Common" ,"higimaa"]
      ]
    },

'''

