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
from config import PHOTO,LOGS, CHANNEL
from Source.play import join_call, logs
from Source.info import (db, add, is_served_call, add_active_video_chat, add_served_call, add_active_chat, gen_thumb, download, remove_active, joinch)
from Source.Data import (get_logger, get_userbot, get_call, get_dev, get_dev_name,get_logger_mode, get_group, get_channel)
import asyncio
from pyrogram.errors import PeerIdInvalid

@Client.on_message(filters.command(["عشوائي", "تشغيل عشوائي"], ""))
async def aii(client: Client, message):
    if await joinch(message):
        return
    try:
        chat_id = message.chat.id
        bot_username = client.me.username
        rep = None
        try:
            rep = await message.reply_text("**≯︰انتظر جاري الاختيار العشوائي**")
        except Exception:
            pass

        try:
            call = await get_call(bot_username)
        except:
            await remove_active(bot_username, chat_id)

        try:
            await call.get_call(message.chat.id)
        except pytgcalls.exceptions.GroupCallNotFound:
            await remove_active(bot_username, chat_id)

        message_id = message.id
        user = await get_userbot(bot_username)
        req = message.from_user.mention if message.from_user else message.chat.title
        raw_list = []

        async for msg in user.get_chat_history("ELNQYBMUSIC"):
            if msg.audio:
                raw_list.append(msg)

        x = random.choice(raw_list)
        file_path = await x.download()
        file_name = x.audio.title
        title = file_name
        dur = x.audio.duration
        duration = seconds_to_min(dur)
        photo = PHOTO
        vid = True if x.video else None
        chat_id = message.chat.id
        user_id = message.from_user.id if message.from_user else 7792403815
        videoid = None
        link = None

        await add(message.chat.id, bot_username, file_path, link, title, duration, videoid, vid, user_id)

        if not await is_served_call(client, message.chat.id):
            await add_active_chat(chat_id)
            await add_served_call(client, chat_id)
            if vid:
                await add_active_video_chat(chat_id)
            link = None
            c = await join_call(client, message_id, chat_id, bot_username, file_path, link, vid)
            if not c:
                await remove_active(bot_username, chat_id)
                if rep:
                    try:
                        await rep.delete()
                    except Exception:
                        pass
                return

        if rep:
            try:
                await rep.delete()
            except Exception:
                pass
        button = panel_buttons(ch, dev, devname)

        try:
            await message.reply_photo(
                photo=photo,
                caption=f"**≯︰بدأ التشغيل العشوائي 🎶 **\n\n**≯︰مده الاغنيه ↫ ❲ {duration} ❳**\n**≯︰طلبت من ↫ ❲ {req} ❳**",
                reply_markup=InlineKeyboardMarkup(button)
            )
        except Exception:
            pass

        await logs(bot_username, client, message)
        await asyncio.sleep(4)


    except Exception:
        pass


