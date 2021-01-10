#takes input from gephi_edges and succ_pred edges and filters out succ pred from gephi edges and also maintain only head tags

import pandas as pd
import csv
import pickle
import math
import itertools
from collections import defaultdict
import sys
import string


edges = pd.read_csv('gephi_edges.csv',header=0,delimiter=',')
tags  = pd.read_csv('/datacsv/Filtags.csv',header=0,delimiter=',')

tag_id = defaultdict(int)
for ind,row in tags.iterrows():
  tag_id[row[1]] = row[0]



with open('comm.p', 'rb') as fp:
  comm = pickle.load(fp)

with open('entropy.p', 'rb') as fp:
  h = pickle.load(fp)

entropy = h

succ = pd.read_csv('succ_pred.csv',header=0,delimiter=',')
for ind,row in succ.iterrows():
  i = edges[((edges.Parent == row[0]) & (edges.Child == row[1]))]
  if(i.empty):
      i = edges[((edges.Parent == row[1]) & (edges.Child == row[0]))]
  if(not i.empty):
    index = i.index
    edges = edges.drop(index)### filtering out succ-pred from subsumption edges



changed = 1
while(changed):
  changed = 0
  for ind,row in succ.iterrows():
    if(entropy[tag_id[row[0]]] != entropy[tag_id[row[1]]]):
      entropy[tag_id[row[0]]] = entropy[tag_id[row[1]]] = max(entropy[tag_id[row[0]]],entropy[tag_id[row[1]]])
      changed = 1 # atleast 1 row changed


for ind,row in edges.iterrows():
  if(entropy[tag_id[row[0]]] < entropy[tag_id[row[1]]]):
    #print(row[0],row[1])
    edges.at[ind,'Parent'] = row[1]
    edges.at[ind,'Child'] = row[0]

# returns weight if succ-pred or else 0
def lcs(X, Y): 
  m = len(X)
  n = len(Y)
  result = 0  
  for i in range(min(m,n)):
    if(X[i]!=Y[i]):
      break
    result = result + 1
  w = float(result)/max(m,n)  
  if(w >= 0.7):
    return w
  elif(w >=0.6):
    if(is_number(X[-1]) or is_number(Y[-1])):
      return w
    else:
      return 0  
  return 0 

# checks if s is floar or not
def is_number(s):
  try:
      float(s)
      return True
  except ValueError:
      return False


# find the head of the tag
def find_head(string):
  if(is_number(string[-1])):
    s = string.split("-")
    if(len(s) > 1):
      s = s[:-1]
      head_str = ""
      for i in s:
        if(i == s[-1]):
          head_str += i
        else:
          head_str += i + "-"  
      return head_str  
    else:
      for i in range(len(string)):
        if(is_number(string[i])):
          return string[:i]
  else:
    return string

rem = []

# there is some mistake in this.. getting duplicates.. see again

# changes succ-pred tags in parent-child relationships to their head nodes
for ind1,row1 in edges.iterrows():
  for ind2,row2 in edges.iterrows():
    if(ind1!=ind2 and (ind1 not in rem or ind2 not in rem)):
      if(lcs(row1[0],row2[0]) >= 0.6 and lcs(row1[1],row2[1]) >= 0.6):
        if(ind2 not in rem):
          rem.append(ind1)
          edges.at[ind2,'Parent'] = find_head(row2[0])
          edges.at[ind2,'Child'] = find_head(row2[1])
        else:
          rem.append(ind2)
          edges.at[ind1,'Parent'] = find_head(row1[0])
          edges.at[ind1,'Child'] = find_head(row1[1])
      if(lcs(row1[0],row2[0]) >= 0.6):
        edges.at[ind1,'Parent'] = find_head(row1[0])
      if(lcs(row1[1],row2[1]) >= 0.6):
        edges.at[ind1,'Child'] = find_head(row1[1])  


# removing duplicate edges
for ind,row in edges.iterrows():
  if(ind in rem):
    edges.drop(ind,inplace=True)

i = edges[(edges.Parent) == (edges.Child)]
edges = edges.drop(i.index)

print(edges)
edges.to_csv('parent_child.csv',index=0)

