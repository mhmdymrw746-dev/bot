
import os, time, random
from flask import Flask
from threading import Thread
import telebot
from telebot import types
from datetime import datetime, timedelta
from collections import defaultdict

TOKEN = os.environ.get("TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "8188263997"))
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

warnings, points, pending_captcha = {}, defaultdict(int), {}
locks = {"links": True, "bots": True, "stickers": False, "photo": False, "video": False}
rules = "1- احترم الكل\n2- ممنوع الروابط\n3- ممنوع السب"
auto_replies = {"سلام": "وعليكم السلام ورحمة الله ❤️", "هلا": "هلا والله نورت 🔥", "صباح الخير": "صباح العسل ☀️"}
flood = defaultdict(list)

def is_admin(c, u):
    try: return bot.get_chat_member(c, u).status in ['administrator','creator']
    except: return False

def panel():
    m = types.InlineKeyboardMarkup(row_width=2)
    m.add(
        types.InlineKeyboardButton("🔒 قفل الكل", callback_data="lock_all"),
        types.InlineKeyboardButton("🔓 فتح الكل", callback_data="unlock_all"),
        types.InlineKeyboardButton(f"🔗 روابط {'✅' if locks['links'] else '❌'}", callback_data="t_links"),
        types.InlineKeyboardButton(f"🤖 بوتات {'✅' if locks['bots'] else '❌'}", callback_data="t_bots"),
        types.InlineKeyboardButton(f"🖼️ صور {'✅' if not locks['photo'] else '❌'}", callback_data="t_photo"),
        types.InlineKeyboardButton(f"🎥 فيديو {'✅' if not locks['video'] else '❌'}", callback_data="t_video"),
        types.InlineKeyboardButton(f"😜 ملصقات {'✅' if not locks['stickers'] else '❌'}", callback_data="t_stickers"),
        types.InlineKeyboardButton("🎯 كابتشا ON/OFF", callback_data="t_captcha"),
        types.InlineKeyboardButton("🏆 التوب", callback_data="top"),
        types.InlineKeyboardButton("⚠️ التحذيرات", callback_data="warns"),
        types.InlineKeyboardButton("👢 طرد الخاملين", callback_data="kick_inactive"),
        types.InlineKeyboardButton("📜 القوانين", callback_data="show_rules"),
        types.InlineKeyboardButton("🔄 تثبيت القوانين", callback_data="pin_rules")
    )
    return m

def user_btn(uid):
    m = types.InlineKeyboardMarkup(row_width=3)
    m.add(
        types.InlineKeyboardButton("🚫 بان", callback_data=f"ban_{uid}"),
        types.InlineKeyboardButton("👢 كيك", callback_data=f"kick_{uid}"),
        types.InlineKeyboardButton("🔇 كتم", callback_data=f"mute_{uid}"),
        types.InlineKeyboardButton("⚠️ تحذير", callback_data=f"warn_{uid}"),
        types.InlineKeyboardButton("➕ 10 نقط", callback_data=f"addp_{uid}"),
        types.InlineKeyboardButton("🏆 نقاطه", callback_data=f"points_{uid}")
    )
    return m

# ===== NEW MEMBERS + CAPTCHA =====
@bot.message_handler(content_types=['new_chat_members'])
def new_member(message):
    for u in message.new_chat_members:
        if locks["bots"] and u.is_bot:
            try: bot.ban_chat_member(message.chat.id, u.id); continue
            except: pass
        
        # Delete join message
        try: bot.delete_message(message.chat.id, message.message_id)
        except: pass

        # Captcha
        code = random.randint(1000,9999)
        pending_captcha[u.id] = code
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(f"اضغط هنا {code} ✅", callback_data=f"captcha_{u.id}_{code}"))
        markup.add(types.InlineKeyboardButton("انا مش بوت 🤖", callback_data=f"captcha_{u.id}_{code}"))
        
        sent = bot.send_message(message.chat.id, f"👋 اهلا {u.first_name}\n\n⚠️ لازم تثبت انك مش بوت في 60 ثانية وتدوس الزرار\nوإلا هتتطرد تلقائي\n\nالقوانين: /rules", reply_markup=markup)
        
        # Auto kick after 60s if not verified
        def check_captcha():
            time.sleep(60)
            if u.id in pending_captcha:
                try:
                    bot.ban_chat_member(message.chat.id, u.id)
                    bot.unban_chat_member(message.chat.id, u.id)
                    bot.send_message(message.chat.id, f"👢 {u.first_name} اتطرد - مأكدش الكابتشا")
                    del pending_captcha[u.id]
                except: pass
        Thread(target=check_captcha, daemon=True).start()

@bot.message_handler(content_types=['left_chat_member'])
def left_member(message):
    try: bot.delete_message(message.chat.id, message.message_id)
    except: pass

# ===== MAIN FILTER =====
@bot.message_handler(func=lambda m: True, content_types=['text','photo','video','sticker','document','audio','voice'])
def all_filter(message):
    if message.chat.type == 'private': return
    if is_admin(message.chat.id, message.from_user.id): 
        points[message.from_user.id] += 1
        return
    
    uid = message.from_user.id
    # Check captcha
    if uid in pending_captcha:
        try: bot.delete_message(message.chat.id, message.message_id); return
        except: pass

    # Locks
    if locks["photo"] and message.content_type == 'photo':
        try: bot.delete_message(message.chat.id, message.message_id); return
        except: pass
    if locks["video"] and message.content_type == 'video':
        try: bot.delete_message(message.chat.id, message.message_id); return
        except: pass
    if locks["stickers"] and message.content_type == 'sticker':
        try: bot.delete_message(message.chat.id, message.message_id); return
        except: pass

    text = (message.text or "").lower()

    if locks["links"] and ("http" in text or "t.me" in text or "www." in text):
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, f"🚫 ممنوع الروابط يا {message.from_user.first_name}")
            return
        except: pass

    # Anti flood
    now = time.time()
    flood[uid] = [t for t in flood[uid] if now - t < 5]
    flood[uid].append(now)
    if len(flood[uid]) > 4:
        try:
            bot.restrict_chat_member(message.chat.id, uid, until_date=datetime.now()+timedelta(minutes=15), can_send_messages=False)
            bot.send_message(message.chat.id, f"🔇 {message.from_user.first_name} اتكتم 15د سبام")
            flood[uid]=[]
            return
        except: pass

    # Auto replies
    for k,v in auto_replies.items():
        if k in text:
            bot.reply_to(message, v)
            break

    points[uid] += 1

