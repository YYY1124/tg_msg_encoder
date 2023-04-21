from pybit.unified_trading import HTTP
from telethon.sync import TelegramClient, events
import re,math,sys,logging,json
from telethon.tl.types import *
from threading import Timer
import init


api=init
client = TelegramClient('googleCloudServer', api.telegram_api_id,api.telegram_api_hash )
client.start()

def program_continuity_checker():
    print ("one hour pass away")
    bybit_API_logger.info("one hour pass away")
    Timer(3600, program_continuity_checker) .start()
   
continuity_timer = Timer(3600, program_continuity_checker).start() 

bybit_session = HTTP(
    testnet=True, 
    api_key=api.bybit_testnet_future_api_key,
    api_secret=api.bybit_testnet_future_api_secret,
)



kosirBitcoin = -1001681322568
kosirBitcoinPaid= -1001763853057
DQ_channel = -1001347867469
testing1 =-835623858
testing2 =-873060948
tommy = 952653251

bybit_API_logger=logging.getLogger(__name__)

file_handler=logging.FileHandler("paid_decoder_operation.log")
log_formatter =logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
file_handler.setFormatter(log_formatter)
stream_handler = logging.StreamHandler()
bybit_API_logger.setLevel(logging.INFO)
bybit_API_logger.addHandler(file_handler)
bybit_API_logger.addHandler(stream_handler)

# strategy_list={"free":{"BTCUSDT":{},"ETHUSDT":{}},
#           "strategy1":{"BTCUSDT":{},"ETHUSDT":{}},
#           "strategy2":{"BTCUSDT":{},"ETHUSDT":{}},
#           "strategy_devin":{"BTCUSDT":{},"ETHUSDT":{}}}



class strategy:
    strategy_list={
          "strategy1":{"BTCUSDT":{},"ETHUSDT":{}},
          "strategy2":{"BTCUSDT":{},"ETHUSDT":{}},
          "strategy_devin":{"BTCUSDT":{},"ETHUSDT":{}}}
    def strategy_getter(stra,symbol):
        if(stra==1):
            return strategy.strategy_list["strategy1"][symbol]
        elif(stra==2):
            return strategy.strategy_list["strategy2"][symbol]
        elif(stra==3):
            return strategy.strategy_list["strategy_devin"][symbol]
        else:
            print(stra)
            bybit_API_logger.exception("wrong strategy number,the getter error occur")
    
    def strategy_setter(stra,symbol,order):
        if(stra==1):
            strategy.strategy_list["strategy1"][symbol]=order
        elif(stra==2):
            strategy.strategy_list["strategy2"][symbol]=order
        elif(stra==3):
            strategy.strategy_list["strategy_devin"][symbol]=order
        else:
            bybit_API_logger.exception("wrong strategy number, the setter error occur")
        print(strategy.strategy_list)
        jsonString=json.dumps(strategy.strategy_list)
        jsonFile=open("existing_order.json","w")
        jsonFile.write(jsonString)
        jsonFile.close


print("the program is receiving message ") ##############################
jsonFile=open("existing_order.json","r")
strategy.strategy_list=json.load(jsonFile) #get the existing order when the program start.
print(strategy.strategy_list)

def matching_strategy(message):
    
    result=re.findall(r"「.*」",message)[0]
    
    if(result == "「1號策略」"):
        return 1
    elif(result == "「2號策略」"):
        return 2
    elif(result == "「Devin 策略」"or"「Devin策略」" ):
        return 3
    else:
        bybit_API_logger.info("can not find the correct strategy, ignore this message")
        return 0

#return true if it is valid, return false if it is noise
def ignoring_noise(message):
    noise= re.search(r'準備平倉|準備開倉|市場短線進入',message)
    if(noise !=None):
        return True;
    else:
        return False;

def matching_side(message):
    strategy_1_long_open = re.search(r"做多開倉|做多入場", message)
    strategy_1_long_close = re.search(r"做多全部平倉|做多平倉\d\d%|做多平倉", message)
    strategy_1_short_open = re.search(r"做空開倉|做空入場", message)
    strategy_1_short_close = re.search(r"做空全部平倉|做空平倉\d\d%|做空平倉", message)
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
    
def side_inverter(side): #work for stop loss function
    if(side=="Sell"):
        return "Buy"
    elif(side=="Buy"):
        return "Sell"

def matching_positionSide(message):
    strategy_1_long_open = re.search(r"做多開倉|做多入場", message)
    strategy_1_long_close = re.search(r"做多全部平倉|做多平倉\d\d%|做多平倉", message)
    strategy_1_short_open = re.search(r"做空開倉|做空入場", message)
    strategy_1_short_close = re.search(r"做空全部平倉|做空平倉\d\d%|做空平倉", message)
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

def matching_symbol(message):  # defining it is BTC or ETH
    strategy_coin = re.search("btc/USDT", message)  # 只有ETH 或者BTC
    if (strategy_coin != None):
        return ("BTCUSDT")
    else:
        return ("ETHUSDT")

