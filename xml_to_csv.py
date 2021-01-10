import pandas as pd
import xml.etree.ElementTree as et
import csv
import requests

tree = et.parse('./super meta/Posts.xml')
tree1 = et.parse('./super meta/Tags.xml')
root = tree.getroot()
root1 = tree1.getroot()
#print(root.tag)
#print(root1.tag)
#print(root.attrib)
#print(root1.attrib)

filt = []
filt1 = []
for child in root:
  #print(child.tag,child.attrib)
  news = {} 
  news['Accepted'] = 0
  for item in child.attrib:
    #print(item,child.attrib[item])
    #print("........")
    #print(type(item))
    if(item == str("Body")):
      if(child.attrib["Body"].encode('utf-8') == ""):
        break
      news["Body"] = child.attrib["Body"].encode('utf-8')
    if(item == 'Id'):
      news["Id"] = child.attrib["Id"]
    if(item == "Tags"):
      news['Tags'] = child.attrib['Tags']
    if(item == "AcceptedAnswerId"):
      news['Accepted'] = 1  
  if(not news == {}):
    filt.append(news)


for child in root1:
  news = {}
  for item in child.attrib:
    #print(item,child.attrib[item])
    if(item == 'Count') and (int(child.attrib["Count"]) < 100):
      break
    else:
      news["Count"] = child.attrib["Count"]
    if(item == 'Id'):
      news["Id"] = child.attrib["Id"]
    if(item == 'TagName'):
      news["TagName"] = child.attrib["TagName"]
    if(item == 'ExcerptPostId'):
      news["ExcerptPostId"] = child.attrib["ExcerptPostId"]
    if(item == 'WikiPostId'):
      news["WikiPostId"] = child.attrib["WikiPostId"]  
  if(not news=={}):
    filt1.append(news)      

#print(filt)

fields = ["Body","Tags","Id","Accepted"]

with open("./datacsv/Filpos.csv",'w') as csvfile:
  writer = csv.DictWriter(csvfile,fieldnames=fields)
  writer.writeheader()
  writer.writerows(filt)


fields1 = ["Id","TagName","Count","ExcerptPostId","WikiPostId"]

with open("./datacsv/Filtags.csv",'w') as csvfile:
  writer = csv.DictWriter(csvfile,fieldnames=fields1)
  writer.writeheader()
  writer.writerows(filt1)
