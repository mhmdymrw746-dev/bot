import telebot, time
from flask import Flask
import threading
BOT_TOKEN = "9005250007:AAEumlmOgX2uQKyfTGdJrG6Nvq3RU657b4Q"
ADMIN_ID = 8188263997
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)
users = {}
@bot.message_handler(commands=['start'])
def start(m):
    if m.from_user.id == ADMIN_ID:
        bot.send_message(m.chat.id, "Bot is ON")
    else:
        bot.send_message(m.chat.id, "اهلا")
@bot.message_handler(func=lambda m: True, content_types=['text','photo','video','voice','document','sticker','audio'])
def handle_all(m):
    if m.from_user.id == ADMIN_ID:
        if m.reply_to_message and m.reply_to_message.message_id in users:
            user_id = users[m.reply_to_message.message_id]
            try:
                bot.copy_message(user_id, m.chat.id, m.message_id)
                bot.reply_to(m, "Sent")
            except:
                bot.reply_to(m, "Blocked")
        return
    try:
        fwd = bot.forward_message(ADMIN_ID, m.chat.id, m.message_id)
        users[fwd.message_id] = m.chat.id
        bot.reply_to(m, "وصلت")
    except Exception as e:
        print(e)
def run_bot():
    while True:
        try:
            bot.infinity_polling()
        except:
            time.sleep(5)
@app.route('/')
def home():
    return "Bot is running"
if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=10000)
from flask import Flask
from threading import Thread
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import os

TOKEN = os.environ.get("9005250007:AAEumlmOgX2uQKyfTGdJrG6Nvq3RU657b4Q")
bot = telebot.TeleBot(9005250007:AAEumlmOgX2uQKyfTGdJrG6Nvq3RU657b4Q)
app = Flask(__name__)

waiting = None
pairs = {}

def main_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("🎲 /play"), KeyboardButton("⛔ /stop"))
    return markup

@app.route('/')
def home():
    return "Random Bot is Live!"

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "أهلا! 😎\nدوس على الأزرار تحت", reply_markup=main_keyboard())

@bot.message_handler(commands=['play'])
@bot.message_handler(func=lambda m: m.text and "play" in m.text.lower())
def play(m):
    global waiting
    user = m.chat.id
    if user in pairs:
        bot.send_message(user, "انت بتكلم حد حاليا")
        return
    if waiting is None or waiting == user:
        waiting = user
        bot.send_message(user, "⏳ بدورلك على حد...")
    else:
        partner = waiting
        waiting = None
        pairs[user] = partner
        pairs[partner] = user
        bot.send_message(user, "🎉 لقيتلك حد! ابدأ كلام", reply_markup=main_keyboard())
        bot.send_message(partner, "🎉 لقيتلك حد! ابدأ كلام", reply_markup=main_keyboard())

@bot.message_handler(commands=['stop'])
@bot.message_handler(func=lambda m: m.text and "stop" in m.text.lower())
def stop(m):
    user = m.chat.id
    if user in pairs:
        partner = pairs[user]
        del pairs[user]
        del pairs[partner]
        bot.send_message(user, "✅ وقفت", reply_markup=main_keyboard())
        bot.send_message(partner, "🚫 الطرف التاني خرج، دوس play", reply_markup=main_keyboard())
    else:
        bot.send_message(user, "انت مش في محادثة", reply_markup=main_keyboard())

@bot.message_handler(func=lambda m: True)
def chat(m):
    user = m.chat.id
    if user in pairs:
        bot.send_message(pairs[user], m.text)
    else:
        bot.send_message(user, "دوس /play الاول", reply_markup=main_keyboard())

def run_bot():
    bot.infinity_polling()

Thread(target=run_bot).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
