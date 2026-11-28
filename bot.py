# -*- coding: utf-8 -*-
# 📥 بوت التحميل - عدي
# 👑 حقوق عدي - جميع الحقوق محفوظة © 2026
# 👑 صنع بواسطة عدي - ممنوع السرقة

import os, time, re, subprocess, traceback, uuid, glob
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

RIGHTS = "👑 حقوق عدي - جميع الحقوق محفوظة © 2026\n👑 صنع بواسطة عدي - ممنوع السرقة"
def fmt_rights():
    return f"\n\n━━━━━━━━━━━━━━\n{RIGHTS}"

# ===== ازرار =====
def main_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("📥 ازاي احمل؟", callback_data="how"),
        InlineKeyboardButton("🎵 تحميل تيك توك", callback_data="tiktok"),
        InlineKeyboardButton("📸 تحميل انستا", callback_data="insta"),
        InlineKeyboardButton("▶️ تحميل يوتيوب", callback_data="youtube"),
        InlineKeyboardButton("📘 تحميل فيس بوك", callback_data="facebook"),
        InlineKeyboardButton("🎵 تحميل اغنية MP3", callback_data="mp3"),
        InlineKeyboardButton("📊 احصائياتي", callback_data="stats"),
        InlineKeyboardButton("👑 حقوق عدي", callback_data="rights"),
        InlineKeyboardButton("🔄 تحديث", callback_data="back"),
    )
    return kb

def after_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("📥 حمل لينك تاني", callback_data="send_link"),
        InlineKeyboardButton("🎵 تحميل تيك توك", callback_data="tiktok"),
        InlineKeyboardButton("📸 تحميل انستا", callback_data="insta"),
        InlineKeyboardButton("▶️ تحميل يوتيوب", callback_data="youtube"),
        InlineKeyboardButton("🏠 القايمة الرئيسية", callback_data="back"),
    )
    return kb

def safe_edit(c, text, kb=None):
    try:
        bot.edit_message_text(text, c.message.chat.id, c.message.message_id, reply_markup=kb)
    except:
        try: bot.send_message(c.message.chat.id, text, reply_markup=kb)
        except: pass

user_stats = {}
def get_stats(uid):
    if uid not in user_stats: user_stats[uid] = {"count": 0}
    return user_stats[uid]

def is_link(text):
    return "http" in text and any(x in text for x in ["tiktok.com","instagram.com","youtube.com","youtu.be","facebook.com","fb.watch","twitter.com","x.com"])

def clean_old_files():
    try:
        for f in glob.glob("dl_*"):
            try: os.remove(f)
            except: pass
    except: pass

def download_video(url, chat_id, is_mp3=False):
    uid = str(uuid.uuid4())[:8]
    out = f"dl_{uid}.%(ext)s"
    # لو MP3
    if is_mp3:
        cmd = ["yt-dlp", "-x", "--audio-format", "mp3", "--audio-quality", "0", "-o", f"dl_{uid}.mp3", "--no-playlist", "--max-filesize", "50M", url]
    else:
        cmd = ["yt-dlp", "-f", "mp4[height<=720]/best[height<=720]/best", "-o", f"dl_{uid}.%(ext)s", "--no-playlist", "--max-filesize", "50M", "--merge-output-format", "mp4", url]
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    files = glob.glob(f"dl_{uid}.*")
    return files[0] if files else None, result.stderr[:500] if result.stderr else ""

@bot.message_handler(commands=['start'])
def start(m):
    st = get_stats(m.from_user.id)
    bot.send_message(m.chat.id,
        f"📥 اهلا يا {m.from_user.first_name} في بوت التحميل!\n\n"
        f"🎵 ابعتلي اي لينك وانا هحملهولك من غير علامة مائية!\n\n"
        f"✅ تيك توك - بدون علامة مائية\n"
        f"✅ انستا - ريلز وستوري وبوست\n"
        f"✅ يوتيوب - فيديو وشورتس\n"
        f"✅ فيس بوك - فيديو وريلز\n"
        f"✅ اغنية MP3 من اي لينك\n\n"
        f"📊 حملت: {st['count']} فيديو\n"
        f"👇 دوس على اي زرار، او ابعت اللينك على طول!"
        f"{fmt_rights()}",
        reply_markup=main_kb())

@bot.message_handler(content_types=['text'])
def handle_text(m):
    text = m.text.strip()
    # لو لينك
    if is_link(text):
        do_download(m, text, False)
        return
    # لو مش لينك - رجعه للازرار
    bot.send_message(m.chat.id, "📥 ابعتلي لينك الفيديو على طول 👇\n\nمثال:\nhttps://www.tiktok.com/...\nhttps://www.instagram.com/reel/...", reply_markup=main_kb())