@bot.message_handler(commands=['start','admin','panel','لوحة'])
def panel_cmd(message):
    if message.chat.type != 'private' and not is_admin(message.chat.id, message.from_user.id): return
    bot.send_message(message.chat.id, f"👑 لوحة التحكم الخارقة\n\n📊 النقاط: {sum(points.values())} رسالة\n⚠️ التحذيرات: {len(warnings)}", reply_markup=panel())

@bot.message_handler(commands=['rules','قوانين'])
def show_rules(message):
    bot.send_message(message.chat.id, f"📜 قوانين {message.chat.title}:\n\n{rules}\n\nللإدارة: /panel")

@bot.callback_query_handler(func=lambda c: True)
def cbs(call):
    d = call.data
    chat_id = call.message.chat.id
    is_adm = is_admin(chat_id, call.from_user.id) or call.from_user.id == ADMIN_ID

    # Captcha check (anyone can click his own)
    if d.startswith("captcha_"):
        _, uid, code = d.split("_")
        uid = int(uid)
        if call.from_user.id != uid and not is_adm:
            bot.answer_callback_query(call.id, "ده مش ليك!")
            return
        if uid in pending_captcha:
            del pending_captcha[uid]
            bot.edit_message_text(f"✅ {call.from_user.first_name} تم التأكيد - نورت الجروب 🔥", chat_id, call.message.message_id)
            bot.answer_callback_query(call.id, "تم ✅")
        return

    if not is_adm:
        bot.answer_callback_query(call.id, "للمشرفين فقط")
        return

    if d.startswith("ban_"):
        uid=int(d.split("_")[1])
        bot.ban_chat_member(chat_id, uid)
        bot.answer_callback_query(call.id, "تم البان")
    elif d.startswith("kick_"):
        uid=int(d.split("_")[1])
        bot.ban_chat_member(chat_id, uid); bot.unban_chat_member(chat_id, uid)
        bot.answer_callback_query(call.id, "تم الطرد")
    elif d.startswith("mute_"):
        uid=int(d.split("_")[1])
        bot.restrict_chat_member(chat_id, uid, until_date=datetime.now()+timedelta(hours=1), can_send_messages=False)
        bot.answer_callback_query(call.id, "كتم ساعة")
    elif d.startswith("warn_"):
        uid=int(d.split("_")[1])
        warnings[uid]=warnings.get(uid,0)+1
        if warnings[uid]>=3:
            bot.ban_chat_member(chat_id, uid); warnings[uid]=0
            bot.send_message(chat_id, f"🚫 ID {uid} اتحظر 3 تحذيرات")
        bot.answer_callback_query(call.id, f"تحذير {warnings[uid]}/3")
    elif d.startswith("points_") or d.startswith("addp_"):
        uid=int(d.split("_")[1])
        if d.startswith("addp_"): points[uid]+=10
        bot.answer_callback_query(call.id, f"نقاطه: {points.get(uid,0)}")
    elif d=="t_links": locks["links"]=not locks["links"]
    elif d=="t_bots": locks["bots"]=not locks["bots"]
    elif d=="t_photo": locks["photo"]=not locks["photo"]
    elif d=="t_video": locks["video"]=not locks["video"]
    elif d=="t_stickers": locks["stickers"]=not locks["stickers"]
    elif d.startswith("t_"):
        bot.answer_callback_query(call.id, "تم التغيير")
    
    if d.startswith("t_"):
        try: bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=panel())
        except: pass
        return

    if d=="lock_all":
        try: bot.set_chat_permissions(chat_id, can_send_messages=False); bot.answer_callback_query(call.id, "تم القفل 🔒")
        except: bot.answer_callback_query(call.id, "لازم اكون ادمن")
    elif d=="unlock_all":
        try: bot.set_chat_permissions(chat_id, can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True); bot.answer_callback_query(call.id, "تم الفتح 🔓")
        except: pass
    elif d=="top":
        top = sorted(points.items(), key=lambda x: x[1], reverse=True)[:5]
        txt="🏆 اكتر ناس بتتكلم:\n"
        for uid, pts in top:
            try: name = bot.get_chat_member(chat_id, uid).user.first_name
            except: name = f"ID {uid}"
            txt+=f"{name}: {pts} نقطة\n"
        bot.send_message(chat_id, txt)
    elif d=="warns":
        if not warnings: bot.send_message(chat_id, "مفيش تحذيرات")
        else: bot.send_message(chat_id, "\n".join([f"ID {k}: {v}/3" for k,v in warnings.items()]))
    elif d=="show_rules":
        bot.send_message(chat_id, f"📜 القوانين:\n{rules}")
    elif d=="pin_rules":
        m=bot.send_message(chat_id, f"📌 القوانين المثبتة:\n{rules}")
        try: bot.pin_chat_message(chat_id, m.message_id)
        except: pass

@app.route('/')
def home(): return "Super Bot v10 - OK"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
Thread(target=run, daemon=True).start()
bot.infinity_polling()
