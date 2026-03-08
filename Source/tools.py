from pyrogram import Client, filters, raw, utils
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, Message
from config import logger as log, logger_mode as logm, OWNER_ID, Bots
from Source.info import (get_served_chats, get_served_users, del_served_chat, del_served_user, activecall, add_active_chat, add_served_call, add_active_video_chat)
from Source.play import (logs, join_call)
from Source.Data import (get_userbot, get_logger, get_dev, get_call, get_group, get_channel)
import aiohttp
import asyncio
from datetime import datetime
from pyrogram.errors import FloodWait
from pyrogram import enums
from typing import Union, List, Iterable
from pyrogram.errors import PeerIdInvalid

BASE = "https://batbin.me/"

async def post(url: str, *args, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, *args, **kwargs) as resp:
            try:
                data = await resp.json()
            except Exception:
                data = await resp.text()
        return data

async def base(text):
    resp = await post(f"{BASE}api/v2/paste", data=text)
    if not resp["success"]:
        return
    link = BASE + resp["message"]
    return link
    
@Client.on_message(filters.command(["الاحصائيات", "❲ الاحصائيات ❳"], ""))
async def analysis(client: Client, message: Message):
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    if message.chat.id == dev or message.from_user.id in OWNER_ID:
        chats = len(await get_served_chats(client))
        user = len(await get_served_users(client))
        return await message.reply_text(f"**≯︰احصائيات البوت كامله ↯.**\n**≯︰ المجموعات ↫ ❲ {chats} ❳ **\n**≯︰ المستخدمين ↫ ❲ {user} ❳ **")

@Client.on_message(filters.command(["❲ الكروبات ❳"], ""))
async def chats_func(client: Client, message: Message):
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    if message.chat.id == dev or message.from_user.id in OWNER_ID:
        chats = await get_served_chats(client)
        count = len(chats)
        return await message.reply_text(f"**≯︰عدد الكروبات ↫ ❲ {count} ❳ **")

@Client.on_message(filters.command(["❲ المشتركين ❳"], ""))
async def users_func(client: Client, message: Message):
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    if message.chat.id == dev or message.from_user.id in OWNER_ID:
        users = await get_served_users(client)
        count = len(users)
        return await message.reply_text(f"**≯︰عدد المشتركين ↫ ❲ {count} ❳ **")

@Client.on_message(filters.command("❲ المكالمات النشطه ❳", ""))
async def geetmeactive(client, message):
  bot_username = client.me.username
  dev = await get_dev(bot_username)
  if message.chat.id == dev or message.from_user.id in OWNER_ID:
   m = await message.reply_text("**≭︰انتظر قليلا ..**")
   count = 0
   text = ""
   for i in activecall[client.me.username]:
       try:
          chat = await client.get_chat(i)
          count += 1
          text += f"**{count}- ❲ [{chat.title}](https://t.me/{chat.username}) ❳\n**" if chat.username else f"**❲ {chat.title} ❳\n**"
       except Exception:
            title = "**Not Found**" 
            count += 1
            text += f"**{count}:- {title} {i}\n**"
   if count == 0:
      return await m.edit("**≭︰لا يوجد مكالمات قيد التشغيل**")
   else:
      try:
        await message.reply_text(text, disable_web_page_preview=True)
      except: 
         link = await base(text)
         await message.reply_text(link)
      return await m.delete()

@Client.on_message(filters.command(["❲ قسم الاذاعه ❳", "❲ للخلف ❳"], ""))
async def cast(client: Client, message):
   bot_username = client.me.username
   dev = await get_dev(bot_username)
   if message.chat.id == dev or message.from_user.id in OWNER_ID:
    kep = ReplyKeyboardMarkup([["❲ اذاعه عام ❳"], ["❲ اذاعه للمجموعات ❳", "❲ اذاعه للمستخدمين ❳"], ["❲ توجيه عام ❳"], ["❲ توجيه للمجموعات ❳", "❲ توجيه للمستخدمين ❳"], ["❲ القائمه الرئيسيه ❳"]], resize_keyboard=True)
    await message.reply_text("**≯︰مرحبا بك عزيزي المطور **\n**≯︰اليك كيبورد اوامر الاذاعات**", reply_markup=kep)

