import os, json, time, threading, requests
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from flask import Flask

TOKEN = os.environ.get("BOT_TOKEN", "PUT_YOUR_TOKEN_HERE")
OWNER_ID = 8188263997
DATA_FILE = "data.json"

SUPPORT_IDS = [8188263997, 7125945857]
MR_CAT_ID = 7125945857
MR_CAT_USERNAME = "cat_max_10"
MR_CAT_PHONE = "+201155973454"
MR_CAT_WHATSAPP = "201155973454"

def load():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f: return json.load(f)
    except: return {"tickets": {}, "ticket_counter": 100, "states": {}, "ratings": [], "live_chats": {}, "queue": [], "callbacks": [], "operator_status": "online", "operator_msg": ""}
def save():
    with open(DATA_FILE, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=2)
data = load(); tickets = data["tickets"]; states = data["states"]; live_chats = data["live_chats"]

app_flask = Flask(__name__)
@app_flask.route('/')
def home(): return "KHEDMA ULTRA ALIVE ✅"
@app_flask.route('/health')
def health(): return "OK"
def run_flask():
    try: app_flask.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
    except: time.sleep(5); run_flask()
def self_ping():
    time.sleep(10); url = os.environ.get("RENDER_EXTERNAL_URL", "")
    if not url: return
    while True:
        try: requests.get(url, timeout=10)
        except: pass
        time.sleep(300)
threading.Thread(target=run_flask, daemon=True).start()
threading.Thread(target=self_ping, daemon=True).start()

def status_emoji():
    s = data.get("operator_status", "online")
    if s == "online": return "🟢 اونلاين - بيرد حالا"
    if s == "busy": return "🟡 مشغول - هتستنى شوية"
    return "🔴 اوفلاين - سيب رسالة وهنرد عليك"

def main_kb(uid):
    st = status_emoji()
    kb = [
        [InlineKeyboardButton(f"💬 شات مباشر - {st}", callback_data="live_start")],
        [InlineKeyboardButton("📞 اطلب مكالمة ☎️", callback_data="request_call"), InlineKeyboardButton("📞 اتصال مباشر", callback_data="call")],
        [InlineKeyboardButton("💚 واتساب", url=f"https://wa.me/{MR_CAT_WHATSAPP}"), InlineKeyboardButton("✈️ تليجرام Mr cat", url=f"https://t.me/{MR_CAT_USERNAME}")],
        [InlineKeyboardButton("📩 اعمل تيكت", callback_data="new_ticket"), InlineKeyboardButton("📋 تيكتاتي", callback_data="my_tickets")],
        [InlineKeyboardButton("❓ اسئلة شائعة", callback_data="faq"), InlineKeyboardButton("⭐ قيمنا", callback_data="rate")],
        [InlineKeyboardButton("⏳ مكاني في الطابور", callback_data="my_queue")],
    ]
    if int(uid) in SUPPORT_IDS:
        kb.append([InlineKeyboardButton("🎧 لوحة خدمة العملاء", callback_data="support_panel")])
        kb.append([InlineKeyboardButton("🟢/🟡/🔴 غير حالتي", callback_data="change_status")])
    return InlineKeyboardMarkup(kb)

def live_end_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⏹️ انهاء المحادثة", callback_data="live_end")],
        [InlineKeyboardButton("📞 اطلب مكالمة", callback_data="request_call")],
    ])

def support_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💬 شاتات مباشرة", callback_data="live_active")],
        [InlineKeyboardButton("⏳ طابور الانتظار", callback_data="queue_list")],
        [InlineKeyboardButton("📞 طلبات المكالمات", callback_data="callback_list")],
        [InlineKeyboardButton("📩 تيكتات مفتوحة", callback_data="support_open")],
        [InlineKeyboardButton("📊 احصائيات", callback_data="support_stats")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="back")],
    ])

def faq_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 ازاي اشحن؟", callback_data="faq_charge")],
        [InlineKeyboardButton("⏰ مواعيد العمل؟", callback_data="faq_time")],
        [InlineKeyboardButton("🔄 استرجاع؟", callback_data="faq_return")],
        [InlineKeyboardButton("📦 الشحن؟", callback_data="faq_shipping")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="back")],
    ])

