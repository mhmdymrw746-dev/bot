import os, json, random, time, threading, requests, traceback
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from flask import Flask

TOKEN = os.environ.get("BOT_TOKEN", "").strip()
OWNER_ID = 8188263997
DATA_FILE = "data.json"

# ===== بيانات Mr cat =====
SUPPORT_IDS = [8188263997, 7125945857]
MR_CAT_ID = 7125945857
MR_CAT_USERNAME = "cat_max_10"
MR_CAT_PHONE = "+201155973454"
MR_CAT_WHATSAPP = "201155973454"

print(f"TOKEN EXISTS: {bool(TOKEN)} - LEN: {len(TOKEN)}")

def load():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            d = json.load(f)
            d.setdefault("tickets", {}); d.setdefault("ticket_counter", 100)
            d.setdefault("states", {}); d.setdefault("ratings", [])
            d.setdefault("live_chats", {}); d.setdefault("queue", [])
            d.setdefault("callbacks", []); d.setdefault("users", {})
            d.setdefault("operator_status", "online"); d.setdefault("operator_msg", "")
            d.setdefault("temp", {})
            return d
    except Exception as e:
        print(f"LOAD ERROR: {e}")
        return {"users": {}, "tickets": {}, "ticket_counter": 100, "states": {}, "ratings": [], "live_chats": {}, "queue": [], "callbacks": [], "operator_status": "online", "operator_msg": "", "temp": {}}

def save():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"SAVE ERROR: {e}")

data = load()
users = data["users"]; tickets = data["tickets"]; states = data["states"]; live_chats = data["live_chats"]

def get_user(uid, username=""):
    uid = str(uid)
    if uid not in users:
        users[uid] = {"id": uid, "username": username, "balance": 1000, "bank": 0, "savings": 0, "loan_left": 0, "loan_pay": 0, "loan_installments": 0, "credit_card": None, "credit_limit": 0, "credit_used": 0, "vip": False, "banned": False, "daily_last": "", "transactions": [], "coins": 0, "level": 1, "xp": 0, "certificates": [], "deposits": [], "bills": {"electric": 0, "water": 0, "internet": 0}}
        save()
    return users[uid]

# ===== سيرفر يخلي البوت صاحي =====
app_flask = Flask(__name__)
@app_flask.route('/')
def home(): return "BOT ALIVE ✅ - " + datetime.now().strftime("%H:%M:%S")
@app_flask.route('/health')
def health(): return "OK"
@app_flask.route('/ping')
def ping(): return "PONG"
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    print(f"FLASK ON PORT {port}")
    try:
        app_flask.run(host="0.0.0.0", port=port, threaded=True)
    except Exception as e:
        print(f"FLASK ERROR: {e}"); time.sleep(3); run_flask()

def self_ping():
    time.sleep(15)
    url = os.environ.get("RENDER_EXTERNAL_URL", "")
    if not url:
        print("NO RENDER URL - SKIP PING")
        return
    while True:
        try:
            r = requests.get(url, timeout=10)
            print(f"PING OK {r.status_code} {datetime.now().strftime('%H:%M:%S')}")
        except Exception as e:
            print(f"PING FAIL: {e}")
        time.sleep(240)

threading.Thread(target=run_flask, daemon=True).start()
threading.Thread(target=self_ping, daemon=True).start()

def status_emoji():
    s = data.get("operator_status", "online")
    if s == "online": return "🟢 اونلاين - بيرد حالا"
    if s == "busy": return "🟡 مشغول - هتستنى شوية"
    return "🔴 اوفلاين - سيب رسالة"

def main_kb(uid):
    kb = [
        [InlineKeyboardButton("💬 شات مباشر 🔴", callback_data="live_start"), InlineKeyboardButton("📞 اطلب مكالمة", callback_data="request_call")],
        [InlineKeyboardButton("💰 بنك | رصيدي", callback_data="bank"), InlineKeyboardButton("🎧 خدمة العملاء", callback_data="support")],
        [InlineKeyboardButton("💚 واتساب Mr cat", url=f"https://wa.me/{MR_CAT_WHATSAPP}"), InlineKeyboardButton("✈️ تليجرام Mr cat", url=f"https://t.me/{MR_CAT_USERNAME}")],
        [InlineKeyboardButton("📩 تيكت جديد", callback_data="new_ticket"), InlineKeyboardButton("📋 تيكتاتي", callback_data="my_tickets")],
        [InlineKeyboardButton("🎁 هدية يومية", callback_data="daily"), InlineKeyboardButton("🏆 الاغنياء", callback_data="top")],
        [InlineKeyboardButton("❓ اسئلة شائعة", callback_data="faq"), InlineKeyboardButton("⭐ قيمنا", callback_data="rate")],
    ]
    if int(uid) in SUPPORT_IDS:
        kb.append([InlineKeyboardButton("🎧 لوحة الدعم", callback_data="support_panel")])
    if str(uid) == str(OWNER_ID):
        kb.append([InlineKeyboardButton("👑 الاونر", callback_data="owner")])
    return InlineKeyboardMarkup(kb)

