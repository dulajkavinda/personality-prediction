import pandas as pd
from numpy import *
import numpy as np
from sklearn import preprocessing
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn import neighbors
import pickle

data = pd.read_csv('train.csv')
array = data.values
# print(array)

# processing data
for i in range(len(array)):
    if array[i][0] == "Male":
        array[i][0] = 1
    else:
        array[i][0] = 0

# print(array)

df = pd.DataFrame(array)

# print(df.head())

maindf = df[[0, 1, 2, 3, 4, 5, 6]]
mainarray = maindf.values
print(mainarray)

temp = df[7]
train_y = temp.values
# print(train_y)
# print(mainarray)
train_y = temp.values

for i in range(len(train_y)):
    train_y[i] = str(train_y[i])

mul_lr = linear_model.LogisticRegression(multi_class='multinomial', solver='newton-cg', max_iter=1000)
mul_lr.fit(mainarray, train_y)

# save the model to disk
pickle.dump(mul_lr, open("./model.pkl", 'wb'))

testdata = pd.read_csv('text.csv')
test = testdata.values

for i in range(len(test)):
    if test[i][0] == "Male":
        test[i][0] = 1
    else:
        test[i][0] = 0

df1=pd.DataFrame(test)

testdf =df1[[0,1,2,3,4,5,6]]
maintestarray=testdf.values
print(maintestarray)

y_pred = mul_lr.predict(maintestarray)
for i in range(len(y_pred)) :
	y_pred[i]=str((y_pred[i]))
DF = pd.DataFrame(y_pred,columns=['Predicted Personality.'])
DF.index=DF.index+1
DF.index.names = ['Person No']
DF.to_csv("output.csv")
