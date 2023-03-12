from telethon.sync import TelegramClient, events
from telethon.tl.types import *
import init

api=init

client = TelegramClient('googleCloudServer3', api.telegram_api_id,api.telegram_api_hash )
client.start()

kosirBitcoin = -1001681322568
kosirBitcoinPaid= -1001763853057
DQ_channel = -1001347867469
testing1 =-835623858
testing2 =-873060948


@client.on(events.NewMessage(chats=kosirBitcoinPaid,incoming=True))
async def my_event_helper(event):
    await client.forward_messages(952653251, event.message)
        


with client:
    client.run_until_disconnected()