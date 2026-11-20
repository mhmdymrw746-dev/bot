import os, requests, telebot, random
from datetime import date, timedelta, datetime, timezone
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
from threading import Thread

app = Flask(__name__)
b = telebot.TeleBot(os.environ.get("TOKEN"), parse_mode="HTML")
@app.route('/')
def home(): return "Bot is Running!"

waiting = []
partners = {}

# ===== خريطة الدوريات - اسم شيك + علم =====
LEAGUE_NAMES = {
    "eng.1": "🏴󐁧󐁢󐁥󐁮󐁧󐁿 الدوري الإنجليزي",
    "esp.1": "🇪🇸 الدوري الإسباني",
    "ita.1": "🇮🇹 الدوري الإيطالي",
    "ger.1": "🇩🇪 الدوري الألماني",
    "fra.1": "🇫🇷 الدوري الفرنسي",
    "ned.1": "🇳🇱 الدوري الهولندي",
    "por.1": "🇵🇹 الدوري البرتغالي",
    "egy.1": "🇪🇬 الدوري المصري",
    "sau.1": "🇸🇦 الدوري السعودي",
    "tur.1": "🇹🇷 الدوري التركي",
    "arg.1": "🇦🇷 الدوري الأرجنتيني",
    "bra.1": "🇧🇷 الدوري البرازيلي",
    "mex.1": "🇲🇽 الدوري المكسيكي",
    "usa.1": "🇺🇸 الدوري الأمريكي",
    "uefa.champions": "⭐ دوري أبطال أوروبا",
    "uefa.europa": "🟠 الدوري الأوروبي",
}
LEAGUES = list(LEAGUE_NAMES.keys())

def main_kb():
    k = InlineKeyboardMarkup(row_width=2)
    k.add(
        InlineKeyboardButton("🔴 • لايف الآن", callback_data="live"),
        InlineKeyboardButton("📅 • اليوم", callback_data="today"),
        InlineKeyboardButton("⏭️ • بكرة", callback_data="tomorrow"),
        InlineKeyboardButton("📆 • بعده", callback_data="after"),
        InlineKeyboardButton("🗓️ • الأسبوع", callback_data="week"),
        InlineKeyboardButton("🎲 • 💬 تــدويــر | لاقي حد", callback_data="random"),
    )
    return k

def chat_kb():
    k = InlineKeyboardMarkup(row_width=2)
    k.add(
        InlineKeyboardButton("⏭️  التالي", callback_data="next"),
        InlineKeyboardButton("🛑  إنهاء", callback_data="stop"),
    )
    return k

def stop_chat(uid, notify=True):
    p = partners.pop(uid, None)
    if p:
        partners.pop(p, None)
        if notify:
            try: b.send_message(p, "😢 <b>الشخص ساب المحادثة</b>\nدوس تدوير تاني 👇", reply_markup=main_kb())
            except: pass
    if uid in waiting: waiting.remove(uid)
    return p

def find_partner(uid):
    if uid in waiting: waiting.remove(uid)
    cand = [u for u in waiting if u != uid]
    if cand:
        partner = random.choice(cand)
        waiting.remove(partner)
        partners[uid]=partner; partners[partner]=uid
        msg = "╔══════════════╗\n  🎉  <b>لقيتلك حد!</b>  🎉\n╚══════════════╝\n\n💬 اتكلم براحتك\n🙈 محدش يعرف انت مين"
        b.send_message(uid, msg, reply_markup=chat_kb())
        b.send_message(partner, msg, reply_markup=chat_kb())
    else:
        waiting.append(uid)
        b.send_message(uid, "🔍 <b>بدورلك على حد...</b>\n⏳ استنى ثواني", reply_markup=chat_kb())

def to_egypt_time(iso):
    # ESPN بيرجع بتوقيت جرينتش، نحوله لمصر +2
    try:
        dt = datetime.fromisoformat(iso.replace("Z","+00:00"))
        dt = dt + timedelta(hours=2)
        return dt.strftime("%H:%M")
    except:
        return iso[11:16]

def get_matches(ds):
    all_m=[]
    for lg in LEAGUES:
        try:
            r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/scoreboard?dates={ds}", timeout=10).json()
            for e in r.get("events",[]):
                comp=e.get("competitions",[{}])[0]
                teams=comp.get("competitors",[])
                if len(teams)<2: continue
                home=next((t for t in teams if t.get("homeAway")=="home"),teams[0])
                away=next((t for t in teams if t.get("homeAway")=="away"),teams[1])
                all_m.append({
                    "home":home.get("team",{}).get("displayName","?"),
                    "away":away.get("team",{}).get("displayName","?"),
                    "league": LEAGUE_NAMES.get(lg, lg),
                    "league_key": lg,
                    "time": to_egypt_time(e.get("date","")),
                    "status":e.get("status",{}).get("type",{}).get("description",""),
                    "state":e.get("status",{}).get("type",{}).get("state",""),
                    "sh":home.get("score"), "sa":away.get("score")
                })
        except: continue
    return all_m

