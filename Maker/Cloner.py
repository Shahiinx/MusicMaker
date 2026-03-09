from pyrogram import filters, Client
from pyrogram import Client as app
from pyromod import listen
from config import API_ID, API_HASH, MONGO_DB_URL,  user as usr, helper as ass, call, appp, OWNER, OWNER_ID, OWNER_NAME, CHANNEL, GROUP, PHOTO, VIDEO
from Source.info import Call, activecall, helper, active
from Source.Data import dev, devname, set_must
from pyrogram.raw.types import InputPeerChannel
from pyrogram.raw.functions.phone import CreateGroupCall
from pytgcalls import PyTgCalls
from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, Message, ChatPrivileges
from pyrogram.enums import ChatType
import sys
import asyncio
import os
import requests
import re
import logging

mo = AsyncIOMotorClient(MONGO_DB_URL)
moo = mo["data"] 
Bots = moo.yousef  
db = moo  
botdb = db.botdb 
blockdb = db.blocked  
Done = []
OFF =True
developers = set()  

async def auto_bot():
    count = 0
    async for i in Bots.find({}):
        bot_username = i["bot_username"]
        try:
            if bot_username not in Done:
                TOKEN = i["token"]
                SESSION = i["session"]
                devo = i["dev"]
                Done.append(bot_username)
                logger = i["logger"]
                
                bot = Client("Source", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN, in_memory=True, plugins=dict(root="Source"))
                user = Client("Source", api_id=API_ID, api_hash=API_HASH, session_string=SESSION, in_memory=True)
                
                await bot.start()
                await user.start()
                
                appp[bot_username] = bot
                usr[bot_username] = user
                activecall[bot_username] = []
                dev[bot_username] = devo
                
                try:
                    devo_chat = await bot.get_chat(devo)
                    devname[bot_username] = devo_chat.first_name
                except:
                    devname[bot_username] = OWNER_NAME
                
                ass[bot_username] = []
                await helper(bot_username)
                await Call(bot_username)
        except Exception as e:
            print(f"[ @{bot_username} ] {e}")

# Bot Arledy Maked

# Served Bots
async def get_users(chatsdb) -> list:
    return [chat async for chat in chatsdb.find({"user_id": {"$gt": 0}})]

async def get_chats(chatsdb) -> list:
    return [chat async for chat in chatsdb.find({"chat_id": {"$lt": 0}})]    
    
    
async def get_served_bots() -> list:
    chats_list = []
    async for chat in botdb.find({"bot_username": {"$exists": True}}):  
        chats_list.append(chat)
    return chats_list

async def is_served_bot(bot_username: int) -> bool:
    chat = await botdb.find_one({"bot_username": bot_username})
    return bool(chat) 

async def add_served_bot(bot_username: int):
    is_served = await is_served_bot(bot_username)
    if is_served:
        return
    return await botdb.insert_one({"bot_username": bot_username})  

async def del_served_bot(bot_username: int):
    is_served = await is_served_bot(bot_username)
    if not is_served:
        return
    return await botdb.delete_one({"bot_username": bot_username})  

# Blocked Users

async def get_block_users() -> list:
    chats_list = []
    async for chat in blockdb.find({}):
        chats_list.append(chat)
    return chats_list

async def is_block_user(user_id: int) -> bool:
    return bool(await blockdb.find_one({"user_id": user_id}))

async def add_block_user(user_id: int):
    if await is_block_user(user_id):
        return
    return await blockdb.insert_one({"user_id": user_id})

async def del_block_user(user_id: int):
    if not await is_block_user(user_id):
        return
    return await blockdb.delete_one({"user_id": user_id})

@app.on_message(filters.private)
async def botooott(client, message):
    try:
        user_id = message.from_user.id
        if (
            message.chat.username not in OWNER
            and user_id not in OWNER_ID
            and str(user_id) not in developers
            and user_id != client.me.id
        ):
            await client.forward_messages(OWNER[0], message.chat.id, message.id)

    except Exception:
        pass

    message.continue_propagation()

