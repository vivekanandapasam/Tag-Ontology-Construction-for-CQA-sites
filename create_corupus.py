# creates corpus in a txt file

import urllib
import pandas as pd
import re
import pickle
import ast

#cleans tha raw html text of body of the posts
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  cleantext = cleantext.replace('\n',' ')
  # print(cleantext,'....')
  return cleantext

out = open("glove_corpus.txt","w")

cat_new = {}
cat_links = pd.read_csv("cat_links.csv",header=0,delimiter=',')
for ind,row in cat_links.iterrows():
  cat_new[row[0]] =  ast.literal_eval(row[1])

tags  = pd.read_csv('datacsv/Filtags.csv',header=0,delimiter=',')


# this piclle file contains all abtsracts of tags from wikipedia
with open('abstract.p', 'rb') as fp:
  abstract = pickle.load(fp)

l = {}
for ind,row in tags.iterrows():
  l[row[1]] = []
  l[row[1]].append(row[3])
  l[row[1]].append(row[4])

# print('here 1')

posts = pd.read_csv('datacsv/Filpos.csv',header=0,delimiter=',')

for tag in abstract.keys():
  string = " "
  if(abstract[tag] != []):
    string += abstract[tag][0]
  # print(abstract[tag][0],out)
  for i in l[tag]:
    try:
      req_post = posts[posts.Id == i]
      # print(cleanhtml(req_post['Body'].iloc[0]),out)
      string += cleanhtml(req_post['Body'].iloc[0])
    except:
      pass  
  for i in cat_links[tag]:
    string += " " + i 
  string = ''.join([i for i in string if not i.isdigit()])

  string += "\n"
  out.write(string)  

