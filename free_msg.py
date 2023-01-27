from telethon.sync import TelegramClient, events
import re

from telethon.tl.types import *
import math
import init
from binance.client import  Client
from binance.enums import *
import json

from pybit import usdt_perpetual

api_id = 25717021
api_hash = "cba79f026856da860d65b354a75d50da"
client = TelegramClient('anon', api_id, api_hash)
client.start()
kosirBitcoin = -1001681322568
DQ_channel = -1001347867469
testing1 =-835623858
testing2 =-873060948

mock_future_api_key = init.mock_future_API_key
mock_future_api_secret = init.mock_future_API_secret


binance_client =  Client(init.mock_future_API_key, init.mock_future_API_secret, testnet=True)

bybit_session = usdt_perpetual.HTTP(
    endpoint='https://api-testnet.bybit.com', 
    api_key="CkSkPAoGdHeo6GscAE",
    api_secret="NxJrZDnyELYP1XcsjEsJ9xqJdgPYAKNm28yk"
)


def matching_side(message):
    strategy_1_long_open = re.search("做多開倉", message)
    strategy_1_long_close = re.search("做多全部平倉", message)
    strategy_1_short_open = re.search("做空開倉", message)
    strategy_1_short_close = re.search("做空全部平倉", message)
    side=""

#"《做多開倉》"
    if(strategy_1_long_open !=None and strategy_1_long_close == None and strategy_1_short_open == None and strategy_1_short_close == None):
        side ='Buy'

        return(side)
#"《做多平倉》"
    if(strategy_1_long_close != None and strategy_1_short_close == None and strategy_1_long_open == None and strategy_1_short_open == None):
        side= 'Sell'
        
        
        return (side);
#"《做空開倉》"
    if(strategy_1_short_open != None and strategy_1_long_open == None and strategy_1_long_close == None and strategy_1_short_close == None ):
        side = 'Sell'
        
        
        return (side);
#"《做空平倉》"
    if(strategy_1_short_close !=None and strategy_1_long_open == None and strategy_1_long_close == None and strategy_1_short_open == None):
        side = 'Buy'
        
        
        return (side);

def matching_positionSide(message):
    strategy_1_long_open = re.search("做多開倉", message)
    strategy_1_long_close = re.search("做多全部平倉", message)
    strategy_1_short_open = re.search("做空開倉", message)
    strategy_1_short_close = re.search("做空全部平倉", message)
    positionSide=""
    

#"《做多開倉》"
    if(strategy_1_long_open !=None and strategy_1_long_close == None and strategy_1_short_open == None and strategy_1_short_close == None):
        
        positionSide=1
        
        return(positionSide)
#"《做多平倉》"
    if(strategy_1_long_close != None and strategy_1_short_close == None and strategy_1_long_open == None and strategy_1_short_open == None):
        
        positionSide=1
        
        return (positionSide);
#"《做空開倉》"
    if(strategy_1_short_open != None and strategy_1_long_open == None and strategy_1_long_close == None and strategy_1_short_close == None ):
        
        positionSide =2
        
        return (positionSide);
#"《做空平倉》"
    if(strategy_1_short_close !=None and strategy_1_long_open == None and strategy_1_long_close == None and strategy_1_short_open == None):
        
        positionSide =2
        
        return (positionSide);

def matching_price(message):
    price= message.split('at',1)
    return(price[1]);

def matching_coin(message):  # defining it is BTC or ETH
    strategy_coin = re.search("btc/USDT", message)  # 只有ETH 或者BTC
    if (strategy_coin != None):
        return ("BTCUSDT")
    else:
        return ("ETHUSDT")

async def getTheQuantity(ratio,price): #ration is the percentage of the balance
    balance=await bybit_getTheUSDTAmount()
    #balance=5000
    leverage=50; #fixed
    return (float(balance)*float(ratio)*float(leverage)/float(price));

# def binance_getTheUSDTAmount():
#     acc =   binance_client.futures_account_balance();
#     USDT_balance=acc[3]['balance']#hard code to get the USDT balance
#     return USDT_balance

async def bybit_getTheUSDTAmount():
    acc =  bybit_session.get_wallet_balance(coin="USDT")
    USDT_balance=acc["result"]["USDT"]["available_balance"]#hard code to get the USDT balance
    return USDT_balance

# def Binance_createNewOrder(symbol,side,positionSide,price,quantity):
#     #BUY LONG == 做多開倉
#     #SELL SHORT ＝＝做空開倉

#     # new_order=binance_client.futures_create_order(
#     #     symbol= 'BTCUSDT', #Type of coin e.g.:"BTCUSDT"
#     #     side=SIDE_SELL ,   #BUY OR Sell
#     #     positionSide= "short", #Long or Short  
#     #     type= FUTURE_ORDER_TYPE_LIMIT,  #the type of order e.g.LIMIT/ MARKET
#     #     quantity=1, # the order amount
#     #     price=18000, # order price ,
#     #     timeInForce = TIME_IN_FORCE_GTC,)

#     new_order=binance_client.futures_create_order(
#         symbol= symbol, #Type of coin e.g.:"BTCUSDT"
#         side=side ,   #BUY OR Sell
#         positionSide= positionSide, #Long or Short  
#         type= FUTURE_ORDER_TYPE_LIMIT,  #the type of order e.g.LIMIT/ MARKET
#         quantity=quantity, # the order amount
#         price=price, # order price ,
#         timeInForce = TIME_IN_FORCE_GTC,)
        
#     order_response.testing_response.update(new_order);
    
#     print(order_response.testing_response);
#     jsonString = json.dumps(order_response.testing_response);
#     jsonFile =open("testing_response","w");
#     jsonFile.write(jsonString);
#     jsonFile.close;        

def bybit_createNewOrder(symbol,side,qty,price,positionSide):
    #BUY LONG == 做多開倉
    #SELL SHORT ＝＝做空開倉
    #Sell Long == 做多平倉
    #Buy Short ＝＝做空平倉

    #1-LONG side of both side mode
    #2-SHORT side of both side mode SHORT
    order=bybit_session.place_active_order(
        symbol=symbol,
        side=side,
        qty=qty,
        price=price,
        order_type="Limit",
        time_in_force="GoodTillCancel",
        reduce_Only=False,
        close_on_trigger=False,
        position_idx=positionSide
    )
    print(order)


@client.on(events.NewMessage(chats=testing1,incoming=True))
async def my_event_helper(event):
    print(event.raw_text)
    symbol=matching_coin(event.raw_text)
    side=matching_side(event.raw_text)
    positionSide=matching_positionSide(event.raw_text)
    price=matching_price(event.raw_text)
    price=math.floor(float(price))
    quantity=await getTheQuantity(ratio=0.05,price=price)
    
    print(quantity)
    
    #bybit_createNewOrder(symbol=symbol,side=side,qty=quantity,price=price,positionSide=positionSide)


with client:
    client.run_until_disconnected()
