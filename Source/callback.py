from pyrogram import filters, Client 
from config import OWNER_NAME, OWNER, GROUP
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from Source.Data import get_dev, get_group, get_dev_name, get_bot_name, get_channel, get_dev_name

@Client.on_callback_query(filters.regex("arbic"))
async def arbic(client: Client, query: CallbackQuery):
    bot = client.me
    bot_username = client.me.username
    BOT_NAME = await get_bot_name(bot_username)
    ch = await get_channel(bot.username)  
    dev = await get_dev(bot.username) 
    await query.answer("القائمة الرئيسية")
    await query.edit_message_text(
    f"**اهلا بك في بوت ↫  {BOT_NAME} \n\n**"
    f"**بوت خاص لتشغيل الأغاني الصوتية والمرئية.\n**"
    f"**قم بإضافة البوت إلى مجموعتك أو قناتك.\n**"
    f"**سيتم تفعيل البوت وانضمام المساعد.\n**"
    f"**استخدم الأزرار لمعرفة أوامر الاستخدام.**",
    reply_markup=InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("❲ لتنصيب بوت مماثل ❳", url=f"https://t.me/{OWNER[0]}")],  
            
            [InlineKeyboardButton("❲ اوامر التشغيل ❳", callback_data="bcmds"),
             InlineKeyboardButton("❲ اوامر التفعيل ❳", callback_data="bhowtouse")],
             
            [InlineKeyboardButton("❲ قناة البوت ❳", url=f"{ch}"),
             InlineKeyboardButton("❲ المطور ❳", user_id=int(dev))],  
             
            [InlineKeyboardButton("❲ 𝖺𝖣𝖣 𝖬𝖾 𝖳𝗈 𝖸𝗈𝗎𝗋 𝖦𝗋𝗈𝗎𝗉𝗌 ❳", url=f"https://t.me/{bot.username}?startgroup=true")]
        ]
    ),
    disable_web_page_preview=True 
)

