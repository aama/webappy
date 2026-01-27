#!/usr/local/bin/python3
'''
query() assembles sparql pdgmquery from pvstring. In order:
Prefixes, Select statement, Prop-val triples, Selection triples,
Order-by 
sourcequery() retrieves single-value targets, for the moment,
source/reemark section(s). Later, lexeme lemma/gloss. (May
eventually be combined with query?)
formsquery() retrieves all forms meeting certain feature specifications.
'''
def query(pvlist,valstring,lang):
    print("\nFrom 'pdgmDispQuery.py': \n====================")
    print(str("pvlist: " + str(pvlist)))
    print(str("valstring: " + valstring))

    #Prefixes
    lpref = lname2labb[lang]
    lprefix = str("PREFIX " + lpref + ": <http://id.oi.uchicago.edu/aama/2013/" + lang + "/>")
    prefixes = str(prefixbase + lprefix + "\n")
    
    # NOTE:
    # This version allows the selection of a subset of a property's
    # values, used in baseapp4 to display, given a set of prop and vals 
    # (say: 'V 3mSg Aff') the forms of this set for a selection of
    # the values of one or more other properties (say: the 'tam' values
    # for a subset of values, e.g. only the 'Prefix' and 'Suffix' 
    # values of the large 'conjClass' property in Afar.
    # Format in valstring: 'conjClass:Prefix+Suffix'.
    # This allows a displayable Pandas pivot table, which would 
    # otherwise exceed the tkinter display capacity if all the values
    # of 'conjClass' were chosen.

    VALUES = ""
    valuelist = []
    vallist = valstring.split(",")
    for val in vallist:
        if ":" in val:
            # NB There should be a ':' in vallist ONLY if
            # among the possible values of a prop only a
            # subselection is wanted: 'prop:val1+val2+val3'
            # means "for 'prop' take only the values 'val1,val2,val3'"
            valueslist = val.split(":")
            valuelist.append(valueslist[0])
            values = valueslist[1].split("+")
            VALS = str("VALUES ?" + valueslist[0] + " {")
            for vals in values:
                VALS = str('  ' + VALS + '"' + vals + '" ' )
            VALS = str(VALS + "}\n")
            VALUES = str(VALUES + VALS)
        else:
            valuelist.append(val)
    valstring = ','.join(valuelist) 

    print(str("valuelist: " + str(valuelist)))
    print(str("valstring: " + valstring))
    print(str("VALUES: " + VALUES))

    #HERE!

    selection = str("?" + valstring.replace(","," ?"))
    selection = selection.replace("-", "")
    select = str("SELECT DISTINCT " + selection + "\nWHERE\n{")
    Lang = lang.capitalize()
    
    # Triples
    triples = ''
    # 1. prop-val triples

    #print(str("pvlist= " + str(pvlist)))
    print("Paradigm Common Property-Value Pairs:")
    for pv in pvlist:
        print("pv= " + str(pv))
        propval = pv.split(":")
        if propval[0] == "lexeme":
            triple = str("    ?s aamas:lexeme / rdfs:label \'" + propval[1] + "\'.\n")
        elif propval[0][0:5] == "token":
            triple = str("    ?s " + lpref + ":" + propval[0] + " \'" + propval[1] +  "\'.\n")
        elif propval[0] == "language":
            triple = str("    ?s aamas:lang aama:" + Lang + " .\n")
        else:
            triple = str("    ?s " + lpref + ":" + propval[0] + " " + lpref + ":" + propval[1] + " .\n")
        triples = triples + triple

    # 2. selection triples
    # sels = valstring.split(",")
    for sel in valuelist:
        sel2 = sel.replace("-", "")

        # In the following apparently trying to introduce structure
        # into tokenNote by introducing something termed 'token-note;
        # Dosen't seem to work -- but would come back to this.
        # Want to insist on "token" but let "token-note" be optional
        #if sel[0:5] == "token":
        #    if sel[5::] == '-note':
        #        triple = str("    OPTIONAL { ?s " + lpref + ":token-note  ?" + sel2 + " }\n")
        #    else:

        if sel == "token":
            triple = str("    ?s " + lpref + ":token  ?" + sel2 + " .\n")
        elif sel[0:9] == "token-note":
            triple = str("    ?s " + lpref + ":" + sel + " ?token-note .\n")
        elif sel == "lexeme":
            triple = str("    ?s aamas:lexeme / rdfs:label ?" + sel2 + " .\n")

        elif sel == "gloss":
            triple = str("    ?s aamas:lexeme / aamas:gloss ?" + sel2 + " .\n")

        elif sel  == "language":
            triple = str("    ?s aamas:lang / rdfs:label ?" + sel2 + " .\n")
       # See if we can simply do without "OPTIOAAL". Not sure why I put
       # it in in the first place. In any case creates difficulties when 
       # single searched item gets marked as OPTIONAL as in, e.g.
       # Afar: Verb,Prefix,uduur%nonFiniteForm,token%   [08/02/25]
       # else:
       #     triple = str("    OPTIONAL { ?s " + lpref + ":" + sel + " / rdfs:label ?" + sel2 + " }\n")
        else:
            triple = str("    ?s " + lpref + ":" + sel + " / rdfs:label ?" + sel2 + " . \n")
        triples = triples + triple
    triples = str(triples + VALUES + "}\n")
    #order statement
    selection = selection.replace("?number", "DESC(?number)")
    selection = selection.replace("?gender ", "DESC(?gender)")
    order = str("ORDER BY " + selection)

    query = str(prefixes + select + triples + order +  "\n")
    print(str("query:\n" + query))
    print("=======================")
    return query