@Client.on_message(filters.command(["❲ اذاعه عام ❳", "❲ اذاعه للمجموعات ❳", "❲ اذاعه للمستخدمين ❳", "❲ توجيه عام ❳", "❲ توجيه للمستخدمين ❳", "❲ توجيه للمجموعات ❳"], ""))
async def cast1(client: Client, message):
   command = message.command[0]
   bot_username = client.me.username
   dev = await get_dev(bot_username)
   if message.chat.id == dev or message.from_user.id in OWNER_ID:
    if command == "❲ اذاعه عام ❳":
     kep = ReplyKeyboardMarkup([["❲ اذاعه عام بالبوت ❳"], ["❲ اذاعه عام بالمساعد ❳"], ["❲ للخلف ❳"]], resize_keyboard=True)
     await message.reply_text("**≯︰مرحبا بك عزيزي المطور **\n**≯︰اليك كيبورد اوامر الاذاعات**", reply_markup=kep)
    elif command == "❲ اذاعه للمجموعات ❳":
     kep = ReplyKeyboardMarkup([["❲ اذاعه للمجموعات بالبوت ❳"], ["❲ اذاعه للمجموعات بالمساعد ❳"], ["❲ للخلف ❳"]], resize_keyboard=True)
     await message.reply_text("**≯︰مرحبا بك عزيزي المطور **\n**≯︰اليك كيبورد اوامر الاذاعات**", reply_markup=kep)
    elif command == "❲ اذاعه للمستخدمين ❳":
     kep = ReplyKeyboardMarkup([["❲ اذاعه للمستخدمين بالبوت ❳"], ["❲ اذاعه للمستخدمين بالمساعد ❳"], ["❲ للخلف ❳"]], resize_keyboard=True)
     await message.reply_text("**≯︰مرحبا بك عزيزي المطور **\n**≯︰اليك كيبورد اوامر الاذاعات**", reply_markup=kep)
    elif command == "❲ توجيه عام ❳":
     kep = ReplyKeyboardMarkup([["❲ توجيه عام بالبوت ❳"], ["❲ للخلف ❳"]], resize_keyboard=True)
     await message.reply_text("**≯︰مرحبا بك عزيزي المطور **\n**≯︰اليك كيبورد اوامر الاذاعات**", reply_markup=kep)
    elif command == "❲ توجيه للمستخدمين ❳":
     kep = ReplyKeyboardMarkup([["❲ توجيه للمستخدمين بالبوت ❳"], ["❲ للخلف ❳"]], resize_keyboard=True)
     await message.reply_text("**≯︰مرحبا بك عزيزي المطور **\n**≯︰اليك كيبورد اوامر الاذاعات**", reply_markup=kep)
    else:
     kep = ReplyKeyboardMarkup([["❲ توجيه للمجموعات بالبوت ❳"], ["❲ للخلف ❳"]], resize_keyboard=True)
     await message.reply_text("**≯︰مرحبا بك عزيزي المطور **\n**≯︰اليك كيبورد اوامر الاذاعات**", reply_markup=kep)

