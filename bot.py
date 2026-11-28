import os, json, random, time, threading, requests
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from flask import Flask

TOKEN = os.environ.get("BOT_TOKEN", "PUT_YOUR_TOKEN_HERE")
OWNER_ID = 8188263997
DATA_FILE = "data.json"

# ===== خدمة العملاء - Mr cat بس =====
SUPPORT_IDS = [8188263997, 7125945857]
SUPPORT_INFO = {7125945857: {"name": "Mr cat", "username": "@cat_max_10", "phone": "+20 115 5973454"}}

def load():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f: return json.load(f)
    except: return {"users": {}, "tickets": {}, "ticket_counter": 100, "states": {}}
def save():
    with open(DATA_FILE, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=2)
data = load(); users = data["users"]; tickets = data["tickets"]; states = data["states"]

def get_user(uid, username=""):
    uid = str(uid)
    if uid not in users:
        users[uid] = {"id": uid, "username": username, "balance": 1000, "bank": 0, "savings": 0,
        "loan": 0, "loan_left": 0, "loan_installments": 0, "loan_total": 0, "loan_pay": 0,
        "credit_card": None, "credit_limit": 0, "credit_used": 0,
        "certificates": [], "deposits": [], "vip": False, "banned": False,
        "daily_last": "", "transactions": [], "joint": None, "joint_balance": 0, "checks": [],
        "coins": 0, "level": 1, "xp": 0, "bills": {"electric": 0, "water": 0, "internet": 0}}
        save()
    return users[uid]

def add_tx(uid, text):
    u = get_user(uid); u["transactions"].insert(0, f"{datetime.now().strftime('%d/%m %H:%M')} - {text}"); u["transactions"] = u["transactions"][:30]; save()

def add_xp(uid, amount):
    u = get_user(uid); u["xp"] += amount
    if u["xp"] >= u["level"]*100: u["level"] += 1; u["xp"] = 0

# ===== يصحي نفسه =====
app_flask = Flask(__name__)
@app_flask.route('/')
def home(): return "TRAN BANK PRO ALIVE ✅"
@app_flask.route('/health')
def health(): return "OK"
def run_flask():
    try: app_flask.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
    except: time.sleep(5); run_flask()
def self_ping():
    time.sleep(10); url = os.environ.get("RENDER_EXTERNAL_URL", "")
    if not url: return
    while True:
        try: requests.get(url, timeout=10); print(f"PING OK {datetime.now()}")
        except: pass
        time.sleep(300)
threading.Thread(target=run_flask, daemon=True).start()
threading.Thread(target=self_ping, daemon=True).start()

# ===== كيبورد =====
def main_kb(uid):
    kb = [
        [InlineKeyboardButton("💰 رصيدي", callback_data="balance"), InlineKeyboardButton("💸 تحويل", callback_data="transfer")],
        [InlineKeyboardButton("🏦 ايداع بنك", callback_data="deposit"), InlineKeyboardButton("🏧 سحب بنك", callback_data="withdraw")],
        [InlineKeyboardButton("🐷 تحويش", callback_data="savings"), InlineKeyboardButton("🐷 اودع تحويش", callback_data="savings_deposit")],
        [InlineKeyboardButton("💳 فيزا", callback_data="visa"), InlineKeyboardButton("💳 اسحب من الفيزا", callback_data="visa_use")],
        [InlineKeyboardButton("💰 قرض", callback_data="loan"), InlineKeyboardButton("💰 سدد قسط", callback_data="loan_pay")],
        [InlineKeyboardButton("📄 شهادة", callback_data="certificates"), InlineKeyboardButton("🏦 وديعة", callback_data="deposit_money")],
        [InlineKeyboardButton("💱 عملات", callback_data="coins"), InlineKeyboardButton("🧾 فواتير", callback_data="bills")],
        [InlineKeyboardButton("🧾 اعمل شيك", callback_data="check_make"), InlineKeyboardButton("👥 حساب مشترك", callback_data="joint")],
        [InlineKeyboardButton("🏧 ATM", callback_data="atm"), InlineKeyboardButton("📜 كشف حساب", callback_data="statement")],
        [InlineKeyboardButton("🎁 هدية يومية", callback_data="daily"), InlineKeyboardButton("🏆 الاغنياء", callback_data="top")],
        [InlineKeyboardButton("🎧 خدمة العملاء", callback_data="support")],
    ]
    if str(uid) == str(OWNER_ID): kb.append([InlineKeyboardButton("👑 الاونر", callback_data="owner")])
    return InlineKeyboardMarkup(kb)

