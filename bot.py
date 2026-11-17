import os, time, threading, re, datetime
from collections import defaultdict
from flask import Flask
import telebot

# ===== سيرفر Render =====
app = Flask(__name__)
@app.route('/')
def home(): return "Protection Bot Running!"
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
threading.Thread(target=run_flask, daemon=True).start()

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
bot.remove_webhook()
time.sleep(2)

# ===== ذاكرة =====
warnings_db = defaultdict(int)
user_msgs = defaultdict(list)
join_times = defaultdict(list)
settings_db = defaultdict(lambda: {
    "lock_link": True, "lock_forward": True, "lock_media": False,
    "lock_sticker": False, "lock_photo": False, "lock_video": False,
    "lock_voice": False, "lock_gif": False,
    "raid_mode": False, "night_mode": False, "welcome": True,
    "max_warn": 3, "flood_limit": 5
})

banned_words = ["كس","شرموط","متناك","كسمك","xxx","porn","sex","fuck","قمار","كازينو","حشيش","مخدرات","دعارة","نيك","طيز","زب","عرص","خول","قحبة"]
links_pattern = r"(http|https|t\.me|telegram\.me|@\w+|www\.|\.com|\.net)"

def is_admin(chat_id, user_id):
    try:
        m = bot.get_chat_member(chat_id, user_id)
        return m.status in ["creator", "administrator"]
    except: return False

def punish(m, reason):
    try: bot.delete_message(m.chat.id, m.message_id)
    except: pass
    warnings_db[m.from_user.id] += 1
    s = settings_db[m.chat.id]
    c = warnings_db[m.from_user.id]
    if c >= s["max_warn"]:
        try:
            bot.ban_chat_member(m.chat.id, m.from_user.id)
            bot.send_message(m.chat.id, f"🚫 {m.from_user.first_name} اتحظر - السبب: {reason}")
        except:
            bot.send_message(m.chat.id, "❌ اديني صلاحية Admin كاملة!")
        warnings_db[m.from_user.id] = 0
    else:
        bot.send_message(m.chat.id, f"⚠️ {m.from_user.first_name} تحذير {c}/{s['max_warn']}\nالسبب: {reason}")

@bot.message_handler(content_types=['new_chat_members'])
def welcome(m):
    s = settings_db[m.chat.id]
    now = time.time()
    join_times[m.chat.id].append(now)
    join_times[m.chat.id] = [t for t in join_times[m.chat.id] if now - t < 30]
    if len(join_times[m.chat.id]) > 5:
        s["raid_mode"] = True
        bot.send_message(m.chat.id, "🚨 هجوم بوتات! اتفعل Raid Mode")
    for u in m.new_chat_members:
        if u.is_bot and u.id != bot.get_me().id:
            try: bot.ban_chat_member(m.chat.id, u.id)
            except: pass
            continue
        if s["welcome"]:
            bot.send_message(m.chat.id, f"👋 اهلا {u.first_name} نورت الجروب!\n📜 اكتب /rules\n🚫 ممنوع الروابط والسبام")

@bot.message_handler(func=lambda m: m.chat.type in ["group","supergroup"], content_types=['text','photo','video','sticker','animation','voice','audio','document','video_note'])
def protect(m):
    if is_admin(m.chat.id, m.from_user.id): return
    s = settings_db[m.chat.id]
    text = m.text or m.caption or ""
    hour = datetime.datetime.now().hour
    if s["night_mode"] and 2 <= hour < 6:
        punish(m, "الجروب مقفول بالليل 🌙"); return
    if s["lock_forward"] and (m.forward_from or m.forward_from_chat):
        punish(m, "فورورد ممنوع"); return
    if s["lock_link"] and re.search(links_pattern, text, re.IGNORECASE):
        punish(m, "روابط ممنوعة"); return
    if s["lock_media"] and m.content_type in ['photo','video','animation','document']:
        punish(m, "ميديا مقفولة"); return
    if s["lock_sticker"] and m.content_type == 'sticker':
        punish(m, "ستيكرات مقفولة"); return
    if s["lock_photo"] and m.content_type == 'photo':
        punish(m, "صور مقفولة"); return
    if s["lock_video"] and m.content_type in ['video','video_note']:
        punish(m, "فيديو مقفول"); return
    if s["lock_voice"] and m.content_type in ['voice','audio']:
        punish(m, "فويس مقفول"); return
    for w in banned_words:
        if w in text.lower():
            punish(m, "كلمة ممنوعة"); return
    now = time.time()
    user_msgs[m.from_user.id].append(now)
    user_msgs[m.from_user.id] = [t for t in user_msgs[m.from_user.id] if now - t < 5]
    if len(user_msgs[m.from_user.id]) > s["flood_limit"]:
        punish(m, "سبام / تكرار سريع"); user_msgs[m.from_user.id] = []; return
    if len(text) > 1500:
        punish(m, "رسالة طويلة جدا"); return

@bot.message_handler(commands=['start','help'])
def start_help(m):
    bot.send_message(m.chat.id, """🛡️ <b>بوت حماية</b>
/ban - حظر | /kick - طرد
/mute - كتم | /unmute - فك كتم
/warn - تحذير | /unwarn - شيل تحذير
/lock link - قفل روابط
/unlock link - فتح روابط
/lock media - قفل ميديا
/lock sticker - قفل ستيكرات
/rules - القوانين
/settings - الاعدادات
/report - تبليغ
/raid on - وضع هجوم
/night on - وضع ليلي
/pin - تثبيت""")

