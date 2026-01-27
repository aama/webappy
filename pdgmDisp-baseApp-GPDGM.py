#!/usr/local/bin/python3

'''
Basic display of 'generalized paradigms' (GPDGM) using tkinter.
On the distinction PDGM ~ GPDGM cf. application intrductiono. But
briefly, by PDGM we mean  the
traditional (Varronic) morphological paradigm set (e.g. the 'Paradigm 
Appendix' of traditional grammars), which consists of, say, for the verb, a
systematic and exhaustive presentation of the possible combinations of 
inflection class, polarity, tense, mood, etc. giving for each possible 
category combination the 'Person-Number-(Gender)' forms of the 
paradigmatic lexical item.
Comma-separted strings of property values in listbox are keys to full 
pdgm-defining prop:val strings (pvstrings/pdgm-dict-LANG.py). SPARQL query
for pdgm  derived from that in pdgmDisp.query. Widgets and grid modeled 
on Mark Roseman, Modern Tkinter -- cf. esp. pp. 67-70.
NOTE: In this one-frame version of pdgmDispUI, paradigm and res
[=SPARQL query formed in pdgmDisp.query()] are inserted into the Tk text
 widgets lpdgm and lquery.

Present [08/27/25] variants are:
pdgmDispui-baseApp.py -- basic display of pdgms and combination in
     pivot tables
(pdgmDispui-baseApp2.py -- experimenting with pivot tables)
pdgmDispui-baseApp3.py -- given set of property-value pairs, what form
     do these have for values of another set of properties. E.g. forms
     for different values of 'tam' in 3sgM verb formms in different
     conjugation classes
pdgmDispui-baseApp4.py -- same as above, but with possibility of 
     restrictting  values of properties to subset (to get manageable
     table).

'''

from tkinter import *
from tkinter import ttk
from SPARQLWrapper import SPARQLWrapper, JSON
from tabulate import tabulate
import pandas as pd
from pandas import Series, DataFrame
from io import StringIO
from IPython.display import display
from pdgmDispQuery import query, sourcequery, pinfoquery
#import for pdgm-display querimport pdgmDispQuery    
#import for pdgm-display query code
import shelve
from pprint import pprint
# import re


f = ('times',16) #'the pleasing font'

 
# Called when the selection in the lbox1 changes; figure out
# which language is currently selected, and then lookup its lcode,
# and from that, its lfile.  As well, clear the selected pdgmmessage, 
# so it doesn't stick around after we start doing
# other things.
def showLfile(*args):
    idxs = lbox.curselection()
    if len(idxs) == 1:
        idx = int(idxs[0])

        lname = languagenames[idx]
        Lname = lname.capitalize()
        #lmsg1.set("%s paradigms:" % Lname)
        mmsg.set("%s morphological props:[vals] list:" % Lname)
        lmsg.set(lname)
        # [08/26/22: get "pdgmPropOrder" value to display
        # at head of pdvals
        lfilename = str("pvlists/" + lname + "-pdgm-values.txt")
        mfilename = str("pvlists/" + lname + "-pdgm-PVN.txt")
        lfile = open(lfilename, "r")
        pdvals = lfile.read()
        mfile = open(mfilename, "r")
        mvals = mfile.read()
        #Following if want to have separate prop-order entry
        # mvals3t = mvals.partition('Paradigm_Property_Order:')
        # mvar.set(mvals3t[0]])
        # ovar = mvals3t[2]
        # omsg.set("(pdgm-name prop order: %s)" % ovar)
        #If retrieve pdgmdict from dbm
        #  pdkeys = lpdgmdict.keys()
        # works in interactive: for k in lpdgmdict.keys(): print(k, end='')
        pvar.set(pdvals)
        mvar.set(mvals)
        #minfo.insert('end',mvals)
        pmsg.set('')

# Called when the user  clicks an item in the lbox2.
def choosePdgm(*args):
    idxs = pbox.curselection()
    if len(idxs)==1:
        idx = int(idxs[0])
        lbox.see(idx)
        pname = pbox.get(idx)
        #[01/21/22] For the moment, too hard to display pname w. %.
        #Would need to be able to invoke pdgmdb at this stage,
        #something like:
        #pnameSel = pdgmdb[pname]
        # pmsg.set("PDGM: %s (# %s)" % (pname, idx))
        pmsg.set(pname)
        print(str("pmsg: " + pmsg))

