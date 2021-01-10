# takes cluster number as input and produces gephi_edges files which has edges of only that cluster 

import pandas as pd
import csv
import sys
import itertools
import string
from collections import Counter
from collections import defaultdict
import pickle

def tag(info,id):
  for ind,row in info.iterrows():
    if(row[0] == id):
      return row[1]



info = pd.read_csv("communities.csv",header=0,delimiter=' ')

l = []

for ind,row in info.iterrows():
  if(row[0].split(":")[0] == str(sys.argv[1])):########## Give the cluster number here
    l.append(row[3])


nodes = pd.read_csv("/datacsv/nodes.csv",header=0,delimiter=',')

edges = pd.read_csv("/datacsv/edges.csv",header=1,delimiter=',')


with open('comm.p', 'rb') as fp:
  comm = pickle.load(fp)


with open('sim.p', 'rb') as fp:
  sim = pickle.load(fp)  

fil_edges = []
sib = []
tot_avg = 0

for ind,row in edges.iterrows():
  if(row[0] in l and row[1] in l):
    fil_edges.append(row)
    tot_avg = tot_avg + row[2]


tot_avg = tot_avg/len(fil_edges)




edg = []
l = []
l.append('Parent')
#l.append('PId')
l.append('Child')
#l.append('CId')
l.append('Weight')
l.append('Similarity')
l.append('Co-occured posts')
edg.append(l)


for i in fil_edges:
  if(float(sim[i[0]][i[1]]) > 0.5):
    l = []
    l.append(tag(nodes,i[0]))
    #l.append(int(i[0]))
    l.append(tag(nodes,i[1]))
    #l.append(int(i[1]))
    l.append(i[2])
    l.append(sim[i[0]][i[1]])
    l.append(comm[i[0]][i[1]])
    edg.append(l)



with open("gephi_edges.csv", 'w') as csvfile: 
  csvwriter = csv.writer(csvfile)  
  csvwriter.writerows(edg)  


