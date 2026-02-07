# Afro-Asiatic Morphology Archive

## AAMA Application Software

There are a number of Python and shell scripts in the webappy directory
for sorting and ordering json-file paradigms, or 
which are exploratory or tentative in nature. However the core
of the AAMA application is constituted by three categories of Python
and shell scripts which operate on the data in the `~/aama-data/data/`
language directories. 

1. Shell scripts to launch and update the datastores: `sh` and `rq` files.
2. Python scripts to maintain and prepare the data files: `pdgmDict- . . .` files.
3. Python scripts to display and manipulate paradigm data: `pdgmDisp . . .` files.

### 1. Shell scripts to launch and update the datastore.
(The shell scripts are all basically the work of Gregg Reynolds.)

    1.1 `fuseki.sh`: 
This is the script which launches the fuseki datastore. 
The Ruby function which actually launches and runs the datastore is located in the 
`FUSEKI_HOME` directory, and  uses as one of its arguments the 
`aamaconfig.ttl` configuration file, which should be inserted into the 
`{FUSEKI_HOME}/apache-jena-fuseki-N.N.N/` directory (e.g., currently on my machine,
`~/jena/apache-jena-fuseki-3.16.0/`). In addition to activating the 
datastore, this function opens a web page  on `localhost:3030` where 
the datastore can be inspected, and where SPARQL queries can be 
independently run against the datastore. For dcumentation and installation 
cf. [Apache Jena Fuseki](https://jena.apache.org/documentation/fuseki2/index.html)
and further here in [github.aama.io](https://aama.github.io./)

    1.2 `aama-datastore-update.sh ../aama-data/data/[LANG]`:
 This script needs to be run whenever new or revised data are added 
to a language's data file in one of the `~/aama-data/data/` language 
directories. The script calls `fudelete.sh` 
to delete the former language graph, `fuquery-gen.sh`
to run the queries `count-triples.rq` and `list-graphs.rq` before and after
deletion, `aama-ttl2fuseki.sh`  to load a new language graph into the
datastore, and `aama-cp2lngrepo.sh` to upload the new/transformed  data 
to the local and github repositories.


    1.3 `aama-cpwebappy2lngrepo.sh`: 
This script performs the same copy and upload functions for
the application shell and Python scripts. 

### 2. Python scripts to generate indices and transformations of the json
 data files. 

    2.1 `pdgmDict-pvlists.py [LANG]`: 
This script generates a file 
`pvlists/[LANG]-pdgm-values.txt` which contains a 'name' for
each paradigm, consisting of a comma-separated list of the values of
each of the morphological properties enumerated in the `common` section
of the term cluster - thus uniquely identifying each paradigm within
the language, and, with the addition of a language designation, within
the whole AAMA paradigm corpus. It also generates two `db` files, 
`pvlists/[LANG]-pdgmdb.db` and `pvlists[LANG]-labldb.db`, which link
each paradigm 'name' respectively with a full 'property:value' list 
and a paradigm 'label' more-or-less arbitrarily assigned to the paradigm 
when the json file was first created.

    2.2 'pdgmDict-schemata.py [LANG]`: 
This script generates a json 
property:value-list dictionary `pvlists/[LANG]-schemata.json` to be
substituted into the `[LANG]-pdgms.json` file every time a property
or value is added or changed in any way. It also generates a more
succinct version of the schemata dictionary, `pvlists/[LANG]-pdgm-PVN.txt`, 
which is used in the basic paradigm display, along with the current
value of the `pdgmPropOrder` variable from the `[LANG]-pdgms.json` file, 
and which determines the order of the properties whose values constitute
the paradigm 'name'.
        
    2.3 `pdgmDict-lexemes.py [LANG]`: 
The lexemes associated with paradigms in the `LANG-pdgms.json` (and 
corresponding `LANG-pdgms.ttl`) files are identified by a `lexemeID` which 
could in principle be any arbitrary alphanumeric symbol sequence, but which in 
practice and for memnonic convenience are lower-ascii approximations of the 
lexeme's lemma. This script, in conjunction with `pdgmDict-lexCheck.py` and 
`pdgmDict-lexRev.py`, generates a `lexemes` section consisting of   dummy 
lexeme  entries (e.g., `lemma = '[x]', gloss = '[y]'`) for every lexemeID. 
This 'lexemes' section must be subsequently filled out by hand (or in an ideal 
case be linked programmatically with a digital lexicon of the language in 
question).

    2.4 `pdgmDict-json2ttl.py [LANG]`: 
After all the foregoing file modifications, this script transforms, section
by section, the `[LANG]-pdgms.jspn` file into a '[LANG}-pdgms.ttl`, and 
includes some 'predicates' from the various RDF semantics applications.
(It is derived from an xsl file originally written by Gregg Reynolds.) 

    2.5 Assorted `pdgmDict-MANIPULATION.py` scripts:
There are in addition a number of scripts aimed at ordering, formatting, 
or extracting information from the 'LANG-pdgms.json' files:

    - pdgmDict-jreplace.py
    
    - pdgmDict-lablesort.py
    
    - pdgmDict-lfam.py
    
    - pdgmDict-lname2labb.py
    
    - pdgmDict-propsets-indiv.py
    
    - pdgmDict-propsets-merged.py
    
    - pdgmDict-reorderPdgmCols.py
    
    - pdgmDict-sourceBib.py
    
    - pdgmDict-template.py
    
(For their functions, see the introductory material of the individual 
script texts.)



### 3. Python scripts to display and manipulate paradigm data.

The three major data-display/manipulation (`pdgmDisp- . . .`) scripts are
descended from an earlier more integrated browser application, which
included both the display and formatting applications and was written
in Clojure. We expect the current version also to eviolve into such a more
integraed browser-oriented from. 

For the moment, this version uses for the graphic user interface widgets 
from the native Python tkinter adaption of the tk graphic interface. The
widgets (cframe, StringVar, Label, Listbox, Text, Button, and Entry, 
with asociated text, textvariable, and command) are placed on the
display  with respect to a column/row grid. After the graphic set-up
commands, the bulk of the script consists of the functions called
by the widget (princiipally `Button`) 'command' argument.


    3.1 `pdgmDisp-baseApp-PDGM.py`: 
    
The graphic setup is a two-colum
display with, in the left column, a language select-list, where a language
choice results in a middle box display of the property-value inventory
of the language's paradigm set, along with an indication of the order of
properties in the value-list names of the paradigm, followed by a
select-list of paradigm 'names'. A 'Display Paradigm' button at the
bottom of the column results in a sequentially numbered display in
the right text-box of the paradigm name, source, notes if present, 
and the paradigm itself. 

If one wishes to see a sequential or side-by-side disiplay of two 
(or more) paradigms, at the bottom of the right-hand side allows the 
entering of a comma-separated list of the sequence-numbers of two or more
 displayed paradigms, followed by a colon, followed by an indication
of the 'pivot' category to be compared.

For example if the third and fifth paradigm displayed were the Present
and Perfedt 'tam' value of the Afar Class1 Verb Affirmative  uduur, and 
one wanted a side-by-side display of these tam forms, one wou;d
enter *3,5:tam*  in the text box, push the 'Combine Paradigms' button,
and see (for the moment, first) a sequential display of the paradigms, and a
display 'pivoted' on the value for 'tam'.

    3.2 `pdgmDisp-baseApp-GPDGM.py`:
    
As its name suggests, this script offers a generalization of the notion 
"paradigm". In many grammatical traditions (cf. the familiar
 "APPENDIX: PARADIGMS" of the standard Indoeuropean and Afroasiatic grammars, 
but also, e.g. 2nd millennium B.C. Sumerian [OIP; Gragg]), this is a complete 
enumeration of the forms considered to model/exemplify a morphological system. 
This is realized as an exhaustive set of tabular presentations each giving, 
e.g.:

   1) for one possible combination out of all the relevant morphological 
catefories: `part-of-speech`, `tense`, `aspect`, 'mood', `case`, 'inflectional
 class`, etc. (= the `property: value' list given in the `common` portion of 
each `termcluster` in `LANG-pdgms.json' )
    
    2) the forms associated with the possible combinations of (e.g., for verbs)
 the `number`, `person`, `gender` properties ( = the 'terms' table [list of 
lists] of the lexemes characterized by the 'common' property set.

In 'pdgmDisp-baseApp-GPDGM.py` we have this same structure of a set of 'common'
 property-value pairs and a "table" of 'terms', except that the `commmon` and 
`terms` except that the set of property-values associated with each is 
completely at the discretion of the investigator. Obviously the regular 
paradigms of the 'LANG-pdgms.json' files are a special case of GPDGM displays, 
as are a very large number of `common`-`term` combinations which do not 
correspond to any possible or occurring form. But by exploring occurring 
combinations of interest, including ones which involve distinct languages, 
this dislay routine opens up the possibility of many potentially interesting 
and relevant form tables.
    
  
    3.3 `pdgmDisp-formsearch.py`: 
    
This script is for the comparison of
realizations of a given property/value combination in different
languages. Two or more languages can be selected from the upper-right
language-selection list. In an Entry box below a list of
desired property=value combinations can be entered. A `Find Form` button
will display a list of paradigms in the designated languages where
the property=value combination list occurs. One or more of these 
paradigms can be selected, and registered by the 'Choose Paradigm' button, 
and the 'Display Paradigm' button will display the chosen paradigms in 
the lower right-side text box. Finally the paradigms in question the
be combined as in the baseApp script.

For example one could want to see whether second-person, feminine, 
pronominal forms, singular or plural, are distinguished in Arabic and 
Coptic-Sahidic, and compare the way they are marked. One would choose 
Arabic and Coptic-Sahidic in the language select-list, enter
 `person=Person2,gender=Fem,pos=Pronoun,number=?number` in the 'Entry'
 box, push the 'Find Forms' button and see in the upper right select
box the relevant forms, and the label  of the paradigm in which each 
form occurs. One could then select any paradigms of interest and see
the full paradigm, sequentially numbered, in the lower right-hand text 
box. For moore precise comparison one could then go on to 'combine'
the paradigms as in the baseApp script.

    3.4 `pdgmDisp-pnames.py`:

This program simply enables the uiser to generate and display, presumably on 
an experimental basis, a "paradigm-name" list in a different order from that 
dictated by the `pdgmPropOrder` feature of the `LANG-pdgms.json` file.

    3.5 `pdgmDispQuery.py`: 
    
Each of the display scripts, 3.1, 3.2, and 3.3,
finds the data it displays by running a SPARQL query against the AAMA datastore.
These queries are formed from the display data request by one or more of the
 `query()` functions contained in this script and which have been imported
into the display script. The query itself, and its CSV output, are
for the moment printed to the terrminal (or eventually to a log file).


