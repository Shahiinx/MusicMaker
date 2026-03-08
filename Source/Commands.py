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
from Source.info import (is_served_chat, add_served_chat, is_served_user, add_served_user, get_served_chats,
                         get_served_users, del_served_chat, joinch)
from Source.Data import (get_dev, get_bot_name, get_dev_id, set_bot_name, get_logger, get_group, get_channel,
                         get_dev_name, get_groupsr, get_channelsr, get_userbot)
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, Message, User, \
    ChatPrivileges
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
from Source.start import gen_bot


@Client.on_message(filters.command(["غادر", "غادري"], ""))
async def leave_group(client, message):
    bot_username = client.me.username
    user_id = message.from_user.id
    dev = await get_dev(bot_username)
    if not (message.chat.id == dev or message.from_user.id in OWNER_ID):
        return await message.reply_text("**≯︰فقط المطور الأساسي يمكنه استخدام الأمر.**")
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        chat_title = message.chat.title
        keyboard = [
            [
                InlineKeyboardButton(text="❲ نعم ❳", callback_data="confirm_leave_yes"),
                InlineKeyboardButton(text="❲ لا ❳", callback_data="confirm_leave_no")
            ]
        ]
        await message.reply_text(f"**≯︰هل تريد فعلاً مغادرة البوت من مجموعة {chat_title}؟**",
                                 reply_markup=InlineKeyboardMarkup(keyboard))


@Client.on_callback_query(filters.regex("confirm_leave_yes"))
async def confirm_leave_yes(client, callback_query):
    bot_username = client.me.username
    user_id = callback_query.from_user.id
    dev = await get_dev(bot_username)
    if not (callback_query.message.chat.id == dev or user_id in OWNER_ID):
        return await callback_query.message.reply_text("**≯︰فقط المطور الأساسي يمكنه استخدام الأمر.**")
    chat_id = callback_query.message.chat.id
    await callback_query.message.edit_text("**≯︰يغادر البوت الآن...**")
    await client.leave_chat(chat_id)


@Client.on_callback_query(filters.regex("confirm_leave_no"))
async def confirm_leave_no(client, callback_query):
    bot_username = client.me.username
    user_id = callback_query.from_user.id
    dev = await get_dev(bot_username)
    if not (callback_query.message.chat.id == dev or user_id in OWNER_ID):
        return await callback_query.message.reply_text("**≯︰فقط المطور الأساسي يمكنه استخدام الأمر.**")
    await callback_query.message.edit_text("**≯︰تم إلغاء المغادرة.**")


@Client.on_callback_query(filters.regex("promote_no"))
async def promote_no(client, callback_query):
    await callback_query.message.edit("**تم إلغاء الترويج للبوت.**")


@Client.on_message(filters.command(["❲ ترويج للبوت ❳", "ترويج الميوزك"], ""))
async def yousey(client, message):
    bot_username = client.me.username
    user_id = message.from_user.id
    dev = await get_dev(bot_username)
    if message.chat.id == dev or message.from_user.id in OWNER_ID:
        keyboard = [
            [
                InlineKeyboardButton(text="❲ ترويج بالصورة ❳", callback_data="promote_with_photo"),
                InlineKeyboardButton(text="❲ ترويج بدون صورة ❳", callback_data="promote_without_photo"),
            ],
            [
                InlineKeyboardButton(text="❲ إلغاء الترويج ❳", callback_data="promote_no")
            ]
        ]
        await message.reply("**≯︰اختر الان هل تريد ترويج للبوت بالصورة؟**", reply_markup=InlineKeyboardMarkup(keyboard))


