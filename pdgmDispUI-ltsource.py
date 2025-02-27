
'''
Basic display of reference paradigms using tkinter.
Comma-separted strings of property values in listbox are keys to full 
pdgm-defining prop:val strings (pvstrings/pdgm-dict-LANG.py). SPARQL query
for pdgm  derived from that in pdgmDisp.query. Widgets and grid modeled 
on Mark Roseman, Modern Tkinter -- cf. esp. pp. 67-70.
NOTE: In this one-frame version of pdgmDispUI, paradigm and res
[=SPARQL query formed in pdgmDisp.query()] are inserted into the Tk text
 widgets lpdgm and lquery.

'''

from tkinter import *
from tkinter import ttk
from SPARQLWrapper import SPARQLWrapper, JSON
from tabulate import tabulate
import pandas as pd
from pandas import Series, DataFrame
from io import StringIO
from IPython.display import display
from pdgmDispQuery import query, sourcequery
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
        # print(pmsg)

#function for the pdgm-display button
def displayPdgm(*args):
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
        print("\/\/\/\/\/\/")
        print(str('\/\/\/\/\/\/ pname: ' + str(pname) + ' \/\/\/\/\/\/'))
        print("\/\/\/\/\/\/")
    pdisp.set('paradigm .... ')
    pvals = pmsg.get()  #get key that user selected
    l = str(lmsg.get())
    # Cf. overlap of guipdgm(), ll.89-160 w. pdgmCombine() 250-310
    # Combine into one function?
    sfile = str('pvlists/' + l + '-pdgmdb')
    print(str("\nPARADIGM 'NAME':\n    " + pvals))
    #print(pvals)
    #print("sfile = ")
    #print(sfile)
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
    svalstring = "note"

    print("1. SPARQL QUERY for 'note':")
    print(str("   Query Output Property: " + svalstring))

    sres = sourcequery(pvlist,svalstring,l)

    print(sres)
    sparql.setQuery(sres)
    sparql.setReturnFormat(JSON)
    sresult = sparql.query().convert() # JSON converted output
    #print('sresult: ' + str(sresult))
    sresult2 = sparql.query() # raw outpuut
    sresults = sresult['results']['bindings']
    #print('sresults: ' + str(sresults))
    sr = sresults[0]
    #print('sr: ' + str(sr))
    note = sr['note']['value']
    
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
    
    # 2.) Get SPARQL query for full pdgm  out of full prop-val
    # pdgm specification in pval
    print("\n2. SPARQL QUERY for paradigm:")
    print(str("   Query Output Properties: " + valstring))
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
    print('pcount:')
    print(pcount)    
    print('pdgmDispDict:')
    print(str(pdgmDispDict))
    for h in header:
        select2.append(h.upper())

    # This gives the simple CSV
    print("FROM WHICH . . .")
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