def support_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👤 Mr cat - خدمة عملاء", url="https://t.me/cat_max_10")],
        [InlineKeyboardButton("📩 اعمل تيكت جديد", callback_data="new_ticket")],
        [InlineKeyboardButton("📋 تيكتاتي", callback_data="my_tickets")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="back")],
    ])
def support_panel_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📋 التيكتات المفتوحة", callback_data="support_open")],
        [InlineKeyboardButton("📊 احصائيات", callback_data="support_stats")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="back")],
    ])

# ===== START =====
async def start(update, context):
    u = update.effective_user; user = get_user(u.id, u.username or "")
    if user["banned"]: await update.message.reply_text("🚫 انت محظور"); return
    txt = f"""🏦 **TRAN BANK PRO** 👑
اهلا {u.first_name} 💙

💰 كاش: {user['balance']:,} ج
🏦 بنك: {user['bank']:,} ج
🐷 تحويش: {user['savings']:,} ج
💳 فيزا: {user['credit_card'] or 'مفيش'}
💰 قرض: {user['loan_left']:,} ج
🪙 كوينز: {user['coins']}
🏆 ليفل: {user['level']} | XP: {user['xp']}
🎫 ID: `{u.id}`
{'👑 VIP' if user['vip'] else ''}

اختار 👇"""
    await update.message.reply_text(txt, reply_markup=main_kb(u.id), parse_mode="Markdown")

# ===== اوامر بنك =====
async def cmd_balance(update, context):
    user = get_user(update.effective_user.id)
    await update.message.reply_text(f"💰 كاش: {user['balance']:,} ج\n🏦 بنك: {user['bank']:,} ج\n🐷 تحويش: {user['savings']:,} ج\n💳 كريديت: {user['credit_used']:,} / {user['credit_limit']:,}\n💰 قرض متبقي: {user['loan_left']:,}\n🪙 كوينز: {user['coins']}")
async def cmd_deposit(update, context):
    if not context.args: await update.message.reply_text("اكتب: `/deposit 1000`", parse_mode="Markdown"); return
    try: amt = int(context.args[0])
    except: await update.message.reply_text("رقم صح"); return
    user = get_user(update.effective_user.id)
    if user["balance"] < amt: await update.message.reply_text("فلوسك مش كفاية"); return
    user["balance"] -= amt; user["bank"] += amt; add_tx(update.effective_user.id, f"ايداع بنك {amt}"); add_xp(update.effective_user.id, 5); save(); await update.message.reply_text(f"✅ اودعت {amt:,} ج")
async def cmd_withdraw(update, context):
    if not context.args: await update.message.reply_text("اكتب: `/withdraw 1000`", parse_mode="Markdown"); return
    try: amt = int(context.args[0])
    except: await update.message.reply_text("رقم صح"); return
    user = get_user(update.effective_user.id)
    if user["bank"] < amt: await update.message.reply_text("فلوس البنك مش كفاية"); return
    user["bank"] -= amt; user["balance"] += amt; add_tx(update.effective_user.id, f"سحب بنك {amt}"); save(); await update.message.reply_text(f"✅ سحبت {amt:,} ج")