def sourcequery(pvlist,svalstring,lang):
    print("\nFrom 'pdgmDispQuery.py': \n====================")
    #print("\nsourcequery function output: \n====================")
    #print(str("pvalue: " + pvalue))
    print(str("svalstring: " + svalstring))
    lpref = lname2labb[lang]
    #print(str("lang, lpref: " + lang + ", " + lpref))
    lprefix = str("PREFIX " + lpref + ": <http://id.oi.uchicago.edu/aama/2013/" + lang + "/>")
    prefixes = str(prefixbase + lprefix + "\n")
    # Selection
    selection = str("?" + svalstring.replace(","," ?"))
    selection = selection.replace("-", "_")
    select = str("SELECT DISTINCT " + selection + "\nWHERE\n{")
    Lang = lang.capitalize()
    # Triples
    triples = ''

    # 1. prop-val triples
    #pvlist = pvalue.split(",")
    #print(str("pvlist= " + str(pvlist)))
    #print("\nParadigm Common Property-Value Pairs:")
    for pv in pvlist:
        #print(str(pv))
        propval = pv.split(":")
        if propval[0] == "language":
            triple = str("    ?s aamas:lang aama:" + Lang + " .\n")
        elif propval[0] == "lexeme":
            triple = str("    ?s aamas:lexeme / rdfs:label \'" +  propval[1] + "\' .\n    ?s aamas:lexeme / rdfs:label ?lexeme  .\n    ?s aamas:lexeme / aamas:gloss ?gloss  .\n")
        else:
            triple = str("    ?s " + lpref + ":" + propval[0] + " " + lpref + ":" + propval[1] + " .\n")
        triples = triples + triple

    # 2. selection triple -- for the moment only 'source'
    triple = str("    ?s aamas:memberOf / rdfs:comment  ?note .\n" )
    triples = triples + triple
    triples = str(triples + "}\n")
    order = str("ORDER BY " + selection)

    query = str(prefixes + select + triples + order)

    return query
 
def pinfoquery(pinfo,lang):
    prefixes = str(prefixbase + "\n")
    selection = str("?" + pinfo.replace(","," ?"))
    select = str("SELECT DISTINCT " + selection + "\nWHERE\n{")
    Lang = lang.capitalize()
    triples = ''
    pvlist = pinfo.split(",")
    for pv in pvlist:
        triple = str("    OPTIONAL { aama:" + Lang + " aamas:" + pv + " ?" + pv + " . }\n")
        triples = triples + triple
    triples = str(triples + "}\n")
    query = str(prefixes + select + triples + "\n")
    return query