def bank_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 رصيدي", callback_data="balance"), InlineKeyboardButton("💸 تحويل", callback_data="transfer")],
        [InlineKeyboardButton("🏦 ايداع", callback_data="deposit"), InlineKeyboardButton("🏧 سحب", callback_data="withdraw")],
        [InlineKeyboardButton("🐷 تحويش", callback_data="savings"), InlineKeyboardButton("💳 فيزا", callback_data="visa")],
        [InlineKeyboardButton("💰 قرض", callback_data="loan"), InlineKeyboardButton("💰 سدد قسط", callback_data="loan_pay")],
        [InlineKeyboardButton("📄 شهادة", callback_data="cert"), InlineKeyboardButton("🏦 وديعة", callback_data="dep_money")],
        [InlineKeyboardButton("🧾 فواتير", callback_data="bills"), InlineKeyboardButton("📜 كشف حساب", callback_data="statement")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="back")],
    ])

def support_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💬 شاتات مباشرة", callback_data="live_active")],
        [InlineKeyboardButton("⏳ طابور", callback_data="queue_list")],
        [InlineKeyboardButton("📞 طلبات مكالمات", callback_data="callback_list")],
        [InlineKeyboardButton("📩 تيكتات مفتوحة", callback_data="support_open")],
        [InlineKeyboardButton("📊 احصائيات", callback_data="support_stats")],
        [InlineKeyboardButton("🟢/🟡/🔴 غير حالتي", callback_data="change_status")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="back")],
    ])

# ===== START =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        u = update.effective_user
        user = get_user(u.id, u.username or "")
        if user["banned"]:
            await update.message.reply_text("🚫 انت محظور من البوت"); return
        txt = f"""🏦🎧 **TRAN - بنك + خدمة عملاء** 👑
اهلا {u.first_name} 💙

💰 كاش: {user['balance']:,} ج | 🏦 بنك: {user['bank']:,} ج
🐷 تحويش: {user['savings']:,} ج | 🪙 كوينز: {user['coins']}

👤 **Mr cat** - {status_emoji()}
📞 {MR_CAT_PHONE} | @{MR_CAT_USERNAME}

🎫 ID: `{u.id}`
اختار 👇"""
        if data.get("operator_msg"):
            txt += f"\n\n📢 {data['operator_msg']}"
        await update.message.reply_text(txt, reply_markup=main_kb(u.id), parse_mode="Markdown")
    except Exception as e:
        print(f"START ERROR: {e}"); traceback.print_exc()

async def cmd_help(update, context):
    await update.message.reply_text("🆘 **مساعدة:**\n\n/start - القايمة\n/balance - رصيدك\n/deposit 1000 - ايداع\n/withdraw 1000 - سحب\n/transfer ID 100 - تحويل\n/daily - هدية\n/top - الاغنياء\n\nMr cat: /reply 101 الرد - /chat ID رسالة - /close 101", parse_mode="Markdown")

# ===== اوامر بنك =====
async def cmd_balance(update, context):
    user = get_user(update.effective_user.id)
    await update.message.reply_text(f"💰 كاش: {user['balance']:,}\n🏦 بنك: {user['bank']:,}\n🐷 تحويش: {user['savings']:,}\n💳 فيزا: {user['credit_used']:,}/{user['credit_limit']:,}\n💰 قرض: {user['loan_left']:,}")
async def cmd_daily(update, context):
    user = get_user(update.effective_user.id); today = datetime.now().strftime("%Y-%m-%d")
    if user["daily_last"] == today: await update.message.reply_text("خدت هديتك النهاردة 🎁"); return
    r = random.randint(100, 500) * (2 if user["vip"] else 1)
    user["balance"] += r; user["daily_last"] = today; user["coins"] += 1; save()
    await update.message.reply_text(f"🎁 خدت {r:,} ج + 1 كوين!")
async def cmd_top(update, context):
    s = sorted(users.values(), key=lambda x: x["balance"]+x["bank"]+x["savings"], reverse=True)[:10]
    txt = "🏆 **اغنى 10:**\n\n"
    for i, u in enumerate(s, 1): txt += f"{i}. @{u['username'] or u['id']} - {u['balance']+u['bank']+u['savings']:,} ج\n"
    await update.message.reply_text(txt, parse_mode="Markdown")

