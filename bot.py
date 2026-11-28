# -*- coding: utf-8 -*-
# 🎤 بوت مغير الصوت - عدي - كله ازرار
# 👑 حقوق عدي - جميع الحقوق محفوظة © 2026

import os, time, random, subprocess, traceback
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

RIGHTS = "👑 حقوق عدي - جميع الحقوق محفوظة © 2026\n👑 صنع بواسطة عدي - ممنوع السرقة"

def fmt_rights():
    return f"\n\n━━━━━━━━━━━━━━\n{RIGHTS}"

# ===== 35 صوت جوه الكود =====
VOICES = {
    "ronaldo":  {"name": "⚽ رونالدو", "filter": "asetrate=44100*0.9,atempo=1.1,volume=1.5"},
    "messi":    {"name": "⚽ ميسي", "filter": "asetrate=44100*1.15,atempo=0.9,volume=1.2"},
    "salah":    {"name": "⚽ محمد صلاح", "filter": "asetrate=44100*0.95,atempo=1.05,volume=1.4,bass=g=5"},
    "neymar":   {"name": "⚽ نيمار", "filter": "asetrate=44100*1.1,atempo=1.0,volume=1.3"},
    "mbappe":   {"name": "⚽ مبابي", "filter": "asetrate=44100*1.05,atempo=1.05,volume=1.4"},
    "haaland":  {"name": "⚽ هالاند", "filter": "asetrate=44100*0.85,atempo=1.0,volume=1.6,bass=g=8"},
    "amr":      {"name": "🎤 عمرو دياب", "filter": "asetrate=44100*0.85,atempo=1.05,volume=1.4"},
    "tamer":    {"name": "🎤 تامر حسني", "filter": "asetrate=44100*0.9,atempo=1.0,volume=1.3"},
    "wegz":     {"name": "🎤 ويجز", "filter": "asetrate=44100*0.8,atempo=1.1,volume=1.5,bass=g=8"},
    "saad":     {"name": "🎤 احمد سعد", "filter": "asetrate=44100*0.88,atempo=1.0,volume=1.4"},
    "singer":   {"name": "🎤 مطرب", "filter": "chorus=0.5:0.9:50:0.4:0.25:2,volume=1.4"},
    "news":     {"name": "🗣️ مذيع اخبار", "filter": "highpass=f=100,lowpass=f=5000,volume=1.5"},
    "adi":      {"name": "👑 عدي - صوت فخم", "filter": "asetrate=44100*0.75,atempo=1.0,volume=1.8,bass=g=10"},
    "chipmunk": {"name": "🐭 سنجاب", "filter": "asetrate=44100*1.8,atempo=0.9,volume=1.2"},
    "clown":    {"name": "🤡 مهرج", "filter": "asetrate=44100*1.4,atempo=1.1,volume=1.3,vibrato=f=10:d=0.5"},
    "santa":    {"name": "🎅 سانتا", "filter": "asetrate=44100*0.8,atempo=0.95,volume=1.5,bass=g=8"},
    "slow":     {"name": "🐢 سلحفاة - بطيء", "filter": "atempo=0.6,volume=1.2"},
    "fast":     {"name": "🐰 ارنب - سريع", "filter": "atempo=1.8,volume=1.2"},
    "monster":  {"name": "👹 وحش", "filter": "asetrate=44100*0.5,atempo=0.9,volume=1.8,bass=g=12"},
    "ghost":    {"name": "👻 شبح", "filter": "asetrate=44100*0.85,atempo=0.9,volume=1.2,echo=0.8:0.9:50:0.3"},
    "devil":    {"name": "😈 شيطان", "filter": "asetrate=44100*0.55,atempo=0.9,volume=1.8,bass=g=12"},
    "wizard":   {"name": "🧙 ساحر", "filter": "asetrate=44100*0.7,atempo=0.9,volume=1.4,echo=0.8:0.9:80:0.4"},
    "dino":     {"name": "🦖 ديناصور", "filter": "asetrate=44100*0.4,atempo=0.8,volume=2.0,bass=g=15"},
    "zombie":   {"name": "🧟 زومبي", "filter": "asetrate=44100*0.6,atempo=0.8,volume=1.7,vibrato=f=8:d=0.6"},
    "girl":     {"name": "👧 بنت صغيرة", "filter": "asetrate=44100*1.5,atempo=0.95,volume=1.2"},
    "baby":     {"name": "👶 بيبي", "filter": "asetrate=44100*1.9,atempo=0.9,volume=1.1"},
    "old":      {"name": "👴 راجل عجوز", "filter": "asetrate=44100*0.7,atempo=0.9,volume=1.3"},
    "grandma":  {"name": "👵 ست كبيرة", "filter": "asetrate=44100*0.75,atempo=0.85,volume=1.3"},
    "robot":    {"name": "🤖 روبوت", "filter": "vibrato=f=15:d=0.8,volume=1.5"},
    "alien":    {"name": "👽 فضائي", "filter": "vibrato=f=30:d=0.9,asetrate=44100*1.3,atempo=0.9"},
    "lion":     {"name": "🦁 اسد", "filter": "asetrate=44100*0.6,atempo=0.9,volume=1.8,bass=g=15"},
    "cat":      {"name": "🐱 قطة", "filter": "asetrate=44100*1.6,atempo=0.9,volume=1.2"},
    "duck":     {"name": "🦆 بطة", "filter": "asetrate=44100*1.3,atempo=1.2,volume=1.3"},
    "phone":    {"name": "📞 تليفون", "filter": "highpass=f=300,lowpass=f=3400,volume=1.5"},
    "radio":    {"name": "📻 راديو", "filter": "highpass=f=200,lowpass=f=3000,volume=1.3"},
    "underwater": {"name": "🌊 تحت المية", "filter": "lowpass=f=800,volume=1.3,echo=0.8:0.9:100:0.3"},
    "echo":     {"name": "🏔️ صدى - كهف", "filter": "aecho=0.8:0.9:100:0.4,volume=1.3"},
    "mosque":   {"name": "🕌 جامع", "filter": "aecho=0.8:0.9:200:0.5|400:0.4,volume=1.4"},
}