@app.on_message(filters.command("❲ تحديث الصانع ❳", ""))
async def update(client, message):
    if message.from_user.id in OWNER_ID:
        try:
            msg = await message.reply_text("**≭︰جاري تحديث الصانع .**", quote=True)
            args = [sys.executable, "main.py"]
            environ = os.environ
            os.execle(sys.executable, *args, environ)
        except Exception as e:
            await message.reply_text(f"فشل تحديث الصانع: {e}", quote=True)
    else:
        await message.reply_text("**≭︰هذا الأمر مخصص لمطوري السورس فقط .**", quote=True)

@app.on_message(filters.command("❲ تشغيل البوتات ❳", ""))
async def turnon(client, message):
    if message.from_user.id in OWNER_ID or str(message.from_user.id) in developers:
        m = await message.reply_text("**≭︰انتظر قليلا ... **")
        try:
            await auto_bot()
            await m.edit_text("**≭︰تم تشغيل جميع البوتات المصنوعه**")
        except Exception as e:
            await m.edit_text(f"**حدث خطأ أثناء تشغيل البوتات:**\n`{e}`")

@app.on_message(filters.command(["❲ تفعيل التنصيب ❳", "❲ تعطيل التنصيب ❳"], ""))
async def bye(client, message):
    user = message.from_user.username
    if message.from_user.id in OWNER_ID or str(message.from_user.id) in developers:
        global OFF
        text = message.text
        if text == "❲ تفعيل التنصيب ❳":
            OFF = None
            await message.reply_text("**≭︰تم تفعيل التنصيب المجاني**")
            return
        if text == "❲ تعطيل التنصيب ❳":
            OFF = True
            await message.reply_text("**≭︰تم تعطيل التنصيب المجاني**")
            return

@app.on_message(filters.command("start") & filters.private)
async def stratmaked(client, message):
    if await is_block_user(message.from_user.id):
        return
    if OFF:
        if message.from_user.id not in OWNER_ID and str(message.from_user.id) not in developers:
            return await message.reply_text(f"**≭︰التنصيب المجاني معطل راسل المبرمج ↫ @{OWNER[0]}**")
    if message.from_user.id in OWNER_ID or str(message.from_user.id) in developers:
        kep = ReplyKeyboardMarkup([
            ["❲ حذف بوت ❳", "❲ صنع بوت ❳"],
            ["❲ تعطيل التنصيب ❳", "❲ تفعيل التنصيب ❳"],
            ["❲ تشغيل البوتات ❳", "❲ تحديث الصانع ❳"],
            ["❲ البوتات المصنوعه ❳", "❲ احصائيات البوتات ❳"],
            ["❲ فلتره البوتات ❳", "❲ فحص البوتات ❳"],
            ["❲ الاسكرينات المفتوحه ❳"],
            ["❲ رفع مطور ❳", "❲ تنزيل مطور ❳"],
            ["❲ المطورين ❳"],
            ["❲ حظر بوت ❳", "❲ حظر مستخدم ❳"],
            ["❲ الغاء حظر بوت ❳", "❲ الغاء حظر مستخدم ❳"],
            ["❲ اذاعه للمطورين ❳", "❲ المكالمات النشطه ❳"],
            ["❲ توجيه عام بجميع البوتات ❳", "❲ اذاعه عام بجميع البوتات ❳"],
            ["❲ 𝚄𝙿𝙳𝙰𝚃𝙴 𝙲𝙾𝙾𝙺𝙸𝙴𝚂 ❳", "❲ 𝚁𝙴𝚂𝚃𝙰𝚁𝚃 𝙲𝙾𝙾𝙺𝙸𝙴𝚂 ❳"],
            ["استخراج جلسه"],
        ], resize_keyboard=True)
        await message.reply_text(f"**≯︰اهلا بك عزيزي المطور**", reply_markup=kep)
    else:
        kep = ReplyKeyboardMarkup([
            ["❲ حذف بوت ❳", "❲ صنع بوت ❳"],
            ["❲ مطور السورس ❳", "❲ السورس ❳"],
            ["استخراج جلسه"],
        ], resize_keyboard=True)
        await message.reply_text(
            f"**≯︰مرحبا بك ❲ {message.from_user.mention} ❳**\n"
            f"**≯︰اليك كيب المصنع **", reply_markup=kep
        )
    