@Client.on_message(filters.command(["❲ اذاعه عام بالبوت ❳", "❲ اذاعه عام بالمساعد ❳", "❲ اذاعه للمجموعات بالبوت ❳", "❲ اذاعه للمجموعات بالمساعد ❳", "❲ اذاعه للمستخدمين بالبوت ❳", "❲ اذاعه للمستخدمين بالمساعد ❳", "❲ توجيه عام بالبوت ❳", "❲ توجيه عام بالمساعد ❳", "❲ توجيه للمجموعات بالبوت ❳", "❲ توجيه للمجموعات بالمساعد ❳", "❲ توجيه للمستخدمين بالبوت ❳", "❲ توجيه للمستخدمين بالمساعد ❳"], ""))
async def cast5(client: Client, message):
  command = message.command[0]
  bot_username = client.me.username
  dev = await get_dev(bot_username)
  if message.chat.id == dev or message.from_user.id in OWNER_ID:
   kep = ReplyKeyboardMarkup([["❲ الغاء ❳"], ["❲ للخلف ❳"], ["❲ القائمه الرئيسيه ❳"]], resize_keyboard=True)
   ask = await client.ask(message.chat.id, "≯︰ارسل الرساله المراد اذاعتها", reply_markup=kep)
   x = ask.id
   y = message.chat.id
   if ask.text == "❲ الغاء ❳":
     return await ask.reply_text("**≯︰تم الغاء الامر**")
   pn = await client.ask(message.chat.id, "≯︰هل تريد تثبيت الرساله ؟\n≯︰ارسل ❲ نعم ❳ او ❲ لا ❳")
   await message.reply_text("**≯︰جاري نشر الرساله قد يستغرق بعض الوقت**")
   text = ask.text
   dn = 0
   fd = 0
   if command == "❲ اذاعه عام بالبوت ❳":
     chats = await get_served_chats(client)
     users = await get_served_users(client)
     chat = []
     for user in users:
         chat.append(int(user["user_id"]))
     for c in chats:
         chat.append(int(c["chat_id"]))
     for i in chat:
         try:
           m = await client.send_message(chat_id=i, text=text)
           dn += 1
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
                    fd += 1
                    continue
     return await message.reply_text(f"**≯︰تم اذاعه الرساله**\n\n**≯︰الارسال الناجح ↫ ❲ {dn} ❳**\n**≯︰الارسال الفاشل ↫ ❲ {fd} ❳**")
   elif command == "❲ اذاعه عام بالمساعد ❳":
     user = await get_userbot(bot_username)
     async for i in user.get_dialogs():
         try:
           m = await user.send_message(chat_id=i.chat.id, text=text)
           dn += 1
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
                    fd += 1
                    continue
     return await message.reply_text(f"**≯︰تم اذاعه الرساله**\n\n**≯︰الارسال الناجح ↫ ❲ {dn} ❳**\n**≯︰الارسال الفاشل ↫ ❲ {fd} ❳**")
   elif command == "❲ اذاعه للمجموعات بالبوت ❳":
     chats = await get_served_chats(client)
     chat = []
     for c in chats:
         chat.append(int(c["chat_id"]))
     for i in chat:
         try:
           m = await client.send_message(chat_id=i, text=text)
           dn += 1
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
                    fd += 1
                    continue
     return await message.reply_text(f"**≯︰تم اذاعه الرساله**\n\n**≯︰الارسال الناجح ↫ ❲ {dn} ❳**\n**≯︰الارسال الفاشل ↫ ❲ {fd} ❳**")
   elif command == "❲ اذاعه للمجموعات بالمساعد ❳":
     user = await get_userbot(bot_username)
     async for i in user.get_dialogs():
         if not i.chat.type == enums.ChatType.PRIVATE:
          try:
           m = await user.send_message(chat_id=i.chat.id, text=text)
           dn += 1
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
                    fd += 1
                    continue
     return await message.reply_text(f"**≯︰تم اذاعه الرساله**\n\n**≯︰الارسال الناجح ↫ ❲ {dn} ❳**\n**≯︰الارسال الفاشل ↫ ❲ {fd} ❳**")
   elif command == "❲ اذاعه للمستخدمين بالبوت ❳":
     chats = await get_served_users(client)
     chat = []
     for c in chats:
         chat.append(int(c["user_id"]))
     for i in chat:
         try:
           i = i
           m = await client.send_message(chat_id=i, text=text)
           dn += 1
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
                    fd += 1
                    continue
     return await message.reply_text(f"**≯︰تم اذاعه الرساله**\n\n**≯︰الارسال الناجح ↫ ❲ {dn} ❳**\n**≯︰الارسال الفاشل ↫ ❲ {fd} ❳**")
   elif command == "❲ اذاعه للمستخدمين بالمساعد ❳":
     client = await get_userbot(bot_username)
     async for i in client.get_dialogs():
         if i.chat.type == enums.ChatType.PRIVATE:
          try:
           m = await client.send_message(chat_id=i.chat.id, text=text)
           dn += 1
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
                    fd += 1
                    continue
     return await message.reply_text(f"**≯︰تم اذاعه الرساله**\n\n**≯︰الارسال الناجح ↫ ❲ {dn} ❳**\n**≯︰الارسال الفاشل ↫ ❲ {fd} ❳**")
   elif command == "❲ توجيه عام بالبوت ❳":
     chats = await get_served_chats(client)
     users = await get_served_users(client)
     chat = []
     for user in users:
         chat.append(int(user["user_id"]))
     for c in chats:
         chat.append(int(c["chat_id"]))
     for i in chat:
         try:
           m = await client.forward_messages(i, y, x)
           dn += 1
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
                    fd += 1
                    continue
     return await message.reply_text(f"**≯︰تم اذاعه الرساله**\n\n**≯︰الارسال الناجح ↫ ❲ {dn} ❳**\n**≯︰الارسال الفاشل ↫ ❲ {fd} ❳**")
   elif command == "❲ توجيه عام بالمساعد ❳":
     client = await get_userbot(bot_username)
     async for i in client.get_dialogs():
         try:
           m = await client.forward_messages(
               chat_id=i.chat.id,
               from_chat_id=message.chat.username,
               message_ids=int(x),
               )
           dn += 1
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
                    fd += 1
                    continue
     return await message.reply_text(f"**≯︰تم اذاعه الرساله**\n\n**≯︰الارسال الناجح ↫ ❲ {dn} ❳**\n**≯︰الارسال الفاشل ↫ ❲ {fd} ❳**")
   elif command == "❲ توجيه للمجموعات بالبوت ❳":
     chats = await get_served_chats(client)
     chat = []
     for user in chats:
         chat.append(int(user["chat_id"]))
     for i in chat:
         try:
           m = await client.forward_messages(i, y, x)
           dn += 1
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
                    fd += 1
                    continue
     return await message.reply_text(f"**≯︰تم اذاعه الرساله**\n\n**≯︰الارسال الناجح ↫ ❲ {dn} ❳**\n**≯︰الارسال الفاشل ↫ ❲ {fd} ❳**")
   elif command == "❲ توجيه للمجموعات بالمساعد ❳":
     client = await get_userbot(bot_username)
     async for i in client.get_dialogs():
         if not i.chat.type == enums.ChatType.PRIVATE:
          try:
           m = await client.forward_messages(i.chat.id, y, x)
           dn += 1
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
                    fd += 1
                    continue
     return await message.reply_text(f"**≯︰تم اذاعه الرساله**\n\n**≯︰الارسال الناجح ↫ ❲ {dn} ❳**\n**≯︰الارسال الفاشل ↫ ❲ {fd} ❳**")
   elif command == "❲ توجيه للمستخدمين بالبوت ❳":
     chats = await get_served_users(client)
     chat = []
     for c in chats:
         chat.append(int(c["user_id"]))
     for i in chat:
         try:
           m = await client.forward_messages(i, y, x)
           dn += 1
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
                    fd += 1
                    continue
     return await message.reply_text(f"**≯︰تم اذاعه الرساله**\n\n**≯︰الارسال الناجح ↫ ❲ {dn} ❳**\n**≯︰الارسال الفاشل ↫ ❲ {fd} ❳**")
   elif command == "❲ توجيه للمستخدمين بالمساعد ❳":
     client = await get_userbot(bot_username)
     async for i in client.get_dialogs():
         if i.chat.type == enums.ChatType.PRIVATE:
          try:
           m = await client.forward_messages(i.chat.id, y, x)
           dn += 1
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
          except:
                    fd += 1
                    continue
     return await message.reply_text(f"**≯︰تم اذاعه الرساله**\n\n**≯︰الارسال الناجح ↫ ❲ {dn} ❳**\n**≯︰الارسال الفاشل ↫ ❲ {fd} ❳**")

