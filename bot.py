import os, json, random, time, threading, requests, traceback
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from flask import Flask

TOKEN = os.environ.get("BOT_TOKEN", "").strip()
OWNER_ID = 8188263997
DATA_FILE = "data.json"

SUPPORT_IDS = [8188263997, 7125945857]
MR_CAT_ID = 7125945857
MR_CAT_USERNAME = "cat_max_10"
MR_CAT_PHONE = "+201155973454"
MR_CAT_WHATSAPP = "201155973454"

# ===== ردود جاهزة لـ Mr cat =====
CANNED = {
    "welcome": "اهلا بيك يا وحش 💙 نورتنا، قولي مشكلتك ايه وانا هحلها معاك حالا 👑",
    "wait": "ثانية واحدة يا وحش بجهزلك الحل 👀",
    "charge": "عشان تشحن ابعتلي المبلغ اللي عايز تشحنه وانا هبعتلك التفاصيل على طول 💰",
    "done": "خلصت يا وحش ✅ جرب دلوقتي وقولي اشتغل ولا لا",
    "thanks": "العفو يا وحش 💙 احنا في خدمتك اي وقت، متنساش تقيمنا ⭐",
    "refund": "تمام هعملك استرجاع حالا، ابعتلي سكرين شوت للمشكلة 📸",
    "offline": "انا مشغول شوية دلوقتي بس سيب رسالتك وهرد عليك اول ما ارجع 🟡",
    "vip": "انت عميل VIP عندنا 👑 ليك اولوية في الرد والشحن اسرع",
}

# ===== ردود تلقائية ذكية =====
AUTO_REPLIES = {
    "شحن": "💰 عايز تشحن؟\nاكتب المبلغ اللي عايز تشحنه او دوس شات مباشر و Mr cat هيرد عليك حالا.",
    "فلوس": "💰 مشكلة في الفلوس؟\nاعمل تيكت واختار تصنيف 'مشكلة فلوس' وهنحلها في اقل من 10 دقايق.",
    "مشكلة": "😔 متزعلش يا وحش، احنا هنحلها.\nابعت سكرين شوت للمشكلة او دوس شات مباشر.",
    "استرجاع": "🔄 عايز استرجاع؟\nاعمل تيكت واختار 'استرجاع' وابعت سكرين شوت.",
    "سلام": "اهلا بيك يا وحش 💙 نورت بوت خدمة العملاء 👑",
    "ازيك": "الحمدلله يا وحش 💙 انت عامل ايه؟ قولي اساعدك ازاي؟",
    "بنك": "🏦 البنك شغال تمام.\nدوس على زرار 'بنك' من القايمة وشوف رصيدك.",
    "فيزا": "💳 عايز فيزا؟\nدوس بنك > فيزا وهعملك فيزا 4000 على طول.",
    "قرض": "💰 القرض اقصى 10,000 ج على 3 اقساط.\nدوس بنك > قرض.",
}

def load():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            d = json.load(f)
            for k, v in {"users": {}, "tickets": {}, "ticket_counter": 100, "states": {}, "ratings": [], "live_chats": {}, "queue": [], "callbacks": [], "operator_status": "online", "operator_msg": "", "temp": {}, "agent_stats": {}}.items():
                d.setdefault(k, v)
            return d
    except:
        return {"users": {}, "tickets": {}, "ticket_counter": 100, "states": {}, "ratings": [], "live_chats": {}, "queue": [], "callbacks": [], "operator_status": "online", "operator_msg": "", "temp": {}, "agent_stats": {}}
def save():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e: print(f"SAVE ERROR: {e}")
data = load(); users = data["users"]; tickets = data["tickets"]; states = data["states"]; live_chats = data["live_chats"]

def get_user(uid, username=""):
    uid = str(uid)
    if uid not in users:
        users[uid] = {"id": uid, "username": username, "balance": 1000, "bank": 0, "savings": 0, "loan_left": 0, "loan_pay": 0, "loan_installments": 0, "credit_card": None, "credit_limit": 0, "credit_used": 0, "vip": False, "banned": False, "daily_last": "", "transactions": [], "coins": 0, "level": 1, "xp": 0, "certificates": [], "deposits": [], "bills": {"electric": 0, "water": 0, "internet": 0}, "tickets_count": 0}
        save()
    return users[uid]

def agent_add(agent_id, action):
    # احصائيات Mr cat
    aid = str(agent_id)
    if aid not in data["agent_stats"]: data["agent_stats"][aid] = {"replied": 0, "closed": 0, "chats": 0, "rating_sum": 0, "rating_count": 0, "first_reply_times": []}
    data["agent_stats"][aid][action] = data["agent_stats"][aid].get(action, 0) + 1
    save()

# ===== سيرفر =====
app_flask = Flask(__name__)
@app_flask.route('/')
def home(): return "BOT ULTRA SUPPORT ALIVE ✅"
@app_flask.route('/health')
def health(): return "OK"
def run_flask():
    try: app_flask.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)), threaded=True)
    except: time.sleep(3); run_flask()
def self_ping():
    time.sleep(15); url = os.environ.get("RENDER_EXTERNAL_URL", "")
    if not url: return
    while True:
        try: requests.get(url, timeout=10)
        except: pass
        time.sleep(240)
def check_slow_tickets():
    # تنبيه لو تيكت اتأخر اكتر من 30 دقيقة
    while True:
        time.sleep(600)
        try:
            now = datetime.now()
            for tid, t in list(tickets.items()):
                if t["status"] == "open" and not t.get("notified_slow"):
                    created = datetime.strptime(t.get("created_full", datetime.now().strftime("%Y-%m-%d %H:%M")), "%Y-%m-%d %H:%M")
                    if (now - created).total_seconds() > 1800:
                        t["notified_slow"] = True; save()
                        print(f"SLOW TICKET {tid}")
        except: pass
