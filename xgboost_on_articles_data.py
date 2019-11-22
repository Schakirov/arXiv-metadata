## open in python3.6

import pandas as pd
import sklearn
import xgboost
import pickle

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
#df = pd.read_csv('parkinsons.data')

def load_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)

df = load_obj('articles_data.pkl')
features = df['eqA']
labels = df['eqC']
labels = [i>1 for i in labels]

scaler = MinMaxScaler((-1, 1))
X = scaler.fit_transform(features)
X_train, X_test, Y_train, Y_test = train_test_split(X, labels, test_size=0.14)
model = xgboost.XGBClassifier()

model.fit(X_train, Y_train)

Y_hat = [round(yhat) for yhat in model.predict(X_test)]
print(accuracy_score(Y_test, Y_hat)) 