@Client.on_message(filters.command("❲ قسم المساعد ❳", ""))
async def helpercn(client, message):
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    userbot = await get_userbot(bot_username)
    me = userbot.me

    user_info = f"**≯︰المعرف ↫ ❲ @{me.username} ❳\n≯︰الايدي ↫ ❲ {me.id} ❳**" if me.username else f"**≯︰الايدي ↫ ❲ {me.id} ❳**"

    try:
        user_chat = await userbot.get_chat(me.id)
        bio = user_chat.bio if user_chat.bio else "لا يوجد بايو"
    except PeerIdInvalid:
        await message.reply_text("عذرًا، لم أستطع العثور على المستخدم.")
        return

    if message.chat.id == dev or message.from_user.id in OWNER_ID:
        keyboard = ReplyKeyboardMarkup(
            [
                ["❲ احصائيات المساعد ❳"],
                ["❲ تغيير الاسم الثاني ❳", "❲ تغيير الاسم الاول ❳"],
                ["❲ تغيير المعرف ❳"],
                ["❲ تغيير النبذه ❳"],
                ["❲ مسح الصوره ❳", "❲ تعيين الصوره ❳"],
                ["❲ خروج المساعد من جميع الكروبات ❳", "❲ انضمام المساعد لمجموعه ❳"],
                ["❲ القائمه الرئيسيه ❳"]
            ],
            resize_keyboard=True
        )

        await message.reply_text(
            f"**≯︰مرحبا بك عزيزي المطور**\n"
            f"**≯︰اليك كيبورد اوامر المساعد**\n\n"
            f"**≯︰الاسم ↫❲ {me.mention} ❳**\n"
            f"{user_info}\n"
            f"**≯︰النبذه ↫ ❲ {bio} ❳**",
            reply_markup=keyboard
        )

