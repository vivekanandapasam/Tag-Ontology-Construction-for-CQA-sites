import sparql
import csv
import pandas as pd
import ast

# the dbpedia links of tags are obtained manuallys

cat_links = {}

dbpedia_links = pd.read_csv('dbpedia_links.csv',header=0,delimiter=',')


for ind,row in dbpedia_links.iterrows():
  link = str(row[2])
  cat_links[row[1]] = []
  if(link!=""):
    link = link.replace("page","resource")
    q = """SELECT ?cat
WHERE {
<""" + link + """> dct:subject ?cat
}"""
    print(q)
    result = sparql.query('http://dbpedia.org/sparql', q)
    for res in result:
      cat = (str(res[0]).rsplit('/',1)[-1]).rsplit(':',1)[-1]
      # print(cat)
      cat_links[row[1]].append(cat)



import pickle
with open('cat_links.p', 'wb') as fp:
  pickle.dump(cat_links, fp, protocol=pickle.HIGHEST_PROTOCOL)


def remove_non_ascii(text):
  return ''.join([i if ord(i) < 128 else ' ' for i in text])

abstracts = {}
dbpedia_links = pd.read_csv('dbpedia_links.csv',header=0,delimiter=',')

for ind,row in dbpedia_links.iterrows():
  link = str(row[2])
  abstracts[row[1]] = []
  if(link!=""):
    link = link.replace("page","resource")
    q = """SELECT (str(?cat) as ?cat)
WHERE {
<""" + link + """> dbo:abstract ?cat
FILTER langMatches( lang(?cat), "EN" )
}"""
    print(q)
    result = sparql.query('http://dbpedia.org/sparql', q)
    for res in result:
      print(type(res[0]))
      abst = (remove_non_ascii(repr(res[0])))
      # print(cat)
      abstracts[row[1]].append(abst)
      # print(abst)



import pickle
with open('abstract.p', 'wb') as fp:
  pickle.dump(abstracts, fp, protocol=pickle.HIGHEST_PROTOCOL)