GROUPS = {
    "celebs": ["ronaldo","messi","salah","neymar","mbappe","haaland","amr","tamer","wegz","saad","singer","news"],
    "funny": ["chipmunk","clown","santa","slow","fast","duck"],
    "scary": ["monster","ghost","devil","wizard","dino","zombie"],
    "people": ["girl","baby","old","grandma","adi"],
    "cartoons": ["robot","alien","lion","cat","duck"],
    "effects": ["phone","radio","underwater","echo","mosque"],
}

# ===== كل الازرار =====
def main_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🎤 ازاي استخدم البوت؟", callback_data="how"),
        InlineKeyboardButton("🎭 كل الاصوات - 35 صوت", callback_data="voices"),
        InlineKeyboardButton("💎 مشاهير", callback_data="cat_celebs"),
        InlineKeyboardButton("🎵 مضحكة", callback_data="cat_funny"),
        InlineKeyboardButton("👻 مرعبة", callback_data="cat_scary"),
        InlineKeyboardButton("👧 بنات وكبار", callback_data="cat_people"),
        InlineKeyboardButton("🤖 كرتون", callback_data="cat_cartoons"),
        InlineKeyboardButton("📞 تأثيرات", callback_data="cat_effects"),
        InlineKeyboardButton("🎲 صوت عشوائي", callback_data="random_voice"),
        InlineKeyboardButton("🎤 ابعت فويس تاني", callback_data="send_voice"),
        InlineKeyboardButton("📊 احصائياتي", callback_data="stats"),
        InlineKeyboardButton("👑 حقوق عدي", callback_data="rights"),
        InlineKeyboardButton("🔄 تحديث", callback_data="back"),
    )
    return kb

