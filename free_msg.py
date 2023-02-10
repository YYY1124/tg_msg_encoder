from telethon.sync import TelegramClient, events
import re

from telethon.tl.types import *
import math
import init
from binance.client import  Client
from binance.enums import *
import json
import sys
import logging
from threading import Timer

from pybit import usdt_perpetual
class strategy:
    free_strategy={"BTCUSDT":{},"ETHUSDT":{}}

    def strategy_getter(symbol):   
        if(symbol=="BTCUSDT"):
            return strategy.free_strategy["BTCUSDT"]
        elif(symbol=="ETHUSDT"):
            return strategy.free_strategy["ETHUSDT"]
        else:
            bybit_API_logger.exception("Wrong Symbol for strategy_getter")
    def strategy_setter(symbol,order):
        if(symbol=="BTCUSDT"):
            strategy.free_strategy["BTCUSDT"]=order
        elif(symbol=="ETHUSDT"):
            strategy.free_strategy["ETHUSDT"]=order
        else:
            bybit_API_logger.exception("Wrong Symbol for strategy_setter")
        bybit_API_logger.info(strategy.free_strategy)
        jsonString=json.dumps(strategy.free_strategy)
        jsonFile=open("free_existing_order.json","w")
        jsonFile.write(jsonString)
        jsonFile.close
api_id = 25717021
api_hash = "cba79f026856da860d65b354a75d50da"

client = TelegramClient('googleCloudServer', api_id, api_hash)
client.start()
def program_continuity_checker():
    print ("one hour pass away")
    bybit_API_logger.info("one hour pass away")
    Timer(3600, program_continuity_checker) .start()
   
continuity_timer = Timer(3600, program_continuity_checker).start() 

bybit_session = usdt_perpetual.HTTP(
    endpoint='https://api-testnet.bybit.com', 
    api_key=init.bybit_testnet_future_api_key,
    api_secret=init.bybit_testnet_future_api_secret
)

print("the program is receiving message ")
jsonFile=open("free_existing_order.json","r")
strategy.free_strategy=json.load(jsonFile) #get the existing order when the program start.
print(strategy.free_strategy)


#when the new position is created, this variable will update
# BTC_last_order=bybit_session.get_active_order(symbol="BTCUSDT",order_status="Filled",limit=1)["result"]["data"][0]
# ETH_last_order=bybit_session.get_active_order(symbol="ETHUSDT",order_status="Filled",limit=1)["result"]["data"][0]



    

kosirBitcoin = -1001681322568

testing1 =-835623858
testing2 =-873060948


bybit_API_logger=logging.getLogger(__name__)

file_handler=logging.FileHandler("free_decoder_operation.log")
log_formatter =logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
file_handler.setFormatter(log_formatter)
stream_handler = logging.StreamHandler()

bybit_API_logger.setLevel(logging.INFO)
bybit_API_logger.addHandler(file_handler)
bybit_API_logger.addHandler(stream_handler)

free_strategy_current_order_id="free_strategy_current_order_id.txt"




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

def matching_symbol(message):  # defining it is BTC or ETH
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

# def updateTheLastOrder(symbol,order):
    
    
#     if(symbol=="BTCUSDT"):
#         global BTC_last_order
#         BTC_last_order=order["result"]
#     elif(symbol=="ETHUSDT"):
#         global ETH_last_order
#         ETH_last_order=order["result"]


async def bybit_getTheUSDTAmount():
    acc =  bybit_session.get_wallet_balance(coin="USDT")
    USDT_balance=acc["result"]["USDT"]["available_balance"]#hard code to get the USDT balance
    return USDT_balance

     

async def bybit_createNewOrder(symbol,side,qty,price,positionSide):
    #BUY LONG == 做多開倉
    #SELL SHORT ＝＝做空開倉
    #Sell Long == 做多平倉
    #Buy Short ＝＝做空平倉

    #1-LONG side of both side mode
    #2-SHORT side of both side mode SHORT
    if(side=="Sell" and positionSide==1): #checking whether it is closing action, This is 做多平倉
        try:
            response=await bybit_closingThePosition(symbol=symbol,side=side,positionSide=positionSide,price=price)
            bybit_API_logger.info(response)
              
        except:
            bybit_API_logger.exception(Exception) #logging the order exception
    elif(side=="Buy" and positionSide==2):#checking whether it is closing action, This is 做空平倉
        
        try:
            response=await bybit_closingThePosition(symbol=symbol,side=side,positionSide=positionSide,price=price)
            bybit_API_logger.info(response)
            
        except:
            bybit_API_logger.exception(Exception) #logging the order exception
            
    else:                              #If it is a opening signal, the below will try to open the position.
        try:
            bybit_API_logger.info('symbol:{} action: {} {} price: {} qty: {}'.format(symbol,side,positionSide,price,qty))
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
            bybit_API_logger.info(order)
            strategy.strategy_setter(symbol=symbol,order=order)
            return order
        except:
            bybit_API_logger.exception(Exception) #logging the order exception

async def bybit_unfilledOrderChecker(symbol): #return ture, if the current order is unfilled
    current_order=strategy.strategy_getter(symbol=symbol)["result"]
    the_unfilled_order=bybit_session.get_active_order(symbol=symbol,order_status="New")["result"]["data"]
    cancelling=False
    if(len(the_unfilled_order)>0): #check is any unfilled order exist, if yes,
        for order in the_unfilled_order:
            if(order["order_id"]==current_order["order_id"]):  #Checking whether the order have been filled, if not, just cancelled the order.
                cancelling=True
    return cancelling 

async def bybit_closingThePosition(symbol,side,positionSide,price):
    current_order=strategy.strategy_getter(symbol=symbol)["result"]
    cancelling=await bybit_unfilledOrderChecker(symbol=symbol) 

    if(cancelling==True): #Checking whether the order have been filled, if not, just cancelled the order.
        response=bybit_session.cancel_active_order(symbol=symbol,order_id=current_order["order_id"])
        strategy.strategy_setter(symbol=symbol,order={})
        return response
    elif(cancelling==False): #if the order have been Created(啱啱開), close the position
        existing_qty=current_order["qty"]
        order=bybit_session.place_active_order(
                        symbol=symbol,
                        side=side,
                        qty=existing_qty,
                        price=price,
                        order_type="Limit",    #Using the Market type , and observating if there are any bugs
                        time_in_force="GoodTillCancel",
                        position_idx=positionSide,
                        reduce_Only=True,
                        close_on_trigger=True)
        strategy.strategy_setter(symbol=symbol,order={})#when the position have been closed, empty the order
        return order
    else:
        bybit_API_logger.exception("Wrong Order Status")



@client.on(events.NewMessage(chats=kosirBitcoin,incoming=True))
async def my_event_helper(event):
    
    logging.info(event.raw_text) #logging in to log
    symbol=matching_symbol(event.raw_text)
    side=matching_side(event.raw_text)
    positionSide=matching_positionSide(event.raw_text)
    price=matching_price(event.raw_text)
    price=math.floor(float(price))
    quantity=round(await getTheQuantity(ratio=0.05,price=price),2)
    
    order= await bybit_createNewOrder(symbol=symbol,side=side,qty=quantity,price=price,positionSide=positionSide)
        

        


 
with client:
    client.run_until_disconnected()
