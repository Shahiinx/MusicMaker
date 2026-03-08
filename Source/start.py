import random
import shutil
import logging
from pyrogram.types import ReplyKeyboardRemove
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pathlib import Path 
from asyncio import gather
from pyrogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import Client, filters
from pyrogram.types import ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client as app
from pyrogram.types import ChatPermissions
from pyrogram import Client, filters, enums
from time import time
from config import OWNER, OWNER_ID, GROUP, OWNER_NAME, PHOTO, VIDEO
from Source.info import (is_served_chat, add_served_chat, is_served_user, add_served_user, get_served_chats, get_served_users, del_served_chat, joinch)
from Source.Data import (get_dev, get_bot_name, get_dev_id, set_bot_name, get_logger, get_group, get_channel, get_dev_name, get_groupsr, get_channelsr, get_userbot)
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, Message, User, ChatPrivileges
from pyrogram import enums
import os
import re
import textwrap
import aiofiles 
import aiohttp
from PIL import (Image, ImageDraw, ImageEnhance, ImageFilter,
                 ImageFont, ImageOps)
from youtubesearchpython.__future__ import VideosSearch
import asyncio
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont, ImageOps
import hashlib
from pyrogram import Client
import string
from pyrogram.types import ChatPrivileges
from pyrogram import Client, filters, enums
from pyrogram.types import ForceReply
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import ChatAdminRequired
OFFPV = set()
async def gen_bot(client, username, photo):
    photo_path = Path("./photo")
    photo_path.mkdir(parents=True, exist_ok=True)
    output_file = photo_path / f"{username}.png"
    if output_file.is_file():
        return str(output_file)
    background = Image.open(photo)
    background.save(output_file)
    return str(output_file)
            
@Client.on_message(filters.new_chat_members)
async def welcome(client: Client, message):
    try:
        bot = client.me
        bot_username = bot.username
        if message.new_chat_members[0].id == bot.id:
            photo = bot.photo.big_file_id
            photo = await client.download_media(photo)
            chat_id = message.chat.id
            bot = await client.get_me()
            username = client.me.username
            nn = await get_dev_name(client, bot_username)
            dev = await get_dev(bot.username)
            ch = await get_channel(bot_username)
            gr = await get_group(bot_username)
            chat_invite_link = message.chat.invite_link
            if not chat_invite_link:
                try:
                    chat_invite_link = await client.export_chat_invite_link(chat_id)
                except:
                    chat_invite_link = "https://t.me/" + message.chat.username if message.chat.username else "لا يمكن جلب الرابط"

            button = [
                [InlineKeyboardButton(text=f"❲ {nn} ❳", user_id=f"{dev}")],
                [
                    InlineKeyboardButton(text="❲ ᏟᎻᎪΝΝᎬᏞ ❳", url=f"{ch}"),
                    InlineKeyboardButton(text="❲ ᏀᎡϴႮᏢ ❳", url=f"{gr}")
                ],
                [InlineKeyboardButton("❲ اضفني لمجموعتك ❳", url=f"https://t.me/{bot.username}?startgroup=true")]
            ]

            await message.reply_photo(
                photo=photo, 
                caption="**≯︰اهلا بك في بوت تشغيل الاغاني \n≯︰تم تفعيل البوت في المجموعه تلقائيا \n≯︰يمكنك تشغيل الموسيقى الان 🎶**", 
                reply_markup=InlineKeyboardMarkup(button)
            )

            logger = await get_dev(bot_username)
            await add_served_chat(client, chat_id)
            chats = len(await get_served_chats(client))

            
            group_button = [[InlineKeyboardButton(text=f"{message.chat.title}", url=chat_invite_link)]]

            await client.send_message(
                logger, 
                f"**≯︰تم تفعيل مجموعه جديده ↯. \n≯︰اسم المجموعه ↫ ❲ [{message.chat.title}]({chat_invite_link}) ❳\n≯︰بواسطه ↫ ❲ {message.from_user.mention} ❳ \n≯︰عدد المجموعات ↫ ❲ {chats} ❳**", 
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(group_button)
            )

    except Exception:
        pass

