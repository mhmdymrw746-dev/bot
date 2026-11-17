import os
import telebot
from telebot import types

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# الناس اللي مستنية شريك
waiting = []
# الناس اللي متوصلين ببعض: {id1: id2, id2: id1}
pairs = {}

def main_keyboard():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("🔍 دورلي على شريك", callback_data="search"))
    kb.add(types.InlineKeyboardButton("⏹️ وقف المحادثة", callback_data="stop"))
    kb.add(types.InlineKeyboardButton("👤 بروفايلي", callback_data="profile"))
    return kb

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
        "اهلا بيك في بوت دورلي على شريك ❤️\nدوس على الزرار وهنوصلك بحد تتكلم معاه",
        reply_markup=main_keyboard())

@bot.callback_query_handler(func=lambda c: True)
def buttons(call):
    uid = call.message.chat.id

    if call.data == "search":
        if uid in pairs:
            bot.answer_callback_query(call.id, "انت متوصل مع حد اصلا!")
            return
        if uid in waiting:
            bot.answer_callback_query(call.id, "انت مستني اصلا...")
            return
        if waiting:
            partner = waiting.pop(0)
            pairs[uid] = partner
            pairs[partner] = uid
            bot.send_message(uid, "✅ لقينالك شريك! ابعت رسالتك دلوقتي", reply_markup=main_keyboard())
            bot.send_message(partner, "✅ لقينالك شريك! ابعت رسالتك دلوقتي", reply_markup=main_keyboard())
        else:
            waiting.append(uid)
            bot.send_message(uid, "⏳ مستنيين حد يدور زيك... اول ما يجي هنوصلكم", reply_markup=main_keyboard())

    elif call.data == "stop":
        if uid in pairs:
            partner = pairs.pop(uid)
            pairs.pop(partner, None)
            bot.send_message(uid, "تم فصل المحادثة ❌", reply_markup=main_keyboard())
            bot.send_message(partner, "الشريك فصل المحادثة ❌", reply_markup=main_keyboard())
        elif uid in waiting:
            waiting.remove(uid)
            bot.send_message(uid, "تم ايقاف البحث", reply_markup=main_keyboard())
        else:
            bot.answer_callback_query(call.id, "انت مش في محادثة اصلا")

    elif call.data == "profile":
        bot.send_message(uid, f"الايدي بتاعك: {uid}\nالحالة: {'في محادثة' if uid in pairs else 'مش في محادثة'}", reply_markup=main_keyboard())

@bot.message_handler(content_types=['text', 'photo', 'voice', 'video', 'sticker'])
def forward_msg(message):
    uid = message.chat.id
    if uid in pairs:
        partner = pairs[uid]
        try:
            bot.copy_message(partner, uid, message.message_id)
        except:
            bot.send_message(uid, "الشريك قفل البوت")
    else:
        bot.send_message(uid, "دوس الاول على 🔍 دورلي على شريك", reply_markup=main_keyboard())

print("Bot is running...")
bot.infinity_polling()
