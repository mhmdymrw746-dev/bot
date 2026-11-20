import os, requests, telebot, random
from datetime import date, timedelta
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
from threading import Thread

app = Flask(__name__)
b = telebot.TeleBot(os.environ.get("TOKEN"), parse_mode="HTML")
WELCOME_PHOTO = "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=800"

@app.route('/')
def home():
    return "Bot is Running!"

waiting = []
partners = {}

# ======== جرافيك الزراير ========
def main_kb():
    k = InlineKeyboardMarkup(row_width=2)
    k.add(
        InlineKeyboardButton("🔴  •  لايف دلوقتي", callback_data="live"),
        InlineKeyboardButton("📅  •  النهاردة", callback_data="today"),
        InlineKeyboardButton("📆  •  بكرة", callback_data="tomorrow"),
        InlineKeyboardButton("🗓️  •  الاسبوع كله", callback_data="week"),
    )
    k.add(InlineKeyboardButton("💬  •  🎲 تــدويــر | لاقي حد تتكلم معاه", callback_data="random"))
    k.add(InlineKeyboardButton("⭐  •  تقييم البوت", callback_data="rate"))
    return k

def chat_kb():
    k = InlineKeyboardMarkup(row_width=2)
    k.add(
        InlineKeyboardButton("⏭️  التالي", callback_data="next"),
        InlineKeyboardButton("🛑  إنهاء", callback_data="stop"),
        InlineKeyboardButton("🏠  القايمة الرئيسية", callback_data="home"),
    )
    return k

def stop_chat(uid, notify=True):
    p = partners.pop(uid, None)
    if p:
        partners.pop(p, None)
        if notify:
            try: b.send_message(p, "💔 <b>الشخص اللي معاك ساب المحادثة</b>\n\nدوس تدوير تاني عشان تلاقي حد جديد 👇", reply_markup=main_kb())
            except: pass
    if uid in waiting: waiting.remove(uid)
    return p

def find_partner(uid):
    if uid in waiting: waiting.remove(uid)
    cands = [u for u in waiting if u != uid]
    if cands:
        p = random.choice(cands)
        waiting.remove(p)
        partners[uid] = p; partners[p] = uid
        msg = "🎉 <b>لقيتلك حد تتكلم معاه!</b>\n\n💬 اتكلم براحتك، صور، فويس، اي حاجة\n⚠️ محدش يعرف انت مين\n⏭️ لو زهقت دوس <b>التالي</b>"
        b.send_message(uid, msg, reply_markup=chat_kb())
        b.send_message(p, msg, reply_markup=chat_kb())
        return True
    else:
        waiting.append(uid)
        b.send_message(uid, "🔍 <b>بدورلك على حد...</b>\n\n⏳ استنى شوية، اول ما نلاقي حد هنوصلكم ببعض\n\n<i>نصيحة: ابعت اللينك لصحابك عشان التدوير يبقى اسرع</i>", reply_markup=chat_kb())
        return False

# ======== الكورة ========
LEAGUES = ["eng.1","esp.1","ita.1","ger.1","fra.1","ned.1","por.1","egy.1","sau.1","tur.1","arg.1","bra.1","mex.1","usa.1","uefa.champions","uefa.europa"]

def get_matches(ds):
    out=[]
    for lg in LEAGUES:
        try:
            r = requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/scoreboard?dates={ds}", timeout=10).json()
            for e in r.get("events", []):
                comp = e.get("competitions", [{}])[0]
                teams = comp.get("competitors", [])
                if len(teams)<2: continue
                home = next((t for t in teams if t.get("homeAway")=="home"), teams[0])
                away = next((t for t in teams if t.get("homeAway")=="away"), teams[1])
                out.append({
                    "home": home.get("team", {}).get("displayName","?"),
                    "away": away.get("team", {}).get("displayName","?"),
                    "league": e.get("league", {}).get("name") or lg,
                    "time": e.get("date","")[11:16],
                    "status": e.get("status", {}).get("type", {}).get("description",""),
                    "state": e.get("status", {}).get("type", {}).get("state",""),
                    "sh": home.get("score"), "sa": away.get("score")
                })
        except: continue
    return out

