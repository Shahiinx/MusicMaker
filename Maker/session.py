import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import (
    PhoneNumberInvalid, PhoneCodeInvalid, PhoneCodeExpired,
    SessionPasswordNeeded, PasswordHashInvalid
)
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import (
    PhoneNumberInvalidError, PhoneCodeInvalidError,
    PhoneCodeExpiredError, SessionPasswordNeededError,
    PasswordHashInvalidError
)
from config import API_ID, API_HASH, CHANNEL, PHOTO

@Client.on_message(filters.text & filters.private)
async def choose_session_type(app, message: Message):
    if message.text.strip() in ["جلسه", "جلسة", "استخراج جلسه", "❲ استخراج جلسه ❳", "استخراج جلسة"]:
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Pyrogram", callback_data="get_pyro")],
                [InlineKeyboardButton("Telethon", callback_data="get_tele")]
            ]
        )
        await message.reply("**≯︰اختر نوع الجلسة التي تريد استخراجها:**", reply_markup=keyboard)


@Client.on_callback_query(filters.regex("get_(pyro|tele)"))
async def start_session_process(app, query: CallbackQuery):
    session_type = query.data.split("_")[1]
    user_id = query.from_user.id
    await query.message.delete()

    try:
        num = await app.ask(user_id, "**≯︰ارسل رقم الهاتف**", timeout=60)
    except asyncio.TimeoutError:
        await app.send_message(user_id, "**≯︰انتهى الوقت حاول مره اخرى..!!**")
        return

    phone = num.text

    if session_type == "pyro":
        client = Client(":memory:", api_id=API_ID, api_hash=API_HASH, in_memory=True)
    else:
        client = TelegramClient(StringSession(), API_ID, API_HASH)

    try:
        await client.connect()
    except:
        return

    try:
        if session_type == "pyro":
            sent_code = await client.send_code(phone)
        else:
            sent_code = await client.send_code_request(phone)
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        await app.send_message(user_id, "**≯︰رقم الهاتف غير صحيح**")
        return

    try:
        code_msg = await app.ask(
            user_id,
            f"**≯︰تم ارسال كود إلى الرقم {phone}**\n"
            "**من فضلك ارسله وبين كل رقم ورقم فاصل**\n"
            "**≯︰مثال: 1 2 3 4 5**",
            filters=filters.text,
            timeout=60
        )
    except asyncio.TimeoutError:
        await app.send_message(user_id, "**≯︰انتهى الوقت حاول مره اخرى..!!**")
        return

    code = code_msg.text.replace(" ", "")

    try:
        if session_type == "pyro":
            await client.sign_in(phone, sent_code.phone_code_hash, code)
        else:
            await client.sign_in(phone, code)
    except (PhoneCodeInvalid, PhoneCodeInvalidError):
        await app.send_message(user_id, "**≯︰الكود غير صحيح**")
        return
    except (PhoneCodeExpired, PhoneCodeExpiredError):
        await app.send_message(user_id, "**≯︰انتهت صلاحية الكود**")
        return
    except (SessionPasswordNeeded, SessionPasswordNeededError):
        try:
            password_msg = await app.ask(user_id, "**≯︰ارسل كلمة السر الآن**", filters=filters.text, timeout=60)
            password = password_msg.text
            if session_type == "pyro":
                await client.check_password(password)
            else:
                await client.sign_in(password=password)
        except (PasswordHashInvalid, PasswordHashInvalidError):
            await app.send_message(user_id, "**≯︰كلمة السر غير صحيحة**")
            return

    session = await client.export_session_string() if session_type == "pyro" else client.session.save()

    try:
        await client.send_message("me", f"**≯︰تم استخراج جلستك {session_type.capitalize()}**\n\n`{session}`\n≯︰احفظها في مكان آمن ولا تشاركها مع أحد")
    except:
        pass

    await app.send_photo(
        user_id,
        photo=PHOTO,
        caption=(
            f"**≯︰عزيزي : {query.from_user.mention}**\n"
            "**≯︰شكراً لك لثقتك بنا**\n\n"
            f"**≯︰جلستك {session_type.capitalize()} :**\n"
            f"`{session}`\n\n"
            "**≯︰تم إرسال نسخة إلى الحافظة أيضاً**"
        ),
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("❲ Source Ch ❳", url=CHANNEL)]]
        )
    )

    await client.disconnect()