@app.on_message(filters.command(["❲ السورس ❳"], ""))
async def alivehi(client: Client, message):
    chat_id = message.chat.id

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("❲ Help Group ❳", url=f"{GROUP}"),
                InlineKeyboardButton("❲ Source Ch ❳", url=f"{CHANNEL}"),
            ],
            [
                 InlineKeyboardButton(f"{OWNER_NAME}", url=f"https://t.me/{OWNER[0]}")
            ]
        ]
    )

    await message.reply_video(
        video=VIDEO,
        caption="≭︰Welcome to Source Music Source",
        reply_markup=keyboard,
    )

@app.on_message(filters.command("❲ المكالمات النشطه ❳", ""))
async def achgs(client, message):
  nn = len(active)
  await message.reply_text(f"**- عدد المكالمات النشطه الان {nn}**")
      
@app.on_message(filters.command(["❲ صنع بوت ❳"], ""))
async def cloner(app: app, message):
    if await is_block_user(message.from_user.id):
        return

    if OFF:
        if not message.from_user.id in OWNER_ID and str(message.from_user.id) not in developers:
            return await message.reply_text(f"**≭︰التنصيب المجاني معطل، راسل المبرمج ↫ @{OWNER[0]}**")

    await message.reply_text("**انتظر قليلاً**")
    user_id = message.from_user.id

    try:
        tokenn = await app.ask(chat_id=user_id, text="**≭︰ارسل توكن البوت**", filters=filters.text)
        token = tokenn.text
        await tokenn.reply_text("**جاري فحص التوكن**")

        bot = Client("Cloner", api_id=API_ID, api_hash=API_HASH, bot_token=token, in_memory=True)
        await bot.start()
    except Exception as e:
        return await message.reply_text(f"**≭{e}︰التوكن غير صحيح**")

    bot_i = await bot.get_me()
    bot_username = bot_i.username

    if await is_served_bot(bot_username):
        await bot.stop()
        return await message.reply_text("**≭︰جرب توكن آخر، هذا البوت مسجل من قبل**")

    if bot_username in Done:
        await bot.stop()
        return await message.reply_text("**≭︰تم تنصيب بوت في هذا التوكن سابقاً**")

    try:
        session_msg = await app.ask(chat_id=user_id, text="**≭︰حسنًا، أرسل كود الجلسة**\n≭︰استخرجه من هذا البوت ↫ @", filters=filters.text)
        session = session_msg.text
        await app.send_message(user_id, "**جاري فحص الجلسه**")

        user = Client("Source", api_id=API_ID, api_hash=API_HASH, session_string=session, in_memory=True)
        await user.start()
    except:
        await bot.stop()
        return await message.reply_text("**≭︰كود الجلسة غير صحيح**")

    loger = await user.create_supergroup("مجموعه البوت", "مجموعة سجل اشعارات البوت")
    if bot_i.photo:
        photo = await bot.download_media(bot_i.photo.big_file_id)
        await user.set_chat_photo(chat_id=loger.id, photo=photo)

    logger = loger.id
    await user.add_chat_members(logger, bot_username)
    await user.promote_chat_member(logger, bot_username, privileges=ChatPrivileges(
        can_change_info=True,
        can_invite_users=True,
        can_delete_messages=True,
        can_restrict_members=True,
        can_pin_messages=True,
        can_promote_members=True,
        can_manage_chat=True,
        can_manage_video_chats=True
    ))
    loggerlink = await user.export_chat_invite_link(logger)

    await user.stop()
    await bot.stop()

    if message.from_user.id in OWNER_ID or str(message.from_user.id) in developers:
        dev = await app.ask(user_id, "**≭︰أرسل آيدي مطور البوت**")
        dev = user_id if dev.text == "انا" else int(dev.text)
    else:
        dev = user_id

    data = {
        "bot_username": bot_username,
        "token": token,
        "session": session,
        "dev": dev,
        "logger": logger,
        "logger_mode": "ON"
    }

    await Bots.insert_one(data)

    try:
        await auto_bot()
    except:
        pass

    await message.reply_text(
        f"**≭︰تم تشغيل البوت ↫ @{bot_username}\n≭︰توكن البوت ↯\n{token}\n\n**"
        f"**≭︰كود جلسة بايروغرام ↯\n{session}\n\n≭︰مجموعة الاشعارات ↯\n[ {loggerlink} ]**",
        disable_web_page_preview=True
    )

    await app.send_message(
        OWNER[0],
        f"**≭︰تنصيب جديد\n\n≭︰الصانع ↫ {message.from_user.mention}\n**"
        f"**≭︰معرف البوت ↫ @{bot_username}\n≭︰توكن البوت ↯\n{token}\n\n**"
        f"**≭︰كود جلسة بايروغرام ↯\n{session}\n\n≭︰مجموعة الاشعارات ↯\n[ {loggerlink} ]**"
    )

