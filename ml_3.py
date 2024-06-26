
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
import random

csv_file_path = 'big_data/ml_v1/5min/'
TP = 0.008
SL = 0.02

df = pd.read_csv(f'{csv_file_path}1000SATSUSDT.csv')

train, valid, test = np.split(df.sample(frac=1), [int(0.6*len(df)), int(0.8*len(df))])



def print_trade(model):
  # df_test = df.iloc[31500:-1]
  df_test = df.iloc[30300:-1]
  # df_test = df.iloc[28980:-1]
  trade_mas = []
  scaler = StandardScaler()
  X = scaler.fit_transform(df_test[:-2])
  number_df_test = 0
  predskasanie_celka = []
  for row in X:
    y = model.predict(np.array([row[:-2]], dtype=float))
    predskasanie_celka.append(y)
    if y[0][0]!=1 and y[0][1]!=1:
      if y[0][0]<0.1:long = 1
      elif y[0][0]>=0.9: long = 0
      else: long = 0
      if y[0][1]<0.1:short = 1
      elif y[0][1]>=0.9: short = 0
      else: short = 0
      trade_mas.append([number_df_test,long,short])
    number_df_test+=1
  print(f'{len(df_test)} | {len(trade_mas)}')
  # print(trade_mas)
  # ниже торговля
  flag_trade = 0
  number_index_mass_trade = 0
  deposit = 100 # депозит
  plecho = 1 # плечо
  depos_mass = {}
  depos_mass_depo = []
  depos_mass_nuber = []
  long_result_plus = 0
  long_result_minus = 0
  short_result_plus = 0
  short_result_minus = 0
  long_trade = 0
  short_trade = 0

  number_trade = 0
  for index, row in df_test.iterrows():
    if flag_trade == 0:
      for res in trade_mas:
        # print(f'{index == (res[0]+31500)} | {index} | {res[0]+31500} |')
        if index == (res[0]+30300):
          if res[1] == 1 and res[2] == 1:
            # see_trade = 'long'
            # price_trade = row['open']
            # TP_price = price_trade*(1+TP) # тейк и стоп для лонга
            # SL_price = price_trade*(1-SL)
            # long_trade+=1
            # flag_trade = 1
            continue
          if res[1] == 1 and res[2] == 0:
            see_trade = 'long'
            price_trade = row['open']
            TP_price = price_trade*(1+TP) # тейк и стоп для лонга
            SL_price = price_trade*(1-SL)
            long_trade+=1
            flag_trade = 1
          elif res[1] == 0 and res[2] == 1:
            short_trade+=1
            see_trade = 'short'
            price_trade = row['open']
            TP_price = price_trade*(1-TP) # Тейк и стоп для шорта
            SL_price = price_trade*(1+SL)
            flag_trade = 1
          else: continue
    else:
      # print(f'Следим - {index}')
      if see_trade == 'long':
        if row['close']>TP_price or row['high']>TP_price:
            long_result_plus+=1 # Значит сработал тейк
            deposit = deposit + deposit*plecho*TP
            flag_trade = 0
            depos_mass_depo.append(deposit)
            depos_mass_nuber.append(number_trade)
            number_trade+=1
        elif row['close']<SL_price or row['low']<SL_price:
            long_result_minus+=1 # значит сработал стоп
            deposit = deposit - deposit*plecho*SL
            flag_trade = 0
            depos_mass_depo.append(deposit)
            depos_mass_nuber.append(number_trade)
            number_trade+=1
      else:
        if row['close']<TP_price or row['low']<TP_price:
            short_result_plus+=1 # Значит сработал тейк
            deposit = deposit + deposit*plecho*TP
            flag_trade = 0
            depos_mass_depo.append(deposit)
            depos_mass_nuber.append(number_trade)
            number_trade+=1
        elif row['close']>SL_price or row['high']>SL_price:
            short_result_minus+=1 # значит сработал стоп
            deposit = deposit - deposit*plecho*SL
            flag_trade = 0
            depos_mass_depo.append(deposit)
            depos_mass_nuber.append(number_trade)
            number_trade+=1
  depos_mass['deposit'] = depos_mass_depo
  depos_mass['number'] = depos_mass_nuber
  depos_mass['long_result_plus'] = long_result_plus
  depos_mass['long_result_minus'] = long_result_minus
  depos_mass['short_result_plus'] = short_result_plus
  depos_mass['short_result_minus'] = short_result_minus
  depos_mass['long_trade'] = long_trade
  depos_mass['short_trade'] = short_trade
  depos_mass['predskasanie_celka'] = predskasanie_celka
  print(f'Депозит = {deposit}')
  print(depos_mass)
  return(depos_mass)
          


