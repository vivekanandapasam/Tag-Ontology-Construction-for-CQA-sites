import re
import pandas as pd
import csv

def ground(comb):
  i = labels[((labels.tag_0 == comb[0]) & (labels.tag_1 == comb[1]))]
  if(i.empty):#if not present it means it is a false negative.. ground truth is 1
    return 1
  else:
    return i.label.values[0]# return label which is ground truth


con = pd.read_csv("all_concept_net_annotations_pc.csv",header=0,delimiter=',')
labels = pd.read_csv("pc_df_of.csv",header=0,delimiter=',')

tp_our = 0
tp_cn  = 0
fp_our = 0
fp_cn = 0
fn_our = 0
fn_cn = 0
total = 0


for ind,row in con.iterrows():
  total+= 1
  if(row[2] == 1 and ground(row)):# 1 is true for our and db
    tp_cn += 1
    tp_our += 1 
  elif(row[2] == 1 and not ground(row)):
    fp_cn += 1
    fp_our += 1 
  elif(row[2] == 2 and ground(row)):# 2 is true for our and not db
    tp_our += 1
    fn_cn += 1
  elif(row[2] == 2 and not ground(row)):
    fp_our += 1
    # tp_db += 1
  elif(row[2] == 3 and ground(row)):# 3 is not present in our but in db
    fn_our += 1
    tp_cn += 1
  else:
    fp_cn += 1    
      
      
      

print("Total: ", total)
total = tp_our+fp_our+fn_our
print("Our results")
print("tp of our: ",tp_our,float(tp_our)/total)
print("fp of our: ",fp_our,float(fp_our)/total)
print("fn of our: ",fn_our,float(fn_our)/total)
total = tp_cn+fp_cn+fn_cn
print("Concept results")    
print("tp of cn: ",tp_cn,float(tp_cn)/total)
print("fp of cn: ",fp_cn,float(fp_cn)/total)
print("fn of cn: ",fn_cn,float(fn_cn)/total)            