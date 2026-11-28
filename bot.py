# -*- coding: utf-8 -*-
# 🎤 بوت مغير الصوت - عدي
# 👑 الحقوق الكاملة: عدي
# 👑 صنع بواسطة عدي - ممنوع سرقة الكود او ازالة الحقوق
# 👑 @Adi_Voice_Bot - جميع الحقوق محفوظة لـ عدي © 2026

import os, time, random, subprocess, json, traceback
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.environ.get("BOT_TOKEN") or "حط_التوكن_بتاعك_هنا"
bot = telebot.TeleBot(TOKEN)

OWNER_ID = 8188263997
OWNER_NAME = "عدي"
RIGHTS = "👑 حقوق عدي - جميع الحقوق محفوظة © 2026\n👑 صنع بواسطة عدي - ممنوع السرقة\n👑 لو عايز بوت زي ده كلم عدي"
WATERMARK = "🎤 بوت مغير الصوت | 👑 عدي"

DB_FILE = "voice_db.json"
if os.path.exists(DB_FILE):
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            DB = json.load(f)
    except:
        DB = {"users": {}, "total": 0, "voices_used": {}}
else:
    DB = {"users": {}, "total": 0, "voices_used": {}}

def save():
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(DB, f, ensure_ascii=False, indent=2)
    except: pass

def get_user(uid, name="ضيف"):
    uid = str(uid)
    if uid not in DB["users"]:
        DB["users"][uid] = {"name": name, "count": 0, "fav": "none", "last_voice": None}
        save()
    return DB["users"][uid]

def fmt_rights():
    return f"\n\n━━━━━━━━━━━━━━\n{RIGHTS}\n{WATERMARK}"

def main_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🎤 ابعت فويس وغيّر صوتك", callback_data="how"),
        InlineKeyboardButton("🎭 كل الاصوات", callback_data="voices"),
        InlineKeyboardButton("⭐ صوتي المفضل", callback_data="myfav"),
        InlineKeyboardButton("🏆 اكتر الاصوات استخداما", callback_data="top"),
        InlineKeyboardButton("📊 احصائياتي", callback_data="stats"),
        InlineKeyboardButton("🎲 صوت عشوائي", callback_data="random_voice_info"),
        InlineKeyboardButton("💎 اصوات المشاهير", callback_data="celebs"),
        InlineKeyboardButton("🤖 اصوات كرتون", callback_data="cartoons"),
        InlineKeyboardButton("👻 اصوات مرعبة", callback_data="scary"),
        InlineKeyboardButton("🎵 اصوات مضحكة", callback_data="funny"),
        InlineKeyboardButton("👑 حقوق عدي", callback_data="rights"),
    )
    return kb

def voices_kb():
    all_voices = [
        ("⚽ رونالدو", "ronaldo"), ("⚽ ميسي", "messi"),
        ("⚽ محمد صلاح", "salah"), ("🎤 عمرو دياب", "amr"),
        ("🎤 تامر حسني", "tamer"), ("👑 عدي", "king"),
        ("🤖 روبوت", "robot"), ("🐭 سنجاب - صوت رفيع", "chipmunk"),
        ("👹 وحش - صوت تخين", "monster"), ("👧 بنت صغيرة", "girl"),
        ("👴 راجل عجوز", "old"), ("👻 شبح", "ghost"),
        ("👽 كائن فضائي", "alien"), ("🦁 اسد", "lion"),
        ("🐱 قطة", "cat"), ("🦖 ديناصور", "dino"),
        ("🎅 سانتا", "santa"), ("🧙 ساحر", "wizard"),
        ("🤡 مهرج", "clown"), ("😈 شيطان", "devil"),
        ("🐢 سلحفاة - بطيء", "slow"), ("🐰 ارنب - سريع", "fast"),
        ("📞 صوت تليفون", "phone"), ("📻 صوت راديو قديم", "radio"),
        ("🌊 صوت تحت المية", "underwater"), ("🏔️ صوت صدى - كهف", "echo"),
        ("🎤 صوت مطرب", "singer"), ("🗣️ صوت مذيع اخبار", "news"),
    ]
    kb = InlineKeyboardMarkup(row_width=2)
    for name, code in all_voices:
        kb.add(InlineKeyboardButton(name, callback_data=f"voice_{code}"))
    kb.add(InlineKeyboardButton("🔙 رجوع", callback_data="back"))
    return kb