@app.on_message(filters.command(["❲ حذف بوت ❳"], ""))
async def delbot(client: app, message):
    if await is_block_user(message.from_user.id):
        return
    if OFF:
        if message.from_user.id not in OWNER_ID and str(message.from_user.id) not in developers:
            return await message.reply_text(f"**≭︰التنصيب المجاني معطل راسل المبرمج ↫ @{OWNER[0]}**")
    if message.from_user.id in OWNER_ID or str(message.from_user.id) in developers:
        ask = await client.ask(message.chat.id, "≭︰ارسل معرف البوت لحذفه", timeout=20)
        bot_username = ask.text
        if "@" in bot_username:
            bot_username = bot_username.replace("@", "")
        bot_exists = False
        async for bot in Bots.find({}): 
            if bot["bot_username"] == bot_username:
                bot_exists = True
                break
        if not bot_exists:
            return await message.reply_text("**≭︰لم يتم صنع البوت**")
        try:
            bb = {"bot_username": bot_username}
            await Bots.delete_one(bb)  
            try:
                Done.remove(bot_username)
            except:
                pass
            try:
                boot = appp[bot_username]
                await boot.stop()
            except:
                pass
            await message.reply_text("**≭︰تم حذف البوت**")
        except Exception as es:
            await message.reply_text(f"**≭︰حدث خطأ **\n**{es}**")
    else:
        bots_made = []
        async for bot in Bots.find({}): 
            if bot.get("dev") == message.chat.id:
                bots_made.append(bot["bot_username"])

        if bot_username not in bots_made:
            return await message.reply_text("**≭︰لم تقم بصنع بوت**")
        try:
            dev = message.chat.id
            dev_data = {"dev": dev}
            await Bots.delete_one(dev_data) 
            await message.reply_text("**≭︰تم حذف بوتك**")
        except Exception as es:
            await message.reply_text(f"**≭︰حدث خطأ **\n**{es}**")
            
@app.on_message(filters.command("❲ البوتات المصنوعه ❳", ""))
async def botsmaked(client, message):
    if message.from_user.id in OWNER_ID or str(message.from_user.id) in developers:
        text = "**≭︰البوتات المصنوعه**"
        b = 0
        async for i in Bots.find({}):  
            try:
                bot_username = i["bot_username"]
                b += 1
                text += f"\n{b}- @{bot_username}"
            except Exception as es:
                print(es)
        
        if b == 0:
            await message.reply_text("**لا يوجد بوتات مصنوعه حالياً.**")
        else:
            text += f"\n\n**≭︰عدد البوتات المصنوعه ↫ ❲ {b} ❳ **"
            await message.reply_text(text)