async def cmd_transfer(update, context):
    if len(context.args) < 2: await update.message.reply_text("اكتب: `/transfer ID المبلغ`", parse_mode="Markdown"); return
    try: tid = context.args[0]; amt = int(context.args[1])
    except: await update.message.reply_text("اكتب صح"); return
    user = get_user(update.effective_user.id)
    if user["balance"] < amt: await update.message.reply_text("فلوسك مش كفاية"); return
    target = get_user(tid); user["balance"] -= amt; target["balance"] += amt; add_tx(update.effective_user.id, f"حولت {amt} لـ {tid}"); add_tx(tid, f"وصلك {amt} من {update.effective_user.id}"); add_xp(update.effective_user.id, 5); save(); await update.message.reply_text(f"✅ حولت {amt:,} لـ {tid}")
async def cmd_top(update, context):
    s = sorted(users.values(), key=lambda x: x["balance"]+x["bank"]+x["savings"], reverse=True)[:10]
    txt = "🏆 **اغنى 10:**\n\n"
    for i, u in enumerate(s, 1): txt += f"{i}. @{u['username'] or u['id']} - {u['balance']+u['bank']+u['savings']:,} ج\n"
    await update.message.reply_text(txt, parse_mode="Markdown")
async def cmd_daily(update, context):
    user = get_user(update.effective_user.id); today = datetime.now().strftime("%Y-%m-%d")
    if user["daily_last"] == today: await update.message.reply_text("خدت هديتك النهاردة"); return
    r = random.randint(100, 500) * (2 if user["vip"] else 1)
    user["balance"] += r; user["daily_last"] = today; user["coins"] += 1; add_xp(update.effective_user.id, 10); save(); await update.message.reply_text(f"🎁 خدت {r:,} ج + 1 كوين!")
async def cmd_visa(update, context):
    user = get_user(update.effective_user.id)
    if user["credit_card"]: await update.message.reply_text(f"💳 فيزتك: {user['credit_card']}\nالحد: {user['credit_limit']:,}\nالمستخدم: {user['credit_used']:,}"); return
    num = f"4000 {random.randint(1000,9999)} {random.randint(1000,9999)} {random.randint(1000,9999)}"
    user["credit_card"] = num; user["credit_limit"] = 5000 if not user["vip"] else 20000; save(); await update.message.reply_text(f"💳 عملتلك فيزا!\n`{num}`\nالحد: {user['credit_limit']:,}", parse_mode="Markdown")

# ===== اوامر اونر =====
async def cmd_addmoney(update, context):
    if update.effective_user.id != OWNER_ID: return
    if len(context.args) < 2: await update.message.reply_text("`/addmoney ID المبلغ`", parse_mode="Markdown"); return
    try: tid = context.args[0]; amt = int(context.args[1])
    except: return
    u = get_user(tid); u["balance"] += amt; save(); await update.message.reply_text(f"✅ ضفت {amt:,} لـ {tid}")
async def cmd_ban(update, context):
    if update.effective_user.id != OWNER_ID: return
    if not context.args: return
    u = get_user(context.args[0]); u["banned"] = True; save(); await update.message.reply_text(f"🚫 حظرت {context.args[0]}")
async def cmd_unban(update, context):
    if update.effective_user.id != OWNER_ID: return
    if not context.args: return
    u = get_user(context.args[0]); u["banned"] = False; save(); await update.message.reply_text(f"✅ فكيت حظر {context.args[0]}")
async def cmd_vip(update, context):
    if update.effective_user.id != OWNER_ID: return
    if not context.args: return
    u = get_user(context.args[0]); u["vip"] = True; u["credit_limit"] = 20000; save(); await update.message.reply_text(f"👑 اديت VIP لـ {context.args[0]}")

