
import numpy as np
from sklearn.utils import shuffle
from sklearn.preprocessing import MinMaxScaler
import os
import pandas as pd
import time
from talib import abstract
import progressbar
import tensorflow as tf
import copy
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

csv_file_path = 'big_data/ml_v1/5min/'

df = pd.read_csv(f'{csv_file_path}1000SATSUSDT.csv')

train, valid, test = np.split(df.sample(frac=1), [int(0.6*len(df)), int(0.8*len(df))])

# получаем в нампи разделенные x и y и массив целиком, передав датафрейм
def scale_dataset(dataframe):
  X = dataframe[dataframe.columns[:-2]].values
  y = dataframe[dataframe.columns[-2:]].values
  scaler = StandardScaler()
  X = scaler.fit_transform(X)
  # data = np.hstack((X, y))
  data = np.hstack((X, np.reshape(y, (-2, 2))))
  return data, X, y

train_data, X_train, y_train = scale_dataset(train)
valid_data, X_valid, y_valid = scale_dataset(valid)
test_data, X_test, y_test = scale_dataset(test)



