@bot.callback_query_handler(func=lambda c: True)
def callbacks(c):
    uid = c.from_user.id
    try:
        st = get_stats(uid)
        d = c.data or ""
        try: bot.answer_callback_query(c.id)
        except: pass

        if d == "back":
            safe_edit(c, f"📥 بوت التحميل - عدي\n\nابعت لينك الفيديو وانا هحملهولك 👇{fmt_rights()}", main_kb()); return
        if d == "how":
            safe_edit(c, f"📥 ازاي تحمل؟ - كله ازرار\n\n1️⃣ روح تيك توك / انستا / يوتيوب\n2️⃣ دوس مشاركة -> نسخ الرابط\n3️⃣ تعال هنا وابعت اللينك\n4️⃣ استنى 10 ثواني وهيجيلك الفيديو من غير علامة مائية\n\n💡 جرب دلوقتي - ابعت اي لينك{fmt_rights()}", main_kb()); return
        if d == "send_link":
            safe_edit(c, f"📥 ابعت اللينك دلوقتي\n\nانسخ لينك الفيديو وابعته هنا 👇", main_kb()); return
        if d == "tiktok":
            safe_edit(c, f"🎵 تحميل تيك توك\n\nابعت لينك فيديو التيك توك وانا هجيبهولك من غير علامة مائية 💧\n\n👇 ابعت اللينك", main_kb()); return
        if d == "insta":
            safe_edit(c, f"📸 تحميل انستا\n\nابعت لينك الريلز او البوست او الستوري\nوانا هحملهولك 👇", main_kb()); return
        if d == "youtube":
            safe_edit(c, f"▶️ تحميل يوتيوب\n\nابعت لينك فيديو يوتيوب او شورتس\nوانا هحملهولك بجودة عالية 👇", main_kb()); return
        if d == "facebook":
            safe_edit(c, f"📘 تحميل فيس بوك\n\nابعت لينك فيديو الفيس او الريلز\nوانا هحملهولك 👇", main_kb()); return
        if d == "mp3":
            safe_edit(c, f"🎵 تحميل اغنية MP3\n\nابعت لينك الفيديو وانا هحولهولك اغنية MP3\n\n💡 دوس على الزرار ده بعد ما تبعت اللينك؟ لا - ابعت اللينك وهقولك تختار فيديو ولا اغنية\n\n👇 ابعت اللينك", main_kb()); return
        if d == "stats":
            safe_edit(c, f"📊 احصائياتك\n\n👤 {c.from_user.first_name}\n📥 حملت: {st['count']} فيديو{fmt_rights()}", main_kb()); return
        if d == "rights":
            safe_edit(c, f"👑 حقوق عدي\n\n👑 صنع بواسطة عدي\n👑 جميع الحقوق محفوظة لـ عدي © 2026\n👑 ممنوع السرقة او النسخ", main_kb()); return
        # ازرار اختيار فيديو ولا اغنية بعد اللينك
        if d.startswith("dl_"):
            parts = d.split("_", 2)
            if len(parts) == 3:
                mode = parts[1]  # video or mp3
                url = parts[2]
                # هنبعت رسالة وهمية عشان نستخدم نفس دالة التحميل
                class FakeMsg: pass
                fake = FakeMsg()
                fake.chat = c.message.chat
                fake.from_user = c.from_user
                do_download(fake, url, mode == "mp3", edit_msg=c)
            return

        safe_edit(c, f"📥 بوت التحميل - عدي{fmt_rights()}", main_kb())
    except Exception as e:
        print(e); traceback.print_exc()

