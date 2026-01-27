#!/usr/local/bin/python3
'''
produces up-tp-date lists:
     lname2labb.dict
     labb2lname.dict

query to produce csv:

PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX aamas: <http://id.oi.uchicago.edu/aama/2013/schema/>
SELECT DISTINCT ?lname ?lpref
WHERE {
	?lang a aamas:Language .
 	?lang rdfs:label ?lname .
  	?lang aamas:lpref ?lpref .
  }
ORDER BY  ?lname

'''

from SPARQLWrapper import SPARQLWrapper, JSON

f = ('times',16) #'the pleasing font'

res = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>/n
PREFIX aamas: <http://id.oi.uchicago.edu/aama/2013/schema/>/n
SELECT DISTINCT ?lname ?lpref/n
WHERE {/n
	?lang a aamas:Language ./n
 	?lang rdfs:label ?lname ./n
  	?lang aamas:lpref ?lpref ./n
  }
ORDER BY  ?lname
"""

sparql = SPARQLWrapper("http://localhost:3030/aama/query")
sparql.setQuery(res)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
results2 = sparql.query()
print("results")
print(results)
print('results2')
print(results2)

