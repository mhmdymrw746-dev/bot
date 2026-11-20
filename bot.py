
import os, requests, telebot
from datetime import date, timedelta
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
from threading import Thread

app = Flask(__name__)
b = telebot.TeleBot(os.environ.get("TOKEN"))
A = "https://www.thesportsdb.com/api/v1/json/3"

@app.route('/')
def home():
    return "Bot is Running!"

def kb():
    k = InlineKeyboardMarkup(row_width=2)
    k.add(
        InlineKeyboardButton("🔴 لايف دلوقتي", callback_data="live"),
        InlineKeyboardButton("📅 النهاردة", callback_data="today"),
        InlineKeyboardButton("📆 بكرة", callback_data="tomorrow"),
        InlineKeyboardButton("📆 بعده", callback_data="after"),
        InlineKeyboardButton("🗓️ الاسبوع كله", callback_data="week"),
        InlineKeyboardButton("🌍 كل الماتشات", callback_data="all")
    )
    return k

def send_day(chat_id, day):
    try:
        r = requests.get(f"{A}/eventsday.php?d={day}&s=Soccer", timeout=20).json()
        ev = r.get("events") or []
        if not ev:
            b.send_message(chat_id, f"مفيش ماتشات يوم {day} 😴")
            return
        txt = f"📅 ماتشات {day} 🌍\nالعدد: {len(ev)} ماتش\n\n"
        c = 0
        for e in ev:
            t = str(e.get("strTime",""))[:5]
            txt += f"⏰ {t} | {e['strHomeTeam']} vs {e['strAwayTeam']}\n🏆 {e.get('strLeague','')} - {e.get('strCountry','')}\n\n"
            c += 1
            if c % 12 == 0:
                b.send_message(chat_id, txt)
                txt = ""
        if txt:
            b.send_message(chat_id, txt)
    except:
        b.send_message(chat_id, "حصل خطأ جرب تاني")

@b.message_handler(commands=['start'])
def start(m):
    b.send_message(m.chat.id, "بوت الكورة العالمي 🌍⚽🔥\n\nكل مواعيد الماتشات من كل الدول\nاختار من الزراير 👇", reply_markup=kb())

@b.callback_query_handler(func=lambda c: True)
def cb(c):
    chat = c.message.chat.id
    b.answer_callback_query(c.id, "بحمل الماتشات... ⏳")
    if c.data == "live":
        try:
            r = requests.get(f"{A}/livescore.php?s=Soccer", timeout=20).json()
            ev = r.get("events") or []
            if not ev:
                b.send_message(chat, "مفيش ماتشات شغالة دلوقتي 😴", reply_markup=kb())
                return
            txt = f"🔴 لايف دلوقتي - {len(ev)} ماتش\n\n"
            for e in ev:
                txt += f"{e['strHomeTeam']} {e['intHomeScore']} - {e['intAwayScore']} {e['strAwayTeam']}\n🏆 {e.get('strLeague','')} - {e.get('strCountry','')} | {e.get('strStatus','')}\n\n"
            for i in range(0, len(txt), 4000):
                b.send_message(chat, txt[i:i+4000])
            b.send_message(chat, "اختار تاني 👇", reply_markup=kb())
        except:
            b.send_message(chat, "حصل خطأ", reply_markup=kb())
    elif c.data == "today":
        send_day(chat, date.today().strftime("%Y-%m-%d"))
        b.send_message(chat, "خلصت 👇", reply_markup=kb())
    elif c.data == "tomorrow":
        send_day(chat, (date.today()+timedelta(days=1)).strftime("%Y-%m-%d"))
        b.send_message(chat, "خلصت 👇", reply_markup=kb())
    elif c.data == "after":
        send_day(chat, (date.today()+timedelta(days=2)).strftime("%Y-%m-%d"))
        b.send_message(chat, "خلصت 👇", reply_markup=kb())
    elif c.data == "week":
        for i in range(7):
            send_day(chat, (date.today()+timedelta(days=i)).strftime("%Y-%m-%d"))
        b.send_message(chat, "دي كل ماتشات الاسبوع 👇", reply_markup=kb())
    elif c.data == "all":
        for i in range(3):
            send_day(chat, (date.today()+timedelta(days=i)).strftime("%Y-%m-%d"))
        b.send_message(chat, "دي كل الماتشات 👇", reply_markup=kb())

def run_bot():
    b.infinity_polling()

Thread(target=run_bot).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
