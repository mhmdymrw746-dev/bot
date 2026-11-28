# -*- coding: utf-8 -*-
# 📥 بوت التحميل - عدي عمرو
# 👑 حقوق عدي - جميع الحقوق محفوظة © 2026
# بوت بيحمل اي فيديو من اي موقع

import os, time, re, subprocess, traceback, uuid, glob, threading
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
from PIL import Image, ImageDraw, ImageFont

# --- سيرفر وهمي عشان Render ميفصلش ---
app = Flask(__name__)
@app.route('/')
def home(): return "Bot Adi is Alive"
threading.Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000))), daemon=True).start()

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

DEV_LINK = "https://t.me/yuoe80"
DEV_USERNAME = "@yuoe80"
RIGHTS = "👑 حقوق عدي - جميع الحقوق محفوظة © 2026\n👑 صنع بواسطة عدي عمرو - ممنوع السرقة"
def fmt_rights():
    return f"\n\n━━━━━━━━━━━━━━\n{RIGHTS}\n📩 تواصل مع المطور: {DEV_USERNAME}\n📢 قناة المطور: {DEV_LINK}"

pending_links = {}
user_stats = {}
MAX_SIZE = 200 * 1024 * 1024

def get_stats(uid):
    if uid not in user_stats: user_stats[uid] = {"count": 0}
    return user_stats[uid]

# ===== بيدعم اي لينك - اي موقع =====
def is_link(text):
    text = text.lower()
    if "http" not in text:
        return False
    # اي لينك فيه نقطة و / - يعتبر فيديو
    # تيك توك - انستا - يوتيوب - فيس - تويتر - اي موقع تاني
    return any(x in text for x in [
        "tiktok.com", "vt.tiktok.com", "vm.tiktok.com",
        "instagram.com", "instagr.am",
        "youtube.com", "youtu.be", "music.youtube.com",
        "facebook.com", "fb.watch", "fb.gg",
        "twitter.com", "x.com",
        "snapchat.com", "pinterest.com", "reddit.com",
        "dailymotion.com", "vimeo.com", "twitch.tv",
        "t.me", "telegram", "likee", "kwai", "capcut",
        ".com", ".net", ".io", ".co", ".me", ".tv", ".cc"
    ])

def extract_link(text):
    m = re.search(r'https?://\S+', text)
    return m.group(0).rstrip(')]}.,!') if m else text.strip()

# ===== واجهة فخمة =====
def main_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("📥 ازاي احمل؟", callback_data="how"),
        InlineKeyboardButton("🎵 تيك توك", callback_data="tiktok"),
        InlineKeyboardButton("📸 انستا", callback_data="insta"),
        InlineKeyboardButton("▶️ يوتيوب", callback_data="youtube"),
        InlineKeyboardButton("📘 فيس بوك", callback_data="facebook"),
        InlineKeyboardButton("🎵 اغنية MP3", callback_data="mp3"),
        InlineKeyboardButton("🌐 اي موقع تاني", callback_data="anym"),
        InlineKeyboardButton("📊 احصائياتي", callback_data="stats"),
        InlineKeyboardButton("👑 حقوق عدي", callback_data="rights"),
        InlineKeyboardButton("📩 تواصل مع المطور", url=DEV_LINK),
        InlineKeyboardButton("📢 قناة المطور", url=DEV_LINK),
    )
    return kb

def after_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("📥 حمل لينك تاني", callback_data="send_link"),
        InlineKeyboardButton("🎵 تيك توك", callback_data="tiktok"),
        InlineKeyboardButton("📸 انستا", callback_data="insta"),
        InlineKeyboardButton("▶️ يوتيوب", callback_data="youtube"),
        InlineKeyboardButton("🏠 القايمة الرئيسية", callback_data="back"),
        InlineKeyboardButton("📩 تواصل مع المطور", url=DEV_LINK),
        InlineKeyboardButton("📢 قناة المطور", url=DEV_LINK),
    )
    return kb