def matching_changingStopLoss(message): #To protect profit, changing the stop loss
    result=re.findall(r"提高止蝕價",message).__len__()
    
    if(result==0):
        return False
    elif(result>0):
        return True

def matching_roundingDecimal(message):
    if(matching_symbol(message)=="BTCUSDT"):
        return 3
    elif (matching_symbol(message)=="ETHUSDT"):
        return 2



def matching_price(message):
    changingStopLoss=matching_changingStopLoss(message)
    if(changingStopLoss==False):
        price= message.split('@',1)
        return(price[1]);
    elif(changingStopLoss==True):
        result=re.findall(r"@.*\uFF0C此",message)[0]
        result=result.split('@',1)
        result=result[1]
        result=result.split('\uFF0C',1)
        result=result[0]
        
        return result
    
def matching_closingSize(message):
    if(matching_changingStopLoss(message)):
        size=re.findall(r"《.*》",message)[0]
        size=size.split("倉",1)[1]
        size=size.split("%",1)[0]
        return int(size)/100
    else: 
        return 1
    
async def protectingPosition(message):
    symbol=matching_symbol(message)
    side=matching_side(message)
    positionSide=matching_positionSide(message)
    price=matching_price(message)
    price=round(float(price),2)
    stra=matching_strategy(message)
    current_order=strategy.strategy_getter(stra=stra,symbol=symbol)["result"]
    existing_qty=current_order["qty"]
    print(existing_qty)
    print(existing_qty*(matching_closingSize(message)))
    
    
    remainder=round(existing_qty-existing_qty*(matching_closingSize(message)),3)
    print(remainder)
    
    
    if(symbol=="BTCUSDT"):
        if(side=="Sell" and positionSide==1):
            bybit_session.set_trading_stop(
                                symbol=symbol,
                                side=side_inverter(side),
                                positionSide=positionSide,
                                stop_loss=(float(matching_price(message))- 300),
                                sl_size=remainder)
        elif(side=="Buy" and positionSide==2):
            bybit_session.set_trading_stop(
                                symbol=symbol,
                                side=side_inverter(side),
                                positionSide=positionSide,
                                stop_loss=(float(matching_price(message))+300),
                                sl_size=remainder)
    elif(symbol=="ETHUSDT"):
        if(side=="Sell" and positionSide==1):
            bybit_session.set_trading_stop(
                                symbol=symbol,
                                side=side_inverter(side),
                                positionSide=positionSide,
                                stop_loss=(float(matching_price(message))-50),
                                sl_size=remainder)
        elif(side=="Buy" and positionSide==2):
            bybit_session.set_trading_stop(
                                symbol=symbol,
                                side=side_inverter(side),
                                positionSide=positionSide,
                                stop_loss=(float(matching_price(message))+50),
                                sl_size=remainder)

async def getTheQuantity(ratio,price): #ration is the percentage of the balance
    balance=await bybit_getTheUSDTAmount()
    #balance=5000
    leverage=15; #fixed
    return (float(balance)*float(ratio)*float(leverage)/float(price));


async def bybit_getTheUSDTAmount():
    acc =  bybit_session.get_wallet_balance(coin="USDT",accountType="CONTRACT")
    
    USDT_balance=acc['result']['list'][0]['coin'][0]['walletBalance']#hard code to get the USDT balance
    
    return USDT_balance

     

async def bybit_createNewOrder(message):
    
    symbol=matching_symbol(message)
    side=matching_side(message)
    positionSide=matching_positionSide(message)
    price=matching_price(message)
    price=round(float(price),2)
    qty=round(await getTheQuantity(ratio=0.04,price=price),matching_roundingDecimal(message))
    stra=matching_strategy(message)

    #BUY LONG == 做多開倉
    #SELL SHORT ＝＝做空開倉
    #Sell Long == 做多平倉
    #Buy Short ＝＝做空平倉

    #1-LONG side of both side mode
    #2-SHORT side of both side mode SHORT
    if(side=="Sell" and positionSide==1): #checking whether it is closing action, This is 做多平倉
        try:
            response=await bybit_closingThePosition(stra=stra,symbol=symbol,side=side,positionSide=positionSide,message=message)
            bybit_API_logger.info(response)
              
        except:
            bybit_API_logger.exception(Exception) #logging the order exception
    elif(side=="Buy" and positionSide==2):#checking whether it is closing action, This is 做空平倉
        
        try:
            response=await bybit_closingThePosition(stra=stra,symbol=symbol,side=side,positionSide=positionSide,message=message)
            bybit_API_logger.info(response)
            
        except:
            bybit_API_logger.exception(Exception) #logging the order exception
            
    else:                              #If it is a opening signal, the below will try to open the position.
        try:
            bybit_API_logger.info('symbol:{} action: {} {} price: {} qty: {}'.format(symbol,side,positionSide,price,qty))
            order=bybit_session.place_order(
                category="linear",
                symbol=symbol,
                side=side,
                qty=qty,
                price=price,
                order_type="Limit",
                time_in_force="GTC",
                reduce_Only=False,
                close_on_trigger=False,
                position_idx=positionSide,
                
            )
            bybit_API_logger.info(order)
            
            strategy.strategy_setter(stra=stra,symbol=symbol,order=order)
            return order
        except:
            bybit_API_logger.exception(Exception) #logging the order exception

