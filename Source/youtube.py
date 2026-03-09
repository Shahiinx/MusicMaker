import os
import re
import asyncio
import requests
import uuid
from yt_dlp import YoutubeDL
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatType
from youtube_search import YoutubeSearch

cookies_file = "cookies/cookies.txt"
downloads_path = "downloads"
os.makedirs(downloads_path, exist_ok=True)
default_thumb_path = "./Shahin/default.jpg"

def clean_filename(name):
    return re.sub(r'[\\/:"*?<>|⧸]', '', name)

@Client.on_message(filters.command(["/song", "/video", "نزل", "تنزيل", "حمل", "تحميل", "يوت", "بحث"], ""))
async def downloaded(client: Client, message: Message):
    video_commands = ["/video", "حمل", "تحميل"]
    audio_commands = ["/song", "نزل", "تنزيل", "يوت", "بحث"]
    m = None

    if len(message.command) == 1:
        if message.chat.type == ChatType.PRIVATE:
            try:
                ask = await client.ask(message.chat.id, "**↯︰ارسل اسم المقطع الآن**", timeout=30)
            except asyncio.TimeoutError:
                return await message.reply("**↯︰انتهى الوقت، يرجى المحاولة مرة أخرى.**")

            if ask.text:
                query = ask.text
            else:
                return await ask.reply_text("**↯︰لم يتم تلقي أي رد، يرجى المحاولة مرة أخرى.**")

            try:
                m = await ask.reply_text("**↯︰جاري البحث انتظر قليلاً 🔎**")
            except:
                m = None
        else:
            try:
                ask = await client.ask(
                    message.chat.id,
                    "**↯︰ارسل الاسم الآن**",
                    filters=filters.user(message.from_user.id),
                    reply_to_message_id=message.id,
                    timeout=8
                )
            except asyncio.TimeoutError:
                return await message.reply("**↯︰انتهى الوقت، حاول مرة أخرى.**")

            query = ask.text
            try:
                m = await ask.reply_text("**↯︰جاري البحث انتظر قليلاً ⚡**")
            except:
                m = None
    else:
        query = message.text.split(None, 1)[1]
        try:
            m = await message.reply_text("**↯︰جاري البحث انتظر قليلاً 🔎**")
        except:
            m = None

    is_video = message.command[0] in video_commands
    ytdl_data = {}
    thumb_name = None
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        if not results:
            if m:
                try: await m.edit("**↯︰لم يتم العثور على نتائج.**")
                except: pass
            return

        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        safe_title = clean_filename(title)
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = os.path.join(downloads_path, f"{safe_title}.jpg")
        thumb = requests.get(thumbnail, allow_redirects=True)
        with open(thumb_name, "wb") as thumb_file:
            thumb_file.write(thumb.content)
        if not os.path.exists(thumb_name):
            thumb_name = default_thumb_path

        if m:
            try: await m.edit("**↯︰جاري التحميل انتظر قليلاً ⚡**")
            except: pass

        unique_id = uuid.uuid4().hex
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' if is_video else 'bestaudio[ext=m4a]',
            'outtmpl': f'{downloads_path}/{unique_id}.%(ext)s',
            'noplaylist': True,
            'quiet': True,
            'cookiefile': cookies_file,
            'merge_output_format': 'mp4' if is_video else None,
            'extractor_args':{
                'youtube': {
                    'player_client':['android']
                }
            }
        }

        loop = asyncio.get_running_loop()
        try:
            ytdl_data = await asyncio.wait_for(
                loop.run_in_executor(None, download_video, ydl_opts, link),
                timeout=300
            )
        except asyncio.TimeoutError:
            if m:
                try: await m.edit("**↯︰انتهى وقت الانتظار أثناء التحميل، حاول لاحقًا.**")
                except: pass
            return

        if is_video:
            await message.reply_video(
                ytdl_data['file'],
                duration=int(ytdl_data.get("duration", 0)),
                thumb=thumb_name,
                caption=ytdl_data["title"],
                supports_streaming=True
            )
        else:
            await message.reply_audio(
                ytdl_data['file'],
                caption=f"**↯︰Uploader : @{client.me.username}**",
                performer=ytdl_data.get("uploader", "YouTube"),
                title=title,
                duration=int(ytdl_data.get("duration", 0)),
                thumb=thumb_name,
            )
        if m:
            try: await m.delete()
            except: pass
    except Exception as e:
        import traceback
        traceback.print_exc()
        error_text = f"**↯︰حدث خطأ أثناء التحميل:**\n`{e}`"
        if m:
            try: await m.edit(error_text)
            except: await message.reply(error_text)
        else:
            await message.reply(error_text)

def download_video(ydl_opts, link):
    with YoutubeDL(ydl_opts) as ytdl:
        ytdl_data = ytdl.extract_info(link, download=True)
        file_name = ytdl.prepare_filename(ytdl_data)
    return {
        'file': file_name,
        'title': ytdl_data['title'],
        'duration': ytdl_data.get('duration', 0),
        'uploader': ytdl_data.get('uploader')
    }
