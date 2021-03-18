import pandas as pd


class Buy_Portfolio:

    def __init__(self, symbol):
        self.symbol = symbol
        self.order_df = pd.DataFrame({"Time": [],
                                      "Price": [],
                                      "Status": []})
        self.trade_df = pd.DataFrame()

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
        self.result()
        print(self.trade_df)

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
