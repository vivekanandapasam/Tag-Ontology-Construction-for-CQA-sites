import sparql
import csv
import pandas as pd
import ast
import sys
import itertools

info = pd.read_csv("communities.csv",header=0,delimiter=' ')

par = pd.read_csv("parent_child.csv",header=0,delimiter=',')

def is_related(comb):
  i = par[((par.Parent == comb[0]) & (par.Child == comb[1]))]
  if(i.empty):
    return 0
  else:
    return i.Similarity.values[0] #rturn similarity


t = []

def is_present(hyper):
  tag = ""
  words = hyper.split('-')
  if(len(words) == 1):
    tag = "_" + hyper + "_"
  else:
    for i in words:
      tag += i + "_"

  q = """PREFIX isa: <http://webisa.webdatacommons.org/concept/>
PREFIX isaont: <http://webisa.webdatacommons.org/ontology#> 
SELECT ?hypernymLabel ?hyponymLabel ?confidence
WHERE{
    GRAPH ?g {
        isa:""" + tag + """ skos:broader ?hyponym.
    }
    isa:""" +tag+""" rdfs:label ?hypernymLabel.
    ?hyponym rdfs:label ?hyponymLabel.
    ?g isaont:hasConfidence ?confidence.
    
}
ORDER BY DESC(?confidence)"""
  try:
    result = sparql.query('http://webisa.webdatacommons.org/sparql', q)
  except:
    result = [] 
  if(result==[]):
    return 0
  else:
    return 1    


for ind,row in info.iterrows():
  #print(row[0].split(":")[0])
  if(row[0].split(":")[0] == str(sys.argv[1])):########## Give the cluster number here
    if(is_present(str(row[2]))):
      t.append(row[2])

def is_parent(hyper,hypo):
  tag = ""
  words = hyper.split('-')
  if(len(words) == 1):
    tag = "_" + hyper + "_"
  else:
    for i in words:
      tag += i + "_"
  hypo = hypo.replace('_',' ')      
  q = """PREFIX isa: <http://webisa.webdatacommons.org/concept/>
PREFIX isaont: <http://webisa.webdatacommons.org/ontology#> 
SELECT ?hypernymLabel ?hyponymLabel ?confidence
WHERE{
    GRAPH ?g {
        isa:""" + tag + """ skos:broader ?hyponym.
    }
    isa:""" +tag+""" rdfs:label ?hypernymLabel.
    ?hyponym rdfs:label ?hyponymLabel.
    ?g isaont:hasConfidence ?confidence.
    
}
ORDER BY DESC(?confidence)"""

  # print(q)
  try:
    result = sparql.query('http://webisa.webdatacommons.org/sparql', q)
  except:
    print("....",hypo,hyper)
    result = []  
  for res in result:
    # print(str(res[1]))
    if(hypo == str(res[1])):
      print(hypo,hyper)
      return float(str(res[2]))
  return 0

# print(is_parent('ubuntu','linux'))

webisa = []
l = []
l.append('Pair')
l.append('Similarity')
l.append('Present_in_webisa')
webisa.append(l)

for comb in itertools.combinations(t,2):
  # print(comb)
  w = is_related(comb)
  if(w):
    l = []
    l.append(comb)
    l.append(w)
    l.append(is_parent(comb[1],comb[0]))
    webisa.append(l)

with open("web_isa.csv", 'w') as csvfile:  
  # creating a csv writer object  
  csvwriter = csv.writer(csvfile)  
  # writing the data rows  
  csvwriter.writerows(webisa)
