import os
import telebot
from telebot import types
import yt_dlp

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# تخزين اللينكات
links = {}

def main_menu():
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("🎬 تحميل فيديو", callback_data="how"),
        types.InlineKeyboardButton("🎵 تحميل صوت", callback_data="how_audio"),
        types.InlineKeyboardButton("📞 تواصل مع عدي", url="https://t.me/odaii4"),
        types.InlineKeyboardButton("🔄 تحديث", callback_data="start")
    )
    return kb

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, 
        "✦ ━━━━━━━━━━━━━━ ✦\n\n"
        "👑 <b>ODAI VIP BOT</b>\n"
        "🎬 <b>أسرع بوت تحميل</b>\n\n"
        "━━━━━━━━━━━━━━\n"
        "📥 <b>تيك توك | يوتيوب</b>\n"
        "📸 <b>انستا | فيس بوك</b>\n"
        "━━━━━━━━━━━━━━\n\n"
        "👇 <b>ابعت اللينك دلوقتي</b>\n"
        "✦ ━━━━━━━━━━━━━━ ✦",
        parse_mode="HTML", reply_markup=main_menu())

@bot.callback_query_handler(func=lambda c: c.data == "start")
def back(c):
    bot.edit_message_text(
        "✦ ━━━━━━━━━━━━━━ ✦\n\n👑 <b>ODAI VIP BOT</b>\n🎬 <b>أسرع بوت تحميل</b>\n\n👇 <b>ابعت اللينك دلوقتي</b>\n✦ ━━━━━━━━━━━━━━ ✦",
        c.message.chat.id, c.message.message_id, parse_mode="HTML", reply_markup=main_menu())
    bot.answer_callback_query(c.id)

@bot.callback_query_handler(func=lambda c: c.data in ["how", "how_audio"])
def how(c):
    bot.answer_callback_query(c.id, "ابعت اللينك الأول 😎", show_alert=True)

@bot.message_handler(func=lambda m: m.text and m.text.startswith("http"))
def ask_quality(m):
    links[m.chat.id] = m.text.strip()
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("🔥 جودة عالية HD", callback_data="dl_high"),
        types.InlineKeyboardButton("⚡ جودة متوسطة", callback_data="dl_mid"),
        types.InlineKeyboardButton("🎵 صوت بس MP3", callback_data="dl_audio"),
        types.InlineKeyboardButton("❌ إلغاء", callback_data="start")
    )
    bot.send_message(m.chat.id,
        "🎬 ━━━━━━━━━━━━━ 🎬\n\n"
        "✅ <b>تمام، لقيت اللينك!</b>\n\n"
        "👇 <b>اختار انت عايز تحمله ازاي:</b>\n"
        "🎬 ━━━━━━━━━━━━━ 🎬",
        parse_mode="HTML", reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data.startswith("dl_"))
def do_dl(c):
    chat_id = c.message.chat.id
    url = links.get(chat_id)
    if not url:
        bot.answer_callback_query(c.id, "ابعت اللينك تاني", show_alert=True)
        return

    bot.edit_message_text("⏳ ━━━━━━━━━━━\n\n📥 <b>جاري التحميل...</b>\n⚡ <i>ثواني والفيديو عندك</i>", chat_id, c.message.message_id, parse_mode="HTML")
    bot.answer_callback_query(c.id)

    try:
        if c.data == "dl_audio":
            opts = {'format': 'bestaudio/best', 'outtmpl': 'audio.%(ext)s', 'quiet': True, 'noplaylist': True}
            mode = "audio"
        elif c.data == "dl_mid":
            opts = {'format': 'mp4[height<=480]/best[height<=480]/best', 'outtmpl': 'video.%(ext)s', 'quiet': True, 'noplaylist': True, 'impersonate': 'chrome'}
            mode = "video"
        else:
            opts = {'format': 'mp4/best/best', 'outtmpl': 'video.%(ext)s', 'quiet': True, 'noplaylist': True, 'impersonate': 'chrome', 'http_headers': {'User-Agent': 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36'}}
            mode = "video"

        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            fname = ydl.prepare_filename(info)
            title = info.get('title', 'فيديو')[:40]

        kb2 = types.InlineKeyboardMarkup()
        kb2.add(types.InlineKeyboardButton("📥 حمل لينك تاني", callback_data="start"))

        if mode == "audio":
            with open(fname, 'rb') as f:
                bot.send_audio(chat_id, f, caption=f"🎵 <b>{title}</b>\n\n✅ <b>تم يا عدي 🔥</b>", parse_mode="HTML", reply_markup=kb2)
        else:
            with open(fname, 'rb') as f:
                bot.send_video(chat_id, f, caption=f"✦ ━━━━━━━━━━━ ✦\n\n🎬 <b>{title}</b>\n\n✅ <b>تم التحميل يا عدي 🔥</b>\n👑 <i>ODAI VIP BOT</i>", parse_mode="HTML", reply_markup=kb2)
        os.remove(fname)
        bot.delete_message(chat_id, c.message.message_id)
    except:
        bot.send_message(chat_id, "⚠️ <b>اللينك محمي، جرب لينك تاني</b>", parse_mode="HTML")

bot.infinity_polling()