# function for pdgm-combine button
def pdgmCombine(*args):
    print('===============================\n')
    lpdgm.insert('end', '\n\n===============================')
    disppdgms = pdgmsDisp.get()
    disppdgms2 = disppdgms.rstrip('\n')
    print('Paradigms displayed so far:')
    #print(str(disppdgms))
    print(disppdgms2)
    disppdgmslist = disppdgms2.split('\n')
    dictpdgms = {}
    for dp in disppdgmslist:
        # print(dp)
        sdp = dp.split(':')
        #print(sdp)
        #print(sdp[0])
        #print(sdp[1])
        dictpdgms[sdp[0]] = sdp[1]
    pdgmsget = pdgms.get()
    print("pdgmsget:")
    print(pdgmsget)
    pdgmsinfo = pdgmsget.split(':')
    #print(str('Pdgm Combine Info: ' + pdgmsget))
    print(str('\nParadigms to combine: ' + pdgmsinfo[0]))
    #print(pdgmsinfo[1])
    pivot = pdgmsinfo[1]
    print(str('Pivot(s) for combined pdgms: ' + pivot))
    #lpdgm.insert('end',(str('PIVOT(S): ' + pivot + '\n')))

    # Get list of pdgms to combine
    pdgmnums = pdgmsinfo[0].split(',')
    pdgmlist = []
    pdgmstr = ""
    for i in pdgmnums:
        # Get its full specification
        pname = dictpdgms[i]
        # pop the lang and make str of pname proper
        pnamelist = pname.split(',')
        lang = pnamelist.pop(0).lower()
        pname = ','.join(pnamelist)
        print(str('\n' + i + ': ' +lang + ' ' + pname))
        # Lots of overlap ll 250-310 w. guidpgm() ll.89-160
        # Combine into one funcion?
        # get db file for lang and find prop-val version of pname
        sfile = str('pvlists/' + lang + '-pdgmdb')
        # get pvalue from pkey in (unshelved) pdgmdb
        pdgmdb = shelve.open(sfile) # open it
        ### pname not the same as used to make pdgmdb
        pvalue = pdgmdb[pname] # get the full prop-val string
        pdgmdb.close()  # close it right away
        pvlist = pvalue.split(",")
        print(str("property-value list formed from pdgm " + i + ":"))
        print(pvlist)
        #pvalue = pvalue[0:-1]
        # find sel str/list [= valstring/list]
        if "%" in pvalue:
            propsel = pvalue.split("%")
            pvalue = propsel[0]
            valstring = propsel[1]
            valstring = valstring.replace("%","")
        else:
            valstring = "number,person,gender,token"
        vallist = valstring.split(',') # = pandas row
        vallist.remove('token')        # = pandas value
        pivlist = pivot.split(',')     # = pandas col
        # XXXXXX
        valstring = str(pivot + ',' + valstring)
        # XXXXXX
        print(str('valstring: ' + valstring))
        # pdgmDisp.query makes SPARQL query out of full prop-val
        # pdgm specification in pval
        res = query(pvlist,valstring,lang)
        #print("The SPARQL query formed from the prop-val list:")
        #print(res)
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
        # print()
        #header =  ("    ").join(select).upper()
        header3 =  (",").join(select)
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
                #print(pdgmrow)
            pdgmrowstr = (",").join(pdgmrow)
            pdgmstr = str(pdgmstr + pdgmrowstr + "\n")
            pdgmlist.append(pdgmrow)
            #print(header3)
            #print(select)
    print("\npdgmlist:")
    print(str(pdgmlist))
    # kludge to get desired category (number & gender) order in pivot table
    #pdgmstr2 = pdgmstr.replace("Singular", " Singular")
    #pdgmstr2 = pdgmstr2.replace("Masc", " Masc")
    pdgmtab = tabulate(pdgmlist, headers=select)
    print(str("\nselect string: " + header3))
    #print('\n')

    print("\nThe csv ('comma-separated-value') output of the SPARQL query:")
    print(str((',').join(select) + '\n' + pdgmstr + '\n'))
    print("\nFormatted version of the csv list:")
    print(pdgmtab)
    pdgmstr2 = str(header3 + '\n' + pdgmstr)
    # Make sure that vallist and pivlist do not overlap
    print(str("vallist1: " + str(vallist)))
    print(str("pivlist1: " + str(pivlist)))
    for i in vallist:
        if i in pivlist:
            vallist.remove(i)
   
    # Turn it into a pandas dataform
    pdgmpd = pd.read_csv(StringIO(pdgmstr2))
    print("\nPDGMS as pandas pd -- pdgmpd:")
    print(pdgmpd)

    # Then 'pivot' on designated properties with pandas pivot()
    # For 'missing values' in pivot (with unstack):
    # The missing value can be filled with a specific value with the 
    # fill_value argument -- e.g. 'df3.unstack(fill_value=-1e9)'
    # https://pandas.pydata.org/docs/user_guide/reshaping.html

    #pivlists = vallist + pivlist
    print(str("vallist2: " + str(vallist)))
    print(str("pivlist2: " + str(pivlist)))

    pdgmpiv1 = pdgmpd.pivot(index=vallist, columns=pivlist, values='token').reset_index()
    pdgmpiv2 = pdgmpd.pivot(index=vallist, columns=pivlist, values='token')
    pdgmpiv2.columns.name=None

    # Get things ordered
    ppiv1 = pdgmpiv1.sort_values(by=['number','person','gender'], ascending=[False,True,False])
    ppiv2 = pdgmpiv2.sort_values(by=['number','person','gender'], ascending=[False,True,False])

    print("\nCombined: paradigm dataform pivoted on 'token' (with index):")
    print(ppiv1)
    print("\n w/o index:")
    print(ppiv2)

    ## Now do left-align
    ## by formatting
    print("\nMethod4: formatting")
    formatted_pdgmpd = ppiv2.map(lambda x: f"{x:<12}")
    # display apparently does not get imported
    print(formatted_pdgmpd)

    #Finally, for missing data replace 'nan'(<'NaN') by '___'
    formattedStr = str(formatted_pdgmpd)
    print(formattedStr)
    p3string = formattedStr.replace('nan', '___')
    print(p3string)

    ## Now insert sequentially and pivoted pdgm combo into display space
    lpdgm.insert('end',str('\nCOMBINE PARADIGMS: ' + pdgmsinfo[0]) + '\n')
    lpdgm.insert("end","\nSEQUENTIALLY COMBINE\n")
    lpdgm.insert('end',pdgmtab)
    lpdgm.insert("end",str("\n\nPIVOT: " + pivot + "\n"))
    #lpdgm.insert('end', formatted_pdgmpd)
    lpdgm.insert('end', p3string)
    #lpdgm.insert('end', pdgmpiv2)
    lpdgm.insert('end', '\n\n===============================\n\n')

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

'''
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
'''

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
root.title('Paradigm Display - ltsource')
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
pdbutton = ttk.Button(cframe, text="Display Paradigm", command=displayPdgm)
pdbutton.grid(column=0, row=25, sticky=W)


# Individual pdgm display space
plabel1 = ttk.Label(cframe, text="Paradigms:", font=f)
plabel1.grid(column=1, row=0, sticky=(N,E))
# pdgm content displayed here in text widget
lpdgm = Text(cframe, state='normal', width=80, height=25, wrap='none')
lpdgm.grid(column=2, row=0, rowspan=25, sticky=(N,S,E,W))

# Combined pdgm display
ttk.Label(cframe, text="Combine Paradigms:").grid(column=1, row=25, sticky=E)
ttk.Label(cframe, text="Format: p1,p2,[...];pivot1,pivot2[...]").grid(column=2, row=25,sticky=W)
pdgms = StringVar()
pdgms_entry = ttk.Entry(cframe, width=25, textvariable=pdgms)
pdgms_entry.grid(column=2, row=26, sticky=W)
ttk.Button(cframe, text="Combine Paradigms", command=pdgmCombine).grid(column=2,row=26, sticky=E)

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


