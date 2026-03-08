# from pyrogram import idle
from pytgcalls import idle
import asyncio
from config import API_HASH, API_ID, BOT_TOKEN, OWNER
from pyrogram import Client
from pyromod import listen
from Source.Data import setup_indexes

bot = Client(
    "Shahin",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="Maker")
)

async def start_bot():
        print("[INFO]: جاري تشغيل البوت")
        await bot.start()
        await setup_indexes(bot)
        await bot.send_message(OWNER[0], "**≭︰تم تشغيل مصنع **") 
        print("[INFO]: بدأ تشغيل المصنع بنجاح")
        await idle()
        
loop = asyncio.get_event_loop()
loop.run_until_complete(start_bot())