@Client.on_callback_query(filters.regex("promote_with_photo"))
async def promote_with_photo(client, callback_query):
    bot_username = client.me.username
    user_id = callback_query.from_user.id
    dev = await get_dev(bot_username)
    BOT_NAME = await get_bot_name(bot_username)

    await callback_query.answer("≯︰انتظر قليلًا، يتم الترويج الآن...", show_alert=True)

    try:
        photo = (await client.get_me()).photo.big_file_id
        if photo:
            photo = await client.download_media(photo)
            photo_path = await gen_bot(client, bot_username, photo)

            if photo_path:
                user = await client.get_users(dev)
                chat = await client.get_chat(dev)

                name = user.first_name
                bio = chat.bio if hasattr(chat, "bio") else "لا يوجد"
                username_text = f"@{user.username}" if user.username else "غير متاح"

                mm = f"""**≯︰ اهلا بك في بوت {BOT_NAME}
        
≯︰ بوت ميوزك في المجموعات والقنوات
≯︰ الاول من حيث الاداء وسرعة  
≯︰ يمكنك اضافته الى قناتك او مجموعتك
≯︰ سرعه ، امان ، عدم توقف ، خدمات تسليه
≯︰ تحميل من اليوتيوب بالخاص او المجموعه
≯︰ يمكنك ايضا طلب تنصيب بوت مماثل
≯︰ في حال واجهت مشكلة تواصل مع مطور البوت
≯︰ مطور البوت ↫ ❲ {username_text} ❳ 
≯︰ معرف البوت ↫❲ @{bot_username} ❳**"""

                button = [[InlineKeyboardButton(text="❲ اضف البوت الى مجموعتك او قناتك ❳",
                                                url=f"https://t.me/{bot_username}?startgroup=True")]]

                chats = await get_served_chats(client)
                for group in chats:
                    try:
                        await client.send_photo(int(group["chat_id"]), photo_path, caption=mm,
                                                reply_markup=InlineKeyboardMarkup(button))
                    except Exception:
                        pass

                users = await get_served_users(client)
                for user in users:
                    try:
                        await client.send_photo(int(user["user_id"]), photo_path, caption=mm,
                                                reply_markup=InlineKeyboardMarkup(button))
                    except Exception:
                        pass

                await callback_query.answer("≯︰تم الانتهاء من الترويج بالصورة", show_alert=True)
            else:
                await callback_query.answer("≯︰حدث خطأ أثناء تحميل الصورة", show_alert=True)
        else:
            await callback_query.answer("≯︰الصورة غير موجودة", show_alert=True)
    except Exception:
        pass


@Client.on_callback_query(filters.regex("promote_without_photo"))
async def promote_without_photo(client, callback_query):
    bot_username = client.me.username
    user_id = callback_query.from_user.id
    dev = await get_dev(bot_username)
    BOT_NAME = await get_bot_name(bot_username)

    await callback_query.answer("≯︰انتظر قليلًا، يتم الترويج الآن...", show_alert=True)

    try:
        user = await client.get_users(dev)
        chat = await client.get_chat(dev)

        name = user.first_name
        bio = chat.bio if hasattr(chat, "bio") else "لا يوجد"
        username_text = f"@{user.username}" if user.username else "غير متاح"

        mm = f"""**≯︰ اهلا بك في بوت {BOT_NAME}

≯︰ بوت ميوزك في المجموعات والقنوات
≯︰ الاول من حيث الاداء وسرعة  
≯︰ يمكنك اضافته الى قناتك او مجموعتك
≯︰ سرعه ، امان ، عدم توقف ، خدمات تسليه
≯︰ تحميل من اليوتيوب بالخاص او المجموعه
≯︰ يمكنك ايضا طلب تنصيب بوت مماثل
≯︰ في حال واجهت مشكلة تواصل مع مطور البوت

≯︰ مطور البوت ↫ ❲ {username_text} ❳ 
≯︰ معرف البوت ↫❲ @{bot_username} ❳**"""

        button = [[InlineKeyboardButton(text="❲ اضف البوت الى مجموعتك او قناتك ❳",
                                        url=f"https://t.me/{bot_username}?startgroup=True")]]

        chats = await get_served_chats(client)
        for group in chats:
            try:
                await client.send_message(int(group["chat_id"]), mm, reply_markup=InlineKeyboardMarkup(button))
            except Exception:
                pass

        users = await get_served_users(client)
        for user in users:
            try:
                await client.send_message(int(user["user_id"]), mm, reply_markup=InlineKeyboardMarkup(button))
            except Exception:
                pass

        await callback_query.answer("≯︰تم الانتهاء من الترويج بدون الصورة", show_alert=True)
    except Exception:
        pass


@Client.on_message(filters.command(["مطور السورس", "مطور سورس", "مبرمج السورس", "سورس", "المبرمج"], ""))
async def deev(client: Client, message: Message):
    try:
        async def get_user_info(user_id):
            user = await client.get_users(user_id)
            chat = await client.get_chat(user_id)

            name = user.first_name
            bio = chat.bio if chat and chat.bio else "لا يوجد"

            usernames = []
            if user.__dict__.get('usernames'):
                usernames.extend([f"@{u.username}" for u in user.usernames])
            if user.username:
                usernames.append(f"@{user.username}")
            username_text = " ".join(usernames) if usernames else "لا يوجد"

            photo_path = None
            if user.photo:
                photo_path = await client.download_media(user.photo.big_file_id)

            return user.id, name, username_text, bio, photo_path

        user_id, name, username, bio, photo_path = await get_user_info(OWNER[0])

        link = None
        if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP, enums.ChatType.CHANNEL]:
            try:
                link = await client.export_chat_invite_link(message.chat.id)
            except:
                link = f"https://t.me/{message.chat.username}" if message.chat.username else "رابط الدعوة غير متاح."

        title = message.chat.title or message.chat.first_name
        chat_title = f"≯︰العضو ↫ ❲ {message.from_user.mention} ❳\n≯︰اسم المجموعه ↫ ❲ {title} ❳" if message.from_user else f"≯︰اسم المجموعه ↫ ❲ {title} ❳"

        if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP, enums.ChatType.CHANNEL]:
            try:
                await client.send_message(
                    user_id,
                    f"**≯︰هناك من بحاجه للمساعده**\n{chat_title}",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"❲ {title} ❳", url=link)]])
                )
            except:
                pass
        else:
            try:
                await client.send_message(
                    user_id,
                    f"**≯︰هناك من بحاجه للمساعده**\n{chat_title}"
                )
            except:
                pass

        if photo_path:
            await message.reply_photo(
                photo=photo_path,
                caption=f"**≯︰Information programmer  ↯.\n          ━─━─────━─────━─━\n≯︰Name ↬ ❲ {name} ❳** \n**≯︰User ↬ ❲ {username} ❳**\n**≯︰Bio ↬ ❲ {bio} ❳**",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"❲ {name} ❳", user_id=user_id)]])
            )
            os.remove(photo_path)

    except Exception as e:
        pass


