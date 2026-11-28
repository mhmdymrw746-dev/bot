# -*- coding: utf-8 -*-
# 🎤 بوت مغير الصوت - عدي
# 👑 حقوق عدي - جميع الحقوق محفوظة © 2026
# 👑 صنع بواسطة عدي - ممنوع سرقة الكود او ازالة الحقوق

import os, time, random, subprocess, json, traceback
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

OWNER_NAME = "عدي"
RIGHTS = "👑 حقوق عدي - جميع الحقوق محفوظة © 2026\n👑 صنع بواسطة عدي - ممنوع السرقة\n👑 لو عايز بوت زي ده كلم عدي"
WATERMARK = "🎤 بوت مغير الصوت | 👑 عدي"

def fmt_rights():
    return f"\n\n━━━━━━━━━━━━━━\n{RIGHTS}\n{WATERMARK}"

# ============================================================
# 🎤 كل الاصوات جوه الكود - 35 صوت
# الاسم + الكود + فلتر ffmpeg بتاعه
# ============================================================
VOICES = {
    # --- مشاهير كورة ---
    "ronaldo":  {"name": "⚽ رونالدو", "filter": "asetrate=44100*0.9,atempo=1.1,volume=1.5,chorus=0.5:0.9:50:0.4:0.25:2"},
    "messi":    {"name": "⚽ ميسي", "filter": "asetrate=44100*1.15,atempo=0.9,volume=1.2"},
    "salah":    {"name": "⚽ محمد صلاح", "filter": "asetrate=44100*0.95,atempo=1.05,volume=1.4,bass=g=5"},
    "neymar":   {"name": "⚽ نيمار", "filter": "asetrate=44100*1.1,atempo=1.0,volume=1.3"},
    "mbappe":   {"name": "⚽ مبابي", "filter": "asetrate=44100*1.05,atempo=1.05,volume=1.4"},
    "haaland":  {"name": "⚽ هالاند", "filter": "asetrate=44100*0.85,atempo=1.0,volume=1.6,bass=g=8"},

    # --- مشاهير غنا ---
    "amr":      {"name": "🎤 عمرو دياب", "filter": "asetrate=44100*0.85,atempo=1.05,volume=1.4,chorus=0.5:0.9:50:0.4:0.25:2"},
    "tamer":    {"name": "🎤 تامر حسني", "filter": "asetrate=44100*0.9,atempo=1.0,volume=1.3"},
    "wegz":     {"name": "🎤 ويجز", "filter": "asetrate=44100*0.8,atempo=1.1,volume=1.5,bass=g=8"},
    "saad":     {"name": "🎤 احمد سعد", "filter": "asetrate=44100*0.88,atempo=1.0,volume=1.4"},
    "singer":   {"name": "🎤 صوت مطرب", "filter": "chorus=0.5:0.9:50|60|40:0.4|0.32|0.3:0.25|0.4|0.3:2|1.3|0.4,volume=1.4,asetrate=44100*0.95"},
    "news":     {"name": "🗣️ مذيع اخبار", "filter": "highpass=f=100,lowpass=f=5000,volume=1.5,asetrate=44100*0.95"},

    # --- عدي ---
    "adi":      {"name": "👑 عدي - صوت فخم", "filter": "asetrate=44100*0.75,atempo=1.0,volume=1.8,bass=g=10,chorus=0.5:0.9:50:0.4:0.25:2"},

    # --- مضحكة ---
    "chipmunk": {"name": "🐭 سنجاب - رفيع", "filter": "asetrate=44100*1.8,atempo=0.9,volume=1.2"},
    "clown":    {"name": "🤡 مهرج", "filter": "asetrate=44100*1.4,atempo=1.1,volume=1.3,vibrato=f=10:d=0.5"},
    "santa":    {"name": "🎅 سانتا", "filter": "asetrate=44100*0.8,atempo=0.95,volume=1.5,bass=g=8"},
    "slow":     {"name": "🐢 سلحفاة - بطيء", "filter": "atempo=0.6,volume=1.2"},
    "fast":     {"name": "🐰 ارنب - سريع", "filter": "atempo=1.8,volume=1.2"},

    # --- مرعبة ---
    "monster":  {"name": "👹 وحش - تخين", "filter": "asetrate=44100*0.5,atempo=0.9,volume=1.8,bass=g=12"},
    "ghost":    {"name": "👻 شبح", "filter": "asetrate=44100*0.85,atempo=0.9,volume=1.2,echo=0.8:0.9:50:0.3,aecho=0.8:0.9:50:0.3"},
    "devil":    {"name": "😈 شيطان", "filter": "asetrate=44100*0.55,atempo=0.9,volume=1.8,bass=g=12,chorus=0.5:0.9:50:0.4:0.25:2"},
    "wizard":   {"name": "🧙 ساحر", "filter": "asetrate=44100*0.7,atempo=0.9,volume=1.4,echo=0.8:0.9:80:0.4"},
    "dino":     {"name": "🦖 ديناصور", "filter": "asetrate=44100*0.4,atempo=0.8,volume=2.0,bass=g=15"},
    "zombie":   {"name": "🧟 زومبي", "filter": "asetrate=44100*0.6,atempo=0.8,volume=1.7,vibrato=f=8:d=0.6"},

    # --- بنات واطفال وكبار ---
    "girl":     {"name": "👧 بنت صغيرة", "filter": "asetrate=44100*1.5,atempo=0.95,volume=1.2"},
    "baby":     {"name": "👶 بيبي", "filter": "asetrate=44100*1.9,atempo=0.9,volume=1.1"},
    "old":      {"name": "👴 راجل عجوز", "filter": "asetrate=44100*0.7,atempo=0.9,volume=1.3,tremolo=f=5:d=0.3"},
    "grandma":  {"name": "👵 ست كبيرة", "filter": "asetrate=44100*0.75,atempo=0.85,volume=1.3,tremolo=f=6:d=0.4"},

    # --- حيوانات وكرتون ---
    "robot":    {"name": "🤖 روبوت", "filter": "vibrato=f=15:d=0.8,volume=1.5,chorus=0.5:0.9:50|60|40:0.4|0.32|0.3:0.25|0.4|0.3:2|1.3|0.4"},
    "alien":    {"name": "👽 كائن فضائي", "filter": "vibrato=f=30:d=0.9,asetrate=44100*1.3,atempo=0.9"},
    "lion":     {"name": "🦁 اسد", "filter": "asetrate=44100*0.6,atempo=0.9,volume=1.8,bass=g=15"},
    "cat":      {"name": "🐱 قطة", "filter": "asetrate=44100*1.6,atempo=0.9,volume=1.2"},
    "duck":     {"name": "🦆 بطة", "filter": "asetrate=44100*1.3,atempo=1.2,volume=1.3,vibrato=f=20:d=0.4"},

    # --- اماكن وتأثيرات ---
    "phone":    {"name": "📞 صوت تليفون", "filter": "highpass=f=300,lowpass=f=3400,volume=1.5"},
    "radio":    {"name": "📻 راديو قديم", "filter": "highpass=f=200,lowpass=f=3000,volume=1.3,chorus=0.5:0.9:50:0.4:0.25:2"},
    "underwater": {"name": "🌊 تحت المية", "filter": "lowpass=f=800,volume=1.3,echo=0.8:0.9:100:0.3"},
    "echo":     {"name": "🏔️ صدى - كهف", "filter": "aecho=0.8:0.9:100:0.4|200:0.3,volume=1.3"},
    "mosque":   {"name": "🕌 صوت جامع - صدى كبير", "filter": "aecho=0.8:0.9:200:0.5|400:0.4|600:0.3,volume=1.4"},
}

