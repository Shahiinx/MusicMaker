from pyrogram import Client, filters
from youtubesearchpython.__future__ import VideosSearch
import os
import aiohttp
import requests
import random
import asyncio
import yt_dlp
from pyrogram.types import Chat
from datetime import datetime, timedelta
from youtube_search import YoutubeSearch
import pytgcalls
from pytgcalls.types.input_stream.quality import (HighQualityAudio,
                                                  HighQualityVideo,
                                                  LowQualityAudio,
                                                  LowQualityVideo,
                                                  MediumQualityAudio,
                                                  MediumQualityVideo)
from typing import Union
from pyrogram import Client, filters
from pyrogram import Client as client
from pyrogram.errors import (ChatAdminRequired,
                             UserAlreadyParticipant,
                             UserNotParticipant)
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType, ChatMemberStatus
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.exceptions import (AlreadyJoinedError,
                                  NoActiveGroupCall,
                                  TelegramServerError)
from pytgcalls.types import (JoinedGroupCallParticipant,
                             LeftGroupCallParticipant, Update)
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.stream import StreamAudioEnded
from config import PHOTO, LOGS
from Source.info import (db, add, is_served_call, add_active_video_chat, add_served_call, add_active_chat, gen_thumb,
                         download, remove_active, joinch)
from Source.Data import (get_logger, get_userbot, get_call, get_dev, get_dev_name, get_logger_mode, get_group,
                         get_channel)
import asyncio
from pyrogram.errors import PeerIdInvalid


def panel_buttons(ch, dev, devname):
    return [
        [
            InlineKeyboardButton(text="ᎬŃᎠ", callback_data="stop"),
            InlineKeyboardButton(text="ᎡᎬՏႮᎷᎬ", callback_data="resume"),
            InlineKeyboardButton(text="ᏢᎪႮՏᎬ", callback_data="pause")
        ],
        [
            InlineKeyboardButton(text="ᏟᎻᎪΝΝᎬᏞ", url=f"{ch}"),
        ],
        [
            InlineKeyboardButton(text=f"{devname}", user_id=dev)
        ],
        [
            InlineKeyboardButton(text="ᏟᏞᎾՏᎬ", callback_data="close_panel")
        ]
    ]


@Client.on_callback_query(filters.regex("close_panel"))
async def close_panel(_, CallbackQuery):
    try:
        await CallbackQuery.message.delete()
    except:
        pass


async def join_assistant(client, chat_id, message_id, userbot, file_path):
    join = None
    try:
        try:
            user = userbot.me
            user_id = user.username if user.username else user.user_id
            user_full = await client.get_users(user_id)
            get = await client.get_chat_member(chat_id, user_full.id)
        except ChatAdminRequired:
            await client.send_message(chat_id, f"**≭︰ارفع البوت ادمن اولا**", reply_to_message_id=message_id)
        if get.status == ChatMemberStatus.BANNED:
            await client.send_message(chat_id,
                                      f"≭︰الغي الحظر عن المساعد لتتمكن من التشغيل\n≭︰الحساب المساعد ↫ ❲ @{user.username} ❳",
                                      reply_to_message_id=message_id)
        else:
            join = True
    except UserNotParticipant:
        chat = await client.get_chat(chat_id)
        if chat.username:
            try:
                await userbot.join_chat(chat.username)
                join = True
            except UserAlreadyParticipant:
                join = True
            except Exception:
                try:
                    invitelink = (await client.export_chat_invite_link(chat_id))
                    if invitelink.startswith("https://t.me/+"):
                        invitelink = invitelink.replace("https://t.me/+", "https://t.me/joinchat/")
                    await asyncio.sleep(3)
                    await userbot.join_chat(invitelink)
                    join = True
                except ChatAdminRequired:
                    return await client.send_message(chat_id, f"**≭︰اعطي البوت صلاحيه دعوه مستخدمين عبر الرابط**",
                                                     reply_to_message_id=message_id)
                except Exception as e:
                    await client.send_message(chat_id, f"**≭︰حدثت مشكله جرب مره اخرى او تواصل مع المطور**",
                                              reply_to_message_id=message_id)
        else:
            try:
                try:
                    invitelink = chat.invite_link
                    if invitelink is None:
                        invitelink = (await client.export_chat_invite_link(chat_id))
                except Exception:
                    try:
                        invitelink = (await client.export_chat_invite_link(chat_id))
                    except ChatAdminRequired:
                        await client.send_message(chat_id, f"**≭︰اعطي البوت صلاحيه دعوه مستخدمين عبر الرابط**",
                                                  reply_to_message_id=message_id)
                    except Exception as e:
                        await client.send_message(chat_id, f"**≭︰حدثت مشكله جرب مره اخرى او تواصل مع المطور**",
                                                  reply_to_message_id=message_id)
                m = await client.send_message(chat_id, "**≭︰جاري تفعيل البوت**")
                if invitelink.startswith("https://t.me/+"):
                    invitelink = invitelink.replace("https://t.me/+", "https://t.me/joinchat/")
                await userbot.join_chat(invitelink)
                join = True
                await m.edit(f"≭︰انضم الحساب المساعد\n≭︰بدء تشغيل الموسيقى \n≭︰الحساب المساعد ↫❲[ {user.mention} ]❳")
            except UserAlreadyParticipant:
                join = True
            except Exception as e:
                await client.send_message(chat_id, f"**≭︰حدثت مشكله جرب مره اخرى او تواصل مع المطور**",
                                          reply_to_message_id=message_id)
    return join


