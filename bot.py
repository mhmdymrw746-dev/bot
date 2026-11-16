import os
from flask import Flask
from threading import Thread
import telebot
from telebot import types
from datetime import datetime, timedelta
from collections import defaultdict

TOKEN = os.environ.get("TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "8188263997"))

if not TOKEN:
    print("TOKEN مش موجود")
    exit()

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

warnings = {}
points = defaultdict(int)
locks = {"links": True}
flood = defaultdict(list)

def is_admin(chat_id, user_id):
    try:
        s = bot.get_chat_member(chat_id, user_id).status
        return s in ['administrator','creator']
    except:
        return False

def main_kb():
    m = types.InlineKeyboardMarkup(row_width=2)
    m.add(
        types.InlineKeyboardButton("🔒 قفل الشات", callback_data="lock"),
        types.InlineKeyboardButton("🔓 فتح الشات", callback_data="unlock"),
        types.InlineKeyboardButton("🔗 روابط ON/OFF", callback_data="t_links"),
        types.InlineKeyboardButton("🏆 التوب", callback_data="top"),
        types.InlineKeyboardButton("⚠️ التحذيرات", callback_data="warns"),
        types.InlineKeyboardButton("📜 القوانين", callback_data="rules")
    )
    return m

def user_kb(uid):
    m = types.InlineKeyboardMarkup(row_width=3)
    m.add(
        types.InlineKeyboardButton("🚫 بان", callback_data=f"ban_{uid}"),
        types.InlineKeyboardButton("👢 كيك", callback_data=f"kick_{uid}"),
        types.InlineKeyboardButton("🔇 كتم", callback_data=f"mute_{uid}"),
        types.InlineKeyboardButton("⚠️ تحذير", callback_data=f"warn_{uid}"),
        types.InlineKeyboardButton("✅ فك كتم", callback_data=f"unmute_{uid}")
    )
    return m

@bot.message_handler(content_types=['new_chat_members'])
def welcome(message):
    for u in message.new_chat_members:
        bot.send_message(message.chat.id, f"اهلا {u.first_name} نورت 🔥", reply_markup=user_kb(u.id))

@bot.message_handler(commands=['start','panel','admin','لوحة'])
def panel(message):
    reply_kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    reply_kb.add(
        types.KeyboardButton("👑 لوحة التحكم"),
        types.KeyboardButton("📜 القوانين"),
        types.KeyboardButton("🔒 قفل الشات"),
        types.KeyboardButton("🔓 فتح الشات")
    )
    bot.send_message(message.chat.id, "👑 دوس على الزرار 👇", reply_markup=reply_kb)
    bot.send_message(message.chat.id, "لوحة التحكم:", reply_markup=main_kb())

@bot.message_handler(func=lambda m: m.text in ["👑 لوحة التحكم","📜 القوانين","🔒 قفل الشات","🔓 فتح الشات"])
def reply_btns(message):
    if message.text == "👑 لوحة التحكم":
        bot.send_message(message.chat.id, "لوحة التحكم:", reply_markup=main_kb())
    elif message.text == "📜 القوانين":
        bot.send_message(message.chat.id, "📜 القوانين:\n1- احترم الكل\n2- ممنوع الروابط\n3- ممنوع السب")
    elif message.text == "🔒 قفل الشات":
        try:
            bot.set_chat_permissions(message.chat.id, can_send_messages=False)
            bot.send_message(message.chat.id, "🔒 تم القفل")
        except:
            bot.reply_to(message, "خليني ادمن")
    elif message.text == "🔓 فتح الشات":
        try:
            bot.set_chat_permissions(message.chat.id, can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True)
            bot.send_message(message.chat.id, "🔓 تم الفتح")
        except:
            pass

@bot.message_handler(func=lambda m: True)
def filters(message):
    if message.chat.type == 'private':
        return
    if is_admin(message.chat.id, message.from_user.id):
        points[message.from_user.id] += 1
        return

    text = (message.text or "").lower()
    uid = message.from_user.id

    if locks["links"] and ("http" in text or "t.me" in text or "www." in text):
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, f"🚫 ممنوع الروابط يا {message.from_user.first_name}")
            return
        except:
            pass

    now = __import__('time').time()
    flood[uid] = [t for t in flood[uid] if now - t < 5]
    flood[uid].append(now)
    if len(flood[uid]) > 4:
        try:
            bot.restrict_chat_member(message.chat.id, uid, until_date=datetime.now()+timedelta(minutes=10), can_send_messages=False)
            bot.send_message(message.chat.id, f"🔇 {message.from_user.first_name} اتكتم 10د سبام")
            flood[uid] = []
        except:
            pass

    points[uid] += 1

