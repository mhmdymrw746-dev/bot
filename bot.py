from flask import Flask
from threading import Thread
import telebot
import os
import requests

TOKEN = os.environ.get("9005250007:AAEumlmOgX2uQKyfTGdJrG6Nvq3RU657b4Q")
bot = telebot.TeleBot(
    9005250007:AAEumlmOgX2uQKyfTGdJrG6Nvq3RU657b4Q)
app = Flask(__name__)

@app.route('/')
def home():
    return "AI Bot is Live!"

def ask_ai(text):
    try:
        url = f"https://text.pollinations.ai/{text}"
        r = requests.get(url, timeout=20)
        return r.text
    except Exception as e:
        return "حصل مشكلة ثواني وجرب تاني 😅"

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "اهلا 🤖 انا بوت ذكاء اصطناعي\nاسألني اي حاجة وهرد عليك فورا!")

@bot.message_handler(func=lambda m: True)
def chat(m):
    bot.send_chat_action(m.chat.id, 'typing')
    answer = ask_ai(m.text)
    bot.send_message(m.chat.id, answer)

def run_bot():
    bot.infinity_polling()

Thread(target=run_bot).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