# ===== دعم =====
async def cmd_reply(update, context):
    if update.effective_user.id not in SUPPORT_IDS: await update.message.reply_text("🚫 انت مش خدمة عملاء"); return
    if len(context.args) < 2: await update.message.reply_text("`/reply 101 الرد`", parse_mode="Markdown"); return
    tid = context.args[0]; txt = " ".join(context.args[1:])
    if tid not in tickets: await update.message.reply_text("مفيش تيكت"); return
    tickets[tid]["status"] = "replied"; tickets[tid]["reply"] = txt; save()
    try: await context.bot.send_message(chat_id=int(tickets[tid]["user_id"]), text=f"🎧 **رد خدمة العملاء على تيكت #{tid}:**\n\n{txt}", parse_mode="Markdown")
    except: pass
    await update.message.reply_text(f"✅ رديت على #{tid}")
async def cmd_close(update, context):
    if update.effective_user.id not in SUPPORT_IDS: await update.message.reply_text("🚫 انت مش خدمة عملاء"); return
    if not context.args: return
    tid = context.args[0]
    if tid not in tickets: return
    tickets[tid]["status"] = "closed"; save(); await update.message.reply_text(f"✅ قفلت #{tid}")

# ===== رسايل =====
async def on_msg(update, context):
    uid = str(update.effective_user.id); text = update.message.text
    st = states.get(uid, "")
    if st == "waiting_ticket":
        states.pop(uid); data["ticket_counter"] += 1; tid = str(data["ticket_counter"])
        tickets[tid] = {"id": tid, "user_id": uid, "username": update.effective_user.username or "", "text": text, "status": "open", "created": datetime.now().strftime("%d/%m %H:%M")}; save()
        await update.message.reply_text(f"✅ عملت تيكت #{tid}\nMr cat هيرد عليك قريب")
        for sid in SUPPORT_IDS:
            try: await context.bot.send_message(chat_id=sid, text=f"🎧 **تيكت جديد #{tid}**\nمن: @{update.effective_user.username or uid} - `{uid}`\n\n{text}\n\n`/reply {tid} الرد`", parse_mode="Markdown")
            except: pass
        return
    if st == "transfer_":
        try: tid, amt = text.split(); amt = int(amt); user = get_user(uid)
        except: await update.message.reply_text("اكتب: `ID المبلغ`"); return
        if user["balance"] < amt: await update.message.reply_text("فلوسك مش كفاية"); return
        target = get_user(tid); user["balance"] -= amt; target["balance"] += amt; save(); await update.message.reply_text(f"✅ حولت {amt:,} لـ {tid}")
        states.pop(uid); save(); return
    if st == "deposit_":
        try: amt = int(text); user = get_user(uid)
        except: await update.message.reply_text("رقم صح"); return
        if user["balance"] < amt: await update.message.reply_text("فلوسك مش كفاية"); return
        user["balance"] -= amt; user["bank"] += amt; save(); await update.message.reply_text(f"✅ اودعت {amt:,}")
        states.pop(uid); save(); return
    if st == "withdraw_":
        try: amt = int(text); user = get_user(uid)
        except: await update.message.reply_text("رقم صح"); return
        if user["bank"] < amt: await update.message.reply_text("فلوس البنك مش كفاية"); return
        user["bank"] -= amt; user["balance"] += amt; save(); await update.message.reply_text(f"✅ سحبت {amt:,}")
        states.pop(uid); save(); return
    if st == "savings_deposit_":
        try: amt = int(text); user = get_user(uid)
        except: await update.message.reply_text("رقم صح"); return
        if user["balance"] < amt: await update.message.reply_text("فلوسك مش كفاية"); return
        user["balance"] -= amt; user["savings"] += amt; save(); await update.message.reply_text(f"🐷 حوشت {amt:,} ج - فايدة 10% كل اسبوع")
        states.pop(uid); save(); return
    if st == "loan_":
        try: amt = int(text); user = get_user(uid)
        except: await update.message.reply_text("رقم صح"); return
        if user["loan_left"] > 0: await update.message.reply_text("عليك قرض قديم سده الاول"); return
        if amt > 10000: await update.message.reply_text("اقصى قرض 10,000"); return
        total = int(amt * 1.2); pay = total // 3
        user["loan"] = amt; user["loan_total"] = total; user["loan_left"] = total; user["loan_installments"] = 3; user["loan_pay"] = pay; user["balance"] += amt; save()
        await update.message.reply_text(f"💰 خدت قرض {amt:,} ج\nهتسدد {total:,} على 3 اقساط\nالقسط: {pay:,} ج")
        states.pop(uid); save(); return
    if st == "cert_":
        try: amt = int(text); user = get_user(uid)
        except: await update.message.reply_text("رقم صح"); return
        if user["balance"] < amt: await update.message.reply_text("فلوسك مش كفاية"); return
        user["balance"] -= amt; user["certificates"].append({"amount": amt, "date": datetime.now().strftime("%Y-%m-%d"), "profit": int(amt*0.2)}); save(); await update.message.reply_text(f"📄 عملت شهادة {amt:,} - هتكسب {int(amt*0.2):,} بعد 3 شهور")
        states.pop(uid); save(); return
    if st == "deposit_money_":
        try: amt = int(text); user = get_user(uid)
        except: await update.message.reply_text("رقم صح"); return
        if user["balance"] < amt: await update.message.reply_text("فلوسك مش كفاية"); return
        user["balance"] -= amt; user["deposits"].append({"amount": amt, "date": datetime.now().strftime("%Y-%m-%d")}); save(); await update.message.reply_text(f"🏦 عملت وديعة {amt:,} - فايدة 15% بعد شهر")
        states.pop(uid); save(); return
    if st == "visa_use_":
        try: amt = int(text); user = get_user(uid)
        except: await update.message.reply_text("رقم صح"); return
        if not user["credit_card"]: await update.message.reply_text("اعمل فيزا الاول"); return
        if user["credit_used"] + amt > user["credit_limit"]: await update.message.reply_text("عديت حد الفيزا"); return
        user["credit_used"] += amt; user["balance"] += amt; save(); await update.message.reply_text(f"💳 سحبت {amt:,} من الفيزا")
        states.pop(uid); save(); return
    if st == "check_make_":
        try: parts = text.split(); tid = parts[0]; amt = int(parts[1])
        except: await update.message.reply_text("اكتب: `ID المبلغ`"); return
        user = get_user(uid)
        if user["balance"] < amt: await update.message.reply_text("فلوسك مش كفاية"); return
        user["balance"] -= amt; code = f"CHK{random.randint(10000,99999)}"
        user["checks"].append({"code": code, "to": tid, "amount": amt})
        target = get_user(tid); target["balance"] += amt; save(); await update.message.reply_text(f"🧾 عملت شيك {code} بـ {amt:,} لـ {tid}")
        states.pop(uid); save(); return
    if st == "joint_":
        try: tid = text.strip(); user = get_user(uid); target = get_user(tid)
        except: await update.message.reply_text("اكتب ID صح"); return
        user["joint"] = tid; target["joint"] = uid; save(); await update.message.reply_text(f"👥 عملت حساب مشترك مع {tid}")
        states.pop(uid); save(); return
    await update.message.reply_text("اكتب /start 👑")