async def join_call(
        client,
        message_id,
        chat_id,
        bot_username,
        file_path,
        link,
        vid: Union[bool, str] = None):
    userbot = await get_userbot(bot_username)
    Done = None
    try:
        call = await get_call(bot_username)
    except Exception:
        return Done

    file_path = file_path
    audio_stream_quality = MediumQualityAudio()
    video_stream_quality = MediumQualityVideo()
    stream = (AudioVideoPiped(file_path, audio_parameters=audio_stream_quality, video_parameters=video_stream_quality)
              if vid else AudioPiped(file_path, audio_parameters=audio_stream_quality))

    try:
        await call.join_group_call(chat_id, stream, stream_type=StreamType().pulse_stream)
        Done = True
    except NoActiveGroupCall:
        h = await join_assistant(client, chat_id, message_id, userbot, file_path)
        if h:
            try:
                await call.join_group_call(chat_id, stream, stream_type=StreamType().pulse_stream)
                Done = True
            except Exception:
                await client.send_message(chat_id, "**≭︰قم ببدأ مكالمه اولا**", reply_to_message_id=message_id)
    except AlreadyJoinedError:
        await call.leave_group_call(chat_id)
        try:
            await call.join_group_call(chat_id, stream, stream_type=StreamType().pulse_stream)
            Done = True
        except Exception:
            await client.send_message(chat_id, "***≭︰اغلق الاتصال وقم بانشاء مكالمه جديده**",
                                      reply_to_message_id=message_id)
    except TelegramServerError:
        await client.send_message(chat_id, "**≭︰اغلق الاتصال وقم بانشاء مكالمه جديده**", reply_to_message_id=message_id)
    except Exception:
        return Done

    return Done


def seconds_to_min(seconds):
    if seconds is not None:
        seconds = int(seconds)
        d, h, m, s = (
            seconds // (3600 * 24),
            seconds // 3600 % 24,
            seconds % 3600 // 60,
            seconds % 3600 % 60,
        )
        if d > 0:
            return "{:02d}:{:02d}:{:02d}:{:02d}".format(d, h, m, s)
        elif h > 0:
            return "{:02d}:{:02d}:{:02d}".format(h, m, s)
        elif m > 0:
            return "{:02d}:{:02d}".format(m, s)
        elif s > 0:
            return "00:{:02d}".format(s)
    return "-"