#function for the pdgm-display button
def displayPInfo(*args):
    idxs = pbox.curselection()
    if len(idxs)==1:
        idx = int(idxs[0])
        lbox.see(idx)
        pinfo = pbox.get(idx)
        #[01/21/22] For the moment, too hard to display pname w. %.
        #Would need to be able to invoke pdgmdb at this stage,
        #something like:
        #pnameSel = pdgmdb[pname]
        # pmsg.set("PDGM: %s (# %s)" % (pname, idx))
        pmsg.set(pinfo)
        print("\/\/\/\/\/\/")
        print(str('\/\/\/\/\/\/ pinfo: ' + str(pinfo) + ' \/\/\/\/\/\/'))
        print("\/\/\/\/\/\/")
    pdisp.set('paradigmInfo .... ')
    pvals = pmsg.get()  #get key that user selected
    print(str("pvals: " + pvals))
    l = str(lmsg.get())
    print(str("lmsg: " + l))
    # Cf. overlap of guipdgm(), ll.89-160 w. pdgmCombine() 250-310
    # Combine into one function?
    print(str("\nPINFO DOMAIN':\n    " + pvals))

    if pvals == 'Language':
        displayLInfo()
    elif pvals == 'Source':
        displaySInfo()
    elif pvals == 'Transcription':
        displayTInfo()
    else:
        displayPDGM()

def displayLInfo(*args):
    # Set up for queries
    sparql = SPARQLWrapper("http://localhost:3030/aama/query")
    l = str(lmsg.get())
    Lang = l.capitalize()
    linfo = (str("Language Information for " + Lang + ":\n"))
    print(linfo)
    pinfo = "subfamily,geodemoURL,geodemoTxt"
    res = pinfoquery(pinfo,l)
    print(res)
    sparql.setQuery(res)
    sparql.setReturnFormat(JSON)
    result = sparql.query().convert() # JSON converted output
    #print("result:")
    #print(result)
    select = result["head"]["vars"]
    print("select:")
    print(select)
    print("\n")
    results = result["results"]["bindings"]
    #print("results:")
    #print(results)
    #print("\n\n")
    for result in results:
        valuerow = []
        for sel in select:
            if sel in result:
                selval = result[sel]["value"]
                selValue = str(sel + ": " + selval)
                print(selValue)
                linfo = str(linfo + selValue + "\n")
                #valuerow.append(selval)
                #print(str("valuerow: " + str(valuerow) + "\n"))
    print(str("linfo:\n" + linfo + "\n"))
    lpdgm.insert('end', linfo)
    lpdgm.insert('end', "\n")


def displaySInfo(*args):    
    sparql = SPARQLWrapper("http://localhost:3030/aama/query")
    l = str(lmsg.get())
    Lang = l.capitalize()
    sinfo = (str("Source Information for " + Lang + ":\n"))
    print(sinfo)
    pinfo = "dataSource,dataSourceNotes"
    res = pinfoquery(pinfo,l)
    print(res)
    sparql.setQuery(res)
    sparql.setReturnFormat(JSON)
    result = sparql.query().convert() # JSON converted output
    #print("result:")
    #print(result)
    select = result["head"]["vars"]
    print("select:")
    print(select)
    print("\n")
    results = result["results"]["bindings"]
    #print("results:")
    #print(results)
    #print("\n\n")
    for result in results:
        valuerow = []
        for sel in select:
            if sel in result:
                selval = result[sel]["value"]
                selValue = str(sel + ": " + selval)
                print(selValue)
                sinfo = str(sinfo + selValue + "\n")
                valuerow.append(selval)
                #print(str("valuerow: " + str(valuerow) + "\n"))
    print(str("sinfo:\n" + sinfo + "\n"))
    lpdgm.insert('end', sinfo)
    lpdgm.insert('end', "\n")


def displayTInfo(*args):    
    sparql = SPARQLWrapper("http://localhost:3030/aama/query")
    l = str(lmsg.get())
    Lang = l.capitalize()
    tinfo = (str("Transcription Information for " + Lang + ":\n"))
    print(tinfo)
    pinfo = "Consonants,Vowels,Prosody"
    res = pinfoquery(pinfo,l)
    print(res)
    sparql.setQuery(res)
    sparql.setReturnFormat(JSON)
    result = sparql.query().convert() # JSON converted output
    #print("result:")
    #print(result)
    select = result["head"]["vars"]
    print("select:")
    print(select)
    print("\n")
    results = result["results"]["bindings"]
    #print("results:")
    #print(results)
    #print("\n\n")
    for result in results:
        valuerow = []
        for sel in select:
            if sel in result:
                selval = result[sel]["value"]
                selValue = str(sel + ": " + selval)
                print(selValue)
                tinfo = str(tinfo + selValue + "\n")
                valuerow.append(selval)
                #print(str("valuerow: " + str(valuerow) + "\n"))
    print(str("tinfo:\n" + tinfo + "\n"))
    lpdgm.insert('end', tinfo)
    lpdgm.insert('end', "\n")

