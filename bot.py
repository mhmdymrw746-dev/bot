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
