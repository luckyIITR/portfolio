import pandas as pd


class Buy_Portfolio:

    def __init__(self, symbol):
        self.symbol = symbol
        self.order_df = pd.DataFrame({"Time": [],
                                      "Price": [],
                                      "Status": []})
        self.trade_df = pd.DataFrame()
        self.day_wise = pd.DataFrame()

    def buy(self, bp, time):
        if len(self.order_df) == 0 or self.order_df.iloc[-1]['Status'] != "BUY":
            self.order_df = self.order_df.append(pd.DataFrame({'Time': [time],
                                                               "Price": [bp],
                                                               'Status': ['BUY']}), ignore_index=True)
        else:
            print("Already Opened Buying Position")

    def square_off(self, sp, time):
        if len(self.order_df) != 0:
            if self.order_df.iloc[-1]['Status'] == "BUY":
                self.order_df = self.order_df.append(pd.DataFrame({'Time': [time],
                                                                   "Price": [sp],
                                                                   'Status': ['Square_Off']}), ignore_index=True)
        else:
            print('No Position opened')

    def check_order_book(self):
        if len(self.order_df) == 0:
            print('Order Book Empty in Check_order_book Function')
            return None
        order_book = self.order_df.copy()
        order_book.set_index('Time', inplace=True, drop=True)
        flag = 1
        dates = sorted(list(set(order_book.index.date)))
        for date in dates:
            if len(order_book[order_book.index.date == date]) % 2 == 0:
                continue
            else:
                flag = 0
                print(date)
                exit("Code terminated Reason: position open")

    def analysis(self):
        if len(self.order_df) == 0:
            print('Order Book Empty in Analysis Function')
            return None
        df = self.order_df.copy()
        df['SP'] = df['Price'].shift(-1)
        self.trade_df = df[df['Status'] == 'BUY'].copy()
        self.trade_df.rename(columns={'Price': 'BP'}, inplace=True)
        self.trade_df = self.trade_df[['Time', 'BP', 'SP']]
        self.trade_df.set_index('Time', inplace=True, drop=True)
        self.trade_df['%change'] = (self.trade_df['SP'] - self.trade_df['BP']) / self.trade_df['BP'] * 100
        self.trade_df['CumReturn'] = ((self.trade_df['%change'] / 100 + 1).cumprod() - 1) * 100
        self.check_order_book()
        self.day_wise_fun()
        self.result()
        # print(self.trade_df)

    def result(self):
        gains = self.trade_df['%change'][self.trade_df['%change'] >= 0].sum()
        ng_count = len(self.trade_df[self.trade_df['%change'] >= 0])
        losses = self.trade_df['%change'][self.trade_df['%change'] < 0].sum()
        nl_count = len(self.trade_df[self.trade_df['%change'] < 0])
        if ng_count > 0:
            avgGain = gains / ng_count
            maxR = self.trade_df['%change'].max()
        else:
            avgGain = 0
            maxR = 'undefined'
        if nl_count > 0:
            avgLoss = losses / nl_count
            maxL = self.trade_df['%change'].min()
            ratio = str(-avgGain / avgLoss)
        else:
            avgLoss = 0
            maxL = 'undefined'
            ratio = "inf"

        if ng_count > 0 or nl_count > 0:
            battingAvg = ng_count / (ng_count + nl_count)
        else:
            battingAvg = 0

        totalR = round(self.trade_df['CumReturn'].iloc[-1], 2)
        print()
        print("###############################################################")
        print("Results for " + self.symbol)
        print("Batting Avg: " + str(battingAvg))
        print("Gain/loss ratio: " + ratio)
        print("Average Gain: " + str(round(avgGain, 2)))
        print("Average Loss: " + str(round(avgLoss, 2)))
        print("Max Return: " + str(round(maxR, 2)))
        print("Max Loss: " + str(maxL))
        print("Total return over " + str(ng_count + nl_count) + " trades: " + str(totalR) + "%")
        print("###############################################################")
        print()

    def day_wise_fun(self):
        df = self.trade_df.copy()
        df = df[['BP', 'SP', '%change']]
        dates = sorted(list(set(df.index.date)))
        for date in dates:
            df1 = df[df.index.date == date].copy()
            df1['cumpro'] = ((df1['%change'] / 100 + 1).cumprod() - 1) * 100
            self.day_wise = self.day_wise.append(pd.DataFrame({'Date': [date],
                                                               'Day_return': [df1['cumpro'].iloc[-1]]}))
        self.day_wise.set_index('Date', inplace=True, drop=True)
        self.day_wise['CumReturn'] = ((self.day_wise['Day_return'] / 100 + 1).cumprod() - 1) * 100