def displayPDGM(*args):   
    pvals = pmsg.get()  #get key that user selected
    print(str("pvals: " + pvals))
    l = str(lmsg.get())
    print(str("lmsg: " + l))
    sfile = str('pvlists/' + l + '-pdgmdb')
    print("sfile = ")
    print(sfile)
    # get pvalue from pkey in (unshelved) pdgmdb
    pdgmdb = shelve.open(sfile) # open it
    ppropval = pdgmdb[pvals] # get the full prop-val string
    pdgmdb.close()  # close it right away
    #print(str('ppropval: ' + ppropval))

    # WARNING! THIS VERSION PRESUPPOSES THAT NON-DEFAULT
    # VALSTRING WILL BE SEPARATED BY SIMPLE '-', NOT '%'
    # Back to '%' [101822]
    if "%" in ppropval:
        propsel = ppropval.split("%")
        pvalue = propsel[0]
        valstring = propsel[1]
    else:
        pvalue = ppropval
        valstring = "number,person,gender,token,token-note"

    # possible test for existence of pval (not used here)
    #check character    #if so display it

    # Print pvalue to terminal
    print("\nParadigm Common Property-Value Pairs:")
    pvlist = pvalue.split(",")
    for pv in pvlist:
        print(str("    " + pv))

    print("\nN.B.: For the moment, 'source' and 'pdgm' are obtained \nby two different queries from two different query functions:\n")

    # Set up for queries
    sparql = SPARQLWrapper("http://localhost:3030/aama/query")

    # 1.) Get SPARQL query for source
    svalstring = "note,lexeme,gloss"

    print("1. SPARQL QUERY for 'note,lexeme,gloss':")
    print(str("   Query Output Property: " + svalstring))

    sres = sourcequery(pvlist,svalstring,l)

    print(sres)
    sparql.setQuery(sres)
    sparql.setReturnFormat(JSON)
    sresult = sparql.query().convert() # JSON converted output
    #print('sresult: ' + str(sresult))
    sresult2 = sparql.query() # raw outpuut
    sresults = sresult['results']['bindings']
    print('sresults: ' + str(sresults))

    #print('sr: ' + str(sr))
    note = sresults[0]['note']['value']
    lexeme = sresults[0]['lexeme']['value']
    gloss = sresults[0]['gloss']['value']
    
    # Note always has a 'source' reference
    # if 'note' contains '::', part after '::' is 'comment'
    source = ''
    comment = ''
    template = ''
    if ' :: ' in note:
        notelist = note.split(' :: ')
        source = notelist[0]
        commentTemplate = notelist[1]
    else:
        source = note
        commentTemplate = ''
    if 'Template' in commentTemplate:
        commentlist = commentTemplate.split('Template')
        comment = commentlist[0]
        template = commentlist[1]
    else:
        comment  = commentTemplate
    print("Note Query Output:")
    print(str('    source: ' + source))
    print(str('    comment: ' + comment))
    print(str('    template: ' + template))
    print(str('    lexeme: ' + lexeme + ' gloss: ' + gloss))
    
    # 2.) Get SPARQL query for full pdgm  out of full prop-val
    # pdgm specification in pval
    print("\n2. SPARQL QUERY for paradigm:")
    print("pvlist: ")
    print(pvlist)
    print("valstring: ")
    print(valstring)
    res = query(pvlist,valstring,l)
    print(res)
    # else:
    #pdisp.set(str('Problem with w: ' + w))
    sparql.setQuery(res)
    sparql.setReturnFormat(JSON)
    result = sparql.query().convert() # JSON converted output
    result2 = sparql.query() # raw outpuut
    #print(str("SPARQLWrapper query URL:\n\n " + str(result2)))
    #print("SPARQLWrapper JSON-formatted output: ")
    #pprint(result)
    select  = result["head"]["vars"]
    select2 = []
    '''
    print("Select2:")
    print(select2)
    print("select: ")
    sel = valstring.replace("-","_")
    print(select)
    # create 'select' row [= header])    
    header = (",").join(select)
    header3 =  (",").join(select2)
    '''
    header = []  # for both CSV and tabular output
    paradigm = "" # this will be the CSV form output 
    paradigm2 = []  # this will be the tabular output
    results = result["results"]["bindings"]
    for result in results:
        #print(str('result:' + str(result)))
        pdgmrow = []
        pdgmrow2 = []
        for sel in select:
            #print(str('sel1: ' + sel))
            # See if 'optional' properties have yielded a value
            if sel in result:
                if sel not in header:
                    header.append(sel)
                selval = result[sel]["value"]
                #print(str('selval: ' + selval))
                # pdgmrow = str(pdgmrow + sel + "      ") 
                pdgmrow.append(selval)
                pdgmrow2.append(selval)
                # i.e.
                # number = result["number"]["value"]
                # person = resnult["person"]["value"]
                # gender = result["gender"]["value"]
                # token  = result["tokenn"]["value"]
                # pdgmrow = (str(number +  "      " + person + "     " + gender + "     " + token + "\n"))
        pdgmrowstr = (",").join(pdgmrow)
        paradigm = str(paradigm + pdgmrowstr + "\n")
        paradigm2.append(pdgmrow2)
    
    headerstr = (",").join(header)
    paradigm = str(headerstr + "\n" + paradigm)
    #print("\nparadigm2 before:")
    #print(paradigm2)
    paradigm3 = paradigm2[:]
    paradigm3.insert(0,header)
    #print("\nparadigm2:")
    #print(paradigm2)
    #pdisp.set(paradigm)
    # qdisp.set(res)

    # Update pcount and pdgmsDisp
    # Assign sequence number to paradigm
    pnum = int(pcount.get()) + 1
    # print(pnum)
    pcount.set(pnum)
    L = l.capitalize()
    plabel = str(pcount.get() + ":" + L + "," + pvals + "\n")
    pdgmDispDict[pnum] = plabel
    # Add new plabel to pdgmsDisp
    # Is it possible to add pdigm3 (as list of lists?)
    # Would have to make pdgmsDisp a dict
    disppdgms = (str(pdgmsDisp.get()) + plabel)
    pdgmsDisp.set(disppdgms)
    #print('pcount:')
    #print(pcount)    
    #print('pdgmDispDict:')
    #print(str(pdgmDispDict))
    for h in header:
        select2.append(h.upper())

    # This gives the simple CSprint("FROM WHICH . . .")
    print("\nCSV query output (from string-formatted output):\n")
    print(paradigm)
    #print("as list of lists:")
    #print(paradigm3)
    #print("paradigm2: [for tabulate]")
    #print(paradigm2)
    #print("\n")
    # This gives 'Paradigm-6' of pdgmDisp-pd.py
    pdgmtab = tabulate(paradigm2, headers = select2)
    print("\nTABLE output via 'tabulate' (from list-formatted output):\n")
    print(pdgmtab)
    print('\n')
    
    # Add 'source' and 'comment' to 'plabel'
    plabel = str(plabel + "Source: " + source + "\n")
    if len(comment) > 0:
        plabel = str(plabel + "Comment: " + comment + "\n")
    if template:
        plabel = str(plabel + "Template: " + template + "\n")
    if lexeme:
        plabel = str(plabel + "Lexeme:'" + lexeme + "', ")
    if gloss:
        plabel = str(plabel + "Gloss:'" + gloss + "'\n")
    plabel += "\n"
    # Write the pdgm(s) to the lpdgm text widget
    lpdgm.insert('end', plabel)
    #lpdgm.insert('end', "\nA-Rendered by 'tabulate':\n ")
    lpdgm.insert('end', pdgmtab)
    lpdgm.insert('end', "\n")
    lpdgm.insert('end', "\n")
    #lpdgm.insert('end', "\nB-Rendered as pandas DataFrame:\n")
    #lpdgm.insert('end', pdgmpd)
    #lpdgm.insert('end', "\n\n")
    #lpdgm.insert('end', paradigm)
    ## For this version print query only to CL interface
    #query header
    #qlabel = str(pcount.get() + ". " + ppropval + "\n")
    # ERROR: NameError: name 'lang' is not defined
    #qtext = str(qlabel + res)

    #lquery.insert('end', qtext)
    #lquery.insert('end', res)
    #lquery.insert('end', "\n")



