# ===== BOT TRAN - تيليجرام - الاونر @TRAN_5 👑 =====
import os, random, time, threading, requests
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

TOKEN = os.environ.get("BOT_TOKEN", "حط_توكن_البوت_هنا")
OWNER_ID = 8188263997
OWNER_USER = "@TRAN_5"

# الدعم
SUPPORT = {
    "@cat_max_10": {"name": "Mr cat", "shift": "صبح", "online": True, "solved": 0},
    "@MOON_104": {"name": "تيتو", "shift": "ليل", "online": True, "solved": 0},
}
SUPPORT_IDS = []  # هنحط ايديهاتهم بعدين

# الداتا
users = {}
tickets = {}
ticket_count = 0
logs = []

def get_user(uid, name="بطل"):
    if uid not in users:
        users[uid] = {"name": name, "money": 1000, "bank": 0, "level": 1, "xp": 0, "job": "عاطل", "married": None, "family": None, "car": None, "house": None, "plane": False, "debt": 0, "banned": False, "last_daily": 0}
    return users[uid]

def fmt(n): return f"{int(n):,}"

def main_kb(is_owner=False):
    kb = [
        [InlineKeyboardButton("💰 فلوسي", callback_data="money"), InlineKeyboardButton("🎰 كازينو", callback_data="casino")],
        [InlineKeyboardButton("🥷 سرقة", callback_data="steal"), InlineKeyboardButton("💼 شغل", callback_data="work")],
        [InlineKeyboardButton("🏦 بنك", callback_data="bank"), InlineKeyboardButton("💸 تحويل", callback_data="transfer")],
        [InlineKeyboardButton("🚗 عربيتي", callback_data="car"), InlineKeyboardButton("🏠 عقارات", callback_data="house")],
        [InlineKeyboardButton("🏆 التوب", callback_data="top"), InlineKeyboardButton("🎁 هدية يومية", callback_data="daily")],
        [InlineKeyboardButton("🆘 دعم البوت", callback_data="support")],
    ]
    if is_owner:
        kb.append([InlineKeyboardButton("👑 لوحة الاونر", callback_data="owner")])
    kb.append([InlineKeyboardButton("👥 فريق الدعم", callback_data="team")])
    return InlineKeyboardMarkup(kb)

# ===== سيرفر ريندر - عشان البوت مينامش =====
app = Flask(__name__)
@app.route("/")
def home(): return "البوت شغال يا اونر 👑🟢 - TRAN BOT - تيليجرام"
@app.route("/ping")
def ping(): return "pong - انا صاحي 😎"
@app.route("/health")
def health(): return {"status": "online", "users": len(users), "tickets": ticket_count}

def keep_alive():
    url = os.environ.get("RENDER_EXTERNAL_URL", "")
    if not url:
        # لو مش متظبط، جرب اللينك بتاعك
        url = "https://bot-tran.onrender.com"
    while True:
        try:
            requests.get(f"{url}/ping", timeout=10)
            print("صحيت نفسي ✅")
        except Exception as e:
            print(f"نمت شوية: {e}")
        time.sleep(240) # كل 4 دقايق

