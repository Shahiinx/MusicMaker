import yt_dlp
import os
import time
import asyncio
from aiocache import SimpleMemoryCache
from pathlib import Path
from typing import Union
from pyrogram import Client as app
from pyrogram import Client, filters
from pyrogram import Client as client
from yt_dlp import YoutubeDL
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from config import appp, OWNER, OWNER_NAME, infophoto, PHOTO
from pymongo import ASCENDING, DESCENDING
from Source.Data import (get_call, get_app, get_userbot, get_group, get_dev, get_dev_name,  get_dev_id, get_data, get_userbot, get_channel, must_join)
from config import API_ID, API_HASH, MONGO_DB_URL, user, call, logger, logger_mode, botname, helper as ass
from motor.motor_asyncio import AsyncIOMotorClient as _mongo_client_
from pymongo import MongoClient
from youtube_search import YoutubeSearch
from youtubesearchpython.__future__ import VideosSearch
from pytgcalls import PyTgCalls, StreamType
from pyrogram.errors import UserNotParticipant, ChatAdminRequired
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pytgcalls.types import (JoinedGroupCallParticipant,
                             LeftGroupCallParticipant, Update)
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.stream import StreamAudioEnded
from pytgcalls.types.input_stream.quality import (HighQualityAudio,
                                                  HighQualityVideo,
                                                  LowQualityAudio,
                                                  LowQualityVideo,
                                                  MediumQualityAudio,
                                                  MediumQualityVideo)