@Client.on_callback_query(filters.regex("english"))
async def english(client: Client, query: CallbackQuery):
    bot = client.me
    ch = await get_channel(bot.username)
    gr = await get_group(bot.username)
    dev = await get_dev(bot.username)
    devname = await get_dev_name(client, bot.username)
    await query.answer("Home Start")
    await query.edit_message_text(
    f"""**≯︰Hello ↫ ❲ {query.from_user.mention} ❳ \n\n≯︰I am a bot to play songs in calls\n≯︰I can play in a group or channel\n≯︰Just add me and raise me as a moderator **""",
        reply_markup=InlineKeyboardMarkup(
            [ 
                [
                    InlineKeyboardButton(
                        "Add me to your Group",
                        url=f"https://t.me/{bot.username}?startgroup=true",
                    )
                ],
                [
                    InlineKeyboardButton("Donate", url=f"https://t.me/{OWNER[0]}")
                ],
                [
                    InlineKeyboardButton("Commands", callback_data="cbcmds"),
                    InlineKeyboardButton("Basic Guide", callback_data="cbhowtouse")
                ],
                [
                    InlineKeyboardButton(
                        "Group", url=f"{GROUP}"
                    ),
                    InlineKeyboardButton(
                        "Channel", url=f"{ch}"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        f"{devname}", user_id=f"{dev}"
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )



@Client.on_callback_query(filters.regex("cbcmds"))
async def cbcmds(_, query: CallbackQuery):
    await query.answer("commands menu")
    await query.edit_message_text(
        f""" **هلو [{query.message.from_user.first_name}](tg://user?id={query.message.from_user.id}) !**
❲ : **تيست ٢""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Admin Cmd", callback_data="cbadmin"),
                    InlineKeyboardButton("Bisc Cmd", callback_data="cbbasic"),
                ],[
                    InlineKeyboardButton("Sudo Cmd", callback_data="cbsudo")
                ],[
                    InlineKeyboardButton("Go Back ", callback_data="english")
                ],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("cbhowtouse"))
async def cbguides(_, query: CallbackQuery):
    await query.answer("user guide")
    await query.edit_message_text(
        f"""**≯︰طريقه تفعيل البوت ↯.**

**≯︰اضف البوت الى المجموعه او القناة**
**≯︰ارفع البوت ادمن مع كل الصلاحيات**
**≯︰ابدأ مكالمه جماعيه جديده**
**≯︰ارسل تشغيل مع اسم المقطع المطلوب**
**≯︰سينظم المساعد تلقائيا ويبدا التشغيل**
**≯︰في حال واجهت اي مشكلة اخرى يمكنك التواصل مع المطور **
**⚡  Developer by {OWNER_NAME}""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Go Back", callback_data="english")]]
        ),
    )

@Client.on_callback_query(filters.regex("cbbasic"))
async def cbbasic(_, query: CallbackQuery):
    await query.answer("basic commands")
    await query.edit_message_text(
         f"""≯︰اوامر التشغيل في المجموعه او القناة ↯.

≯︰ تشغيل ↫ لتشغيل الموسيقى  
≯︰فيديو  ↫ لتشغيل مقطع فيديو 
≯︰تشغيل عشوائي  ↫ لتشغيل اغنيه عشوائيه 
≯︰ابحث ↫ للبحث في اليوتيوب
≯︰يوت او تنزيل او نزل + اسم الاغنيه ↫ لتحميل Mp3
≯︰حمل + اسم الفيديو ↫ لتحميل فيديو**
**≯︰في حال واجهت اي مشكلة اخرى يمكنك التواصل مع المطور **
**Developer by ⚡ {OWNER_NAME}""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Go Back", callback_data="cbcmds")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbadmin"))
async def cbadmin(_, query: CallbackQuery):
    await query.answer("admin commands")
    await query.edit_message_text(
                f"""≯︰اوامر الادمنيه ↯. 

**≯︰استئناف - لتكمله التشغيل**
**≯︰تخطي ↫ لتخطي المقطع المشغل**
**≯︰ايقاف مؤقت - ايقاف التشغيل موقتأ**
**≯︰ايقاف ≯︰انهاء ↫ لانهاء تشغيل المقطع **
**≯︰تكرار ≯︰كررها ↫ لتكرار تشغيل المقطع**
**≯︰في حال واجهت اي مشكلة اخرى يمكنك التواصل مع المطور**
**⚡  Developer by {OWNER_NAME}**""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Go Back", callback_data="cbcmds")]]
        ),
    )

@Client.on_callback_query(filters.regex("cbsudo"))
async def cbsudo(_, query: CallbackQuery):
    await query.answer("SUDO COMMANDS")
    await query.edit_message_text(
        f"""≯︰اوامر مطورين البوت ↯.
**≯︰الاحصائيات **
**≯︰الكروبات**
**≯︰المشتركين**
**≯︰تعيين اسم البوت **
**≯︰اوامر الاذاعه**
**≯︰تغيير مكان الاشعارات ***
**≯︰تفعيل ≯︰تعطيل الاشعارات**
**≯︰اعدادات الحساب المساعد**
**≯︰في حال واجهت اي مشكلة اخرى يمكنك التواصل مع المطور **
**Developer by ⚡ {OWNER_NAME}""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("❲ للخلف ❳", callback_data="cbcmds")]]
        ),
    )


@Client.on_callback_query(filters.regex("bhowtouse"))
async def acbguides(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**≯︰طريقه تفعيل البوت ↯.**

**≯︰اضف البوت الى المجموعه او القناة**
**≯︰ارفع البوت ادمن مع كل الصلاحيات**
**≯︰ابدأ مكالمه جماعيه جديده**
**≯︰ارسل تشغيل مع اسم المقطع المطلوب**
**≯︰سينظم المساعد تلقائيا ويبدا التشغيل**
**≯︰في حال لم ينضم المساعد راسل الدعم من  هنا  {GROUP}**
**Developer by ⚡ {OWNER_NAME}""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("❲ للخلف ❳", callback_data="arbic")]]
        ),
    )


@Client.on_callback_query(filters.regex("bcmds"))
async def acbcmds(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**≯︰اهلا بك في بوت ↫❲ [{query.from_user.first_name}](tg://user?id={query.from_user.id}) ❳  
≯︰اختر ما تريده من اوامر البوت ↯**.""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("❲ اوامر التشغيل ❳", callback_data="bbasic"),
                    InlineKeyboardButton("❲ اوامر الادمنيه ❳", callback_data="badmin"),
                ],
                [
                    InlineKeyboardButton("❲ اوامر المطورين ❳", callback_data="bsudo"),
                    InlineKeyboardButton("❲ اوامر الحمايه ❳", callback_data="acbsecurity"),
                
                ],
                [
               
                    InlineKeyboardButton("❲ اوامر اضافية ❳", callback_data="jhg")
               
                ],
                [
                    InlineKeyboardButton("❲ القائمه الاساسيه ❳", callback_data="arbic")
                ],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("bbasic"))
async def acbbasic(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**≯︰اوامر التشغيل في المجموعه او القناة ↯.

≯︰تشغيل ↫ لتشغيل الموسيقى  
≯︰فيديو  ↫ لتشغيل مقطع فيديو 
≯︰تشغيل عشوائي  ↫ لتشغيل اغنيه عشوائيه 
≯︰ابحث ↫ للبحث في اليوتيوب
≯︰يوت او تنزيل او نزل + اسم الاغنيه ↫ لتحميل Mp3
≯︰حمل + اسم الفيديو ↫ لتحميل فيديو"
≯︰في حال واجهت اي مشكلة اخرى يمكنك التواصل مع المطور
Developer by ⚡ {OWNER_NAME}**""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("❲ للخلف ❳", callback_data="bcmds")]]
        ),
    )


@Client.on_callback_query(filters.regex("badmin"))
async def acbadmin(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**≯︰اوامر الادمنيه ↯. 

≯︰استئناف - لتكمله التشغيل
≯︰تخطي ↫ لتخطي المقطع المشغل
≯︰ايقاف مؤقت - ايقاف التشغيل موقتأ
≯︰ايقاف ≯︰انهاء ↫ لانهاء تشغيل المقطع 
≯︰تكرار ≯︰كررها ↫ لتكرار تشغيل المقطع
≯︰في حال واجهت اي مشكلة اخرى يمكنك التواصل مع المطور
Developer by ⚡ {OWNER_NAME}**""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("❲ للخلف ❳", callback_data="bcmds")]]
        ),
    )

@Client.on_callback_query(filters.regex("bsudo"))
async def sudo_set(client: Client, query: CallbackQuery):
    await query.answer(" اوامر المطورين")
    await query.edit_message_text(
       f"""**≯︰اوامر مطورين البوت ↯.
≯︰بنك
≯︰الاحصائيات 
≯︰الكروبات
≯︰المشتركين
≯︰تعيين اسم البوت 
≯︰اوامر الاذاعه
≯︰تغيير مكان الاشعارات 
≯︰تفعيل ≯︰تعطيل الاشعارات
≯︰اعدادات الحساب المساعد
≯︰في حال واجهت اي مشكلة اخرى يمكنك التواصل مع المطور
Developer by ⚡ {OWNER_NAME}**""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("❲ للخلف ❳", callback_data="bcmds")]]
        ),
    )
