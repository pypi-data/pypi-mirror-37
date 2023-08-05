
from binance.client import Client
import time
import matplotlib
from matplotlib import cm
import matplotlib.pyplot as plt
from binance.enums import *
import save_historical_data_Roibal
from BinanceKeys import BinanceKey1


api_key = BinanceKey1['OfBLqIoRvQCloLCSc5lmrN5ikapHhDul27yn6TrsM5X7l0dkw64ME0ESkEkBatNL']
api_secret = BinanceKey1['9Jwb6sR6z8N4jWlK9n0bZrHAeipA8FaYibl5VFnBoE0t3CmnY1CyVWKCekOmpg2r']

client = Client(api_key, api_secret)

# get a deposit address for BTC
address = client.get_deposit_address(asset='BTC')

def run():
    # get system status
    #Create List of Crypto Pairs to Watch
    list_of_symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT','BNBBTC', 'ETHBTC', 'LTCBTC']
    micro_cap_coins = ['ICXBNB', 'BRDBNB', 'NAVBNB', 'RCNBNB']

    #Get Status of Exchange & Account
    try:
        status = client.get_system_status()
        print("\nExchange Status: ", status)

        #Account Withdrawal History Info
        withdraws = client.get_withdraw_history()
        print("\nClient Withdraw History: ", withdraws)

        #get Exchange Info
        info = client.get_exchange_info()
        print("\nExchange Info (Limits): ", info)
    except():
        pass

    # place a test market buy order, to place an actual order use the create_order function
    # if '1000 ms ahead of server time' error encountered, visit https://github.com/sammchardy/python-binance/issues/249
    try:
        order = client.create_test_order(
            symbol='BNBBTC',
            side=Client.SIDE_BUY,
            type=Client.ORDER_TYPE_MARKET,
            quantity=100)
    except:
        print("\n \n \nATTENTION: NON-VALID CONNECTION WITH BINANCE \n \n \n")

    #Get Info about Coins in Watch List
    coin_prices(list_of_symbols)
    coin_tickers(list_of_symbols)
    #for symbol in list_of_symbols:
    #    market_depth(symbol)

    #for coin in micro_cap_coins:
    #    visualize_market_depth(1, 1, coin)
    for coin in micro_cap_coins:
        scalping_orders(coin, 1, 1)

    #get recent trades
    trades = client.get_recent_trades(symbol='BNBBTC')
    print("\nRecent Trades: ", trades)
    print("Local Time: ", time.localtime())
    print("Recent Trades Time: ", convert_time_binance(trades[0]['time']))

    #get historical trades
    try:
        hist_trades = client.get_historical_trades(symbol='BNBBTC')
        print("\nHistorical Trades: ", hist_trades)
    except:
        print('\n \n \nATTENTION: NON VALID CONNECTION WITH BINANCE \n \n \n')

    #get aggregate trades
    agg_trades = client.get_aggregate_trades(symbol='BNBBTC')
    print("\nAggregate Trades: ", agg_trades)


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




def portfolio_management(deposit = '10000', withdraw=0, portfolio_amt = '0', portfolio_type='USDT', test_acct='True'):
    
    
    pass



if __name__ == "__main__":
    run()