@Client.on_message(filters.command("❲ احصائيات المساعد ❳", ""))
async def userrrrr(client: Client, message):
    bot_username = client.me.username
    dev = await get_dev(bot_username)

    if message.chat.id == dev or message.from_user.id in OWNER_ID:
        client = await get_userbot(bot_username)
        mm = await message.reply_text("Collecting stats")
        start = datetime.now()
        u, g, sg, c, b, a_chat = 0, 0, 0, 0, 0, 0

        Meh = client.me
        usere = Meh.mention

        async for dialog in client.get_dialogs():
            try:
                type = dialog.chat.type
                if type == enums.ChatType.PRIVATE:
                    u += 1
                elif type == enums.ChatType.BOT:
                    b += 1
                elif type == enums.ChatType.GROUP:
                    g += 1
                elif type == enums.ChatType.SUPERGROUP:
                    sg += 1
                    user_s = await dialog.chat.get_member(int(Meh.id))
                    if user_s.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
                        a_chat += 1
                elif type == enums.ChatType.CHANNEL:
                    c += 1
            except Exception as e:
                print(f"Error processing dialog: {e}")

        end = datetime.now()
        ms = (end - start).seconds

        await mm.edit_text(
            f"""**≯︰اليك احصائيات المساعد مفصله ↯.**

≯︰**تم الرد في ↫ ❲ {ms} ❳ ثانيه**
≯︰**عدد محادثات الخاص ↫ ❲ {u} ❳**
≯︰**عدد الكروبات العاديه ↫ ❲ {g} ❳**
≯︰**عدد الكروبات السوبر ↫ ❲ {sg} ❳**
≯︰**عدد القنوات فالحساب ↫ ❲ {c} ❳**
≯︰**عدد المجموعات الادمن فيها ↫ ❲ {a_chat} ❳**
≯︰**عدد البوتات فالحساب ↫ ❲ {b} ❳**
≯︰**هذه احصائيات ↫ ❲ {usere} ❳**"""
        )

@Client.on_message(filters.command("❲ تغيير الاسم الاول ❳", ""))
async def change_first_name(client: Client, message):
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    if message.chat.id == dev or message.from_user.id in OWNER_ID:
        try:
            name = await client.ask(message.chat.id, "≯︰ارسل الاسم الجديد")
            name = name.text
            userbot = await get_userbot(bot_username)
            await userbot.update_profile(first_name=name)
            await message.reply_text("**≯︰تم تغيير اسم المساعد**")
        except Exception as e:
            await message.reply_text(f"≯︰حدثت مشكله في تغيير الاسم\n{e}")

