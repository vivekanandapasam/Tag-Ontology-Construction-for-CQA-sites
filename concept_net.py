import requests
import pandas as pd
import itertools
import sys
import os
from time import sleep


# ubs_sibs is produced in all_relationships.py 
rel = pd.read_csv("subs_sibs.csv",header=0,delimiter=',')

def is_related(comb):
  i = rel[((rel.Pair == comb))]
  if(i.empty):
    return 0
  else:
    # print(type(i))
    # print(i)
    # print(i.Similarity.values[0])
    # print(type(i.Similarity))
    return (i.Parent_Child.values[0],i.Siblings_glove.values[0],i.Siblings_lda.values[0]) #rturn similarity


# print(is_related(str(('performance', 'memory'))))
# sys.exit(1)


concept_net = []
l =[]
l.append('Pair')
l.append('our_rel(\'PC,Sib_g,Sib_l\')')
l.append('con_net_rel')
concept_net.append(l)

info = pd.read_csv("communities.csv",header=0,delimiter=' ')

l = []

for ind,row in info.iterrows():
  if(row[0].split(":")[0] == str(sys.argv[1])):########## Give the cluster number here
    # print(row[2])
    q = "http://api.conceptnet.io/query?node=/c/en/" + str(row[2]).replace('-','_')
    r = requests.get(q).json()
    if(r['edges']!=[]):
      # print(str(row[2]).replace('-','_'),'....')
      l.append(row[2])

print(len(l),'....')

for comb in itertools.combinations(l,2) :
  a = comb[0].replace('-','_')
  b = comb[1].replace('-','_')
  ####replace - with _

  uri = """http://api.conceptnet.io/query?node=/c/en/""" + a+"""&other=/c/en/"""+ b
  
  try:
    response = requests.get(uri)
    # sleep(1)
    obj = response.json()
    if(obj['edges']!=[]):
      print(comb)
      is_re = is_related(str(comb))
      for edge in obj['edges']:
        l1 = []
        l1.append(comb)
        if(is_re):
          l1.append(is_re)
        else:
          l1.append(is_re)
        l1.append(str(edge['start']['label']) + ' ' + str(edge['rel']['label']) + ' ' + str(edge['end']['label']))  
        concept_net.append(l1)
        # print(edge['start']['label'],edge['rel']['label'],edge['end']['label'])
      # print(uri)
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)
    print(e)
    print(uri)
    # print(requests.get(uri).json())
    pass 
    # break        


import csv
with open("concept_net.csv", 'w') as csvfile:  
  # creating a csv writer object  
  csvwriter = csv.writer(csvfile)  
  # writing the data rows  
  csvwriter.writerows(concept_net)