def voices_kb(codes=None):
    if codes is None: codes = list(VOICES.keys())
    kb = InlineKeyboardMarkup(row_width=2)
    for code in codes:
        kb.add(InlineKeyboardButton(VOICES[code]["name"], callback_data=f"voice_{code}"))
    kb.add(InlineKeyboardButton("🎲 صوت عشوائي", callback_data="random_voice"))
    kb.add(InlineKeyboardButton("🔙 رجوع للقايمة", callback_data="back"))
    return kb

def after_voice_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🎭 جرب صوت تاني", callback_data="voices"),
        InlineKeyboardButton("🎲 صوت عشوائي", callback_data="random_voice"),
        InlineKeyboardButton("🎤 ابعت فويس جديد", callback_data="send_voice"),
        InlineKeyboardButton("🏠 القايمة الرئيسية", callback_data="back"),
    )
    return kb

def safe_edit(c, text, kb=None):
    try:
        bot.edit_message_text(text, c.message.chat.id, c.message.message_id, reply_markup=kb)
    except:
        try: bot.send_message(c.message.chat.id, text, reply_markup=kb)
        except: pass

user_last_voice = {}
user_stats = {}

def get_stats(uid):
    if uid not in user_stats: user_stats[uid] = {"count": 0, "fav": "لسه مخترتش"}
    return user_stats[uid]

def convert_voice(inp, out, code):
    filt = VOICES[code]["filter"]
    subprocess.run(["ffmpeg","-y","-i",inp,"-af",filt,"-c:a","libmp3lame","-q:a","4",out], capture_output=True, timeout=30)
    return os.path.exists(out) and os.path.getsize(out) > 1000

@bot.message_handler(commands=['start'])
def start(m):
    st = get_stats(m.from_user.id)
    bot.send_message(m.chat.id,
        f"🎤 اهلا يا {m.from_user.first_name}!\n\n"
        f"🎙️ ابعت فويس وانا هحولهولك بـ 35 صوت!\n"
        f"⚽ رونالدو - ميسي - صلاح - روبوت - سنجاب - وحش...\n\n"
        f"📊 تحويلاتك: {st['count']}\n"
        f"👇 دوس على اي زرار تحت، او ابعت فويس على طول!"
        f"{fmt_rights()}",
        reply_markup=main_kb())

@bot.message_handler(content_types=['voice','audio'])
def handle_voice(m):
    try:
        file_info = bot.get_file(m.voice.file_id if m.voice else m.audio.file_id)
        data = bot.download_file(file_info.file_path)
        path = f"voice_{m.from_user.id}.ogg"
        with open(path, "wb") as f: f.write(data)
        user_last_voice[m.from_user.id] = path
        bot.send_message(m.chat.id, f"✅ استلمت الفويس! اختار الصوت اللي عايزه من الازرار 👇{fmt_rights()}", reply_markup=voices_kb())
    except:
        bot.send_message(m.chat.id, "❌ حصلت غلطة، ابعت الفويس تاني", reply_markup=main_kb())

@bot.message_handler(func=lambda m: True)
def any_msg(m):
    bot.send_message(m.chat.id, "🎤 دوس على زرار من دول 👇 مش محتاج تكتب حاجة", reply_markup=main_kb())