def celebs_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("⚽ رونالدو", callback_data="voice_ronaldo"),
        InlineKeyboardButton("⚽ ميسي", callback_data="voice_messi"),
        InlineKeyboardButton("⚽ محمد صلاح", callback_data="voice_salah"),
        InlineKeyboardButton("⚽ نيمار", callback_data="voice_neymar"),
        InlineKeyboardButton("🎤 عمرو دياب", callback_data="voice_amr"),
        InlineKeyboardButton("🎤 تامر حسني", callback_data="voice_tamer"),
        InlineKeyboardButton("🎤 ويجز", callback_data="voice_wegz"),
        InlineKeyboardButton("🎤 احمد سعد", callback_data="voice_saad"),
        InlineKeyboardButton("👑 عدي", callback_data="voice_king"),
        InlineKeyboardButton("🔙 رجوع", callback_data="back"),
    )
    return kb

def cartoons_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🐭 ميكي ماوس", callback_data="voice_chipmunk"),
        InlineKeyboardButton("[STRIPPED 3 bytes] sponge بوب", callback_data="voice_fast"),
        InlineKeyboardButton("🦁 سيمبا", callback_data="voice_lion"),
        InlineKeyboardButton("🐱 توم", callback_data="voice_cat"),
        InlineKeyboardButton("🤖 روبوت", callback_data="voice_robot"),
        InlineKeyboardButton("👽 كائن فضائي", callback_data="voice_alien"),
        InlineKeyboardButton("🔙 رجوع", callback_data="back"),
    )
    return kb

def scary_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("👻 شبح", callback_data="voice_ghost"),
        InlineKeyboardButton("👹 وحش", callback_data="voice_monster"),
        InlineKeyboardButton("😈 شيطان", callback_data="voice_devil"),
        InlineKeyboardButton("🧙 ساحر", callback_data="voice_wizard"),
        InlineKeyboardButton("🦖 ديناصور", callback_data="voice_dino"),
        InlineKeyboardButton("🔙 رجوع", callback_data="back"),
    )
    return kb

def funny_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🐭 سنجاب", callback_data="voice_chipmunk"),
        InlineKeyboardButton("🤡 مهرج", callback_data="voice_clown"),
        InlineKeyboardButton("🐢 سلحفاة", callback_data="voice_slow"),
        InlineKeyboardButton("🐰 ارنب", callback_data="voice_fast"),
        InlineKeyboardButton("🎅 سانتا", callback_data="voice_santa"),
        InlineKeyboardButton("🔙 رجوع", callback_data="back"),
    )
    return kb

def safe_edit(c, text, kb=None):
    try:
        bot.edit_message_text(text, c.message.chat.id, c.message.message_id, reply_markup=kb)
    except:
        try: bot.send_message(c.message.chat.id, text, reply_markup=kb)
        except: pass

def safe_answer(c, text):
    try: bot.answer_callback_query(c.id, text)
    except: pass

