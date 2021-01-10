import pandas as pd
import csv
from collections import defaultdict
import math
import numpy as np
from collections import Counter
import random
#import wikipedia

tags = pd.read_csv("datacsv/Filtags.csv",header=0,delimiter=',')

tags = tags[tags.Count > 100]

tags.to_csv('datacsv/Filtags.csv',index=False)

#tags = tags.drop(['_Count','_Count','_ExcerptPostId','_WikiPostId'],axis=1)
#print(tags.head(5))
#tags.to_csv("/home/vivekananda/Desktop/Mini Project/datacsv/nodes.csv",sep=',')

tagid = defaultdict(int)
tagname = dict()
for index,row in tags.iterrows():
  tagid[row[1].lower()] = row[0]
  tagname[row[0]] = row[1].lower()


class post:
  def __init__(self,id,tags,body):
    self.id = id
    self.tags = tags
    self.body = body


class tag:
  def __init__(self,id,posts):
    self.id = id
    self.posts = posts


pos_to_tag = defaultdict(list)
tag_to_pos = defaultdict(list)

#concepts = []

reader = pd.read_csv("datacsv/Filpos.csv",header=0,delimiter=',')
print(reader.shape)

def addpos(tag,posid):
  tag_to_pos[tagid[tag]].append(posid)

'''
#edited here
n = len(reader.index)
while(len(tag_to_pos) < 300 ):############### see here 300
  print(len(tag_to_pos))
  row = reader.iloc[random.randint(0,n-1)]
  tag = ""
  #print(row[1])
  for i in str(row[1]):
    if i == '>':
      tag = tag.lower()
      pos_to_tag[row[2]].append(tagid[tag])
      if tag not in tag_to_pos:
        addpos(tag,row[2])
      tag = ""  
    elif i == '<':
      tag = ""
    else: 
      tag += i

'''
for index,row in reader.iterrows():
  #print(index)
  tag = ""
  #print(row[1])
  for i in str(row[0]):
    if i == '>':
      tag = tag.lower()
      if(tag in tagid):########### added condition here
        pos_to_tag[row[1]].append(tagid[tag])
        #if tag not in tag_to_pos:
        addpos(tag,row[1])
      #if(wikipedia.search(tag)):
      #    concepts.append(tag)
      #print(tag)
      tag = ""
    elif i == '<':
      tag = ""
    else: 
      tag += i



print(len(pos_to_tag))
#print(pos_to_tag)
print(len(tag_to_pos))
#print(len(concepts))






