
import os
from flask import Flask
from threading import Thread
import telebot

TOKEN = os.environ.get("TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "8188263997"))

if not TOKEN:
    raise ValueError("TOKEN not set in Environment Variables!")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hello! Send me any message and it will reach the developer.")

@bot.message_handler(func=lambda m: True)
def handle_all(message):
    if message.from_user.id == ADMIN_ID:
        return
    try:
        bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
        bot.reply_to(message, "Your message has been sent to the developer!")
    except Exception as e:
        print(f"Error: {e}")

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running - OK"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    Thread(target=run_flask, daemon=True).start()
    print("Bot started...")
    bot.infinity_polling()