# ===== زرار =====
async def buttons(update, context):
    q = update.callback_query; await q.answer(); uid = str(q.from_user.id); user = get_user(uid, q.from_user.username or ""); d = q.data
    if d == "back": await q.edit_message_text(f"🏦 **TRAN BANK PRO**\n💰 كاش: {user['balance']:,} ج\n🏦 بنك: {user['bank']:,} ج", reply_markup=main_kb(uid), parse_mode="Markdown"); return
    if d == "balance": await q.edit_message_text(f"💰 كاش: {user['balance']:,} ج\n🏦 بنك: {user['bank']:,} ج\n🐷 تحويش: {user['savings']:,} ج\n💳 كريديت: {user['credit_used']:,} / {user['credit_limit']:,}\n💰 قرض: {user['loan_left']:,}\n🪙 كوينز: {user['coins']}\n🎫 ID: `{uid}`", reply_markup=main_kb(uid), parse_mode="Markdown"); return
    if d == "transfer": states[uid] = "transfer_"; save(); await q.edit_message_text("💸 ابعت: `ID المبلغ`", parse_mode="Markdown"); return
    if d == "deposit": states[uid] = "deposit_"; save(); await q.edit_message_text("🏦 اكتب المبلغ اللي هتودعه في البنك:"); return
    if d == "withdraw": states[uid] = "withdraw_"; save(); await q.edit_message_text("🏧 اكتب المبلغ اللي هتسحبه من البنك:"); return
    if d == "savings": await q.edit_message_text(f"🐷 تحويشك: {user['savings']:,} ج\nفايدة 10% كل اسبوع\nدوس اودع تحويش عشان تحوش", reply_markup=main_kb(uid)); return
    if d == "savings_deposit": states[uid] = "savings_deposit_"; save(); await q.edit_message_text("🐷 اكتب المبلغ اللي هتحوشه:"); return
    if d == "visa":
        if not user["credit_card"]:
            num = f"4000 {random.randint(1000,9999)} {random.randint(1000,9999)} {random.randint(1000,9999)}"; user["credit_card"] = num; user["credit_limit"] = 20000 if user["vip"] else 5000; save(); await q.edit_message_text(f"💳 فيزتك: `{num}`\nالحد: {user['credit_limit']:,}", reply_markup=main_kb(uid), parse_mode="Markdown")
        else: await q.edit_message_text(f"💳 فيزتك: {user['credit_card']}\nالحد: {user['credit_limit']:,}\nالمستخدم: {user['credit_used']:,}", reply_markup=main_kb(uid)); return
    if d == "visa_use": states[uid] = "visa_use_"; save(); await q.edit_message_text("💳 اكتب المبلغ اللي هتسحبه من الفيزا:"); return
    if d == "loan":
        if user["loan_left"] > 0: await q.edit_message_text(f"💰 عليك قرض: {user['loan_left']:,} ج\nالقسط: {user['loan_pay']:,} ج\nفاضل: {user['loan_installments']} اقساط", reply_markup=main_kb(uid))
        else: states[uid] = "loan_"; save(); await q.edit_message_text("💰 اكتب مبلغ القرض (اقصى 10,000):\nهتسدده على 3 اقساط بفايدة 20%"); return
    if d == "loan_pay":
        if user["loan_left"] <= 0: await q.edit_message_text("مفيش قرض عليك ✅", reply_markup=main_kb(uid)); return
        if user["balance"] < user["loan_pay"]: await q.edit_message_text("فلوسك مش كفاية للقسط", reply_markup=main_kb(uid)); return
        user["balance"] -= user["loan_pay"]; user["loan_left"] -= user["loan_pay"]; user["loan_installments"] -= 1
        if user["loan_left"] <= 0: user["loan_left"] = 0; user["loan"] = 0; user["loan_installments"] = 0
        save(); await q.edit_message_text(f"✅ سددت قسط {user['loan_pay']:,} ج\nالمتبقي: {user['loan_left']:,} ج", reply_markup=main_kb(uid)); return
    if d == "certificates":
        txt = "📄 **شهاداتك:**\n\n"
        for c in user["certificates"]: txt += f"- {c['amount']:,} ج - ربح {c['profit']:,} - {c['date']}\n"
        if not user["certificates"]: txt += "مفيش شهادات"
        await q.edit_message_text(txt + "\n\nعايز تعمل شهادة؟ اكتب المبلغ:", reply_markup=main_kb(uid)); states[uid] = "cert_"; save(); return
    if d == "deposit_money":
        txt = "🏦 **ودايعك:**\n\n"
        for dep in user["deposits"]: txt += f"- {dep['amount']:,} ج - {dep['date']}\n"
        if not user["deposits"]: txt += "مفيش ودايع"
        await q.edit_message_text(txt + "\n\nاكتب مبلغ الوديعة:", reply_markup=main_kb(uid)); states[uid] = "deposit_money_"; save(); return
    if d == "coins":
        if user["coins"] > 0:
            gain = user["coins"] * 100; user["balance"] += gain; user["coins"] = 0; save(); await q.edit_message_text(f"💱 حولت كوينز لـ {gain:,} ج!", reply_markup=main_kb(uid))
        else: await q.edit_message_text(f"💱 معاك {user['coins']} كوين\n1 كوين = 100 ج\nخد هدية يومية عشان تجمع كوينز", reply_markup=main_kb(uid)); return
    if d == "bills":
        b = user["bills"]; total = b["electric"] + b["water"] + b["internet"]
        if total == 0:
            b["electric"] = random.randint(50, 200); b["water"] = random.randint(30, 100); b["internet"] = random.randint(100, 300); save(); total = b["electric"] + b["water"] + b["internet"]
        await q.edit_message_text(f"🧾 **فواتيرك:**\n⚡ كهربا: {b['electric']:,} ج\n💧 مياه: {b['water']:,} ج\n🌐 نت: {b['internet']:,} ج\n\nالاجمالي: {total:,} ج\n\nدوس دفع لو عايز تدفع", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💳 ادفع الفواتير", callback_data="bills_pay")],[InlineKeyboardButton("🔙 رجوع", callback_data="back")]])); return
    if d == "bills_pay":
        b = user["bills"]; total = b["electric"] + b["water"] + b["internet"]
        if user["balance"] < total: await q.edit_message_text("فلوسك مش كفاية", reply_markup=main_kb(uid)); return
        user["balance"] -= total; user["bills"] = {"electric": 0, "water": 0, "internet": 0}; save(); await q.edit_message_text(f"✅ دفعت فواتير {total:,} ج", reply_markup=main_kb(uid)); return
    if d == "check_make": states[uid] = "check_make_"; save(); await q.edit_message_text("🧾 اكتب: `ID المبلغ` عشان تعمل شيك:"); return
    if d == "joint":
        if user["joint"]: await q.edit_message_text(f"👥 حسابك المشترك مع: {user['joint']}", reply_markup=main_kb(uid))
        else: states[uid] = "joint_"; save(); await q.edit_message_text("👥 اكتب ID صاحبك عشان تعمل حساب مشترك:"); return
    if d == "atm": await q.edit_message_text("🏧 **ATM**\nاسحب واودع بسرعة من زرار سحب / ايداع", reply_markup=main_kb(uid)); return
    if d == "statement":
        tx = "\n".join(user["transactions"][:15]) or "مفيش معاملات"; await q.edit_message_text(f"📜 **كشف حساب:**\n\n{tx}", reply_markup=main_kb(uid), parse_mode="Markdown"); return
    if d == "daily":
        today = datetime.now().strftime("%Y-%m-%d")
        if user["daily_last"] == today: await q.edit_message_text("🎁 خدت هديتك النهاردة", reply_markup=main_kb(uid)); return
        r = random.randint(100, 500) * (2 if user["vip"] else 1); user["balance"] += r; user["daily_last"] = today; user["coins"] += 1; add_xp(uid, 10); save(); await q.edit_message_text(f"🎁 خدت {r:,} ج + 1 كوين!", reply_markup=main_kb(uid)); return
    if d == "top":
        s = sorted(users.values(), key=lambda x: x["balance"]+x["bank"]+x["savings"], reverse=True)[:10]; txt = "🏆 **اغنى 10:**\n\n"
        for i, u in enumerate(s, 1): txt += f"{i}. @{u['username'] or u['id']} - {u['balance']+u['bank']+u['savings']:,} ج\n"
        await q.edit_message_text(txt, reply_markup=main_kb(uid), parse_mode="Markdown"); return
    if d == "support":
        if int(uid) in SUPPORT_IDS:
            open_t = len([t for t in tickets.values() if t["status"] == "open"]); await q.edit_message_text(f"🎧 **لوحة خدمة العملاء**\n\n👤 انت: {SUPPORT_INFO.get(int(uid), {}).get('name', 'اونر')}\n📩 مفتوحة: {open_t}\n📊 اجمالي: {len(tickets)}", reply_markup=support_panel_kb(), parse_mode="Markdown")
        else: await q.edit_message_text("🎧 **خدمة العملاء**\n\n👤 **Mr cat**\nيوزر: @cat_max_10\nجوال: +20 115 5973454", reply_markup=support_menu(), parse_mode="Markdown"); return
    if d == "new_ticket": states[uid] = "waiting_ticket"; save(); await q.edit_message_text("📩 اكتب شكوتك بالتفصيل:"); return
    if d == "my_tickets":
        my = [t for t in tickets.values() if t["user_id"] == uid]
        if not my: await q.edit_message_text("مفيش تيكتات", reply_markup=support_menu()); return
        txt = "📋 **تيكتاتك:**\n\n"
        for t in my[-5:]: txt += f"#{t['id']} - {t['status']} - {t['text'][:30]}\n"
        await q.edit_message_text(txt, reply_markup=support_menu(), parse_mode="Markdown"); return
    if d == "support_open":
        if int(uid) not in SUPPORT_IDS: return
        open_t = [t for t in tickets.values() if t["status"] == "open"]
        if not open_t: await q.edit_message_text("مفيش تيكتات مفتوحة ✅", reply_markup=support_panel_kb()); return
        txt = "📋 **تيكتات مفتوحة:**\n\n"
        for t in open_t[-10:]: txt += f"#{t['id']} - @{t['username']} - {t['text'][:40]}\n`/reply {t['id']} الرد`\n\n"
        await q.edit_message_text(txt, reply_markup=support_panel_kb(), parse_mode="Markdown"); return
    if d == "support_stats":
        if int(uid) not in SUPPORT_IDS: return
        open_t = len([t for t in tickets.values() if t["status"] == "open"]); closed_t = len([t for t in tickets.values() if t["status"] == "closed"])
        await q.edit_message_text(f"📊 **احصائيات:**\n\n👥 يوزرز: {len(users)}\n📩 مفتوحة: {open_t}\n✅ مقفولة: {closed_t}\n📊 اجمالي: {len(tickets)}", reply_markup=support_panel_kb(), parse_mode="Markdown"); return
    if d == "owner":
        if str(uid) != str(OWNER_ID): return
        await q.edit_message_text("👑 **لوحة الاونر**\n\n`/addmoney ID المبلغ`\n`/ban ID`\n`/unban ID`\n`/vip ID`\n`/reply 101 الرد`\n`/close 101`", reply_markup=main_kb(uid), parse_mode="Markdown"); return

def main():
    while True:
        try:
            app = ApplicationBuilder().token(TOKEN).build()
            app.add_handler(CommandHandler("start", start)); app.add_handler(CommandHandler("balance", cmd_balance)); app.add_handler(CommandHandler("deposit", cmd_deposit)); app.add_handler(CommandHandler("withdraw", cmd_withdraw)); app.add_handler(CommandHandler("transfer", cmd_transfer)); app.add_handler(CommandHandler("top", cmd_top)); app.add_handler(CommandHandler("daily", cmd_daily)); app.add_handler(CommandHandler("visa", cmd_visa)); app.add_handler(CommandHandler("addmoney", cmd_addmoney)); app.add_handler(CommandHandler("ban", cmd_ban)); app.add_handler(CommandHandler("unban", cmd_unban)); app.add_handler(CommandHandler("vip", cmd_vip)); app.add_handler(CommandHandler("reply", cmd_reply)); app.add_handler(CommandHandler("close", cmd_close))
            app.add_handler(CallbackQueryHandler(buttons)); app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_msg))
            print("TRAN BANK PRO FULL STARTED ✅"); app.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)
        except Exception as e: print(f"CRASH RESTART: {e}"); time.sleep(5)
if __name__ == "__main__": main()