@Client.on_message(filters.command(["❲ تفعيل التواصل ❳", "❲ تعطيل التواصل ❳"], ""))
async def byyye(client, message):
    user = message.from_user.username
    dev = await get_dev(client.me.username)
    if message.chat.id == dev or message.from_user.id in OWNER_ID:
        text = message.text
        if text == "❲ تفعيل التواصل ❳":
            if client.me.username in OFFPV:
                OFFPV.remove(client.me.username)
                await message.reply_text("**≯︰تم تفعيل التواصل**")
            else:
                await message.reply_text("**≯︰التواصل مفعل سابقا**")
        elif text == "❲ تعطيل التواصل ❳":
            if client.me.username not in OFFPV:
                OFFPV.add(client.me.username)
                await message.reply_text("**≯︰تم تعطيل التواصل**")
            else:
                await message.reply_text("**≯︰التواصل معطل سابقا**")


@Client.on_message(filters.private)
async def botoot(client: Client, message: Message):
    if client.me.username not in OFFPV:
        if await joinch(message):
            return
        
        bot_username = client.me.username
        user_id = message.chat.id
    

        if not await is_served_user(client, user_id):
            await add_served_user(client, user_id)

        dev = await get_dev(bot_username)
        if message.from_user.id == dev or message.from_user.id in OWNER_ID or message.from_user.id == client.me.id:
            if message.reply_to_message:
                u = message.reply_to_message.forward_from
                try:
                    await client.send_message(u.id, text=message.text)
                    await message.reply_text(f"**≯︰تم ارسال رسالتك الى ↫❲ {u.mention} ❳**")
                except Exception:
                    pass
        else:
            try:
                await client.forward_messages(dev, message.chat.id, message.id)
            except Exception as e:
                pass
    message.continue_propagation()        

@Client.on_message(filters.left_chat_member)
async def bot_kicked(client: Client, message):
    try:
        bot = client.me
        bot_username = bot.username
        if message.left_chat_member.id == bot.id:
            logger = await get_dev(bot_username)
            chat_id = message.chat.id
            await client.send_message(logger, f"**≯︰تم طرد البوت من مجموعه ↯.**\n**\n≯︰اسم المجموعه ↫ ❲ {message.chat.title} ❳**\n**≯︰بواسطه ↫** ❲ {message.from_user.mention} ❳")
            await del_served_chat(client, chat_id)
    except Exception:
        pass

@Client.on_message(filters.command(["/start", "❲ القائمه الرئيسيه ❳"], ""))
async def start(client: Client, message):
    try:
        if not message.chat.type == enums.ChatType.PRIVATE:
            if await joinch(message):
                return
        
        bot_username = client.me.username
        dev = await get_dev(bot_username) 
        nn = await get_dev_name(client, bot_username)
      
        if message.chat.id == dev or message.from_user.id in OWNER_ID:
            kep = ReplyKeyboardMarkup([
                ["❲ تعيين اسم البوت ❳"],
                ["❲ تعطيل الاشتراك الإجباري ❳", "❲ تفعيل الاشتراك الإجباري ❳"],
                ["❲ المكالمات النشطه ❳"],
                ["❲ تعطيل التواصل ❳", "❲ تفعيل التواصل ❳"],
                ["❲ تشغيل في قناه او مجموعه ❳"],
                ["❲ تعيين مجموعه البوت ❳", "❲ تعيين قناة البوت ❳"],
                ["❲ الكروبات ❳", "❲ المشتركين ❳"],
                ["❲ الاحصائيات ❳", "❲ ترويج للبوت ❳"],
                ["❲ قسم المساعد ❳", "❲ قسم الاذاعه ❳"],
                ["❲ تعطيل الاشعارات ❳", "❲ تفعيل الاشعارات ❳"],
                ["❲ تنظيف الملفات ❳", "❲ تغيير مكان الاشعارات ❳"],
                ["❲ مطورين السورس ❳"]
            ], resize_keyboard=True)

            await message.reply_text("**≯︰اهلا بك ، عزيزي المطور الاساسي .**", reply_markup=kep)
        else:
            bot = await client.get_me()
            username = client.me.username
            BOT_NAME = await get_bot_name(bot_username)
            ch = await get_channel(bot_username)
            gr = await get_group(bot.username)
            dev = await get_dev(bot.username)
            devname = await get_dev_name(client, bot.username)

            sddd = (
            f"**≯︰اهلا بك في بوت ↫  {BOT_NAME} \n\n**"
            f"**≯︰بوت خاص لتشغيل الأغاني الصوتية والمرئية\n**"
            f"**≯︰قم بإضافة البوت إلى مجموعتك أو قناتك\n**"
            f"**≯︰سيتم تفعيل البوت وانضمام المساعد\n**"
            f"**≯︰استخدم الأزرار لمعرفة أوامر الاستخدام**"
            
            )
            
            button = [
                    [InlineKeyboardButton("❲ لتنصيب بوت مماثل ❳", url=f"https://t.me/{OWNER[0]}")],
                    [InlineKeyboardButton("❲ اوامر التشغيل ❳", callback_data="bcmds"),
                     InlineKeyboardButton("❲ اوامر التفعيل ❳", callback_data="bhowtouse")],
                    [InlineKeyboardButton("❲ قناة البوت ❳", url=f"{ch}"),
                     InlineKeyboardButton("❲ المطور ❳", user_id=f"{dev}")],
                    [InlineKeyboardButton("❲ 𝖺𝖣𝖣 𝖬𝖾 𝖳𝗈 𝖸𝗈𝗎𝗋 𝖦𝗋𝗈𝗎𝗉𝗌 ❳", url=f"https://t.me/{bot.username}?startgroup=true")]
                ]
            
            if not bot.photo:
                sent_message = await client.send_message(message.chat.id, sddd, reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(button))
            else:
                photo = bot.photo.big_file_id
                photo = await client.download_media(photo)
                photo = await gen_bot(client, username, photo)
                
                sent_message = await client.send_photo(message.chat.id, photo=photo, caption=sddd, reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(button))
    except Exception:
        pass
        
