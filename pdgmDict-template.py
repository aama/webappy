#!/usr/local/bin/python3
'''
Program which takes paradigms with termcluster of form:

    "terms": [
      ["pngData" ,"token"],
      ["Bform" ,"cegesicu"],
      ["Aform" ,"yegesuu"]
    ]

and transforms it into canonical paradigm form:

   "terms": [
      ["number" ,"person" ,"gender" ,"token"],
      ["Singular" ,"Person1" ,"Common" ,"[form]"],
             . . . 
             . . .
             . . .
      ["Plural" ,"Person3" ,"Common" ,"[form]"]
     ]

following one of the two template arrays: template1, template2 
'''

import json
import sys

# For CL argument
lang = sys.argv[1]

print(str('LANG: ' + lang))
lfile = str('../aama-data/data/' + lang + '/' + lang + '-pdgms-rev.json')
outfile1 = str('pvlists/' + lang + '-termclusters-new.json')
outfile2 = str('pdgmfiles/' + lang + '-pdgms-rev.json')
jdata = json.load(open(lfile))

termclusters = []
tccount = len(jdata['termclusters'])
print(str('tccount:' + str(tccount))) 
#for i in range(tccount):
for i in range(tccount):
    # Find template-based pdgms  and transfer 'pngData' into
    # value of new 'lexForm' common preperty
    pdgm = jdata['termclusters'][i]
    if pdgm['terms'][0][0] == 'pngData':
        template1 = [
            ["number" ,"person" ,"gender" ,"pngData"],
            ["Singular" ,"Person1" ,"Common" ,"Aform"],
            ["Singular" ,"Person2" ,"Common" ,"Bform"],
            ["Singular" ,"Person3" ,"Masc" ,"Aform"],
            ["Singular" ,"Person3" ,"Fem" ,"Bform"],
            ["Plural" ,"Person1in" ,"Common" ,"Aform"],
            ["Plural" ,"Person1ex" ,"Common" ,"Bform"],
            ["Plural" ,"Person2" ,"Common" ,"Bform"],
            ["Plural" ,"Person3" ,"Common" ,"Aform"]
        ]
        template2 = [
            ["number" ,"person" ,"gender" ,"pngData"],
            ["Singular" ,"Person1" ,"Common" ,"ABform"],
            ["Singular" ,"Person2" ,"Common" ,"ABform"],
            ["Singular" ,"Person3" ,"Masc" ,"ABform"],
            ["Singular" ,"Person3" ,"Fem" ,"ABform"],
            ["Plural" ,"Person1in" ,"Common" ,"ABform"],
            ["Plural" ,"Person1ex" ,"Common" ,"ABform"],
            ["Plural" ,"Person2" ,"Common" ,"ABform"],
            ["Plural" ,"Person3" ,"Common" ,"ABform"]
        ]
        if len(pdgm['terms']) == 3:
            template = template1
            tName = 'template1'
            prop1 = pdgm['terms'][1][0]
            val1 = (pdgm['terms'][1][1])
            #prop2 - pdgm1['terms'][2][0]
            val2 = (pdgm['terms'][2][1])
            if prop1 == 'Aform':
                lexForm = (str(val1 + ',' + val2))
            else:
                lexForm = (str(val2 + ',' + val1))
        else:
            template = template2
            tName = 'template2'
            prop1 = pdgm['terms'][1][0]
            val1 = (pdgm['terms'][1][1])
            lexForm = str(val1)
        print("lexform:")
        print(lexForm)
        print("template:")
        print(tName)

        # Get lexform and lexlist
        pvcom = pdgm['common']
        pvcom['lexForm'] = lexForm
        print("pvcom['lexform']")
        print(pvcom['lexForm'])
        lexlist = lexForm.split(',')
        print("lexlist:")
        print(lexlist)

        # Substitute lex values for Aform, Bform, or ABform
        newterms = template
        newterms[0][3] = "token"
        for i in range(len(newterms)):
            if template[i][3] == 'Aform':
                newterms[i][3] = lexlist[0]
            if template[i][3] == 'Bform':
                newterms[i][3] = lexlist[1]
            if template[i][3] == 'ABform':
                newterms[i][3] = lexlist[0]
        pdgm['terms'] = newterms
        print('newterms:')
        print(newterms)

    #print("newterms:")
    #print(newterms)
    #print("terms:")
    #print(terms)
    #print("pdgm1:")
    #print(pdgm1)
    print("\nparadigm:")
    print(pdgm)
    print("\n\n")
    termclusters.append(pdgm)
jdata['termclusters'] = termclusters
#pvals = str(lang + subfamily + lpref .  . . .)
# FIND WAY TO INSERT CLUSTERS INTO LFILE
file = open(outfile1, "w")
file.write(str(termclusters))
file = open(outfile2, "w")
file.write(str(jdata))
(file remooved)