@app.on_message(filters.command(["❲ حظر بوت ❳", "❲ حظر مستخدم ❳", "❲ الغاء حظر بوت ❳", "❲ الغاء حظر مستخدم ❳"], ""))
async def blockk(client: app, message):
    if message.from_user.id in OWNER_ID or str(message.from_user.id) in developers:
        ask = await client.ask(message.chat.id, "**≭︰ارسل المعرف**", timeout=10)
        if ask.text == "الغاء":
            return await ask.reply_text("**≭︰تم الغاء الامر**")
        i = ask.text
        if "@" in i:
            i = i.replace("@", "")
        if message.command[0] == "❲ حظر بوت ❳" or message.command[0] == "❲ الغاء حظر بوت ❳":
            bot_username = i
            if await is_served_bot(bot_username):
                if message.command[0] == "❲ الغاء حظر بوت ❳":
                    await del_served_bot(bot_username)
                    return await ask.reply_text("**≭︰تم الغاء حظر البوت**")
                else:
                    return await ask.reply_text("**≭︰تم حظر البوت فعلا**")
            else:
                if message.command[0] == "❲ الغاء حظر بوت ❳":
                    return await ask.reply_text("**≭︰تم حظر البوت فعلا**")
                await add_served_bot(bot_username)
                try:
                    Done.remove(bot_username)
                    boot = appp[bot_username]
                    await boot.stop()
                    user = usr[bot_username]
                    await user.stop()
                except Exception as e:
                    print(f"Error while stopping bot: {e}")
                return await ask.reply_text("**≭︰تم حظر البوت**")
        else:
            try:
                user_id = int(i)
                if await is_block_user(user_id):
                    if message.command[0] == "❲ الغاء حظر مستخدم ❳":
                        await del_block_user(user_id)
                        return await ask.reply_text("**≭︰تم الغاء حظر المستخدم من المصنع**")
                    return await ask.reply_text("**≭︰المستخدم غير محظور**")
                else:
                    if message.command[0] == "❲ حظر مستخدم ❳":
                        return await ask.reply_text("**≭︰المستخدم محظور بالفعل**")
                    await add_block_user(user_id)
                    return await ask.reply_text("**≭︰تم حظر المستخدم**")
            except ValueError:
                return await ask.reply_text("**≭︰الرجاء إرسال معرف صحيح للمستخدم أو البوت**")
            except Exception as e:
                print(f"Error while processing user: {e}")
                return await ask.reply_text("**≭︰حدث خطأ أثناء معالجة المعرف**")
   
