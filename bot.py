import os, json, random, time, threading, requests, traceback, re
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from flask import Flask

TOKEN = os.environ.get("BOT_TOKEN", "").strip()
OWNER_ID = 8188263997
MR_CAT_ID = 7125945857
MR_CAT_USERNAME = "cat_max_10"
MR_CAT_PHONE = "+201155973454"
MR_CAT_WHATSAPP = "201155973454"
DATA_FILE = "data.json"
SUPPORT_IDS = [OWNER_ID, MR_CAT_ID]

# ===== تحميل الداتا - لو بايظة امسحها وابدأ جديد =====
def load():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            d = json.load(f)
            if not isinstance(d, dict): raise ValueError("bad data")
            for k, v in {"users": {}, "tickets": {}, "ticket_counter": 100, "states": {}, "ratings": [], "live_chats": {}, "queue": [], "callbacks": [], "operator_status": "online", "operator_msg": "", "temp": {}}.items():
                d.setdefault(k, v)
            # امسح اي حالات عالقة قديمة - دي اللي كانت بتبوظ الشات
            d["states"] = {}
            d["temp"] = {}
            return d
    except Exception as e:
        print(f"LOAD RESET - OLD DATA CORRUPTED: {e}")
        return {"users": {}, "tickets": {}, "ticket_counter": 100, "states": {}, "ratings": [], "live_chats": {}, "queue": [], "callbacks": [], "operator_status": "online", "operator_msg": "", "temp": {}}
def save():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e: print(f"SAVE ERR: {e}")
data = load(); users = data["users"]; tickets = data["tickets"]; states = data["states"]; live_chats = data["live_chats"]

def get_user(uid, username=""):
    uid = str(uid)
    if uid not in users:
        users[uid] = {"id": uid, "username": username, "balance": 1000, "bank": 0, "savings": 0, "loan_left": 0, "loan_pay": 0, "loan_installments": 0, "credit_card": None, "credit_limit": 0, "credit_used": 0, "vip": False, "banned": False, "daily_last": "", "transactions": [], "coins": 0, "level": 1, "xp": 0, "certificates": [], "deposits": [], "bills": {"electric": 0, "water": 0, "internet": 0}}
        save()
    return users[uid]

# ===== سيرفر =====
app_flask = Flask(__name__)
@app_flask.route('/')
def home(): return "BOT FIXED ALIVE ✅ " + datetime.now().strftime("%H:%M:%S")
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
threading.Thread(target=run_flask, daemon=True).start()
threading.Thread(target=self_ping, daemon=True).start()

# ===== اهم دالة - دي اللي كانت بتبوظ كل حاجة =====
async def safe_edit(q, text, reply_markup=None):
    # لو الرسالة هي هي تليجرام بيرفض الـ edit وبيهنج البوت
    # دلوقتي لو فشل الـ edit هنبعت رسالة جديدة ومش هنقول حاول مرة اخرى
    try:
        if q.message and q.message.text == text:
            # نفس الرسالة - متعملش edit
            return True
        await q.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")
        return True
    except Exception as e:
        err = str(e).lower()
        if "message is not modified" in err:
            return True  # مش غلطة اصلا - الرسالة هي هي
        if "message to edit not found" in err or "message can't be edited" in err:
            # الرسالة قديمة - ابعت جديدة
            try: await q.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")
            except:
                try: await q.message.reply_text(text, reply_markup=reply_markup)
                except: pass
            return True
        print(f"EDIT FAIL: {e}")
        try: await q.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")
        except:
            try: await q.message.reply_text(text, reply_markup=reply_markup)
            except: pass
        return True

async def safe_send(bot, chat_id, text, reply_markup=None):
    try:
        await bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup, parse_mode="Markdown")
        return True
    except Exception as e:
        print(f"SEND FAIL to {chat_id}: {e}")
        try: await bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
        except Exception as e2: print(f"SEND FAIL 2: {e2}")
        return False

def status_emoji():
    s = data.get("operator_status", "online")
    return "🟢 اونلاين" if s=="online" else "🟡 مشغول" if s=="busy" else "🔴 اوفلاين"

