'''
This veersion of formsearch is intended to use tree-view for 
language list. [01/27/23]

Basic framework for formsearch  using tkinter.
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
import shelve
from pdgmDispQuery import query, formsquery    #import for pdgm-display query code
#import json
#import pprint
# import re


f = ('times',16) #'the pleasing font'; used in llabel1, pdglabl

 
# Called when the selection in the lbox1 changes; figure out
# which language is currently selected, and then lookup its lcode,
# and from that, its lfile.  As well, clear the selected pdgmmessage, 
# so it doesn't stick around after we start doing
# other things.
def showLangs(*args):
    idxs = lbox.curselection()
    idxslist = list(idxs)
    print('llist: ')
    print(idxslist)
    lnameslist = []
    for i in idxslist:
        idx = int(i)
        lname = languagenames[idx]
        #lmsg1.set("Paradigms for %s" % lname)
        lnameslist.append(lname) 
    languages= (',').join(lnameslist)
    print(languages)
    llmsg.set(languages)

def choosePdgms(*args):
    idxs = lforms.curselection()
    idxslist = list(idxs)
    print('resultlist: ')
    print(resultlist)
    print('lformslist: ')
    print(idxslist)
    pnameslist = []
    for i in idxslist:
        idx = int(i)
        print(str('idx = ' + str(idx)))
        form = resultlist[idx]
        pname = form[-1].strip('()')
        print(str('pname: ' + str(pname)))
        pnameslist.append(pname)
    pnames = (',').join(pnameslist)
    print(pnames)
    #pdgms= (',').join(pnameslist)
    #print(str('pdgms: ' + pdgms))
    pdgmmsg.set(pnames)

def pvpairsSearch(*args):
    print('===============================\n')
    lforms.insert('end', '\n===============================\n')
    languages = llmsg.get()
    qstring = pvpairs.get()
    #resultlist = []
    resultstr = ""
    # Make SPARQL query
    res = formsquery(languages,qstring)
    print(str("QUERY: \n" + res))
    # Submit it to paradigm datasrore
    sparql = SPARQLWrapper("http://localhost:3030/aama/query")
    sparql.setQuery(res)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    results2 = sparql.query()
    #print("results")
    #print(results)
    #print('results2')
    #print(results2)
    title = str('FORM SEARCH: ' + qstring)
    resultlist.append(title)
    select = results["head"]["vars"]
    # print()
    header =  (" ").join(select)
    resultlist.append(header)
    uline = '-' * len(header)
    header3 =  (",").join(select)
    resultlist.append(uline)
    for result in results["results"]["bindings"]:
        # print(result)
        resultrow = []
        for sel in select:
            #print(str('sel: ' + sel))
            if sel in result:
                #if result[sel]:
                if sel == 'pdgmLabel':
                    selval = str('(' + result[sel]["value"] + ')')
                else:
                    selval = result[sel]["value"]
            else:
                selval = "--"
            resultrow.append(selval)
            #print('resultrow: ')
            #print(resultrow)
            resultrowstr = (",").join(resultrow)
        resultstr = str(resultstr + resultrowstr + "\n")
        resultlist.append(resultrow)
    #print(header3)
    #print(select)
    # kludge to get desired category order in pivot table
    #pdgmstr2 = pdgmstr.replace("Singular", " Singular")
    #pdgmstr2 = pdgmstr2.replace("Masc", " Masc")
    #print(select)
    #formslist = []
    lformslist.set(resultlist)
    #print('result list: ')
    #print(resultlist)
    lforms.insert('end', '\n\n===============================\n\n')

def displayPdgms(*args):
    pdgmids = pdgmmsg.get()
    plabellist = pdgmids.split(',')
    print('\nFor each paradigm:')
    for i in plabellist:
        #Presumption is  that first item in each plabel is '[LANG]:'
        print(i)
        pname = (i).split('_')
        lang = pname[0]
        print(str('lang = ' + lang))
        pdgmlist = []
        pdgmstr = ""
        sfile = str('pvlists/' + lang + 'labldb')
        # get pvalue from pkey in (unshelved) pdgmdb
        labldb = shelve.open(sfile) # open it
        pvalue = labldb[i] # get the full prop-val string
        labldb.close()  # close it right away
        if "%" in pvalue:
            propsel = pvalue.split("%")
            pvalue = propsel[0]
            valstring = propsel[1]
            valstring = valstring.replace("%","")
        else:
            valstring = "number,person,gender,token"
        vallist = valstring.split(',') # = pandas row
        vallist.remove('token')        # = pandas value
        # The following 6 lines are in order to get 'lang'
        # There has to be a more direct way!
        pvlist = pvalue.split(',')
        pvdict = {}
        for pv in pvlist:
            pt = pv.split(':')
            pvdict[pt[0]] = pt[1]
        lang = pvdict['language']    
        #print(str('valstring: ' + valstring))
        # pdgmDisp.query makes SPARQL query out of full prop-val
        # pdgm specification in pval
        res = query(pvalue,valstring,lang)
        # print("\nThe SPARQL query from the prop-val list:\n")
        # print(res)
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
        select2 = []
        for s in select:
            select2.append(s.upper())
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
        # Make pdgm label:
        plabel = str("\nParadigm for " + i + ":\n" + pvalue + "\n")
        # Make pdgm table:
        pdgmtab = tabulate(pdgmlist, headers = select2)
        print("Table:")
        print(plabel)
        print(pdgmtab)
        # Write the pdgm(s) to the pdgms text widget
        pdgms.insert('end', plabel)
        pdgms.insert('end', pdgmtab)
        pdgms.insert('end', "\n")
        pdgms.insert('end', "\n")



#languagenames = ('beja-hud', 'afar', 'oromo', 'somali-standard')

languagenames = ['afar', 'alaaba', 'alagwa', 'akkadian-ob', 'arabic', 'arbore', 'awngi', 'bayso', 'beja-alm', 'beja-hud', 'beja-rei', 'beja-rop', 'beja-van', 'beja-wed', 'berber-ghadames', 'bilin', 'boni-jara', 'boni-kijee-bala', 'boni-kilii', 'burji', 'burunge', 'coptic-sahidic', 'dahalo', 'dhaasanac', 'dizi', 'egyptian-middle', 'elmolo', 'gawwada', 'gedeo', 'geez', 'hadiyya', 'hausa', 'hdi', 'hebrew', 'iraqw', 'kambaata', 'kemant', 'khamtanga', 'koorete', 'maale', 'mubi', 'oromo', 'rendille', 'saho', 'shinassha', 'sidaama', 'somali', 'syriac', 'tsamakko', 'wolaytta', 'yaaku', 'yemsa']

formslist = []
resultlist = []
#pcount = "1"
#print(str("pcount1 = " + pcount))

# Root and Frame
# NOTE ON WINDOW HEIGHT/WIDTH;
# Present root.geometry seems to be optimal, as far as it goes. 
# Can increase pbox and decrease lquery (and vice-versa).
# Would addition of scrollbar to lquery or lpdgm give more optioms?
root = Tk()
root.geometry('1200x1200')
root.title('Form Search New')
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

# State variables
lnames = StringVar(value=languagenames) # lbox1
lformslist = StringVar(value=formslist)
pvar = StringVar()
pmsg = StringVar()
#lmsg1 = StringVar()
llmsg = StringVar()
pdgmmsg = StringVar()
pcount = StringVar()
pdisp = StringVar()
qdisp = StringVar()

# Create  widgets

llablgen = ttk.Label(cframe, text="Choose Languages:")
llablgen.grid(column=0, row=0, padx=10, pady=5)
lbox = Listbox(cframe, listvariable=lnames, selectmode='multiple', width=100, height=15)
lbox.grid(column=0, row=1, rowspan=20, sticky=(N,S,E,W), pady=5, padx=5)

#lcbutton = ttk.Button(cframe, text='Clear Languages', command=clearLangs, default='active')
#lcbutton.grid(column=0, row=22, sticky=W)
#pdbutton.grid(column=0, row=25, sticky=E)

ttk.Label(cframe, text="Choose Property/Value Queries").grid(column=0, row=22, sticky=W)
pvpairs = StringVar()
pvpairs_entry = ttk.Entry(cframe, width=35, textvariable=pvpairs)
pvpairs_entry.grid(column=0, row=23, sticky=W)
ttk.Button(cframe, text="Find Forms", command=pvpairsSearch).grid(column=0,row=24, sticky=W)
pcbutton = ttk.Button(cframe, text='Choose Paradigm', command=choosePdgms, default='active')
pcbutton.grid(column=0, row=25, sticky=W)
pdbutton = ttk.Button(cframe, text="Display Paradigms", command=displayPdgms)
pdbutton.grid(column=0, row=25, sticky=E)

#ttk.Label(cframe, text="Format: 'person=Person2,gender=Fem,pos=?pos,number=?number'").grid(column=0, row=25, sticky=W)

llabel1 = ttk.Label(cframe, text="Languages:", font=f)
llabel1.grid(column=1, row=0, sticky=(N,E))
llabel2 = ttk.Label(cframe, textvariable=llmsg, anchor=W)
llabel2.grid(column=2, row=0,  sticky=W)
# pdgm content displayed here in Listbox  widget
lforms = Listbox(cframe, listvariable=lformslist, selectmode='multiple', width=80, height=100)
lforms.grid(column=2, row=2, rowspan=20, sticky=(W, E))
pdgmslb1 = ttk.Label(cframe, text="Paradigms:", font=f)
pdgmslb1.grid(column=1, row=22, sticky=(N,E))
pdgmslb2 = ttk.Label(cframe, textvariable=pdgmmsg, anchor=W)
pdgmslb2.grid(column=2, row=22, sticky=W)
# query content displayed here in text widget
pdgms = Text(cframe, state='normal', width=80, height=15, wrap='none')
pdgms.grid(column=2, row=23, rowspan=3, sticky=(W, E))
#pdbutton = ttk.Button(cframe, text="Display Paradigm", command=guipdgm)



for child in  cframe.winfo_children(): child.grid_configure(padx=5, pady=5)

# Set event bindings for when the selection in lbox1 changes,
# when the user double clicks the list, and when they hit the Return key
lbox.bind('<<ListboxSelect>>', showLangs)
lbox.bind('<Double-1>', showLangs)
root.bind('<Return>', showLangs)
#lforms.bind('<<ListboxSelect>>', showForms)
#lforms.bind('<Double-1>', showForms)
#root.bind('<Return>', showForms)


# Colorize alternating lines of the lbox1
for i in range(0,len(languagenames),2):
    lbox.itemconfigure(i, background='#f0f0ff')

# Set the starting state of the interface
#  including clearing the messages.
#  Select the first language in the list; because the 
# <<ListboxSelect> event is only
# fired when user makes a change, we explicitly call showLfile.
#pmsg.set('')
llmsg.set('')
pcount.set('0')
pdisp.set('paradigm ....')
#qdisp.set('query    ....')
lbox.selection_set(0)
showLangs()


root.mainloop()


