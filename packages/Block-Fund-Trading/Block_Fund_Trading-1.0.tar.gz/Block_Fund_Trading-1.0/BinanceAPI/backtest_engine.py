
from binance.client import Client
import time
import matplotlib
from matplotlib import cm
import matplotlib.pyplot as plt
from binance.enums import *
import save_historical_data_Roibal
from BinanceKeys import BinanceKey1
import numpy as np
import pandas as pd
import Order_Book


api_key = BinanceKey1['api_key']
api_secret = BinanceKey1['api_secret']

client = Client(api_key, api_secret)

address = client.get_deposit_address(asset='BTC')

class backtest:
    def __init__(self, coins):
        
    def run_test(self):

        result_sum = []
        total_profit = 0
        total_trades = 0

        base_funds = 1
        alt_funds = 0
        capital = 0
        trades = 0
        in_trade = False
        stop_loss = 0
        last_buy = 0
        won = 0
        lost = 0
        cur_trade_sym = ''

        for c in self.coins:
            der = self.calc_derived(c)
            self.all_candles.append(der)

            length = len(self.all_candles[0]) - 10

            for i in range(self.long_lookback + 1, length):
                for a in self.all_candles:

                    symbol = a[i]['symbol']
                    time_n = a[i]['time']
                    close = a[i]['close']
                    high = a[i]['high']
                    low = a[i]['low']
                    dev = a[i]['st_dev']
                    ma = a[i]['m_avg']
                    l_ma = a[i]['l_ma']
                    N = a[i]['N']
                    position = abs(close - ma)

                    last_close = a[i - 1]['close']
                    last_dev = a[i - 1]['st_dev']
                    last_ma = a[i - 1]['m_avg']
                    bench_l_ma = a[i - 1]['l_ma']
                    last_postion = abs(last_close - last_ma)

                    if not in_trade and close < ma and position > dev * 2 and l_ma > bench_l_ma:
                        price = close
                        last_buy = price
                        if symbol == 'BTC-DOGE':
                            stop_loss = price - N
                        else:
                            stop_loss = price - N * .4
                        alt_funds = (base_funds / price) * 0.9985
                        base_funds = 0
                        trades += 1
                        in_trade = True
                        cur_trade_sym = symbol
                        print(
                            str(time_n) + ' ' + symbol + " Price low and post out-of-band peak, bought " + "{:.2f}".format(
                                alt_funds) + self.green + " at " + "{:.8f}".format(
                                price) + self.stop_col)
                    if in_trade and cur_trade_sym == symbol:
                        if close < stop_loss:
                            base_funds = (alt_funds * stop_loss) * 0.9985
                            capital = base_funds
                            alt_funds = 0
                            in_trade = False
                            lost += 1
                            print(
                                str(time_n) + ' ' + symbol + " Stop-loss triggered, sold at  " + self.red + "{:.8f}".format(
                                    stop_loss) + self.stop_col + " resulting balance = " + "{:.3f}".format(base_funds))
                            print('')
                            print('')
                        elif close > ma and position > dev * 2 and close > last_buy * 1.02:  # or (symbol == 'BTC-DOGE' and close > last_buy * 1.05)):  #and position < last_postion:
                            price = close
                            base_funds = (alt_funds * price) * 0.9985
                            capital = base_funds
                            alt_funds = 0
                            in_trade = False
                            if close > last_buy:
                                color = self.green
                                won += 1
                            else:
                                color = self.red
                                lost += 1
                            print(str(
                                time_n) + ' ' + symbol + " Price high and post out-of-band peak, sold at  " + color + "{:.8f}".format(
                                close) + self.stop_col + " resulting balance = " + "{:.3f}".format(base_funds))
                            print('')
                            print('')

            print('Final capital = ' + str(capital))
            print("Made " + str(trades) + " trades")
            print("Won " + str(won) + " lost " + str(lost))