threading.Thread(target=run_flask, daemon=True).start()
threading.Thread(target=self_ping, daemon=True).start()
threading.Thread(target=check_slow_tickets, daemon=True).start()

def status_emoji():
    s = data.get("operator_status", "online")
    if s == "online": return "🟢 اونلاين - بيرد حالا"
    if s == "busy": return "🟡 مشغول"
    return "🔴 اوفلاين"

def main_kb(uid):
    kb = [
        [InlineKeyboardButton("💬 شات مباشر 🔴", callback_data="live_start"), InlineKeyboardButton("📞 اطلب مكالمة", callback_data="request_call")],
        [InlineKeyboardButton("💰 بنك | رصيدي", callback_data="bank"), InlineKeyboardButton("🎧 خدمة العملاء", callback_data="support")],
        [InlineKeyboardButton("💚 واتساب", url=f"https://wa.me/{MR_CAT_WHATSAPP}"), InlineKeyboardButton("✈️ تليجرام Mr cat", url=f"https://t.me/{MR_CAT_USERNAME}")],
        [InlineKeyboardButton("📩 تيكت جديد", callback_data="new_ticket"), InlineKeyboardButton("📋 تيكتاتي", callback_data="my_tickets")],
        [InlineKeyboardButton("🎁 هدية يومية", callback_data="daily"), InlineKeyboardButton("🏆 الاغنياء", callback_data="top")],
        [InlineKeyboardButton("❓ اسئلة شائعة", callback_data="faq"), InlineKeyboardButton("⭐ قيمنا", callback_data="rate")],
    ]
    if int(uid) in SUPPORT_IDS: kb.append([InlineKeyboardButton("🎧 لوحة الدعم", callback_data="support_panel")])
    if str(uid) == str(OWNER_ID): kb.append([InlineKeyboardButton("👑 الاونر", callback_data="owner")])
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
        [InlineKeyboardButton("🔥 تيكتات مستعجلة", callback_data="support_urgent")],
        [InlineKeyboardButton("⏳ طابور", callback_data="queue_list")],
        [InlineKeyboardButton("📞 طلبات مكالمات", callback_data="callback_list")],
        [InlineKeyboardButton("📩 كل التيكتات المفتوحة", callback_data="support_open")],
        [InlineKeyboardButton("📊 احصائيات + اداء Mr cat", callback_data="support_stats")],
        [InlineKeyboardButton("💬 ردود جاهزة", callback_data="canned_list")],
        [InlineKeyboardButton("🟢/🟡/🔴 غير حالتي", callback_data="change_status")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="back")],
    ])

def category_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 شحن / فلوس", callback_data="cat_charge")],
        [InlineKeyboardButton("🐛 مشكلة تقنية", callback_data="cat_bug")],
        [InlineKeyboardButton("🔄 استرجاع", callback_data="cat_refund")],
        [InlineKeyboardButton("💡 اقتراح", callback_data="cat_suggest")],
        [InlineKeyboardButton("❓ استفسار عام", callback_data="cat_general")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="back")],
    ])

def priority_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🟢 عادي", callback_data="pri_normal")],
        [InlineKeyboardButton("🟡 مهم", callback_data="pri_important")],
        [InlineKeyboardButton("🔴 مستعجل جدا", callback_data="pri_urgent")],
    ])

def canned_kb(uid):
    # ردود جاهزة - لازم نعرف هنرد على مين
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👋 ترحيب", callback_data=f"canned_welcome_{uid}")],
        [InlineKeyboardButton("⏳ استنى ثانية", callback_data=f"canned_wait_{uid}")],
        [InlineKeyboardButton("💰 شحن", callback_data=f"canned_charge_{uid}")],
        [InlineKeyboardButton("✅ خلصت", callback_data=f"canned_done_{uid}")],
        [InlineKeyboardButton("🙏 شكر", callback_data=f"canned_thanks_{uid}")],
        [InlineKeyboardButton("🔄 استرجاع", callback_data=f"canned_refund_{uid}")],
        [InlineKeyboardButton("👑 VIP", callback_data=f"canned_vip_{uid}")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="support_panel")],
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        u = update.effective_user; user = get_user(u.id, u.username or "")
        if user["banned"]: await update.message.reply_text("🚫 انت محظور"); return
        txt = f"""🏦🎧 **TRAN - بنك + دعم احترافي** 👑
اهلا {u.first_name} 💙

💰 كاش: {user['balance']:,} | 🏦 بنك: {user['bank']:,}
🐷 تحويش: {user['savings']:,} | 🪙 {user['coins']}

👤 **Mr cat** - {status_emoji()}
📞 {MR_CAT_PHONE} | @{MR_CAT_USERNAME}
🎫 ID: `{u.id}`"""
        if data.get("operator_msg"): txt += f"\n\n📢 {data['operator_msg']}"
        await update.message.reply_text(txt, reply_markup=main_kb(u.id), parse_mode="Markdown")
    except Exception as e: print(f"START ERROR: {e}")

async def cmd_help(update, context):
    await update.message.reply_text("🆘 /start - القايمة\n/balance - رصيدك\n/daily - هدية\n\nالدعم: /reply 101 رد - /chat ID رد - /close 101 - /status online", parse_mode="Markdown")
async def cmd_balance(update, context):
    user = get_user(update.effective_user.id); await update.message.reply_text(f"💰 كاش: {user['balance']:,}\n🏦 بنك: {user['bank']:,}\n🐷 تحويش: {user['savings']:,}")
async def cmd_daily(update, context):
    user = get_user(update.effective_user.id); today = datetime.now().strftime("%Y-%m-%d")
    if user["daily_last"] == today: await update.message.reply_text("خدت هديتك النهاردة"); return
    r = random.randint(100,500)*(2 if user["vip"] else 1); user["balance"]+=r; user["daily_last"]=today; user["coins"]+=1; save(); await update.message.reply_text(f"🎁 خدت {r:,} + 1 كوين!")
