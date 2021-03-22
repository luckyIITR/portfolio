import pandas as pd
import os
import datetime as dt


def get_data():
    dbd = r'F:\Database\option-drice\2019-banknifty\June\June\TXT 01-05-19 to 27-06-19 (Expiry Day)'
    loc = os.path.join(dbd, "BANKNIFTY30000PE.txt")

    data = pd.read_csv(loc, sep=",", header=0,
                       names=['Symbol', 'date', 'time', 'Open', 'High', 'Low', 'Close', 'x'])
    data = data[['date', 'time', 'Open', 'Low', 'High', 'Close']].copy()
    data['date'] = pd.to_datetime(data['date'], format='%Y/%m/%d')
    data['time'] = pd.to_datetime(data['time'], format='%H:%M')
    data['Time'] = [dt.datetime.combine(data.loc[e, 'date'], data.loc[e, 'time'].time()) for e in data.index]
    data = data[['Time', 'Open', 'Low', 'High', 'Close']].copy()
    data.set_index('Time', inplace=True, drop=True)
    return data
