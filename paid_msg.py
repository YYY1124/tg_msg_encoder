from pybit import usdt_perpetual
from telethon.sync import TelegramClient, events
import re,math,sys,logging
from telethon.tl.types import *
from threading import Timer
import init

api=init
client = TelegramClient('macTesting', api.telegram_api_id,api.telegram_api_hash )
#client.start()

def program_continuity_checker():
    print ("one hour pass away")
    bybit_API_logger.info("one hour pass away")
    Timer(3600, program_continuity_checker) .start()
   
#continuity_timer = Timer(3600, program_continuity_checker).start() 

bybit_session = usdt_perpetual.HTTP(
    endpoint='https://api-testnet.bybit.com', 
    api_key=api.bybit_testnet_future_api_key,
    api_secret=api.bybit_testnet_future_api_secret
)

print("the program is receiving message ")

kosirBitcoin = -1001681322568
DQ_channel = -1001347867469
testing1 =-835623858
testing2 =-873060948

bybit_API_logger=logging.getLogger(__name__)

file_handler=logging.FileHandler("paid_decoder_operation.log")
log_formatter =logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
file_handler.setFormatter(log_formatter)
stream_handler = logging.StreamHandler()
bybit_API_logger.setLevel(logging.INFO)
bybit_API_logger.addHandler(file_handler)
bybit_API_logger.addHandler(stream_handler)

strategy_list={"free":{"BTCUSDT":{},"ETHUSDT":{}},
          "strategy1":{"BTCUSDT":{},"ETHUSDT":{}},
          "strategy2":{"BTCUSDT":{},"ETHUSDT":{}},
          "strategy_devin":{"BTCUSDT":{},"ETHUSDT":{}}}

def matching_strategy(message):
    
    result=re.findall(r"「.*」",message)[0] 
    
    if(result == "「1號策略」"):
        return 1
    elif(result == "「2號策略」"):
        return 2
    elif(result == "「Devin策略」"):
        return 3
    else:
        bybit_API_logger.info("can not find the correct strategy, ignore this message")

def matching_side(message):
    strategy_1_long_open = re.search(r"做多開倉", message)
    strategy_1_long_close = re.search(r"做多全部平倉|做多平倉\d\d%", message)
    strategy_1_short_open = re.search(r"做空開倉", message)
    strategy_1_short_close = re.search(r"做空全部平倉|做空平倉\d\d%", message)
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

def updateTheLastOrder(strategy,symbol,order):
    
    if(strategy==1):
        global strategy_list
        strategy_list["strategy1"][symbol]=order["result"]

    elif(strategy==2):
        
        strategy_list["strategy2"][symbol]=order["result"]
    elif(strategy==3):
        
        strategy_list["strategy3"][symbol]=order["result"]


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
            response=await bybit_closingThePosition(symbol=symbol,side=side,positionSide=positionSide)
            bybit_API_logger.info(response)
              
        except:
            bybit_API_logger.exception(Exception) #logging the order exception
    elif(side=="Buy" and positionSide==2):#checking whether it is closing action, This is 做空平倉
        
        try:
            response=await bybit_closingThePosition(symbol=symbol,side=side,positionSide=positionSide)
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
            updateTheLastOrder(symbol=symbol,order=order)
            print(ETH_last_order)
            return order
        except:
            bybit_API_logger.exception(Exception) #logging the order exception
    
async def bybit_closingThePosition(symbol,side,positionSide):
    if(symbol=="BTCUSDT"):
            current_order=BTC_last_order
    elif(symbol=="ETHUSDT"):
            current_order=ETH_last_order
        
    if(current_order["order_status"]=="New"): #Checking whether the order have been filled, if not, just cancelled the order.
        response=bybit_session.cancel_active_order(symbol=symbol,order_id=current_order["order_id"])
        return response
    elif(current_order["order_status"]=="Created" or current_order["order_status"]=="Filled"): #if the order have been Created(啱啱開), close the position
        existing_qty=current_order["qty"]
        order=bybit_session.place_active_order(
            symbol=symbol,
            side=side,
            qty=existing_qty,
            order_type="Market",    #Using the Market type , and observating if there are any bugs
            time_in_force="GoodTillCancel",
            position_idx=positionSide,
            reduce_Only=True,
            close_on_trigger=True)
        updateTheLastOrder(symbol=symbol,order=order)
        return order
    else:
        bybit_API_logger.exception("Wrong Order Status")

    

def main():
    message="btc/USDT 「2號策略」《做空平倉60%》@ 22963.09"
    result= matching_side(message)
    print(result)

if __name__==main():
    main()