@app.on_message(filters.command(["❲ توجيه عام بجميع البوتات ❳", "❲ اذاعه عام بجميع البوتات ❳"], ""))
async def casttoall(client: app, message):
    if message.from_user.id in OWNER_ID or str(message.from_user.id) in developers:
        sss = "التوجيه" if message.command[0] == "❲ توجيه عام بجميع البوتات ❳" else "الاذاعه"
        ask = await client.ask(message.chat.id, f"**≭︰ارسل لي {sss} **", timeout=30)
        x = ask.id
        y = message.chat.id
        if ask.text == "الغاء":
            return await ask.reply_text("≭︰تم الغاء الامر")
        
        pn = await client.ask(message.chat.id, "≭︰هل تريد تثبيت الاذاعه\n≭︰ارسل ❲ نعم ❳ او ❲ لا ❳", timeout=10)
        h = await message.reply_text("**≭︰انتظر لحين انتهاء الاذاعه**")
        
        b = 0
        s = 0
        c = 0
        u = 0
        sc = 0
        su = 0
        
        async for bott in Bots.find({}): 
            try:
                b += 1
                s += 1
                bot_username = bott["bot_username"]
                session = bott["session"]
                bot = appp[bot_username]
                user = usr[bot_username]
                db = mo[bot_username]
                chatsdb = db.chats
                chats = await get_chats(chatsdb)
                usersdb = db.users
                users = await get_users(usersdb)
                all = []
                for i in users:
                    all.append(int(i["user_id"]))
                for i in chats:
                    all.append(int(i["chat_id"]))
                
                for i in all:
                    if message.command[0] == "❲ توجيه عام بجميع البوتات ❳":
                        try:
                            m = await bot.forward_messages(i, y, x)
                            if m.chat.type == ChatType.PRIVATE:
                                u += 1
                            else:
                                c += 1
                            if pn.text == "نعم":
                                try:
                                    await m.pin(disable_notification=False)
                                except:
                                    continue
                        except FloodWait as e:
                            flood_time = int(e.value)
                            if flood_time > 200:
                                continue
                            await asyncio.sleep(flood_time)
                        except Exception as e:
                            continue
                    else:
                        try:
                            m = await bot.send_message(chat_id=i, text=ask.text)
                            if m.chat.type == ChatType.PRIVATE:
                                u += 1
                            else:
                                c += 1
                            if pn.text == "نعم":
                                await m.pin(disable_notification=False)
                        except FloodWait as e:
                            flood_time = int(e.value)
                            if flood_time > 200:
                                continue
                            await asyncio.sleep(flood_time)
                        except Exception as e:
                            continue
                
                async for i in user.get_dialogs():
                    chat_id = i.chat.id
                    if message.command[0] == "❲ توجيه عام بجميع البوتات ❳":
                        try:
                            m = await user.forward_messages(i, y, x)
                            if m.chat.type == ChatType.PRIVATE:
                                su += 1
                            else:
                                sc += 1
                            if pn.text == "نعم":
                                await m.pin(disable_notification=False)
                        except FloodWait as e:
                            flood_time = int(e.value)
                            if flood_time > 200:
                                continue
                            await asyncio.sleep(flood_time)
                        except Exception as e:
                            continue
                    else:
                        try:
                            m = await user.send_message(chat_id, ask.text)
                            if m.chat.type == ChatType.PRIVATE:
                                su += 1
                            else:
                                sc += 1
                            if pn.text == "نعم":
                                await m.pin(disable_notification=False)
                        except FloodWait as e:
                            flood_time = int(e.value)
                            if flood_time > 200:
                                continue
                            await asyncio.sleep(flood_time)
                        except Exception as e:
                            continue
            except Exception as es:
                print(es)
                await message.reply_text(es)
        
        try:
            await message.reply_text(f"**≭︰تم الاذاعه في جميع البوتات**\n**≭︰تم الاذاعه في ↫❲ {b} ❳ مصنوع**\n**≭︰اذيعت الى ❲ {c} ❳ مجموعة ❲ {u} ❳ مستخدم**\n**≭︰تم الاذاعه في ↫❲ {s} ❳ مساعد**\n**≭︰اذيعت الى ❲ {sc} ❳ مجموعة ❲ {su} ❳ مستخدم**")
        except Exception as es:
            await message.reply_text(es)

@app.on_message(filters.command(["❲ اذاعه للمطورين ❳"], ""))
async def cast_dev(client, message):
    if message.from_user.id in OWNER_ID or str(message.from_user.id) in developers:
        ask = await client.ask(message.chat.id, "**≭︰ارسل لي المراد اذاعته**", timeout=30)
        if ask.text == "الغاء":
            return await ask.reply_text("≭︰تم الغاء الامر")

        d = 0
        f = 0

        async for i in Bots.find({}):  
            try:
                dev = i["dev"]
                bot_username = i["bot_username"]
                bot = appp[bot_username]
                try: 
                    await bot.send_message(dev, ask.text)
                    d += 1
                except Exception as es:
                    print(es)
                    f += 1
            except Exception:
                f += 1

        return await ask.reply_text(f"**≭︰نجح الارسال الى ❲ {d} ❳ مطور\n**≭︰فشل الارسال الى ❲ {f} ❳ مطور**")

