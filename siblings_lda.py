from glove import Glove
from glove import Corpus
import pandas as pd
import string,nltk
from collections import defaultdict
import re
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
import numpy as np
import itertools
import sys
from gensim.parsing.preprocessing import remove_stopwords
import ast
import model.labeled_lda as llda
from pyemd import emd
import csv
import pickle

tags  = pd.read_csv('datacsv/Filtags.csv',header=0,delimiter=',')
t = []
for ind,row in tags.iterrows():
  t.append(row[1])




from gensim.models import KeyedVectors
model = KeyedVectors.load_word2vec_format("results_glove.txt",binary=False)


info = pd.read_csv("datacsv/communities.csv",header=0,delimiter=' ')
l = []

for ind,row in info.iterrows():
  #print(row[0].split(":")[0])
  if(row[0].split(":")[0] == str(sys.argv[1])):########## Give the cluster number here
    l.append(row[2])

# load labelled lda model from disk
llda_model = llda.LldaModel()
llda_model.load_model_from_dir('lda_model_dbpedia', load_derivative_properties=False)
# print("Top-10 terms of topic  ", llda_model.top_terms_of_topic("chrome", 20, False))

# sys.exit(1)


cat_new = {}
cat_links = pd.read_csv("cat_links.csv",header=0,delimiter=',')
for ind,row in cat_links.iterrows():
  cat_new[row[0]] =  ast.literal_eval(row[1])


# checks if s is floar or not
def is_number(s):
  try:
      float(s)
      return True
  except ValueError:
      return False

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

siblings = []
col = []
col.append('Tag1')
col.append('Tag2')
col.append('Distance')
siblings.append(col)


rep = string.maketrans(string.punctuation, ' '*len(string.punctuation))
for comb in itertools.combinations(l,2):
  if(lcs(comb[0],comb[1]) < 0.6): # eliminating succ_pred relationships
    l1 = []
    l2 = []
    for i in cat_new[comb[0]]:
      i = i.translate(rep)
      for j in word_tokenize((i.lower())):
        try:
          topics = llda_model.top_terms_of_topic(j,5, False)
          l1 += topics
        except:
          pass    
    for i in cat_new[comb[1]]:
      i = i.translate(rep)
      for j in word_tokenize((i.lower())):
        try:
          topics = llda_model.top_terms_of_topic(j,5, False)
          l2 += topics  
        except:
          pass
    dist = model.wmdistance(l1, l2)
    if(dist < 0.15):
      print(comb[0],comb[1],dist)
      col = []
      col.append(comb[0])
      col.append(comb[1])
      col.append(dist)
      siblings.append(col)


with open("siblings_lda.csv", 'w') as csvfile:  
  # creating a csv writer object  
  csvwriter = csv.writer(csvfile)  
  # writing the data rows  
  csvwriter.writerows(siblings)

    








