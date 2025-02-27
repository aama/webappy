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
    lpref = lname2labb[lang]
    lprefix = str("PREFIX " + lpref + ": <http://id.oi.uchicago.edu/aama/2013/" + lang + "/>")
    prefixes = str(prefixbase + lprefix + "\n")
    
    selection = str("?" + valstring.replace(","," ?"))
    selection = selection.replace("-", "")
    select = str("SELECT DISTINCT " + selection + "\nWHERE\n{")
    Lang = lang.capitalize()
    
    # Triples
    triples = ''
    # 1. prop-val triples
    #pvlist = pvalue.split(",")
    print(str("pvlist= " + str(pvlist)))
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
    sels = valstring.split(",")
    for sel in sels:
        sel2 = sel.replace("-", "")
        # Want to insist on "token" but let "token-note" be optional
        if sel[0:5] == "token":
            if sel[5::] == '-note':
                triple = str("    OPTIONAL { ?s " + lpref + ":token-note  ?" + sel2 + " }\n")
            else:
                triple = str("   OPTIONAL { ?s " + lpref + ":token  ?" + sel2 + " }\n")
        #elif sel == "tokenNote":
            #triple = str("    ?s " + lpref + ":tokenNote ?tokenNote .\n")
        elif sel == "lexeme":
            triple = str("    ?s aamas:lexeme / rdfs:label ?" + sel2 + " .\n")
        elif sel  == "language":
            triple = str("    ?s aamas:lang / rdfs:label ?" + sel2 + " .\n")
        else:
            triple = str("    OPTIONAL { ?s " + lpref + ":" + sel + " / rdfs:label ?" + sel2 + " }\n")
        triples = triples + triple
    triples = str(triples + "}\n")
    #order statement
    selection = selection.replace("?number", "DESC(?number)")
    selection = selection.replace("?gender ", "DESC(?gender)")
    order = str("ORDER BY " + selection)

    query = str(prefixes + select + triples + order +  "\n")

    print("=======================")
    return query

def sourcequery(pvlist,svalstring,lang):
    #print("\nFrom 'pdgmDispQuery.py': \n====================")
    #print("\nsourcequery function output: \n====================")
    #print(str("pvalue: " + pvalue))
    #print(str("svalstring: " + svalstring))
    lpref = lname2labb[lang]
    #print(str("lang, lpref: " + lang + ", " + lpref))
    lprefix = str("PREFIX " + lpref + ": <http://id.oi.uchicago.edu/aama/2013/" + lang + "/>")
    prefixes = str(prefixbase + lprefix + "\n")
    # Selection
    selection = str("?" + svalstring)
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
            triple = str("    ?s aamas:lexeme / rdfs:label \'" +  propval[1] + "\' .\n")
        else:
            triple = str("    ?s " + lpref + ":" + propval[0] + " " + lpref + ":" + propval[1] + " .\n")
        triples = triples + triple

    # 2. selection triple -- for the moment only 'source'
    triple = str("    ?s aamas:memberOf / rdfs:comment  ?note .\n" )
    triples = triples + triple
    triples = str(triples + "}\n")

    query = str(prefixes + select + triples )

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
        print(str('lang = ' + lang))
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
 