async def start(update, context):
    u = update.effective_user
    txt = f"""🎧 **خدمة عملاء - اتصال مباشر** 👑
اهلا {u.first_name} 💙

👤 **Mr cat**
{status_emoji()}
📱 @{MR_CAT_USERNAME}
📞 {MR_CAT_PHONE}

لو Mr cat اونلاين دوس شات مباشر وهيرد عليك حالا 🔥
لو مشغول دوس اطلب مكالمة وهنكلمك.

🎫 ID: `{u.id}`"""
    if data.get("operator_msg"):
        txt += f"\n\n📢 **رسالة من Mr cat:**\n{data['operator_msg']}"
    await update.message.reply_text(txt, reply_markup=main_kb(u.id), parse_mode="Markdown")

# ===== اوامر الدعم =====
async def cmd_reply(update, context):
    if update.effective_user.id not in SUPPORT_IDS: return
    if len(context.args) < 2: await update.message.reply_text("`/reply 101 الرد`", parse_mode="Markdown"); return
    tid = context.args[0]; txt = " ".join(context.args[1:])
    if tid not in tickets: return
    tickets[tid]["status"] = "replied"; tickets[tid]["reply"] = txt; save()
    try: await context.bot.send_message(chat_id=int(tickets[tid]["user_id"]), text=f"🎧 **Mr cat رد عليك:**\n\n{txt}", parse_mode="Markdown")
    except: pass
    await update.message.reply_text(f"✅ رديت على #{tid}")
async def cmd_close(update, context):
    if update.effective_user.id not in SUPPORT_IDS: return
    if not context.args: return
    tid = context.args[0]
    if tid not in tickets: return
    tickets[tid]["status"] = "closed"; save()
    try: await context.bot.send_message(chat_id=int(tickets[tid]["user_id"]), text=f"✅ تيكت #{tid} اتقفل 💙")
    except: pass
    await update.message.reply_text(f"✅ قفلت #{tid}")
async def cmd_chat(update, context):
    if update.effective_user.id not in SUPPORT_IDS: return
    if len(context.args) < 2: await update.message.reply_text("`/chat ID رسالتك`", parse_mode="Markdown"); return
    uid = context.args[0]; txt = " ".join(context.args[1:])
    try:
        await context.bot.send_message(chat_id=int(uid), text=f"💬 **Mr cat:**\n\n{txt}", parse_mode="Markdown", reply_markup=live_end_kb())
        await update.message.reply_text(f"✅ بعت لـ {uid}")
    except: await update.message.reply_text("مش عارف ابعتله")
async def cmd_endchat(update, context):
    if update.effective_user.id not in SUPPORT_IDS: return
    if not context.args: return
    uid = context.args[0]
    if uid in live_chats: del live_chats[uid]; save()
    try: await context.bot.send_message(chat_id=int(uid), text="⏹️ Mr cat انهى المحادثة 💙", reply_markup=main_kb(int(uid)))
    except: pass
    await update.message.reply_text(f"✅ انهيت شات {uid}")
async def cmd_status(update, context):
    if update.effective_user.id not in SUPPORT_IDS: return
    if not context.args: await update.message.reply_text("`/status online` او `busy` او `offline`"); return
    s = context.args[0].lower()
    if s in ["online", "busy", "offline"]:
        data["operator_status"] = s; save(); await update.message.reply_text(f"✅ حالتك بقت {s}")
async def cmd_broadcast(update, context):
    # رسالة لكل الناس اللي كلموا البوت
    if update.effective_user.id != OWNER_ID: return
    if not context.args: await update.message.reply_text("`/broadcast الرسالة`"); return
    txt = " ".join(context.args)
    data["operator_msg"] = txt; save()
    await update.message.reply_text(f"✅ حطيت رسالة Mr cat: {txt}")