@app.on_message(filters.command("❲ احصائيات البوتات ❳", ""))
async def botstatus(client, message):
    if message.from_user.id in OWNER_ID or str(message.from_user.id) in developers:
        m = 0
        d = 0
        u = 0
        text = ""
        
        try:
            async for i in Bots.find({}):  
                try:
                    bot_username = i["bot_username"]
                    database = mo[bot_username]
                    chatsdb = database.chats
                    chat = len(await get_chats(chatsdb))
                    m += chat
                    chatsdb = database.users
                    chat = len(await get_users(chatsdb))
                    u += chat
                    d += 1
                except Exception as e:
                    print(e)
        except:
            return await message.reply_text("**≭︰لا يوجد بوتات مصنوعه**")
        
        try:
            await message.reply_text(f"**≭︰عدد البوتات ↫❲ {d} ❳**\n\n**≭︰جميع المجموعات ↫❲ {m} ❳**\n**≭︰جميع المشتركين ↫❲  {u} ❳**")
        except:
            await message.reply_text("**≭︰لا يوجد بوتات مصنوعه**")
 
 
@app.on_message(filters.command(["❲ فحص البوتات ❳"], ""))
async def testbots(client, message):
    if message.from_user.id in OWNER_ID or str(message.from_user.id) in developers:
        text = "≭︰احصائيات البوتات"
        b = 0
        async for i in Bots.find({}):  
            try:
                bot_username = i["bot_username"]
                database = mo[bot_username]
                chatsdb = database.chats
                g = len(await get_chats(chatsdb))
                b += 1
                text += f"\n**{b}- @{bot_username} ، Group ↬ {g}**"
            except Exception as es:
                print(es)
        await message.reply_text(text)



@app.on_message(filters.command(["❲ فلتره البوتات ❳"], ""))
async def checkbot(client: app, message):
    if message.from_user.id in OWNER_ID or str(message.from_user.id) in developers:
        ask = await client.ask(message.chat.id, "**≭︰ارسل الحد الادنى للاحصائيات**", timeout=30)
        if ask.text == "الغاء":
            return await ask.reply_text("≭︰تم الغاء الامر")

        try:
            m = int(ask.text)
        except ValueError:
            return await ask.reply_text("≭︰يجب أن يكون رقماً صحيحاً")

        text = f"≭︰تم حذف البوتات التي تحتوي على اقل من ↫ ❲ {m} ❳ مجموعه"
        b = 0

        async for i in Bots.find({}):  
            try:
                bot_username = i["bot_username"]
                database = mo[bot_username]
                chatsdb = database.chats
                g = len(await get_chats(chatsdb))
                if g < m:
                    b += 1
                    boot = appp[bot_username]
                    await boot.stop()
                    await Bots.delete_one({"bot_username": bot_username})  
                    try:
                        Done.remove(bot_username)
                    except:
                        pass
                    try:
                        await boot.stop()
                        user = usr[bot_username]
                        await user.stop()
                    except:
                        pass
                    text += f"\n**{b}- @{bot_username} ، Group ↬ {g}**"
            except Exception as es:
                print(es)

        await message.reply_text(text)
        
@app.on_message(filters.command(["❲ رفع مطور ❳"], ""))
async def promote_developer(client: app, message):
    if message.from_user.id in OWNER_ID:
        ask = await client.ask(message.chat.id, "**≭︰ارسل ايدي المستخدم الذي تريد رفعه مطوراً**", timeout=30)
        if ask.text == "الغاء":
            return await ask.reply_text("**≭︰تم الغاء الامر**")
        
        developer_id = ask.text.strip()  
        developers.add(developer_id)  
        await ask.reply_text(f"**≭︰تم رفع {developer_id} كمطور بنجاح**")