import aiohttp
from io import BytesIO
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps, ImageFont
import textwrap
from pyrogram import Client
import re
import requests
def change_image_size(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

ouos = PHOTO
cookies_file = "/root/cookies/cookies.txt"

async def get_user_image(user_id, client):
    try:
        user = await client.get_users(user_id)
        if user.photo:
            image_file = await client.download_media(user.photo.big_file_id)
            return Image.open(image_file)
        else:
            return await get_user_image(6094238403, client)
    except Exception:
        async with aiohttp.ClientSession() as session:
            async with session.get(ouos) as response:
                if response.status == 200:
                    image_data = await response.read()
                    return Image.open(BytesIO(image_data))
                else:
                    return Image.new('RGB', (1280, 720), color=(255, 255, 255))

async def gen_thumb(videoid, photo, bot_username, client):
    downloads_path = Path("./downloads")
    downloads_path.mkdir(parents=True, exist_ok=True) 
    output_file = downloads_path / f"{photo}_{videoid}.png"
    if output_file.is_file():
       return str(output_file)
    try:
        dev_id = await get_dev_id(bot_username)
        dev_image = await get_user_image(dev_id, client)
        if dev_image is None:
            dev_image = await get_user_image(6094238403, client)

        url = f"https://www.youtube.com/watch?v={videoid}"
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            try:
                title = result["title"]
                title = re.sub("\W+", " ", title)
                title = title.title()
            except:
                title = "Unsupported Title"
            try:
                duration = result["duration"]
            except:
                duration = "Unknown Mins"
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            try:
                views = result["viewCount"]["short"]
            except:
                views = "Unknown Views"
            try:
                channel = result["channel"]["name"]
            except:
                channel = "Unknown Channel"

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    image_data = await resp.read()
                    thumbnail_image = Image.open(BytesIO(image_data))
                else:
                    return ouos
        youtube_image = thumbnail_image
        youtube_image = change_image_size(1280, 720, youtube_image)
        background = youtube_image.filter(ImageFilter.BoxBlur(5)) 
        enhancer = ImageEnhance.Brightness(background)
        background = enhancer.enhance(0.6)  
        Xcenter = dev_image.width / 2
        Ycenter = dev_image.height / 2
        x1 = Xcenter - 250
        y1 = Ycenter - 250
        x2 = Xcenter + 250
        y2 = Ycenter + 250
        logo = dev_image.crop((x1, y1, x2, y2))
        logo.thumbnail((520, 520), Image.Resampling.LANCZOS)
        logo = ImageOps.expand(logo, border=15, fill="white")
        background.paste(logo, (50, 100))
        draw = ImageDraw.Draw(background)
        font = ImageFont.truetype("./Shahin/font2.ttf", 40)
        font2 = ImageFont.truetype("./Shahin/font2.ttf", 70)
        arial = ImageFont.truetype("./Shahin/font2.ttf", 30)
        para = textwrap.wrap(title, width=32)
        j = 0
        draw.text(
            (600, 150),
            infophoto,
            fill="white",
            stroke_width=2,
            stroke_fill="white",
            font=font2,
        )
        for line in para:
            if j == 1:
                j += 1
                draw.text(
                    (600, 340),
                    f"{line}",
                    fill="white",
                    stroke_width=1,
                    stroke_fill="white",
                    font=font,
                )
            if j == 0:
                j += 1
                draw.text(
                    (600, 280),
                    f"{line}",
                    fill="white",
                    stroke_width=1,
                    stroke_fill="white",
                    font=font,
                )
        views = str(views)
        duration = str(duration)
        channel = str(channel)
        draw.text(
            (600, 450),
            f"Views : {views[:23]}",
            (255, 255, 255),
            font=arial,
        )
        draw.text(
            (600, 500),
            f"Duration : {duration[:23]} Mins",
            (255, 255, 255),
            font=arial,
        )
        draw.text(
            (600, 550),
            f"Channel : {channel}",
            (255, 255, 255),
            font=arial,
        )
        background.save(output_file) 
        return str(output_file)
    except Exception:
        return ouos

db = {}

async def add(
    chat_id,
    bot_username,
    file_path,
    link,
    title,
    duration,
    videoid,
    vid,
    user_id
):
    put = {
        "title": title,
        "dur": duration,
        "user_id": user_id,
        "chat_id": chat_id,
        "vid": vid,
        "file_path": file_path,
        "link": link,
        "videoid": videoid,
        "played": 0,
    }
    chat_key = f"{bot_username}{chat_id}"
    if chat_key not in db:
        db[chat_key] = []
    db[chat_key].append(put)

# Users
# Served Users

async def is_served_user(client, user_id: int) -> bool:
    userdb = await get_data(client)
    userdb = userdb.users
    user = await userdb.find_one({"user_id": user_id})
    return bool(user)  

async def get_served_users(client) -> list:
    userdb = await get_data(client)
    userdb = userdb.users 
    users_list = []
    async for user in userdb.find({"user_id": {"$gt": 0}}):  
        users_list.append(user)
    return users_list

async def add_served_user(client, user_id: int):
    userdb = await get_data(client)
    userdb = userdb.users
    if await is_served_user(client, user_id):  
        return
    return await userdb.insert_one({"user_id": user_id})

async def del_served_user(client, user_id: int):
    chats = await get_data(client)
    chatsdb = chats.users
    if not await is_served_user(client, user_id):
        return
    return await chatsdb.delete_one({"user_id": user_id})

# Served Chats
async def get_served_chats(client) -> list:
    chats = await get_data(client)
    chatsdb = chats.chats
    chats_list = []
    async for chat in chatsdb.find({"chat_id": {"$lt": 0}}):  
        chats_list.append(chat)
    return chats_list

async def is_served_chat(client, chat_id: int) -> bool:
    chats = await get_data(client)
    chatsdb = chats.chats
    chat = await chatsdb.find_one({"chat_id": chat_id})
    return bool(chat)  

async def add_served_chat(client, chat_id: int):
    chats = await get_data(client)
    chatsdb = chats.chats
    if await is_served_chat(client, chat_id):
        return
    return await chatsdb.insert_one({"chat_id": chat_id})

async def del_served_chat(client, chat_id: int):
    chats = await get_data(client)
    chatsdb = chats.chats
    if not await is_served_chat(client, chat_id):
        return
    return await chatsdb.delete_one({"chat_id": chat_id})

# Served Call
activecall = {}

async def get_served_call(bot_username) -> list:
    return activecall[bot_username]


async def is_served_call(client, chat_id: int) -> bool:
    bot_username = client.me.username
    if chat_id not in activecall[bot_username]:
        return False
    else:
        return True


async def add_served_call(client, chat_id: int):
    bot_username = client.me.username
    if chat_id not in activecall[bot_username]:
        activecall[bot_username].append(chat_id)


async def remove_served_call(bot_username, chat_id: int):
    if chat_id in activecall[bot_username]:
        activecall[bot_username].remove(chat_id)

# Active Voice Chats
active = []

async def get_active_chats() -> list:
    return active


async def is_active_chat(chat_id: int) -> bool:
    if chat_id not in active:
        return False
    else:
        return True


async def add_active_chat(chat_id: int):
    if chat_id not in active:
        active.append(chat_id)


async def remove_active_chat(chat_id: int):
    if chat_id in active:
        active.remove(chat_id)


# Active Video Chats
activevideo = []

async def get_active_video_chats() -> list:
    return activevideo


async def is_active_video_chat(chat_id: int) -> bool:
    if chat_id not in activevideo:
        return False
    else:
        return True


async def add_active_video_chat(chat_id: int):
    if chat_id not in activevideo:
        activevideo.append(chat_id)


async def remove_active_video_chat(chat_id: int):
    if chat_id in activevideo:
        activevideo.remove(chat_id)

async def remove_active(bot_username, chat_id: int):
   chat = f"{bot_username}{chat_id}"
   try:
    db[chat] = []
   except:
      pass
   try:
        await remove_active_video_chat(chat_id)
   except:
        pass
   try:
        await remove_active_chat(chat_id)
   except:
        pass
   try:
        await remove_served_call(bot_username, chat_id)
   except:
        pass

async def download(bot_username: str, link: str, video: Union[bool, str] = None):
    loop = asyncio.get_running_loop()
    async def audio_dl():
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": f"downloads/{bot_username}%(id)s.%(ext)s",
            "geo_bypass": True,
            "nocheckcertificate": True,
            "quiet": True,
            "no_warnings": True,
            "cookiefile": cookies_file,
            "extractaudio": True,
            "prefer_ffmpeg": True,
        }
        downloader = yt_dlp.YoutubeDL(ydl_opts)
        info = await asyncio.to_thread(downloader.extract_info, link, download=True)
        file_path = f"downloads/{bot_username}{info['id']}.{info['ext']}"
        return file_path
    if video:
        try:
            proc = await asyncio.create_subprocess_exec(
                "yt-dlp", "-g", "-f", "best[height<=?720][width<=?1280]", link,
                "--cookies", cookies_file,
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            if stdout:
                return stdout.decode().strip().split("\n")[0]
            if stderr:
                raise Exception(f"Error: {stderr.decode().strip()}")
            return None
        except Exception as e:
            print(f"Video download error: {e}")
            return None
    retries = 3
    for attempt in range(retries):
        try:
            return await audio_dl()
        except Exception as e:
            if attempt < retries - 1:
                await asyncio.sleep(5)
                continue
            else:
                print(f"Failed to download after {retries} attempts: {e}")
                return None

async def change_stream(bot_username, client, chat_id):
    try:
        chat = f"{bot_username}{chat_id}"
        check = db.get(chat)
        if not check or not isinstance(check, list) or len(check) == 0:
            await remove_active(bot_username, chat_id)
            try:
                return await client.leave_group_call(chat_id)
            except Exception:
                return
        popped = check.pop(0)
        if not check:
            del db[chat]
            await remove_active(bot_username, chat_id)
            try:
                return await client.leave_group_call(chat_id)
            except Exception:
                return
        data = check[0]
        file_path = data["file_path"]
        title = data["title"]
        dur = data["dur"]
        user_id = data["user_id"]
        video = data["vid"]
        videoid = data["videoid"]
        link = data["link"]
        data["played"] = 0
        audio_stream_quality = MediumQualityAudio()
        video_stream_quality = MediumQualityVideo()
        app = appp[bot_username] 
        if link:
            try:
                file_path = await download(bot_username, link, video)
            except Exception:
                return await app.send_message(chat_id, f"**≭︰حدثت مشكله اثناء تشغيل التالي**")
        stream = (
            AudioVideoPiped(file_path, audio_parameters=audio_stream_quality, video_parameters=video_stream_quality)
            if video else
            AudioPiped(file_path, audio_parameters=audio_stream_quality)
        )
        try:
            await client.change_stream(chat_id, stream)
        except Exception:
            return await app.send_message(chat_id, f"**≭︰حدثت مشكله اثناء تشغيل التالي**")
        from Source.play import panel_buttons
        img = await gen_thumb(videoid, user_id, bot_username, app)
        requester = (await app.get_users(user_id)).mention
        button = await panel_buttons(bot_username)
        await app.send_photo(
            chat_id,
            photo=img,
            caption=f"**⦿ Skipped Streaming..\n\n◕ 𝖲𝗈𝗇𝗀 𝖭𝖺𝗆𝖾 : {title}\n◕ 𝖣𝗎𝗋𝖺𝗍𝗂𝗈𝗇 𝖳𝗂𝗆𝖾 ❲ {dur} ❳\n◕ 𝖱𝖾𝗊𝗎𝖾𝗌𝗍 𝖡𝗒 : ❲ {requester} ❳**",
            reply_markup=InlineKeyboardMarkup(button)
        )
    except Exception as e:
        print(f"خطأ في دالة change_stream: {e}")
        
async def helper(bot_username):
   user = await get_userbot(bot_username)
   gr = await get_group(bot_username)
   @user.on_message(filters.private)
   async def helperuser(client, update):
     if not update.chat.id in ass[bot_username]:
      ass[bot_username].append(update.chat.id)

async def Call(bot_username):
  call = await get_call(bot_username)
  @call.on_kicked()
  @call.on_closed_voice_chat()
  @call.on_left()
  async def stream_services_handler(client, chat_id: int):
     return await remove_active(bot_username, chat_id)

  @call.on_stream_end()
  async def stream_end_handler1(client, update: Update):
    if not isinstance(update, StreamAudioEnded):
        return
    await change_stream(bot_username, client, update.chat_id)

async def joinch(message):
    try:
        if not message.from_user:
            return
        ii = await must_join(message._client.me.username)
        if ii == "معطل":
            return
        cch = await get_channel(message._client.me.username)  
        ch = cch.replace("https://t.me/", "") if cch.startswith("https://t.me/") else cch
        try:
            await message._client.get_chat_member(ch, message.from_user.id)
        except UserNotParticipant:
            try:
                await message.reply(
                    f"**↯︰عذࢪاً عمࢪي انت غيࢪ مشتࢪك بقناه البوت**\n\n**↯︰قنـاة الـبـوت : « {cch} »**",
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("اضـغط هنا للأشتـراك القنـاة 🚦", url=f"https://t.me/{ch}")]]
                    )
                )
            except ChatAdminRequired:
                pass
            return True
        except ChatAdminRequired:
            pass
        except:
            pass

    except Exception as e:
        print(f"حدث خطأ في الكود: {e}")