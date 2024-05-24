# Скрипт объединения датафреймов из папок по дням в единый фрейм за все месяцы по каждой монете отдельно.
# В итоге в паепке будут лежать csv с названиями монет, в которых будут объедененные данные за все дни торговли

import os
import pandas as pd
import time
from talib import abstract
import progressbar

path = 'big_data/5min/'
csv_file_path = 'big_data/ml_v1/5min/'

# # ШАГ 1
# # получаем название коинов и чистим от багованых
# print('Шаг 1. Получаем название коинов и чистим от багованых. Приступаем')
# coin = next(os.walk(f'{path}0/'))[2] # получаем все названия файлов в папке 0 - монеты
# for i in range(len(coin)):
#     coin[i] = coin[i][:-4] # чистим названия от расширения .csv - оставляем только название монеты
# coin.remove('GLMUSDT') # Чистим от монет, которые потерялись в процессе
# coin.remove('OMUSDT')
# coin.remove('VANRYUSDT')
# coin.remove('ANTUSDT')
# coin.remove('XMRUSDT')
# print('Шаг 1. Выполнено')

# # ШАГ 2
# # цикл ниже объединяет датафреймы с одинаковыми названиями файлов в один
# print('Шаг 2. Объединяем датафреймы с одинаковыми названиями файлов в один. Приступаем')
# arr = next(os.walk(f'{path}'))[1] # получаем все папки по пути
# arr = [eval(i) for i in arr] # преобразуем названия папок в числа
# bar = progressbar.ProgressBar(maxval=len(arr)).start() # прогресс бар в консоли
# for folder in sorted(arr): # итерируемся по отсортированному массиву с названием папок от 0 до N
#     bar.update(folder)
#     if folder !=0:
#         for coin_name in coin:
#             df = pd.read_csv(f'{path}{folder}/{coin_name}.csv')
#             df_res = pd.read_csv(f'{csv_file_path}{coin_name}.csv')
#             df_res = df_res._append(df.iloc[1:len(df)])
#             df_res.to_csv(f'{csv_file_path}{coin_name}.csv', index=False)
# print('Шаг 2. Выполнено')
            
# # # ШАГ 3
# # # цикл ниже удаляет ненужные столбцы
# print('Шаг 3. Удаляем ненужные столбцы. Приступаем')
# coin = next(os.walk(f'{csv_file_path}/'))[2] # получаем все названия файлов в папке 0 - монеты
# bar = progressbar.ProgressBar(maxval=len(coin)).start() # прогресс бар в консоли
# for i in range(len(coin)):
#     coin[i] = coin[i][:-4] # чистим названия от расширения .csv - оставляем только название монеты
#     df = pd.read_csv(f'{csv_file_path}{coin[i]}.csv')
#     df_new = df.drop(['close_time','Unnamed: 0','open_time'], axis=1)
#     df_new.to_csv(f'{csv_file_path}{coin[i]}.csv', index=False)
#     bar.update(i)
# print('Шаг 3. Выполнено')


# # ШАГ 4
# # Добавляем значения прижатия к коридору
# print('Шаг 4. Добавляем значения прижатия к коридору. Приступаем')
# hall_mass = []
# coin = next(os.walk(f'{csv_file_path}/'))[2] # получаем все названия файлов в папке 0 - монеты
# bar = progressbar.ProgressBar(maxval=len(coin)).start() # прогресс бар в консоли
# for coin_name in coin:
#     coin_name = coin_name[:-4] # чистим названия от расширения .csv - оставляем только название монеты
#     df = pd.read_csv(f'{csv_file_path}{coin_name}.csv')
#     bar.update(coin_name)
#     a = abstract.BBANDS(df, timeperiod=5, nbdevup=2.0, nbdevdn=2.0, matype=0)
#     hall_mass[:] = []
#     for index, row in df.iterrows():
#         if index >4:
#             if (a['upperband'].iloc[index-1]-a['lowerband'].iloc[index-1]) == 0: # иногда индикатор показывает одинаковый верх и низ - ошибка, обнуляем ее занчение, чтобы потом вычистить
#                 hall_mass.append(0)
#             else:
#                 canal_procent = (df['close'].iloc[index-1]-a['lowerband'].iloc[index-1])/(a['upperband'].iloc[index-1]-a['lowerband'].iloc[index-1])
#                 hall_mass.append(round(canal_procent,5))
#         else:
#             hall_mass.append(0)
#     df['hall'] = hall_mass
#     df.to_csv(f'{csv_file_path}{coin_name}.csv', index=False)  
# print('Шаг 4. Выполнено')  