def user_kb(uid):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💬 شات مباشر مع Mr cat 🔴 اضغط هنا", callback_data="live_start")],
        [InlineKeyboardButton("📞 اطلب مكالمة", callback_data="request_call"), InlineKeyboardButton("💰 البنك", callback_data="bank")],
        [InlineKeyboardButton("💚 واتساب", url=f"https://wa.me/{MR_CAT_WHATSAPP}"), InlineKeyboardButton("✈️ تليجرام Mr cat", url=f"https://t.me/{MR_CAT_USERNAME}")],
        [InlineKeyboardButton("📩 تيكت جديد", callback_data="new_ticket"), InlineKeyboardButton("📋 تيكتاتي", callback_data="my_tickets")],
        [InlineKeyboardButton("🎁 هدية يومية", callback_data="daily"), InlineKeyboardButton("🏆 الاغنياء", callback_data="top")],
        [InlineKeyboardButton("❓ اسئلة شائعة", callback_data="faq"), InlineKeyboardButton("⭐ قيمنا", callback_data="rate")],
    ])
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
        [InlineKeyboardButton("🟢 اونلاين", callback_data="set_online"), InlineKeyboardButton("🟡 مشغول", callback_data="set_busy"), InlineKeyboardButton("🔴 اوفلاين", callback_data="set_offline")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="back")],
    ])
def live_kb():
    return InlineKeyboardMarkup([[InlineKeyboardButton("⏹️ انهاء الشات", callback_data="live_end")]])

# ===== START - بيمسح اي حالة عالقة =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        u = update.effective_user; uid = str(u.id)
        # امسح اي حالة عالقة - ده اللي كان بيخلي البوت يقول حاول مرة اخرى
        if uid in states: states.pop(uid)
        if uid in data.get("temp", {}): data["temp"].pop(uid)
        save()
        if int(uid) == MR_CAT_ID:
            open_t = len([t for t in tickets.values() if t["status"]=="open"])
            await update.message.reply_text(f"🎧 **لوحة Mr cat - دعم بس** 👑\n\nحالتك: {status_emoji()}\n💬 شات مباشر: {len(live_chats)}\n📩 مفتوحة: {open_t}\n📊 اجمالي: {len(tickets)}\n\n**اوامرك:**\n`/reply 101 الرد`\n`/chat ID ردك`\n`/close 101`\n`/endchat ID`", reply_markup=support_kb(), parse_mode="Markdown")
            return
        user = get_user(uid, u.username or "")
        if user["banned"]: await update.message.reply_text("🚫 انت محظور"); return
        txt = f"🏦🎧 **TRAN - بنك + دعم** 👑\nاهلا {u.first_name} 💙\n\n💰 كاش: {user['balance']:,} | 🏦 بنك: {user['bank']:,}\n👤 **Mr cat** - {status_emoji()}\n📞 {MR_CAT_PHONE}\n🎫 ID: `{uid}`\n\nاختار 👇"
        if data.get("operator_msg"): txt += f"\n\n📢 {data['operator_msg']}"
        await update.message.reply_text(txt, reply_markup=user_kb(uid), parse_mode="Markdown")
    except Exception as e:
        print(f"START ERR: {e}"); traceback.print_exc()
        try: await update.message.reply_text("اهلا بيك 👑 اكتب /start")
        except: pass

# ===== اوامر الدعم - شغالة 100% =====
async def cmd_reply(update, context):
    if update.effective_user.id not in SUPPORT_IDS: await update.message.reply_text("🚫 مش دعم"); return
    if len(context.args) < 2: await update.message.reply_text("اكتب: `/reply 101 الرد`", parse_mode="Markdown"); return
    tid = re.sub(r'[^0-9]', '', context.args[0]); txt = " ".join(context.args[1:])
    if tid not in tickets: await update.message.reply_text(f"مفيش تيكت #{tid}"); return
    tickets[tid]["status"]="replied"; tickets[tid]["reply"]=txt; save()
    await safe_send(context.bot, int(tickets[tid]["user_id"]), f"🎧 **Mr cat رد عليك:**\n\n{txt}")
    await update.message.reply_text(f"✅ رديت على #{tid}")
async def cmd_close(update, context):
    if update.effective_user.id not in SUPPORT_IDS: return
    if not context.args: await update.message.reply_text("`/close 101`"); return
    tid = re.sub(r'[^0-9]', '', context.args[0])
    if tid not in tickets: await update.message.reply_text(f"مفيش تيكت #{tid}"); return
    tickets[tid]["status"]="closed"; save()
    await safe_send(context.bot, int(tickets[tid]["user_id"]), f"✅ تيكت #{tid} اتقفل 💙")
    await update.message.reply_text(f"✅ قفلت #{tid}")