@bot.callback_query_handler(func=lambda c: True)
def callbacks(c):
    uid = c.from_user.id
    try:
        st = get_stats(uid)
        d = c.data or ""
        try: bot.answer_callback_query(c.id)
        except: pass

        if d == "back":
            safe_edit(c, f"🎤 بوت مغير الصوت - عدي\n\nابعت فويس واختار الصوت 👇{fmt_rights()}", main_kb()); return
        if d == "how":
            safe_edit(c, f"🎤 ازاي؟ - كله ازرار\n\n1️⃣ دوس على زرار وابعته\n2️⃣ سجل فويس وابعته\n3️⃣ دوس على زرار الصوت اللي عايزه\n4️⃣ هيجيلك الفويس الجديد\n\n👇 جرب دلوقتي{fmt_rights()}", main_kb()); return
        if d == "send_voice":
            safe_edit(c, f"🎤 ابعت فويس دلوقتي\n\n🎙️ دوس على علامة الميكروفون تحت وسجل اي حاجة وابعتهالي\n\nوبعدين اختار الصوت من الازرار 👇{fmt_rights()}", main_kb()); return
        if d == "voices":
            safe_edit(c, f"🎭 كل الاصوات - 35 صوت\n\nدوس على اي صوت 👇{fmt_rights()}", voices_kb()); return
        if d.startswith("cat_"):
            cat = d.replace("cat_", "")
            titles = {"celebs":"💎 مشاهير","funny":"🎵 مضحكة","scary":"👻 مرعبة","people":"👧 بنات وكبار","cartoons":"🤖 كرتون","effects":"📞 تأثيرات"}
            safe_edit(c, f"{titles.get(cat,'🎭 اصوات')}\n\nدوس على اي صوت 👇{fmt_rights()}", voices_kb(GROUPS.get(cat, []))); return
        if d == "stats":
            safe_edit(c, f"📊 احصائياتك\n\n👤 {c.from_user.first_name}\n🎤 تحويلاتك: {st['count']}\n⭐ المفضل: {st['fav']}{fmt_rights()}", main_kb()); return
        if d == "random_voice":
            if uid not in user_last_voice:
                safe_edit(c, f"🎲 ابعت فويس الاول!\n\nدوس هنا 👇 وبعدين ابعت فويس", main_kb()); return
            do_convert(c, random.choice(list(VOICES.keys()))); return
        if d == "rights":
            safe_edit(c, f"👑 حقوق عدي\n\n👑 صنع بواسطة عدي\n👑 جميع الحقوق محفوظة لـ عدي © 2026\n👑 ممنوع السرقة او النسخ", main_kb()); return

        if d.startswith("voice_"):
            code = d.replace("voice_", "")
            if uid not in user_last_voice or not os.path.exists(user_last_voice[uid]):
                safe_edit(c, f"🎤 ابعت فويس الاول!\n\n🎭 الصوت اللي اخترته: {VOICES[code]['name']}\n\nدوس على الزرار ده وبعدين ابعت فويس 👇", main_kb()); return
            do_convert(c, code); return

        safe_edit(c, f"🎤 بوت مغير الصوت - عدي{fmt_rights()}", main_kb())
    except Exception as e:
        print(e)
        traceback.print_exc()
        try: bot.send_message(c.message.chat.id, "حصلت غلطة، دوس على زرار تاني 👇", reply_markup=main_kb())
        except: pass

def do_convert(c, code):
    try:
        uid = c.from_user.id
        st = get_stats(uid)
        name = VOICES[code]["name"]
        bot.send_message(c.message.chat.id, f"⏳ بحوّل صوتك لـ {name}... استنى 3 ثواني 🎤")
        out = f"out_{uid}_{code}.mp3"
        ok = convert_voice(user_last_voice[uid], out, code)
        if ok:
            st["count"] += 1; st["fav"] = name
            with open(out, "rb") as f:
                bot.send_voice(c.message.chat.id, f, caption=f"🎤 صوتك بقى: {name}\n\n🎙️ جرب صوت تاني من الازرار 👇{fmt_rights()}", reply_markup=after_voice_kb())
            try: os.remove(out)
            except: pass
            bot.send_message(c.message.chat.id, f"🎉 خلاص! صوتك بقى {name}\n\n👇 دوس على اي زرار:{fmt_rights()}", reply_markup=after_voice_kb())
        else:
            bot.send_message(c.message.chat.id, "❌ حصلت غلطة، جرب صوت تاني 👇", reply_markup=voices_kb())
    except Exception as e:
        print(e)
        bot.send_message(c.message.chat.id, "❌ حصلت غلطة، جرب تاني 👇", reply_markup=voices_kb())

if __name__ == "__main__":
    print("Voice Bot Adi - ALL BUTTONS - 35 voices")
    try: bot.delete_webhook(drop_pending_updates=True)
    except: pass
    time.sleep(2)
    while True:
        try:
            bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)
            break
        except Exception as e:
            print(f"retry: {e}"); time.sleep(10)