class Sell_Portfolio:

    def __init__(self, symbol):
        self.symbol = symbol
        self.order_df = pd.DataFrame({"Time": [],
                                      "Price": [],
                                      "Status": []})
        self.trade_df = pd.DataFrame()
        self.day_wise = pd.DataFrame()

    def sell(self, sp, time):
        if len(self.order_df) == 0 or self.order_df.iloc[-1]['Status'] != "SELL":
            self.order_df = self.order_df.append(pd.DataFrame({'Time': [time],
                                                               "Price": [sp],
                                                               'Status': ['SELL']}), ignore_index=True)
        else:
            print("Already Opened Buying Position")

    def square_off(self, bp, time):
        if len(self.order_df) != 0:
            if self.order_df.iloc[-1]['Status'] == "SELL":
                self.order_df = self.order_df.append(pd.DataFrame({'Time': [time],
                                                                   "Price": [bp],
                                                                   'Status': ['Square_Off']}), ignore_index=True)
        else:
            print('No Position opened')

    def check_order_book(self):
        if len(self.order_df) == 0:
            print('Order Book Empty in Check_order_book Function')
            return None
        order_book = self.order_df.copy()
        order_book.set_index('Time', inplace=True, drop=True)
        flag = 1
        dates = sorted(list(set(order_book.index.date)))
        for date in dates:
            if len(order_book[order_book.index.date == date]) % 2 == 0:
                continue
            else:
                flag = 0
                print(date)
                exit("Code terminated Reason: position open")

    def analysis(self):
        if len(self.order_df) == 0:
            print('Order Book Empty in Analysis Function')
            return None
        df = self.order_df.copy()
        df['BP'] = df['Price'].shift(-1)
        self.trade_df = df[df['Status'] == 'SELL'].copy()
        self.trade_df.rename(columns={'Price': 'SP'}, inplace=True)
        self.trade_df = self.trade_df[['Time', 'SP', 'BP']]
        self.trade_df.set_index('Time', inplace=True, drop=True)
        self.trade_df['change'] = self.trade_df['SP'] - self.trade_df['BP']
        self.trade_df['CumReturn'] = self.trade_df['change'].cumsum()
        self.check_order_book()
        self.day_wise_fun()
        self.result()
        # print(self.trade_df)

    def result(self):
        gains = self.trade_df['change'][self.trade_df['change'] >= 0].sum()
        ng_count = len(self.trade_df[self.trade_df['change'] >= 0])
        losses = self.trade_df['change'][self.trade_df['change'] < 0].sum()
        nl_count = len(self.trade_df[self.trade_df['change'] < 0])
        if ng_count > 0:
            avgGain = gains / ng_count
            maxR = self.trade_df['change'].max()
            maxR = str(round(maxR, 2))
        else:
            avgGain = 0
            maxR = 'undefined'
        if nl_count > 0:
            avgLoss = losses / nl_count
            maxL = self.trade_df['change'].min()
            ratio = str(-avgGain / avgLoss)
        else:
            avgLoss = 0
            maxL = 'undefined'
            ratio = "inf"

        if ng_count > 0 or nl_count > 0:
            battingAvg = ng_count / (ng_count + nl_count)
        else:
            battingAvg = 0

        totalR = round(self.trade_df['CumReturn'].iloc[-1], 2)
        print()
        print("###############################################################")
        print("Results for " + self.symbol)
        print("Batting Avg: " + str(battingAvg))
        print("Gain/loss ratio: " + ratio)
        print("Average Gain: " + str(round(avgGain, 2)))
        print("Average Loss: " + str(round(avgLoss, 2)))
        print("Max Return: " + maxR)
        print("Max Loss: " + str(maxL))
        print("Total return over " + str(ng_count + nl_count) + " trades: " + str(totalR))
        print("###############################################################")
        print()

    def day_wise_fun(self):
        df = self.trade_df.copy()
        df = df[['BP', 'SP', 'change']]
        dates = sorted(list(set(df.index.date)))
        for date in dates:
            df1 = df[df.index.date == date].copy()
            df1['cumpro'] = df1['change'].cumsum()
            self.day_wise = self.day_wise.append(pd.DataFrame({'Date': [date],
                                                               'Day_return': [df1['cumpro'].iloc[-1]]}))
        self.day_wise.set_index('Date', inplace=True, drop=True)
        self.day_wise['CumReturn'] = self.day_wise['Day_return'].cumsum()


