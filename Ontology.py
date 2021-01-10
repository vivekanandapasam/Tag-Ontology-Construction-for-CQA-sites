from cleandata import tag_to_pos
from cleandata import pos_to_tag
from cleandata import tagid
from cleandata import tagname
import pandas as pd
from collections import defaultdict
import math
import numpy as np
import itertools
import csv
import sys
import gc
from heapq import nlargest

comm = defaultdict(lambda: defaultdict(lambda:0))



# this function calculates google distance
def gdistance(tag1,tag2):
  common = sum([x == y for x in tag_to_pos[tag1] for y in tag_to_pos[tag2]] )
  comm[tag1][tag2] = comm[tag2][tag1] = common
  if(common == 0):
    return float('inf')
  nume = max(math.log(len(tag_to_pos[tag1])),math.log(len(tag_to_pos[tag2])))-math.log(common)
  #nume = max((len(tag_to_pos[tag1])),(len(tag_to_pos[tag2])))-(common)
  denom = math.log(len(pos_to_tag)) - min(math.log(len(tag_to_pos[tag1])),math.log(len(tag_to_pos[tag2])))
  #denom = (len(pos_to_tag)) - min((len(tag_to_pos[tag1])),(len(tag_to_pos[tag2])))
  return nume/denom


# claculates subsumption
def subsum(tag1,tag2):
  num = sim[tag1][tag2]
  den = 1
  for i in sim[tag1]:
    den += sim[tag1][i]
  return (num/den)




sim = defaultdict(lambda: defaultdict(lambda:0))

# similarity calculation
for comb in itertools.combinations(tag_to_pos.keys(),2):
  #print(gdistance(comb[0],comb[1]))
  sim[comb[0]][comb[1]] = sim[comb[1]][comb[0]] = 1/(math.exp(gdistance(comb[0],comb[1])))

#print(sim)

sim_new = {}
comm_new = {}


# converting defaultdict to dict so that it can be written to a pickle file. Or else create normal dict insted of defaultdict in the beginning itself.
for i in sim.keys():
  sim_new[i] = {}
  comm_new[i] = {}
  for j in sim[i].keys():
    sim_new[i][j] = sim[i][j]
    comm_new[i][j] = comm[i][j]

#print(sim_new)

import pickle


# wrting to pickle files
with open('sim.p', 'wb') as fp:
  pickle.dump(sim_new, fp, protocol=pickle.HIGHEST_PROTOCOL)

with open('comm.p', 'wb') as fp:
  pickle.dump(comm_new, fp, protocol=pickle.HIGHEST_PROTOCOL)

print("sim done")


# subsumption calculation
p = defaultdict(lambda: defaultdict(lambda:0))
for comb in itertools.combinations(tag_to_pos.keys(),2):
  p[comb[0]][comb[1]] = subsum(comb[0],comb[1]) * 10000# multiplying by 10000 for scaling
  
  
#print(p)


# wrting to a pickle file
# with open('sub.p', 'wb') as fp:
#   pickle.dump(p, fp, protocol=pickle.HIGHEST_PROTOCOL)
  
print("p done")

h = defaultdict(lambda : 0)

# finding entropy 'h' for each tag
for i in tag_to_pos.keys():
  for j in tag_to_pos.keys():
    #print(h[i])
    if(i!=j):
      #if(p[i][j] <= 0):
        #print(p[i][j],"..")
      h[i] -= p[i][j]*math.log( 1 + p[i][j])
#print(h)

h = {k:v for k,v in sorted(h.items(),key = lambda item: item[1])}
#print(h)
print("h done")

def N_large(c):
  count  = len(p[c])
  count = int(count/10)
  top = nlargest(count,p[c],key=p[c].get)
  return top

v = set()


filt = []

# forming edges
for i in h:
  #print(i,h[i])
  v.add(i)
  #print(tagname[i])
  top = []
  top = N_large(i)
  for j in top:
    news ={}
    if(h[i] < h[j] and comm[i][j] > 0):#(0.05)*(max(len(tag_to_pos[i]),len(tag_to_pos[j])))):############ should add some threshold
      news["Source"] = i
      news["Target"] = j
      news["Weight"] = p[i][j]
      filt.append(news)

# wrting edges
with open("./datacsv/edges.csv",'w') as csvfile:
  writer = csv.DictWriter(csvfile,delimiter = ' ' ,fieldnames=['Source','Target','Weight'])
  writer.writeheader()
  writer.writerows(filt)

################# should also create nodes file

df = pd.read_csv("./datacsv/Filtags.csv",header=0,delimiter=',')
df.rename(columns = {'Id' : 'id','TagName' : 'label'},inplace = True)
df.update('"' + df[['label']].astype(str) + '"')
del df['Count']
print(df.to_string(index = False))
df.to_csv("./datacsv/nodes.csv",index=False,sep=' ')






