import model.labeled_lda as llda
import pandas as pd
import csv
import pickle
import ast
import sys
from gensim.parsing.preprocessing import remove_stopwords
import re

# uncomment this while loading from the model

# # load from disk
# llda_model_new = llda.LldaModel()
# llda_model_new.load_model_from_dir('lda_model_dataset', load_derivative_properties=False)
# print "llda_model_new", llda_model_new
# llda_model = llda_model_new
# print "Top-10 terms of topic  ", llda_model.top_terms_of_topic("Microsoft_email_software", 20, False)
# print "Top-10 terms of topic  ", llda_model.top_terms_of_topic("Email", 20, False)

# # print "Doc-Topic Matrix: \n", llda_model.theta
# # print "Topic-Term Matrix: \n", llda_model.beta



# sys.exit(1)
cat_links  = pd.read_csv('cat_links.csv',header=0,delimiter=',')

# with open('abstract.p', 'rb') as fp:
#   abstract = pickle.load(fp)

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  cleantext = cleantext.replace('\n',' ')
  # print(cleantext,'....')
  return cleantext

abstract = {}
dataset = pd.read_csv('tag_wiki_excerpt.csv',header=0,delimiter=',')
for ind,row in dataset.iterrows():
  # print(row[0])
  string = ""
  try:
    string += row[1]
  except:
    pass  
  try:
    string += cleanhtml(row[2])
  except:
    pass  
  abstract[row[0]] = string


labeled_documents = []
for ind,row in cat_links.iterrows():
  l = ast.literal_eval(row[1])
  if(l!=[]):
    # print(row[0],l)
    result = remove_stopwords(abstract[row[0]].lower())
    result = ''.join([i for i in result if not i.isdigit()])
    labeled_documents.append((result,[x.lower() for x in l]))
    print(result,l)

llda_model = llda.LldaModel(labeled_documents=labeled_documents, alpha_vector=0.01)
print(llda_model)

for i in range(0,200):
    print("iteration %s sampling..." % (llda_model.iteration + 1))
    llda_model.training(1)
    print("after iteration: %s, perplexity: %s" % (llda_model.iteration, llda_model.perplexity()))
    print("delta beta: %s" % llda_model.delta_beta)
    if llda_model.is_convergent(method="beta", delta=0.1):
        break



# save to disk
save_model_dir = "lda_model_dataset"
# llda_model.save_model_to_dir(save_model_dir, save_derivative_properties=True)
llda_model.save_model_to_dir(save_model_dir)