# ===== الشات المباشر - متصلح بالكامل =====
async def cmd_chat(update, context):
    # Mr cat يرد: /chat 123456 اهلا بيك
    if update.effective_user.id not in SUPPORT_IDS:
        await update.message.reply_text("🚫 انت مش دعم"); return
    if len(context.args) < 2:
        await update.message.reply_text("اكتب كده بالظبط:\n`/chat ID رسالتك`\nمثال:\n`/chat 123456789 اهلا بيك`", parse_mode="Markdown"); return
    uid_raw = context.args[0]
    uid = re.sub(r'[^0-9]', '', uid_raw)
    txt = " ".join(context.args[1:])
    print(f"MR CAT CHAT -> {uid}: {txt}")
    # لو العميل مش في شات مباشر، دخله فيه تلقائي
    if uid not in live_chats:
        live_chats[uid] = {"started": datetime.now().strftime("%H:%M"), "username": ""}; save()
        print(f"AUTO ADD LIVE CHAT {uid}")
    ok = await safe_send(context.bot, int(uid), f"💬 **Mr cat:**\n\n{txt}", reply_markup=live_kb())
    if ok: await update.message.reply_text(f"✅ وصلت لـ {uid}")
    else: await update.message.reply_text(f"❌ مش عارف ابعت لـ {uid}\nاتأكد انه بعت /start للبوت الاول")

async def cmd_endchat(update, context):
    if update.effective_user.id not in SUPPORT_IDS: return
    if not context.args: await update.message.reply_text("`/endchat ID`"); return
    uid = re.sub(r'[^0-9]', '', context.args[0])
    if uid in live_chats: del live_chats[uid]; save()
    await safe_send(context.bot, int(uid), "⏹️ Mr cat انهى المحادثة 💙\n⭐ قيمنا من البوت", reply_markup=user_kb(int(uid)))
    await update.message.reply_text(f"✅ انهيت شات {uid}")
async def cmd_status(update, context):
    if update.effective_user.id not in SUPPORT_IDS: return
    if not context.args: await update.message.reply_text("`/status online` / `busy` / `offline`"); return
    s = context.args[0].lower()
    if s in ["online","busy","offline"]: data["operator_status"]=s; save(); await update.message.reply_text(f"✅ حالتك بقت: {s}")
async def cmd_addmoney(update, context):
    if update.effective_user.id != OWNER_ID: return
    if len(context.args) < 2: return
    try: tid = re.sub(r'[^0-9]', '', context.args[0]); amt=int(context.args[1])
    except: return
    u = get_user(tid); u["balance"]+=amt; save(); await update.message.reply_text(f"✅ ضفت {amt:,} لـ {tid}")
async def cmd_ban(update, context):
    if update.effective_user.id != OWNER_ID: return
    if not context.args: return
    u = get_user(re.sub(r'[^0-9]', '', context.args[0])); u["banned"]=True; save(); await update.message.reply_text("🚫 حظرت")
async def cmd_unban(update, context):
    if update.effective_user.id != OWNER_ID: return
    if not context.args: return
    u = get_user(re.sub(r'[^0-9]', '', context.args[0])); u["banned"]=False; save(); await update.message.reply_text("✅ فكيت")
async def cmd_vip(update, context):
    if update.effective_user.id != OWNER_ID: return
    if not context.args: return
    u = get_user(re.sub(r'[^0-9]', '', context.args[0])); u["vip"]=True; u["credit_limit"]=20000; save(); await update.message.reply_text("👑 VIP")