# ترتيب الاصوات في الازرار
VOICE_GROUPS = {
    "celebs": ["ronaldo","messi","salah","neymar","mbappe","haaland","amr","tamer","wegz","saad","singer","news"],
    "funny": ["chipmunk","clown","santa","slow","fast","duck"],
    "scary": ["monster","ghost","devil","wizard","dino","zombie"],
    "people": ["girl","baby","old","grandma","adi"],
    "cartoons": ["robot","alien","lion","cat","duck"],
    "effects": ["phone","radio","underwater","echo","mosque"],
}

def main_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🎤 ابعت فويس وغيّر صوتك", callback_data="how"),
        InlineKeyboardButton("🎭 كل الاصوات - 35 صوت", callback_data="voices"),
        InlineKeyboardButton("💎 اصوات المشاهير", callback_data="cat_celebs"),
        InlineKeyboardButton("🎵 اصوات مضحكة", callback_data="cat_funny"),
        InlineKeyboardButton("👻 اصوات مرعبة", callback_data="cat_scary"),
        InlineKeyboardButton("👧 بنات وكبار", callback_data="cat_people"),
        InlineKeyboardButton("🤖 كرتون وحيوانات", callback_data="cat_cartoons"),
        InlineKeyboardButton("📞 تأثيرات واماكن", callback_data="cat_effects"),
        InlineKeyboardButton("🎲 صوت عشوائي", callback_data="random_voice"),
        InlineKeyboardButton("📊 احصائياتي", callback_data="stats"),
        InlineKeyboardButton("👑 حقوق عدي", callback_data="rights"),
    )
    return kb