# تغيير الاسم الثاني
@Client.on_message(filters.command("❲ تغيير الاسم الثاني ❳", ""))
async def change_last_name(client: Client, message):
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    if message.chat.id == dev or message.from_user.id in OWNER_ID:
        try:
            name = await client.ask(message.chat.id, "≯︰ارسل الاسم الجديد")
            name = name.text
            userbot = await get_userbot(bot_username)
            await userbot.update_profile(last_name=name)
            await message.reply_text("**≯︰تم تغيير اسم المساعد**")
        except Exception as e:
            await message.reply_text(f"≯︰حدثت مشكله في تغيير الاسم\n{e}")

# تغيير النبذة
@Client.on_message(filters.command("❲ تغيير النبذه ❳", ""))
async def change_bio(client: Client, message):
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    if message.chat.id == dev or message.from_user.id in OWNER_ID:
        try:
            bio = await client.ask(message.chat.id, "≯︰ارسل النبذه الجديده")
            bio = bio.text
            userbot = await get_userbot(bot_username)
            await userbot.update_profile(bio=bio)
            await message.reply_text("**≯︰تم تغيير نبذه المساعد**")
        except Exception as e:
            await message.reply_text(f"≯︰حدثت مشكله في تغيير النبذه\n{e}")

# تغيير المعرف
@Client.on_message(filters.command("❲ تغيير المعرف ❳", ""))
async def change_username(client: Client, message):
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    if message.chat.id == dev or message.from_user.id in OWNER_ID:
        try:
            username = await client.ask(message.chat.id, "≯︰ارسل المعرف الجديد")
            username = username.text
            userbot = await get_userbot(bot_username)
            await userbot.set_username(username)
            await message.reply_text("**≯︰تم تغيير معرف المساعد**")
        except Exception as e:
            await message.reply_text(f"≯︰حدثت مشكله في تغيير المعرف\n{e}")

# تغيير الصورة
@Client.on_message(filters.command("❲ تعيين الصوره ❳", ""))
async def change_photo(client: Client, message):
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    if message.chat.id == dev or message.from_user.id in OWNER_ID:
        try:
            m = await client.ask(message.chat.id, "≯︰ارسل الصوره الجديده")
            photo = await m.download()
            userbot = await get_userbot(bot_username)
            await userbot.set_profile_photo(photo=photo)
            await message.reply_text("**≯︰تم تغيير صوره المساعد**")
        except Exception as e:
            await message.reply_text(f"≯︰حدثت مشكله في تغيير الصوره\n{e}")

# مسح الصور
@Client.on_message(filters.command("❲ مسح الصوره ❳", ""))
async def delete_photos(client: Client, message):
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    if message.chat.id == dev or message.from_user.id in OWNER_ID:
        try:
            userbot = await get_userbot(bot_username)
            photos = await userbot.get_profile_photos("me")
            if len(photos) > 1:
                await userbot.delete_profile_photos([p.file_id for p in photos[1:]])
            await message.reply_text("**≯︰تم مسح صوره المساعد**")
        except Exception as e:
            await message.reply_text(f"≯︰حدثت مشكله في مسح الصوره\n{e}")
            
@Client.on_message(filters.command("❲ انضمام المساعد لمجموعه ❳", ""))
async def joined(client: Client, message):
  bot_username = client.me.username
  dev = await get_dev(bot_username)
  if message.chat.id == dev or message.from_user.id in OWNER_ID:
   try:
    name = await client.ask(message.chat.id, "**≯︰ارسل رابط الكروب للانضمام**")
    name = name.text
    if "https" in name: 
     if not "+" in name: 
       name = name.replace("https://t.me/", "")
    client = await get_userbot(bot_username)
    await client.join_chat(name)
    await message.reply_text("**≯︰تم انضمام المساعد للكروب**")
   except Exception as es:
     await message.reply_text(f"≯︰حدثت مشكله في انضمام المساعد \n {es}")