def safe_edit(c, text, kb=None):
    try:
        bot.edit_message_text(text, c.message.chat.id, c.message.message_id, reply_markup=kb)
    except:
        try: bot.send_message(c.message.chat.id, text, reply_markup=kb)
        except: pass

# ===== العلامة المائية - شعار + اسم على كل فيديو =====
def add_watermark(input_file, output_file):
    try:
        if os.path.exists("logo.png"):
            # 1 - الشعار فوق يمين - صغير
            cmd = [
                "ffmpeg", "-y", "-i", input_file, "-i", "logo.png",
                "-filter_complex", "[1]scale=140:-1[logo];[0][logo]overlay=main_w-overlay_w-20:20",
                "-preset", "ultrafast", "-crf", "28", "-codec:a", "copy", output_file
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
            if not os.path.exists(output_file):
                return False

            # 2 - اسمك تحت شمال - صغير وشيك
            img = Image.new('RGBA', (500, 80), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 34)
            except:
                font = ImageFont.load_default()
            text = "Adi Amr - عدي عمرو"
            for dx, dy in [(3,3),(3,0),(0,3)]:
                draw.text((dx, dy), text, font=font, fill=(0,0,0,200))
            draw.text((0, 0), text, font=font, fill=(255,255,255,230))
            img.save("name.png")

            tmp = "tmp_" + output_file
            cmd2 = [
                "ffmpeg", "-y", "-i", output_file, "-i", "name.png",
                "-filter_complex", "[1]scale=iw*0.28:-1[nm];[0][nm]overlay=20:main_h-overlay_h-20",
                "-preset", "ultrafast", "-crf", "28", "-codec:a", "copy", tmp
            ]
            subprocess.run(cmd2, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
            if os.path.exists(tmp):
                os.remove(output_file)
                os.rename(tmp, output_file)
            return True
        return False
    except Exception as e:
        print("Watermark error:", e)
        return False

def download_video(url, chat_id, is_mp3=False):
    uid = str(uuid.uuid4())[:8]
    # لو اللينك مختصر زي vt.tiktok - yt-dlp بيفكه لوحده
    if is_mp3:
        cmd = ["yt-dlp", "-x", "--audio-format", "mp3", "--audio-quality", "0",
               "-o", f"dl_{uid}.mp3", "--no-playlist", "--max-filesize", "200M",
               "--user-agent", "Mozilla/5.0", url]
    else:
        # بيحمل اي فيديو - افضل جودة لحد 1080p
        cmd = ["yt-dlp", "-f", "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best/best",
               "-o", f"dl_{uid}.%(ext)s", "--no-playlist", "--max-filesize", "200M",
               "--merge-output-format", "mp4",
               "--user-agent", "Mozilla/5.0",
               "--no-warnings", url]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    files = glob.glob(f"dl_{uid}.*")
    # لو ملقاش فيديو - جرب صيغة عامة لأي موقع
    if not files:
        cmd2 = ["yt-dlp", "-o", f"dl_{uid}.%(ext)s", "--no-playlist", "--max-filesize", "200M", url]
        result = subprocess.run(cmd2, capture_output=True, text=True, timeout=300)
        files = glob.glob(f"dl_{uid}.*")
    return files[0] if files else None, result.stderr[:500] if result.stderr else ""

@bot.message_handler(commands=['start'])
def start(m):
    st = get_stats(m.from_user.id)
    bot.send_message(m.chat.id,
        f"✦ ━━━━━━━━━━━━━ ✦\n"
        f"  👋 اهلا يا {m.from_user.first_name}\n"
        f"  🚀 بوت التحميل - عدي عمرو\n"
        f"✦ ━━━━━━━━━━━━━ ✦\n\n"
        f"✅ تيك توك - عادي ومختصر vt.tiktok.com\n"
        f"✅ انستا - ريلز وستوري وبوست\n"
        f"✅ يوتيوب - فيديو وشورتس\n"
        f"✅ فيس بوك - فيديو وريلز\n"
        f"✅ تويتر / سناب / بنترست / ريديت\n"
        f"✅ 🌐 اي موقع تاني فيه فيديو!\n"
        f"✅ اغنية MP3 من اي لينك\n"
        f"✅ جودة عالية لحد 1080p - حتى 200 MB\n\n"
        f"📊 حملت: {st['count']} فيديو\n"
        f"👇 دوس على اي زرار، او ابعت اي لينك على طول!"
        f"{fmt_rights()}",
        reply_markup=main_kb())

@bot.message_handler(content_types=['text'])
def handle_text(m):
    text = m.text.strip()
    if is_link(text):
        link = extract_link(text)
        do_download(m, link, False)
        return
    bot.send_message(m.chat.id, "📥 ابعتلي اي لينك فيديو على طول 👇\n\nمثال:\nhttps://vt.tiktok.com/ZSsUjdphu/\nhttps://www.tiktok.com/...\nhttps://www.instagram.com/reel/...\nhttps://youtu.be/...", reply_markup=main_kb())

@bot.callback_query_handler(func=lambda c: True)
def callbacks(c):
    uid = c.from_user.id
    try:
        st = get_stats(uid)
        d = c.data or ""
        try: bot.answer_callback_query(c.id)
        except: pass

        if d == "back":
            safe_edit(c, f"✦ بوت التحميل - عدي عمرو ✦\n\nابعت اي لينك فيديو وانا هحملهولك 👇{fmt_rights()}", main_kb()); return
        if d == "how":
            safe_edit(c, f"📥 ازاي تحمل؟\n\n1️⃣ روح اي موقع - تيك توك / انستا / يوتيوب / اي موقع\n2️⃣ دوس مشاركة -> نسخ الرابط\n3️⃣ تعال هنا وابعت اللينك\n4️⃣ اختار فيديو ولا اغنية\n5️⃣ استنى وهيجيلك الفيديو 👑\n\n💡 جرب دلوقتي - ابعت اي لينك{fmt_rights()}", main_kb()); return
        if d == "send_link":
            safe_edit(c, f"📥 ابعت اللينك دلوقتي\n\nانسخ لينك الفيديو وابعته هنا 👇", main_kb()); return
        if d == "tiktok":
            safe_edit(c, f"🎵 تحميل تيك توك\n\nابعت لينك فيديو التيك توك - عادي او مختصر vt.tiktok.com\nوانا هجيبهولك من غير علامة مائية 💧\n\n👇 ابعت اللينك", main_kb()); return
        if d == "insta":
            safe_edit(c, f"📸 تحميل انستا\n\nابعت لينك الريلز او البوست او الستوري\nوانا هحملهولك 👇", main_kb()); return
        if d == "youtube":
            safe_edit(c, f"▶️ تحميل يوتيوب\n\nابعت لينك فيديو يوتيوب او شورتس\nوانا هحملهولك بجودة عالية 👇", main_kb()); return
        if d == "facebook":
            safe_edit(c, f"📘 تحميل فيس بوك\n\nابعت لينك فيديو الفيس او الريلز\nوانا هحملهولك 👇", main_kb()); return
        if d == "anym":
            safe_edit(c, f"🌐 تحميل من اي موقع\n\nالبوت بيحمل من اي موقع فيه فيديو:\nتيك توك - انستا - يوتيوب - فيس - تويتر - سناب - بنترست - ريديت - فيميو - واي موقع تاني\n\n👇 ابعت اي لينك", main_kb()); return
        if d == "mp3":
            safe_edit(c, f"🎵 تحميل اغنية MP3\n\nابعت اي لينك وانا هحولهولك اغنية MP3\n\n👇 ابعت اللينك", main_kb()); return
        if d == "stats":
            safe_edit(c, f"📊 احصائياتك\n\n👤 {c.from_user.first_name}\n📥 حملت: {st['count']} فيديو{fmt_rights()}", main_kb()); return
        if d == "rights":
            safe_edit(c, f"👑 حقوق عدي\n\n👑 صنع بواسطة عدي عمرو\n👑 جميع الحقوق محفوظة لـ عدي عمرو © 2026\n👑 ممنوع السرقة او النسخ\n\n📩 تواصل: {DEV_USERNAME}\n📢 قناة: {DEV_LINK}", main_kb()); return

        if d.startswith("dl_"):
            parts = d.split("_")
            if len(parts) != 3: return
            mode = parts[1]
            key = parts[2]
            url = pending_links.get(key)
            if not url:
                bot.send_message(c.message.chat.id, "❌ اللينك ده قديم، ابعت لينك جديد", reply_markup=main_kb()); return
            try: bot.delete_message(c.message.chat.id, c.message.message_id)
            except: pass
            class FakeMsg: pass
            fake = FakeMsg()
            fake.chat = c.message.chat
            fake.from_user = c.from_user
            do_download(fake, url, mode == "mp3", is_from_button=True)
            return

        safe_edit(c, f"📥 بوت التحميل - عدي عمرو{fmt_rights()}", main_kb())
    except Exception as e:
        print(e); traceback.print_exc()

def do_download(m, url, is_mp3=False, is_from_button=False):
    chat_id = m.chat.id
    uid = m.from_user.id
    st = get_stats(uid)

    if not is_from_button and not is_mp3:
        key = str(uuid.uuid4())[:8]
        pending_links[key] = url
        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton("🎬 فيديو MP4", callback_data=f"dl_video_{key}"),
            InlineKeyboardButton("🎵 اغنية MP3", callback_data=f"dl_mp3_{key}"),
        )
        bot.send_message(chat_id, f"📥 لقيت اللينك!\n\nتحب احملهولك ايه؟ 👇\n\n{url[:80]}...", reply_markup=kb)
        return

    msg = bot.send_message(chat_id, f"⏳ بحمل دلوقتي... استنى 10-20 ثانية 📥")
    try:
        file_path, err = download_video(url, chat_id, is_mp3=is_mp3)
        if file_path and os.path.exists(file_path):
            st["count"] += 1
            size = os.path.getsize(file_path) / 1024 / 1024
            if size > 200:
                bot.send_message(chat_id, f"❌ الفيديو كبير اوي ({size:.1f} MB) - الحد الاقصى 200 MB", reply_markup=after_kb())
                try: os.remove(file_path)
                except: pass
                return

            if is_mp3:
                with open(file_path, "rb") as f:
                    bot.send_audio(chat_id, f, caption=f"🎵 اغنيتك جاهزة!\n\n✦ عدي عمرو ✦\n📩 تواصل مع المطور: {DEV_USERNAME}\n📢 قناة المطور: {DEV_LINK}\n\n📥 حملت: {st['count']} حاجة\n{fmt_rights()}", reply_markup=after_kb())
            else:
                # --- حفر في السر - مفاجأة 👑 ---
                final_path = "final_" + file_path
                if add_watermark(file_path, final_path):
                    try: os.remove(file_path)
                    except: pass
                    file_path = final_path

                with open(file_path, "rb") as f:
                    bot.send_video(chat_id, f, caption=f"✅ الفيديو جاهز! 🔥\n\n✦ عدي عمرو ✦\n👑 جميع الحقوق محفوظة لـ عدي عمرو\n📩 تواصل مع المطور: {DEV_USERNAME}\n📢 قناة المطور: {DEV_LINK}\n\n📥 حملت: {st['count']} حاجة\n{fmt_rights()}", reply_markup=after_kb(), supports_streaming=True)
            try: os.remove(file_path)
            except: pass
            try: bot.delete_message(chat_id, msg.message_id)
            except: pass
        else:
            bot.edit_message_text(f"❌ معرفتش احمل اللينك ده\n\nممكن يكون:\n- الفيديو خاص / محذوف\n- الموقع طالب تسجيل دخول\n- اللينك غلط\n\nجرب لينك تاني 👇\n\nلو مش راضي يحمل خالص - كلم المطور: {DEV_USERNAME}{fmt_rights()}", chat_id, msg.message_id, reply_markup=after_kb())
    except Exception as e:
        print(f"download error: {e}")
        traceback.print_exc()
        try: bot.edit_message_text(f"❌ حصلت غلطة، جرب لينك تاني 👇{fmt_rights()}", chat_id, msg.message_id, reply_markup=after_kb())
        except: pass

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
