import pandas as pd
from collections import defaultdict
import math
import numpy as np
import itertools
import csv
import sys
import gc
import pickle
from heapq import nlargest

tags  = pd.read_csv('filtags.csv',header=0,delimiter=',')
tagid = defaultdict(str)
count = defaultdict(int)
for ind,row in tags.iterrows():
  tagid[row[0]] = str(row[1])
  count[row[0]] = int(row[2])


info = pd.read_csv("communities.csv",header=0,delimiter=' ')

l = []

for ind,row in info.iterrows():
  if(row[0].split(":")[0] == '2'):########## Give the cluster number here
    l.append(row[3])

with open('comm.p', 'rb') as fp:
  comm = pickle.load(fp)

support = []
l1 = []
l1.append("Parent")
l1.append("Child")
l1.append("Support")
support.append(l1)

for comb in itertools.combinations(l,2):
  l1 = []
  if(count[comb[0]] > count[comb[1]]):
    l1.append(tagid[comb[0]])
    l1.append(tagid[comb[1]])
  else:
    l1.append(tagid[comb[1]])
    l1.append(tagid[comb[0]])
  # print(comb[0],comb[1])
  l1.append(float(comm[comb[0]][comb[1]])/(count[comb[0]] + count[comb[1]] - comm[comb[0]][comb[1]]))
  support.append(l1)
     
with open("support.csv", 'w') as csvfile:    
  csvwriter = csv.writer(csvfile)    
  csvwriter.writerows(support)