async def cmd_top(update, context):
    s = sorted(users.values(), key=lambda x: x["balance"]+x["bank"]+x["savings"], reverse=True)[:10]; txt="🏆 **اغنى 10:**\n\n"
    for i,u in enumerate(s,1): txt+=f"{i}. @{u['username'] or u['id']} - {u['balance']+u['bank']+u['savings']:,} ج\n"
    await update.message.reply_text(txt, parse_mode="Markdown")

# ===== دعم محسن =====
async def cmd_reply(update, context):
    if update.effective_user.id not in SUPPORT_IDS: return
    if len(context.args) < 2: await update.message.reply_text("`/reply 101 الرد`", parse_mode="Markdown"); return
    tid = context.args[0]; txt = " ".join(context.args[1:])
    if tid not in tickets: await update.message.reply_text("مفيش تيكت"); return
    tickets[tid]["status"]="replied"; tickets[tid]["reply"]=txt; tickets[tid]["replied_by"]=str(update.effective_user.id); tickets[tid]["replied_at"]=datetime.now().strftime("%H:%M"); save()
    agent_add(update.effective_user.id, "replied")
    try: await context.bot.send_message(chat_id=int(tickets[tid]["user_id"]), text=f"🎧 **Mr cat رد عليك:**\n\n{txt}\n\n⭐ قيمنا من البوت", parse_mode="Markdown")
    except: pass
    await update.message.reply_text(f"✅ رديت على #{tid} - {tickets[tid].get('category','عام')} - {tickets[tid].get('priority','عادي')}")
async def cmd_close(update, context):
    if update.effective_user.id not in SUPPORT_IDS: return
    if not context.args: return
    tid = context.args[0]
    if tid not in tickets: return
    tickets[tid]["status"]="closed"; tickets[tid]["closed_at"]=datetime.now().strftime("%d/%m %H:%M"); save()
    agent_add(update.effective_user.id, "closed")
    try: await context.bot.send_message(chat_id=int(tickets[tid]["user_id"]), text=f"✅ تيكت #{tid} اتقفل.\nاتحلت مشكلتك؟\n⭐ قيمنا من البوت - دوس ⭐ قيمنا", reply_markup=main_kb(int(tickets[tid]["user_id"])))
    except: pass
    await update.message.reply_text(f"✅ قفلت #{tid}")
async def cmd_chat(update, context):
    if update.effective_user.id not in SUPPORT_IDS: return
    if len(context.args) < 2: await update.message.reply_text("`/chat ID رسالتك`", parse_mode="Markdown"); return
    uid = context.args[0]; txt = " ".join(context.args[1:])
    try:
        await context.bot.send_message(chat_id=int(uid), text=f"💬 **Mr cat:**\n\n{txt}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⏹️ انهاء", callback_data="live_end")],[InlineKeyboardButton("⭐ قيم Mr cat", callback_data="rate")]]))
        agent_add(update.effective_user.id, "chats")
        await update.message.reply_text("✅ بعت")
    except Exception as e: await update.message.reply_text(f"مش عارف ابعت: {e}")
async def cmd_endchat(update, context):
    if update.effective_user.id not in SUPPORT_IDS: return
    if not context.args: return
    uid = context.args[0]
    if uid in live_chats: del live_chats[uid]; save()
    try: await context.bot.send_message(chat_id=int(uid), text="⏹️ Mr cat انهى المحادثة\n⭐ قيمنا بقى", reply_markup=main_kb(int(uid)))
    except: pass
    await update.message.reply_text("✅ انهيت")
async def cmd_status(update, context):
    if update.effective_user.id not in SUPPORT_IDS: return
    if not context.args: await update.message.reply_text("`/status online` / `busy` / `offline`"); return
    s = context.args[0].lower()
    if s in ["online","busy","offline"]: data["operator_status"]=s; save(); await update.message.reply_text(f"✅ حالتك: {s}")
async def cmd_addmoney(update, context):
    if update.effective_user.id != OWNER_ID: return
    if len(context.args) < 2: return
    try: tid = context.args[0]; amt = int(context.args[1])
    except: return
    u = get_user(tid); u["balance"]+=amt; save(); await update.message.reply_text(f"✅ ضفت {amt:,} لـ {tid}")
async def cmd_ban(update, context):
    if update.effective_user.id != OWNER_ID: return
    if not context.args: return
    u = get_user(context.args[0]); u["banned"]=True; save(); await update.message.reply_text(f"🚫 حظرت {context.args[0]}")
async def cmd_unban(update, context):
    if update.effective_user.id != OWNER_ID: return
    if not context.args: return
    u = get_user(context.args[0]); u["banned"]=False; save(); await update.message.reply_text(f"✅ فكيت {context.args[0]}")
async def cmd_vip(update, context):
    if update.effective_user.id != OWNER_ID: return
    if not context.args: return
    u = get_user(context.args[0]); u["vip"]=True; u["credit_limit"]=20000; save(); await update.message.reply_text(f"👑 VIP لـ {context.args[0]}")

