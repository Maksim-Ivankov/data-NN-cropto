import numpy as np
from sklearn.utils import shuffle
from sklearn.preprocessing import MinMaxScaler
import os
import pandas as pd
import time
from talib import abstract
import progressbar
import tensorflow as tf

csv_file_path = 'big_data/ml_v1/5min/'

train_labels = [] # обучающие метки
train_samples = [] # обучающие образцы



# coin = next(os.walk(f'{csv_file_path}/'))[2] # получаем все названия файлов в папке 0 - монеты
# for coin_name in coin:
#     coin_name = coin_name[:-4] # чистим названия от расширения .csv - оставляем только название монеты
df = pd.read_csv(f'{csv_file_path}1000SATSUSDT.csv')
# train, valid, test = np.split(df.sample(frac=1),[int(0.6*len(df)), int(0.8*len(df))])

x = df[df.columns[:-2]].values
y = df[df.columns[-2:]].values



input = tf.keras.Input(shape=(33,), name='input')
layer_1 = tf.keras.layers.Dense(33, activation='relu', name='hidden_layer_1')(input)
dropout = tf.keras.layers.Dropout(0.2, name='dropout')(layer_1)
layer_2 = tf.keras.layers.Dense(10, name='hidden_layer_2')(dropout)
layer_3 = tf.keras.layers.Dense(5, activation='relu', name='hidden_layer_3')(layer_2)
output = tf.keras.layers.Dense(2, name='output')(layer_3)

model_2 = tf.keras.Model(
    inputs=input,
    outputs=output,
)


# Скомпилируем
model_2.compile(
    optimizer='Adam',
    loss='mse',
    metrics=['mean_absolute_error']
)

# # Обучим
# model_2.fit(
#     x, # Набор входных данных
#     y, # Набор правильных ответов
#     validation_split=0.2, # Этот параметр автоматически выделит часть обучающего набора на валидационные данные. В данном случа 20%
#     epochs=1000, # Процесс обучения завершится после 10 эпох
#     batch_size = 64 # Набор данных будет разбит на пакеты (батчи) по 8 элементов набора в каждом. 
# )

# Если ошибка не уменьшается на протяжении указанного количества эпох, то процесс обучения прерывается и модель инициализируется весами с самым низким показателем параметра "monitor"
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss', # указывается параметр, по которому осуществляется ранняя остановка. Обычно это функция потреть на валидационном наборе (val_loss)
    patience=10, # количество эпох по истечении которых закончится обучение, если показатели не улучшатся
    mode='min', # указывает, в какую сторону должна быть улучшена ошибка
    restore_best_weights=True # если параметр установлен в true, то по окончании обучения модель будет инициализирована весами с самым низким показателем параметра "monitor"
)

# Сохраняет модель для дальнейшей загрузки
model_checkpoint = tf.keras.callbacks.ModelCheckpoint(
    filepath='models/1.keras', # путь к папке, где будет сохранена модель
    monitor='val_loss',
    save_best_only=True, # если параметр установлен в true, то сохраняется только лучшая модель
    mode='min'
)

# Сохраняет логи выполнения обучения, которые можно будет посмотреть в специальной среде TensorBoard
tensorboard = tf.keras.callbacks.TensorBoard(
    log_dir='log/', # путь к папке где будут сохранены логи
)

model_2.fit(
    x,
    y,
    validation_split=0.2,
    epochs=500,
    batch_size = 128,
    callbacks = [
        early_stopping,
        model_checkpoint,
        tensorboard
    ]
)


# %load_ext tensorboard
# %tensorboard --logdir "log"










