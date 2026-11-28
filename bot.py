# ============================================================
# 👑 BOT: @oday500310bot
# 👨‍💻 DEV: @TRAN_5 - Adi Amr
# 📢 CHANNEL: @yuoe80
# 👑 OWNER: 8188263997
# ============================================================

# ==================== 1 - المكتبات ====================
import os, json, asyncio, subprocess, threading, time, glob, re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ChatMemberHandler, filters, ContextTypes
from flask import Flask
import yt_dlp

# ==================== 2 - الاعدادات ====================
TOKEN = os.environ.get("BOT_TOKEN")
DEV_LINK = "https://t.me/TRAN_5"
DEV_USERNAME = "@TRAN_5"
CHANNEL_ID = "@yuoe80"
CHANNEL_LINK = "https://t.me/yuoe80"
BOT_LINK = "https://t.me/oday500310bot"
OWNER_ID = 8188263997
BOT_ENABLED = True

# ==================== 3 - الحماية العالية ====================
BANNED_FILE = "banned.json"
USERS_FILE = "users.json"
RATE_LIMIT = {}  # منع السبام - كل واحد 1 فيديو كل 10 ثواني
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 ميجا اقصى حجم
BLOCKED_WORDS = ["porn", "xxx", "sex"]

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

def is_spam(user_id):
    now = time.time()
    if user_id in RATE_LIMIT and now - RATE_LIMIT[user_id] < 10:
        return True
    RATE_LIMIT[user_id] = now
    return False

def is_safe_url(url):
    if not url.startswith("http"): return False
    if any(w in url.lower() for w in BLOCKED_WORDS): return False
    allowed = ["tiktok.com", "vt.tiktok.com", "instagram.com", "youtube.com", "youtu.be", "facebook.com", "fb.watch", "fb.gg", "twitter.com", "x.com", "snapchat.com", "pinterest.com", "reddit.com", "threads.net", "kwai.com", "likee.video"]
    return any(d in url.lower() for d in allowed)

# ==================== 4 - الاشتراك ====================
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

# ==================== 5 - القوائم - كله أزرار ====================
def main_menu(user_id):
    buttons = [
        [InlineKeyboardButton("📥 حمل فيديو", callback_data="how_to")],
        [InlineKeyboardButton("📢 اشترك في القناة", url=CHANNEL_LINK)],
        [InlineKeyboardButton("📩 تواصل مع المطور", url=DEV_LINK)],
        [InlineKeyboardButton("📢 قناة المطور", url=CHANNEL_LINK)],
        [InlineKeyboardButton("ℹ️ المنصات المدعومة", callback_data="platforms")],
        [InlineKeyboardButton("🛡️ الحماية", callback_data="protection")],
    ]
    if user_id == OWNER_ID:
        buttons.append([InlineKeyboardButton("👑 لوحة تحكم الاونر", callback_data="open_admin")])
    return InlineKeyboardMarkup(buttons)

def admin_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⏸️ اطفي البوت", callback_data="bot_off"), InlineKeyboardButton("▶️ شغل البوت", callback_data="bot_on")],
        [InlineKeyboardButton("📢 ابعت رسالة لكل الناس", callback_data="broadcast_start")],
        [InlineKeyboardButton("📊 الاحصائيات", callback_data="stats"), InlineKeyboardButton("🚫 المحظورين", callback_data="banned_list")],
        [InlineKeyboardButton("✅ فك حظر الكل", callback_data="unban_all")],
        [InlineKeyboardButton("🔙 رجوع للقايمة", callback_data="back_home")]
    ])

# ==================== 6 - /start ====================
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
    await update.message.reply_text(f"اهلا بيك يا {user.first_name} 👑🔥\n\nبوت تحميل فيديوهات من كل المنصات بدون علامة مائية ✅\n\nاختار من تحت 👇",
        reply_markup=main_menu(user.id))