async def on_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update.message: return
        uid = str(update.effective_user.id); user = get_user(uid, update.effective_user.username or "")
        if user["banned"]: return
        text = update.message.text or update.message.caption or ""
        if update.message.voice: text = "🎤 رسالة صوتية"
        if update.message.photo and not text: text = "🖼️ صورة"
        if update.message.photo and update.message.caption: text = f"🖼️ {update.message.caption}"
        st = states.get(uid, "")

        # شات مباشر
        if uid in live_chats and int(uid) not in SUPPORT_IDS:
            for sid in SUPPORT_IDS:
                try:
                    if update.message.photo: await context.bot.send_photo(chat_id=sid, photo=update.message.photo[-1].file_id, caption=f"💬 شات مباشر من @{update.effective_user.username or uid} - `{uid}`\n\n{text}\n\n`/chat {uid} ردك`", parse_mode="Markdown")
                    elif update.message.voice:
                        await context.bot.send_voice(chat_id=sid, voice=update.message.voice.file_id)
                        await context.bot.send_message(chat_id=sid, text=f"🎤 فويس من `{uid}` - `/chat {uid} ردك`", parse_mode="Markdown")
                    else: await context.bot.send_message(chat_id=sid, text=f"💬 **شات مباشر**\nمن: @{update.effective_user.username or uid} - `{uid}`\n\n{text}\n\n`/chat {uid} ردك`", parse_mode="Markdown")
                except: pass
            await update.message.reply_text("✅ وصلت لـ Mr cat 👀", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⏹️ انهاء", callback_data="live_end")]]))
            return

        # حالات بنك
        if st == "transfer_":
            states.pop(uid); save()
            try: tid, amt = text.split(); amt=int(amt)
            except: await update.message.reply_text("اكتب: `ID المبلغ`", parse_mode="Markdown"); return
            if user["balance"] < amt: await update.message.reply_text("فلوسك مش كفاية"); return
            t = get_user(tid); user["balance"]-=amt; t["balance"]+=amt; save(); await update.message.reply_text(f"✅ حولت {amt:,} لـ {tid}"); return
        if st == "deposit_":
            states.pop(uid); save()
            try: amt=int(text)
            except: await update.message.reply_text("ابعت رقم"); return
            if user["balance"] < amt: await update.message.reply_text("فلوسك مش كفاية"); return
            user["balance"]-=amt; user["bank"]+=amt; save(); await update.message.reply_text(f"✅ اودعت {amt:,}"); return
        if st == "withdraw_":
            states.pop(uid); save()
            try: amt=int(text)
            except: await update.message.reply_text("ابعت رقم"); return
            if user["bank"] < amt: await update.message.reply_text("فلوس البنك مش كفاية"); return
            user["bank"]-=amt; user["balance"]+=amt; save(); await update.message.reply_text(f"✅ سحبت {amt:,}"); return
        if st == "savings_":
            states.pop(uid); save()
            try: amt=int(text)
            except: await update.message.reply_text("ابعت رقم"); return
            if user["balance"] < amt: await update.message.reply_text("فلوسك مش كفاية"); return
            user["balance"]-=amt; user["savings"]+=amt; save(); await update.message.reply_text(f"🐷 حوشت {amt:,}"); return
        if st == "loan_":
            states.pop(uid); save()
            try: amt=int(text)
            except: await update.message.reply_text("ابعت رقم"); return
            if user["loan_left"]>0: await update.message.reply_text("عليك قرض قديم"); return
            if amt>10000: await update.message.reply_text("اقصى 10,000"); return
            total=int(amt*1.2); pay=total//3; user["loan_left"]=total; user["loan_pay"]=pay; user["loan_installments"]=3; user["balance"]+=amt; save(); await update.message.reply_text(f"💰 خدت قرض {amt:,} - هتسدد {total:,} على 3 اقساط - القسط {pay:,}"); return
        if st == "cert_":
            states.pop(uid); save()
            try: amt=int(text)
            except: await update.message.reply_text("ابعت رقم"); return
            if user["balance"]<amt: await update.message.reply_text("فلوسك مش كفاية"); return
            user["balance"]-=amt; user["certificates"].append({"amount": amt}); save(); await update.message.reply_text(f"📄 عملت شهادة {amt:,}"); return
        if st == "dep_money_":
            states.pop(uid); save()
            try: amt=int(text)
            except: await update.message.reply_text("ابعت رقم"); return
            if user["balance"]<amt: await update.message.reply_text("فلوسك مش كفاية"); return
            user["balance"]-=amt; user["deposits"].append({"amount": amt}); save(); await update.message.reply_text(f"🏦 عملت وديعة {amt:,}"); return
        if st == "visa_use_":
            states.pop(uid); save()
            try: amt=int(text)
            except: await update.message.reply_text("ابعت رقم"); return
            if not user["credit_card"]: await update.message.reply_text("اعمل فيزا الاول"); return
            if user["credit_used"]+amt > user["credit_limit"]: await update.message.reply_text("عديت حد الفيزا"); return
            user["credit_used"]+=amt; user["balance"]+=amt; save(); await update.message.reply_text(f"💳 سحبت {amt:,} من الفيزا"); return

        # تيكت - بعد اختيار التصنيف والاولوية
        if st == "waiting_ticket_text":
            states[uid]="waiting_ticket_done"; data.setdefault("temp", {})[uid] = {"text": text, "category": data.get("temp", {}).get(uid, {}).get("category", "عام")}; save()
            await update.message.reply_text("تمام! اختار اولوية التيكت:", reply_markup=priority_kb()); return
        if st == "waiting_rate":
            states.pop(uid); save()
            try: rate=int(text)
            except: await update.message.reply_text("ابعت رقم 1-5"); return
            data["ratings"].append({"user": uid, "rate": rate, "time": datetime.now().strftime("%d/%m")}); save()
            # احسب اداء Mr cat
            if data["agent_stats"].get(str(MR_CAT_ID)):
                s = data["agent_stats"][str(MR_CAT_ID)]; s["rating_sum"]+=rate; s["rating_count"]+=1; save()
            await update.message.reply_text(f"شكرا على تقييمك {rate} ⭐💙"); return
        if st == "waiting_name":
            states[uid]="waiting_phone"; data.setdefault("temp", {})[uid]={"name": text}; save(); await update.message.reply_text(f"تمام يا {text} 👑\nاكتب رقم موبايلك:"); return
        if st == "waiting_phone":
            temp = data.get("temp", {}).get(uid, {}); name=temp.get("name","عميل"); states.pop(uid)
            data["callbacks"].append({"user_id": uid, "username": update.effective_user.username or "", "name": name, "phone": text, "time": datetime.now().strftime("%d/%m %H:%M"), "done": False}); save()
            await update.message.reply_text(f"✅ سجلنا طلب مكالمة يا {name} على {text}\nMr cat هيكلمك 📞")
            for sid in SUPPORT_IDS:
                try: await context.bot.send_message(chat_id=sid, text=f"📞 **طلب مكالمة!**\n👤 {name}\n📱 {text}\n✈️ @{update.effective_user.username or uid} - `{uid}`", parse_mode="Markdown")
                except: pass
            return

        # رد تلقائي ذكي - لو العميل مش في حالة معينة
        if int(uid) not in SUPPORT_IDS and not st:
            low = text.lower()
            for key, reply in AUTO_REPLIES.items():
                if key in low:
                    await update.message.reply_text(reply, reply_markup=main_kb(uid))
                    # لو كتب مشكلة كبيرة افتح شات مباشر تلقائي
                    if key in ["مشكلة", "استرجاع"]:
                        for sid in SUPPORT_IDS:
                            try: await context.bot.send_message(chat_id=sid, text=f"⚠️ **تنبيه ذكي:** العميل `{uid}` كتب كلمة '{key}'\nرسالته: {text}", parse_mode="Markdown")
                            except: pass
                    return
        if data.get("operator_status")=="offline" and int(uid) not in SUPPORT_IDS and not st:
            await update.message.reply_text("🌙 Mr cat اوفلاين دلوقتي.\nاعمل تيكت او اطلب مكالمة وهنرد عليك الصبح 💙", reply_markup=main_kb(uid)); return
        await update.message.reply_text("اكتب /start عشان القايمة 👑", reply_markup=main_kb(uid))
    except Exception as e:
        print(f"ON_MSG ERROR: {e}"); traceback.print_exc()
        try: await update.message.reply_text("حصلت مشكلة صغيرة، جرب /start")
        except: pass

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        q = update.callback_query; await q.answer(); uid = str(q.from_user.id); user = get_user(uid, q.from_user.username or ""); d = q.data
        if d == "back": await q.edit_message_text(f"🏦🎧 **TRAN**\n💰 كاش: {user['balance']:,} | 🏦 بنك: {user['bank']:,}", reply_markup=main_kb(uid), parse_mode="Markdown"); return
        if d == "bank": await q.edit_message_text("🏦 **البنك:**", reply_markup=bank_kb()); return
        if d == "balance": await q.edit_message_text(f"💰 كاش: {user['balance']:,}\n🏦 بنك: {user['bank']:,}\n🐷 تحويش: {user['savings']:,}\n💳 فيزا: {user['credit_used']:,}/{user['credit_limit']:,}\n💰 قرض: {user['loan_left']:,}\n🪙 كوينز: {user['coins']}", reply_markup=bank_kb(), parse_mode="Markdown"); return
        if d == "transfer": states[uid]="transfer_"; save(); await q.edit_message_text("💸 ابعت: `ID المبلغ`", parse_mode="Markdown"); return
        if d == "deposit": states[uid]="deposit_"; save(); await q.edit_message_text("🏦 اكتب المبلغ:"); return
        if d == "withdraw": states[uid]="withdraw_"; save(); await q.edit_message_text("🏧 اكتب المبلغ:"); return
        if d == "savings": states[uid]="savings_"; save(); await q.edit_message_text(f"🐷 تحويشك: {user['savings']:,}\nاكتب المبلغ:"); return
        if d == "visa":
            if not user["credit_card"]:
                num = f"4000 {random.randint(1000,9999)} {random.randint(1000,9999)} {random.randint(1000,9999)}"; user["credit_card"]=num; user["credit_limit"]=20000 if user["vip"] else 5000; save(); await q.edit_message_text(f"💳 فيزتك: `{num}`\nالحد: {user['credit_limit']:,}", reply_markup=bank_kb(), parse_mode="Markdown")
            else: await q.edit_message_text(f"💳 فيزتك: {user['credit_card']}\nالحد: {user['credit_limit']:,}\nالمستخدم: {user['credit_used']:,}", reply_markup=bank_kb()); return
        if d == "loan":
            if user["loan_left"]>0: await q.edit_message_text(f"💰 عليك: {user['loan_left']:,} - القسط: {user['loan_pay']:,}", reply_markup=bank_kb())
            else: states[uid]="loan_"; save(); await q.edit_message_text("💰 اكتب مبلغ القرض (اقصى 10,000):"); return
        if d == "loan_pay":
            if user["loan_left"]<=0: await q.edit_message_text("مفيش قرض ✅", reply_markup=bank_kb()); return
            if user["balance"]<user["loan_pay"]: await q.edit_message_text("فلوسك مش كفاية", reply_markup=bank_kb()); return
            user["balance"]-=user["loan_pay"]; user["loan_left"]-=user["loan_pay"]; user["loan_installments"]-=1
            if user["loan_left"]<=0: user["loan_left"]=0; user["loan_installments"]=0
            save(); await q.edit_message_text(f"✅ سددت قسط\nالمتبقي: {user['loan_left']:,}", reply_markup=bank_kb()); return
        if d == "cert": states[uid]="cert_"; save(); await q.edit_message_text("📄 اكتب مبلغ الشهادة:"); return
        if d == "dep_money": states[uid]="dep_money_"; save(); await q.edit_message_text("🏦 اكتب مبلغ الوديعة:"); return
        if d == "bills":
            b=user["bills"]; total=b["electric"]+b["water"]+b["internet"]
            if total==0: b["electric"]=random.randint(50,200); b["water"]=random.randint(30,100); b["internet"]=random.randint(100,300); save(); total=b["electric"]+b["water"]+b["internet"]
            await q.edit_message_text(f"🧾 **فواتيرك:**\n⚡ {b['electric']:,} | 💧 {b['water']:,} | 🌐 {b['internet']:,}\nالاجمالي: {total:,}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💳 ادفع", callback_data="bills_pay")],[InlineKeyboardButton("🔙 رجوع", callback_data="bank")]])); return
        if d == "bills_pay":
            b=user["bills"]; total=b["electric"]+b["water"]+b["internet"]
            if user["balance"]<total: await q.edit_message_text("فلوسك مش كفاية", reply_markup=bank_kb()); return
            user["balance"]-=total; user["bills"]={"electric":0,"water":0,"internet":0}; save(); await q.edit_message_text(f"✅ دفعت {total:,}", reply_markup=bank_kb()); return
        if d == "statement": await q.edit_message_text(f"📜 **كشف حساب:**\n\n" + ("\n".join(user["transactions"][:10]) or "مفيش معاملات"), reply_markup=bank_kb(), parse_mode="Markdown"); return
        if d == "daily":
            today=datetime.now().strftime("%Y-%m-%d")
            if user["daily_last"]==today: await q.edit_message_text("خدت هديتك النهاردة", reply_markup=main_kb(uid)); return
            r=random.randint(100,500)*(2 if user["vip"] else 1); user["balance"]+=r; user["daily_last"]=today; user["coins"]+=1; save(); await q.edit_message_text(f"🎁 خدت {r:,} + 1 كوين!", reply_markup=main_kb(uid)); return
        if d == "top":
            s=sorted(users.values(), key=lambda x: x["balance"]+x["bank"]+x["savings"], reverse=True)[:10]; txt="🏆 **اغنى 10:**\n\n"
            for i,u in enumerate(s,1): txt+=f"{i}. @{u['username'] or u['id']} - {u['balance']+u['bank']+u['savings']:,} ج\n"
            await q.edit_message_text(txt, reply_markup=main_kb(uid), parse_mode="Markdown"); return

        # ===== دعم محسن =====
        if d == "support":
            await q.edit_message_text(f"🎧 **خدمة عملاء احترافية**\n\n👤 Mr cat - {status_emoji()}\n📱 @{MR_CAT_USERNAME}\n📞 {MR_CAT_PHONE}\n\n📊 تقييم Mr cat: ⭐ {round(data.get('agent_stats',{}).get(str(MR_CAT_ID),{}).get('rating_sum',0)/max(1,data.get('agent_stats',{}).get(str(MR_CAT_ID),{}).get('rating_count',1)),1)}/5", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💬 شات مباشر", callback_data="live_start")],[InlineKeyboardButton("📞 اطلب مكالمة", callback_data="request_call")],[InlineKeyboardButton("📩 تيكت جديد", callback_data="new_ticket")],[InlineKeyboardButton("🔙 رجوع", callback_data="back")]]), parse_mode="Markdown"); return
        if d == "new_ticket": await q.edit_message_text("📩 **اختار تصنيف التيكت:**", reply_markup=category_kb()); return
        if d.startswith("cat_"):
            mp={"cat_charge":"شحن / فلوس","cat_bug":"مشكلة تقنية","cat_refund":"استرجاع","cat_suggest":"اقتراح","cat_general":"استفسار عام"}
            cat = mp.get(d, "عام"); data.setdefault("temp", {})[uid]={"category": cat}; states[uid]="waiting_ticket_text"; save()
            await q.edit_message_text(f"تمام اخترت: **{cat}**\n\nاكتب مشكلتك بالتفصيل في رسالة واحدة + ممكن تبعت صورة / فويس:", parse_mode="Markdown"); return
        if d.startswith("pri_"):
            mp={"pri_normal":"عادي 🟢","pri_important":"مهم 🟡","pri_urgent":"مستعجل 🔴"}
            pri = mp.get(d, "عادي"); temp = data.get("temp", {}).get(uid, {}); cat = temp.get("category","عام"); text = temp.get("text","")
            states.pop(uid); data["ticket_counter"]+=1; tid=str(data["ticket_counter"])
            tickets[tid]={"id": tid, "user_id": uid, "username": q.from_user.username or "", "text": text, "category": cat, "priority": pri, "status": "open", "created": datetime.now().strftime("%d/%m %H:%M"), "created_full": datetime.now().strftime("%Y-%m-%d %H:%M"), "reply": ""}; save()
            user["tickets_count"]=user.get("tickets_count",0)+1; save()
            await q.edit_message_text(f"✅ عملت تيكت #{tid}\n\n🏷️ التصنيف: {cat}\n⚡ الاولوية: {pri}\n📝 {text[:60]}\n\nMr cat هيرد عليك قريب 🎧", reply_markup=main_kb(uid))
            emoji = "🔴🔴🔴" if "مستعجل" in pri else "🟡" if "مهم" in pri else "🟢"
            for sid in SUPPORT_IDS:
                try: await context.bot.send_message(chat_id=sid, text=f"{emoji} **تيكت جديد #{tid} - {pri}**\n🏷️ {cat}\nمن: @{q.from_user.username or uid} - `{uid}`\n\n{text}\n\n`/reply {tid} الرد`\nللرد الجاهز دوس هنا 👇", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💬 ردود جاهزة", callback_data=f"canned_menu_{uid}")],[InlineKeyboardButton("✅ اقفل", callback_data=f"close_ticket_{tid}")]]))
                except: pass
            return
        if d.startswith("close_ticket_"):
            if int(uid) not in SUPPORT_IDS: return
            tid = d.replace("close_ticket_","")
            if tid in tickets: tickets[tid]["status"]="closed"; save(); await q.edit_message_text(f"✅ قفلت #{tid}", reply_markup=support_kb())
            return
        if d.startswith("canned_menu_"):
            target = d.replace("canned_menu_","")
            await q.edit_message_text("💬 **اختار رد جاهز:**", reply_markup=canned_kb(target)); return
        if d.startswith("canned_"):
            if int(uid) not in SUPPORT_IDS: return
            parts = d.split("_"); key = parts[1]; target = parts[2]
            txt = CANNED.get(key, "")
            try: await context.bot.send_message(chat_id=int(target), text=f"💬 **Mr cat:**\n\n{txt}", reply_markup=main_kb(int(target)))
            except: pass
            await q.edit_message_text(f"✅ بعت رد جاهز: {txt[:30]}...", reply_markup=support_kb()); return
        if d == "canned_list":
            if int(uid) not in SUPPORT_IDS: return
            txt = "💬 **الردود الجاهزة:**\n\n"
            for k,v in CANNED.items(): txt+=f"• {k}: {v[:40]}...\n"
            await q.edit_message_text(txt, reply_markup=support_kb()); return
        if d == "support_urgent":
            if int(uid) not in SUPPORT_IDS: return
            urg = [t for t in tickets.values() if t["status"]=="open" and "مستعجل" in t.get("priority","")]
            if not urg: await q.edit_message_text("مفيش تيكتات مستعجلة ✅", reply_markup=support_kb()); return
            txt="🔴 **تيكتات مستعجلة:**\n\n"
            for t in urg: txt+=f"#{t['id']} - {t['category']} - @{t['username']} - {t['text'][:40]}\n`/reply {t['id']} الرد`\n\n"
            await q.edit_message_text(txt, reply_markup=support_kb(), parse_mode="Markdown"); return

        if d == "request_call": states[uid]="waiting_name"; save(); await q.edit_message_text("📞 **طلب مكالمة**\nاكتب اسمك:"); return
        if d == "live_start":
            if data.get("operator_status")=="offline": await q.edit_message_text("🔴 Mr cat اوفلاين.\nاعمل تيكت او اطلب مكالمة.", reply_markup=main_kb(uid)); return
            if uid in live_chats: await q.edit_message_text("انت في شات مباشر already 💬", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⏹️ انهاء", callback_data="live_end")]])); return
            if data.get("operator_status")=="busy":
                if uid not in data["queue"]: data["queue"].append(uid); save()
                pos=data["queue"].index(uid)+1; await q.edit_message_text(f"🟡 Mr cat مشغول.\n⏳ رقمك: {pos}", reply_markup=main_kb(uid)); return
            live_chats[uid]={"started": datetime.now().strftime("%H:%M"), "username": q.from_user.username or ""}; save()
            await q.edit_message_text("💬 **انت في شات مباشر مع Mr cat** 🟢\nابعت نص / صورة / فويس", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⏹️ انهاء", callback_data="live_end")]]))
            for sid in SUPPORT_IDS:
                try: await context.bot.send_message(chat_id=sid, text=f"🔴 **عميل دخل شات مباشر!**\nمن: @{q.from_user.username or uid} - `{uid}`\n\n`/chat {uid} ردك`", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💬 ردود جاهزة", callback_data=f"canned_menu_{uid}")]]))
                except: pass
            return
        if d == "live_end":
            if uid in live_chats: del live_chats[uid]; save()
            if uid in data.get("queue", []): data["queue"].remove(uid); save()
            await q.edit_message_text("⏹️ انهيت المحادثة 💙\n⭐ قيمنا بقى", reply_markup=main_kb(uid))
            for sid in SUPPORT_IDS:
                try: await context.bot.send_message(chat_id=sid, text=f"⏹️ العميل `{uid}` انهى الشات")
                except: pass
            return
        if d == "my_tickets":
            my=[t for t in tickets.values() if t["user_id"]==uid]
            if not my: await q.edit_message_text("مفيش تيكتات", reply_markup=main_kb(uid)); return
            txt="📋 **تيكتاتك (ارشيف):**\n\n"
            for t in my[-8:]:
                emoji="🟢" if t["status"]=="open" else "🟡" if t["status"]=="replied" else "⚫"
                txt+=f"{emoji} #{t['id']} - {t.get('category','عام')} - {t.get('priority','عادي')}\n{t['text'][:45]}\n"
                if t.get("reply"): txt+=f"↩️ {t['reply'][:45]}\n"
                txt+="\n"
            await q.edit_message_text(txt, reply_markup=main_kb(uid), parse_mode="Markdown"); return
        if d == "faq": await q.edit_message_text("❓ **اسئلة شائعة:**\n\n💰 الشحن: كلم Mr cat\n⏰ المواعيد: 10ص - 12م\n🔄 الاسترجاع: اعمل تيكت\n📦 الشحن: 5-30 دقيقة\n🏦 البنك: دوس بنك من القايمة", reply_markup=main_kb(uid)); return
        if d == "rate": states[uid]="waiting_rate"; save(); await q.edit_message_text("⭐ **قيم Mr cat من 1 لـ 5:**\nابعت رقم:"); return
        if d == "support_panel":
            if int(uid) not in SUPPORT_IDS: return
            open_t=len([t for t in tickets.values() if t["status"]=="open"]); urg=len([t for t in tickets.values() if t["status"]=="open" and "مستعجل" in t.get("priority","")])
            await q.edit_message_text(f"🎧 **لوحة الدعم الاحترافية**\n\nحالتك: {status_emoji()}\n💬 شات: {len(live_chats)}\n🔴 مستعجل: {urg}\n⏳ طابور: {len(data.get('queue',[]))}\n📞 مكالمات: {len([c for c in data.get('callbacks',[]) if not c['done']])}\n📩 مفتوحة: {open_t}", reply_markup=support_kb(), parse_mode="Markdown"); return
        if d == "live_active":
            if int(uid) not in SUPPORT_IDS: return
            if not live_chats: await q.edit_message_text("مفيش شاتات", reply_markup=support_kb()); return
            txt="💬 **شاتات:**\n\n"
            for cid,info in live_chats.items(): txt+=f"@{info['username']} - `{cid}`\n`/chat {cid} ردك`\n\n"
            await q.edit_message_text(txt, reply_markup=support_kb(), parse_mode="Markdown"); return
        if d == "queue_list":
            if int(uid) not in SUPPORT_IDS: return
            qlist=data.get("queue",[])
            if not qlist: await q.edit_message_text("الطابور فاضي ✅", reply_markup=support_kb()); return
            txt="⏳ **طابور:**\n\n"
            for i,cid in enumerate(qlist,1): txt+=f"{i}. `{cid}`\n"
            await q.edit_message_text(txt, reply_markup=support_kb(), parse_mode="Markdown"); return
        if d == "callback_list":
            if int(uid) not in SUPPORT_IDS: return
            cbs=[c for c in data.get("callbacks",[]) if not c["done"]]
            if not cbs: await q.edit_message_text("مفيش طلبات", reply_markup=support_kb()); return
            txt="📞 **طلبات مكالمات:**\n\n"
            for c in cbs[-10:]: txt+=f"👤 {c['name']} - {c['phone']} - `{c['user_id']}`\n"
            await q.edit_message_text(txt, reply_markup=support_kb(), parse_mode="Markdown"); return
        if d == "support_open":
            if int(uid) not in SUPPORT_IDS: return
            open_t=[t for t in tickets.values() if t["status"]=="open"]
            if not open_t: await q.edit_message_text("مفيش تيكتات ✅", reply_markup=support_kb()); return
            txt="📋 **تيكتات مفتوحة:**\n\n"
            for t in open_t[-10:]: txt+=f"#{t['id']} - {t.get('category','عام')} - {t.get('priority','عادي')} - @{t['username']}\n{t['text'][:40]}\n`/reply {t['id']} الرد`\n\n"
            await q.edit_message_text(txt, reply_markup=support_kb(), parse_mode="Markdown"); return
        if d == "support_stats":
            if int(uid) not in SUPPORT_IDS: return
            open_t=len([t for t in tickets.values() if t["status"]=="open"]); closed_t=len([t for t in tickets.values() if t["status"]=="closed"])
            stats=data.get("agent_stats",{}).get(str(MR_CAT_ID),{})
            avg=stats.get("rating_sum",0)/max(1,stats.get("rating_count",1)) if stats.get("rating_count") else 0
            await q.edit_message_text(f"📊 **احصائيات + اداء Mr cat**\n\n👥 يوزرز: {len(users)}\n💬 شات: {len(live_chats)}\n📩 مفتوحة: {open_t}\n✅ مقفولة: {closed_t}\n\n👤 **Mr cat:**\n💬 رد على: {stats.get('replied',0)} تيكت\n✅ قفل: {stats.get('closed',0)} تيكت\n💬 شاتات: {stats.get('chats',0)}\n⭐ تقييم: {avg:.1f}/5 من {stats.get('rating_count',0)} تقييم", reply_markup=support_kb(), parse_mode="Markdown"); return
        if d == "change_status":
            if int(uid) not in SUPPORT_IDS: return
            await q.edit_message_text("غير حالتك:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🟢 اونلاين", callback_data="set_online")],[InlineKeyboardButton("🟡 مشغول", callback_data="set_busy")],[InlineKeyboardButton("🔴 اوفلاين", callback_data="set_offline")],[InlineKeyboardButton("🔙 رجوع", callback_data="back")]])); return
        if d in ["set_online","set_busy","set_offline"]:
            if int(uid) not in SUPPORT_IDS: return
            mp={"set_online":"online","set_busy":"busy","set_offline":"offline"}; data["operator_status"]=mp[d]; save(); await q.edit_message_text(f"✅ حالتك: {mp[d]}", reply_markup=main_kb(uid)); return
        if d == "owner":
            if str(uid)!=str(OWNER_ID): return
            await q.edit_message_text("👑 **الاونر:**\n\n`/addmoney ID المبلغ`\n`/ban ID`\n`/unban ID`\n`/vip ID`\n`/reply 101 الرد`\n`/chat ID رسالة`\n`/close 101`\n`/status online`", reply_markup=main_kb(uid), parse_mode="Markdown"); return
    except Exception as e:
        print(f"BUTTON ERROR: {e}"); traceback.print_exc()
        try: await q.edit_message_text("حصلت مشكلة، دوس /start تاني")
        except: pass

async def error_handler(update, context):
    print(f"ERROR: {context.error}"); traceback.print_exc()

def main():
    if not TOKEN:
        print("❌ BOT_TOKEN مش موجود!"); 
        while True: time.sleep(60)
    while True:
        try:
            print("🚀 STARTING BOT ULTRA SUPPORT...")
            app = ApplicationBuilder().token(TOKEN).build()
            app.add_handler(CommandHandler("start", start)); app.add_handler(CommandHandler("help", cmd_help)); app.add_handler(CommandHandler("balance", cmd_balance)); app.add_handler(CommandHandler("daily", cmd_daily)); app.add_handler(CommandHandler("top", cmd_top))
            app.add_handler(CommandHandler("reply", cmd_reply)); app.add_handler(CommandHandler("close", cmd_close)); app.add_handler(CommandHandler("chat", cmd_chat)); app.add_handler(CommandHandler("endchat", cmd_endchat)); app.add_handler(CommandHandler("status", cmd_status))
            app.add_handler(CommandHandler("addmoney", cmd_addmoney)); app.add_handler(CommandHandler("ban", cmd_ban)); app.add_handler(CommandHandler("unban", cmd_unban)); app.add_handler(CommandHandler("vip", cmd_vip))
            app.add_handler(CallbackQueryHandler(buttons))
            app.add_handler(MessageHandler((filters.TEXT | filters.PHOTO | filters.VOICE) & ~filters.COMMAND, on_msg))
            app.add_error_handler(error_handler)
            print("✅ BOT STARTED"); app.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)
        except Exception as e: print(f"❌ CRASH: {e}"); time.sleep(3)
if __name__ == "__main__": main()