def send_day(chat_id, day_obj, only_live=False):
    ds = day_obj.strftime("%Y%m%d")
    show = day_obj.strftime("%Y-%m-%d")
    b.send_message(chat_id, f"⏳ <b>جاري تحميل ماتشات {show}...</b>")
    matches = get_matches(ds)
    if only_live:
        matches = [m for m in matches if m["state"]=="in"]
        if not matches:
            b.send_message(chat_id, "😴 <b>مفيش ماتشات لايف دلوقتي</b>\n\nجرب بعد شوية 👇", reply_markup=main_kb())
            return
        txt = f"🔴 <b>لايف دلوقتي</b>  •  {len(matches)} ماتش\n━━━━━━━━━━━━━━\n\n"
        for m in matches:
            txt += f"🔴 <b>{m['home']} {m['sh']} - {m['sa']} {m['away']}</b>\n🏆 {m['league']}  •  {m['status']}\n➖➖➖➖➖➖\n"
    else:
        if not matches:
            b.send_message(chat_id, f"😴 <b>مفيش ماتشات يوم {show}</b>", reply_markup=main_kb())
            return
        txt = f"⚽ <b>ماتشات {show}</b>\n🌍 <b>{len(matches)} ماتش من كل العالم</b>\n━━━━━━━━━━━━━━\n\n"
        for m in matches:
            if m["state"]=="in":
                txt += f"🔴 <b>{m['home']} {m['sh']} - {m['sa']} {m['away']}</b>\n🏆 {m['league']}\n➖➖➖➖➖➖\n"
            elif m["state"]=="post":
                txt += f"✅ <b>{m['home']} {m['sh']} - {m['sa']} {m['away']}</b>\n🏆 {m['league']}\n➖➖➖➖➖➖\n"
            else:
                txt += f"⏰ <b>{m['time']}</b>  |  <b>{m['home']}</b> 🆚 <b>{m['away']}</b>\n🏆 {m['league']}\n➖➖➖➖➖➖\n"
    for i in range(0, len(txt), 4000):
        b.send_message(chat_id, txt[i:i+4000])
    b.send_message(chat_id, "👇 <b>اختار تاني</b>", reply_markup=main_kb())

# ======== Handlers ========
@b.message_handler(commands=['start'])
def start(m):
    try:
        b.send_photo(m.chat.id, WELCOME_PHOTO, caption="""⚽ <b>أهلا بيك في MOHAMEDY BOT 🔥</b>

━━━━━━━━━━━━━━
🌍 <b>قسم الكورة</b>
كل ماتشات العالم - لايف و مواعيد

💬 <b>قسم التدوير</b>
لاقي حد عشوائي تتكلم معاه
من غير ما حد يعرف انت مين

━━━━━━━━━━━━━━
👇 <b>اختار من هنا</b>""", reply_markup=main_kb())
    except:
        b.send_message(m.chat.id, "⚽ <b>أهلا بيك في MOHAMEDY BOT 🔥</b>\n\nاختار 👇", reply_markup=main_kb())

@b.callback_query_handler(func=lambda c: True)
def cb(c):
    chat = c.message.chat.id
    b.answer_callback_query(c.id, "تمام ✨")
    if c.data == "home":
        b.send_message(chat, "🏠 <b>القايمة الرئيسية</b>", reply_markup=main_kb())
    elif c.data == "rate":
        b.send_message(chat, "⭐ <b>شكرا يا وحش!</b>\nابعت البوت لصحابك وخلي التدوير يولع 🔥", reply_markup=main_kb())
    elif c.data == "random":
        if chat in partners: b.send_message(chat, "انت بتتكلم مع حد دلوقتي", reply_markup=chat_kb())
        else: find_partner(chat)
    elif c.data == "next":
        stop_chat(chat); find_partner(chat)
    elif c.data == "stop":
        stop_chat(chat); b.send_message(chat, "✅ <b>خلصت المحادثة</b>", reply_markup=main_kb())
    elif c.data == "live": send_day(chat, date.today(), only_live=True)
    elif c.data == "today": send_day(chat, date.today())
    elif c.data == "tomorrow": send_day(chat, date.today()+timedelta(days=1))
    elif c.data == "week":
        for i in range(7): send_day(chat, date.today()+timedelta(days=i))

@b.message_handler(content_types=['text','photo','voice','video','sticker','animation'])
def any_msg(m):
    uid = m.chat.id
    if uid in partners:
        pid = partners[uid]
        try:
            if m.content_type == 'text': b.send_message(pid, f"💬 {m.text}")
            elif m.content_type == 'photo': b.send_photo(pid, m.photo[-1].file_id, caption=m.caption or "")
            elif m.content_type == 'voice': b.send_voice(pid, m.voice.file_id)
            elif m.content_type == 'video': b.send_video(pid, m.video.file_id)
            elif m.content_type == 'sticker': b.send_sticker(pid, m.sticker.file_id)
            elif m.content_type == 'animation': b.send_animation(pid, m.animation.file_id)
        except:
            b.send_message(uid, "الشخص التاني قفل", reply_markup=main_kb()); stop_chat(uid, notify=False)
    else:
        if m.text and not m.text.startswith("/"):
            b.send_message(uid, "👇 <b>اختار من القايمة</b>", reply_markup=main_kb())

def run_bot():
    b.infinity_polling(skip_pending=True)
Thread(target=run_bot, daemon=True).start()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