# function for pdgm- button
def displayGPDGM(*args):
    print('===============================\n')
    lpdgm.insert('end', '\n\n===============================')
    vstring = str(forms_entry.get()) 
    valstr = str(props_entry.get())
    lang = str(lmsg.get())
    sfile = str('pvlists/' + lang + '-vpdb')
    v2pdb = shelve.open(sfile)
    vlist = vstring.split(',')
    print(str('vstring: ' + vstring))
    print(str('vlist: ' + str(vlist)))
    pvlist = []
    for val in vlist:
        print(str('val: ' + val))
        prop = v2pdb[val]
        print(str('prop: ' + prop))
        pv = str(prop + ':' + val)
        pvlist.append(pv)
    v2pdb.close()

    print(str("For Words with Property:Value Features\n: " + str(pvlist)))
    print(str("Find the forms with properties:: " + valstr))
    print(str("Language: " + lang))
    # pdgmDisp.query makes SPARQL query out of full prop-val
    # pdgm specification in pval
    res = query(pvlist,valstr,lang)
    print("The SPARQL query formed from the GPDGM list:")
    print(res)
    sparql = SPARQLWrapper("http://localhost:3030/aama/query")
    sparql.setQuery(res)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    results2 = sparql.query()
    #print("results")
    #print(results)
    #print('results2')
    #print(results2)
    select = results["head"]["vars"]
    print(str("select: " + str(select) + "\n"))
    #header =  ("    ").join(select).upper()
    header3 =  (",").join(select)
    pdgmlist = []
    pdgmstr = ""
    for result in results["results"]["bindings"]:
        #print(result)
        pdgmstr = ""
        pdgmrow = []
        for sel in select:
            #print(sel)
            if sel in result:
                if sel == 'gloss':
                    selval = str("'" + result[sel]["value"] + "'")
                else:
                    #if result[sel]:
                    selval = result[sel]["value"]
            else:
                selval = "--"
            pdgmrow.append(selval)
        print(pdgmrow)
        pdgmrowstr = (",").join(pdgmrow)
        pdgmstr = str(pdgmstr + pdgmrowstr + "\n")
        pdgmlist.append(pdgmrow)
        #print(header3)
        #print(select)
    # kludge to get desired category (number & gender) order in pivot table
    pdgmstr2 = pdgmstr.replace("Singular", " Singular")
    pdgmstr2 = pdgmstr2.replace("Masc", " Masc")
    pdgmstr2 = str(header3 + '\n' + pdgmstr2)
    #print("pdgmstr2:")
    #print(pdgmstr2)
    pdgmtab = tabulate(pdgmlist, headers=select)
    #print(str("\nselect string: " + header3))
    #print('\n')

    #print("\nThe csv ('comma-separated-value') output of the SPARQL que ry:")
    #print(str((',').join(select) + '\n' + pdgmstr + '\n'))
    print("\nFormatted version of the csv list:")
    print(pdgmtab)

    # To make pivt tables
    # First make a pandas DataFrame
    #print("\npdgmlist:")
    #print(str(pdgmlist))

    vallist = valstr.split(',')
    print("vallist:")
    print(vallist)
    #pdgmdf = pd.read_csv(StringIO(pdgmstr2))
    pdgmpd = pd.DataFrame(data=pdgmlist, columns=select)
    print("\npdgmpd")  
    print(pdgmpd)

    pivstr = str(pivot_entry.get())
    if pivstr:
        pivotlist = pivstr.split(";") 
        print(str("pivotlist: " + str(pivotlist)))
        col = pivotlist[0].split(",")
        print(str('columns: ' + str(col)))
        ndx = pivotlist[1].split(",")
        print(str('index: ' + str(ndx)))
        val = pivotlist[2]

    try:
        pdgmpdpiv = pdgmpd.pivot(columns=col,index=ndx,values=val)
    except:
        pdgmpdpiv = "[No pivot table for this data.]"

    #Alternate, more orthodox 'except'':
    #except ValueError as e:
    #    print(f"Error: {e}):

        ## Now do left-align
        ## by formatting
        #print("\nMethod4: formatting")
        #pdgmpd = pdgmpd.map(lambda x: f"{x:<12}")
        # display apparently does not get imported
        #print("pivot paradigm")
        #print(pdgmpd)
 
    ## Now insert form request and forms
    lpdgm.insert('end',str('\nLanguage: ' + lang  + '\n'))
    lpdgm.insert('end',str('For the term cluster:\n    ' + vstring  + '\n'))
    lpdgm.insert('end',str('Posible values for:\n     ' + valstr + '\n\n'))
    #lpdgm.insert('end','Table: \n')
    #lpdgm.insert('end', pdgmpd )
    #lpdgm.insert('end','\n\nPivot Table: \n')
    lpdgm.insert('end', pdgmpdpiv)
    lpdgm.insert('end', '\n\n===============================\n')