# ===== اوامر دعم =====
async def cmd_reply(update, context):
    if update.effective_user.id not in SUPPORT_IDS: await update.message.reply_text("🚫 مش خدمة عملاء"); return
    if len(context.args) < 2: await update.message.reply_text("اكتب: `/reply 101 الرد`", parse_mode="Markdown"); return
    tid = context.args[0]; txt = " ".join(context.args[1:])
    if tid not in tickets: await update.message.reply_text("مفيش تيكت"); return
    tickets[tid]["status"] = "replied"; tickets[tid]["reply"] = txt; save()
    try: await context.bot.send_message(chat_id=int(tickets[tid]["user_id"]), text=f"🎧 **Mr cat رد عليك:**\n\n{txt}", parse_mode="Markdown")
    except Exception as e: print(f"REPLY SEND FAIL: {e}")
    await update.message.reply_text(f"✅ رديت على #{tid}")
async def cmd_close(update, context):
    if update.effective_user.id not in SUPPORT_IDS: return
    if not context.args: return
    tid = context.args[0]
    if tid not in tickets: await update.message.reply_text("مفيش تيكت"); return
    tickets[tid]["status"] = "closed"; save()
    try: await context.bot.send_message(chat_id=int(tickets[tid]["user_id"]), text=f"✅ تيكت #{tid} اتقفل 💙")
    except: pass
    await update.message.reply_text(f"✅ قفلت #{tid}")
async def cmd_chat(update, context):
    if update.effective_user.id not in SUPPORT_IDS: return
    if len(context.args) < 2: await update.message.reply_text("اكتب: `/chat ID رسالتك`", parse_mode="Markdown"); return
    uid = context.args[0]; txt = " ".join(context.args[1:])
    try:
        await context.bot.send_message(chat_id=int(uid), text=f"💬 **Mr cat:**\n\n{txt}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⏹️ انهاء", callback_data="live_end")]]))
        await update.message.reply_text("✅ بعت")
    except Exception as e: await update.message.reply_text(f"مش عارف ابعت: {e}")
async def cmd_endchat(update, context):
    if update.effective_user.id not in SUPPORT_IDS: return
    if not context.args: return
    uid = context.args[0]
    if uid in live_chats: del live_chats[uid]; save()
    try: await context.bot.send_message(chat_id=int(uid), text="⏹️ Mr cat انهى المحادثة", reply_markup=main_kb(int(uid)))
    except: pass
    await update.message.reply_text("✅ انهيت")
async def cmd_status(update, context):
    if update.effective_user.id not in SUPPORT_IDS: return
    if not context.args: await update.message.reply_text("`/status online` / `busy` / `offline`"); return
    s = context.args[0].lower()
    if s in ["online","busy","offline"]: data["operator_status"] = s; save(); await update.message.reply_text(f"✅ حالتك: {s}")
# اونر
async def cmd_addmoney(update, context):
    if update.effective_user.id != OWNER_ID: return
    if len(context.args) < 2: await update.message.reply_text("`/addmoney ID المبلغ`", parse_mode="Markdown"); return
    try: tid = context.args[0]; amt = int(context.args[1])
    except: await update.message.reply_text("رقم غلط"); return
    u = get_user(tid); u["balance"] += amt; save(); await update.message.reply_text(f"✅ ضفت {amt:,} لـ {tid}")
async def cmd_ban(update, context):
    if update.effective_user.id != OWNER_ID: return
    if not context.args: return
    u = get_user(context.args[0]); u["banned"] = True; save(); await update.message.reply_text(f"🚫 حظرت {context.args[0]}")
async def cmd_unban(update, context):
    if update.effective_user.id != OWNER_ID: return
    if not context.args: return
    u = get_user(context.args[0]); u["banned"] = False; save(); await update.message.reply_text(f"✅ فكيت {context.args[0]}")
async def cmd_vip(update, context):
    if update.effective_user.id != OWNER_ID: return
    if not context.args: return
    u = get_user(context.args[0]); u["vip"] = True; u["credit_limit"] = 20000; save(); await update.message.reply_text(f"👑 VIP لـ {context.args[0]}")

