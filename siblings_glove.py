from glove import Glove
from glove import Corpus
import pandas as pd
import string,nltk
from collections import defaultdict
import re
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
import numpy
import itertools
import sys
from gensim.parsing.preprocessing import remove_stopwords
import ast
import csv
from pyemd import emd
import pickle

tags  = pd.read_csv('/datacsv/Filtags.csv',header=0,delimiter=',')
t = []
for ind,row in tags.iterrows():
  t.append(row[1])



from gensim.models import KeyedVectors
model = KeyedVectors.load_word2vec_format("results_glove.txt",binary=False)


info = pd.read_csv("/datacsv/communities.csv",header=0,delimiter=' ')
l = []

for ind,row in info.iterrows():
  #print(row[0].split(":")[0])
  if(row[0].split(":")[0] == str(sys.argv[1])):########## Give the cluster number here
    l.append(row[2])




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
        l1.append(j)
    for i in cat_new[comb[1]]:
      i = i.translate(rep)
      for j in word_tokenize((i.lower())):
        l2.append(j)  

    dist = model.wmdistance(l1, l2)
    if(dist < 0.25):
      col = []
      col.append(comb[0])
      col.append(comb[1])
      col.append(dist)
      siblings.append(col)
      print(comb[0],comb[1],dist)


with open("siblings_glove.csv", 'w') as csvfile:  
  # creating a csv writer object  
  csvwriter = csv.writer(csvfile)  
  # writing the data rows  
  csvwriter.writerows(siblings)


#### uncomment this part for creating wiki model for the first time



# def read_corpus(file):
#   print('hi')
#   with open(file,'r') as f:
#     for line in f:
#       # line = line.decode("utf8")
#       #line = re.sub("[\(\[].*?[\)\]]", "", line)
#       line = line.lower()
#       line = line.replace('<literal','')
#       line = line.translate(None, string.punctuation)
#       text_tokens = word_tokenize(line)
#       #text_tokens = re.split("(\w[\w']*)",line)
#       tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]
#       # print(tokens_without_sw)
#       yield tokens_without_sw


# f = open('glove_corpus.txt','r')
# f1 = open('corpus_new.txt','w')
# for line in f:
#   f1.write(''.join([i if ord(i) < 128 else ' ' for i in line]))




# get_data = read_corpus('corpus_new.txt')

# corpus_model = Corpus()
# corpus_model.fit(get_data,window = 100)
# epochs = 10
# no_threads = 8

# glove = Glove(no_components = 100,learning_rate = 0.05)
# glove.fit(corpus_model.matrix,epochs=epochs,no_threads=no_threads,verbose = True)
# glove.add_dictionary(corpus_model.dictionary)
# glove.save('wiki_glove.model')

# with open("results_glove.txt", "w") as f:
#     for word in glove.dictionary:
#         f.write(word)
#         f.write(" ")
#         for i in range(0, 100):
#             f.write(str(glove.word_vectors[glove.dictionary[word]][i]))
#             f.write(" ")
#         f.write("\n")



# glove = Glove()
# glove = glove.load('wiki_glove.model')