# ===== رسايل - نص + صوت + صورة =====
async def on_msg(update, context):
    uid = str(update.effective_user.id)
    # لو صورة او فويس من عميل في شات مباشر
    is_media = update.message.photo or update.message.voice or update.message.video_note
    text = update.message.text or update.message.caption or ""
    if update.message.voice: text = "🎤 بعت رسالة صوتية"
    if update.message.photo: text = f"🖼️ بعت صورة - {update.message.caption or 'بدون تعليق'}"
    st = states.get(uid, "")

    if uid in live_chats and int(uid) not in SUPPORT_IDS:
        for sid in SUPPORT_IDS:
            try:
                if update.message.photo:
                    await context.bot.send_photo(chat_id=sid, photo=update.message.photo[-1].file_id, caption=f"💬 **شات مباشر**\nمن: @{update.effective_user.username or uid} - `{uid}`\n\n{update.message.caption or ''}\n\n`/chat {uid} ردك`", parse_mode="Markdown")
                elif update.message.voice:
                    await context.bot.send_voice(chat_id=sid, voice=update.message.voice.file_id, caption=f"💬 فويس من `{uid}` - `/chat {uid} ردك`")
                else:
                    await context.bot.send_message(chat_id=sid, text=f"💬 **شات مباشر**\nمن: @{update.effective_user.username or uid} - `{uid}`\n\n{text}\n\n`/chat {uid} ردك`", parse_mode="Markdown")
            except: pass
        await update.message.reply_text("✅ وصلت لـ Mr cat 👀", reply_markup=live_end_kb())
        return

    if st == "waiting_ticket":
        states.pop(uid); data["ticket_counter"] += 1; tid = str(data["ticket_counter"])
        tickets[tid] = {"id": tid, "user_id": uid, "username": update.effective_user.username or "", "text": text, "status": "open", "created": datetime.now().strftime("%d/%m %H:%M"), "reply": ""}; save()
        await update.message.reply_text(f"✅ عملت تيكت #{tid}\nMr cat هيرد عليك قريب 🎧")
        for sid in SUPPORT_IDS:
            try: await context.bot.send_message(chat_id=sid, text=f"🎧 **تيكت جديد #{tid}**\nمن: @{update.effective_user.username or uid} - `{uid}`\n\n{text}\n\n`/reply {tid} الرد`", parse_mode="Markdown")
            except: pass
        return
    if st == "waiting_rate":
        states.pop(uid)
        try: rate = int(text)
        except: await update.message.reply_text("ابعت رقم 1-5"); return
        data["ratings"].append({"user": uid, "rate": rate, "time": datetime.now().strftime("%d/%m")}); save()
        await update.message.reply_text(f"شكرا {rate} ⭐💙"); return
    if st == "waiting_name":
        states[uid] = "waiting_phone"; data.setdefault("temp", {})[uid] = {"name": text}; save()
        await update.message.reply_text("تمام يا " + text + " 👑\nاكتب رقم موبايلك:"); return
    if st == "waiting_phone":
        temp = data.get("temp", {}).get(uid, {})
        name = temp.get("name", "عميل")
        states.pop(uid)
        # سجل طلب مكالمة
        data["callbacks"].append({"user_id": uid, "username": update.effective_user.username or "", "name": name, "phone": text, "time": datetime.now().strftime("%d/%m %H:%M"), "done": False}); save()
        await update.message.reply_text(f"✅ تمام يا {name}!\nسجلنا طلب مكالمة على رقم {text}\nMr cat هيكلمك في اقرب وقت 📞\nرقمك في الطابور: {len(data['callbacks'])}")
        for sid in SUPPORT_IDS:
            try: await context.bot.send_message(chat_id=sid, text=f"📞 **طلب مكالمة جديد!**\n👤 الاسم: {name}\n📱 الرقم: {text}\n✈️ يوزر: @{update.effective_user.username or uid} - `{uid}`\n⏰ {data['callbacks'][-1]['time']}\n\nاتصل بيه على طول 👇\n`{text}`", parse_mode="Markdown")
            except: pass
        return
    if st == "waiting_status_msg":
        states.pop(uid); data["operator_msg"] = text; save(); await update.message.reply_text(f"✅ حطيت رسالة: {text}"); return
    # لو Mr cat اوفلاين والعميل بعت رسالة عادية - رد تلقائي
    if data.get("operator_status") == "offline" and int(uid) not in SUPPORT_IDS:
        await update.message.reply_text("🌙 Mr cat اوفلاين دلوقتي.\nسيب رسالتك هنا او اعمل تيكت وهنرد عليك اول ما نرجع 💙\nاو اطلب مكالمة وهنكلمك الصبح.", reply_markup=main_kb(uid))
        return
    await update.message.reply_text("اكتب /start 👑", reply_markup=main_kb(uid))

