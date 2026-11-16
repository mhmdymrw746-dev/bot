‏from flask import Flask
‏from threading import Thread
‏import telebot, os
‏
‏TOKEN = os.environ.get("9005250007:AAFtDZv0cowJcovzdh9vmxmUT2h4JGONlk4")
‏bot = telebot.TeleBot(9005250007:AAFtDZv0cowJcovzdh9vmxmUT2h4JGONlk4)
‏app = Flask(__name__)
‏
‏@app.route('/')
‏def home():
‏    return "Bot is Live"
‏
‏@bot.message_handler(commands=['start'])
‏def start(m):
‏    bot.reply_to(m, "اهلا انا شغال 🤖")
‏
‏@bot.message_handler(func=lambda m: True)
‏def all_msg(m):
‏    bot.reply_to(m, "وصلت المطور عدي")
‏
‏def run():
‏    bot.infinity_polling()
‏
‏Thread(target=run).start()
‏
‏if __name__ == "__main__":
‏    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
