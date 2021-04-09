import os
import pandas as pd
import datetime as dt
import mplfinance as mpf
import yfinance as yf
from Portfolio import Buy_Portfolio, Sell_Portfolio, Combine_result, Plot
from scipy.signal import find_peaks


def get_peaks(today):
    y1 = today.loc[:, 'High'].values
    # x = np.array([i for i in range(1, len(y1) + 1)])
    peaks1, _ = find_peaks(y1)

    y2 = today.loc[:, 'Low'].values * -1
    # x = np.array([i for i in range(1, len(y1) + 1)])
    peaks2, _ = find_peaks(y2)
    return y1, y2, peaks1, peaks2

def get_dir():
    cwd = r"F:\Database\option-drice\2019-banknifty"
    all = os.listdir(cwd)
    fold = []
    for element in all:
        if element[-4:] != ".zip":
            fold.append(element)
    for i in range(len(fold)):
        x = os.path.join(cwd, fold[i])
        fold[i] = os.path.join(x, fold[i])
    for i in range(len(fold)):
        for element in os.listdir(fold[i]):
            if element[-4:] != ".zip":
                fold[i] = os.path.join(fold[i], element)
    return fold


def get_data(dbd, contract):
    loc = os.path.join(dbd, contract)

    data = pd.read_csv(loc, sep=",", header=0,
                       names=['Symbol', 'date', 'time', 'Open', 'High', 'Low', 'Close', 'x'])
    data = data[['date', 'time', 'Open', 'Low', 'High', 'Close']].copy()
    data['date'] = pd.to_datetime(data['date'], format='%Y/%m/%d')
    data['time'] = pd.to_datetime(data['time'], format='%H:%M')
    data['Time'] = [dt.datetime.combine(data.loc[e, 'date'], data.loc[e, 'time'].time()) for e in data.index]
    data = data[['Time', 'Open', 'Low', 'High', 'Close']].copy()
    data.set_index('Time', inplace=True, drop=True)
    ohlc_dict = {'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last'}
    data = data.resample('5T').agg({'Open': 'first',
                                    'High': 'max',
                                    'Low': 'min',
                                    'Close': 'last'})
    data = data[data.index.month == data.index.date[-1].month]
    data.dropna(inplace=True)
    return data


def extract_dates(dbd):
    contract = os.listdir(dbd)[0]
    loc = os.path.join(dbd, contract)

    data = pd.read_csv(loc, sep=",", header=0,
                       names=['Symbol', 'date', 'time', 'Open', 'High', 'Low', 'Close', 'x'])
    data = data[['date', 'time', 'Open', 'Low', 'High', 'Close']].copy()
    data['date'] = pd.to_datetime(data['date'], format='%Y/%m/%d')
    data['time'] = pd.to_datetime(data['time'], format='%H:%M')
    data['Time'] = [dt.datetime.combine(data.loc[e, 'date'], data.loc[e, 'time'].time()) for e in data.index]
    data = data[['Time', 'Open', 'Low', 'High', 'Close']].copy()
    data.set_index('Time', inplace=True, drop=True)
    ohlc_dict = {'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last'}
    data = data.resample('5T').agg({'Open': 'first',
                                    'High': 'max',
                                    'Low': 'min',
                                    'Close': 'last'})
    data = data[data.index.month == data.index.date[-1].month]
    data.dropna(inplace=True)
    return sorted(list(set(data.index.date)))


def banknify(date):
    df = yf.download('^NSEBANK', start=date, end=date + dt.timedelta(days=1))
    return df['Open'].iloc[-1]


def check(x):
    global bnf_ltp
    if bnf_ltp-600 < int(x[9:14]) < bnf_ltp-400 and x[14:16] == "PE":
        return True
    elif bnf_ltp + 600 >int(x[9:14]) > bnf_ltp+400 and x[14:16] == 'CE':
        return True
    return False


def get_today(df, date):
    return df[df.index.date == date]

# mpf.plot(data)

dirs = get_dir()

for dir in dirs:
    # break
    # extracted dates inside a month
    dates = extract_dates(dir)
    for date in dates:
        # break
        bnf_ltp = banknify(date)
        bnf_ltp = round(bnf_ltp/100)*100
        contracts = os.listdir(dir)
        contracts = list(filter(check, contracts))
        port2 = Sell_Portfolio("texrt")
        for contract in contracts:
            # break
            df_5min = get_data(dir, contract)
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