# # ШАГ 5
# # Добавляем индикаторы
# print('Шаг 5. Добавляем индикаторы. Приступаем')
# DEMA_mas  = []
# EMA_mas  = []
# HT_TRENDLINE_mas  = []
# KAMA_mas  = []
# MA_mas  = []
# MIDPOINT_mas  = []
# MIDPRICE_mas  = []
# SMA_mas  = []
# TEMA_mas  = []
# TRIMA_mas  = []
# WMA_mas  = []
# ADX_mas  = []
# ADXR_mas  = []
# APO_mas  = []
# AROON_mas_down = []
# AROON_mas_up = []
# BOP_mas  = []
# CCI_mas  = []
# CMO_mas  = []
# DX_mas  = []
# MACD_mas  = []
# MFI_mas  = []
# MINUS_DI_mas  = []
# MINUS_DM_mas  = []
# MOM_mas  = []
# PLUS_DI_mas  = []
# ROC_mas  = []
# CDLEVENINGSTAR_mas  = []
# coin = next(os.walk(f'{csv_file_path}/'))[2] # получаем все названия файлов в папке 0 - монеты
# count_bar = 0
# for coin_name in coin:
#     coin_name = coin_name[:-4] # чистим названия от расширения .csv - оставляем только название монеты
#     df = pd.read_csv(f'{csv_file_path}{coin_name}.csv')
#     df.rename(columns={'VOLUME':'volume'},inplace=True)
#     bar = progressbar.ProgressBar(maxval=len(df)).start() # прогресс бар в консоли
#     count_bar+=1
#     DEMA_mas[:] = []
#     EMA_mas[:] = []
#     HT_TRENDLINE_mas[:] = []
#     KAMA_mas[:] = []
#     MA_mas[:] = []
#     MIDPOINT_mas[:] = []
#     MIDPRICE_mas[:] = []
#     SMA_mas[:] = []
#     TEMA_mas[:] = []
#     TRIMA_mas[:] = []
#     WMA_mas[:] = []
#     ADX_mas[:] = []
#     ADXR_mas[:] = []
#     APO_mas[:] = []
#     AROON_mas_down[:] = []
#     AROON_mas_up[:] = []
#     BOP_mas[:] = []
#     CCI_mas[:] = []
#     CMO_mas[:] = []
#     DX_mas[:] = []
#     MACD_mas[:] = []
#     MFI_mas[:] = []
#     MINUS_DI_mas[:] = []
#     MINUS_DM_mas[:] = []
#     MOM_mas[:] = []
#     PLUS_DI_mas[:] = []
#     ROC_mas[:] = []
#     CDLEVENINGSTAR_mas[:] = []
#     DEMA = abstract.DEMA(df, timeperiod=30)
#     EMA = abstract.EMA(df, timeperiod=30)
#     HT_TRENDLINE = abstract.HT_TRENDLINE(df)
#     KAMA = abstract.KAMA(df, timeperiod=30)
#     MA = abstract.MA(df, timeperiod=30, matype=0)
#     MIDPOINT = abstract.MIDPOINT(df, timeperiod=14)
#     MIDPRICE = abstract.MIDPRICE(df, timeperiod=14)
#     SMA = abstract.SMA(df, timeperiod=30)
#     TEMA = abstract.TEMA(df, timeperiod=30)
#     TRIMA = abstract.TRIMA(df, timeperiod=30)
#     WMA = abstract.WMA(df, timeperiod=30)
#     ADX = abstract.ADX(df,14)
#     ADXR = abstract.ADXR(df,14)
#     APO = abstract.APO(df,14)
#     AROON = abstract.AROON(df,14)
#     BOP = abstract.BOP(df,14)
#     CCI = abstract.CCI(df,14)
#     CMO = abstract.CMO(df,14)
#     DX = abstract.DX(df,14)
#     MACD = abstract.MACD(df,12, 26, 9)
#     MFI = abstract.MFI(df,14)
#     MINUS_DI = abstract.MINUS_DI(df,14)
#     MINUS_DM = abstract.MINUS_DM(df,14)
#     MOM = abstract.MOM(df,14)
#     PLUS_DI = abstract.PLUS_DI(df,14)
#     ROC = abstract.ROC(df, 14)
#     CDLEVENINGSTAR = abstract.CDLEVENINGSTAR(df)
#     for index, row in df.iterrows():
#         bar.update(index)
#         if index >30:
#             DEMA_mas.append(round(DEMA[index-1],8))
#             EMA_mas.append(round(EMA[index-1],8))
#             HT_TRENDLINE_mas.append(round(HT_TRENDLINE[index-1],8))
#             KAMA_mas.append(round(KAMA[index-1],8))
#             MA_mas.append(round(MA[index-1],8))
#             MIDPOINT_mas.append(round(MIDPOINT[index-1],8))
#             MIDPRICE_mas.append(round(MIDPRICE[index-1],8))
#             SMA_mas.append(round(SMA[index-1],8))
#             TEMA_mas.append(round(TEMA[index-1],8))
#             TRIMA_mas.append(round(TRIMA[index-1],8))
#             WMA_mas.append(round(WMA[index-1],8))
#             ADX_mas.append(round(ADX[index-1],8))
#             ADXR_mas.append(round(ADXR[index-1],8))
#             APO_mas.append(round(APO[index-1],8))
#             AROON_mas_down.append(round(AROON['aroondown'][index-1],8))
#             AROON_mas_up.append(round(AROON['aroonup'][index-1],8))
#             BOP_mas.append(round(BOP[index-1],8))
#             CCI_mas.append(round(CCI[index-1],8))
#             CMO_mas.append(round(CMO[index-1],8))
#             DX_mas.append(round(DX[index-1],8))
#             MACD_mas.append(round(MACD['macdsignal'][index-1],8))
#             MFI_mas.append(round(MFI[index-1],8))
#             MINUS_DI_mas.append(round(MINUS_DI[index-1],8))
#             MINUS_DM_mas.append(round(MINUS_DM[index-1],8))
#             MOM_mas.append(round(MOM[index-1],8))
#             PLUS_DI_mas.append(round(PLUS_DI[index-1],8))
#             ROC_mas.append(round(ROC[index-1],8))
#             CDLEVENINGSTAR_mas.append(round(CDLEVENINGSTAR[index-1],8))
#         else:
#             DEMA_mas.append(0)
#             EMA_mas.append(0)
#             HT_TRENDLINE_mas.append(0)
#             KAMA_mas.append(0)
#             MA_mas.append(0)
#             MIDPOINT_mas.append(0)
#             MIDPRICE_mas.append(0)
#             SMA_mas.append(0)
#             TEMA_mas.append(0)
#             TRIMA_mas.append(0)
#             WMA_mas.append(0)
#             ADX_mas.append(0)
#             ADXR_mas.append(0)
#             APO_mas.append(0)
#             AROON_mas_down.append(0)
#             AROON_mas_up.append(0)
#             BOP_mas.append(0)
#             CCI_mas.append(0)
#             CMO_mas.append(0)
#             DX_mas.append(0)
#             MACD_mas.append(0)
#             MFI_mas.append(0)
#             MINUS_DI_mas.append(0)
#             MINUS_DM_mas.append(0)
#             MOM_mas.append(0)
#             PLUS_DI_mas.append(0)
#             ROC_mas.append(0)
#             CDLEVENINGSTAR_mas.append(0)
#     df['DEMA'] = DEMA_mas
#     df['EMA'] = EMA_mas
#     df['HT_TRENDLINE'] = HT_TRENDLINE_mas
#     df['KAMA'] = KAMA_mas
#     df['MA'] = MA_mas
#     df['MIDPOINT'] = MIDPOINT_mas
#     df['MIDPRICE'] = MIDPRICE_mas
#     df['SMA'] = SMA_mas
#     df['TEMA'] = TEMA_mas
#     df['TRIMA'] = TRIMA_mas
#     df['WMA'] = WMA_mas
#     df['ADX'] = ADX_mas
#     df['ADXR'] = ADXR_mas
#     df['APO'] = APO_mas
#     df['AROON_down'] = AROON_mas_down
#     df['AROON_up'] = AROON_mas_up
#     df['BOP'] = BOP_mas
#     df['CCI'] = CCI_mas
#     df['CMO'] = CMO_mas
#     df['DX'] = DX_mas
#     df['MACD'] = MACD_mas
#     df['MFI'] = MFI_mas
#     df['MINUS_DI'] = MINUS_DI_mas
#     df['MINUS_DM'] = MINUS_DM_mas
#     df['MOM'] = MOM_mas
#     df['PLUS_DI'] = PLUS_DI_mas
#     df['ROC'] = ROC_mas
#     df['CDLEVENINGSTAR'] = CDLEVENINGSTAR_mas
#     df.to_csv(f'{csv_file_path}{coin_name}.csv', index=False)  
#     print(f'{count_bar}/{len(coin)} | {coin_name} добавлен')
# print('Шаг 5. Выполнено')  

# ШАГ 6
# Добавляем значения прижатия к коридору
print('Шаг 6. Чистим от первых 31 пустых значений. Приступаем')
hall_mass = []
coin = next(os.walk(f'{csv_file_path}/'))[2] # получаем все названия файлов в папке 0 - монеты
bar = progressbar.ProgressBar(maxval=len(coin)).start() # прогресс бар в консоли
count_step_6 = 0
for coin_name in coin:
    coin_name = coin_name[:-4] # чистим названия от расширения .csv - оставляем только название монеты
    df = pd.read_csv(f'{csv_file_path}{coin_name}.csv')
    bar.update(count_step_6)
    count_step_6+=1
    df = df.drop (index=[ 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31 ]) 
    df.to_csv(f'{csv_file_path}{coin_name}.csv', index=False) 
print('Шаг 6. Сделано') 






























































