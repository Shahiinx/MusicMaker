from config import API_ID, API_HASH, MONGO_DB_URL, user, call, logger, logger_mode, botname, GROUP as GROUPOWNER, CHANNEL as CHANNELOWNER, OWNER, OWNER_NAME, OWNER_ID, mo, moo, Bots, botdb, blockdb
from pymongo import MongoClient
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pyrogram.errors import SessionPasswordNeeded, FloodWait, RPCError
from motor.motor_asyncio import AsyncIOMotorClient
bot_name = moo.bot_name
channeldb = moo.ch
CHANNEL = {}
groupdb = moo.gr
GROUP = {}
channeldbsr = moo.chsr
CHANNELsr = {}
groupdbsr = moo.grsr
GROUPsr = {}
botss = Bots
dev = {} 
devname = {}
boot = {}
mustdb = moo.must
must = {}

async def setup_indexes(client):
    await Bots.create_index([("bot_username", 1)], unique=True)
    await blockdb.create_index([("user_id", 1)])
    userdb = await get_data(client)
    await userdb.users.create_index([("user_id", 1)], unique=True)
    chatsdb = await get_data(client)
    await chatsdb.chats.create_index([("chat_id", 1)], unique=True)
    
def is_valid_telegram_url(url: str) -> bool:
    return url.startswith("https://t.me/") or url.startswith("http://t.me/")

def extract_username_from_url(url: str) -> str:
    return url.replace("https://t.me/", "").replace("http://t.me/", "").strip("/")    
    
# Developer Id
async def get_dev(bot_username: str):
    if bot_username in dev:
        return dev[bot_username]

    bot_data = await botss.find_one({"bot_username": bot_username}, {"dev": 1})
    if bot_data:
        dev_id = bot_data["dev"]
        dev[bot_username] = dev_id
        return dev_id
    return None
    
async def get_dev_id(bot_username):
    if bot_username in dev:
        return str(dev[bot_username])

    bot_data = await botss.find_one({"bot_username": bot_username})
    if bot_data:
        dev_id = bot_data.get("dev_id", "")
        dev[bot_username] = dev_id
        return str(dev_id)
# Developer Name
async def get_dev_name(client: Client, bot_username: str):
    if bot_username in devname:
        return devname[bot_username]

    bot_data = await botss.find_one({"bot_username": bot_username}, {"dev": 1})
    if not bot_data:
        return None

    dev_id = bot_data["dev"]
    try:
        user_info = await client.get_chat(dev_id)
        first_name = user_info.first_name
        devname[bot_username] = first_name
        return first_name
    except:
        return None
# Bot Name
async def get_bot_name(bot_username: str):
    if bot_username in botname:
        return botname[bot_username]

    bot_data = await bot_name.find_one({"bot_username": bot_username}, {"bot_name": 1})
    if bot_data:
        bot_name_value = bot_data.get("bot_name", "بلاك")
        botname[bot_username] = bot_name_value
        return bot_name_value
    return "بلاك"

async def set_bot_name(bot_username: str, BOT_NAME: str):
    botname[bot_username] = BOT_NAME
    await bot_name.update_one({"bot_username": bot_username}, {"$set": {"bot_name": BOT_NAME}}, upsert=True)

# Bot group
async def get_group(bot_username: str):
    if bot_username in GROUP:
        return GROUP[bot_username]

    bot_data = await groupdb.find_one({"bot_username": bot_username}, {"group": 1})
    if bot_data:
        group = bot_data.get("group", GROUPOWNER)
        GROUP[bot_username] = group
        return group
    return GROUPOWNER

async def set_group(bot_username: str, group: str):
    GROUP[bot_username] = group
    await groupdb.update_one({"bot_username": bot_username}, {"$set": {"group": group}}, upsert=True)

# Bot channel
async def get_channel(bot_username: str):
    if bot_username in CHANNEL:
        return CHANNEL[bot_username]

    bot_data = await channeldb.find_one({"bot_username": bot_username}, {"channel": 1})
    if bot_data:
        channel = bot_data.get("channel", CHANNELOWNER)
        CHANNEL[bot_username] = channel
        return channel
    return CHANNELOWNER

async def set_channel(bot_username: str, channel: str):
    CHANNEL[bot_username] = channel
    await channeldb.update_one({"bot_username": bot_username}, {"$set": {"channel": channel}}, upsert=True)
