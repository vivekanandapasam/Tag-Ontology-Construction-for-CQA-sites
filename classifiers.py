import sklearn
from sklearn.model_selection import train_test_split
import pandas as pd
from imblearn.over_sampling import SMOTE 
import numpy as np 
from sklearn.linear_model import LogisticRegression 
from sklearn.preprocessing import StandardScaler 
from sklearn.metrics import confusion_matrix, classification_report
# data = pd.read_csv("balanced_pc.csv",header=0,delimiter=',')
data = pd.read_csv("sib_df_of.csv",header=1,delimiter=',')
f = []
X = []
label = []
for ind,row in data.iterrows():
  f = []
  # if(str(row[2]) == "Yes"):
  #   f.append(1)
  # else:
  #   f.append(0)
  f.append(row[3])
  # if(str(row[4]) == "Yes"):
  #   f.append(1)
  # else:
  #   f.append(0)
  f.append(row[5])   
  X.append(f)
  label.append(int(row[6]))    


X_train, X_test, y_train, y_test = train_test_split(X,label,test_size = 0.3, random_state = 0) 
 
# describes info about train and test set 
# print("Number transactions X_train dataset: ", X_train.shape) 
# print("Number transactions y_train dataset: ", y_train.shape) 
# print("Number transactions X_test dataset: ", X_test.shape) 
# print("Number transactions y_test dataset: ", y_test.shape) 
lr = LogisticRegression() 
  
# train the model on train set 
lr.fit(X_train, y_train) 
  
predictions = lr.predict(X_test) 
  
# print classification report 
print(classification_report(y_test, predictions)) 
sm = SMOTE(random_state = 2)
print("Before OverSampling, counts of label '1': {}".format(y_train.count(1))) 
print("Before OverSampling, counts of label '0': {} \n".format(y_train.count(0))) 
 
X_train_res, y_train_res = sm.fit_sample(X_train, y_train)

print("After OverSampling, counts of label '1': {}".format(sum(y_train_res == 1))) 
print("After OverSampling, counts of label '0': {}".format(sum(y_train_res == 0))) 
lr1 = LogisticRegression() 
lr1.fit(X_train_res, y_train_res.ravel()) 
predictions = lr1.predict(X_test) 
  
# print classification report 
print(classification_report(y_test, predictions)) 



# svm classifier
from sklearn import svm

#Create a svm Classifier
clf = svm.SVC(kernel='rbf') # Linear Kernel

#Train the model using the training sets
clf.fit(X_train_res, y_train_res.ravel())

#Predict the response for test dataset
y_pred = clf.predict(X_test)

print(classification_report(y_test, y_pred)) 


# Naive bayes classifiers
from sklearn.naive_bayes import GaussianNB

#Create a Gaussian Classifier
gnb = GaussianNB()

#Train the model using the training sets
gnb.fit(X_train_res, y_train_res.ravel())

#Predict the response for test dataset
y_pred = gnb.predict(X_test)
print(classification_report(y_test, y_pred)) 


#random forrest
from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(max_depth=3, random_state=0)
clf.fit(X_train_res, y_train_res.ravel())

#Predict the response for test dataset
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))
