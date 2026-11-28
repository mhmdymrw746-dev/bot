import os
import telebot
from telebot import types
import yt_dlp
import threading
from flask import Flask

# --- سيرفر وهمي عشان Render ميفصلش ---
app = Flask(__name__)
@app.route('/')
def home():
    return "OK"
threading.Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000))), daemon=True).start()

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
pending_links = {}

MAX_SIZE = 200 * 1024 * 1024  # 200 MB

# --- واجهة فخمة ---
def main_keyboard():
    m = types.InlineKeyboardMarkup(row_width=2)
    m.add(
        types.InlineKeyboardButton("🎬 تيك توك", callback_data="tiktok"),
        types.InlineKeyboardButton("📸 انستجرام", callback_data="insta"),
        types.InlineKeyboardButton("▶️ يوتيوب", callback_data="youtube"),
        types.InlineKeyboardButton("ℹ️ طريقة الاستخدام", callback_data="how"),
    )
    return m

def back_keyboard():
    m = types.InlineKeyboardMarkup()
    m.add(types.InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="home"))
    return m

@bot.message_handler(commands=['start'])
def start(message):
    text = (
        "✦ ━━━━━━━━━━━━━ ✦\n"
        "  👋 أهلاً بيك\n"
        "  🚀 بوت التحميل السريع\n"
        "✦ ━━━━━━━━━━━━━ ✦\n\n"
        "▸ تحميل من تيك توك - انستجرام - يوتيوب\n"
        "▸ بجودة عالية وبدون علامة مائية\n"
        "▸ حتى 200 ميجابايت\n\n"
        "📩 ابعت اللينك دلوقتي وسيب الباقي عليا"
    )
    bot.send_message(message.chat.id, text, reply_markup=main_keyboard())

@bot.callback_query_handler(func=lambda c: True)
def buttons(call):
    bot.answer_callback_query(call.id)
    d = call.data

    if d == "home":
        bot.edit_message_text(
            "✦ ━━━━━━━━━━━━━ ✦\n  🚀 بوت التحميل السريع\n✦ ━━━━━━━━━━━━━ ✦\n\n📩 ابعت اللينك دلوقتي",
            call.message.chat.id, call.message.message_id, reply_markup=main_keyboard())
    elif d == "how":
        bot.edit_message_text(
            "📖 طريقة الاستخدام\n\n"
            "1️⃣ انسخ رابط الفيديو\n"
            "2️⃣ ابعته هنا\n"
            "3️⃣ اختار فيديو أو صوت\n"
            "4️⃣ استنى التحميل\n\n"
            "💡 ملحوظة: لازم الفيديو يكون عام مش خاص",
            call.message.chat.id, call.message.message_id, reply_markup=back_keyboard())
    elif d in ["tiktok", "insta", "youtube"]:
        names = {"tiktok": "تيك توك 🎬", "insta": "انستجرام 📸", "youtube": "يوتيوب ▶️"}
        bot.send_message(call.message.chat.id, f"📩 ابعت لينك {names[d]} دلوقتي")
    elif d.startswith("dl_"):
        _, kind, key = d.split("_")
        url = pending_links.get(key)
        if not url:
            bot.send_message(call.message.chat.id, "⚠️ اللينك انتهى، ابعته تاني")
            return
        msg = bot.send_message(call.message.chat.id, "⏳ جاري التحميل... 0%")
        do_download(call.message.chat.id, url, kind, msg.message_id)

@bot.message_handler(func=lambda m: m.text and m.text.startswith("http"))
def handle_link(message):
    url = message.text.strip()
    key = str(message.message_id)
    pending_links[key] = url

    m = types.InlineKeyboardMarkup(row_width=2)
    m.add(
        types.InlineKeyboardButton("🎬 فيديو عالي الجودة", callback_data=f"dl_video_{key}"),
        types.InlineKeyboardButton("🎵 صوت MP3", callback_data=f"dl_audio_{key}"),
    )
    bot.send_message(message.chat.id,
        "✅ تم استلام الرابط\n\nاختر الصيغة المطلوبة:",
        reply_markup=m)

def progress_hook(d, chat_id, msg_id, last=[0]):
    if d['status'] == 'downloading':
        try:
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            downloaded = d.get('downloaded_bytes', 0)
            if total > 0:
                percent = int(downloaded / total * 100)
                if percent - last[0] >= 20:
                    last[0] = percent
                    bar = "▓" * (percent // 10) + "░" * (10 - percent // 10)
                    bot.edit_message_text(f"⏳ جاري التحميل...\n{bar} {percent}%\n📦 {downloaded//1024//1024} / {total//1024//1024} MB",
                        chat_id, msg_id)
        except:
            pass

def do_download(chat_id, url, kind, msg_id):
    try:
        # --- نجيب معلومات الاول ونتأكد من الحجم ---
        with yt_dlp.YoutubeDL({'quiet': True, 'noplaylist': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'فيديو')[:60]
            filesize = info.get('filesize') or info.get('filesize_approx') or 0

        if filesize > MAX_SIZE:
            bot.edit_message_text(f"❌ الفيديو كبير جداً ({filesize//1024//1024} MB)\nالحد الأقصى 200 MB", chat_id, msg_id)
            return

        if kind == "video":
            opts = {
                'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'merge_output_format': 'mp4',
                'outtmpl': 'dl_%(id)s.%(ext)s',
                'quiet': True,
                'noplaylist': True,
                'progress_hooks': [lambda d: progress_hook(d, chat_id, msg_id)],
            }
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                # لو عمل merge هيبقى mp4
                if not os.path.exists(filename):
                    filename = filename.rsplit('.', 1)[0] + ".mp4"

            size = os.path.getsize(filename)
            if size > MAX_SIZE:
                os.remove(filename)
                bot.edit_message_text("❌ حجم الملف أكبر من 200 MB", chat_id, msg_id)
                return

            bot.edit_message_text("📤 جاري الرفع...", chat_id, msg_id)
            with open(filename, 'rb') as f:
                # من غير اي تاج
                bot.send_video(chat_id, f, caption=title)
            os.remove(filename)
            bot.delete_message(chat_id, msg_id)

        else:
            opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'dl_%(id)s.%(ext)s',
                'quiet': True,
                'noplaylist': True,
                'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
                'progress_hooks': [lambda d: progress_hook(d, chat_id, msg_id)],
            }
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                base = ydl.prepare_filename(info).rsplit('.', 1)[0]
                filename = base + ".mp3"

            size = os.path.getsize(filename)
            if size > MAX_SIZE:
                os.remove(filename)
                bot.edit_message_text("❌ حجم الملف أكبر من 200 MB", chat_id, msg_id)
                return

            bot.edit_message_text("📤 جاري الرفع...", chat_id, msg_id)
            with open(filename, 'rb') as f:
                bot.send_audio(chat_id, f, caption=title, title=title)
            os.remove(filename)
            bot.delete_message(chat_id, msg_id)

    except Exception as e:
        print("Error:", e)
        try:
            bot.edit_message_text("❌ لم يتم التحميل\nجرب رابط آخر، تأكد ان الفيديو عام وليس خاص", chat_id, msg_id)
        except:
            bot.send_message(chat_id, "❌ لم يتم التحميل، جرب رابط آخر")

print("Bot Started...")
bot.delete_webhook(drop_pending_updates=True)
bot.infinity_polling()