class Combine_result:
    def __init__(self, df1, df2,symbol):
        self.df1 = df1
        self.df2 = df2
        self.final = pd.DataFrame()
        self.symbol = symbol
        self.day_wise = pd.DataFrame()

    def combine(self):
        if len(self.df1) > 0 and len(self.df2) > 0:
            self.final = pd.concat([self.df1, self.df2], axis=0)
            self.final = self.final[['BP', 'SP']].copy()
            self.final.sort_index(axis=0, inplace=True)
        elif len(self.df1) > 0 and len(self.df2) == 0:
            self.final = self.df1
            self.final = self.final[['BP', 'SP']].copy()
            self.final.sort_index(axis=0, inplace=True)
        elif len(self.df1) == 0 and len(self.df2) > 0:
            self.final = self.df2
            self.final = self.final[['BP', 'SP']].copy()
            self.final.sort_index(axis=0, inplace=True)
        self.final['%change'] = (self.final['SP'] - self.final['BP']) / self.final['BP'] * 100
        self.final['CumReturn'] = ((self.final['%change'] / 100 + 1).cumprod() - 1) * 100
        self.result()
        self.day_wise_fun()
        # print(self.final)

    def result(self):
        gains = self.final['%change'][self.final['%change'] >= 0].sum()
        ng_count = len(self.final[self.final['%change'] >= 0])
        losses = self.final['%change'][self.final['%change'] < 0].sum()
        nl_count = len(self.final[self.final['%change'] < 0])
        if ng_count > 0:
            avgGain = gains / ng_count
            maxR = self.final['%change'].max()
        else:
            avgGain = 0
            maxR = 'undefined'
        if nl_count > 0:
            avgLoss = losses / nl_count
            maxL = self.final['%change'].min()
            ratio = str(-avgGain / avgLoss)
        else:
            avgLoss = 0
            maxL = 'undefined'
            ratio = "inf"

        if ng_count > 0 or nl_count > 0:
            battingAvg = ng_count / (ng_count + nl_count)
        else:
            battingAvg = 0

        totalR = round(self.final['CumReturn'].iloc[-1], 2)
        print()
        print("###############################################################")
        print("Results for " + self.symbol)
        print("Batting Avg: " + str(battingAvg))
        print("Gain/loss ratio: " + ratio)
        print("Average Gain: " + str(round(avgGain, 2)))
        print("Average Loss: " + str(round(avgLoss, 2)))
        print("Max Return: " + str(round(maxR, 2)))
        print("Max Loss: " + str(maxL))
        print("Total return over " + str(ng_count + nl_count) + " trades: " + str(totalR) + "%")
        print("###############################################################")
        print()

    def day_wise_fun(self):
        df = self.final.copy()
        df = df[['BP', 'SP', '%change']]
        dates = sorted(list(set(df.index.date)))
        for date in dates:
            df1 = df[df.index.date == date].copy()
            df1['cumpro'] = ((df1['%change'] / 100 + 1).cumprod() - 1) * 100
            self.day_wise = self.day_wise.append(pd.DataFrame({'Date': [date],
                                                               'Day_return': [df1['cumpro'].iloc[-1]]}))
        self.day_wise.set_index('Date', inplace=True, drop=True)
        self.day_wise['CumReturn'] = ((self.day_wise['Day_return'] / 100 + 1).cumprod() - 1) * 100
        # print(self.day_wise)


class Plot:
    def __init__(self,df1,df2,df3,df4,symbol):
        self.df1 = df1
        self.df2 = df2
        self.df3 = df3
        self.df4 = df4
        self.symbol = symbol

    def plot(self):
        import matplotlib.pyplot as plt
        f, ax = plt.subplots(2, 2, figsize=(16, 9), dpi=90, facecolor='w', edgecolor='k')
        f.suptitle(self.symbol)
        if len(self.df1) != 0:
            ax[0, 0].plot(self.df1)  # row=0, col=0
            ax[0, 0].title.set_text('Trade Wise Return BUY SIDE')
            ax[0, 0].grid()

        if len(self.df2) != 0:
            ax[0, 1].plot(self.df2, 'b')  # row=1, col=0
            ax[0, 1].title.set_text('Trade Wise Return SELL SIDE')
            ax[0, 1].grid()

        if len(self.df3) != 0:
            ax[1, 0].plot(self.df3, 'g')  # row=0, col=1
            ax[1, 0].title.set_text('TOTAL Return Trade wise')
            ax[1, 0].grid()

        if len(self.df4) != 0:
            ax[1, 1].plot(self.df4, 'k')  # row=1, col=1
            ax[1, 1].title.set_text('TOTAL Return Day Wise')
            ax[1, 1].grid()
        # txt="I need the caption to be present a little below X-axis\n" \
        #     "I need the caption to be present a little below X-axis"
        # f.text(.05,.05,txt)
        f.tight_layout()
        plt.show()