@bot.callback_query_handler(func=lambda c: True)
def callbacks(call):
    d = call.data
    chat_id = call.message.chat.id

    if d == "lock":
        try:
            bot.set_chat_permissions(chat_id, can_send_messages=False)
            bot.answer_callback_query(call.id, "تم القفل 🔒")
        except:
            bot.answer_callback_query(call.id, "خليني ادمن")
    elif d == "unlock":
        try:
            bot.set_chat_permissions(chat_id, can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True)
            bot.answer_callback_query(call.id, "تم الفتح 🔓")
        except:
            pass
    elif d == "t_links":
        locks["links"] = not locks["links"]
        bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=main_kb())
        bot.answer_callback_query(call.id, f"روابط {'ON' if locks['links'] else 'OFF'}")
    elif d == "top":
        top = sorted(points.items(), key=lambda x: x[1], reverse=True)[:5]
        txt = "🏆 التوب:\n"
        for uid, pts in top:
            try:
                name = bot.get_chat_member(chat_id, uid).user.first_name
            except:
                name = str(uid)
            txt += f"{name}: {pts}\n"
        bot.send_message(chat_id, txt)
    elif d == "warns":
        if not warnings:
            bot.send_message(chat_id, "مفيش تحذيرات")
        else:
            bot.send_message(chat_id, "\n".join([f"ID {k}: {v}/3" for k,v in warnings.items()]))
    elif d == "rules":
        bot.send_message(chat_id, "📜 القوانين:\n1- احترم الكل\n2- ممنوع الروابط\n3- ممنوع السب")
    elif d.startswith("ban_"):
        uid = int(d.split("_")[1])
        bot.ban_chat_member(chat_id, uid)
        bot.answer_callback_query(call.id, "تم البان")
    elif d.startswith("kick_"):
        uid = int(d.split("_")[1])
        bot.ban_chat_member(chat_id, uid)
        bot.unban_chat_member(chat_id, uid)
        bot.answer_callback_query(call.id, "تم الطرد")
    elif d.startswith("mute_"):
        uid = int(d.split("_")[1])
        bot.restrict_chat_member(chat_id, uid, until_date=datetime.now()+timedelta(hours=1), can_send_messages=False)
        bot.answer_callback_query(call.id, "كتم ساعة")
    elif d.startswith("unmute_"):
        uid = int(d.split("_")[1])
        bot.restrict_chat_member(chat_id, uid, can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True)
        bot.answer_callback_query(call.id, "فك كتم")
    elif d.startswith("warn_"):
        uid = int(d.split("_")[1])
        warnings[uid] = warnings.get(uid, 0) + 1
        if warnings[uid] >= 3:
            bot.ban_chat_member(chat_id, uid)
            bot.send_message(chat_id, f"🚫 ID {uid} اتحظر 3 تحذيرات")
            warnings[uid] = 0
        bot.answer_callback_query(call.id, f"تحذير {warnings[uid]}/3")

@app.route('/')
def home():
    return "Bot is Live"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

Thread(target=run, daemon=True).start()
bot.infinity_polling()