# ===== استقبال الرسايل - الشات المباشر اول حاجة =====
async def on_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update.message: return
        uid = str(update.effective_user.id)
        print(f"MSG FROM {uid}: {update.message.text}")

        # Mr cat لو بعت رسالة عادية من غير /chat - فهمه
        if int(uid) == MR_CAT_ID:
            text = update.message.text or ""
            if text and not text.startswith("/"):
                await update.message.reply_text("🎧 يا Mr cat عشان ترد على عميل في شات مباشر اكتب:\n\n`/chat ID ردك`\n\nمثال:\n`/chat 123456789 اهلا بيك`\n\nاو شوف الشاتات النشطة من لوحتك 👇", reply_markup=support_kb(), parse_mode="Markdown")
            return

        user = get_user(uid, update.effective_user.username or "")
        if user["banned"]: return
        text = update.message.text or update.message.caption or ""
        if update.message.voice: text = "🎤 رسالة صوتية"
        if update.message.photo and not text: text = "🖼️ صورة"
        st = states.get(uid, "")

        # ===== 1 - الشات المباشر - لازم يكون اول حاجة قبل اي state =====
        if uid in live_chats:
            print(f"LIVE CHAT MSG {uid} -> SUPPORT")
            # ابعت لـ Mr cat والاونر
            for sid in SUPPORT_IDS:
                try:
                    if update.message.photo:
                        await context.bot.send_photo(chat_id=sid, photo=update.message.photo[-1].file_id, caption=f"💬 **شات مباشر**\nمن: @{update.effective_user.username or uid} - `{uid}`\n\n{update.message.caption or ''}\n\nللرد اكتب:\n`/chat {uid} ردك`", parse_mode="Markdown")
                    elif update.message.voice:
                        await context.bot.send_voice(chat_id=sid, voice=update.message.voice.file_id)
                        await context.bot.send_message(chat_id=sid, text=f"🎤 فويس من `{uid}`\n`/chat {uid} ردك`", parse_mode="Markdown")
                    else:
                        await context.bot.send_message(chat_id=sid, text=f"💬 **شات مباشر**\nمن: @{update.effective_user.username or uid} - `{uid}`\n\n{text}\n\nللرد اكتب:\n`/chat {uid} ردك`", parse_mode="Markdown")
                except Exception as e: print(f"LIVE FORWARD FAIL {sid}: {e}")
            # رد للعميل ان رسالته وصلت
            await update.message.reply_text("✅ وصلت لـ Mr cat... هيرد عليك حالا 👀", reply_markup=live_kb())
            return

        # ===== 2 - حالات البنك والتيكت =====
        if st == "transfer_":
            states.pop(uid); save()
            try: tid, amt = text.split(); amt=int(amt); tid=re.sub(r'[^0-9]', '', tid)
            except: await update.message.reply_text("اكتب صح: `ID المبلغ`", parse_mode="Markdown"); return
            if user["balance"] < amt: await update.message.reply_text("فلوسك مش كفاية"); return
            t = get_user(tid); user["balance"]-=amt; t["balance"]+=amt; save(); await update.message.reply_text(f"✅ حولت {amt:,} لـ {tid}"); return
        if st == "deposit_":
            states.pop(uid); save()
            try: amt=int(text)
            except: await update.message.reply_text("ابعت رقم بس"); return
            if user["balance"] < amt: await update.message.reply_text("فلوسك مش كفاية"); return
            user["balance"]-=amt; user["bank"]+=amt; save(); await update.message.reply_text(f"✅ اودعت {amt:,}"); return
        if st == "withdraw_":
            states.pop(uid); save()
            try: amt=int(text)
            except: await update.message.reply_text("ابعت رقم بس"); return
            if user["bank"] < amt: await update.message.reply_text("فلوس البنك مش كفاية"); return
            user["bank"]-=amt; user["balance"]+=amt; save(); await update.message.reply_text(f"✅ سحبت {amt:,}"); return
        if st == "savings_":
            states.pop(uid); save()
            try: amt=int(text)
            except: await update.message.reply_text("ابعت رقم بس"); return
            if user["balance"] < amt: await update.message.reply_text("فلوسك مش كفاية"); return
            user["balance"]-=amt; user["savings"]+=amt; save(); await update.message.reply_text(f"🐷 حوشت {amt:,}"); return
        if st == "loan_":
            states.pop(uid); save()
            try: amt=int(text)
            except: await update.message.reply_text("ابعت رقم بس"); return
            if user["loan_left"]>0: await update.message.reply_text("عليك قرض قديم"); return
            if amt>10000: await update.message.reply_text("اقصى 10,000"); return
            total=int(amt*1.2); pay=total//3; user["loan_left"]=total; user["loan_pay"]=pay; user["loan_installments"]=3; user["balance"]+=amt; save(); await update.message.reply_text(f"💰 خدت قرض {amt:,} - هتسدد {total:,} على 3 اقساط"); return
        if st == "cert_":
            states.pop(uid); save()
            try: amt=int(text)
            except: await update.message.reply_text("ابعت رقم بس"); return
            if user["balance"]<amt: await update.message.reply_text("فلوسك مش كفاية"); return
            user["balance"]-=amt; user["certificates"].append({"amount": amt}); save(); await update.message.reply_text(f"📄 عملت شهادة {amt:,}"); return
        if st == "dep_money_":
            states.pop(uid); save()
            try: amt=int(text)
            except: await update.message.reply_text("ابعت رقم بس"); return
            if user["balance"]<amt: await update.message.reply_text("فلوسك مش كفاية"); return
            user["balance"]-=amt; user["deposits"].append({"amount": amt}); save(); await update.message.reply_text(f"🏦 عملت وديعة {amt:,}"); return
        if st == "waiting_ticket":
            states.pop(uid); data["ticket_counter"]+=1; tid=str(data["ticket_counter"])
            tickets[tid]={"id": tid, "user_id": uid, "username": update.effective_user.username or "", "text": text, "status": "open", "created": datetime.now().strftime("%d/%m %H:%M"), "reply": ""}; save()
            await update.message.reply_text(f"✅ عملت تيكت #{tid}\nMr cat هيرد عليك قريب 🎧")
            for sid in SUPPORT_IDS:
                try: await context.bot.send_message(chat_id=sid, text=f"🎧 **تيكت جديد #{tid}**\nمن: @{update.effective_user.username or uid} - `{uid}`\n\n{text}\n\n`/reply {tid} الرد`", parse_mode="Markdown")
                except: pass
            return
        if st == "waiting_rate":
            states.pop(uid); save()
            try: rate=int(text)
            except: await update.message.reply_text("ابعت رقم 1-5"); return
            data["ratings"].append({"user": uid, "rate": rate}); save(); await update.message.reply_text(f"شكرا {rate} ⭐💙"); return
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
        if st == "waiting_status_msg":
            states.pop(uid); data["operator_msg"]=text; save(); await update.message.reply_text(f"✅ حطيت رسالة: {text}", reply_markup=support_kb()); return

        await update.message.reply_text("اكتب /start عشان القايمة 👑", reply_markup=user_kb(uid))
    except Exception as e:
        print(f"ON_MSG ERROR: {e}"); traceback.print_exc()
        # مش هنقول حاول مرة اخرى - هنقول /start بس
        try: await update.message.reply_text("اكتب /start 👑", reply_markup=user_kb(str(update.effective_user.id)))
        except: pass