# ==================== 7 - كل الازرار ====================
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
            await query.edit_message_text("✅ تمام! انت مشترك، ابعت اللينك دلوقتي 👑🔥", reply_markup=main_menu(user_id))
        else:
            await query.answer("❌ لسه مش مشترك! اشترك الاول", show_alert=True)
        return

    if data == "back_home":
        await query.edit_message_text("اهلا بيك 👑🔥\n\nابعت لينك الفيديو وهحملهولك على طول 😉", reply_markup=main_menu(user_id))
        return

    if data == "how_to":
        await query.edit_message_text("📥 <b>ازاي تحمل؟</b>\n\n1️⃣ انسخ لينك الفيديو\n2️⃣ ابعته هنا\n3️⃣ استنى ثواني وهيجيلك الفيديو ✅\n\n📩 المطور: @TRAN_5",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="back_home")]]))
        return

    if data == "platforms":
        await query.edit_message_text("📱 <b>المنصات المدعومة:</b>\n\n✅ TikTok\n✅ Instagram - ريلز / ستوري / بوست\n✅ YouTube - فيديو / شورتس\n✅ Facebook - فيديو / ريلز\n✅ Twitter / X\n✅ Snapchat\n✅ Pinterest\n✅ Reddit\n✅ Threads\n✅ Kwai / Likee",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="back_home")]]))
        return

    if data == "protection":
        await query.edit_message_text("🛡️ <b>الحماية:</b>\n\n✅ اشتراك اجباري في القناة\n✅ اللي يخرج = حظر للأبد\n✅ منع السبام - 1 فيديو كل 10 ثواني\n✅ حظر الروابط المشبوهة\n✅ حد اقصى 50 ميجا\n✅ لوحة اونر محمية بالايدي",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="back_home")]]))
        return

    # ===== لوحة الاونر =====
    if data == "open_admin":
        if user_id != OWNER_ID:
            await query.answer("❌ مش ليك!", show_alert=True); return
        status = "🟢 شغال" if BOT_ENABLED else "🔴 مطفي"
        await query.edit_message_text(f"👑 <b>لوحة تحكم الاونر</b>\n\n🤖 الحالة: {status}\n👥 المستخدمين: {len(KNOWN_USERS)}\n🚫 المحظورين: {len(BANNED)}",
            parse_mode="HTML", reply_markup=admin_menu())
        return

    if user_id != OWNER_ID and data in ["bot_off", "bot_on", "broadcast_start", "stats", "unban_all", "banned_list"]:
        await query.answer("❌ مش ليك!", show_alert=True); return

    if data == "bot_off":
        BOT_ENABLED = False
        await query.edit_message_text("🔴 البوت اتطفى!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("▶️ شغل البوت", callback_data="bot_on")],[InlineKeyboardButton("🔙 لوحة الاونر", callback_data="open_admin")]]))
        await context.bot.send_message(chat_id=CHANNEL_ID, text="🔴 البوت مطفي دلوقتي للصيانة، هنرجع قريب ⭐")
    elif data == "bot_on":
        BOT_ENABLED = True
        await query.edit_message_text("🟢 البوت اشتغل تاني! 🔥", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⏸️ اطفي البوت", callback_data="bot_off")],[InlineKeyboardButton("🔙 لوحة الاونر", callback_data="open_admin")]]))
        await context.bot.send_message(chat_id=CHANNEL_ID, text="🟢 البوت اشتغل تاني! ابعتوا اللينكات 👑🔥")
    elif data == "broadcast_start":
        context.user_data["waiting_broadcast"] = True
        await query.edit_message_text("📢 ابعت الرسالة اللي عايز تبعتها لكل الناس دلوقتي:\n(نص / صورة / فيديو)",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ الغاء", callback_data="open_admin")]]))
    elif data == "stats":
        await query.edit_message_text(f"📊 الاحصائيات:\n\n👥 المستخدمين: {len(KNOWN_USERS)}\n🚫 المحظورين: {len(BANNED)}\n🤖 الحالة: {'🔴 مطفي' if not BOT_ENABLED else '🟢 شغال'}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 لوحة الاونر", callback_data="open_admin")]]))
    elif data == "banned_list":
        if not BANNED:
            txt = "✅ مفيش حد محظور"
        else:
            txt = "🚫 المحظورين:\n" + "\n".join([f"- <code>{b}</code>" for b in list(BANNED)[:20]])
        await query.edit_message_text(txt, parse_mode="HTML", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 لوحة الاونر", callback_data="open_admin")]]))
    elif data == "unban_all":
        BANNED.clear(); save_json(BANNED_FILE, BANNED)
        await query.edit_message_text("✅ تم فك حظر الكل!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 لوحة الاونر", callback_data="open_admin")]]))

# ==================== 8 - الارسال الجماعي ====================
async def broadcast_handler(update, context):
    if update.effective_user.id == OWNER_ID and context.user_data.get("waiting_broadcast"):
        context.user_data["waiting_broadcast"] = False
        sent, failed = 0, 0
        await update.message.reply_text(f"⏳ جاري الارسال لـ {len(KNOWN_USERS)} واحد...")
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

# ==================== 9 - التحميل - كل المنصات ====================
def get_platform(url):
    u = url.lower()
    if "tiktok" in u: return "TikTok"
    if "instagram" in u: return "Instagram"
    if "youtube" in u or "youtu.be" in u: return "YouTube"
    if "facebook" in u or "fb." in u: return "Facebook"
    if "twitter" in u or "x.com" in u: return "Twitter / X"
    if "snapchat" in u: return "Snapchat"
    if "pinterest" in u: return "Pinterest"
    if "reddit" in u: return "Reddit"
    if "threads" in u: return "Threads"
    return "فيديو"