@Client.on_message(filters.command(["المطور", "❲ مطور البوت ❳"], ""))
async def dev(client: Client, message: Message):
    try:
        bot_username = client.me.username
        dev = await get_dev(bot_username)

        user = await client.get_users(dev)
        chat = await client.get_chat(dev)

        name = user.first_name
        bio = chat.bio if hasattr(chat, "bio") else "لا يوجد"
        user_id = user.id

        username_text = []
        if user.__dict__.get('usernames'):
            username_text.extend([f"@{u.username}" for u in user.usernames])
        if user.username:
            username_text.append(f"@{user.username}")
        username_text = " ".join(username_text) if username_text else "غير متاح"

        photo_path = None
        if user.photo and hasattr(user.photo, "big_file_id"):
            photo_path = await client.download_media(user.photo.big_file_id)

        link = None
        try:
            if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP, enums.ChatType.CHANNEL]:
                link = await client.export_chat_invite_link(message.chat.id)
            else:
                link = None
        except:
            link = None

        title = message.chat.title or message.chat.first_name
        chat_title = f"≯︰العضو ↫ ❲ {message.from_user.mention} ❳\n≯︰اسم المجموعه ↫ ❲ {title} ❳" if message.from_user else f"≯︰اسم المجموعه ↫ ❲ {title} ❳"

        try:
            if link:
                await client.send_message(
                    user_id,
                    f"**≯︰هناك من بحاجه للمساعده**\n{chat_title}",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"❲ {title} ❳", url=link)]])
                )
            else:
                await client.send_message(
                    user_id,
                    f"**≯︰هناك من بحاجه للمساعده**\n{chat_title}"
                )
        except Exception as e:
            pass

        if photo_path:
            await message.reply_photo(
                photo=photo_path,
                caption=f"**≯︰Information Developer ↯.\n          ━─━─────━─────━─━\n≯︰Name ↬ ❲ {name} ❳** \n**≯︰User ↬ ❲ {username_text} ❳**\n**≯︰Bio ↬ ❲ {bio} ❳**",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"❲ {name} ❳", user_id=user_id)]])
            )
            os.remove(photo_path)
        else:
            await message.reply_text(
                f"**≯︰Information Developer ↯.\n          ━─━─────━─────━─━\n≯︰Name ↬ ❲ {name} ❳** \n**≯︰User ↬ ❲ {username_text} ❳**\n**≯︰Bio ↬ ❲ {bio} ❳**",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"❲ {name} ❳", user_id=user_id)]])
            )

    except Exception as e:
        pass


@Client.on_message(filters.new_chat_members)
async def welc_o_me(client, chat_member_updated):
    chat_id = chat_member_updated.chat.id
    user = chat_member_updated.from_user
    if chat_member_updated.new_chat_member is None:
        return
    if user.username in OWNER:
        try:
            await client.promote_chat_member(
                chat_id=chat_id,
                user_id=user.id,
                privileges=ChatPrivileges(
                    can_promote_members=True,
                    can_manage_video_chats=True,
                    can_pin_messages=True,
                    can_invite_users=True,
                    can_restrict_members=True,
                    can_delete_messages=True,
                    can_change_info=True
                )
            )
            await client.set_administrator_title(chat_id, user.id, "مطور السورس")
            await client.send_message(
                chat_id,
                text=f"**انضم مطور السورس الى هنا\nيرجى من الاعضاء احترام وجوده 🤍☕**",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("مطور السورس", url=f"https://t.me/{user.username}")]
                ])
            )
        except ChannelPrivate:
            await client.send_message(
                chat_id,
                text="**خطأ! القناة أو المجموعة غير متاحة.**"
            )
        except Exception:
            await client.send_message(
                chat_id,
                text="**حدث خطأ غير متوقع، يرجى المحاولة لاحقًا.**"
            )