bot = [
    "عيون {} العسليات",
    "موجود حبي قول ؟",
    "موجود بس لاتزانخ",
    "اطلق من يصيح {}",
    "عيفني مشغول بتشغيل الاغاني",
    "عيفني بحالي",
    "نعم يقلب قلبي",
    "احكي شبدك",
    "تحكي شبدك ؟ ولا اكتمك 🌚",
    "قول يقلبو",
    "عيون {} العسليات",
     "عيون {} ",
    "نعم يقلب {}",
    "شبك ولاك ؟ صار ساعه تصيح",
    "قلب {}",
    "نجب",
    "بذمتك اذا انت بدالي تقبل يسوون بيك هيج ؟",
]

selections = [
    "انت البوت صحلي باسمي {}",
    "حاج بوت اسمي {}",
    "عندي اسم تراا",
    "تقبل احد يصيحلك بوت ؟",
    "صحلي باسمي {} لا نتضارب",
    "اسمي {} ولك",
    "خلص قلتلك اسمي {}😒",
    "انت البوت قمنقلع 😂",
    "قول",
    "راسي صار يوجعني من وراك قمنقلع",
    "ياخي والله بحبك بس صحلي {}",
    "تدري راح احبك اكتر لو ناديتلي {}",
    "خراس بقى دوختني",
    "مو فاضيلك  قمنقلع",
    "لك احكي شبدك",
    "علي طلاق اسمي {}",
]

@Client.on_message(filters.command(["/alive", "معلومات", "سورس", "السورس", "❲ السورس ❳"], ""))
async def alive(client: Client, message: Message):
    try:
        chat_id = message.chat.id
        ch = await get_channelsr(client.me.username)
        gr = await get_groupsr(client.me.username)
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(f"{OWNER_NAME}", url=f"https://t.me/{OWNER[0]}")
            ], 
            [
                InlineKeyboardButton("❲ Source Ch ❳", url=f"{ch}"),
                InlineKeyboardButton("❲ Exp Source ❳", url=f"{gr}")
            ],
            [
                InlineKeyboardButton("❲ Add To Your Group ❳", url=f"https://t.me/{client.me.username}?startgroup=true")
            ]
        ])

        alive_msg = f"**≯︰Welcome to Source Music **"

        await message.reply_video(video=VIDEO, caption=alive_msg, reply_markup=keyboard)
    except Exception:
        pass

@Client.on_message(filters.command(["/ping", "بنك"], ""))
async def ping_pong(client: Client, message: Message):
    try:
        if message.chat.type != enums.ChatType.PRIVATE:
            if await joinch(message):
                return
        start = time()
        m_reply = await message.reply_text("pinging...")
        delta_ping = time() - start
        await m_reply.edit_text(f"≯︰سرعه السيرفر ↫ {delta_ping * 1000:.3f} ms")
    except Exception as e:
        pass