# sr group
async def get_groupsr(bot_username: str):
    if bot_username in GROUPsr:
        return GROUPsr[bot_username]

    bot_data = await groupdbsr.find_one({"bot_username": bot_username}, {"groupsr": 1})
    if bot_data:
        groupsr = bot_data.get("groupsr", GROUPOWNER)
        GROUPsr[bot_username] = groupsr
        return groupsr
    return GROUPOWNER

async def set_groupsr(bot_username: str, groupsr: str):
    GROUPsr[bot_username] = groupsr
    await groupdbsr.update_one({"bot_username": bot_username}, {"$set": {"groupsr": groupsr}}, upsert=True)
# sr channel
async def get_channelsr(bot_username: str):
    if bot_username in CHANNELsr:
        return CHANNELsr[bot_username]

    bot_data = await channeldbsr.find_one({"bot_username": bot_username}, {"channelsr": 1})
    if bot_data:
        channelsr = bot_data.get("channelsr", CHANNELOWNER)
        CHANNELsr[bot_username] = channelsr
        return channelsr
    return CHANNELOWNER
    
async def set_channelsr(bot_username: str, channelsr: str):
    CHANNELsr[bot_username] = channelsr
    await channeldbsr.update_one({"bot_username": bot_username}, {"$set": {"channelsr": channelsr}}, upsert=True)

@Client.on_message(filters.command("❲ تعيين قناة البوت ❳", ""))
async def set_botch(client: Client, message):
    user_id = message.from_user.id  
    dev = await get_dev(client.me.username) 
    if message.chat.id == dev or user_id in OWNER_ID:
        NAME = await client.ask(message.chat.id, "**≭︰ارسل رابط القناة**", filters=filters.text)
        channel_url = NAME.text.strip()

        if not is_valid_telegram_url(channel_url):
            await message.reply_text("✘ الرابط غير صالح، يجب أن يبدأ بـ https://t.me/")
            return

        username = extract_username_from_url(channel_url)
        try:
            chat = await client.get_chat(username)
            if chat.type.name != "CHANNEL":
                raise ValueError
        except Exception:
            await message.reply_text("✘ لم أتمكن من العثور على هذه القناة. تأكد أن الرابط صحيح وأن البوت عضو فيها.")
            return

        bot_username = client.me.username
        await set_channel(bot_username, channel_url)
        await message.reply_text("**≭︰تم حفظ القناة**")

@Client.on_message(filters.command("❲ تعيين مجموعه البوت ❳", ""))
async def set_botgr(client: Client, message):
    user_id = message.from_user.id  
    dev = await get_dev(client.me.username) 
    if message.chat.id == dev or user_id in OWNER_ID:
        NAME = await client.ask(message.chat.id, "≭︰ارسل رابط المجموعه", filters=filters.text)
        group_url = NAME.text.strip()

        if not is_valid_telegram_url(group_url):
            await message.reply_text("✘ الرابط غير صالح، يجب أن يبدأ بـ https://t.me/")
            return

        username = extract_username_from_url(group_url)
        try:
            chat = await client.get_chat(username)
            if chat.type.name not in ["GROUP", "SUPERGROUP"]:
                raise ValueError
        except Exception:
            await message.reply_text("✘ لم أتمكن من العثور على هذه المجموعة. تأكد أن الرابط صحيح وأن البوت عضو فيها.")
            return

        bot_username = client.me.username
        await set_group(bot_username, group_url)
        await message.reply_text("**≭︰تم حفظ المجموعه**")
   
@Client.on_message(filters.command("❲ تعيين قناة السورس ❳", ""))
async def set_botchsr(client: Client, message):
  user_id = message.from_user.id  
  if message.from_user.id in OWNER_ID:
   NAME = await client.ask(message.chat.id, "≭︰ارسل رابط القناة", filters=filters.text)
   channelsr = NAME.text
   bot_username = client.me.username
   await set_channelsr(bot_username, channelsr)
   await message.reply_text("**≭︰تم حفظ قناة السورس**")
   return
   
@Client.on_message(filters.command("❲ تعيين مجموعة السورس ❳", ""))
async def set_botgrsr(client: Client, message):
  user_id = message.from_user.id  
  if message.from_user.id in OWNER_ID:
   NAME = await client.ask(message.chat.id, "≭︰ارسل رابط المجموعه", filters=filters.text)
   groupsr = NAME.text
   bot_username = client.me.username
   await set_groupsr(bot_username, groupsr)
   await message.reply_text("**≭︰تم حفظ المجموعه**")
   return