def add_watermark(inp, out):
    try:
        cmd = ["ffmpeg", "-y", "-i", inp, "-vf", "drawtext=text='Adi Amr | @TRAN_5':fontcolor=white:fontsize=28:box=1:boxcolor=black@0.6:boxborderw=8:x=w-tw-20:y=h-th-20", "-c:a", "copy", out]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60)
        if os.path.exists(out) and os.path.getsize(out) > 1000:
            return out
    except: pass
    return inp

async def handle_message(update, context):
    user = update.effective_user
    if await broadcast_handler(update, context): return
    url = update.message.text.strip() if update.message.text else ""

    # حماية: مش لينك
    if not url.startswith("http"):
        await update.message.reply_text("❌ ابعت لينك فيديو صحيح!", reply_markup=main_menu(user.id)); return
    # حماية: لينك مش مدعوم
    if not is_safe_url(url):
        await update.message.reply_text("❌ المنصة دي مش مدعومة!\n\nشوف المنصات المدعومة من الزرار 👇", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📱 المنصات المدعومة", callback_data="platforms")]])); return
    # حماية: محظور
    if user.id in BANNED:
        await update.message.reply_text("🚫 انت محظور من البوت للأبد لانك خرجت من القناة!",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📩 كلم المطور", url=DEV_LINK)]])); return
    # حماية: البوت مطفي
    if not BOT_ENABLED and user.id != OWNER_ID:
        await update.message.reply_text("🔴 البوت مطفي دلوقتي من المطور @TRAN_5\nجرب بعد شوية ⭐",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📢 تابع القناة", url=CHANNEL_LINK)]])); return
    # حماية: سبام
    if user.id != OWNER_ID and is_spam(user.id):
        await update.message.reply_text("⏳ استنى 10 ثواني بين كل فيديو والتاني!"); return
    # حماية: اشتراك
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
    msg = await update.message.reply_text(f"⏳ جاري التحميل من {platform}... 🔥")

    try:
        await log_to_channel(context, user, url, platform)
        os.makedirs("downloads", exist_ok=True)
        for f in glob.glob("downloads/*"): 
            try: os.remove(f)
            except: pass

        # محاولة 1: جودة عالية
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': 'downloads/%(id)s.%(ext)s',
            'quiet': True, 'no_warnings': True, 'noplaylist': True,
            'merge_output_format': 'mp4',
            'http_headers': {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1', 'Referer': 'https://www.tiktok.com/'},
        }
        file_path = None
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
        except:
            # محاولة 2: اي جودة - دي اللي بتنقذ TikTok
            ydl_opts2 = {'format': 'best', 'outtmpl': 'downloads/%(id)s.%(ext)s', 'quiet': True, 'noplaylist': True}
            with yt_dlp.YoutubeDL(ydl_opts2) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)

        if not file_path or not os.path.exists(file_path):
            files = glob.glob("downloads/*")
            if files: file_path = max(files, key=os.path.getctime)
            else: raise Exception("No file")

        # حماية: حجم كبير
        if os.path.getsize(file_path) > MAX_FILE_SIZE:
            await msg.edit_text("❌ الفيديو كبير جدا (اكتر من 50 ميجا)!\nجرب فيديو اقصر",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="back_home")]]))
            return

        final_file = add_watermark(file_path, file_path.rsplit(".", 1)[0] + "_wm.mp4")

        await update.message.reply_video(video=open(final_file, 'rb'),
            caption=f"✅ تم التحميل من {platform}\n\n📩 المطور: {DEV_USERNAME}\n📢 القناة: {CHANNEL_LINK}\n\n🔗 الأصلي: {url}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📩 تواصل مع المطور", url=DEV_LINK)],
                [InlineKeyboardButton("📢 قناة المطور", url=CHANNEL_LINK)],
                [InlineKeyboardButton("🔄 حمل فيديو تاني", callback_data="back_home")]
            ]))
        await msg.delete()
        for f in glob.glob("downloads/*"):
            try: os.remove(f)
            except: pass
    except Exception as e:
        print("DOWNLOAD ERROR:", e)
        await msg.edit_text(f"❌ اللينك ده مش شغال!\n\nجرب:\n1️⃣ انسخ اللينك تاني من مشاركة -> نسخ الرابط\n2️⃣ جرب فيديو تاني\n\nكلم المطور: {DEV_USERNAME}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📩 المطور", url=DEV_LINK)],[InlineKeyboardButton("🔙 رجوع", callback_data="back_home")]]))

# ==================== 10 - اللي يخرج من القناة = حظر ====================
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

# ==================== 11 - Flask + التشغيل ====================
flask_app = Flask(__name__)
@flask_app.route('/')
def home(): return "Bot is Running 👑🔥 - Adi Amr | @TRAN_5"
@flask_app.route('/health')
def health(): return "OK"

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