# ===== استقبال الرسايل - متصلح =====
async def on_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update.message: return
        uid = str(update.effective_user.id)
        user = get_user(uid, update.effective_user.username or "")
        if user["banned"]: return
        text = update.message.text or update.message.caption or ""
        if update.message.voice: text = "🎤 رسالة صوتية"
        if update.message.photo and not text: text = "🖼️ صورة"
        if update.message.photo and update.message.caption: text = f"🖼️ {update.message.caption}"
        st = states.get(uid, "")

        # 1 - شات مباشر
        if uid in live_chats and int(uid) not in SUPPORT_IDS:
            for sid in SUPPORT_IDS:
                try:
                    if update.message.photo:
                        await context.bot.send_photo(chat_id=sid, photo=update.message.photo[-1].file_id, caption=f"💬 شات مباشر من @{update.effective_user.username or uid} - `{uid}`\n\n{text}\n\n`/chat {uid} ردك`", parse_mode="Markdown")
                    elif update.message.voice:
                        await context.bot.send_voice(chat_id=sid, voice=update.message.voice.file_id)
                        await context.bot.send_message(chat_id=sid, text=f"🎤 فويس من `{uid}` - `/chat {uid} ردك`", parse_mode="Markdown")
                    else:
                        await context.bot.send_message(chat_id=sid, text=f"💬 **شات مباشر**\nمن: @{update.effective_user.username or uid} - `{uid}`\n\n{text}\n\n`/chat {uid} ردك`", parse_mode="Markdown")
                except Exception as e: print(f"LIVE FORWARD FAIL: {e}")
            await update.message.reply_text("✅ وصلت لـ Mr cat 👀", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⏹️ انهاء", callback_data="live_end")]]))
            return

        # 2 - حالات البنك
        if st == "transfer_":
            states.pop(uid); save()
            try: tid, amt = text.split(); amt = int(amt)
            except: await update.message.reply_text("اكتب صح: `ID المبلغ`", parse_mode="Markdown"); return
            if user["balance"] < amt: await update.message.reply_text("فلوسك مش كفاية"); return
            target = get_user(tid); user["balance"] -= amt; target["balance"] += amt; save(); await update.message.reply_text(f"✅ حولت {amt:,} لـ {tid}"); return
        if st == "deposit_":
            states.pop(uid); save()
            try: amt = int(text)
            except: await update.message.reply_text("ابعت رقم"); return
            if user["balance"] < amt: await update.message.reply_text("فلوسك مش كفاية"); return
            user["balance"] -= amt; user["bank"] += amt; save(); await update.message.reply_text(f"✅ اودعت {amt:,}"); return
        if st == "withdraw_":
            states.pop(uid); save()
            try: amt = int(text)
            except: await update.message.reply_text("ابعت رقم"); return
            if user["bank"] < amt: await update.message.reply_text("فلوس البنك مش كفاية"); return
            user["bank"] -= amt; user["balance"] += amt; save(); await update.message.reply_text(f"✅ سحبت {amt:,}"); return
        if st == "savings_":
            states.pop(uid); save()
            try: amt = int(text)
            except: await update.message.reply_text("ابعت رقم"); return
            if user["balance"] < amt: await update.message.reply_text("فلوسك مش كفاية"); return
            user["balance"] -= amt; user["savings"] += amt; save(); await update.message.reply_text(f"🐷 حوشت {amt:,}"); return
        if st == "loan_":
            states.pop(uid); save()
            try: amt = int(text)
            except: await update.message.reply_text("ابعت رقم"); return
            if user["loan_left"] > 0: await update.message.reply_text("عليك قرض قديم"); return
            if amt > 10000: await update.message.reply_text("اقصى قرض 10,000"); return
            total = int(amt*1.2); pay = total//3
            user["loan_left"] = total; user["loan_pay"] = pay; user["loan_installments"] = 3; user["balance"] += amt; save()
            await update.message.reply_text(f"💰 خدت قرض {amt:,}\nهتسدد {total:,} على 3 اقساط\nالقسط {pay:,}"); return
        if st == "cert_":
            states.pop(uid); save()
            try: amt = int(text)
            except: await update.message.reply_text("ابعت رقم"); return
            if user["balance"] < amt: await update.message.reply_text("فلوسك مش كفاية"); return
            user["balance"] -= amt; user["certificates"].append({"amount": amt, "date": datetime.now().strftime("%Y-%m-%d")}); save(); await update.message.reply_text(f"📄 عملت شهادة {amt:,}"); return
        if st == "dep_money_":
            states.pop(uid); save()
            try: amt = int(text)
            except: await update.message.reply_text("ابعت رقم"); return
            if user["balance"] < amt: await update.message.reply_text("فلوسك مش كفاية"); return
            user["balance"] -= amt; user["deposits"].append({"amount": amt, "date": datetime.now().strftime("%Y-%m-%d")}); save(); await update.message.reply_text(f"🏦 عملت وديعة {amt:,}"); return
        if st == "visa_use_":
            states.pop(uid); save()
            try: amt = int(text)
            except: await update.message.reply_text("ابعت رقم"); return
            if not user["credit_card"]: await update.message.reply_text("اعمل فيزا الاول"); return
            if user["credit_used"] + amt > user["credit_limit"]: await update.message.reply_text("عديت حد الفيزا"); return
            user["credit_used"] += amt; user["balance"] += amt; save(); await update.message.reply_text(f"💳 سحبت {amt:,} من الفيزا"); return

        # 3 - تيكت
        if st == "waiting_ticket":
            states.pop(uid); data["ticket_counter"] += 1; tid = str(data["ticket_counter"])
            tickets[tid] = {"id": tid, "user_id": uid, "username": update.effective_user.username or "", "text": text, "status": "open", "created": datetime.now().strftime("%d/%m %H:%M"), "reply": ""}; save()
            await update.message.reply_text(f"✅ عملت تيكت #{tid}\nMr cat هيرد عليك قريب 🎧")
            for sid in SUPPORT_IDS:
                try: await context.bot.send_message(chat_id=sid, text=f"🎧 **تيكت جديد #{tid}**\nمن: @{update.effective_user.username or uid} - `{uid}`\n\n{text}\n\n`/reply {tid} الرد`", parse_mode="Markdown")
                except: pass
            return
        if st == "waiting_rate":
            states.pop(uid); save()
            try: rate = int(text)
            except: await update.message.reply_text("ابعت رقم 1-5"); return
            data["ratings"].append({"user": uid, "rate": rate, "time": datetime.now().strftime("%d/%m")}); save(); await update.message.reply_text(f"شكرا {rate} ⭐💙"); return
        if st == "waiting_name":
            states[uid] = "waiting_phone"; data.setdefault("temp", {})[uid] = {"name": text}; save(); await update.message.reply_text(f"تمام يا {text} 👑\nاكتب رقم موبايلك:"); return
        if st == "waiting_phone":
            temp = data.get("temp", {}).get(uid, {}); name = temp.get("name", "عميل"); states.pop(uid)
            data["callbacks"].append({"user_id": uid, "username": update.effective_user.username or "", "name": name, "phone": text, "time": datetime.now().strftime("%d/%m %H:%M"), "done": False}); save()
            await update.message.reply_text(f"✅ سجلنا طلب مكالمة يا {name} على {text}\nMr cat هيكلمك 📞")
            for sid in SUPPORT_IDS:
                try: await context.bot.send_message(chat_id=sid, text=f"📞 **طلب مكالمة!**\n👤 {name}\n📱 {text}\n✈️ @{update.effective_user.username or uid} - `{uid}`", parse_mode="Markdown")
                except: pass
            return

        # رد تلقائي لو اوفلاين
        if data.get("operator_status") == "offline" and int(uid) not in SUPPORT_IDS:
            await update.message.reply_text("🌙 Mr cat اوفلاين دلوقتي.\nاعمل تيكت او اطلب مكالمة وهنرد عليك الصبح 💙", reply_markup=main_kb(uid)); return
        await update.message.reply_text("اكتب /start عشان القايمة 👑", reply_markup=main_kb(uid))
    except Exception as e:
        print(f"ON_MSG ERROR: {e}"); traceback.print_exc()
        try: await update.message.reply_text("حصلت مشكلة صغيرة، جرب تاني /start")
        except: pass

# ===== زرار =====
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        q = update.callback_query; await q.answer(); uid = str(q.from_user.id); user = get_user(uid, q.from_user.username or ""); d = q.data
        if d == "back":
            await q.edit_message_text(f"🏦🎧 **TRAN - بنك + خدمة عملاء**\n💰 كاش: {user['balance']:,} | 🏦 بنك: {user['bank']:,}", reply_markup=main_kb(uid), parse_mode="Markdown"); return
        if d == "bank": await q.edit_message_text("🏦 **البنك:**\nاختار 👇", reply_markup=bank_kb()); return
        if d == "balance": await q.edit_message_text(f"💰 كاش: {user['balance']:,}\n🏦 بنك: {user['bank']:,}\n🐷 تحويش: {user['savings']:,}\n💳 فيزا: {user['credit_used']:,}/{user['credit_limit']:,}\n💰 قرض: {user['loan_left']:,}\n🪙 كوينز: {user['coins']}\n🎫 ID: `{uid}`", reply_markup=bank_kb(), parse_mode="Markdown"); return
        if d == "transfer": states[uid] = "transfer_"; save(); await q.edit_message_text("💸 ابعت: `ID المبلغ`\nمثال: `123456 500`", parse_mode="Markdown"); return
        if d == "deposit": states[uid] = "deposit_"; save(); await q.edit_message_text("🏦 اكتب المبلغ اللي هتودعه:"); return
        if d == "withdraw": states[uid] = "withdraw_"; save(); await q.edit_message_text("🏧 اكتب المبلغ اللي هتسحبه:"); return
        if d == "savings": states[uid] = "savings_"; save(); await q.edit_message_text(f"🐷 تحويشك: {user['savings']:,}\nاكتب المبلغ اللي هتحوشه:"); return
        if d == "visa":
            if not user["credit_card"]:
                num = f"4000 {random.randint(1000,9999)} {random.randint(1000,9999)} {random.randint(1000,9999)}"; user["credit_card"] = num; user["credit_limit"] = 20000 if user["vip"] else 5000; save()
                await q.edit_message_text(f"💳 فيزتك: `{num}`\nالحد: {user['credit_limit']:,}", reply_markup=bank_kb(), parse_mode="Markdown")
            else: await q.edit_message_text(f"💳 فيزتك: {user['credit_card']}\nالحد: {user['credit_limit']:,}\nالمستخدم: {user['credit_used']:,}", reply_markup=bank_kb()); return
        if d == "loan":
            if user["loan_left"] > 0: await q.edit_message_text(f"💰 عليك: {user['loan_left']:,}\nالقسط: {user['loan_pay']:,}\nفاضل: {user['loan_installments']} اقساط", reply_markup=bank_kb())
            else: states[uid] = "loan_"; save(); await q.edit_message_text("💰 اكتب مبلغ القرض (اقصى 10,000):"); return
        if d == "loan_pay":
            if user["loan_left"] <= 0: await q.edit_message_text("مفيش قرض عليك ✅", reply_markup=bank_kb()); return
            if user["balance"] < user["loan_pay"]: await q.edit_message_text("فلوسك مش كفاية", reply_markup=bank_kb()); return
            user["balance"] -= user["loan_pay"]; user["loan_left"] -= user["loan_pay"]; user["loan_installments"] -= 1
            if user["loan_left"] <= 0: user["loan_left"] = 0; user["loan_installments"] = 0
            save(); await q.edit_message_text(f"✅ سددت قسط\nالمتبقي: {user['loan_left']:,}", reply_markup=bank_kb()); return
        if d == "cert": states[uid] = "cert_"; save(); await q.edit_message_text("📄 اكتب مبلغ الشهادة (ربح 20%):"); return
        if d == "dep_money": states[uid] = "dep_money_"; save(); await q.edit_message_text("🏦 اكتب مبلغ الوديعة (فايدة 15%):"); return
        if d == "bills":
            b = user["bills"]; total = b["electric"] + b["water"] + b["internet"]
            if total == 0: b["electric"] = random.randint(50,200); b["water"] = random.randint(30,100); b["internet"] = random.randint(100,300); save(); total = b["electric"]+b["water"]+b["internet"]
            await q.edit_message_text(f"🧾 **فواتيرك:**\n⚡ كهربا: {b['electric']:,}\n💧 مياه: {b['water']:,}\n🌐 نت: {b['internet']:,}\n\nالاجمالي: {total:,}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💳 ادفع", callback_data="bills_pay")],[InlineKeyboardButton("🔙 رجوع", callback_data="bank")]])); return
        if d == "bills_pay":
            b = user["bills"]; total = b["electric"]+b["water"]+b["internet"]
            if user["balance"] < total: await q.edit_message_text("فلوسك مش كفاية", reply_markup=bank_kb()); return
            user["balance"] -= total; user["bills"] = {"electric": 0, "water": 0, "internet": 0}; save(); await q.edit_message_text(f"✅ دفعت {total:,} ج", reply_markup=bank_kb()); return
        if d == "statement":
            tx = "\n".join(user["transactions"][:10]) or "مفيش معاملات"
            await q.edit_message_text(f"📜 **كشف حساب:**\n\n{tx}", reply_markup=bank_kb(), parse_mode="Markdown"); return
        if d == "daily":
            today = datetime.now().strftime("%Y-%m-%d")
            if user["daily_last"] == today: await q.edit_message_text("خدت هديتك النهاردة 🎁", reply_markup=main_kb(uid)); return
            r = random.randint(100,500) * (2 if user["vip"] else 1); user["balance"] += r; user["daily_last"] = today; user["coins"] += 1; save(); await q.edit_message_text(f"🎁 خدت {r:,} ج + 1 كوين!", reply_markup=main_kb(uid)); return
        if d == "top":
            s = sorted(users.values(), key=lambda x: x["balance"]+x["bank"]+x["savings"], reverse=True)[:10]; txt = "🏆 **اغنى 10:**\n\n"
            for i, u in enumerate(s, 1): txt += f"{i}. @{u['username'] or u['id']} - {u['balance']+u['bank']+u['savings']:,} ج\n"
            await q.edit_message_text(txt, reply_markup=main_kb(uid), parse_mode="Markdown"); return
        # دعم
        if d == "support":
            await q.edit_message_text(f"🎧 **خدمة العملاء**\n\n👤 Mr cat - {status_emoji()}\n📱 @{MR_CAT_USERNAME}\n📞 {MR_CAT_PHONE}", reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💬 شات مباشر", callback_data="live_start")],
                [InlineKeyboardButton("📞 اطلب مكالمة", callback_data="request_call")],
                [InlineKeyboardButton("📩 تيكت جديد", callback_data="new_ticket")],
                [InlineKeyboardButton("🔙 رجوع", callback_data="back")],
            ]), parse_mode="Markdown"); return
        if d == "call":
            await q.edit_message_text(f"📞 **اتصال مباشر**\n\n👤 Mr cat\n📞 `{MR_CAT_PHONE}`\nدوس على الرقم واتصل", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📞 اطلب مكالمة", callback_data="request_call")],[InlineKeyboardButton("🔙 رجوع", callback_data="back")]]), parse_mode="Markdown"); return
        if d == "request_call": states[uid] = "waiting_name"; save(); await q.edit_message_text("📞 **طلب مكالمة**\nاكتب اسمك:"); return
        if d == "live_start":
            if data.get("operator_status") == "offline": await q.edit_message_text("🔴 Mr cat اوفلاين.\nاعمل تيكت او اطلب مكالمة.", reply_markup=main_kb(uid)); return
            if uid in live_chats: await q.edit_message_text("انت في شات مباشر already 💬 ابعت رسالتك.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⏹️ انهاء", callback_data="live_end")]])); return
            if data.get("operator_status") == "busy":
                if uid not in data["queue"]: data["queue"].append(uid); save()
                pos = data["queue"].index(uid)+1
                await q.edit_message_text(f"🟡 Mr cat مشغول.\n⏳ رقمك في الطابور: {pos}", reply_markup=main_kb(uid)); return
            live_chats[uid] = {"started": datetime.now().strftime("%H:%M"), "username": q.from_user.username or ""}; save()
            await q.edit_message_text("💬 **انت في شات مباشر مع Mr cat** 🟢\nابعت نص / صورة / فويس", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⏹️ انهاء", callback_data="live_end")]]))
            for sid in SUPPORT_IDS:
                try: await context.bot.send_message(chat_id=sid, text=f"🔴 **عميل دخل شات مباشر!**\nمن: @{q.from_user.username or uid} - `{uid}`\n\n`/chat {uid} ردك`", parse_mode="Markdown")
                except: pass
            return
        if d == "live_end":
            if uid in live_chats: del live_chats[uid]; save()
            if uid in data.get("queue", []): data["queue"].remove(uid); save()
            await q.edit_message_text("⏹️ انهيت المحادثة 💙", reply_markup=main_kb(uid))
            for sid in SUPPORT_IDS:
                try: await context.bot.send_message(chat_id=sid, text=f"⏹️ العميل `{uid}` انهى الشات")
                except: pass
            return
        if d == "new_ticket": states[uid] = "waiting_ticket"; save(); await q.edit_message_text("📩 اكتب مشكلتك في رسالة واحدة:"); return
        if d == "my_tickets":
            my = [t for t in tickets.values() if t["user_id"] == uid]
            if not my: await q.edit_message_text("مفيش تيكتات", reply_markup=main_kb(uid)); return
            txt = "📋 **تيكتاتك:**\n\n"
            for t in my[-5:]: txt += f"#{t['id']} - {t['status']} - {t['text'][:50]}\n"
            await q.edit_message_text(txt, reply_markup=main_kb(uid), parse_mode="Markdown"); return
        if d == "faq":
            await q.edit_message_text("❓ **اسئلة شائعة:**\n\n💰 الشحن: كلم Mr cat\n⏰ المواعيد: 10ص - 12م\n🔄 الاسترجاع: اعمل تيكت\n📦 الشحن: 5-30 دقيقة", reply_markup=main_kb(uid)); return
        if d == "rate": states[uid] = "waiting_rate"; save(); await q.edit_message_text("⭐ قيمنا 1-5:"); return
        if d == "support_panel":
            if int(uid) not in SUPPORT_IDS: return
            open_t = len([t for t in tickets.values() if t["status"] == "open"])
            await q.edit_message_text(f"🎧 **لوحة الدعم**\n\nحالتك: {status_emoji()}\n💬 شات: {len(live_chats)}\n⏳ طابور: {len(data.get('queue',[]))}\n📞 مكالمات: {len([c for c in data.get('callbacks',[]) if not c['done']])}\n📩 مفتوحة: {open_t}", reply_markup=support_kb(), parse_mode="Markdown"); return
        if d == "live_active":
            if int(uid) not in SUPPORT_IDS: return
            if not live_chats: await q.edit_message_text("مفيش شاتات", reply_markup=support_kb()); return
            txt = "💬 **شاتات:**\n\n"
            for cid, info in live_chats.items(): txt += f"@{info['username']} - `{cid}`\n`/chat {cid} ردك`\n\n"
            await q.edit_message_text(txt, reply_markup=support_kb(), parse_mode="Markdown"); return
        if d == "queue_list":
            if int(uid) not in SUPPORT_IDS: return
            qlist = data.get("queue", [])
            if not qlist: await q.edit_message_text("الطابور فاضي ✅", reply_markup=support_kb()); return
            txt = "⏳ **طابور:**\n\n"
            for i, cid in enumerate(qlist, 1): txt += f"{i}. `{cid}`\n"
            await q.edit_message_text(txt, reply_markup=support_kb(), parse_mode="Markdown"); return
        if d == "callback_list":
            if int(uid) not in SUPPORT_IDS: return
            cbs = [c for c in data.get("callbacks", []) if not c["done"]]
            if not cbs: await q.edit_message_text("مفيش طلبات", reply_markup=support_kb()); return
            txt = "📞 **طلبات مكالمات:**\n\n"
            for c in cbs[-10:]: txt += f"👤 {c['name']} - {c['phone']} - `{c['user_id']}`\n"
            await q.edit_message_text(txt, reply_markup=support_kb(), parse_mode="Markdown"); return
        if d == "support_open":
            if int(uid) not in SUPPORT_IDS: return
            open_t = [t for t in tickets.values() if t["status"] == "open"]
            if not open_t: await q.edit_message_text("مفيش تيكتات ✅", reply_markup=support_kb()); return
            txt = "📋 **تيكتات:**\n\n"
            for t in open_t[-10:]: txt += f"#{t['id']} - @{t['username']} - {t['text'][:50]}\n`/reply {t['id']} الرد`\n\n"
            await q.edit_message_text(txt, reply_markup=support_kb(), parse_mode="Markdown"); return
        if d == "support_stats":
            if int(uid) not in SUPPORT_IDS: return
            open_t = len([t for t in tickets.values() if t["status"] == "open"]); closed_t = len([t for t in tickets.values() if t["status"] == "closed"])
            avg = sum([r["rate"] for r in data["ratings"]]) / len(data["ratings"]) if data["ratings"] else 0
            await q.edit_message_text(f"📊 **احصائيات:**\n\n👥 يوزرز: {len(users)}\n💬 شات: {len(live_chats)}\n📩 مفتوحة: {open_t}\n✅ مقفولة: {closed_t}\n⭐ تقييم: {avg:.1f}/5", reply_markup=support_kb(), parse_mode="Markdown"); return
        if d == "change_status":
            if int(uid) not in SUPPORT_IDS: return
            await q.edit_message_text("غير حالتك:", reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🟢 اونلاين", callback_data="set_online")],
                [InlineKeyboardButton("🟡 مشغول", callback_data="set_busy")],
                [InlineKeyboardButton("🔴 اوفلاين", callback_data="set_offline")],
                [InlineKeyboardButton("🔙 رجوع", callback_data="back")],
            ])); return
        if d in ["set_online","set_busy","set_offline"]:
            if int(uid) not in SUPPORT_IDS: return
            mp = {"set_online":"online","set_busy":"busy","set_offline":"offline"}
            data["operator_status"] = mp[d]; save(); await q.edit_message_text(f"✅ حالتك: {mp[d]}", reply_markup=main_kb(uid)); return
        if d == "owner":
            if str(uid) != str(OWNER_ID): return
            await q.edit_message_text("👑 **الاونر:**\n\n`/addmoney ID المبلغ`\n`/ban ID`\n`/unban ID`\n`/vip ID`\n`/reply 101 الرد`\n`/chat ID رسالة`\n`/close 101`\n`/status online`", reply_markup=main_kb(uid), parse_mode="Markdown"); return
    except Exception as e:
        print(f"BUTTON ERROR: {e}"); traceback.print_exc()
        try: await q.edit_message_text("حصلت مشكلة، دوس /start تاني")
        except: pass