mongo_client = None

async def get_data(client):
    global mongo_client
    if not mongo_client:
        mongo_client = AsyncIOMotorClient(MONGO_DB_URL)  
    bot_username = client.me.username
    return mongo_client[bot_username]

async def get_userbot(bot_username: str):
    if bot_username in user:
        userbot = user[bot_username]
        try:
            await userbot.get_me()
            return userbot
        except (SessionPasswordNeeded, FloodWait, RPCError) as e:
            del user[bot_username]
            print(f"تمت إزالة الجلسة غير الصالحة للبوت: {bot_username}")
    bot_data = await botss.find_one({"bot_username": bot_username})
    if bot_data:
        session = bot_data["session"]
        try:
            userbot = Client("Source", api_id=API_ID, api_hash=API_HASH, session_string=session)
            await userbot.get_me()
            user[bot_username] = userbot
            print(f"تم تحميل الجلسة بنجاح للبوت: {bot_username}")
            return userbot
        except Exception as e:
            print(f"حدث خطأ أثناء تحميل الجلسة للبوت {bot_username}: {e}")
            return None
    
    print(f"لم يتم العثور على بيانات للبوت: {bot_username}")
    return None

async def get_call(bot_username: str):
    if bot_username in call:
        return call[bot_username]

    bot_data = await botss.find_one({"bot_username": bot_username})
    userbot = await get_userbot(bot_username)
    if userbot:
        callo = PyTgCalls(userbot, cache_duration=100)
        await callo.start()
        call[bot_username] = callo
        return callo
    return None

async def get_app(bot_username: str):
    if bot_username in boot:
        return boot[bot_username]

    bot_data = await botss.find_one({"bot_username": bot_username})
    if bot_data:
        token = bot_data["token"]
        app = Client("Source", api_id=API_ID, api_hash=API_HASH, bot_token=token, plugins=dict(root="Source"))
        boot[bot_username] = app
        return app
    return None
    
async def get_logger(bot_username: str):
    if bot_username in logger:
        return logger[bot_username]

    bot_data = await botss.find_one({"bot_username": bot_username})
    if bot_data:
        logger_value = bot_data.get("logger", None)
        logger[bot_username] = logger_value
        return logger_value
    return None
    
async def get_logger_mode(bot_username: str):
    if bot_username in logger_mode:
        return logger_mode[bot_username]

    bot_data = await botss.find_one({"bot_username": bot_username})
    if bot_data:
        logger_mode_value = bot_data.get("logger_mode", None)
        logger_mode[bot_username] = logger_mode_value
        return logger_mode_value
    return None
    
async def must_join(bot_username: str):
    if bot_username in must:
        return must[bot_username]

    bot_data = await mustdb.find_one({"bot_username": bot_username})
    if bot_data:
        must_value = bot_data.get("getmust", "معطل")
        must[bot_username] = must_value
        return must_value
    return "معطل"

#async def set_must(bot_username: str, m: str):
#    must_value = "مفعل" if m != "❲ تعطيل الاشتراك الإجباري ❳" else "معطل"
#    must[bot_username] = must_value
#    await mustdb.update_one({"bot_username": bot_username}, {"$set": {"getmust": must_value}}, upsert=True)

async def set_must(bot_username: str, m: str):
    # إصلاح المنطق المعكوس
    must_value = "مفعل" if m == "❲ تفعيل الاشتراك الإجباري ❳" else "معطل"
    must[bot_username] = must_value
    await mustdb.update_one(
        {"bot_username": bot_username}, 
        {"$set": {"getmust": must_value}}, 
        upsert=True
    )

            
@Client.on_message(filters.command(["❲ تعطيل الاشتراك الإجباري ❳", "❲ تفعيل الاشتراك الإجباري ❳"], ""))
async def set_join_must(client: Client, message):
    user_id = message.from_user.id  
    dev = await get_dev(client.me.username) 
    if message.chat.id == dev or message.from_user.id in OWNER_ID:
        bot_username = client.me.username
        m = message.command[0]
        await set_must(bot_username, m)
        if message.command[0] == "❲ تعطيل الاشتراك الإجباري ❳":
            await message.reply_text("**≭︰تم تعطيل الاشتراك الاجباري**")
        else:
            await message.reply_text("**≭︰تم تفعيل الاشتراك الاجباري**")
        return