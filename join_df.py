# Скрипт объединения датафреймов из папок по дням в единый фрейм за все месяцы по каждой монете отдельно.
# В итоге в паепке будут лежать csv с названиями монет, в которых будут объедененные данные за все дни торговли

import os
import pandas as pd

path = 'big_data/5min/'

coin = next(os.walk(f'{path}0/'))[2] # получаем все названия файлов в папке 0 - монеты
for i in range(len(coin)):
    coin[i] = coin[i][:-4] # чистим названия от расширения .csv - оставляем только название монеты
coin.remove('GLMUSDT') # Чистим от монет, которые потерялись в процессе
coin.remove('OMUSDT')
coin.remove('VANRYUSDT')
coin.remove('ANTUSDT')
coin.remove('XMRUSDT')


arr = next(os.walk(f'{path}'))[1] # получаем все папки по пути
arr = [eval(i) for i in arr] # преобразуем названия папок в числа
for folder in sorted(arr): # итерируемся по отсортированному массиву с названием папок от 0 до N
    print(folder)
    for coin_name in coin:
        pd.read_csv(f'{path}{folder}/{coin_name}.csv')
        




















































































