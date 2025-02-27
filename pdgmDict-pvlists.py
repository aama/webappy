#!/usr/local/bin/python3
'''
Makes two 'list' files and two 'dict' files, and associated mdb files
out of the termcluster's 'common' sections : 
  pdgm-values: for common value display in list boxes. Uses prop-
               list given in pdgmPropOrder if given, otherwise
               'default'. 
  pdgm-props: gives common prop:val pairs, plus '%' and pdgm-prop vars
  pdgm-propvals: maps pdgm-values strings onto pdgm-props
               (plus '%' + prop-vars if NOT number-person-gender-token)
  pdgmdb: db file associated with pdgm-propvals
  pdgm-label: gives propval list associated with each pdgm label
  labldb: db file assicated with pdgm-label
  pdgmdb: db file for mapping of val-string to propval string, 
----------------
04/04/24 - going back to separating lexical and morphotactic pdgms in pdgm-values.txt; append 'morph-' instead of 'morph' to pdgmvals 
'''

import json
import shelve
import sys
#def pdgmidx(lang)

# For CL argument
language = sys.argv[1]

# For single lang:
#language = input('Type language name: ')

languagenames = (language, )


# For corpus:
#languagenames = ('aari', 'afar', 'alaaba', 'alagwa', 'akkadian-ob', 'arabic', 'arbore', 'awngi', 'bayso', 'beja-alm', 'beja-hud', 'beja-rei', 'beja-rop', 'beja-van', 'beja-wed', 'berber-ghadames', 'bilin', 'boni-jara', 'boni-kijee-bala', 'boni-kilii', 'burji', 'burunge', 'coptic-sahidic', 'dahalo', 'dhaasanac', 'dizi', 'egyptian-middle', 'elmolo', 'gawwada', 'gedeo', 'geez', 'hadiyya', 'hausa', 'hdi', 'hebrew', 'iraqw', 'kambaata', 'kemant', 'khamtanga', 'koorete', 'maale', 'mubi', 'oromo', 'rendille', 'saho', 'shinassha', 'sidaama', 'somali', 'syriac', 'tsamakko', 'wolaytta', 'yaaku', 'yemsa')

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

     # Possible to combine following two?
     # 1. db file with full p:v equivalence for v,v,... (= 'pdggm name')
     # [used in pdgmDispUI-ltsource.py]
     mdbfile = str('pvlists/' + lang + '-pdgmdb')
     # 2. db file with full p:v equivalence for lng-v-v-... ( = 'pdgm label')
     # [used in pdgmDispUI-formsearch.py]
     ldbfile = str('pvlists/' + lang + '-labldb')

     shelffile1 = shelve.open(mdbfile)
     shelffile2 = shelve.open(ldbfile)

     # 'tcprops' = ordered list of all properties, formal + morphosyntactic
     # occurring in termcluster.common section. Read in from json file
     tcprops = jdata['pdgmPropOrder']
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
         # read-in 'common' section
         plabel = jdata['termclusters'][i]['label']
         # print(str('plabel= ' + plabel))
         tccommon = jdata['termclusters'][i]['common']
         tpltcc = list(tccommon.items())
         #print(str('tpltcc: ' + str(tpltcc)))
         # Check that all props in tccommon are covered vy
         # tcprops. If not, add them at the end.
         if tcprops != ["default"]:
              for tup in tpltcc:
                   if tup[0] not in tcprops:
                        tcprops.append(tup[0])
                        print(str('NEW TCPROP!: ' + str(tup[0])))
         pdgmvals = []
         pdgmpropvals = []
         # NEED TO DECIDE IF FOLLOWING IS NECESSARY [101822]
         # If so have to change conventions about '-'
         # Initialize pdgmpropvals list with language
         # [unless do this already with tpltcc]
         # Could also add lang to pdgmvals, but not clear
         # at this point that that would be necessary
         langprop = str("language:" + lang)
         pdgmpropvals.append(langprop)
         lexval = ''
         # for val put tup[1] in list
         # for propval put tuples in list in format tup[0]:tup[1] ('prop:val')
         # In following, non-default option simmply puts (prop:)value in
         # tcprops order, but writes 'morph' if this is a 'morphClass' pdgm;
         #otherwise takes default (= alphabretic) order,
         # but puts pos at head and lexeme at tail
         # NB tcprops ["default"] means that no pdgmPropOrder specified.
         if tcprops != ["default"]:
              for prop in tcprops:
                   for tup in tpltcc:
                        if tup[0] == prop:
                             if tup[0] ==  'morphClass':
                                  pdgmvals.append(str('morph-' + tup[1]))
                                  pdgmpropvals.append(str(tup[0] + ":" + tup[1]))
                             else:
                                  pdgmvals.append(str(tup[1]))
                                  pdgmpropvals.append(str(tup[0] + ":" + tup[1]))
         else:
               for tup in tpltcc:
                    if tup[0] == 'pos':
                         pdgmvals.insert(0,str(tup[1]))
                         pdgmpropvals.insert(0,str(tup[0] + ":" + tup[1]))
                    elif tup[0] ==  'lexeme':
                         lexval = str(tup[1])
                    elif tup[0] ==  'morphClass':
                         pdgmvals.append(str('morph-' + tup[1]))
                         pdgmpropvals.append(str(tup[0] + ":" + tup[1]))
                    else:
                         pdgmvals.append(str(tup[1]))
                         pdgmpropvals.append(str(tup[0] + ":" + tup[1]))
               if lexval:
                    pdgmvals.append(lexval)
                    pdgmpropvals.append(str('lexeme:' + lexval))

                      
         #print(str(pdgmvals))
         # read sel from row-0 of 'terms'
         sel =  jdata['termclusters'][i]['terms'][0]
         # if not default (num,pers,gen,token), add to pval list
         # selprops used only if want non-default sel in pdgm list
         selprops = ''
         #selprops2 = str("%" + ",".join(sel) + "%")
         # Test whether sel is a subset of the default png pdgm selset
         pngselset = {'number', 'person', 'gender', 'token', 'token-note'}
         selset = set(sel)
         # If the props of sel not all contained in pngselset
         if not selset <= pngselset:
             selprops = str("%" + ",".join(sel) + "%")
         # do defaullt lists
         ppvstring = ','.join(pdgmpropvals)
         # with ALL %
         #ppvstring2 = str(ppvstring + selprops2)
         # with only non-default %
         ppvstring = str(ppvstring + selprops)
         # following version if want non-default sel in pdgm list
         pvalstring = str(','.join(pdgmvals) + selprops)
         # else, list with NO %
         #pvalstring = (','.join(pdgmvals))
         #pdgmlabels += str('"' + plabel + '": "' + ppvstring + '",\n')
         #pdgmdict += str('"' + pvalstring + '": "' + ppvstring + '",\n')
         if 'morph-' in pvalstring:
              pvalmphlist.append(pvalstring)
         else:
              pvallexlist.append(pvalstring)
         #pprops += str(' ' + ppvstring2 + '\n')
         #print(str(pvalstring + ' = ' + ppvstring))
         #print(str(plabel + ' = ' + ppvstring))
         shelffile1[pvalstring] = ppvstring
         shelffile2[plabel] = ppvstring
         # print(str(pvalstring + ' = ' + ppvstring))
         
     shelffile1.close()
     shelffile2.close()
     # combine pvalmphlist and pvallexlist into file with sorted pvals
     pvallexsort = sorted(pvallexlist)
     pvalmphsort = sorted(pvalmphlist)
     pvalslex = '\n'.join(pvallexsort)
     pvalsmph = '\n'.join(pvalmphsort)
     pvals = ''
     lexhead = "+++++++++++++++++\nPARADIGMS-LEXICAL\n+++++++++++++++++\n"
     mphhead = "\n+++++++++++++++++++++++\nPARADIGMS-MORPHOTACTIC\n+++++++++++++++++++++++\n"
     pvals = str(lexhead + pvalslex + mphhead + pvalsmph)
     file = open(outfile1, "w")
     file.write(str(pvals))
     file.close()

'''
Edit this file to eliminate vars that only contribute to outfiles 2,3,4
     #print(str("pvals: " + lang))
     #print(str(pvals))
     #print(str("pdgmdict: " + lang))
     #print(str(pdgmdict))
     # pdgm-props
     file = open(outfile2, "w")
     file.write(str(pprops))
     file.close
     # pdgm-propvals
     file = open(outfile3, "w")
     file.write(str(pdgmdict))
     file.close()
     # pdgm labels
     file = open(outfile4, "w")
     file.write(str(pdgmlabels))
     file.close
NOTE: script which generates these files script-bck/pdgmDict-newlists.py



Verb,morph-StemFormBaseNasal,Base,NasExt,Suffix
%tam,polarity,pngform ,token% 
= 
language:dhaasanac,pos:Verb,morphClass:StemFormBaseNasal,derivedStem:Base,derivedStemAug:NasExt,conjclass:Suffix
%tam,polarity,pngform ,token%





BAD:

pvals: Verb,morph-StemFormBase_NasExt,Base_NasExt,Suffix%tam,polarity,pngform

ppropval = pdgmdb[pvals] # get the full prop-val string

'''
