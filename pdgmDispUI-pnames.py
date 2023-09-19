'''
Program to generate pdgm names given input propsequence list.
Should should generate list(s) of pdgmDisp-newlists and display
in frame to right.

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
import json
from tabulate import tabulate
import pandas as pd
from pandas import Series, DataFrame
from io import StringIO
import shelve
from pdgmDispQuery import query, formsquery    #import for pdgm-display query code
# import re


f = ('times',16) #'the pleasing font'; used in llabel1, pdglabl

 
# Called when the selection in the lbox1 changes; figure out
# which language is currently selected, and then lookup its lcode,
# and from that, its lfile.  As well, clear the selected pdgmmessage, 
# so it doesn't stick around after we start doing
# other things.
def showLang(*args):
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
        #lfilename = str("pvlists/pdgm-values-" + lname + ".txt")
        mfilename = str("pvlists/" + lname + "-pdgm-PVN.txt")
        #lfile = open(lfilename, "r")
        #pdvals = lfile.read()
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
        #pvar.set(pdvals)
        mvar.set(mvals)
        #minfo.insert('end',mvals)
        #pmsg.set('')

def ppvarsearch(*args):
    language = lmsg.get()
    tcpropstr = proporder.get()
    tcprops = tcpropstr.split(',')
    print(str('LANG: ' + language))
    print('Prop Order: ')
    print(tcprops)
    lfile = str('../aama-data/data/' + language + '/' + language + '-pdgms.json')
    jdata = json.load(open(lfile))
    pvallist = []
    # get the number of pdgms in the file
    tccount = len(jdata['termclusters'])
    #tccount = 1
    print(str('tccount:' + str(tccount)))
    for i in range(tccount):
        # read-in 'common' section
        tccommon = jdata['termclusters'][i]['common']
        tpltcc = list(tccommon.items())
        print(str('tpltcc: ' + str(tpltcc)))
        pdgmvals = []
        for prop in tcprops:
            #print(prop)
            for tup in tpltcc:
                #print(str('tup[0]: ' + str(tup[0])))
                #print(str('tup[1]: ' + str(tup[1])))
                if tup[0] == prop:
                    pdgmvals.append(str(tup[1]))
                   
        #print(str('pdgmvals= ' + str(pdgmvals)))
        # read sel from row-0 of 'terms'
        sel =  jdata['termclusters'][i]['terms'][0]
        selprops = ''
        # if not default (num,pers,gen,token), add to pval list
        # selprops used only if want non-default sel in pdgm list
        selprops2 = str("%" + ",".join(sel) + "%")
        # Test whether sel is a subset of the default png pdgm selset
        pngselset = {'number', 'person', 'gender', 'token', 'token-note'}
        selset = set(sel)
        # If the props of sel not all contained in pngselset
        if not selset <= pngselset:
            selprops = str("%" + ",".join(sel) + "%")
        pvalstring = str(','.join(pdgmvals) + selprops)
        pvallist.append(pvalstring)
    # write files with sorted pvals
    pvalsort = sorted(pvallist)
    #pvalsort.insert(0,str(','.join(tcprops)))
    pvals = '\n'.join(pvalsort)
    print(str('\npvals: \n\n' + str(pvals)))
    pnameslist.set(pvals)
    pnames.insert('end', language)
    pnames.insert('end', "\n")
    pnames.insert('end', tcpropstr)
    pnames.insert('end', "\n")
    pnames.insert('end', pvals)
    pnames.insert('end', "\n\n")



#languagenames = ('beja-hud', 'afar', 'oromo', 'somali-standard')

languagenames = ['afar', 'alaaba', 'alagwa', 'akkadian-ob', 'arabic', 'arbore', 'awngi', 'bayso', 'beja-alm', 'beja-hud', 'beja-rei', 'beja-rop', 'beja-van', 'beja-wed', 'berber-ghadames', 'bilin', 'boni-jara', 'boni-kijee-bala', 'boni-kilii', 'burji', 'burunge', 'coptic-sahidic', 'dahalo', 'dasenech', 'dhaasanac', 'dizi', 'egyptian-middle', 'elmolo', 'gawwada', 'gedeo', 'geez', 'hadiyya', 'hausa', 'hdi', 'hebrew', 'iraqw', 'kambaata', 'kemant', 'khamtanga', 'koorete', 'maale', 'mubi', 'oromo', 'rendille', 'saho', 'shinassha', 'sidaama', 'somali', 'syriac', 'tsamakko', 'wolaytta', 'yaaku', 'yemsa']

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
root.title('Generate Pradigm Value-Name lists')
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
lformslist = StringVar(value=formslist)
pvar = StringVar()
pmsg = StringVar()
#lmsg1 = StringVar()
lmsg = StringVar()
pdgmmsg = StringVar()
pcount = StringVar()
#pdisp = StringVar()
qdisp = StringVar()

# Create  widgets

llablgen = ttk.Label(cframe, text="Choose Language:")
llablgen.grid(column=0, row=0, padx=10, pady=5)
lnames = StringVar(value=languagenames) # lbox1
lbox = Listbox(cframe, listvariable=lnames, selectmode='browse', width=50, height=5)
lbox.grid(column=0, row=1, rowspan=3, sticky=(N,S,E,W), pady=5, padx=5)

#lcbutton = ttk.Button(cframe, text='Clear Languages', command=clearLangs, default='active')
#lcbutton.grid(column=0, row=22, sticky=W)
#pdbutton.grid(column=0, row=25, sticky=E)

# language morphological prop-val dispay
mmsg = StringVar() # "L prop-val schema"
mlabl = ttk.Label(cframe, textvariable=mmsg, anchor=W)
mlabl.grid(column=0, row=4, sticky=(W,E))

# morophological info
mvar = StringVar() # Content of PVN file
mbox = Listbox(cframe, listvariable=mvar, selectmode='browse', width=80, height=3)
mbox.grid(column=0, row=5, rowspan=3, sticky=(N,S,E,W), pady=5, padx=5)

ttk.Label(cframe, text="Enter Comma-separated list of Properties").grid(column=0, row=22, sticky=W)
proporder = StringVar()
porder_entry = ttk.Entry(cframe, width=35, textvariable=proporder)
porder_entry.grid(column=0, row=23, sticky=W)
ttk.Button(cframe, text="Generate Pname List", command=ppvarsearch).grid(column=0, row=24, sticky=W)

#ttk.Label(cframe, text="Format: 'person=Person2,gender=Fem,pos=?pos,number=?number'").grid(column=0, row=25, sticky=W)

pnamelabel1 = ttk.Label(cframe, text="Property Order:", font=f)
pnamelabel1.grid(column=1, row=0, sticky=(N,E))
pnamelabel = proporder.get()
pnamelabel2 = ttk.Label(cframe, text=pnamelabel, font=f)
pnamelabel2.grid(column=2, row=0, sticky=(N,E))
# pdgm content displayed here in text  widget
pnameslist = StringVar()
pnames = Text(cframe, state='normal', width=80, height=100, wrap='none')
pnames.grid(column=2, row=1, rowspan=30, sticky=(W, E))
# If eventually have pdgm display
#pdgmslb1 = ttk.Label(cframe, text="Paradigms:", font=f)
#pdgmslb1.grid(column=1, row=22, sticky=(N,E))
# query content displayed here in text widget
#pdgms = Text(cframe, state='normal', width=80, height=15, wrap='none')
#pdgms.grid(column=2, row=22, rowspan=3, sticky=(W, E))
#pdbutton = ttk.Button(cframe, text="Display Paradigm", command=guipdgm)

for child in  cframe.winfo_children(): child.grid_configure(padx=5, pady=5)

# Set event bindings for when the selection in lbox1 changes,
# when the user double clicks the list, and when they hit the Return key
lbox.bind('<<ListboxSelect>>', showLang)
lbox.bind('<Double-1>', showLang)
root.bind('<Return>', showLang)
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
lmsg.set('')
pcount.set('0')
#pdisp.set('paradigm ....')
#qdisp.set('query    ....')
lbox.selection_set(0)
showLang()


root.mainloop()


