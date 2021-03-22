import pandas as pd
import os
import datetime as dt
from finta import TA
from Portfolio import Buy_Portfolio, Sell_Portfolio, Combine_result, Plot
from scipy.signal import find_peaks
from pandas import Timestamp
import datetime

dbd = r'C:\Users\lucky\PycharmProjects\alice-order\Converted'


def get_data(sb):
    with open(os.path.join(dbd, sb), 'r') as file:
        m = file.read()
    df = pd.DataFrame(eval(m))
    data = df.ltp.resample('5Min').ohlc()
    return data


def get_today(df, date):
    return df[df.index.date == date]


def get_peaks(today):
    y1 = today.loc[:, 'High'].values
    # x = np.array([i for i in range(1, len(y1) + 1)])
    peaks1, _ = find_peaks(y1)

    y2 = today.loc[:, 'Low'].values * -1
    # x = np.array([i for i in range(1, len(y1) + 1)])
    peaks2, _ = find_peaks(y2)
    return y1, y2, peaks1, peaks2


# dbd = r'F:\Database\option-drice\2021- banknifty\January\January\TXT 02-11-20 to 28-01-21 [Expiry Day]'

for sym in os.listdir(dbd):
    # break
    sym = 'BANKNIFTY MAR 32000.0 PE.txt'
    df_5min = get_data(sym)
    df_5min.dropna(inplace=True)
    df_5min = df_5min.rename({'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close'}, axis=1)
    df_5min = df_5min[df_5min.index.month == df_5min.index[-1].month]

    dates = sorted(list(set(df_5min.index.date)))

    port2 = Sell_Portfolio(sym)

    for date in dates:
        # break
        today = get_today(df_5min, date)
        flag = 0
        for e in today.index:
            if e == today.index[0]:
                continue
            if flag == 0 and today.loc[e, 'Close'] < 15:
                break
            y1, y2, peaks1, peaks2 = get_peaks(today.loc[:e, ])
            if len(peaks1) == 0 or len(peaks2) == 0:
                continue

            if today.loc[e, 'Low'] < y2[peaks2[-1]] * -1 and flag == 0:
                port2.sell(y2[peaks2[-1]] * -1, e)
                flag = 1
            elif today.loc[e, 'High'] > y1[peaks1[-1]] and flag == 1:
                port2.square_off(y1[peaks1[-1]], e)
                flag = 0
            if flag == 1 and e.time() == today.index[-1].time():
                port2.square_off(today.loc[e, 'Open'], e)
    port2.analysis()

    # port2.trade_df['CumReturn'].plot()
port2.trade_df