threading.Thread(target=keep_alive, daemon=True).start()

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# ===== أوامر البوت =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    name = update.effective_user.first_name
    u = get_user(uid, name)
    is_owner = (uid == OWNER_ID)
    await update.message.reply_text(
        f"🏦 *بنك TRAN* 👑\nأهلا يا {name} يا بطل، اختار:",
        reply_markup=main_kb(is_owner), parse_mode="Markdown"
    )

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    name = q.from_user.first_name
    u = get_user(uid, name)
    data = q.data
    is_owner = (uid == OWNER_ID)

    if data == "money":
        await q.edit_message_text(f"💰 *فلوسك يا {name}*\nكاش: {fmt(u['money'])}\nبنك: {fmt(u['bank'])}\nمستوى: {u['level']} | XP: {u['xp']}\nشغل: {u['job']}", parse_mode="Markdown", reply_markup=main_kb(is_owner))
    elif data == "casino":
        if u["money"] < 100:
            await q.edit_message_text("ممعكش فلوس للكازينو 😭", reply_markup=main_kb(is_owner)); return
        if random.random() < 0.45:
            u["money"] += 500; txt = "كسبت 500 في الكازينو 🎰🔥"
        else:
            u["money"] -= 200; txt = "خسرت 200 🎰😭"
        await q.edit_message_text(txt, reply_markup=main_kb(is_owner))
    elif data == "steal":
        if random.random() < 0.5:
            win = random.randint(200, 1200); u["money"] += win; logs.append(f"{name} سرق {win}")
            txt = f"سرقت {fmt(win)} 🥷🔥"
        else:
            u["money"] = max(0, u["money"]-300); txt = "اتمسكت! اتخصم منك 300 😂🚨"
        await q.edit_message_text(txt, reply_markup=main_kb(is_owner))
    elif data == "work":
        jobs = [("دليفري", 300), ("مبرمج", 800), ("حرامي", 1000), ("تاجر", 600)]
        j, amt = random.choice(jobs); u["money"] += amt; u["xp"] += 10
        if u["xp"] >= 100: u["level"] += 1; u["xp"] = 0
        await q.edit_message_text(f"اشتغلت {j} وكسبت {fmt(amt)} 💼", reply_markup=main_kb(is_owner))
    elif data == "bank":
        await q.edit_message_text("🏦 *البنك*\n/ايداع 1000\n/سحب 500\n/قرض 5000\n/سدد\n/فلوسي", parse_mode="Markdown", reply_markup=main_kb(is_owner))
    elif data == "transfer":
        await q.edit_message_text("اكتب: /تحويل 500 @حد", reply_markup=main_kb(is_owner))
    elif data == "car":
        await q.edit_message_text(f"عربيتك: {u['car'] or 'معندكش'} 🚗\nاشتري بـ /اشتري عربية 15000", reply_markup=main_kb(is_owner))
    elif data == "house":
        await q.edit_message_text("🏠 عقارات:\n/اشتري شقة 20000\n/اشتري طيارة 100000", reply_markup=main_kb(is_owner))
    elif data == "top":
        top = sorted(users.values(), key=lambda x: x["money"]+x["bank"], reverse=True)[:5]
        t = "🏆 *التوب 5* 👑\n"
        for i, x in enumerate(top): t += f"{i+1}. {x['name']} - {fmt(x['money']+x['bank'])}\n"
        await q.edit_message_text(t, parse_mode="Markdown", reply_markup=main_kb(is_owner))
    elif data == "daily":
        now = time.time()
        if now - u["last_daily"] < 86400:
            await q.edit_message_text("خدت اليومية خلاص 😂", reply_markup=main_kb(is_owner)); return
        u["last_daily"] = now; u["money"] += 1000
        await q.edit_message_text("خدت 1000 يومية 🎁💰", reply_markup=main_kb(is_owner))
    elif data == "support":
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🐛 البوت مش شغال", callback_data="sup_bug")],
            [InlineKeyboardButton("💰 فلوسي راحت", callback_data="sup_money")],
            [InlineKeyboardButton("🥷 حد سرقني", callback_data="sup_steal")],
            [InlineKeyboardButton("💡 عندي فكرة", callback_data="sup_idea")],
            [InlineKeyboardButton("🔙 رجوع", callback_data="back")],
        ])
        await q.edit_message_text("🆘 *دعم البوت*\nعندك مشكلة؟ اختار:", parse_mode="Markdown", reply_markup=kb)
    elif data.startswith("sup_"):
        global ticket_count
        ticket_count += 1; tid = ticket_count
        probs = {"sup_bug": "البوت مش شغال", "sup_money": "فلوسي راحت", "sup_steal": "حد سرقني", "sup_idea": "عندي فكرة"}
        prob = probs.get(data, "مشكلة عامة")
        tickets[tid] = {"user": uid, "name": name, "problem": prob, "status": "مفتوحة", "support": None}
        # اشعار للاونر والدعم
        notif = f"🔔 *حد عايز دعم!*\n👤 {name}\n🎫 تذكرة #{tid}\n📝 {prob}\nمين هيقبل؟"
        kb2 = InlineKeyboardMarkup([[InlineKeyboardButton("✅ انا هكلمه", callback_data=f"accept_{tid}")]])
        # ابعت للاونر
        try:
            await context.bot.send_message(chat_id=OWNER_ID, text=notif, reply_markup=kb2, parse_mode="Markdown")
        except: pass
        # ابعت للدعم - حط ايديهاتهم هنا
        for sid in SUPPORT_IDS:
            try: await context.bot.send_message(chat_id=sid, text=notif, reply_markup=kb2, parse_mode="Markdown")
            except: pass
        await q.edit_message_text(f"تم يا بطل ❤️✅\nرقم تذكرتك: #{tid}\nبعتنا للدعم، واللي فاضي هيقبل ويكلمك\n@TRAN_5 @cat_max_10 @MOON_104", reply_markup=main_kb(is_owner))
    elif data.startswith("accept_"):
        tid = int(data.split("_")[1]); tk = tickets.get(tid)
        if not tk:
            await q.edit_message_text("مفيش تذكرة بالرقم ده"); return
        if tk["support"]:
            await q.edit_message_text(f"خلاص {tk['support']} قبلها"); return
        tk["support"] = name; tk["status"] = "مقبولة"
        await q.edit_message_text(f"✅ انت قبلت تذكرة #{tid}\nكلم {tk['name']} دلوقتي ❤️\nاوامر: /تعويض {tid} 1000 - /قفل {tid} - /انقل {tid}")
        try: await context.bot.send_message(chat_id=tk["user"], text=f"الدعم {name} قبل طلبك وهيكلمك دلوقتي ❤️")
        except: pass
    elif data == "owner" and is_owner:
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("💰 ادي للكل 1000", callback_data="owner_give")],
            [InlineKeyboardButton("📊 احصائيات", callback_data="owner_stats")],
            [InlineKeyboardButton("📩 التذاكر", callback_data="owner_tickets")],
            [InlineKeyboardButton("👥 فريق الدعم", callback_data="team")],
            [InlineKeyboardButton("🔙 رجوع", callback_data="back")],
        ])
        await q.edit_message_text("👑 *لوحة الاونر @TRAN_5*", parse_mode="Markdown", reply_markup=kb)
    elif data == "owner_give" and is_owner:
        for x in users.values(): x["money"] += 1000
        await q.edit_message_text("ديت للكل 1000 🎁👑", reply_markup=main_kb(True))
    elif data == "owner_stats" and is_owner:
        total = sum(x["money"]+x["bank"] for x in users.values())
        await q.edit_message_text(f"📊 *احصائيات*\nعدد الناس: {len(users)}\nفلوس البنك: {fmt(total)}\nتذاكر: {ticket_count}", parse_mode="Markdown", reply_markup=main_kb(True))
    elif data == "owner_tickets" and is_owner:
        open_t = [(k, v) for k, v in tickets.items() if v["status"] == "مفتوحة"]
        if not open_t: await q.edit_message_text("مفيش تذاكر ✅", reply_markup=main_kb(True)); return
        t = "📩 *التذاكر:*\n"
        for k, v in open_t: t += f"#{k} - {v['name']}: {v['problem']}\n"
        await q.edit_message_text(t, parse_mode="Markdown", reply_markup=main_kb(True))
    elif data == "team":
        t = "👥 *فريق الدعم:*\n👑 @TRAN_5 - الاونر الكبير\n🟢 @cat_max_10 - Mr cat - شيفت صبح\n🌙 @MOON_104 - تيتو - شيفت ليل\n\nأي حد عايز دعم، يجيلهم اشعار واللي فاضي يقبل ويكلمه ⚡"
        await q.edit_message_text(t, reply_markup=main_kb(is_owner))
    elif data == "back":
        await q.edit_message_text("🏦 *بنك TRAN* 👑\nاختار:", reply_markup=main_kb(is_owner))

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message: return
    uid = update.effective_user.id; name = update.effective_user.first_name; text = update.message.text.strip(); low = text.lower()
    u = get_user(uid, name); owner = (uid == OWNER_ID)
    if low.startswith("/مشكلة"):
        global ticket_count
        ticket_count += 1; tid = ticket_count
        prob = text.replace("/مشكلة", "").strip() or "مشكلة عامة"
        tickets[tid] = {"user": uid, "name": name, "problem": prob, "status": "مفتوحة", "support": None}
        kb2 = InlineKeyboardMarkup([[InlineKeyboardButton("✅ انا هكلمه", callback_data=f"accept_{tid}")]])
        notif = f"🔔 *حد عايز دعم!*\n👤 {name}\n🎫 تذكرة #{tid}\n📝 {prob}"
        try: await context.bot.send_message(chat_id=OWNER_ID, text=notif, reply_markup=kb2, parse_mode="Markdown")
        except: pass
        await update.message.reply_text(f"تم يا بطل ❤️✅ رقم تذكرتك #{tid}")
        return
    if low.startswith("/اقبل"):
        try: tid = int(text.split()[1])
        except: await update.message.reply_text("اكتب /اقبل رقم"); return
        tk = tickets.get(tid)
        if tk and not tk["support"]:
            tk["support"] = name; tk["status"] = "مقبولة"
            await update.message.reply_text(f"✅ قبلت #{tid}، كلم {tk['name']}")
        return
    if low.startswith("/قفل"):
        try: tid = int(text.split()[1])
        except: return
        if tid in tickets: tickets[tid]["status"] = "مقفولة"; await update.message.reply_text(f"قفلت #{tid} ✅")
        return
    if low.startswith("/تعويض"):
        try: _, tid, amt = text.split(); tid=int(tid); amt=int(amt)
        except: return
        tk = tickets.get(tid)
        if tk: get_user(tk["user"])["money"] += amt; await update.message.reply_text(f"ديت {tk['name']} {fmt(amt)} ✅")
        return
    if low.startswith("/ايداع"):
        try: a = int(text.split()[1])
        except: return
        if u["money"] < a: await update.message.reply_text("ممعكش 😭"); return
        u["money"] -= a; u["bank"] += a; await update.message.reply_text(f"حطيت {fmt(a)} في البنك ✅"); return
    if low.startswith("/سحب"):
        try: a = int(text.split()[1])
        except: return
        if u["bank"] < a: await update.message.reply_text("البنك مفهوش 😭"); return
        u["bank"] -= a; u["money"] += a; await update.message.reply_text(f"سحبت {fmt(a)} ✅"); return
    if low == "/فلوسي":
        await update.message.reply_text(f"💰 فلوسك يا {name}\nكاش: {fmt(u['money'])}\nبنك: {fmt(u['bank'])}"); return
    if low == "/صحيني" and owner:
        await update.message.reply_text("انا صاحي يا اونر 👑😎"); return
    if low == "/حالة":
        await update.message.reply_text("شغال 100% يا اونر، نمت 0 دقيقة 🟢👑"); return

# ===== تشغيل =====
def main():
    threading.Thread(target=run_flask, daemon=True).start()
    app_tg = ApplicationBuilder().token(TOKEN).build()
    app_tg.add_handler(CommandHandler("start", start))
    app_tg.add_handler(CallbackQueryHandler(handle_button))
    app_tg.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    # اوامر نصية زي /مشكلة /اقبل /قفل /تعويض /ايداع /سحب /فلوسي
    app_tg.add_handler(MessageHandler(filters.COMMAND, handle_text))
    print("البوت صاحي 👑🔥")
    app_tg.run_polling()

if __name__ == "__main__":
    main()