@Client.on_message(filters.command(["❲ تشغيل مخصص ❳", "❲ تشغيل في قناه او مجموعه ❳"], ""))
async def pla1y(client: Client, message):
    if await joinch(message):
        return
    YouSef = message
    bot_username = client.me.username
    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else 6094238403
    message_id = message.id
    gr = await get_group(bot_username)
    ch = await get_channel(bot_username)

    if not message.reply_to_message:
        if len(message.command) == 1:
            if message.chat.type == ChatType.CHANNEL:
                return await message.reply_text("**قم كتابة شيئ لتشغيلة.**")
            try:
                ask = await client.ask(message.chat.id, "ارسل معرف المجموعه", reply_to_message_id=message.id, filters=filters.user(message.from_user.id), timeout=20)
                GUS = ask.text
                ushh = (await client.get_chat(GUS)).id
                chat_id = ushh
            except:
                return
            try:
                name = await client.ask(message.chat.id, text="**ارسل اسم او رابط الي تريد تشغيله.**", reply_to_message_id=message.id, filters=filters.user(message.from_user.id), timeout=20)
                name = name.text
                rep = await message.reply_text("**جاري التشغيل انتظر قليلا.**")
            except:
                return
        else:
            name = message.text.split(None, 1)[1]

        try:
            results = VideosSearch(name, limit=1)
        except Exception:
            return await rep.edit("**لم يتم العثور علي نتائج.**")

        for result in (await results.next())["result"]:
            title = result["title"]
            duration = result["duration"]
            videoid = result["id"]
            yturl = result["link"]
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]

        if "v" in message.command[0] or "ف" in message.command[0]:
            vid = True
        else:
            vid = None

        await rep.edit("**جاري التشغيل انتظر قليلا ⚡ .**")
        results = YoutubeSearch(name, max_results=5).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"

        if await is_served_call(client, ushh):
            chat_id = ushh
            title = title.title()
            file_path = None
            await add(ushh, bot_username, file_path, link, title, duration, videoid, vid, user_id)
            chat = f"{bot_username}{chat_id}"
            position = len(db.get(chat)) - 1
            chatname = f"[{message.chat.title}](https://t.me/{message.chat.username})" if message.chat.username else f"{message.chat.title}"
            chatname = f"{message.author_signature}" if message.author_signature else chatname
            requester = chatname if YouSef.views else f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"


            if message.from_user:
                if message.from_user.photo:
                    photo_id = message.from_user.photo.big_file_id
                elif message.chat.photo:
                    photo_id = message.chat.photo.big_file_id
                else:
                    ouos = await client.get_chat("Y_o_V")
                    photo_id = ouos.photo.big_file_id
            elif message.chat.photo:
                photo_id = message.chat.photo.big_file_id
            else:
                ouos = await client.get_chat("Y_o_V")
                photo_id = ouos.photo.big_file_id


            photo = await client.download_media(photo_id)
            photo = await gen_thumb(videoid, photo, bot_username, client)
            await message.reply_photo(photo=photo, caption=f"Add Track To Playlist » {position}\n\nSong Name : {title[:18]}\nDuration Time : {duration}\nRequests By : {requester}")
            await logs(bot_username, client, message)
        else:
            chat_id = ushh
            title = title.title()
            await add_active_chat(chat_id)
            await add_served_call(client, chat_id)
            if vid:
                await add_active_video_chat(chat_id)
            file_path = await download(bot_username, link, vid)
            await add(ushh, bot_username, file_path, link, title, duration, videoid, vid, user_id)
            c = await join_call(client, message_id, chat_id, bot_username, file_path, link, vid)
            if not c:
                await remove_active(bot_username, chat_id)
            if rep:
                return await rep.delete()
            chatname = f"[{message.chat.title}](https://t.me/{message.chat.username})" if message.chat.username else f"{message.chat.title}"
            chatname = f"{message.author_signature}" if message.author_signature else chatname
            requester = chatname if YouSef.views else f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"


            if message.from_user:
                if message.from_user.photo:
                    photo_id = message.from_user.photo.big_file_id
                elif message.chat.photo:
                    photo_id = message.chat.photo.big_file_id
                else:
                    ouos = await client.get_chat("Y_o_V")
                    photo_id = ouos.photo.big_file_id
            elif message.chat.photo:
                photo_id = message.chat.photo.big_file_id
            else:
                ouos = await client.get_chat("Y_o_V")
                photo_id = ouos.photo.big_file_id


            photo = await client.download_media(photo_id)
            photo = await gen_thumb(videoid, photo, bot_username, client)
            await message.reply_photo(photo=photo, caption=f"Starting Playing Now\n\nSong Name : {title}\nDuration Time : {duration}\nRequests By : {requester}")
            await logs(bot_username, client, message)

        button = panel_buttons(ch, dev, devname)

        if message.chat.type == ChatType.PRIVATE:
            if message.chat.type == ChatType.CHANNEL:
                return await message.reply_text("يمكنك التشغيل بحسابك الخاص فقط.")

        if not len(message.command) == 1:
            rep = await message.reply_text("جاري التشغيل انتظر قليلا.")

        try:
            call = await get_call(bot_username)
        except:
            await remove_active(bot_username, chat_id)

        try:
            await call.get_call(ushh)
        except pytgcalls.exceptions.GroupCallNotFound:
            await remove_active(bot_username, chat_id)
        else:
            if message.reply_to_message and message.reply_to_message.media:
                rep = await message.reply_text("جاري تشغيل الملف انتظر قليلا 🚦 .")
                photo = PHOTO
                if message.reply_to_message.video or message.reply_to_message.document:
                    vid = True
                else:
                    vid = None
                file_path = await message.reply_to_message.download()
                if message.reply_to_message.audio:
                    file_name = message.reply_to_message.audio
                elif message.reply_to_message.voice:
                    file_name = message.reply_to_message.voice
                elif message.reply_to_message.video:
                    file_name = message.reply_to_message.video
                else:
                    file_name = message.reply_to_message.document
                    title = file_name.file_name
                duration = seconds_to_min(file_name.duration)
                link = None

                if await is_served_call(client, ushh):
                    chat_id = ushh
                    videoid = None
                    await add(ushh, bot_username, file_path, link, title, duration, videoid, vid, user_id)
                    chat = f"{bot_username}{chat_id}"
                    position = len(db.get(chat)) - 1
                    chatname = f"[{message.chat.title}](https://t.me/{message.chat.username})" if message.chat.username else f"{message.chat.title}"
                    chatname = f"{message.author_signature}" if message.author_signature else chatname
                    requester = chatname if YouSef.views else f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
                    await message.reply_photo(photo=photo, caption=f"Add Track To Playlist » {position}\n\nSong Name : {title}\nDuration Time {duration}\nRequests By : {requester}", reply_markup=InlineKeyboardMarkup(button))
                    await logs(bot_username, client, message)
                else:
                    chat_id = ushh
                    videoid = None
                    await add_active_chat(chat_id)
                    await add_served_call(client, chat_id)
                    if vid:
                        await add_active_video_chat(chat_id)
                    await add(ushh, bot_username, file_path, link, title, duration, videoid, vid, user_id)
                    c = await join_call(client, message_id, chat_id, bot_username, file_path, link, vid)
                    if not c:
                        await remove_active(bot_username, chat_id)
                    if rep:
                        return await rep.delete()
                    chatname = f"[{message.chat.title}](https://t.me/{message.chat.username})" if message.chat.username else f"{message.chat.title}"
                    chatname = f"{message.author_signature}" if message.author_signature else chatname
                    requester = chatname if YouSef.views else f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
                    await message.reply_photo(photo=photo, caption=f"Starting Playing Now\n\nSong Name : {title}\nDuration Time {duration}\nRequests By : {requester}", reply_markup=InlineKeyboardMarkup(button))
                    await logs(bot_username, client, message)

        try:
            os.remove(file_path)
            os.remove(photo)
        except:
            pass

        await rep.delete()