@Client.on_message(filters.command("❲ خروج المساعد من جميع الكروبات ❳", ""))
async def leave_all_groups_and_channels(client: Client, message):
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    if message.chat.id == dev or message.from_user.id in OWNER_ID:
        try:
            mm = await message.reply_text("**≯︰جاري محاولة الخروج من جميع الكروبات والقنوات..**.")
            userbot = await get_userbot(bot_username)
            dialogs = [dialog async for dialog in userbot.get_dialogs()]
            left_count = 0

       
            logger_group = await get_logger(bot_username)

            for dialog in dialogs:
            
                if dialog.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP, enums.ChatType.CHANNEL]:
                   
                    if dialog.chat.id == logger_group:
                        continue

                    try:
   
                        await userbot.leave_chat(dialog.chat.id)
                        left_count += 1
                        await asyncio.sleep(5) 
                    except Exception as e:
                        await message.reply_text(f"**≯︰تعذر الخروج من {dialog.chat.title}\n الخطأ: {e}**")

            await mm.edit_text(f"**≯︰تم خروج المساعد من {left_count} كروب/قناة بنجاح**")
        except Exception as es:
            await message.reply_text(f"**≯︰حدثت مشكله في خروج المساعد من الكروبات والقنوات \n {es}**")

@Client.on_message(filters.command(["❲ تغيير مكان الاشعارات ❳", "❲ تفعيل الاشعارات ❳", "❲ تعطيل الاشعارات ❳"], ""))
async def set_history(client: Client, message):
    bot_username = client.me.username
    dev = await get_dev(bot_username)

    if message.chat.id == dev or message.from_user.id in OWNER_ID:
        logger = None

        if message.command[0] == "❲ تغيير مكان الاشعارات ❳":
            ask = await client.ask(message.chat.id, "**⏎︰ارسل ايدي الكروب او القناة**", timeout=30)
            logger = ask.text.strip().replace("@", "")

        bot_data = await Bots.find_one({"bot_username": bot_username})
        if not bot_data:
            return await message.reply_text("**⏎︰تعذر العثور على بيانات البوت**")

        token = bot_data["token"]
        session = bot_data["session"]
        dev = bot_data["dev"]
        logger_old = bot_data["logger"]
        logger_mode = bot_data["logger_mode"]

        if message.command[0] == "❲ تغيير مكان الاشعارات ❳":
            if logger_old == logger:
                return await ask.reply_text("**⏎︰تم تعيين هذا المكان فعلا**")

            try:
                user = await get_userbot(bot_username)
                await client.send_message(logger, "**⏎︰انتظر قليلا**")
                await user.send_message(logger, "**⏎︰جاري تغيير مكان اشعارات التشغيل**")

                await Bots.delete_one({"bot_username": bot_username})
                await asyncio.sleep(2)

                new_data = {
                    "bot_username": bot_username,
                    "token": token,
                    "session": session,
                    "dev": dev,
                    "logger": logger,
                    "logger_mode": logger_mode
                }
                await Bots.insert_one(new_data)
                log[bot_username] = logger
                await ask.reply_text("**⏎︰تم تعيين مكان اشعارات التشغيل الجديد**")
            except Exception:
                await ask.reply_text("**⏎︰تأكد أن البوت والحساب المساعد مشرفين**")

        else:
            mode = "ON" if message.command[0] == "❲ تفعيل الاشعارات ❳" else "OFF"

            if logger_mode == mode:
                status = "مفعله" if mode == "ON" else "معطله"
                return await message.reply_text(f"**⏎︰الاشعارات {status} فعلا**")

            try:
                await Bots.delete_one({"bot_username": bot_username})
                new_data = {
                    "bot_username": bot_username,
                    "token": token,
                    "session": session,
                    "dev": dev,
                    "logger": logger_old,
                    "logger_mode": mode
                }
                await Bots.insert_one(new_data)
                logm[bot_username] = mode
                action = "تفعيل" if mode == "ON" else "تعطيل"
                await message.reply_text(f"**⏎︰تم {action} الاشعارات**")
            except Exception:
                await message.reply_text("**⏎︰حدثت مشكلة أثناء تغيير الإعدادات**")