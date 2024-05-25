
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
import matplotlib.pyplot as plt

csv_file_path = 'big_data/ml_v1/5min/'

df = pd.read_csv(f'{csv_file_path}1000SATSUSDT.csv')

train, valid, test = np.split(df.sample(frac=1), [int(0.6*len(df)), int(0.8*len(df))])

def print_trade(model):
  global X_test
#   cols = ['open','high','low','close','volume','hall','DEMA','EMA','HT_TRENDLINE','KAMA','MA','MIDPOINT','MIDPRICE','SMA','TEMA','TRIMA','WMA','ADX','ADXR','APO','AROON_down','AROON_up','BOP','CCI','CMO','DX','MACD','MFI','MINUS_DI','MINUS_DM','MOM','PLUS_DI','ROC','long','short']
#   df = pd.DataFrame(data=test_data, columns=cols)
  
#   result_model = model.predict(X_test)

  y = model.predict(X_test, verbose=0)
  
  print(y)

#   for data in X_test:
#     result_model = model.predict(list(data))
#     print(result_model)
#     time.sleep(5)


# получаем в нампи разделенные x и y и массив целиком, передав датафрейм
def scale_dataset(dataframe):
  X = dataframe[dataframe.columns[:-2]].values
  y = dataframe[dataframe.columns[-2:]].values
  scaler = StandardScaler()
  X = scaler.fit_transform(X)
  # data = np.hstack((X, y))
  data = np.hstack((X, np.reshape(y, (-2, 2))))
  return data, X, y

def plot_history(history,title,model):
  data_trade = print_trade(model)

  fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
  ax1.plot(history.history['loss'], label='Потери')
  ax1.plot(history.history['val_loss'], label='Значение потери')
  ax1.set_xlabel('Эпохи')
  ax1.set_ylabel('Бинарная кроссэнтропия')
  ax1.grid(True)

  ax2.plot(history.history['accuracy'], label='Точность')
  ax2.plot(history.history['val_accuracy'], label='Значение точности')
  ax2.set_xlabel('Эпохи')
  ax2.set_ylabel('точность')
  ax2.grid(True)

  ax1.set_title(title)

  plt.savefig(f'graph/{title}.png')
#   plt.show()

train_data, X_train, y_train = scale_dataset(train)
valid_data, X_valid, y_valid = scale_dataset(valid)
test_data, X_test, y_test = scale_dataset(test)

def train_model(X_train, y_train, num_nodes, dropout_prob, lr, batch_size, epochs):
  nn_model = tf.keras.Sequential([
      tf.keras.layers.Dense(num_nodes, activation='relu', input_shape=(33,)),
      tf.keras.layers.Dropout(dropout_prob),
      tf.keras.layers.Dense(num_nodes, activation='relu'),
      tf.keras.layers.Dropout(dropout_prob),
      tf.keras.layers.Dense(2, activation='sigmoid')
  ])

  nn_model.compile(optimizer=tf.keras.optimizers.Adam(lr), loss='tversky',
                  metrics=['accuracy'])
  history = nn_model.fit(
    X_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.2
  )

  return nn_model, history

least_val_loss = float('inf')
least_loss_model = None
epochs=100
for num_nodes in [33, 66, 99]:
  for dropout_prob in[0, 0.2]:
    for lr in [0.01, 0.005, 0.001]:
      for batch_size in [32, 64, 128]:
        title_graph = f"{num_nodes} nodes, dropout {dropout_prob}, lr {lr}, batch size {batch_size}"
        model, history = train_model(X_train, y_train, num_nodes, dropout_prob, lr, batch_size, epochs)
        plot_history(history,title_graph,model)
        val_loss = model.evaluate(X_valid, y_valid)[0]
        if val_loss < least_val_loss:
          least_val_loss = val_loss
          least_loss_model = model































