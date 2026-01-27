'''
Basic framework for formsearch  using tkinter.
Comma-separted strings of property values in listbox are keys to full 
pdgm-defining prop:val strings (pvstrings/pdgm-dict-LANG.py). SPARQL query
 for pdgm  derived from that in pdgmDisp.query. Widgets and grid modeled 
on Mark Roseman, Modern Tkinter -- cf. esp. pp. 67-70.
NOTE: In this one-frame version of pdgmDispUI, paradigm and res
[=SPARQL query formed in pdgmDisp.query()] are inserted into the Tk text
 widgets lpdgm and lquery.

[e.g. "pos=Pronoun,person=Person2,gender=Fem,number=?number"]

[NOTE: 09/22/25 - Not sure what this script, dated 07/27/23, does - probably superceeded by subsequent sctipts.]
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
    #print('llist: ')
    #print(idxslist)
    lnameslist = []
    for i in idxslist:
        idx = int(i)
        lname = languagenames[idx]
        #lmsg1.set("Paradigms for %s" % lname)
        lnameslist.append(lname) 
    languages= (',').join(lnameslist)
    #print(languages)
    llmsg.set(languages)

def choosePdgms(*args):
    idxs = lforms.curselection()
    idxslist = list(idxs)
    #resultstr = lformslist.get()
    #resultlist = resultstr.split(',')
    #print('resultlist: ')
    #print(resultlist)
    #print('lformslist: ')
    #print(idxslist)
    pnameslist = []
    for i in idxslist:
        idx = int(i)
        #print(str('idx = ' + str(idx)))
        form = resultlist[idx]
        pname = form[-1].strip('()')
        #print(str('pname: ' + str(pname)))
        pnameslist.append(pname)
    pnames = (',').join(pnameslist)
    print(str('pnames: ' + pnames))
    #pdgms= (',').join(pnameslist)
    #print(str('pdgms: ' + pdgms))
    pdgmmsg.set(pnames)

def pvpairsSearch(*args):
    print('\n===============================\n===============================')
    lforms.insert('end', '\n===============================\n')
    # From lang select-list
    languages = llmsg.get()
    print("languages for formsquery:")
    print(languages)
    # From prop=Val entry form
    qstring = pvpairs.get()
    qstring2 = qstring.rstrip('\n')
    print("qstring for formsquery:")
    print(qstring2)
    #resultlist = []
    resultstr = ""
    # Make SPARQL query
    res = formsquery(languages,qstring2)
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
                    #NB: If I tray any other symbols but '()' to
                    #    set pdgmLabel graphically apart, program
                    #    inserts a '{}' around the pdgmLabel
                    selval = str('(' + result[sel]["value"] + ')')
                    #selval.strip('{}')
                    #selval = str('[' + selval1 + ']')
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
    #print("pdgmids:")
    #print(pdgmids)
    plabellist = pdgmids.split(',')
    ##print('\nFor each of the  paradigms:')
    for i in plabellist:
        #Presumption is  that first item in each plabel is '[labbrev]
        # Have to get lname from labbrev

        #print(i)
        pname = (i).split('-')
        labbrev = pname[0]
        lang = labb2lname[labbrev]
        #print(str('lang = ' + lang))
        pdgmlist = []
        pdgmstr = ""
        sfile = str('pvlists/' + lang + '-labldb')
        #print(str('sfile: ' + sfile))
        # get pvalue from pkey in (unshelved) pdgmdb
        labldb = shelve.open(sfile) # open it
        pvalue = labldb[i] # get the full prop-val string
        labldb.close()  # close it right away
        #print("pvalue:")
        #print(pvalue)
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
        #print(str('valstring: ' + valstring))
        # pdgmDisp.query makes SPARQL query out of full prop-val
        # pdgm specification in pval
        res = query(pvlist,valstring,lang)
        # print("\nThe SPARQL query from the prop-val list:\n")
        # print(res)
        #print('\n')
        # pause = input("Press <return> to continue:")
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

        # Update pcount and pdgmsDisp
        # Assign sequence number to paradigm
        pnum = int(pcount.get()) + 1
        # print(pnum)
        pcount.set(pnum)
        L = lang.capitalize()
        # [OLD] Make pdgm label:
        # plabel = str("\nParadigm for " + i + ":\n" + pvalue + "\n")
        plabel = str(pcount.get() + ":" + L + "," + pvalue + "\n")
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
        #for h in header:
           # select2.append(h.upper())

        # Make pdgm table:
        pdgmtab = tabulate(pdgmlist, headers = select2)
        print("Table:")
        print(plabel)
        print(pdgmtab)
        # Write the pdgm(s) to the pdgms text widget
        lpdgm.insert('end', plabel)
        lpdgm.insert('end', pdgmtab)
        lpdgm.insert('end', "\n")
        lpdgm.insert('end', "\n")

# function for pdgm-combine button
def pdgmCombine(*args):
    print('===============================\n')
    lpdgm.insert('end', '\n\n===============================')

    # Make a dictionary out of pdgmsDisp
    disppdgms = pdgmsDisp.get()
    #print("disppdgms:")
    #print(str(disppdgms))
    disppdgms2 = disppdgms.rstrip('\n')
    #print('Paradigms displayed so far:')
    #print(str(disppdgms))
    #print(disppdgms2)
    disppdgmslist = disppdgms2.split('\n')
    dictpdgms = {}
    for dp in disppdgmslist:
        #print("dp:")
        #print(dp)
        sdp = dp.split(',')
        #print("sdp:")
        #print(sdp)
        pid = sdp[0].split(':')
        #print(sdp)
        #print("pnum:")
        #print(pid[0])
        #print(sdp[0])
        #print(sdp[1:])
        dictpdgms[pid[0]] = sdp[1:]

    # See which pdgms you want and what is the pivot
    pdgmsget = pdgms.get()
    #print("pdgmsget:")
    #print(pdgmsget)
    pdgmsinfo = pdgmsget.split(':')
    #print(str('Pdgm Combine Info: ' + pdgmsget))
    #print(str('\nParadigms to combine: ' + pdgmsinfo[0]))
    #print(pdgmsinfo[1])
    pivot = pdgmsinfo[1]
    print(str('Pivot(s) for combined pdgms: ' + pivot))
    #lpdgm.insert('end',(str('PIVOT(S): ' + pivot + '\n')))

    # Get list of pdgmsdisp to combine
    pdgmnums = pdgmsinfo[0].split(',')
    pdgmlist = []
    pdgmstr = ""
    for i in pdgmnums:
        # Get its full specification
        pnamelist = dictpdgms[i]
        #print("pname: ")
        #print(pnamelist)


        # Get rid oF 'num:LN,'
        # Rest = pvlist
        # pnamelist = pname.split(',')
        lname = pnamelist[0]
        lang = lname.removeprefix('language:')
        pvlist = pnamelist
        #print(str("property-value list formed from pdgm " + i + ":"))
        #print(pvlist)
        #Assuming for nnow number,person,gender values only!
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
    #print("\npdgmlist:")
    #print(str(pdgmlist))
    # kludge to get desired category (number & gender) order in pivot table
    #pdgmstr2 = pdgmstr.replace("Singular", " Singular")
    #pdgmstr2 = pdgmstr2.replace("Masc", " Masc")
    pdgmtab = tabulate(pdgmlist, headers=select)
    #print(str("\nselect string: " + header3))
    #print('\n')

    print("\nThe csv ('comma-separated-value') output of the SPARQL query:")
    print(str((',').join(select) + '\n' + pdgmstr + '\n'))
    print("\nFormatted version of the csv list:")
    print(pdgmtab)
    pdgmstr2 = str(header3 + '\n' + pdgmstr)
    # Make sure that vallist and pivlist do not overlap
    #print(str("vallist1: " + str(vallist)))
    #print(str("pivlist1: " + str(pivlist)))
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
    #print(formattedStr)
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


#languagenames = ('beja-hud', 'afar', 'oromo', 'somali-standard')

labb2lname = {'bhu': 'beja-hud', 'afr': 'afar', 'orm': 'oromo', 'som': 'somali', 'alb': 'alaaba', 'alg': 'alagwa', 'aob': 'akkadian-ob', 'aar': 'aari', 'arb': 'arabic', 'abr': 'arbore', 'awn': 'awngi', 'bay': 'bayso', 'bal': 'beja-alm', 'bre': 'beja-rei', 'bro': 'beja-rop', 'bva': 'beja-van', 'bwe': 'beja-wed', 'bgh': 'berber-ghadames', 'bil': 'bilin', 'boj': 'boni-jara', 'bob': 'boni-kijee-bala', 'bok': 'boni-kilii', 'brs': 'burji-sas', 'brw': 'burji-wed', 'brn': 'burunge', 'csa': 'coptic-sahidic', 'dah': 'dahalo', 'das': 'dasenech', 'dha': 'dhaasanac', 'diz': 'dizi', 'egm': 'egyptian-middle', 'elm': 'elmolo', 'gaw': 'gawwada', 'ged': 'gedeo', 'gez': 'geez', 'had': 'hadiyya', 'hau': 'hausa', 'hdi': 'hdi', 'heb': 'hebrew', 'irq': 'iraqw', 'kam': 'kambaata', 'kem': 'kemant', 'khm': 'khamtanga', 'kor': 'koorete', 'mal': 'maale', 'mub': 'mubi', 'ren': 'rendille', 'sah': 'saho', 'shn': 'shinassha', 'sid': 'sidaama', 'syr': 'syriac', 'tsm': 'tsamakko', 'wol': 'wolaytta', 'yak': 'yaaku', 'yem': 'yemsa'}

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
root.title('Form Search4')
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

# pdgmsDisp is a running list of displayed pdgms
# every pdgm displayed in a session is kept here with a
# sequence ID no and its name so that its CSV can be regenerated
# from its sequence umber in the 'Combine Paradigms' box
pdgmsDisp = StringVar() # added to for each displayed pdgm
pdgmDispDict = {}


# Create  widgets

llablgen = ttk.Label(cframe, text="Choose Languages:")
llablgen.grid(column=0, row=0, padx=10, pady=5)
lbox = Listbox(cframe, listvariable=lnames, selectmode='multiple', width=100, height=15)
lbox.grid(column=0, row=1, rowspan=15, sticky=(N,S,E,W), pady=5, padx=5)

#lcbutton = ttk.Button(cframe, text='Clear Languages', command=clearLangs, default='active')
#lcbutton.grid(column=0, row=22, sticky=W)
#pdbutton.grid(column=0, row=25, sticky=E)

ttk.Label(cframe, text="Enter List of prop=Value/prop=?value Queries").grid(column=0, row=18, sticky=W)
#ttk.Label(cframe, text="Enter List of prop=Value/prop=?value Queries").grid(column=0, row=18, sticky=W)
pvpairs = StringVar()
pvpairs_entry = ttk.Entry(cframe, width=35, textvariable=pvpairs)
pvpairs_entry.grid(column=0, row=19, sticky=W)
ttk.Button(cframe, text="Find Forms", command=pvpairsSearch).grid(column=0,row=20, sticky=W)
pcbutton = ttk.Button(cframe, text='Choose Paradigm', command=choosePdgms, default='active')
pcbutton.grid(column=0, row=21, sticky=W)
pdbutton = ttk.Button(cframe, text="Display Paradigms", command=displayPdgms)
pdbutton.grid(column=0, row=21, sticky=E)

# Combined pdgm display
ttk.Label(cframe, text="Combine Paradigms [for now npg values only!]:").grid(column=0, row=22, sticky=W)
ttk.Label(cframe, text="Format: p1,p2,[...];pivot1,pivot2[...]").grid(column=0, row=23,sticky=W)
#ttk.Label(cframe, text="Format: p1,p2,[...];pivot1,pivot2[...]").grid(column=2, row=24,sticky=W)
pdgms = StringVar()
pdgms_entry = ttk.Entry(cframe, width=25, textvariable=pdgms)
pdgms_entry.grid(column=0, row=24, sticky=W)
ttk.Button(cframe, text="Combine Paradigms", command=pdgmCombine).grid(column=0,row=25, sticky=W)



#ttk.Label(cframe, text="Format: 'person=Person2,gender=Fem,pos=?pos,number=?number'").grid(column=0, row=25, sticky=W)

llabel1 = ttk.Label(cframe, text="Languages:", font=f)
llabel1.grid(column=1, row=0, sticky=(N,E))
llabel2 = ttk.Label(cframe, textvariable=llmsg, anchor=W)
llabel2.grid(column=2, row=0,  sticky=W)
# pdgm content displayed here in Listbox  widget
lforms = Listbox(cframe, listvariable=lformslist, selectmode='multiple', width=70, height=100)
lforms.grid(column=2, row=2, rowspan=15, sticky=(W, E))
pdgmslb1 = ttk.Label(cframe, text="Paradigms:", font=f)
pdgmslb1.grid(column=1, row=18, sticky=(N,E))
pdgmslb2 = ttk.Label(cframe, textvariable=pdgmmsg, anchor=W)
pdgmslb2.grid(column=2, row=18, sticky=W)
# query content displayed here in text widget
lpdgm = Text(cframe, state='normal', width=70, height=20, wrap='none')
lpdgm.grid(column=2, row=19, rowspan=10, sticky=(W, E))
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


'''
person=Person2,gender=Fem,pos=?pos,number=?number
person=Person2,gender=Fem,pos=Pronoun,number=?number
person=Person2,tam=Imperfect,polarity=Affirmative,conjClass=Class1
'''