VOICE_FILTERS = {
    "ronaldo": "asetrate=44100*0.9,atempo=1.1,volume=1.5,chorus=0.5:0.9:50|60|40:0.4|0.32|0.3:0.25|0.4|0.3:2|1.3|0.4",
    "messi": "asetrate=44100*1.15,atempo=0.9,volume=1.2",
    "salah": "asetrate=44100*0.95,atempo=1.05,volume=1.4,bass=g=5",
    "neymar": "asetrate=44100*1.1,atempo=1.0,volume=1.3",
    "amr": "asetrate=44100*0.85,atempo=1.05,volume=1.4,chorus=0.5:0.9:50:0.4:0.25:2",
    "tamer": "asetrate=44100*0.9,atempo=1.0,volume=1.3",
    "wegz": "asetrate=44100*0.8,atempo=1.1,volume=1.5,bass=g=8",
    "saad": "asetrate=44100*0.88,atempo=1.0,volume=1.4",
    "king": "asetrate=44100*0.75,atempo=1.0,volume=1.8,bass=g=10,chorus=0.5:0.9:50:0.4:0.25:2",
    "robot": "vibrato=f=15:d=0.8,volume=1.5,chorus=0.5:0.9:50|60|40:0.4|0.32|0.3:0.25|0.4|0.3:2|1.3|0.4",
    "chipmunk": "asetrate=44100*1.8,atempo=0.9,volume=1.2",
    "monster": "asetrate=44100*0.5,atempo=0.9,volume=1.8,bass=g=12",
    "girl": "asetrate=44100*1.5,atempo=0.95,volume=1.2",
    "old": "asetrate=44100*0.7,atempo=0.9,volume=1.3,tremolo=f=5:d=0.3",
    "ghost": "asetrate=44100*0.85,atempo=0.9,volume=1.2,echo=0.8:0.9:50:0.3,aecho=0.8:0.9:50:0.3",
    "alien": "vibrato=f=30:d=0.9,asetrate=44100*1.3,atempo=0.9",
    "lion": "asetrate=44100*0.6,atempo=0.9,volume=1.8,bass=g=15",
    "cat": "asetrate=44100*1.6,atempo=0.9,volume=1.2",
    "dino": "asetrate=44100*0.4,atempo=0.8,volume=2.0,bass=g=15",
    "santa": "asetrate=44100*0.8,atempo=0.95,volume=1.5,bass=g=8",
    "wizard": "asetrate=44100*0.7,atempo=0.9,volume=1.4,echo=0.8:0.9:80:0.4",
    "clown": "asetrate=44100*1.4,atempo=1.1,volume=1.3,vibrato=f=10:d=0.5",
    "devil": "asetrate=44100*0.55,atempo=0.9,volume=1.8,bass=g=12,chorus=0.5:0.9:50:0.4:0.25:2",
    "slow": "atempo=0.6,volume=1.2",
    "fast": "atempo=1.8,volume=1.2",
    "phone": "highpass=f=300,lowpass=f=3400,volume=1.5",
    "radio": "highpass=f=200,lowpass=f=3000,volume=1.3,chorus=0.5:0.9:50:0.4:0.25:2",
    "underwater": "lowpass=f=800,volume=1.3,echo=0.8:0.9:100:0.3",
    "echo": "aecho=0.8:0.9:100:0.4|200:0.3,volume=1.3",
    "singer": "chorus=0.5:0.9:50|60|40:0.4|0.32|0.3:0.25|0.4|0.3:2|1.3|0.4,volume=1.4,asetrate=44100*0.95",
    "news": "highpass=f=100,lowpass=f=5000,volume=1.5,asetrate=44100*0.95",
}

VOICE_NAMES = {
    "ronaldo": "⚽ رونالدو", "messi": "⚽ ميسي", "salah": "⚽ محمد صلاح", "neymar": "⚽ نيمار",
    "amr": "🎤 عمرو دياب", "tamer": "🎤 تامر حسني", "wegz": "🎤 ويجز", "saad": "🎤 احمد سعد",
    "king": "👑 عدي", "robot": "🤖 روبوت", "chipmunk": "🐭 سنجاب", "monster": "👹 وحش",
    "girl": "👧 بنت صغيرة", "old": "👴 راجل عجوز", "ghost": "👻 شبح", "alien": "👽 كائن فضائي",
    "lion": "🦁 اسد", "cat": "🐱 قطة", "dino": "🦖 ديناصور", "santa": "🎅 سانتا",
    "wizard": "🧙 ساحر", "clown": "🤡 مهرج", "devil": "😈 شيطان", "slow": "🐢 سلحفاة",
    "fast": "🐰 ارنب", "phone": "📞 تليفون", "radio": "📻 راديو", "underwater": "🌊 تحت المية",
    "echo": "🏔️ صدى - كهف", "singer": "🎤 مطرب", "news": "🗣️ مذيع اخبار",
}

def convert_voice(input_path, output_path, voice_code):
    filt = VOICE_FILTERS.get(voice_code, VOICE_FILTERS["robot"])
    cmd = ["ffmpeg", "-y", "-i", input_path, "-af", filt, "-c:a", "libmp3lame", "-q:a", "4", output_path]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    return os.path.exists(output_path) and os.path.getsize(output_path) > 1000

@bot.message_handler(commands=['start','help','menu'])
def start(m):
    u = get_user(m.from_user.id, m.from_user.first_name)
    bot.send_message(m.chat.id,
        f"🎤 اهلا بيك في بوت مغير الصوت!\n\n"
        f"👋 ازيك يا {m.from_user.first_name}؟\n\n"
        f"🎙️ ابعتلي اي فويس - وانا هرجعهولك بـ 30 صوت مختلف!\n"
        f"⚽ رونالدو، ميسي، صلاح، روبوت، سنجاب، وحش، بنت، شبح...\n\n"
        f"📊 عدد تحويلاتك: {u['count']}\n"
        f"🎭 صوتك المفضل: {VOICE_NAMES.get(u['fav'], 'لسه مخترتش')}\n\n"
        f"👇 دوس على اي زرار تحت، او ابعت فويس على طول!"
        f"{fmt_rights()}",
        reply_markup=main_kb())