def voices_kb(codes=None):
    if codes is None:
        codes = list(VOICES.keys())
    kb = InlineKeyboardMarkup(row_width=2)
    for code in codes:
        v = VOICES.get(code)
        if v:
            kb.add(InlineKeyboardButton(v["name"], callback_data=f"voice_{code}"))
    kb.add(InlineKeyboardButton("🔙 رجوع", callback_data="back"))
    return kb

def cat_kb(cat):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton("🎭 كل الاصوات", callback_data="voices"))
    kb.add(InlineKeyboardButton("🔙 رجوع", callback_data="back"))
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
    if uid not in user_stats:
        user_stats[uid] = {"count": 0, "fav": "لسه"}
    return user_stats[uid]

def convert_voice(input_path, output_path, voice_code):
    filt = VOICES.get(voice_code, {}).get("filter", "atempo=1.0")
    cmd = ["ffmpeg", "-y", "-i", input_path, "-af", filt, "-c:a", "libmp3lame", "-q:a", "4", output_path]
    subprocess.run(cmd, capture_output=True, timeout=30)
    return os.path.exists(output_path) and os.path.getsize(output_path) > 1000

@bot.message_handler(commands=['start','help','menu'])
def start(m):
    st = get_stats(m.from_user.id)
    bot.send_message(m.chat.id,
        f"🎤 اهلا يا {m.from_user.first_name} في بوت مغير الصوت!\n\n"
        f"🎙️ ابعتلي اي فويس - وانا هرجعهولك بـ 35 صوت مختلف!\n"
        f"⚽ رونالدو، ميسي، صلاح، عمرو دياب، ويجز، روبوت، سنجاب، وحش، بنت، شبح...\n\n"
        f"📊 تحويلاتك: {st['count']} | ⭐ المفضل: {st['fav']}\n"
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
        bot.send_message(m.chat.id, f"✅ استلمت الفويس! اختار الصوت اللي عايزه 👇{fmt_rights()}", reply_markup=voices_kb())
    except Exception as e:
        print(f"voice error: {e}")
        bot.send_message(m.chat.id, "❌ حصلت غلطة في الفويس، ابعته تاني")

@bot.message_handler(func=lambda m: True)
def any_msg(m):
    bot.send_message(m.chat.id, "🎤 ابعتلي فويس على طول، او اختار من الازرار 👇", reply_markup=main_kb())

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
            safe_edit(c, f"🎤 ازاي تستخدم البوت؟\n\n1️⃣ ابعت اي فويس (سجل صوتك)\n2️⃣ اختار الصوت من الازرار\n3️⃣ استنى 3 ثواني وهيجيلك الفويس الجديد\n4️⃣ ابعته لصحابك واعملهم مقلب 😂\n\n💡 ممكن تحول نفس الفويس لـ 35 صوت مختلف!{fmt_rights()}", main_kb()); return
        if d == "voices":
            safe_edit(c, f"🎭 كل الاصوات - 35 صوت\n\nاختار الصوت اللي عايزه 👇\nلو لسه مبعتش فويس، ابعت فويس الاول{fmt_rights()}", voices_kb()); return
        if d.startswith("cat_"):
            cat = d.replace("cat_", "")
            titles = {"celebs":"💎 اصوات المشاهير","funny":"🎵 اصوات مضحكة","scary":"👻 اصوات مرعبة","people":"👧 بنات وكبار","cartoons":"🤖 كرتون وحيوانات","effects":"📞 تأثيرات واماكن"}
            codes = VOICE_GROUPS.get(cat, [])
            safe_edit(c, f"{titles.get(cat, '🎭 اصوات')}\n\nاختار صوت 👇{fmt_rights()}", voices_kb(codes)); return
        if d == "stats":
            safe_edit(c, f"📊 احصائياتك يا عدي\n\n👤 اسمك: {c.from_user.first_name}\n🎤 تحويلاتك: {st['count']}\n⭐ صوتك المفضل: {st['fav']}{fmt_rights()}", main_kb()); return
        if d == "random_voice":
            if uid not in user_last_voice:
                safe_edit(c, f"🎲 ابعت فويس الاول وبعدين دوس صوت عشوائي!{fmt_rights()}", main_kb()); return
            code = random.choice(list(VOICES.keys()))
            do_convert(c, code); return
        if d == "rights":
            safe_edit(c, f"👑 حقوق عدي\n\n👑 البوت ده من صنع عدي\n👑 جميع الحقوق محفوظة لـ عدي © 2026\n👑 ممنوع سرقة الكود او ازالة الحقوق\n👑 ممنوع نسخ البوت بدون اذن عدي\n\n🎤 بوت مغير الصوت - النسخة الاصلية", main_kb()); return

        if d.startswith("voice_"):
            code = d.replace("voice_", "")
            if code not in VOICES:
                bot.send_message(c.message.chat.id, "الصوت ده مش موجود"); return
            if uid not in user_last_voice or not os.path.exists(user_last_voice[uid]):
                safe_edit(c, f"🎤 ابعت فويس الاول!\n\n🎙️ سجل اي حاجة بصوتك وابعتهالي، وبعدين اختار الصوت ده تاني 👇\n\n🎭 الصوت اللي اخترته: {VOICES[code]['name']}{fmt_rights()}", voices_kb()); return
            do_convert(c, code); return

        safe_edit(c, f"🎤 بوت مغير الصوت - عدي\n\nابعت فويس واختار الصوت 👇{fmt_rights()}", main_kb())
    except Exception as e:
        print(f"callback error: {e}")
        traceback.print_exc()
        try: bot.send_message(c.message.chat.id, "حصلت غلطة، ابعت الفويس تاني 🎤", reply_markup=main_kb())
        except: pass

def do_convert(c, code):
    try:
        uid = c.from_user.id
        st = get_stats(uid)
        name = VOICES[code]["name"]
        bot.send_message(c.message.chat.id, f"⏳ بحوّل صوتك لـ {name}... استنى 3 ثواني 🎤")
        input_path = user_last_voice[uid]
        output_path = f"out_{uid}_{code}.mp3"
        ok = convert_voice(input_path, output_path, code)
        if ok:
            st["count"] += 1; st["fav"] = name
            with open(output_path, "rb") as f:
                bot.send_voice(c.message.chat.id, f, caption=f"🎤 صوتك بقى: {name}\n\n🎙️ جرب صوت تاني من الازرار 👇\n{fmt_rights()}", reply_markup=voices_kb())
            try: os.remove(output_path)
            except: pass
            bot.send_message(c.message.chat.id, f"🎉 خلاص! صوتك بقى {name}\n\n🎤 عايز تجرب صوت تاني لنفس الفويس؟ دوس على اي زرار 👇\n📊 تحويلاتك: {st['count']}{fmt_rights()}", reply_markup=voices_kb())
        else:
            bot.send_message(c.message.chat.id, "❌ حصلت غلطة في التحويل، جرب صوت تاني 🎤", reply_markup=voices_kb())
    except Exception as e:
        print(f"convert error: {e}")
        bot.send_message(c.message.chat.id, "❌ حصلت غلطة، جرب فويس تاني", reply_markup=voices_kb())

if __name__ == "__main__":
    print("Voice Bot Adi is running... 🎤 35 voices loaded")
    try: bot.delete_webhook(drop_pending_updates=True)
    except: pass
    time.sleep(2)
    while True:
        try:
            bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)
            break
        except Exception as e:
            print(f"Polling error: {e} - retry...")
            time.sleep(10)