@app.on_message(filters.command(["❲ تنزيل مطور ❳"], ""))
async def demote_developer(client: app, message):
    if message.from_user.id in OWNER_ID:
        ask = await client.ask(message.chat.id, "**≭︰ارسل ايدي المستخدم الذي تريد تنزيله من المطورين**", timeout=30)
        if ask.text == "الغاء":
            return await ask.reply_text("**≭︰تم الغاء الامر**")
        
        developer_id = ask.text.strip()  
        if developer_id in developers:
            developers.remove(developer_id) 
            await ask.reply_text(f"**≭︰تم تنزيل {developer_id} من قائمة المطورين**")
        else:
            await ask.reply_text(f"**≭︰المستخدم {developer_id} ليس مطوراً حاليا**")
            
@app.on_message(filters.command(["❲ المطورين ❳"], ""))
async def show_developers(client: app, message):
    if message.from_user.id in OWNER_ID:
        if developers:
            developer_list = "\n".join(developers)
            await message.reply_text(f"**≭︰قائمة المطورين:\n{developer_list}**")
        else:
            await message.reply_text("**≭︰لا يوجد مطورين في القائمة**")   
            
youtubee = ""

def is_valid_url(url):
    regex = re.compile(r'^(?:http|https)://[\w.-]+(?:\.[\w.-]+)+(?:\/\S*)?$')
    return re.match(regex, url) is not None

@app.on_message(filters.command("❲ 𝚄𝙿𝙳𝙰𝚃𝙴 𝙲𝙾𝙾𝙺𝙸𝙴𝚂 ❳", "") & filters.private, group=5478789)
async def set_cookies(client: Client, message: Message):
    if message.from_user.id in OWNER_ID or str(message.from_user.id) in developers: 
        try:
            foxx = await client.ask(
                chat_id=message.chat.id, 
                text="**أرسل الآن مسار ارفعه من هنا ↫ https://batbin.me**", 
                timeout=30
            )
            global youtubee
            if is_valid_url(foxx.text):
                youtubee = foxx.text
                await message.reply_text("** تم تعيين الكوكيز بنجاح**.")
            else:
                await message.reply_text("** الرابط غير صالح، تأكد من أنك أرسلت رابطًا صحيحًا.**")
        except Exception as e:
            await message.reply_text(f"** حدث خطأ أثناء تعيين يوتيوب: {e}**")

@app.on_message(filters.command("❲ 𝚁𝙴𝚂𝚃𝙰𝚁𝚃 𝙲𝙾𝙾𝙺𝙸𝙴𝚂 ❳", "") & filters.private, group=5417845789)
async def restart_cookies(client: Client, message: Message):
    if message.from_user.id in OWNER_ID or str(message.from_user.id) in developers: 
        try:
            save_file()
            await message.reply_text("** تم تحديث الكوكيز بنجاح.**")
        except Exception as e:
            await message.reply_text(f"** حدث خطأ أثناء تحديث: {e}**")

def save_file():
    global youtubee
    try:
        headers = {
            'Accept': 'text/plain',
            'User-Agent': 'python-requests'
        }
        file_path = "./cookies/cookies.txt"
        if os.path.exists(file_path):
            os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        if is_valid_url(youtubee):
            response = requests.get(youtubee, headers=headers)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(response.text)
    except Exception:
        pass  

@app.on_message(filters.command(["❲ الاسكرينات المفتوحه ❳"], ""))
async def kinhsker(client: Client, message):
 if message.from_user.id in OWNER_ID or str(message.from_user.id) in developers:
    n = 0
    response_message = "** ≯︰قائمة الاسكرينات المفتوحه **\n\n"
    for screen in os.listdir("/var/run/screen/S-root"):
        n += 1
        response_message += f"{n} - ( `{screen}` )\n"
    await message.reply_text(response_message)                            
