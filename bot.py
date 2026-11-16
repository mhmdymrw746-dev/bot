import os
import csv
from datetime import datetime
from flask import Flask
from threading import Thread
import telebot
from telebot import types

TOKEN = os.environ.get("TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "8188263997"))

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
CSV_FILE = "messages.csv"

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        csv.writer(f).writerow(["Date", "Time", "User ID", "Username", "Name", "Message"])

def save_message(user_id, username, name, text):
    now = datetime.now()
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        csv.writer(f).writerow([now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"), user_id, username, name, text])

def admin_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📊 تحميل الشيت", callback_data="download"),
        types.InlineKeyboardButton("📈 عدد الرسايل", callback_data="count"),
        types.InlineKeyboardButton("🗑️ مسح الشيت", callback_data="clear"),
        types.InlineKeyboardButton("ℹ️ المساعدة", callback_data="help")
    )
    return markup

def user_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📩 ابعت رسالة", "ℹ️ عن البوت")
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, f"اهلا يا مطور 👑\nID: {ADMIN_ID}\nاختار من الأزرار:", reply_markup=admin_keyboard())
    else:
        bot.send_message(message.chat.id, "اهلا بيك! 👋\nابعت رسالتك وهتوصل للمطور فورا", reply_markup=user_keyboard())

@bot.callback_query_handler(func=lambda call: True)
def handle_buttons(call):
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "مش ليك يا غالي 😅")
        return

    if call.data == "download":
        if os.path.exists(CSV_FILE):
            bot.send_document(call.message.chat.id, open(CSV_FILE, 'rb'), caption="📊 ملف كل الرسايل")
        else:
            bot.send_message(call.message.chat.id, "مفيش رسايل لسه")
    
    elif call.data == "count":
        try:
            with open(CSV_FILE, 'r', encoding='utf-8') as f:
                count = len(list(csv.reader(f))) - 1
            bot.send_message(call.message.chat.id, f"📈 إجمالي الرسايل: {count} رسالة")
        except:
            bot.send_message(call.message.chat.id, "0 رسالة")
    
    elif call.data == "clear":
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("✅ ايوه امسح", callback_data="confirm_clear"),
            types.InlineKeyboardButton("❌ لا", callback_data="cancel")
        )
        bot.send_message(call.message.chat.id, "متأكد عايز تمسح كل الرسايل؟", reply_markup=markup)
    
    elif call.data == "confirm_clear":
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            csv.writer(f).writerow(["Date", "Time", "User ID", "Username", "Name", "Message"])
        bot.send_message(call.message.chat.id, "✅ تم مسح الشيت")
    
    elif call.data == "cancel":
        bot.send_message(call.message.chat.id, "تمام، ممسحناش حاجة", reply_markup=admin_keyboard())
    
    elif call.data == "help":
        bot.send_message(call.message.chat.id, "الأوامر:\n/start - الأزرار\n/sheet - تحميل الشيت", reply_markup=admin_keyboard())

@bot.message_handler(func=lambda m: True)
def handle_all(message):
    if message.text == "📊 تحميل الشيت" or message.text == "📩 ابعت رسالة" or message.text == "ℹ️ عن البوت":
        return

    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, "لوحة التحكم:", reply_markup=admin_keyboard())
        return

    user = message.from_user
    username = f"@{user.username}" if user.username else "بدون يوزر"
    name = f"{user.first_name or ''} {user.last_name or ''}".strip()
    text = message.text or message.caption or "ملف/صورة"

    save_message(user.id, username, name, text)
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    bot.reply_to(message, "✅ رسالتك اتبعتت واتسجلت!")

app = Flask(__name__)
@app.route('/')
def home(): return "Bot with Buttons - OK"
def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
Thread(target=run_flask, daemon=True).start()
bot.infinity_polling()
