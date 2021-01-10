import pandas as pd
import csv
import sys
import itertools
import string
import pickle
from collections import defaultdict

# takes id and returns the tag string
def tag(info,id):
  for ind,row in info.iterrows():
    if(row[0] == id):
      return row[1]

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
  if(w >= 0.2):
    return w
  elif(w >=0.1):
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

with open('entropy.p', 'rb') as fp:
  h = pickle.load(fp)


tags  = pd.read_csv('filtags.csv',header=0,delimiter=',')

tag_id = defaultdict(int)
for ind,row in tags.iterrows():
  tag_id[row[1]] = row[0]


def succ(X,Y):
  m = len(X)
  n = len(Y)
  if(m>n):
    return 0
  elif(n>m):
    return 1
  else:    
    result = 0  
    for i in range(min(m,n)):
      if(X[i]!=Y[i]):
        break
      result = result + 1
    v1 = X[result:]
    v2 = Y[result:]
    if(is_number(v1) and is_number(v2)):
      if(float(v1) > float(v2)):
        return 0
      else:
        return 1
    else:
      if(h[tag_id[X]] > h[tag_id[Y]]):
        return 0
      else:
        return 1  
  return 1



info = pd.read_csv("communities.csv",header=0,delimiter=' ')


with open('comm.p', 'rb') as fp:
  comm = pickle.load(fp)


l = []

for ind,row in info.iterrows():
  #print(row[0].split(":")[0])
  if(row[0].split(":")[0] == str(sys.argv[1])):########## Give the cluster number here
    l.append(row[2])


suuc_pred = []
l1 = []
l1.append('Predecessor')
l1.append('Successor')
l1.append('Weight')
suuc_pred.append(l1)

for comb in itertools.combinations(l,2):
  weight = lcs(comb[0],comb[1])
  if(weight >= 0.1):#### adjust hyper param here
    l = []
    if(succ(comb[0],comb[1]) == 1):
      l.append(comb[0])
      l.append(comb[1])
      l.append(weight)
      print(comb[0],comb[1],".......")
    else:
      l.append(comb[1])
      l.append(comb[0])
      l.append(weight)
      print(comb[1],comb[0])  
    suuc_pred.append(l)

with open("succ_pred.csv", 'w') as csvfile:  
  # creating a csv writer object  
  csvwriter = csv.writer(csvfile)  
  # writing the data rows  
  csvwriter.writerows(suuc_pred)