# Where is queryApply used?
def queryApply(res):
    sparql = SPARQLWrapper("http://localhost:3030/aama/query")
    sparql.setQuery(res)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    results2 = sparql.query()
    print("results")
    print(results)
    #print('results2')
    #print(results2)
    select = results["head"]["vars"]
    print("select:")
    print(select)
    #header =  ("    ").join(select).upper()

    header3 =  (",").join(select)
    pdgmstr = ""
    pdgmlist = [select,]
    for result in results["results"]["bindings"]:
        #print(result)
        pdgmrow = []
        for sel in select:
            #print(sel)
            if sel in result:
                #if result[sel]:
                selval = result[sel]["value"]
            else:
                selval = "--"
            pdgmrow.append(selval)
            print(str("pdgmrow: " + str(pdgmrow)))
        pdgmrowstr = (",").join(pdgmrow)
        pdgmstr = str(pdgmstr + pdgmrowstr + "\n")
        pdgmlist.append(pdgmrow)
    print("paradigm list:")
    print(pdgmlist)
    return pdgmlist


def makePdgmDict(*args):
    # Make a dictionary of pdgms displayed so far
    # (Can this be made part of main app?)
    disppdgms = pdgmsDisp.get()
    disppdgms2 = disppdgms.rstrip('\n')
    print('Paradigms displayed so far:')
    #print(str(disppdgms))
    print(disppdgms2)
    disppdgmslist = disppdgms2.split('\n')
    dictpdgms = {}
    for dp in disppdgmslist:
        #print(dp)
        sdp = dp.split(':')
        #print(sdp)
        #print(sdp[0])
        #print(sdp[1])
        dictpdgms[sdp[0]] = sdp[1]
    return dictpdgms