async def error_handler(update, context):
    print(f"ERROR: {context.error}"); traceback.print_exc()

def main():
    if not TOKEN:
        print("❌ BOT_TOKEN مش موجود! حطه في Render Environment")
        # خلي السيرفر شغال عشان ريندر ميقعش
        while True: time.sleep(60)
    while True:
        try:
            print("🚀 STARTING BOT...")
            app = ApplicationBuilder().token(TOKEN).build()
            app.add_handler(CommandHandler("start", start))
            app.add_handler(CommandHandler("help", cmd_help))
            app.add_handler(CommandHandler("balance", cmd_balance))
            app.add_handler(CommandHandler("daily", cmd_daily))
            app.add_handler(CommandHandler("top", cmd_top))
            app.add_handler(CommandHandler("reply", cmd_reply))
            app.add_handler(CommandHandler("close", cmd_close))
            app.add_handler(CommandHandler("chat", cmd_chat))
            app.add_handler(CommandHandler("endchat", cmd_endchat))
            app.add_handler(CommandHandler("status", cmd_status))
            app.add_handler(CommandHandler("addmoney", cmd_addmoney))
            app.add_handler(CommandHandler("ban", cmd_ban))
            app.add_handler(CommandHandler("unban", cmd_unban))
            app.add_handler(CommandHandler("vip", cmd_vip))
            app.add_handler(CallbackQueryHandler(buttons))
            # ده كان الغلط الكبير - صلحته
            app.add_handler(MessageHandler((filters.TEXT | filters.PHOTO | filters.VOICE) & ~filters.COMMAND, on_msg))
            app.add_error_handler(error_handler)
            print("✅ BOT STARTED - مستني رسايل...")
            app.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)
        except Exception as e:
            print(f"❌ CRASH - هيرجع بعد 3 ثواني: {e}"); traceback.print_exc(); time.sleep(3)

if __name__ == "__main__": main()
