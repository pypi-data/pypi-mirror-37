from Keys.keys import API_keys
import sqlite3
import sqlalchemy
from sqlalchemy import create_engine
from twisted.internet import task
from twisted.internet import reactor
from BinanceAPI.client import Client
import time
from BinanceAPI.enums import *
import save_historical_data_to_replace
from BinanceKeys import BinanceKey1
import numpy as np
import pandas as pd
from pandas.io import sql





api_key = BinanceKey1['OfBLqIoRvQCloLCSc5lmrN5ikapHhDul27yn6TrsM5X7l0dkw64ME0ESkEkBatNL']
api_secret = BinanceKey1['9Jwb6sR6z8N4jWlK9n0bZrHAeipA8FaYibl5VFnBoE0t3CmnY1CyVWKCekOmpg2r']

client = Client(api_key, api_secret)

# get a deposit address for BTC
address = client.get_deposit_address(asset='BTC')

sym = 'ETHBTC'



#connection to databse file





    
class Scrapper():
    def __init__(self, assetpair ='', exchange = ''):
        self.current_spread = current_spread
        self.assetpair = ''
        self.exchange = ''
        self.symbol = symbol
        self.df_asks = df_asks
        self.df = df
        self.df_bids = df_bids
        self.df_spread = df_spread
        

    def scrapper(sym, num_entries=20):

       
        i=1 #Used as a counter for number of entries
        j=1
        depth = client.get_order_book(symbol=sym)
        
        server_time = (client.get_server_time())
        aa = str(server_time)
        bb = aa.replace("{'serverTime': ","")
        aa = bb.replace("}","")
        timestamp_server=int(aa)
        #apply the removal of dict.
        timestamp = convert_time_binance(server_time)

        ask_prices = []
        ask_volumes = []
        bid_prices = []
        bid_volumes = []
        spread = []
        servertime = []
        
        while i<num_entries:
            for ask in depth['asks']:
                aa = str(ask)
                bb = aa.replace("[","")
                aa = bb.replace(", ]]", "")
                bb = aa.replace("'","")
                bb = bb.split(",")
                ask_prices.insert(1, bb[0])
                ask_volumes.insert(1, bb[1])
                i+=1
            #turn this list into a indexed series=> then into a dataframe
        while j<num_entries:
            for bid in depth['bids']:
                gg = str(bid)
                zz = gg.replace("[","")
                gg = zz.replace(", ]]", "")
                zz = gg.replace("'","")
                gg = zz.split(",")
                bid_prices.insert(1, gg[0])
                bid_volumes.insert(1, gg[1])
                j+= 1
               
        s1 = pd.Series(ask_prices)
        s2 = pd.Series(ask_volumes)
        s3 = pd.Series(bid_prices)
        s4 = pd.Series(bid_volumes)
        df = pd.DataFrame(dict(askprices = s1, askvolumes = s2, bidprices = s3, bidvolumes = s4)).reset_index()
        df = df.drop(['index'], axis=1)

        df_asks = pd.DataFrame(dict(update_time = timestamp, askprices = s1, askvolumes = s2)).reset_index()
        df_asks= df_asks.drop(['index'], axis=1)

        df_bids = pd.DataFrame(dict(bidprices = s3, bidvolumes = s4)).reset_index()
        df_bids= df_bids.drop(['index'], axis=1)

        df.info(verbose = True)

        min_askorderprice = float(min(ask_prices))
        max_bidorder_price = float(max(bid_prices))
        current_spread = round(((min_askorderprice - max_bidorder_price)/min_askorderprice), 7) # this is the current bid ask spread
        spread.append(current_spread)
        servertime.append(timestamp_server)
        
        s5 = pd.Series(spread)
        s6 = pd.Series(servertime)
        df_spread = pd.DataFrame(dict(servertime = s6, spread = s5))


     
        return df, df_asks, df_bids, df_spread
    

     

def convert_time_binance(gt):
    #Converts from Binance Time Format (milliseconds) to time-struct
    #From Binance-Trader Comment Section Code
    gt = client.get_server_time()
    aa = str(gt)
    bb = aa.replace("{'serverTime': ","")
    aa = bb.replace("}","")
    gg=int(aa)
    ff=gg-10799260
    uu=ff/1000
    yy=int(uu)
    tt=time.localtime(yy)
    tt = str(tt)
    return tt


def market_depth(sym, num_entries=20):
    #Get market depth
    #Retrieve and format market depth (order book) including time-stamp
    i=0     #Used as a counter for number of entries
    print("Order Book: ", convert_time_binance(client.get_server_time()))
    depth = client.get_order_book(symbol=sym)
    print(depth)
    print(depth['asks'][0])
    ask_tot=0.0
    ask_price =[]
    ask_quantity = []
    bid_price = []
    bid_quantity = []
    bid_tot = 0.0
    place_order_ask_price = 0
    place_order_bid_price = 0
    max_order_ask = 0
    max_order_bid = 0
    print("\n", sym, "\nDepth     ASKS:\n")
    print("Price     Amount")
    for ask in depth['asks']:
        if i<num_entries:
            if float(ask[1])>float(max_order_ask):
                #Determine Price to place ask order based on highest volume
                max_order_ask=ask[1]
                place_order_ask_price=round(float(ask[0]),5)-0.0001
            #ask_list.append([ask[0], ask[1]])
            ask_price.append(float(ask[0]))
            ask_tot+=float(ask[1])
            ask_quantity.append(ask_tot)
            #print(ask)
            i+=1
    j=0     #Secondary Counter for Bids
    print("\n", sym, "\nDepth     BIDS:\n")
    print("Price     Amount")
    for bid in depth['bids']:
        if j<num_entries:
            if float(bid[1])>float(max_order_bid):
                #Determine Price to place ask order based on highest volume
                max_order_bid=bid[1]
                place_order_bid_price=round(float(bid[0]),5)+0.0001
            bid_price.append(float(bid[0]))
            bid_tot += float(bid[1])
            bid_quantity.append(bid_tot)
            #print(bid)
            j+=1
    return ask_price, ask_quantity, bid_price, bid_quantity, place_order_ask_price, place_order_bid_price




        
        
def series_orders(sym, num_entries=20):
    i=0     #Used as a counter for number of entries
    print("Order Book: ", convert_time_binance(client.get_server_time()))
    depth = client.get_order_book(symbol=sym)
    print(depth)
    return depth


