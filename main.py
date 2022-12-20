import math

import pandas as pd
import numpy as np
from model import Model
from math import *

# chargement des donnees
df = pd.read_csv('C:\\Users\\USER\\PycharmProjects\\datamining2groupeferhat\\adm_data.csv')


def convert_classes(s):
    if s >= 0.50:
        return 1
    elif s < 0.50:
        return 0


def convert_data(df: pd.DataFrame):
    l = []
    for _, r in df.iterrows():
        t = list(r[1:])
        t[-1] = convert_classes(t[-1])
        l.append(t)

    return l


def accuracy(prediction, trues):
    if len(prediction) != len(trues):
        raise ValueError('les longueur sont different')
    s = 0
    for i in range(len(trues)):
        if trues[i] == prediction[i]:
            s = s + 1
    return s / len(trues)


L = convert_data(df)
L = np.array(L)
np.random.shuffle(L)
X = L[:, :7]
Y = L[:, 7]
Y = list(Y)
l2 = []
a=int(len(X)*0.7)
x_train = X[0: a]
y_train = Y[0: a]
x_test = X[a:]
y_test = Y[a:]
att = ["GRE_Score", "TOEFL_Score", "University_Rating", "SOP", "LOR", "CGPA", "Research"]
m = Model()
r = m.fit(x_train, y_train)
y_pred = m.predict_all(r,x_test,att)
print(len(y_pred[0]))
print(len(y_test))
print(accuracy(y_pred[0],y_test))