@bot.message_handler(content_types=['voice','audio'])
def handle_voice(m):
    try:
        u = get_user(m.from_user.id, m.from_user.first_name)
        bot.send_message(m.chat.id, "⏳ استلمت الفويس... اختار الصوت اللي عايزه 👇", reply_markup=voices_kb())
        file_info = bot.get_file(m.voice.file_id if m.voice else m.audio.file_id)
        downloaded = bot.download_file(file_info.file_path)
        input_path = f"voice_{m.from_user.id}_{int(time.time())}.ogg"
        with open(input_path, "wb") as f:
            f.write(downloaded)
        u["last_voice"] = input_path
        save()
        bot.send_message(m.chat.id,
            f"✅ الفويس اتحفظ!\n\n🎤 دلوقتي اختار الصوت اللي عايز تحوله ليه من الازرار فوق 👆\n\n"
            f"💡 تقدر تختار اكتر من صوت لنفس الفويس - كل مرة هيطلعلك فويس جديد!"
            f"{fmt_rights()}",
            reply_markup=voices_kb())
    except Exception as e:
        print(f"voice error: {e}")
        bot.send_message(m.chat.id, "❌ حصلت غلطة في الفويس، ابعته تاني")

@bot.message_handler(func=lambda m: True)
def any_msg(m):
    txt = (m.text or "").lower()
    if "فويس" in txt or "صوت" in txt:
        bot.send_message(m.chat.id, "🎤 ابعتلي فويس وانا هحولهولك لأي صوت تختاره 👇", reply_markup=voices_kb())
    else:
        bot.send_message(m.chat.id, "🎤 ابعتلي فويس على طول، او اختار من الازرار 👇", reply_markup=main_kb())