@bot.message_handler(commands=['ban','kick','mute','unmute','unban','warn','unwarn'])
def admin_actions(m):
    if not is_admin(m.chat.id, m.from_user.id):
        bot.reply_to(m, "❌ للادمن بس!"); return
    if not m.reply_to_message:
        bot.reply_to(m, "❌ رد على رسالة الشخص!"); return
    target = m.reply_to_message.from_user
    cmd = m.text.split()[0].replace('/','').split('@')[0]
    try:
        if cmd == 'ban':
            bot.ban_chat_member(m.chat.id, target.id)
            bot.send_message(m.chat.id, f"🚫 {target.first_name} اتحظر")
        elif cmd == 'kick':
            bot.ban_chat_member(m.chat.id, target.id)
            bot.unban_chat_member(m.chat.id, target.id)
            bot.send_message(m.chat.id, f"👢 {target.first_name} اتطرد")
        elif cmd == 'mute':
            bot.restrict_chat_member(m.chat.id, target.id, can_send_messages=False, until_date=int(time.time())+3600)
            bot.send_message(m.chat.id, f"🔇 {target.first_name} اتكتم ساعة")
        elif cmd == 'unmute':
            bot.restrict_chat_member(m.chat.id, target.id, can_send_messages=True, can_send_media_messages=True)
            bot.send_message(m.chat.id, f"🔊 {target.first_name} اتفك كتمه")
        elif cmd == 'unban':
            bot.unban_chat_member(m.chat.id, target.id)
            bot.send_message(m.chat.id, f"✅ {target.first_name} اتفك حظره")
        elif cmd == 'warn':
            warnings_db[target.id] += 1
            bot.send_message(m.chat.id, f"⚠️ {target.first_name} تحذير {warnings_db[target.id]}/3")
            if warnings_db[target.id] >= 3:
                bot.ban_chat_member(m.chat.id, target.id); warnings_db[target.id]=0
        elif cmd == 'unwarn':
            warnings_db[target.id] = 0
            bot.send_message(m.chat.id, f"✅ اتشال التحذير من {target.first_name}")
    except:
        bot.send_message(m.chat.id, "❌ اديني صلاحية Admin كاملة!")

@bot.message_handler(commands=['lock','unlock'])
def lock_cmd(m):
    if not is_admin(m.chat.id, m.from_user.id): return
    parts = m.text.split()
    if len(parts) < 2:
        bot.reply_to(m, "مثال: /lock link"); return
    what = parts[1].lower(); s = settings_db[m.chat.id]
    on = m.text.startswith('/lock')
    mp = {"link":"lock_link","forward":"lock_forward","media":"lock_media","sticker":"lock_sticker","photo":"lock_photo","video":"lock_video","voice":"lock_voice","gif":"lock_gif"}
    if what in mp:
        s[mp[what]] = on
        bot.send_message(m.chat.id, f"{'🔒 اتقفل' if on else '🔓 اتفتح'}: {what}")

@bot.message_handler(commands=['settings'])
def settings_cmd(m):
    s = settings_db[m.chat.id]
    txt = "⚙️ <b>اعدادات الجروب:</b>\n"
    for k,v in s.items(): txt += f"{k}: {'✅' if v else '❌'}\n"
    bot.send_message(m.chat.id, txt)

@bot.message_handler(commands=['rules'])
def rules_cmd(m):
    bot.send_message(m.chat.id, "📜 <b>قوانين الجروب:</b>\n1- ممنوع الروابط\n2- ممنوع السبام\n3- ممنوع الشتايم\n4- ممنوع الفورورد\n5- 3 تحذيرات = حظر")

@bot.message_handler(commands=['pin'])
def pin_cmd(m):
    if is_admin(m.chat.id, m.from_user.id) and m.reply_to_message:
        bot.pin_chat_message(m.chat.id, m.reply_to_message.message_id)
        bot.send_message(m.chat.id, "📌 اتثبت!")

@bot.message_handler(commands=['report'])
def report_cmd(m):
    if m.reply_to_message:
        bot.send_message(m.chat.id, "✅ اتبعت التبليغ للادمن")
        try:
            admins = bot.get_chat_administrators(m.chat.id)
            for a in admins:
                bot.send_message(a.user.id, f"🚨 تبليغ في {m.chat.title} على {m.reply_to_message.from_user.first_name}")
        except: pass

@bot.message_handler(commands=['raid','night'])
def modes(m):
    if not is_admin(m.chat.id, m.from_user.id): return
    s = settings_db[m.chat.id]
    on = "on" in m.text
    if m.text.startswith('/raid'): s["raid_mode"] = on
    else: s["night_mode"] = on
    bot.send_message(m.chat.id, f"✅ تم: {'ON' if on else 'OFF'}")

@bot.message_handler(commands=['clean'])
def clean(m):
    if is_admin(m.chat.id, m.from_user.id):
        warnings_db.clear()
        bot.send_message(m.chat.id, "🧹 اتمسحت كل التحذيرات")

print("Protection Bot Running...")
bot.infinity_polling()
