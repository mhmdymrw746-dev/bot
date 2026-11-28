import os, json, asyncio, subprocess, threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ChatMemberHandler, filters, ContextTypes
from flask import Flask
import yt_dlp

TOKEN = os.environ.get("BOT_TOKEN")
DEV_LINK = "https://t.me/TRAN_5"
DEV_USERNAME = "@TRAN_5"
CHANNEL_ID = "@yuoe80"
CHANNEL_LINK = "https://t.me/yuoe80"
BOT_LINK = "https://t.me/oday500310bot"

# ===== الاونر - انت =====
OWNER_ID = 8188263997
BOT_ENABLED = True

BANNED_FILE = "banned.json"
USERS_FILE = "users.json"

try:
    with open(BANNED_FILE) as f: BANNED = set(json.load(f))
except: BANNED = set()
try:
    with open(USERS_FILE) as f: KNOWN_USERS = set(json.load(f))
except: KNOWN_USERS = set()

def save_json(file, data):
    with open(file, "w") as f: json.dump(list(data), f)
def ban_user(uid):
    BANNED.add(uid); save_json(BANNED_FILE, BANNED)

async def is_subscribed(context, user_id):
    try:
        m = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return m.status in ["member", "administrator", "creator"]
    except: return False

async def log_to_channel(context, user, url, platform):
    try:
        name = user.first_name or "بدون اسم"
        username = f"@{user.username}" if user.username else "بدون يوزر"
        await context.bot.send_message(chat_id=CHANNEL_ID,
            text=f"🔥 <b>عضو جديد جرب البوت!</b>\n\n👤 الاسم: {name}\n🆔 اليوزر: {username}\n🆔 الايدي: <code>{user.id}</code>\n🎬 حمل من: {platform}\n🔗 اللينك: {url}",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🚀 جرب البوت", url=BOT_LINK)]]))
    except: pass

def main_menu(user_id):
    buttons = [
        [InlineKeyboardButton("📢 اشترك في القناة", url=CHANNEL_LINK)],
        [InlineKeyboardButton("📩 تواصل مع المطور", url=DEV_LINK)],
        [InlineKeyboardButton("📢 قناة المطور", url=CHANNEL_LINK)],
        [InlineKeyboardButton("ℹ️ ازاي استخدم البوت؟", callback_data="how_to")],
    ]
    if user_id == OWNER_ID:
        buttons.append([InlineKeyboardButton("👑 لوحة تحكم الاونر", callback_data="open_admin")])
    return InlineKeyboardMarkup(buttons)

async def start(update, context):
    user = update.effective_user
    if user.id in BANNED:
        await update.message.reply_text("🚫 انت محظور من البوت للأبد لانك خرجت من القناة!",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📩 كلم المطور لفك الحظر", url=DEV_LINK)]]))
        return
    if not BOT_ENABLED and user.id != OWNER_ID:
        await update.message.reply_text("🔴 البوت مطفي دلوقتي من المطور @TRAN_5\nجرب بعد شوية ⭐",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📢 تابع القناة", url=CHANNEL_LINK)]]))
        return
    if not await is_subscribed(context, user.id):
        await update.message.reply_text("⚠️ <b>لازم تشترك في القناة الاول عشان البوت يشتغل!</b>\n\nاشترك ودوس تحقق 👇",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 اشترك في القناة", url=CHANNEL_LINK)],
                [InlineKeyboardButton("✅ انا اشتركت - تحقق", callback_data="check_sub")],
                [InlineKeyboardButton("📩 المطور", url=DEV_LINK)]
            ]))
        return
    KNOWN_USERS.add(user.id); save_json(USERS_FILE, KNOWN_USERS)
    await update.message.reply_text(f"اهلا بيك يا {user.first_name} 👑🔥\n\nابعت لينك فيديو من TikTok / Instagram / YouTube / Facebook / X\nوهحملهولك على طول 😉\n\nاختار من تحت 👇",
        reply_markup=main_menu(user.id))

async def all_buttons(update, context):
    global BOT_ENABLED
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data
    await query.answer()

    if data == "check_sub":
        if user_id in BANNED:
            await query.answer("🚫 انت محظور للأبد!", show_alert=True); return
        if await is_subscribed(context, user_id):
            KNOWN_USERS.add(user_id); save_json(USERS_FILE, KNOWN_USERS)
            await query.edit_message_text("✅ تمام! انت مشترك، ابعت اللينك دلوقتي 👑🔥",
                reply_markup=main_menu(user_id))
        else:
            await query.answer("❌ لسه مش مشترك! اشترك الاول", show_alert=True)
        return

    if data == "how_to":
        await query.edit_message_text("ℹ️ <b>ازاي تستخدم البوت؟</b>\n\n1️⃣ اشترك في القناة\n2️⃣ انسخ لينك الفيديو من TikTok / Insta / YouTube\n3️⃣ ابعته هنا\n4️⃣ هيجيلك الفيديو على طول بدون علامة مائية ✅\n\n📩 المطور: @TRAN_5",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 اشترك في القناة", url=CHANNEL_LINK)],
                [InlineKeyboardButton("🔙 رجوع", callback_data="back_home")]
            ]))
        return

    if data == "back_home":
        await query.edit_message_text(f"اهلا بيك 👑🔥\n\nابعت لينك الفيديو وهحملهولك على طول 😉",
            reply_markup=main_menu(user_id))
        return

    if data == "open_admin":
        if user_id != OWNER_ID:
            await query.answer("❌ مش ليك!", show_alert=True); return
        status = "🟢 شغال" if BOT_ENABLED else "🔴 مطفي"
        await query.edit_message_text(f"👑 <b>لوحة تحكم الاونر</b>\n\n🤖 حالة البوت: {status}\n👥 المستخدمين: {len(KNOWN_USERS)}\n🚫 المحظورين: {len(BANNED)}",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⏸️ اطفي البوت", callback_data="bot_off")],
                [InlineKeyboardButton("▶️ شغل البوت", callback_data="bot_on")],
                [InlineKeyboardButton("📢 ابعت رسالة لكل الناس", callback_data="broadcast_start")],
                [InlineKeyboardButton("📊 الاحصائيات", callback_data="stats")],
                [InlineKeyboardButton("✅ فك حظر الكل", callback_data="unban_all")],
                [InlineKeyboardButton("🔙 رجوع للقايمة", callback_data="back_home")]
            ]))
        return

    if user_id != OWNER_ID and data in ["bot_off", "bot_on", "broadcast_start", "stats", "unban_all"]:
        await query.answer("❌ مش ليك!", show_alert=True); return

    if data == "bot_off":
        BOT_ENABLED = False
        await query.edit_message_text("🔴 البوت اتطفى! محدش هيعرف يستخدمه غيرك",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("▶️ شغل البوت", callback_data="bot_on")],
                [InlineKeyboardButton("🔙 لوحة الاونر", callback_data="open_admin")]
            ]))
        await context.bot.send_message(chat_id=CHANNEL_ID, text="🔴 البوت مطفي دلوقتي للصيانة، هنرجع قريب ⭐")
    elif data == "bot_on":
        BOT_ENABLED = True
        await query.edit_message_text("🟢 البوت اشتغل تاني! 🔥",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⏸️ اطفي البوت", callback_data="bot_off")],
                [InlineKeyboardButton("🔙 لوحة الاونر", callback_data="open_admin")]
            ]))
        await context.bot.send_message(chat_id=CHANNEL_ID, text="🟢 البوت اشتغل تاني! ابعتوا اللينكات 👑🔥")
    elif data == "broadcast_start":
        context.user_data["waiting_broadcast"] = True
        await query.edit_message_text("📢 ابعت الرسالة اللي عايز تبعتها لكل الناس دلوقتي:\n(نص / صورة / فيديو / اي حاجة)",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ الغاء", callback_data="open_admin")]]))
    elif data == "stats":
        await query.edit_message_text(f"📊 الاحصائيات:\n\n👥 المستخدمين: {len(KNOWN_USERS)}\n🚫 المحظورين: {len(BANNED)}\n🤖 الحالة: {'🔴 مطفي' if not BOT_ENABLED else '🟢 شغال'}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 لوحة الاونر", callback_data="open_admin")]]))
    elif data == "unban_all":
        BANNED.clear(); save_json(BANNED_FILE, BANNED)
        await query.edit_message_text("✅ تم فك حظر الكل!",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 لوحة الاونر", callback_data="open_admin")]]))

async def broadcast_handler(update, context):
    if update.effective_user.id == OWNER_ID and context.user_data.get("waiting_broadcast"):
        context.user_data["waiting_broadcast"] = False
        sent, failed = 0, 0
        await update.message.reply_text(f"⏳ جاري الارسال لـ {len(KNOWN_USERS)} واحد...",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("👑 لوحة الاونر", callback_data="open_admin")]]))
        for uid in list(KNOWN_USERS):
            try:
                await context.bot.copy_message(chat_id=uid, from_chat_id=update.effective_chat.id, message_id=update.message.message_id)
                sent += 1
            except: failed += 1
            await asyncio.sleep(0.05)
        await update.message.reply_text(f"✅ تم!\n\n📩 وصلت لـ: {sent}\n❌ فشل: {failed}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("👑 لوحة الاونر", callback_data="open_admin")]]))
        return True
    return False

def get_platform(url):
    if "tiktok" in url: return "TikTok"
    if "instagram" in url: return "Instagram"
    if "youtube" in url or "youtu.be" in url: return "YouTube"
    if "facebook" in url or "fb." in url: return "Facebook"
    if "twitter" in url or "x.com" in url: return "Twitter / X"
    return "فيديو"

def add_watermark(inp, out):
    cmd = ["ffmpeg", "-y", "-i", inp, "-vf", "drawtext=text='Adi Amr | @TRAN_5':fontcolor=white:fontsize=28:box=1:boxcolor=black@0.6:boxborderw=8:x=w-tw-20:y=h-th-20", "-c:a", "copy", out]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return out if os.path.exists(out) else inp

async def handle_message(update, context):
    user = update.effective_user
    if await broadcast_handler(update, context): return
    url = update.message.text.strip() if update.message.text else ""
    if not url.startswith("http"):
        await update.message.reply_text("❌ ابعت لينك فيديو صحيح!", reply_markup=main_menu(user.id)); return
    if user.id in BANNED:
        await update.message.reply_text("🚫 انت محظور من البوت للأبد لانك خرجت من القناة!",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📩 كلم المطور", url=DEV_LINK)]])); return
    if not BOT_ENABLED and user.id != OWNER_ID:
        await update.message.reply_text("🔴 البوت مطفي دلوقتي من المطور @TRAN_5\nجرب بعد شوية ⭐",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📢 تابع القناة", url=CHANNEL_LINK)]])); return
    if not await is_subscribed(context, user.id):
        if user.id in KNOWN_USERS:
            ban_user(user.id)
            await update.message.reply_text("👋 لقد خرجت من القناة مع سلامة ⭐\n\n🚫 تم حظرك من البوت للأبد!\nعشان ترجع كلم المطور: @TRAN_5",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📩 كلم المطور لفك الحظر", url=DEV_LINK)]]))
            return
        await update.message.reply_text("⚠️ <b>البوت مش هيشتغل!</b>\n\nانت مش مشترك في القناة\nاشترك الاول 👇", parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📢 اشترك في القناة", url=CHANNEL_LINK)],[InlineKeyboardButton("✅ انا اشتركت - تحقق", callback_data="check_sub")]]))
        return
    KNOWN_USERS.add(user.id); save_json(USERS_FILE, KNOWN_USERS)
    platform = get_platform(url)
    msg = await update.message.reply_text("⏳ جاري التحميل... 🔥")
    try:
        await log_to_channel(context, user, url, platform)
        os.makedirs("downloads", exist_ok=True)
        ydl_opts = {'format': 'best[ext=mp4]/best', 'outtmpl': 'downloads/%(id)s.%(ext)s', 'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
        final_file = add_watermark(file_path, file_path.replace(".mp4", "_wm.mp4"))
        await update.message.reply_video(video=open(final_file, 'rb'),
            caption=f"✅ تم التحميل بنجاح\n\n📩 المطور: {DEV_USERNAME}\n📢 القناة: {CHANNEL_LINK}\n\n🔗 رابط الفيديو الأصلي: {url}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📩 تواصل مع المطور", url=DEV_LINK)],
                [InlineKeyboardButton("📢 قناة المطور", url=CHANNEL_LINK)],
                [InlineKeyboardButton("🔄 حمل فيديو تاني", callback_data="back_home")]
            ]))
        await msg.delete()
        try: os.remove(file_path); os.remove(final_file)
        except: pass
    except Exception as e:
        print(e); await msg.edit_text(f"❌ حصل خطأ!\nكلم المطور: {DEV_USERNAME}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📩 المطور", url=DEV_LINK)]]))

async def on_leave(update, context):
    try:
        member = update.chat_member
        if member.chat.username != "yuoe80": return
        if member.new_chat_member.status in ["left", "kicked"]:
            user = member.from_user; ban_user(user.id)
            try: await context.bot.send_message(chat_id=user.id, text="👋 لقد خرجت من القناة مع سلامة ⭐\n\n🚫 تم حظرك من البوت للأبد!\nلو عايز ترجع كلم المطور: @TRAN_5",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📩 كلم المطور", url=DEV_LINK)]]))
            except: pass
            await context.bot.send_message(chat_id=CHANNEL_ID, text=f"👋 واحد خرج من القناة واتحظر! 🚫\n👤 {user.first_name} - @{user.username or 'بدون يوزر'}")
    except Exception as e: print(e)

# ===== Flask عشان Render =====
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is Running 👑🔥 - Adi Amr | @TRAN_5"

@flask_app.route('/health')
def health():
    return "OK"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)

def main():
    threading.Thread(target=run_flask, daemon=True).start()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(all_buttons))
    app.add_handler(ChatMemberHandler(on_leave, ChatMemberHandler.CHAT_MEMBER))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