async def logs(bot_username, client, message):
    try:
        if await get_logger_mode(bot_username) == "OFF":
            return
        logger = await get_logger(bot_username)
        log = LOGS
        if message.chat.type == ChatType.CHANNEL:
            chat = f"[{message.chat.title}](t.me/{message.chat.username})" if message.chat.username else message.chat.title
            name = f"{message.author_signature}" if message.author_signature else chat
            text = f"**≭︰بدأ تشغيل اغنيه ↯.\n\n≭︰اسم الكروب ↫ ❲ {chat} ❳\n≭︰ايدي الكروب ↫ ❲ {message.chat.id} ❳\n≭︰اسم المشغل : ↫❲ {name} ❳\n\n≭︰امر التشغيل ↫ ❲ {message.text} ❳**"
        else:
            chat = f"[{message.chat.title}](t.me/{message.chat.username})" if message.chat.username else message.chat.title
            user = f"≭︰معرف المشغل ↫ ❲ @{message.from_user.username} ❳" if message.from_user.username else f"≭︰ايدي المشغل ↫ ❲ {message.from_user.id} ❳"
            text = f"**≭︰بدأ تشغيل اغنيه **\n\n**≭︰اسم الكروب ↫ ❲ {chat} ❳**\n**≭︰ايدي الكروب ↫ ❲ {message.chat.id} ❳**\n**≭︰اسم المشغل ↫ ❲ {message.from_user.mention} ❳**\n**{user}**\n\n**≭︰امر التشغيل ↫ ❲ {message.text} ❳**"
        await client.send_message(logger, text=text, disable_web_page_preview=True)
        return await man.send_message(log, text=f"[ @{bot_username} ]\n{text}", disable_web_page_preview=True)
    except:
        pass


@Client.on_message(filters.command(["مين شغل", "م شغل", "مين مشغل"], ""))
async def last_played_user(client: Client, message):
    chat_id = message.chat.id
    bot_username = client.me.username

    last_user_id = db.get(f"{bot_username}_last_user_{chat_id}")
    if not last_user_id:
        return await message.reply_text("**≯︰لا يوجد أحد قام بالتشغيل حتى الآن .**")

    try:
        user = await client.get_users(last_user_id)
        name = user.first_name
        mention = f"[{name}](tg://user?id={last_user_id})"
        await message.reply_text(f"**≯︰آخر من قام بالتشغيل هو :** {mention}")
    except:
        await message.reply_text("**≯︰حدث خطأ في جلب معلومات آخر مشغل .**")


