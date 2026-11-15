from flask import Flask
from threading import Thread
import telebot
import os

TOKEN = os.environ.get("9005250007:AAEumlmOgX2uQKyfTGdJrG6Nvq3RU657b4Q")
bot = telebot.TeleBot(9005250007:AAEumlmOgX2uQKyfTGdJrG6Nvq3RU657b4Q)
app = Flask(__name__)

waiting = None
pairs = {}

@app.route('/')
def home():
    return "Bot is Live!"

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "اهلا بيك 😎\nارسل رسالتك وصاحب البوت هيرد عليك\nدوس /play عشان تكلم حد عشوائي")

@bot.message_handler(commands=['play'])
def play(m):
    global waiting
    user = m.chat.id
    if user in pairs:
        return
    if waiting is None or waiting == user:
        waiting = user
        bot.send_message(user, "بدورلك على حد...")
    else:
        partner = waiting
        waiting = None
        pairs[user] = partner
        pairs[partner] = user
        bot.send_message(user, "لقيتلك حد! ابدأ كلام")
        bot.send_message(partner, "لقيتلك حد! ابدأ كلام")

@bot.message_handler(commands=['stop'])
def stop(m):
    user = m.chat.id
    if user in pairs:
        partner = pairs[user]
        del pairs[user]
        del pairs[partner]
        bot.send_message(user, "وقفت")
        bot.send_message(partner, "الطرف التاني خرج")

@bot.message_handler(func=lambda m: True)
def chat(m):
    user = m.chat.id
    if user in pairs:
        bot.send_message(pairs[user], m.text)

def run_bot():
    bot.infinity_polling()

Thread(target=run_bot).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
