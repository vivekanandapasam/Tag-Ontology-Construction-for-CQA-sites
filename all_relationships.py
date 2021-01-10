#takes parent child and sibling relationships and combines them for cluster 

# this is done just to see the results

import pandas as pd
import re
import pickle
import csv
import itertools
import sys

tags  = pd.read_csv('Filtags.csv',header=0,delimiter=',')
info = pd.read_csv("communities.csv",header=0,delimiter=' ')
par_chl = pd.read_csv("parent_child.csv",header=0,delimiter=',')
lda_sib = pd.read_csv("siblings_lda.csv",header=0,delimiter=',')
glove_sib = pd.read_csv("siblings_glove.csv",header=0,delimiter=',')


l = []

for ind,row in info.iterrows():
  #print(row[0].split(":")[0])
  if(row[0].split(":")[0] == str(sys.argv[1])):########## Give the cluster number here
    l.append(row[2])


rel = []
cols = []
cols.append('Pair')
cols.append('Parent_Child')
cols.append('Siblings_lda')
cols.append('Siblings_glove')
rel.append(cols)

def is_parent_child(tag1,tag2):
  i = par_chl[((par_chl.Parent == tag1) & (par_chl.Child == tag2))]
  if(i.empty):
    return 0
  else:
    # print(type(i))
    # print(i)
    # print(i.Similarity.values[0])
    # print(type(i.Similarity))
    return 1
    return i.Similarity.values[0] #rturn similarity


def is_lda_sibling(tag1,tag2):
  i = lda_sib[((lda_sib.Tag1 == tag1) & (lda_sib.Tag2 == tag2))]
  if(i.empty):
    return -1
  else:
    return i.Distance.values[0]# rturn dis

def is_glove_sibling(tag1,tag2):
  i = glove_sib[((glove_sib.Tag1 == tag1) & (glove_sib.Tag2 == tag2))]
  if(i.empty):
    return -1
  else:
    return i.Distance.values[0]# rturn dis  



# Assuming that the headnodes are present in the tags

for comb in itertools.combinations(l,2):
  # i = if p-c # check for reverse also
  # print(comb)
  wpc_1 = is_parent_child(comb[0],comb[1])
  wpc_2 = is_parent_child(comb[1],comb[0])
  wls_1 = is_lda_sibling(comb[0],comb[1])
  wls_2 = is_lda_sibling(comb[1],comb[0])
  wlg_1 = is_glove_sibling(comb[0],comb[1])
  wlg_2 = is_glove_sibling(comb[1],comb[0])
  if(wpc_1 or wpc_2 or wls_1 != -1 or wls_2 != -1 or wlg_1 != -1 or wlg_2!= -1):
    col = []
    if(wpc_1 or wpc_2):
      if(wpc_1):
        col.append(comb)
        col.append('Yes' + ' ' + str(wpc_1))
      if(wpc_2):
        col.append((comb[1],comb[0]))
        col.append('Yes' + ' ' + str(wpc_2))
    else:
      col.append(comb)
      col.append('No')

    if(wls_1!= -1 or wls_2!= -1):
      if(wls_1!= -1):
        col.append('Yes' + ' ' + str(wls_1))
      else:
          col.append('Yes' + ' ' + str(wls_2))
    else:
      col.append('No')  
    if(wlg_1!= -1 or wlg_2!= -1):
      if(wlg_1!= -1):
        col.append('Yes' + ' ' + str(wlg_1))
      else:
        col.append('Yes' + ' ' + str(wlg_2))    
    else:
      col.append('No')    
    rel.append(col)


with open("subs_sibs.csv", 'w') as csvfile:  
  # creating a csv writer object  
  csvwriter = csv.writer(csvfile)  
  # writing the data rows  
  csvwriter.writerows(rel)