def send_day(chat_id, day_obj, only_live=False):
    ds=day_obj.strftime("%Y%m%d")
    show=day_obj.strftime("%d / %m / %Y")
    b.send_message(chat_id, f"⏳ <b>بحمل ماتشات {show}...</b>")
    ms=get_matches(ds)
    if only_live: ms=[m for m in ms if m["state"]=="in"]
    if not ms:
        b.send_message(chat_id, "😴 <b>مفيش ماتشات دلوقتي</b>", reply_markup=main_kb()); return

    # نجمع الماتشات حسب الدوري عشان الشكل يبقى نضيف
    from collections import OrderedDict
    grouped = OrderedDict()
    for m in ms:
        grouped.setdefault(m["league"], []).append(m)

    txt = f"╔══════════════════╗\n   ⚽ <b>ماتشات {show}</b> ⚽\n   🌍 <b>{len(ms)} ماتش</b> • 🇪🇬 <b>بتوقيت مصر</b>\n╚══════════════════╝\n\n"
    for league, games in grouped.items():
        txt += f"━━━━━━━━━━━━━━\n{league}  •  {len(games)} ماتش\n━━━━━━━━━━━━━━\n"
        for m in games:
            if m["state"]=="in":
                txt+=f"🔴  <b>{m['home']}  {m['sh']} - {m['sa']}  {m['away']}</b>\n    ⏱️ {m['status']}\n"
            elif m["state"]=="post":
                txt+=f"✅  <b>{m['home']}  {m['sh']} - {m['sa']}  {m['away']}</b>\n"
            else:
                txt+=f"⏰  <b>{m['time']}</b>  |  {m['home']}  🆚  {m['away']}\n"
        txt += "\n"
    for i in range(0,len(txt),4000):
        b.send_message(chat_id, txt[i:i+4000])
    b.send_message(chat_id, "⚡ <b>اختار اللي بعده 👇</b>", reply_markup=main_kb())

@b.message_handler(commands=['start'])
def start(m):
    b.send_message(m.chat.id,
        "╔══════════════════╗\n"
        "   ⚽  <b>أهلا بيك يا نجم</b>  ⚽\n"
        "╚══════════════════╝\n\n"
        "🌍 <b>كل ماتشات العالم</b> بتوقيت مصر\n"
        "💬 <b>تدوير</b> لاقي حد تتكلم معاه\n\n"
        "👇 <b>اختار:</b>", reply_markup=main_kb())

@b.callback_query_handler(func=lambda c: True)
def cb(c):
    chat=c.message.chat.id
    b.answer_callback_query(c.id, "تمام ⚡")
    if c.data=="random":
        if chat in partners: b.send_message(chat, "انت بتتكلم مع حد دلوقتي", reply_markup=chat_kb())
        else: find_partner(chat)
    elif c.data=="next": stop_chat(chat); find_partner(chat)
    elif c.data=="stop": stop_chat(chat); b.send_message(chat, "✅ <b>خلصت المحادثة</b>", reply_markup=main_kb())
    elif c.data=="live": send_day(chat, date.today(), True)
    elif c.data=="today": send_day(chat, date.today())
    elif c.data=="tomorrow": send_day(chat, date.today()+timedelta(days=1))
    elif c.data=="after": send_day(chat, date.today()+timedelta(days=2))
    elif c.data=="week":
        for i in range(3): send_day(chat, date.today()+timedelta(days=i))

@b.message_handler(content_types=['text','photo','voice','video','sticker','animation'])
def any_msg(m):
    uid=m.chat.id
    if uid in partners:
        pid=partners[uid]
        try:
            if m.content_type=='text': b.send_message(pid, f"💬 {m.text}")
            elif m.content_type=='photo': b.send_photo(pid, m.photo[-1].file_id, caption=m.caption or "")
            elif m.content_type=='voice': b.send_voice(pid, m.voice.file_id)
            elif m.content_type=='video': b.send_video(pid, m.video.file_id)
            elif m.content_type=='sticker': b.send_sticker(pid, m.sticker.file_id)
            elif m.content_type=='animation': b.send_animation(pid, m.animation.file_id)
        except:
            b.send_message(uid, "الشخص التاني خرج 😢", reply_markup=main_kb()); stop_chat(uid, False)
    else:
        if m.text and not m.text.startswith("/"):
            b.send_message(uid, "👇 <b>اختار من القايمة:</b>", reply_markup=main_kb())

def run_bot(): b.infinity_polling(skip_pending=True)
Thread(target=run_bot, daemon=True).start()
if __name__=='__main__': app.run(host='0.0.0.0', port=int(os.environ.get("PORT",10000)))
