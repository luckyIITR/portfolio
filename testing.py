from Portfolio import Buy_Portfolio, Sell_Portfolio, Combine_result, Plot
import yfinance as yf
from finta import TA
import pandas as pd
from datetime import timedelta
import datetime as dt


def get_data(symbol, tp):
    daily = yf.download(tickers=symbol, interval="5m", period=f"{str(tp)}d")
    daily.index = daily.index.tz_localize(None)
    daily.drop(["Adj Close", 'Volume'], axis=1, inplace=True)
    return daily


def get_today(df, date):
    return df[df.index.date == date]


data = get_data('HDFCBANK.NS', 60)
data['ATR'] = TA.ATR(data)
data = pd.concat([data, TA.MACD(data)], axis=1)
dates = sorted(list(set(data.index.date)))[1:]

port1 = Buy_Portfolio('HDFCBANK')
bp = -1
atr = -1
for date in dates:
    today = get_today(data, date)
    flag = 0
    for e in today.index:
        if e.time() < dt.datetime(2020, 2, 2, 9, 30).time():
            continue
        if e.time() > dt.datetime(2020, 2, 2, 14, 45).time() and flag == 0:
            continue
        if today.loc[e, 'MACD'] > today.loc[e, 'SIGNAL'] and today.loc[e - timedelta(minutes=5), 'MACD'] < today.loc[
            e - timedelta(minutes=5), 'SIGNAL'] and flag == 0 and today.loc[e, 'MACD'] < -.5 and today.loc[
            e, 'SIGNAL'] < -.5:
            port1.buy(today.loc[e, 'Close'], e)
            bp = today.loc[e, 'Close']
            atr = today.loc[e, 'ATR']
            flag = 1
            continue
        if today.loc[e, 'Low'] < bp - 4 * atr and flag == 1:
            port1.square_off(bp - 3 * atr, e)
            flag = 0

        if today.loc[e, 'High'] > bp + 7 * atr and flag == 1:
            port1.square_off(bp + 3 * atr, e)
            flag = 0

        if flag == 1 and e.time() == dt.datetime(2020, 2, 2, 15, 25).time():
            port1.square_off(today.loc[e, 'Open'], e)
            flag = 0
port1.analysis()
print(port1.trade_df)
print(port1.day_wise)