@bot.callback_query_handler(func=lambda c: True)
def callbacks(c):
    uid = c.from_user.id
    try:
        u = get_user(uid, c.from_user.first_name)
        d = c.data or ""
        try: bot.answer_callback_query(c.id)
        except: pass

        if d == "back":
            safe_edit(c, f"🎤 بوت مغير الصوت\n\nابعت فويس واختار الصوت 👇{fmt_rights()}", main_kb()); return
        if d == "how":
            safe_edit(c, f"🎤 ازاي تستخدم البوت؟\n\n1️⃣ ابعت اي فويس (سجل صوتك)\n2️⃣ اختار الصوت من الازرار\n3️⃣ استنى 3 ثواني وهيجيلك الفويس الجديد\n4️⃣ ابعته لصحابك واعملهم مقلب 😂\n\n💡 ممكن تحول نفس الفويس لـ 30 صوت مختلف!\n\n🎤 جرب دلوقتي - سجل فويس وابعته{fmt_rights()}", main_kb()); return
        if d == "voices":
            safe_edit(c, f"🎭 كل الاصوات - 30 صوت\n\nاختار الصوت اللي عايزه 👇\nلو لسه مبعتش فويس، ابعت فويس الاول وبعدين اختار{fmt_rights()}", voices_kb()); return
        if d == "celebs":
            safe_edit(c, f"💎 اصوات المشاهير\n\nاختار حد من المشاهير 👇{fmt_rights()}", celebs_kb()); return
        if d == "cartoons":
            safe_edit(c, f"🤖 اصوات كرتون\n\nاختار صوت كرتوني 👇{fmt_rights()}", cartoons_kb()); return
        if d == "scary":
            safe_edit(c, f"👻 اصوات مرعبة\n\nاختار صوت مرعب وخوف صحابك 😈{fmt_rights()}", scary_kb()); return
        if d == "funny":
            safe_edit(c, f"🎵 اصوات مضحكة\n\nاختار صوت مضحك واعمل مقلب 😂{fmt_rights()}", funny_kb()); return
        if d == "myfav":
            safe_edit(c, f"⭐ صوتك المفضل\n\n🎭 {VOICE_NAMES.get(u['fav'], 'لسه مخترتش')}\n📊 عدد تحويلاتك: {u['count']}{fmt_rights()}", main_kb()); return
        if d == "top":
            sorted_voices = sorted(DB["voices_used"].items(), key=lambda x: x[1], reverse=True)[:10]
            txt = "🏆 اكتر الاصوات استخداما:\n\n"
            for i, (code, cnt) in enumerate(sorted_voices, 1):
                txt += f"{i}. {VOICE_NAMES.get(code, code)} - {cnt} مرة\n"
            if not sorted_voices: txt += "لسه مفيش حد جرب، انت اول واحد!"
            safe_edit(c, txt + fmt_rights(), main_kb()); return
        if d == "stats":
            safe_edit(c, f"📊 احصائياتك\n\n👤 اسمك: {u['name']}\n🎤 عدد تحويلاتك: {u['count']}\n⭐ صوتك المفضل: {VOICE_NAMES.get(u['fav'], 'لسه')}\n📊 اجمالي تحويلات البوت: {DB['total']}{fmt_rights()}", main_kb()); return
        if d == "random_voice_info":
            if not u.get("last_voice"):
                safe_edit(c, f"🎲 ابعت فويس الاول وبعدين دوس صوت عشوائي!\n\n🎤 سجل اي حاجة وابعتهالي{fmt_rights()}", main_kb()); return
            code = random.choice(list(VOICE_NAMES.keys()))
            do_convert(c, u, code); return
        if d == "rights":
            safe_edit(c, f"👑 حقوق عدي\n\n"
                f"👑 البوت ده من صنع عدي\n"
                f"👑 جميع الحقوق محفوظة لـ عدي © 2026\n"
                f"👑 ممنوع سرقة الكود او ازالة الحقوق\n"
                f"👑 ممنوع نسخ البوت بدون اذن عدي\n\n"
                f"🎤 بوت مغير الصوت - النسخة الاصلية\n"
                f"👑 لو عايز بوت زي ده كلم عدي", main_kb()); return

        if d.startswith("voice_"):
            code = d.replace("voice_", "")
            if not u.get("last_voice") or not os.path.exists(u["last_voice"]):
                safe_edit(c, f"🎤 ابعت فويس الاول!\n\n🎙️ سجل اي حاجة بصوتك وابعتهالي، وبعدين اختار الصوت ده تاني 👇\n\n🎭 الصوت اللي اخترته: {VOICE_NAMES.get(code, code)}{fmt_rights()}", voices_kb()); return
            do_convert(c, u, code); return

        safe_edit(c, f"🎤 بوت مغير الصوت\n\nابعت فويس واختار الصوت 👇{fmt_rights()}", main_kb())
    except Exception as e:
        print(f"callback error: {e}")
        traceback.print_exc()
        try: bot.send_message(c.message.chat.id, "حصلت غلطة، ابعت الفويس تاني 🎤", reply_markup=main_kb())
        except: pass

def do_convert(c, u, code):
    try:
        bot.send_message(c.message.chat.id, f"⏳ بحوّل صوتك لـ {VOICE_NAMES.get(code, code)}... استنى 3 ثواني 🎤")
        input_path = u["last_voice"]
        output_path = f"out_{c.from_user.id}_{int(time.time())}_{code}.mp3"
        ok = convert_voice(input_path, output_path, code)
        if ok:
            u["count"] += 1; u["fav"] = code; DB["total"] += 1
            DB["voices_used"][code] = DB["voices_used"].get(code, 0) + 1
            save()
            with open(output_path, "rb") as f:
                bot.send_voice(c.message.chat.id, f, caption=f"🎤 صوتك بقى: {VOICE_NAMES.get(code, code)}\n\n🎙️ جرب صوت تاني من الازرار 👇\n{fmt_rights()}", reply_markup=voices_kb())
            try: os.remove(output_path)
            except: pass
            bot.send_message(c.message.chat.id, f"🎉 خلاص! صوتك بقى {VOICE_NAMES.get(code, code)}\n\n🎤 عايز تجرب صوت تاني لنفس الفويس؟ دوس على اي زرار 👇\n📊 تحويلاتك: {u['count']}{fmt_rights()}", reply_markup=voices_kb())
        else:
            bot.send_message(c.message.chat.id, "❌ حصلت غلطة في التحويل، ابعت الفويس تاني وجرب صوت تاني 🎤", reply_markup=voices_kb())
    except Exception as e:
        print(f"convert error: {e}")
        bot.send_message(c.message.chat.id, "❌ حصلت غلطة، جرب فويس تاني او صوت تاني 🎤", reply_markup=voices_kb())

if __name__ == "__main__":
    print("Voice Bot is running... 🎤 - عدي")
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