languagenames = ['aari', 'afar', 'alaaba', 'alagwa', 'akkadian-ob', 'arabic', 'arbore', 'awngi', 'bayso', 'beja-alm', 'beja-hud', 'beja-rei', 'beja-rop', 'beja-van', 'beja-wed', 'berber-ghadames', 'bilin', 'boni-jara', 'boni-kijee-bala', 'boni-kilii', 'burji-sas', 'burji-wed','burunge', 'coptic-sahidic', 'dahalo', 'dhaasanac', 'dizi', 'egyptian-middle', 'elmolo', 'gawwada', 'gedeo', 'geez', 'hadiyya', 'hausa', 'hdi', 'hebrew', 'iraqw', 'kambaata', 'kemant', 'khamtanga', 'koorete', 'maale', 'mubi', 'oromo', 'rendille', 'saho', 'shinassha', 'sidaama', 'somali', 'syriac', 'tsamakko', 'wolaytta', 'yaaku', 'yemsa']

#pcount = "1"
#print(str("pcount1 = " + pcount))

# Root and Frame
# NOTE ON WINDOW HEIGHT/WIDTH;
# Present root.geometry seems to be optimal, as far as it goes. 
# Can increase pbox and decrease lquery (and vice-versa).
# Would addition of scrollbar to lquery or lpdgm give more optioms?
root = Tk()
root.geometry('1200x1200')
root.title('Display - gPDGM')
# Configure cols and rows
# from UIa
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0,weight=1)

## Create and grid the outer content frame
cframe = ttk.Frame(root, padding=(10, 10, 22, 20))
cframe.grid(column=0, row=0, sticky=(N,W,E,S))
# from A
cframe.grid_columnconfigure(0, weight=1)
cframe.grid_rowconfigure(5, weight=1)

#following var set initially and in guipdgm() but apparently 
#never displayed
pdisp = StringVar()
# following set in showLfile() and in choosePdgm()
lmsg = StringVar()
pmsg = StringVar()
pcount = StringVar()

