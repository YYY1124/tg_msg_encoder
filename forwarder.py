from telethon.sync import TelegramClient, events
from telethon.tl.types import *
import init

api=init

client = TelegramClient('macTesting', api.telegram_api_id,api.telegram_api_hash )
client.start()

kosirBitcoin = -1001681322568
kosirBitcoinPaid= -1001763853057
DQ_channel = -1001347867469
testing1 =-835623858
testing2 =-873060948
tommy =952653251
testing_channel=-1001917173201


@client.on(events.NewMessage(chats=kosirBitcoinPaid,incoming=True))
async def my_event_helper(event):
    try:
        await client.forward_messages(tommy, event.message)
    except:
        print(Exception)
        
        


with client:
    client.run_until_disconnected()