import sqlite3
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
from pandas.io import sql


api_key = BinanceKey1['OfBLqIoRvQCloLCSc5lmrN5ikapHhDul27yn6TrsM5X7l0dkw64ME0ESkEkBatNL']
api_secret = BinanceKey1['9Jwb6sR6z8N4jWlK9n0bZrHAeipA8FaYibl5VFnBoE0t3CmnY1CyVWKCekOmpg2r']

client = Client(api_key, api_secret)

# get a deposit address for BTC
address = client.get_deposit_address(asset='BTC')

symbol = ['ETHBTC']

pd.set_option('display.max_row', 1000)

pd.set_option('display.max_columns', 50)




    


def store_historical_trades(symbol, num_entries = 500):


    
    trade_id =[]
    trade_price =[]
    trade_quantity =[]
    trade_timestamp =[]
    trade_maker_status =[]
    trade_best_match_status =[]
    
    


    try:

        con = sqlite3.connect("/Users/maarten/binance.db")
        print('SQLite connection is open')

        df.to_sql("historical_trades", con, if_exists = 'append', index = False,)


    finally:
        con.close()
        print('SQLite connection is closed')

    return df
   



def convert_time_binance(gt):
    #Converts from Binance Time Format (milliseconds) to time-struct
    #From Binance-Trader Comment Section Code
    #gt = client.get_server_time()
    print("Binance Time: ", gt)
    print(time.localtime())
    aa = str(gt)
    bb = aa.replace("{'serverTime': ","")
    aa = bb.replace("}","")
    gg=int(aa)
    ff=gg-10799260
    uu=ff/1000
    yy=int(uu)
    tt=time.localtime(yy)
    #print(tt)
    return tt












#place an order on Binance
"""
order = client.create_order(
    symbol='BNBBTC',
    side=SIDE_BUY,
    type=ORDER_TYPE_LIMIT,
    timeInForce=TIME_IN_FORCE_GTC,
    quantity=100,
    price='0.00001')
"""

if __name__ == "__main__":
    store_historical_trades(symbol)
