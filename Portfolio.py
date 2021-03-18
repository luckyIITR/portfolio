import pandas as pd


class Portfolio:

    def __init__(self, symbol):
        self.symbol = symbol
        self.order_df = pd.DataFrame({"Time": [],
                                      "Price": [],
                                      "Status": []})

    def buy(self, bp, time):
        self.order_df = self.order_df.append(pd.DataFrame({'Time': [time],
                                                           "Price": [bp],
                                                           'Status': ['BUY']}), ignore_index=True)

    def square_off(self, sp, time):
        self.order_df = self.order_df.append(pd.DataFrame({'Time': [time],
                                                           "Price": [sp],
                                                           'Status': ['SQ']}), ignore_index=True)