# ===== زرار - كله safe_edit =====
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        q = update.callback_query; await q.answer(); uid = str(q.from_user.id); d = q.data
        print(f"BUTTON {uid}: {d}")
        # Mr cat لو دوست بنك بالغلط
        if int(uid) == MR_CAT_ID and d in ["bank","balance","transfer","deposit","withdraw","savings","visa","loan","loan_pay","cert","dep_money","bills","statement","daily","top"]:
            await safe_edit(q, "🎧 انت Mr cat - دعم بس 👑\nدي لوحتك:", reply_markup=support_kb()); return
        user = get_user(uid, q.from_user.username or "") if int(uid) != MR_CAT_ID else None

        if d == "back":
            if int(uid) == MR_CAT_ID: await safe_edit(q, "🎧 **لوحة Mr cat**", reply_markup=support_kb())
            elif int(uid) == OWNER_ID: await safe_edit(q, "👑 **الاونر**", reply_markup=support_kb())
            else: await safe_edit(q, f"🏦🎧 **TRAN**\n💰 كاش: {user['balance']:,} | 🏦 بنك: {user['bank']:,}", reply_markup=user_kb(uid))
            return
        if d == "bank": await safe_edit(q, "🏦 **البنك:**", reply_markup=bank_kb()); return
        if d == "balance": await safe_edit(q, f"💰 كاش: {user['balance']:,}\n🏦 بنك: {user['bank']:,}\n🐷 تحويش: {user['savings']:,}\n💳 فيزا: {user['credit_used']:,}/{user['credit_limit']:,}\n💰 قرض: {user['loan_left']:,}", reply_markup=bank_kb()); return
        if d == "transfer": states[uid]="transfer_"; save(); await safe_edit(q, "💸 ابعت: `ID المبلغ`"); return
        if d == "deposit": states[uid]="deposit_"; save(); await safe_edit(q, "🏦 اكتب المبلغ اللي هتودعه:"); return
        if d == "withdraw": states[uid]="withdraw_"; save(); await safe_edit(q, "🏧 اكتب المبلغ اللي هتسحبه:"); return
        if d == "savings": states[uid]="savings_"; save(); await safe_edit(q, f"🐷 تحويشك: {user['savings']:,}\nاكتب المبلغ:"); return
        if d == "visa":
            if not user["credit_card"]:
                num = f"4000 {random.randint(1000,9999)} {random.randint(1000,9999)} {random.randint(1000,9999)}"; user["credit_card"]=num; user["credit_limit"]=20000 if user["vip"] else 5000; save(); await safe_edit(q, f"💳 فيزتك: `{num}`\nالحد: {user['credit_limit']:,}", reply_markup=bank_kb())
            else: await safe_edit(q, f"💳 فيزتك: {user['credit_card']}\nالحد: {user['credit_limit']:,}", reply_markup=bank_kb())
            return
        if d == "loan":
            if user["loan_left"]>0: await safe_edit(q, f"💰 عليك: {user['loan_left']:,} - القسط: {user['loan_pay']:,}", reply_markup=bank_kb())
            else: states[uid]="loan_"; save(); await safe_edit(q, "💰 اكتب مبلغ القرض (اقصى 10,000):")
            return
        if d == "loan_pay":
            if user["loan_left"]<=0: await safe_edit(q, "مفيش قرض ✅", reply_markup=bank_kb()); return
            if user["balance"]<user["loan_pay"]: await safe_edit(q, "فلوسك مش كفاية", reply_markup=bank_kb()); return
            user["balance"]-=user["loan_pay"]; user["loan_left"]-=user["loan_pay"]; user["loan_installments"]-=1
            if user["loan_left"]<=0: user["loan_left"]=0; user["loan_installments"]=0
            save(); await safe_edit(q, f"✅ سددت قسط\nالمتبقي: {user['loan_left']:,}", reply_markup=bank_kb()); return
        if d == "cert": states[uid]="cert_"; save(); await safe_edit(q, "📄 اكتب مبلغ الشهادة:"); return
        if d == "dep_money": states[uid]="dep_money_"; save(); await safe_edit(q, "🏦 اكتب مبلغ الوديعة:"); return
        if d == "bills":
            b=user["bills"]; total=b["electric"]+b["water"]+b["internet"]
            if total==0: b["electric"]=random.randint(50,200); b["water"]=random.randint(30,100); b["internet"]=random.randint(100,300); save(); total=b["electric"]+b["water"]+b["internet"]
            await safe_edit(q, f"🧾 **فواتيرك:**\n⚡ {b['electric']:,} | 💧 {b['water']:,} | 🌐 {b['internet']:,}\nالاجمالي: {total:,}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💳 ادفع", callback_data="bills_pay")],[InlineKeyboardButton("🔙 رجوع", callback_data="bank")]])); return
        if d == "bills_pay":
            b=user["bills"]; total=b["electric"]+b["water"]+b["internet"]
            if user["balance"]<total: await safe_edit(q, "فلوسك مش كفاية", reply_markup=bank_kb()); return
            user["balance"]-=total; user["bills"]={"electric":0,"water":0,"internet":0}; save(); await safe_edit(q, f"✅ دفعت {total:,}", reply_markup=bank_kb()); return
        if d == "statement": await safe_edit(q, "📜 **كشف حساب:**\n" + ("\n".join(user["transactions"][:10]) or "مفيش معاملات"), reply_markup=bank_kb()); return
        if d == "daily":
            today=datetime.now().strftime("%Y-%m-%d")
            if user["daily_last"]==today: await safe_edit(q, "خدت هديتك النهاردة 🎁", reply_markup=user_kb(uid)); return
            r=random.randint(100,500)*(2 if user["vip"] else 1); user["balance"]+=r; user["daily_last"]=today; user["coins"]+=1; save(); await safe_edit(q, f"🎁 خدت {r:,} + 1 كوين!", reply_markup=user_kb(uid)); return
        if d == "top":
            s=sorted(users.values(), key=lambda x: x["balance"]+x["bank"]+x["savings"], reverse=True)[:10]; txt="🏆 **اغنى 10:**\n\n"
            for i,u in enumerate(s,1): txt+=f"{i}. @{u['username'] or u['id']} - {u['balance']+u['bank']+u['savings']:,} ج\n"
            await safe_edit(q, txt, reply_markup=user_kb(uid)); return
        if d == "request_call": states[uid]="waiting_name"; save(); await safe_edit(q, "📞 **طلب مكالمة**\nاكتب اسمك:"); return

        # ===== الشات المباشر - الجزء المهم =====
        if d == "live_start":
            print(f"LIVE START {uid} - status {data.get('operator_status')}")
            # امسح اي state قديم عشان الرسالة تروح للشات مش للتيكت
            if uid in states: states.pop(uid)
            if data.get("operator_status")=="offline":
                await safe_edit(q, "🔴 Mr cat اوفلاين دلوقتي.\nاعمل تيكت او اطلب مكالمة.", reply_markup=user_kb(uid)); return
            if uid in live_chats:
                await safe_edit(q, "انت already في شات مباشر 💬\nابعت رسالتك دلوقتي و Mr cat هيرد عليك.", reply_markup=live_kb()); return
            if data.get("operator_status")=="busy":
                if uid not in data["queue"]: data["queue"].append(uid); save()
                pos=data["queue"].index(uid)+1; await safe_edit(q, f"🟡 Mr cat مشغول.\n⏳ رقمك في الطابور: {pos}\nاول ما يفضى هيكلمك.", reply_markup=user_kb(uid)); return
            # دخله شات مباشر
            live_chats[uid]={"started": datetime.now().strftime("%H:%M"), "username": q.from_user.username or ""}; save()
            print(f"LIVE CHAT CREATED {uid} - total {len(live_chats)}")
            await safe_edit(q, "💬 **انت دلوقتي في شات مباشر مع Mr cat** 🟢\n\nابعت اي رسالة دلوقتي - نص / صورة / فويس - وهتوصله على طول.\n\nMr cat هيرد عليك هنا في نفس الشات.", reply_markup=live_kb())
            for sid in SUPPORT_IDS:
                try: await context.bot.send_message(chat_id=sid, text=f"🔴 **عميل دخل شات مباشر!**\nمن: @{q.from_user.username or uid} - `{uid}`\n\nعشان ترد اكتب:\n`/chat {uid} ردك`", parse_mode="Markdown")
                except Exception as e: print(f"LIVE NOTIFY FAIL {sid}: {e}")
            return
        if d == "live_end":
            if uid in live_chats: del live_chats[uid]; save()
            if uid in data.get("queue", []): data["queue"].remove(uid); save()
            await safe_edit(q, "⏹️ انهيت المحادثة 💙\n⭐ قيمنا بقى", reply_markup=user_kb(uid) if int(uid)!=MR_CAT_ID else support_kb())
            for sid in SUPPORT_IDS:
                try: await context.bot.send_message(chat_id=sid, text=f"⏹️ العميل `{uid}` انهى الشات")
                except: pass
            return
        if d == "live_active":
            if int(uid) not in SUPPORT_IDS: return
            if not live_chats: await safe_edit(q, "مفيش شاتات مباشرة دلوقتي ✅\nلما حد يدخل شات هيجيلك تنبيه هنا.", reply_markup=support_kb()); return
            txt="💬 **شاتات مباشرة نشطة:**\n\n"
            for cid,info in live_chats.items(): txt+=f"@{info.get('username','')} - `{cid}` - {info.get('started','')}\nللرد:\n`/chat {cid} ردك`\n\n"
            await safe_edit(q, txt, reply_markup=support_kb()); return

        if d == "new_ticket": states[uid]="waiting_ticket"; save(); await safe_edit(q, "📩 اكتب مشكلتك في رسالة واحدة:"); return
        if d == "my_tickets":
            my=[t for t in tickets.values() if t["user_id"]==uid]
            if not my: await safe_edit(q, "مفيش تيكتات", reply_markup=user_kb(uid)); return
            txt="📋 **تيكتاتك:**\n\n"
            for t in my[-5:]: txt+=f"#{t['id']} - {t['status']} - {t['text'][:50]}\n"
            await safe_edit(q, txt, reply_markup=user_kb(uid)); return
        if d == "faq": await safe_edit(q, "❓ **اسئلة شائعة:**\n\n💰 الشحن: كلم Mr cat\n⏰ المواعيد: 10ص - 12م\n🔄 الاسترجاع: اعمل تيكت\n📦 الشحن: 5-30 دقيقة", reply_markup=user_kb(uid)); return
        if d == "rate": states[uid]="waiting_rate"; save(); await safe_edit(q, "⭐ قيمنا 1-5 - ابعت رقم:"); return
        if d == "support_panel":
            if int(uid) not in SUPPORT_IDS: return
            open_t=len([t for t in tickets.values() if t["status"]=="open"])
            await safe_edit(q, f"🎧 **لوحة الدعم**\n\nحالتك: {status_emoji()}\n💬 شات: {len(live_chats)}\n📩 مفتوحة: {open_t}", reply_markup=support_kb(), parse_mode="Markdown"); return
        if d == "queue_list":
            if int(uid) not in SUPPORT_IDS: return
            qlist=data.get("queue",[])
            if not qlist: await safe_edit(q, "الطابور فاضي ✅", reply_markup=support_kb()); return
            txt="⏳ **طابور:**\n\n"
            for i,cid in enumerate(qlist,1): txt+=f"{i}. `{cid}`\n"
            await safe_edit(q, txt, reply_markup=support_kb()); return
        if d == "callback_list":
            if int(uid) not in SUPPORT_IDS: return
            cbs=[c for c in data.get("callbacks",[]) if not c["done"]]
            if not cbs: await safe_edit(q, "مفيش طلبات", reply_markup=support_kb()); return
            txt="📞 **طلبات مكالمات:**\n\n"
            for c in cbs[-10:]: txt+=f"👤 {c['name']} - {c['phone']} - `{c['user_id']}`\n"
            await safe_edit(q, txt, reply_markup=support_kb()); return
        if d == "support_open":
            if int(uid) not in SUPPORT_IDS: return
            open_t=[t for t in tickets.values() if t["status"]=="open"]
            if not open_t: await safe_edit(q, "مفيش تيكتات ✅", reply_markup=support_kb()); return
            txt="📋 **تيكتات:**\n\n"
            for t in open_t[-10:]: txt+=f"#{t['id']} - @{t['username']} - {t['text'][:50]}\n`/reply {t['id']} الرد`\n\n"
            await safe_edit(q, txt, reply_markup=support_kb()); return
        if d == "support_stats":
            if int(uid) not in SUPPORT_IDS: return
            open_t=len([t for t in tickets.values() if t["status"]=="open"]); closed_t=len([t for t in tickets.values() if t["status"]=="closed"])
            await safe_edit(q, f"📊 **احصائيات:**\n\n👥 يوزرز: {len(users)}\n💬 شات: {len(live_chats)}\n📩 مفتوحة: {open_t}\n✅ مقفولة: {closed_t}", reply_markup=support_kb(), parse_mode="Markdown"); return
        if d in ["set_online","set_busy","set_offline"]:
            if int(uid) not in SUPPORT_IDS: return
            mp={"set_online":"online","set_busy":"busy","set_offline":"offline"}; data["operator_status"]=mp[d]; save(); await safe_edit(q, f"✅ حالتك بقت: {mp[d]}", reply_markup=support_kb()); return
        if d == "set_msg":
            if int(uid) not in SUPPORT_IDS: return
            states[uid]="waiting_status_msg"; save(); await safe_edit(q, "📢 اكتب الرسالة اللي هتظهر للعملاء:"); return
    except Exception as e:
        print(f"BUTTON ERROR: {e}"); traceback.print_exc()
        # مش هنقول حاول مرة اخرى - هنبعت /start
        try: await q.message.reply_text("اكتب /start 👑")
        except: pass

async def error_handler(update, context):
    print(f"ERROR: {context.error}"); traceback.print_exc()

def main():
    if not TOKEN:
        print("❌ BOT_TOKEN مش موجود!"); 
        while True: time.sleep(60)
    while True:
        try:
            print("🚀 STARTING FIXED BOT...")
            app = ApplicationBuilder().token(TOKEN).build()
            app.add_handler(CommandHandler("start", start))
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
            app.add_handler(MessageHandler((filters.TEXT | filters.PHOTO | filters.VOICE) & ~filters.COMMAND, on_msg))
            app.add_error_handler(error_handler)
            print("✅ BOT STARTED - LIVE CHAT FIXED")
            app.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)
        except Exception as e: print(f"CRASH: {e}"); time.sleep(3)
if __name__ == "__main__": main()