@Client.on_message(filters.command(["/help", "الاوامر", "اوامر"], ""))
async def starhelp(client: Client, message: Message):
    if not message.chat.type == enums.ChatType.PRIVATE:
        if await joinch(message):
            return

    bot = await client.get_me()
    photo = bot.photo.big_file_id
    photo = await client.download_media(photo)
    bot_username = client.me.username
    devname = await get_dev_name(client, bot.username)  
    dev = await get_dev(bot_username)

    await message.reply_photo(
        photo=photo,
        caption=f"",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("اللغة العربية 🇸🇾", callback_data="arbic"),
                    InlineKeyboardButton("English language 🇺🇲", callback_data="english")
                ],
                [
                    InlineKeyboardButton("اضف البوت الي مجموعتك ⚡", url=f"https://t.me/{bot.username}?startgroup=true")
                ],
                [
                    InlineKeyboardButton(text=f"{devname}", user_id=f"{dev}")  
                ],
            ]
        )
    )

    try:
        os.remove(photo)
    except:
        pass

@Client.on_message(filters.command(["تفعيل"], "") & ~filters.private)
async def pipong(client: Client, message: Message):
   if len(message.command) == 1:
    if not message.chat.type == enums.ChatType.PRIVATE:
      if await joinch(message):
            return
    await message.reply_text("**≯︰تم تفعيل البوت**")
    return 

@Client.on_message(filters.command(["كت"], ""))
async def bottttttt(client: Client, message: Message):
    if await joinch(message):
        return

@Client.on_message(filters.command("❲ تعيين اسم البوت ❳", ""))
async def set_bot(client: Client, message: Message):
    try:
        NAME = await client.ask(message.chat.id, "**≯︰ارسل اسم البوت الجديد**", filters=filters.text, timeout=30)
        BOT_NAME = NAME.text
        bot_username = client.me.username
        await set_bot_name(bot_username, BOT_NAME)
        await message.reply_text("**≯︰تم تغيير اسم البوت**")
    except Exception:
        pass  

@Client.on_message(filters.command(["❲ تنظيف الملفات ❳"], ""))
async def manual_delete(client: Client, message: Message):
    folders = ["./downloads", "./photo"]
    success = True 

    for folder_path in folders:
        try:
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
            os.makedirs(folder_path)  
        except Exception:
            success = False 

    if success:
        await message.reply_text("**≯︰تم تنظيف الملفات بنجاح.**")
    else:
        await message.reply_text("**≯︰فشل في تنظيف الملفات.**")

@Client.on_message(filters.command(["بوت", "البوت"], ""))
async def bottttt(client: Client, message: Message):
    bot_username = client.me.username
    BOT_NAME = await get_bot_name(bot_username)
    bar = random.choice(selections).format(BOT_NAME)
    
    try:
        await message.reply_text(f"**[{bar}](https://t.me/{bot_username}?startgroup=True)**", disable_web_page_preview=True)
    except ChatAdminRequired:
        pass

@Client.on_message(filters.text)
async def bott(client: Client, message: Message):
    bot_username = client.me.username
    BOT_NAME = await get_bot_name(bot_username)
    if message.text == BOT_NAME:
        bar = random.choice(bot).format(BOT_NAME)
        await message.reply_text(f"**[{bar}](https://t.me/{bot_username}?startgroup=True)**", disable_web_page_preview=True)
    message.continue_propagation()

@Client.on_message(~filters.private)
async def booot(client: Client, message: Message):
    chat_id = message.chat.id
    if not await is_served_chat(client, chat_id):
        try:
            await add_served_chat(client, chat_id)
            chats = len(await get_served_chats(client))
            bot_username = client.me.username
            dev = await get_dev(bot_username)
            username = f"https://t.me/{message.chat.username}" if message.chat.username else None
            mention = message.from_user.mention if message.from_user else message.chat.title
            await client.send_message(dev, f"**≯︰تم تفعيل مجموعه تلقائياً\n≯︰عدد المجموعات الان ↫❲ {chats} ❳ **\n≯︰اسم المجموعه ↫ ❲ [{message.chat.title}]({username}) ❳\n≯︰بواسطه ↫ ❲ {mention} ❳", disable_web_page_preview=True)
            await client.send_message(chat_id, f"**صلي على نبي وتبسم 🤍✨**")
            return
        except:
            pass  
    message.continue_propagation()