@Client.on_callback_query(filters.regex("acbsecurity"))
async def acbsecurity(_, query: CallbackQuery):
    await query.answer(
        "≯︰اوامر الحماية غير متاحة حاليا. 🚧",
        show_alert=True
    )
    
    
@Client.on_callback_query(filters.regex("youj"))
async def youj(_, query: CallbackQuery):
    await query.answer(
        "اوامر الإضافية غير متاحة حاليا. 🚧",
        show_alert=True
    )    
    
@Client.on_callback_query(filters.regex("jhg"))
async def jhg(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**الاوامر الإضافية ⚡:
┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉
≯︰صراحه » اسئلة صراحه
≯︰الجاسوس » لعبة ترفيهيه 
≯︰تويت » اسئله ترفيهيه
≯︰اعلام » معرفة الاعلام من الصور
≯︰لغز » الغاز مشهوره
≯︰مشاهير » معرفة المشاهير من الصور
≯︰ممثلين » معرفه الممثلين من الصور
≯︰مغنين » معرفه المغنين من الصور
≯︰لاعبين » معرفه اللاعبين من الصور
≯︰لو خيروك » اختار حاجه من اتنين
≯︰تحدي » تحديات مسليه 
≯︰مختلف » معرفه الرمز المختلف
≯︰امثله » امثله معروفه 
≯︰تفكيك » تركب الكلمه المفككه
≯︰فزوره » فزوره مشوره وتحلها
≯︰اسئله » اسئله متنوعه
┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉
⚡️  Developer by 𓏺 {OWNER_NAME}**""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("❲ للخلف ❳", callback_data="bcmds")]]
        ),
    )    
    