def do_download(m, url, is_mp3=False, edit_msg=None):
    chat_id = m.chat.id
    uid = m.from_user.id
    st = get_stats(uid)
    # لو اول مرة - اسأله فيديو ولا اغنية عن طريق ازرار
    if not is_mp3 and edit_msg is None:
        kb = InlineKeyboardMarkup(row_width=2)
        # نختصر اللينك في الكول باك - هنستخدم اخر جزء بس عشان تليجرام ليه حد 64 حرف
        # هنخزن اللينك في dict
        key = str(uuid.uuid4())[:8]
        pending_links[key] = url
        kb.add(
            InlineKeyboardButton("🎬 فيديو MP4", callback_data=f"dl_video_{key}"),
            InlineKeyboardButton("🎵 اغنية MP3", callback_data=f"dl_mp3_{key}"),
        )
        bot.send_message(chat_id, f"📥 لقيت اللينك!\n\nتحب احملهولك ايه؟ 👇\n\n{url[:80]}...", reply_markup=kb)
        return

    # لو جاي من زرار - نفذ التحميل
    msg = bot.send_message(chat_id, f"⏳ بحمل دلوقتي... استنى 10-20 ثانية 📥\n\n{url[:60]}...")
    try:
        # لو is_mp3 جاي من زرار - لازم نجيب اللينك الحقيقي
        real_url = url
        # لو url هو key - نجيبه من pending
        if url in pending_links:
            real_url = pending_links[url]
        file_path, err = download_video(real_url, chat_id, is_mp3=is_mp3)
        if file_path and os.path.exists(file_path):
            st["count"] += 1
            size = os.path.getsize(file_path) / 1024 / 1024
            if is_mp3:
                with open(file_path, "rb") as f:
                    bot.send_audio(chat_id, f, caption=f"🎵 اغنيتك جاهزة!\n\n📥 حملت: {st['count']} حاجة\n{fmt_rights()}", reply_markup=after_kb())
            else:
                if size > 48:
                    bot.send_message(chat_id, f"❌ الفيديو كبير اوي ({size:.1f} MB) - تليجرام مش بيقبل اكتر من 50 MB\n\nجرب فيديو اصغر 👇", reply_markup=after_kb())
                else:
                    with open(file_path, "rb") as f:
                        bot.send_video(chat_id, f, caption=f"✅ الفيديو جاهز! من غير علامة مائية 🔥\n\n📥 حملت: {st['count']} حاجة\n{fmt_rights()}", reply_markup=after_kb(), supports_streaming=True)
            try: os.remove(file_path)
            except: pass
            try: bot.delete_message(chat_id, msg.message_id)
            except: pass
        else:
            bot.edit_message_text(f"❌ معرفتش احمل اللينك ده\n\nممكن يكون:\n- الفيديو خاص / محذوف\n- انستا طالب تسجيل دخول\n- اللينك غلط\n\nجرب لينك تاني 👇{fmt_rights()}", chat_id, msg.message_id, reply_markup=after_kb())
    except Exception as e:
        print(f"download error: {e}")
        traceback.print_exc()
        try: bot.edit_message_text(f"❌ حصلت غلطة، جرب لينك تاني 👇{fmt_rights()}", chat_id, msg.message_id, reply_markup=after_kb())
        except: pass

pending_links = {}

# تعديل بسيط للكول باك بتاع التحميل - عشان الكود اللي فوق
@bot.callback_query_handler(func=lambda c: c.data.startswith("dl_"))
def dl_callback(c):
    try: bot.answer_callback_query(c.id)
    except: pass
    d = c.data  # dl_video_KEY او dl_mp3_KEY
    parts = d.split("_")
    if len(parts) != 3: return
    mode = parts[1]
    key = parts[2]
    url = pending_links.get(key)
    if not url:
        bot.send_message(c.message.chat.id, "❌ اللينك ده قديم، ابعت لينك جديد", reply_markup=main_kb()); return
    # امسح رسالة الاختيار
    try: bot.delete_message(c.message.chat.id, c.message.message_id)
    except: pass
    class FakeMsg: pass
    fake = FakeMsg()
    fake.chat = c.message.chat
    fake.from_user = c.from_user
    # ننفذ التحميل مباشرة
    chat_id = c.message.chat.id
    uid = c.from_user.id
    st = get_stats(uid)
    is_mp3 = (mode == "mp3")
    msg = bot.send_message(chat_id, f"⏳ بحمل دلوقتي... استنى 10-20 ثانية 📥")
    try:
        file_path, err = download_video(url, chat_id, is_mp3=is_mp3)
        if file_path and os.path.exists(file_path):
            st["count"] += 1
            size = os.path.getsize(file_path) / 1024 / 1024
            if is_mp3:
                with open(file_path, "rb") as f:
                    bot.send_audio(chat_id, f, caption=f"🎵 اغنيتك جاهزة!\n\n📥 حملت: {st['count']} حاجة\n{fmt_rights()}", reply_markup=after_kb())
            else:
                if size > 48:
                    bot.send_message(chat_id, f"❌ الفيديو كبير اوي ({size:.1f} MB) - جرب فيديو اصغر 👇", reply_markup=after_kb())
                else:
                    with open(file_path, "rb") as f:
                        bot.send_video(chat_id, f, caption=f"✅ الفيديو جاهز! من غير علامة مائية 🔥\n\n📥 حملت: {st['count']} حاجة\n{fmt_rights()}", reply_markup=after_kb(), supports_streaming=True)
            try: os.remove(file_path)
            except: pass
            try: bot.delete_message(chat_id, msg.message_id)
            except: pass
        else:
            bot.edit_message_text(f"❌ معرفتش احمل اللينك ده\n\nممكن يكون خاص او محذوف\nجرب لينك تاني 👇{fmt_rights()}", chat_id, msg.message_id, reply_markup=after_kb())
    except Exception as e:
        print(e)
        bot.send_message(chat_id, "❌ حصلت غلطة، جرب لينك تاني", reply_markup=after_kb())

if __name__ == "__main__":
    print("Download Bot Adi is running... 📥")
    try: bot.delete_webhook(drop_pending_updates=True)
    except: pass
    time.sleep(2)
    while True:
        try:
            bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)
            break
        except Exception as e:
            print(f"retry: {e}"); time.sleep(10)