@Client.on_message(filters.command(["/play", "play", "/vplay", "شغل", "تشغيل", "فيد", "فيديو"], ""))
async def play(client: Client, message):
    if await joinch(message):
        return

    bot_username = client.me.username
    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else "levvoid"
    message_id = message.id
    Source = message
    ch = await get_channel(bot_username)
    dev = await get_dev(bot_username)
    devname = await get_dev_name(client, bot_username)
    button = panel_buttons(ch, dev, devname)

    try:
        await message.delete()
    except:
        pass

    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text(
            "**≭︰لا يمكن تشغيلي هنا اضفني الى مجموعه**",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("اضف البوت لمجموعتك", url=f"https://t.me/{bot_username}?startgroup=True")]]
            )
        )

    if not len(message.command) == 1:
        try:
            rep = await message.reply_text("**جاري التشغيل انتظر قليلاً ..🚦**")
        except:
            return

    try:
        call = await get_call(bot_username)
        await call.get_call(chat_id)
    except:
        await remove_active(bot_username, chat_id)

    async def get_requester():
        if Source.views:
            return f"{message.author_signature}" if message.author_signature else message.chat.title
        return f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"

    async def get_photo():
        try:
            if message.from_user:
                user = await client.get_users(message.from_user.id)
                if user.photo and user.photo.big_file_id:
                    return await client.download_media(user.photo.big_file_id)
            if message.chat.photo:
                return await client.download_media(message.chat.photo.big_file_id)
            ahmed = await client.get_chat("cecrr")
            if ahmed.photo:
                return await client.download_media(ahmed.photo.big_file_id)
        except Exception:
            pass
        return "./Shahin/default.jpg"

    async def send_reply(message, photo, title, duration, requester, videoid, button, position=None, start=False):
        title = title[:18] if not start else title
        line1 = "Starting Playing Now" if start else f"Added Track To Playlist : {position if position is not None else '0'}"
        caption = (
            f"**⦿ {line1}**\n\n"
            f"◕ **Song Name:** {title}\n"
            f"◕ **Duration Time:** {duration}\n"
            f"◕ **Request By:** {requester}"
        )
        if not photo or not os.path.exists(photo):
            photo = "./Shahin/default.jpg"
        return await message.reply_photo(
            photo=photo,
            caption=caption,
            reply_markup=InlineKeyboardMarkup(button)
        )

    if not message.reply_to_message:
        if len(message.command) == 1:
            if message.chat.type == ChatType.CHANNEL:
                return await message.reply_text("**≯︰قم كتابة شيئ لتشغيلة .**")
            try:
                name_msg = await client.ask(
                    chat_id,
                    text="**≯︰ارسل اسم او رابط الي تريد تشغيله .**",
                    reply_to_message_id=message_id,
                    filters=filters.user(user_id),
                    timeout=200
                )
                name = name_msg.text
                rep = await message.reply_text("**جاري التشغيل انتظر قليلاً ..🚦**")
            except:
                return
        else:
            name = message.text.split(None, 1)[1]

        try:
            results = VideosSearch(name, limit=1)
            response = await results.next()
            if not response.get("result"):
                return await rep.edit("**≯︰تعذر العثور على الفيديو أو لم يتم التعرف عليه .**")
            result = response["result"][0]
        except Exception:
            return await rep.edit("**≯︰حدث خطأ أثناء البحث عن الفيديو .**")

        title, duration, videoid, yturl = result["title"], result["duration"], result["id"], result["link"]
        vid = "v" in message.command[0] or "ف" in message.command[0]
        await rep.edit("**جاري التشغيل انتظر قليلاً ..⚡**")

        if await is_served_call(client, chat_id):
            await add(chat_id, bot_username, None, yturl, title, duration, videoid, vid, user_id)
            db[f"{bot_username}_last_user_{chat_id}"] = user_id
            position = len(db.get(f"{bot_username}{chat_id}")) - 1
            requester = await get_requester()
            photo = await gen_thumb(videoid, await get_photo(), bot_username, client)
            await send_reply(message, photo, title, duration, requester, videoid, button, position)
        else:
            await add_active_chat(chat_id)
            await add_served_call(client, chat_id)
            if vid:
                await add_active_video_chat(chat_id)
            file_path = await download(bot_username, yturl, vid)
            if file_path in ["auth_error", "download_failed", None]:
                await rep.edit("**≯︰حدث خطأ اثناء تحميل الفيديو.**")
                return
            await add(chat_id, bot_username, file_path, yturl, title, duration, videoid, vid, user_id)
            db[f"{bot_username}_last_user_{chat_id}"] = user_id
            c = await join_call(client, message_id, chat_id, bot_username, file_path, yturl, vid)
            if not c:
                await remove_active(bot_username, chat_id)
                return await rep.delete()
            requester = await get_requester()
            photo = await gen_thumb(videoid, await get_photo(), bot_username, client)
            await send_reply(message, photo, title, duration, requester, videoid, button, start=True)

        await logs(bot_username, client, message)
        await rep.delete()

    else:
        if not message.reply_to_message.media:
            return
        rep = await message.reply_text("**≯︰جاري تشغيل الملف انتظر قليلا 🚦 .**")
        vid = bool(message.reply_to_message.video or message.reply_to_message.document)
        file_path = await message.reply_to_message.download()

        media = (
                message.reply_to_message.audio or
                message.reply_to_message.voice or
                message.reply_to_message.video or
                message.reply_to_message.document
        )
        if media is None:
            await rep.edit("**≯︰الرد لا يحتوي على ملف صوتي أو فيديو صالح.**")
            return

        title = getattr(media, "file_name", "ملف بدون اسم")
        duration = seconds_to_min(getattr(media, "duration", 0))
        link = None
        videoid = None

        photo = await get_photo()

        if await is_served_call(client, chat_id):
            await add(chat_id, bot_username, file_path, link, title, duration, videoid, vid, user_id)
            db[f"{bot_username}_last_user_{chat_id}"] = user_id
            position = len(db.get(f"{bot_username}{chat_id}")) - 1
            requester = await get_requester()
            await send_reply(message, photo, title, duration, requester, videoid, button, position)
        else:
            await add_active_chat(chat_id)
            await add_served_call(client, chat_id)
            if vid:
                await add_active_video_chat(chat_id)
            await add(chat_id, bot_username, file_path, link, title, duration, videoid, vid, user_id)
            db[f"{bot_username}_last_user_{chat_id}"] = user_id
            c = await join_call(client, message_id, chat_id, bot_username, file_path, link, vid)
            if not c:
                await remove_active(bot_username, chat_id)
                return await rep.delete()
            requester = await get_requester()
            await send_reply(message, photo, title, duration, requester, videoid, button, start=True)

        await logs(bot_username, client, message)
        await rep.delete()

    try:
        os.remove(file_path)
        os.remove(photo)
    except:
        pass
