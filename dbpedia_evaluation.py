import pandas as pd

def ground(comb):
  i = labels[((labels.tag_0 == comb[0]) & (labels.tag_1 == comb[1]))]
  if(i.empty):#if not present it means it is a false negative.. ground truth is 1
    return 1
  else:
    return i.label.values[0]# return label which is ground truth


dbpedia = pd.read_csv("dbpedia_annotations.csv",header=0,delimiter=',')
labels = pd.read_csv("pc_df_of.csv",header=0,delimiter=',')

tp_our = 0
tp_db  = 0
fp_our = 0
fp_db = 0
fn_our = 0
fn_db = 0
total = 0

for ind,row in dbpedia.iterrows():
  total += 1
  if(row[2] == 2 and ground(row)):# 2 is true for our and db
    tp_db += 1
    tp_our += 1 
  elif(row[2] == 2 and not ground(row)):
    fp_db += 1
    fp_our += 1 
  elif(row[2] == 0 and ground(row)):# 0 is true for our and not db
    tp_our += 1
    fn_db += 1
  elif(row[2] == 0 and not ground(row)):
    fp_our += 1
    # tp_db += 1
  elif(row[2] == 1 and ground(row)):# 1 is not present in our but in db
    fn_our += 1
    tp_db += 1
  else:
    fp_db += 1    
      

# print(ground(["linux","debian"]))

print("Total: ", total)
total = tp_our+fp_our+fn_our
print("Our results")
print("tp of our: ",tp_our,float(tp_our)/total)
print("fp of our: ",fp_our,float(fp_our)/total)
print("fn of our: ",fn_our,float(fn_our)/total)
total = tp_db+fp_db+fn_db      
print("Dbpedia results")    
print("tp of db: ",tp_db,float(tp_db)/total)
print("fp of db: ",fp_db,float(fp_db)/total)
print("fn of db: ",fn_db,float(fn_db)/total)      