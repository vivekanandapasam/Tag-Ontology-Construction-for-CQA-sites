import re
import pandas as pd
import csv

def ground(comb):
  i = labels[((labels.tag_0 == comb[0]) & (labels.tag_1 == comb[1]))]
  if(i.empty):#if not present it means it is a false negative.. ground truth is 1
    return 1
  else:
    return i.label.values[0]# return label which is ground truth


webis = pd.read_csv("all_webis_labels.csv",header=0,delimiter=',')
labels = pd.read_csv("pc_df_of.csv",header=0,delimiter=',')

tp_our = 0
tp_web  = 0
fp_our = 0
fp_web = 0
fn_our = 0
fn_web = 0
total = 0

for ind,row in labels.iterrows():
  if(row[4] == 1 and row[2] == "Yes"):
    tp_our += 1
  elif(row[4] == 0 and row[2] == "Yes"):
    fp_our += 1
  elif(row[4] == 1 and row[2] == "No"):
    fn_our += 1

total = tp_our+fp_our+fn_our
print("Our results")
print("tp of our: ",tp_our,float(tp_our)/total)
print("fp of our: ",fp_our,float(fp_our)/total)
print("fn of our: ",fn_our,float(fn_our)/total)
      
  