def formsquery(languages,qstring):
    # To ask whether specific forms exist in one or more langs,
    # e.g. whether 2f exists in [alagwa, . . .]
    # qstring = 'person=Person2,gender=Fem,number=?number,pos=?pos'
    # Select statement
    pvals = qstring.split(",")
    selection = '?language '
    for pval in pvals:
        if '?' in pval:
            qpval = pval.split('=')
            qval = str(qpval[1] + 'label ') 
            selection += qval
    selection += '?token ?pdgmLabel'
    select = str('SELECT DISTINCT ' + selection + '\nWHERE {\n')
    #print(select)
    triples = ''
    prefixes = prefixbase
    llist = languages.split(",")            
    for lang in llist:
        #print(str('lang = ' + lang))
        # Get lpref
        lpref = lname2labb[lang]
        # Update prefixes
        lprefix = str("PREFIX " + lpref + ": <http://id.oi.uchicago.edu/aama/2013/" + lang + "/>")
        prefixes = str(prefixes + lprefix + "\n")
        # Initialize triples
        triples += str('{GRAPH aamag:' + lang + '{\n')
        # triples += str('{GRAPH aamag:' + lang + '{\n?s ?p ?o .\n')
        # Get lpref
        lpref = lname2labb[lang]
        # Triples
        # 1. prop-val triples
        #pvlist = pvalue.split(",")
        for pval in pvals:
            if '?' in pval:
                qpval = pval.split('=')
                qvalLabel = str(qpval[1] + 'label ') 
                triple = str('?s ' + lpref + ':' + qpval[0] + ' ' + qpval[1] + ' .\n' + qpval[1] + ' rdfs:label ' + qvalLabel + ' .\n')
                triples += triple
            else:
                qpval = pval.split('=')
                triple = str('?s ' + lpref + ':' + qpval[0] + ' ' + lpref + ':' + qpval[1] + ' .\n')
                triples += triple
        # 2. fixed triples
        tkntrpl = str('?s ' + lpref + ':token ?token .\n')
        pdgmtrpl = '?s aamas:memberOf ?pdgm .\n?pdgm rdfs:label ?pdgmLabel .\n'
        langtrpl = '?s aamas:lang ?lng .\n?lng  rdfs:label ?language .\n'
        triples += str(tkntrpl + pdgmtrpl + langtrpl + '}}\n')
        if lang != llist[-1]:
            triples += 'UNION\n'
        else:
            triples += '}\n'
    # Order statement
    order = str('ORDER BY  ' + selection)

    query = str(prefixes + select + triples + order + '\n')
    # print(str('QUERY:\n' + query))

    return query

lname2labb = {'beja-hud': 'bhu', 'afar': 'afr', 'oromo': 'orm', 'somali': 'som', 'alaaba': 'alb', 'alagwa': 'alg', 'akkadian-ob': 'aob', 'aari': 'aar', 'arabic': 'arb', 'arbore': 'abr', 'awngi': 'awn', 'bayso': 'bay', 'beja-alm': 'bal','beja-rei': 'bre', 'beja-rop': 'bro', 'beja-van': 'bva', 'beja-wed': 'bwe', 'berber-ghadames': 'bgh', 'bilin': 'bil', 'boni-jara': 'boj', 'boni-kijee-bala': 'bob', 'boni-kilii': 'bok', 'burji-sas': 'brs', 'burji-wed': 'brw','burunge': 'brn', 'coptic-sahidic': 'csa', 'dahalo': 'dah', 'dasenech': 'das', 'dhaasanac': 'dha', 'dizi': 'diz', 'egyptian-middle': 'egm', 'elmolo': 'elm', 'gawwada': 'gaw', 'gedeo': 'ged', 'geez': 'gez', 'hadiyya': 'had', 'hausa': 'hau', 'hdi': 'hdi', 'hebrew': 'heb', 'iraqw': 'irq', 'kambaata': 'kam', 'kemant': 'kem', 'khamtanga': 'khm', 'koorete': 'kor', 'maale': 'mal', 'mubi': 'mub', 'rendille': 'ren', 'saho': 'sah', 'shinassha': 'shn', 'sidaama': 'sid', 'syriac': 'syr', 'tsamakko': 'tsm', 'wolaytta': 'wol', 'yaaku': 'yak', 'yemsa': 'yem'}
        
    # Prefixes and select statement
prefixbase = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
PREFIX aama: <http://id.oi.uchicago.edu/aama/2013/> 
PREFIX aamas: <http://id.oi.uchicago.edu/aama/2013/schema/>
PREFIX aamag: <http://oi.uchicago.edu/aama/2013/graph/>
"""










'''
   {GRAPH aamag:alagwa {
   ?s ?p ?o .
   ?s alg:person alg:Person2 .
   ?s alg:gender alg:Fem .
   ?s alg:number ?number .
   ?number rdfs:label ?numberLabel .
   ?s alg:pos ?pos .
   ?pos rdfs:label ?posLabel .
   ?s alg:token ?token .
   ?s aamas:memberOf ?pdgm .
   ?pdgm rdfs:label ?pdgmLabel .
   ?s aamas:lang ?lng .
   ?lng rdfs:label ?language .
    }}
    UNION

PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX aama: <http://id.oi.uchicago.edu/aama/2013/>
PREFIX aamas: <http://id.oi.uchicago.edu/aama/2013/schema/>
PREFIX aamag: <http://oi.uchicago.edu/aama/2013/graph/>
PREFIX alb: <http://id.oi.uchicago.edu/aama/2013/alaaba/>
SELECT DISTINCT ?source 
WHERE
{    ?s aamas:lang aama:Alaaba .
    ?s alb:pos alb:Pronoun .
    ?s alb:proClass alb:AbsPoss .
    ?s aamas:memberOf / rdfs:comment ?source.
}

''' 
 