# pdgmsDisp is a running list of displayed pdgms
# every pdgm displayed in a session is kept here with a
# sequence ID no and its name so that its CSV can be regenerated
# from its sequence umber in the 'Combine Paradigms' box
pdgmsDisp = StringVar() # added to for each displayed pdgm
pdgmDispDict = {}

# language selection
llablgen = ttk.Label(cframe, text="Choose Language:")

llablgen.grid(column=0, row=0, padx=10, pady=5)
lnames = StringVar(value=languagenames) # one lang selected by showLfile()
lbox = Listbox(cframe, listvariable=lnames, selectmode='browse', width=50, height=5)
lbox.grid(column=0, row=1, rowspan=3, sticky=(N,S,E,W), pady=5, padx=5)

# language morphological prop-val dispay
mmsg = StringVar() # "L prop-val schema"
mlabl = ttk.Label(cframe, textvariable=mmsg, anchor=W)
mlabl.grid(column=0, row=4, sticky=(W,E))

# morophological info
mvar = StringVar() # Content of PVN file
mbox = Listbox(cframe, listvariable=mvar, selectmode='browse', width=80, height=3)
mbox.grid(column=0, row=5, rowspan=3, sticky=(N,S,E,W), pady=5, padx=5)

# chosen language-name display
lmsg1 = StringVar() # "L paradigms:"
lplabl = ttk.Label(cframe, textvariable=lmsg1, anchor=W)
lplabl.grid(column=0, row=9, sticky=(W,E))

#Following if want separate pdgm name prop order label
#omsg = StringVar() # "pname prop order"
#olabl = ttk.Label(cframe, textvariable=omsg, anchor=W)
#olabl.grid(column=0, row=10, sticky=(W,E))

# pdgms of selected language
pvar = StringVar() # List of pdgms provided by showLfile()
pbox = Listbox(cframe, listvariable=pvar, selectmode='browse', width=80, height=15)
pbox.grid(column=0, row=10, rowspan=15, sticky=(N,S,E,W), pady=5, padx=5)
# NB: the following selectmode [the correct one for Listbox, NOT 'extended']
# allows selection of multiple entries, but of course program can't use it.
# It does work here if one chooses only one,
#pbox = Listbox(cframe, listvariable=pvar, selectmode='multiple', width=100, height=15)

#pcbutton = ttk.Button(cframe, text='Choose Paradigm', command=choosePdgm, default='active')
#pcbutton.grid(column=0, row=25, sticky=W)
pdbutton = ttk.Button(cframe, text="Display PDGM", command=displayPInfo)
pdbutton.grid(column=0, row=25, sticky=W)

pvButton = ttk.Button(cframe, text="Display GPDGM:", command=displayGPDGM)
pvButton.grid(column=0, row=26, sticky=W)


# Individual pdgm display space
plabel1 = ttk.Label(cframe, text="Display:", font=f)
plabel1.grid(column=1, row=0, sticky=(N,E))
# pdgm content displayed here in text widget
lpdgm = Text(cframe, state='normal', width=80, height=25, wrap='word')
lpdgm.grid(column=2, row=0, rowspan=25, sticky=(N,S,E,W))

# Combined pdgm display
ttk.Label(cframe, text="GPDGM Specs:").grid(column=1, row=25, sticky=E)

ttk.Label(cframe, text="1.Common Vals: 'val1','val2',... ").grid(column=2, row=25,sticky=W)
forms = StringVar()
forms_entry = ttk.Entry(cframe, width=25, textvariable=forms)
forms_entry.grid(column=2, row=26, sticky=W)

ttk.Label(cframe, text="2.PDGM Props : prop1,prop2,...       ").grid(column=2, row=25,sticky=E)
props = StringVar()
props_entry = ttk.Entry(cframe, width=25, textvariable=props)
props_entry.grid(column=2, row=26, sticky=E)

ttk.Label(cframe, text="3.Output Form: colProps;ndxProp(s);valProp(s)").grid(column=2, row=27,sticky=W)
pivot = StringVar()
pivot_entry = ttk.Entry(cframe, width=25, textvariable=pivot)
pivot_entry.grid(column=2, row=27, sticky=E)


# ttk.Label(cframe, text="[Formats --  Combine: N,N,N...:Pivot,Pivot...; Template: templ-pdgm-no:data-pdgm-no]").grid(column=2, row=26, sticky=W)
'''
# Hven't been able to find out how to format/grid  more than 1 ttk.Entry
ttk.Label(cframe, text="Paradigm Pivots: ").grid(column=1, row=18, sticky=W)
pivots = StringVar()
pivots_entry = ttk.Entry(cframe, width= 10, textvariable=pivots)
pdgms_entry.grid(column=2, row=18, sticky=W)
ttk.Button(cframe, text="Pivot", command=pdgmPivot).grid(column=2,row=18, sticky=E)
'''

