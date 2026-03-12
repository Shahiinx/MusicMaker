import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.exceptions import NoActiveGroupCall, TelegramServerError, AlreadyJoinedError
from pyrogram.errors import PeerIdInvalid, ChatAdminRequired, UserAlreadyParticipant, UserNotParticipant
from pyrogram.raw import types
from pyrogram.errors import FloodWait
from Source.Data import get_call, get_userbot, get_dev, get_logger, get_channel

@Client.on_message(filters.regex("^مين في الكول$|^مين ف الكول$|^مين في كول$"))
async def check_call(client, message):
    try:
        call_instance = await get_call(client.me.username)

        try:
            await call_instance.join_group_call(
                message.chat.id,
                AudioPiped("Shahin/CallCheckAudio.mp3"),
                stream_type=StreamType().pulse_stream
            )
        except AlreadyJoinedError:
            pass

        text = "**الموجدين في الكول 👥:\n\n**"
        participants = await call_instance.get_participants(message.chat.id)

        if not participants:
            try:
                await message.reply("**≯︰لا يوجد أحد في المكالمة.**")
            except:
                pass
            await call_instance.leave_group_call(message.chat.id)
            return

        k = 0
        for participant in participants:
            if isinstance(participant.user_id, int):
                try:
                    user = await client.get_users(participant.user_id)
                    status = "🗣 **يتحدث**" if not participant.muted else "👤 **يستمع**"
                    k += 1
                    text += f"**{k}.** {user.mention} - {status}\n"
                except PeerIdInvalid:
                    k += 1
                    text += f"**{k}.** مستخدم غير معروف - 👤 **يستمع**\n"
                except:
                    pass
            else:
                k += 1
                text += f"**{k}.** مستخدم مجهول - 👤 **يستمع**\n"

        text += f"\n**👥 عددهم : {len(participants)}**"
        try:
            await message.reply(text)
        except:
            pass

        try:
            await call_instance.leave_group_call(message.chat.id)
        except:
            pass

    except NoActiveGroupCall:
        try:
            await message.reply("**قم بتشغيل المكالمة أولاً ..🚦\n**")
        except:
            pass

    except TelegramServerError:
        try:
            await message.reply("❗ **حدثت مشكلة، حاول مرة أخرى لاحقًا.**")
        except:
            pass

    except Exception:
        pass

@Client.on_message(filters.service)
async def notify_invite(client, message):
    try:
        if not message.video_chat_members_invited:
            return

        inviter = message.from_user.mention if message.from_user else "مستخدم غير معروف"

        if message.video_chat_members_invited.users:
            invited_users = "، ".join(
                f"[{user.first_name}](tg://user?id={user.id})"
                for user in message.video_chat_members_invited.users
            )
        else:
            invited_users = "لم يتم العثور على مدعوين"

        await message.reply(
            f"**≯︰قام {inviter} بدعوة: {invited_users}**"
        )

    except Exception:
        pass