async def buttons(update, context):
    q = update.callback_query; await q.answer(); uid = str(q.from_user.id); d = q.data
    if d == "back": await q.edit_message_text("🎧 **خدمة عملاء** 👑\nاختار 👇", reply_markup=main_kb(uid), parse_mode="Markdown"); return
    if d == "call":
        await q.edit_message_text(f"📞 **اتصال مباشر**\n\n👤 Mr cat\n📞 `{MR_CAT_PHONE}`\n\nدوس على الرقم واتصل على طول\nاو اطلب مكالمة وهو هيكلمك.", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📞 اطلب مكالمة", callback_data="request_call")],
            [InlineKeyboardButton("💚 واتساب", url=f"https://wa.me/{MR_CAT_WHATSAPP}")],
            [InlineKeyboardButton("🔙 رجوع", callback_data="back")]
        ]), parse_mode="Markdown"); return
    if d == "request_call":
        states[uid] = "waiting_name"; save()
        await q.edit_message_text("📞 **طلب مكالمة**\n\nعشان Mr cat يكلمك، اكتب اسمك:"); return
    if d == "my_queue":
        qlist = data.get("queue", [])
        if uid not in qlist: await q.edit_message_text("انت مش في الطابور دلوقتي ✅", reply_markup=main_kb(uid)); return
        pos = qlist.index(uid) + 1
        await q.edit_message_text(f"⏳ **مكانك في الطابور: {pos}**\nقدامك {pos-1} واحد\nاستنى شوية Mr cat هيكلمك 💙", reply_markup=main_kb(uid)); return
    if d == "live_start":
        if data.get("operator_status") == "offline":
            await q.edit_message_text("🔴 Mr cat اوفلاين دلوقتي.\nاعمل تيكت او اطلب مكالمة وهنرد عليك الصبح 💙", reply_markup=main_kb(uid)); return
        if uid in live_chats: await q.edit_message_text("انت في شات مباشر already 💬\nابعت رسالتك.", reply_markup=live_end_kb()); return
        # لو مشغول دخل طابور
        if data.get("operator_status") == "busy":
            if uid not in data["queue"]: data["queue"].append(uid); save()
            pos = data["queue"].index(uid) + 1
            await q.edit_message_text(f"🟡 Mr cat مشغول دلوقتي.\n\n⏳ دخلت الطابور - رقمك: {pos}\nقدامك {pos-1} واحد\nاول ما يفضى هيكلمك على طول.", reply_markup=main_kb(uid)); return
        live_chats[uid] = {"started": datetime.now().strftime("%H:%M"), "username": q.from_user.username or ""}; save()
        await q.edit_message_text("💬 **انت في شات مباشر مع Mr cat** 🟢\n\nابعت نص / صورة / فويس - كله بيوصل.\nعشان تنهي دوس انهاء.", reply_markup=live_end_kb())
        for sid in SUPPORT_IDS:
            try: await context.bot.send_message(chat_id=sid, text=f"🔴 **عميل دخل شات مباشر!**\nمن: @{q.from_user.username or uid} - `{uid}`\n\n`/chat {uid} ردك`\n`/endchat {uid}`", parse_mode="Markdown")
            except: pass
        return
    if d == "live_end":
        if uid in live_chats: del live_chats[uid]; save()
        if uid in data.get("queue", []): data["queue"].remove(uid); save()
        await q.edit_message_text("⏹️ انهيت المحادثة 💙\nقيمنا بقى ⭐", reply_markup=main_kb(uid))
        for sid in SUPPORT_IDS:
            try: await context.bot.send_message(chat_id=sid, text=f"⏹️ العميل `{uid}` انهى الشات")
            except: pass
        return
    if d == "change_status":
        if int(uid) not in SUPPORT_IDS: return
        await q.edit_message_text("غير حالتك:", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🟢 اونلاين", callback_data="set_online")],
            [InlineKeyboardButton("🟡 مشغول", callback_data="set_busy")],
            [InlineKeyboardButton("🔴 اوفلاين", callback_data="set_offline")],
            [InlineKeyboardButton("📢 حط رسالة للعملاء", callback_data="set_msg")],
            [InlineKeyboardButton("🔙 رجوع", callback_data="back")],
        ])); return
    if d in ["set_online", "set_busy", "set_offline"]:
        if int(uid) not in SUPPORT_IDS: return
        mp = {"set_online": "online", "set_busy": "busy", "set_offline": "offline"}
        data["operator_status"] = mp[d]; save()
        await q.edit_message_text(f"✅ حالتك بقت {mp[d]}", reply_markup=main_kb(uid)); return
    if d == "set_msg":
        states[uid] = "waiting_status_msg"; save(); await q.edit_message_text("اكتب الرسالة اللي هتظهر لكل العملاء:"); return
    if d == "new_ticket": states[uid] = "waiting_ticket"; save(); await q.edit_message_text("📩 اكتب مشكلتك في رسالة واحدة:"); return
    if d == "my_tickets":
        my = [t for t in tickets.values() if t["user_id"] == uid]
        if not my: await q.edit_message_text("مفيش تيكتات", reply_markup=main_kb(uid)); return
        txt = "📋 **تيكتاتك:**\n\n"
        for t in my[-5:]: txt += f"#{t['id']} - {t['status']} - {t['text'][:50]}\n"
        await q.edit_message_text(txt, reply_markup=main_kb(uid), parse_mode="Markdown"); return
    if d == "faq": await q.edit_message_text("❓ **اسئلة شائعة:**", reply_markup=faq_kb()); return
    if d == "faq_charge": await q.edit_message_text("💰 كلم Mr cat @cat_max_10", reply_markup=faq_kb()); return
    if d == "faq_time": await q.edit_message_text("⏰ من 10 الصبح لـ 12 بالليل", reply_markup=faq_kb()); return
    if d == "faq_return": await q.edit_message_text("🔄 اعمل تيكت وهنحلها", reply_markup=faq_kb()); return
    if d == "faq_shipping": await q.edit_message_text("📦 من 5 لـ 30 دقيقة", reply_markup=faq_kb()); return
    if d == "rate": states[uid] = "waiting_rate"; save(); await q.edit_message_text("⭐ قيمنا 1-5:"); return
    if d == "support_panel":
        if int(uid) not in SUPPORT_IDS: return
        open_t = len([t for t in tickets.values() if t["status"] == "open"])
        await q.edit_message_text(f"🎧 **لوحة خدمة العملاء**\n\nحالتك: {status_emoji()}\n💬 شات مباشر: {len(live_chats)}\n⏳ طابور: {len(data.get('queue',[]))}\n📞 طلبات مكالمات: {len([c for c in data.get('callbacks',[]) if not c['done']])}\n📩 تيكتات مفتوحة: {open_t}", reply_markup=support_kb(), parse_mode="Markdown"); return
    if d == "live_active":
        if int(uid) not in SUPPORT_IDS: return
        if not live_chats: await q.edit_message_text("مفيش شاتات", reply_markup=support_kb()); return
        txt = "💬 **شاتات نشطة:**\n\n"
        for cid, info in live_chats.items(): txt += f"@{info['username']} - `{cid}`\n`/chat {cid} ردك`\n\n"
        await q.edit_message_text(txt, reply_markup=support_kb(), parse_mode="Markdown"); return
    if d == "queue_list":
        if int(uid) not in SUPPORT_IDS: return
        qlist = data.get("queue", [])
        if not qlist: await q.edit_message_text("الطابور فاضي ✅", reply_markup=support_kb()); return
        txt = "⏳ **طابور:**\n\n"
        for i, cid in enumerate(qlist, 1): txt += f"{i}. `{cid}` - `/chat {cid} اهلا`\n"
        await q.edit_message_text(txt, reply_markup=support_kb(), parse_mode="Markdown"); return
    if d == "callback_list":
        if int(uid) not in SUPPORT_IDS: return
        cbs = [c for c in data.get("callbacks", []) if not c["done"]]
        if not cbs: await q.edit_message_text("مفيش طلبات مكالمات", reply_markup=support_kb()); return
        txt = "📞 **طلبات مكالمات:**\n\n"
        for c in cbs[-10:]: txt += f"👤 {c['name']} - {c['phone']} - `{c['user_id']}` - {c['time']}\n"
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
        await q.edit_message_text(f"📊 **احصائيات:**\n\n💬 شات: {len(live_chats)}\n⏳ طابور: {len(data.get('queue',[]))}\n📞 مكالمات: {len(data.get('callbacks',[]))}\n📩 مفتوحة: {open_t}\n✅ مقفولة: {closed_t}\n⭐ تقييم: {avg:.1f}/5", reply_markup=support_kb(), parse_mode="Markdown"); return

def main():
    while True:
        try:
            app = ApplicationBuilder().token(TOKEN).build()
            app.add_handler(CommandHandler("start", start))
            app.add_handler(CommandHandler("reply", cmd_reply))
            app.add_handler(CommandHandler("close", cmd_close))
            app.add_handler(CommandHandler("chat", cmd_chat))
            app.add_handler(CommandHandler("endchat", cmd_endchat))
            app.add_handler(CommandHandler("status", cmd_status))
            app.add_handler(CommandHandler("broadcast", cmd_broadcast))
            app.add_handler(CallbackQueryHandler(buttons))
            app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO | filters.VOICE & ~filters.COMMAND, on_msg))
            print("KHEDMA ULTRA STARTED ✅"); app.run_polling(drop_pending_updates=True)
        except Exception as e: print(f"CRASH: {e}"); time.sleep(5)
if __name__ == "__main__": main()
