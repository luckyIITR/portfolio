#%%
from Portfolio import Buy_Portfolio, Sell_Portfolio, Combine_result, Plot
import datetime as dt
from datetime import timedelta
import time
import pandas as pd

port = Buy_Portfolio('SBIN')
# port.square_off(112, dt.datetime.now())
port.buy(110, dt.datetime.now())
port.square_off(112, dt.datetime.now())

port.buy(109, dt.datetime.now())
port.square_off(111, dt.datetime.now())

port.buy(113, dt.datetime.now() + timedelta(days=1))
port.square_off(114, dt.datetime.now() + timedelta(days=1))

port.buy(113, dt.datetime.now() + timedelta(days=1))
port.square_off(118, dt.datetime.now() + timedelta(days=1))
port.analysis()
# print(port.order_df)
# print(port.trade_df)
print(port.day_wise)
df1 = port.trade_df
# print(df)
#


port2 = Sell_Portfolio('SBIN')
# port.square_off(112, dt.datetime.now())
port2.sell(111, dt.datetime.now())
#
port2.square_off(115, dt.datetime.now())
port2.sell(118, dt.datetime.now() + timedelta(days=1))
port2.square_off(114, dt.datetime.now() + timedelta(days=1))

port2.analysis()
# print(port2.order_df)
# print(port2.trade_df)
print(port2.day_wise)
gf1 = port2.trade_df

# df1 = df1[['%change', 'CumReturn']]
# gf1 = gf1[['%change', 'CumReturn']]
print(df1)
# print("###########")
# print(gf1)

comb = Combine_result(df1, gf1, 'SBIN')
comb.combine()
# print(comb.final)
# print(comb.day_wise)

ploting = Plot(port.trade_df['CumReturn'], port2.trade_df['CumReturn'], comb.final['CumReturn'],
               comb.day_wise['CumReturn'], 'SBIN')
ploting.plot()

# %%