#return ture, if the current order is unfilled
async def bybit_unfilledOrderChecker(symbol,stra): 
    current_order=strategy.strategy_getter(stra=stra,symbol=symbol)["result"]
    the_unfilled_order=bybit_session.get_active_order(symbol=symbol,order_status="New")["result"]["data"]
    cancelling=False
    if(len(the_unfilled_order)>0): #check is any unfilled order exist, if yes,
        for order in the_unfilled_order:
            if(order["order_id"]==current_order["order_id"]):  #Checking whether the order have been filled, if not, just cancelled the order.
                cancelling=True
    return cancelling 

def positionChecker(stra,symbol):
    if(strategy.strategy_getter(stra=stra,symbol=symbol)=={}):
        bybit_API_logger.info("This position does not exist, there is nothing to close.")
        return {}
    else:
        return strategy.strategy_getter(stra=stra,symbol=symbol)["result"]

####TODO the ETH order would left some position behind


async def bybit_closingThePosition(stra,symbol,side,positionSide,message):
    significantFigures=matching_roundingDecimal(message)
    current_order=positionChecker(stra,symbol) #return {} when there is no position exist
    if(current_order!={}):
        cancelling=await bybit_unfilledOrderChecker(symbol=symbol,stra=stra) 

        existing_qty=current_order["qty"]
        remainder=round(existing_qty-round(existing_qty*(matching_closingSize(message)),significantFigures),significantFigures)
        if(cancelling==True): #The current order is unfilled, cancelled the order.
            response=bybit_session.cancel_active_order(symbol=symbol,order_id=current_order["order_id"])
            strategy.strategy_setter(stra=stra,symbol=symbol,order={}) #when the order have been cancelled, empty the order
            return response
        elif(cancelling==False):  #If the unfilled order list doesnt have the current order, assume it was filled
            
            changingStopLoss=matching_changingStopLoss(message)
            if(changingStopLoss==False): #Close all 100% position
                if(stra==2):
                    try:
                        bybit_session.set_trading_stop(
                                symbol=symbol,
                                side=side_inverter(side),
                                positionSide=positionSide,
                                stop_loss=0,
                                sl_size=existing_qty)
                        
                    except:
                        bybit_API_logger.exception(Exception)

                
                order=bybit_session.place_active_order(
                            symbol=symbol,
                            side=side,
                            qty=existing_qty,
                            order_type="Market",    #Using the Market type , and observating if there are any bugs
                            time_in_force="GoodTillCancel",
                            position_idx=positionSide,
                            reduce_Only=True,
                            close_on_trigger=True)
                
                strategy.strategy_setter(stra=stra,symbol=symbol,order={})#when the position have been closed, empty the order
                return order
            
            
            elif(changingStopLoss==True): ######################fixed the closing size is 60% manually
                remainder=round(existing_qty-round(existing_qty*(matching_closingSize(message)),significantFigures),significantFigures)
                order_qty=round(existing_qty*matching_closingSize(message),significantFigures)
                print("/////")
                print(order_qty)
                print(remainder)
                print("//////")
                
                #bybit_session.full_partial_position_tp_sl_switch(symbol=symbol,tp_sl_mode="Partial")
                if(matching_closingSize(message)==0.6):
                    bybit_session.set_trading_stop(
                                symbol=symbol,
                                side=side_inverter(side),
                                positionSide=positionSide,
                                stop_loss=current_order["price"],
                                sl_size=remainder)
                elif(matching_closingSize(message)==0.3):
                   try:
                       await protectingPosition(message)
                   except:
                       bybit_API_logger.exception(Exception)

                order=bybit_session.place_active_order(
                            symbol=symbol,
                            side=side,
                            qty=order_qty,
                            order_type="Market",    #Using the Market type , and observating if there are any bugs
                            time_in_force="GoodTillCancel",
                            position_idx=positionSide,
                            reduce_Only=True,
                            close_on_trigger=True
                            )
                
                order["result"]["qty"]=round(remainder,significantFigures) #update the reaminder qty of the order
                print("######")
                print(order["result"]["qty"])
                strategy.strategy_setter(stra=stra,symbol=symbol,order=order)
                return order
        
   

    

@client.on(events.NewMessage(chats=testing1,incoming=True))
async def my_event_helper(event):
    bybit_API_logger.info(event.raw_text) #logging in to log
   
    if(ignoring_noise(event.raw_text)):
        bybit_API_logger.error("noise message, already ignored")
        return None
    else:
        order= await bybit_createNewOrder(message=event.raw_text)
        

        


 
with client:
    client.run_until_disconnected()