# получаем в нампи разделенные x и y и массив целиком, передав датафрейм
def scale_dataset(dataframe):
  X = dataframe[dataframe.columns[:-2]].values
  y = dataframe[dataframe.columns[-2:]].values
  scaler = StandardScaler()
  X = scaler.fit_transform(X)
  # data = np.hstack((X, y))
  data = np.hstack((X, np.reshape(y, (-2, 2))))
  return data, X, y

def plot_history(history,title,model,i):
  data_trade = print_trade(model)

  fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10, 4))
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
  

  ax3.plot(data_trade['deposit'], label='Депозит')
  # ax3.plot(data_trade['number'], label='Номер сделки')
  ax3.set_xlabel('Номер сделки')
  ax3.set_ylabel('Депозит')
  ax3.grid(True)

  ax1.set_title(title)
  ax3.set_title(f'Л+ {data_trade['long_result_plus']}|Л- {data_trade['long_result_minus']}|Ш+ {data_trade['short_result_plus']}|Ш- {data_trade['short_result_minus']}|Лонгов {data_trade['long_trade']}|Шортов {data_trade['short_trade']}')
  # plt.figtext(0, 0, data_trade['predskasanie_celka'], fontsize=6)
  plt.savefig(f'graph/{i}.png')
  # plt.show()

train_data, X_train, y_train = scale_dataset(train)
valid_data, X_valid, y_valid = scale_dataset(valid)
test_data, X_test, y_test = scale_dataset(test)

def train_model(X_train, y_train, num_nodes, dropout_prob, lr, batch_size, epochs,activat_1,activat_2,activat_3,potery):
  nn_model = tf.keras.Sequential([
      tf.keras.layers.Dense(dropout_prob, activation=activat_1, input_shape=(19,)),
      tf.keras.layers.Dropout(0.2),
      tf.keras.layers.Dense(num_nodes, activation=activat_2),
      tf.keras.layers.Dropout(0.2),
      tf.keras.layers.Dense(2, activation=activat_3)
  ])

  nn_model.compile(optimizer=tf.keras.optimizers.Adam(lr), loss=potery,
                  metrics=['accuracy'])
  history = nn_model.fit(
    X_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.2
  )

  return nn_model, history

least_val_loss = float('inf')
least_loss_model = None
epochs=200
num_nodes = 15
dropout_prob = 20
lr = 0.001
batch_size = 64
activat_1 = 'linear'
activat_2 = 'gelu'
activat_3 = 'relu'
potery = 'msle'
title_graph = f"{num_nodes}|{dropout_prob}|{lr}|{batch_size}|{activat_1}\n|{activat_2}|{activat_3}|{potery}"
model, history = train_model(X_train, y_train, num_nodes, dropout_prob, lr, batch_size, epochs,activat_1,activat_2,activat_3,potery)
plot_history(history,title_graph,model,4)
val_loss = model.evaluate(X_valid, y_valid)[0]
if val_loss < least_val_loss:
  least_val_loss = val_loss
  least_loss_model = model



# least_val_loss = float('inf')
# least_loss_model = None
# epochs=100
# for i in range(200):
#   num_nodes = random.choice([2,5,10,15,20,30,50,100])
#   dropout_prob = random.choice([2,5,10,15,20,30,50,100])
#   lr = random.choice([0.01, 0.005, 0.001])
#   batch_size = random.choice([32, 64, 128])
#   activat_1 = random.choice(['elu','exponential','gelu','hard_sigmoid','hard_silu','hard_swish','leaky_relu','linear','log_softmax','mish','relu','selu','sigmoid','silu','softmax','softplus','softsign','swish','tanh'])
#   activat_2 = random.choice(['elu','exponential','gelu','hard_sigmoid','hard_silu','hard_swish','leaky_relu','linear','log_softmax','mish','relu','selu','sigmoid','silu','softmax','softplus','softsign','swish','tanh'])
#   activat_3 = random.choice(['elu','exponential','gelu','hard_sigmoid','hard_silu','hard_swish','leaky_relu','linear','log_softmax','mish','relu','selu','sigmoid','silu','softmax','softplus','softsign','swish','tanh'])
#   potery = random.choice(['binary_crossentropy','MAE','MAPE','MSE','MSLE','binary_focal_crossentropy','categorical_crossentropy','categorical_focal_crossentropy','cosine_similarity','dice','hinge','huber','kld','mae','mape','mse','msle','poisson','squared_hinge','tversky'])
#   title_graph = f"{num_nodes}|{dropout_prob}|{lr}|{batch_size}|{activat_1}\n|{activat_2}|{activat_3}|{potery}"
#   model, history = train_model(X_train, y_train, num_nodes, dropout_prob, lr, batch_size, epochs,activat_1,activat_2,activat_3,potery)
#   plot_history(history,title_graph,model,i)
#   val_loss = model.evaluate(X_valid, y_valid)[0]
#   if val_loss < least_val_loss:
#     least_val_loss = val_loss
#     least_loss_model = model

