# For display of query text
#qdisp = StringVar()
#qlabel = ttk.Label(cframe, text="Query:", font=f)
#qlabel.grid(column=1, row=22, sticky=(N,W))
#lquery = Text(cframe, state='normal', width=80, height=15, wrap='none')
#lquery.grid(column=2, row=22, rowspan=3, sticky=(W, E))


for child in  cframe.winfo_children(): child.grid_configure(padx=5, pady=5)

# Set event bindings for when the selection in lbox1 changes,
# when the user double clicks the list, and when they hit the Return key
lbox.bind('<<ListboxSelect>>', showLfile)
lbox.bind('<Double-1>', showLfile)
root.bind('<Return>', showLfile)


# Colorize alternating lines of the lbox1
for i in range(0,len(languagenames),2):
    lbox.itemconfigure(i, background='#f0f0ff')

# Set the starting state of the interface
#  including clearing the messages.
#  Select the first language in the list; because the 
# <<ListboxSelect> event is only
# fired when user makes a change, we explicitly call showLfile.
#pmsg.set('')
lmsg1.set('')
pcount.set('0')
pdisp.set('paradigm ....')
#qdisp.set('query    ....')
lbox.selection_set(0)
showLfile()


root.mainloop()


#pos:Verb,conjClass:Prefix,clauseType:Main,lexeme:yiqiin,polarity:Affirmative,number:Singular,person:Person3,gender:Masc
 
'''
valstring:
Afar
pos:Verb,conjClass:Prefix,polarity:Affirmative,number:Singular,person:Person3,gender:Masc
pos:Verb,polarity:Affirmative,number:Singular,person:Person3,gender:Masc
conjClass:Prefix+Suffix,tam,token
Somali
pos:Verb,conjClass:Prefix,clauseType:Main,polarity:Affirmative,number:Singular,person:Person3,gender:Masc
pos:Verb,conjClass:Prefix,clauseType:Main,lexeme:yiqiin,polarity:Affirmative,number:Singular,person:Person3,gender:Masc
pos:Verb,conjClass:Suffix,clauseType:Main,polarity:Affirmative,number:Singular,person:Person3,gender:Masc
	lexeme:joogso+kari+samee+sug,tam,token 
TODO:conjSubClass,lexeme:joogso+kari+samee+sug,tam,token
Verb,Suffix,Main,Affirmative,Singular,Person3,Masc	
conjSubClass,lexeme:joogso+kari+samee+sug,tam,token
conjSubClass,lexeme;tam;token
Verb,Prefix,Main,Affirmative,Singular,Person3,Masc	
lexeme:yidi+yiil+yimi+yiqiin,gloss,tam,token
lexeme,gloss;tam;token
Verb,Main,Affirmative,Singular,Person3,Masc
conjClass,lexeme:yiil+yiqiin+joogso+sug,gloss,tam,to
conjClass,lexeme,gloss;tam;token
    # NOTE:
    # The default pivot list assumes a tripartite select-list as 
    # entered in the 'props_entry' and repeated in the 'select' list
    # which is used in the SPARQL query.  .
    # A more adequate version of the pivot list option will allow
    # user-input of the ccolumn and index options of the pivot
    # transformation.

    #Hve to be able to allow more than one value in cols/index.
    # Case in point: Somali Suffix verbw where index would be 'tam',
    # but for some 'conjSubClass' a few tam are represented by more than 
    # one lexeme, do that a 2-dimensional columns section is necessary.
    # So: give Dataframe for all, then pivot table if possible, (gracefuL) 
    # error# message otherwise.

    # Try:  pos:Verb,conjClass:Suffix,clauseType:Main,polarity:Affirmative,number:Singular,person:Person3,gender:Masc
    # conjSubClass,tam,token  VS. lexeme,tam,token

 
    v2pDict = str('pvlists/' + lang + '-' + 'v2p.dict')
    dictValProp = open(v2pDict)
    vlist= vstring.split(',')
    pvlist = []
    for val in vlist:
        prop = dictValProp[val]
 
        pv = str(prop + ':' + val)
        pvlist.append(pv)
'''
