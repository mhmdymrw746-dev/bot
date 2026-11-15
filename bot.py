import telebot, time
BOT_TOKEN = "9005250007:AAEumlmOgX2uQKyfTGdJrG6Nvq3RU657b4Q"
ADMIN_ID = 8188263997
bot = telebot.TeleBot(BOT_TOKEN)
users = {}
@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "البوت شغال 24 ساعة 🔥")
@bot.message_handler(func=lambda m: m.from_user.id != ADMIN_ID, content_types=['text','photo','video','voice','document','sticker'])
def to_owner(m):
    fwd = bot.forward_message(ADMIN_ID, m.chat.id, m.message_id)
    users[fwd.message_id] = m.chat.id
    bot.reply_to(m, "✅ وصلت للمالك")
@bot.message_handler(func=lambda m: m.from_user.id == ADMIN_ID, content_types=['text','photo','video','voice','document','sticker'])
def from_owner(m):
    if m.reply_to_message and m.reply_to_message.message_id in users:
        bot.copy_message(users[m.reply_to_message.message_id], m.chat.id, m.message_id)
print("BOT ON")
while True:
    try:
        bot.infinity_polling()
    except:
        time.sleep(5)
