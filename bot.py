import os, json, random, time, threading, requests, traceback, re
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from flask import Flask

TOKEN = os.environ.get("BOT_TOKEN", "").strip()
KING_ID = 8188263997
MR_CAT_ID = 7125945857
MR_CAT_USERNAME = "cat_max_10"
MR_CAT_WHATSAPP = "201155973454"
DATA_FILE = "data.json"
SUPPORT_IDS = [KING_ID, MR_CAT_ID]

# ===== رتب المملكة السعودية =====
RANKS = {
 "king": {"name": "👑 الملك", "power": 100},
 "crown": {"name": "🤴 ولي العهد", "power": 95},
 "princess": {"name": "👸 الأميرة", "power": 90},
 "diwan": {"name": "🎩 رئيس الديوان", "power": 85},
 "prince": {"name": "👑 أمير منطقة", "power": 80},
 "sheikh": {"name": "💎 شيخ قبيلة", "power": 70},
 "general": {"name": "🛡️ قائد الجيش", "power": 65},
 "police": {"name": "👮 مدير الشرطة", "power": 60},
 "minister": {"name": "💰 وزير", "power": 55},
 "trader": {"name": "💰 تاجر كبير", "power": 45},
 "citizen": {"name": "🇸🇦 مواطن سعودي", "power": 25},
 "resident": {"name": "🧑 مقيم", "power": 15},
 "slave": {"name": "⛓️ عبد", "power": 5},
}
RANK_ORDER = ["slave","resident","citizen","trader","minister","police","general","sheikh","prince","diwan","princess","crown","king"]
REGIONS = {"riyadh": "🏰 الرياض", "makkah": "🕌 مكة", "madina": "🕌 المدينة", "jeddah": "🌊 جدة", "dammam": "🛢️ الدمام", "qassim": "🌴 القصيم", "abha": "🏔️ أبها"}

def load():
    try:
        with open(DATA_FILE,"r",encoding="utf-8") as f:
            d=json.load(f)
            for k,v in {"users":{},"tickets":{},"ticket_counter":100,"states":{},"ratings":[],"live_chats":{},"queue":[],"callbacks":[],"operator_status":"online","temp":{},"kingdom":{"law":"الملك هو القانون 👑🇸🇦","treasury":0,"banned_count":0,"jizya":200,"zakat":2.5,"oil_price":80,"national_day":False},"courts":[],"reports":[],"shura":[]}.items(): d.setdefault(k,v)
            d["states"]={}; d["temp"]={}; return d
    except: return {"users":{},"tickets":{},"ticket_counter":100,"states":{},"ratings":[],"live_chats":{},"queue":[],"callbacks":[],"operator_status":"online","temp":{},"kingdom":{"law":"الملك هو القانون 👑🇸🇦","treasury":0,"banned_count":0,"jizya":200,"zakat":2.5,"oil_price":80,"national_day":False},"courts":[],"reports":[],"shura":[]}
def save():
    try:
        with open(DATA_FILE,"w",encoding="utf-8") as f: json.dump(data,f,ensure_ascii=False,indent=2)
    except: pass
data=load(); users=data["users"]; tickets=data["tickets"]; states=data["states"]; live_chats=data["live_chats"]

def get_user(uid,username=""):
    uid=str(uid)
    if uid not in users:
        rank="king" if uid==str(KING_ID) else "diwan" if uid==str(MR_CAT_ID) else "resident"
        users[uid]={"id":uid,"username":username,"rank":rank,"balance":1000,"bank":0,"savings":0,"loan_left":0,"loan_pay":0,"loan_installments":0,"credit_card":None,"credit_limit":5000,"credit_used":0,"vip":False,"banned":False,"ban_reason":"","daily_last":"","transactions":[],"coins":0,"level":1,"xp":0,"certificates":[],"deposits":[],"bills":{"electric":0,"water":0,"internet":0},"tribute_paid":"","warnings":0,"muted_until":0,"jailed_until":0,"region":"riyadh","has_id":False,"has_passport":False,"has_license":False,"citizenship":False,"house":"لا يوجد","car":"لا يوجد","oil_wells":0,"stocks":{"aramco":0,"neom":0,"bank":0},"shares":0,"visits":0,"hasanats":0,"married_to":"","warnings_count":0}
        save()
    if uid==str(KING_ID): users[uid]["rank"]="king"; users[uid]["banned"]=False
    if uid==str(MR_CAT_ID) and users[uid]["rank"]=="resident": users[uid]["rank"]="diwan"
    return users[uid]

# ===== سيرفر =====
app_flask=Flask(__name__)
@app_flask.route('/')
def home(): return "KINGDOM SAUDI ALIVE 👑🇸🇦 "+datetime.now().strftime("%H:%M:%S")
@app_flask.route('/health')
def health(): return "OK"
def run_flask():
    try: app_flask.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)),threaded=True)
    except: time.sleep(3); run_flask()
def self_ping():
    time.sleep(15); url=os.environ.get("RENDER_EXTERNAL_URL","")
    if not url: return
    while True:
        try: requests.get(url,timeout=10)
        except: pass
        time.sleep(240)
threading.Thread(target=run_flask,daemon=True).start()
threading.Thread(target=self_ping,daemon=True).start()

async def safe_edit(q,text,reply_markup=None):
    try:
        if q.message and q.message.text==text: return True
        await q.edit_message_text(text,reply_markup=reply_markup,parse_mode="Markdown"); return True
    except Exception as e:
        if "message is not modified" in str(e).lower(): return True
        try: await q.message.reply_text(text,reply_markup=reply_markup,parse_mode="Markdown")
        except:
            try: await q.message.reply_text(text,reply_markup=reply_markup)
            except: pass
        return True
async def safe_send(bot,chat_id,text,reply_markup=None):
    try: await bot.send_message(chat_id=chat_id,text=text,reply_markup=reply_markup,parse_mode="Markdown"); return True
    except:
        try: await bot.send_message(chat_id=chat_id,text=text,reply_markup=reply_markup); return True
        except: return False
def status_emoji(): return "🟢 اونلاين" if data.get("operator_status")=="online" else "🟡 مشغول" if data.get("operator_status")=="busy" else "🔴 اوفلاين"
def is_muted(u): return time.time()<u.get("muted_until",0)
def is_jailed(u): return time.time()<u.get("jailed_until",0)

# ===== كيبوردات - كله ازرار =====
def king_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👑 عرش المملكة",callback_data="kingdom"),InlineKeyboardButton("🏛️ مجلس الوزراء",callback_data="ministries")],
        [InlineKeyboardButton("👥 كل الرعايا - تحكم",callback_data="king_users")],
        [InlineKeyboardButton("🔨 حظر",callback_data="act_ban"),InlineKeyboardButton("⛓️ سجن",callback_data="act_jail"),InlineKeyboardButton("🔇 كتم",callback_data="act_mute")],
        [InlineKeyboardButton("💰 غرامة",callback_data="act_fine"),InlineKeyboardButton("⚠️ تحذير",callback_data="act_warn"),InlineKeyboardButton("📈 ترقية",callback_data="act_promote")],
        [InlineKeyboardButton("📉 تنزيل لعبد",callback_data="act_demote"),InlineKeyboardButton("⚖️ المحكمة",callback_data="courts")],
        [InlineKeyboardButton("🏦 البنك المركزي",callback_data="bank"),InlineKeyboardButton("🛢️ ارامكو",callback_data="aramco")],
        [InlineKeyboardButton("🏙️ نيوم",callback_data="neom"),InlineKeyboardButton("🗺️ المناطق",callback_data="regions")],
        [InlineKeyboardButton("🪪 أبشر",callback_data="absher"),InlineKeyboardButton("💬 شات مباشر",callback_data="live_start")],
        [InlineKeyboardButton("📢 اعلان ملكي",callback_data="king_broadcast"),InlineKeyboardButton("🎁 عفو ملكي",callback_data="royal_pardon")],
        [InlineKeyboardButton("🇸🇦 اليوم الوطني",callback_data="national_day"),InlineKeyboardButton("💰 خزينة المملكة",callback_data="treasury")],
        [InlineKeyboardButton("👁️ كاميرات المملكة",callback_data="spy"),InlineKeyboardButton("🔒 قفل المملكة",callback_data="lock_kingdom")],
        [InlineKeyboardButton("📊 احصائيات",callback_data="stats")],
    ])
def vizier_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💬 شاتات مباشرة",callback_data="live_active")],
        [InlineKeyboardButton("📩 تيكتات مفتوحة",callback_data="support_open"),InlineKeyboardButton("⚖️ قضايا",callback_data="courts")],
        [InlineKeyboardButton("⏳ طابور",callback_data="queue_list"),InlineKeyboardButton("📞 طلبات مكالمات",callback_data="callback_list")],
        [InlineKeyboardButton("💬 ردود جاهزة",callback_data="quick_replies")],
        [InlineKeyboardButton("🟢 اونلاين",callback_data="set_online"),InlineKeyboardButton("🟡 مشغول",callback_data="set_busy"),InlineKeyboardButton("🔴 اوفلاين",callback_data="set_offline")],
        [InlineKeyboardButton("🏰 المملكة",callback_data="kingdom")],
    ])
def user_kb(uid):
    u=get_user(uid)
    kb=[
        [InlineKeyboardButton(f"{RANKS[u['rank']]['name']} | {REGIONS.get(u['region'],'🏰 الرياض')}",callback_data="my_rank")],
        [InlineKeyboardButton("🏰 المملكة",callback_data="kingdom"),InlineKeyboardButton("🏦 البنك المركزي",callback_data="bank")],
        [InlineKeyboardButton("🏛️ الحكومة",callback_data="gov_user"),InlineKeyboardButton("🪪 أبشر",callback_data="absher")],
        [InlineKeyboardButton("🗺️ المناطق",callback_data="regions"),InlineKeyboardButton("🛢️ ارامكو",callback_data="aramco")],
        [InlineKeyboardButton("🏙️ نيوم",callback_data="neom"),InlineKeyboardButton("🛒 سوق المملكة",callback_data="market")],
        [InlineKeyboardButton("🎰 كازينو الرياض",callback_data="casino"),InlineKeyboardButton("🎡 عجلة الحظ",callback_data="wheel")],
        [InlineKeyboardButton("💬 شات مع الديوان",callback_data="live_start"),InlineKeyboardButton("👑 شات مع الملك",callback_data="live_king")],
        [InlineKeyboardButton("👥 مجلس الشورى",callback_data="shura"),InlineKeyboardButton("📩 شكوى",callback_data="new_ticket")],
        [InlineKeyboardButton("⚖️ ارفع قضية",callback_data="file_case"),InlineKeyboardButton("👮 بلاغ",callback_data="file_report")],
        [InlineKeyboardButton("🎁 هدية يومية",callback_data="daily"),InlineKeyboardButton("🏆 الاغنياء",callback_data="top")],
    ]
    if u["rank"]=="slave": kb.insert(1,[InlineKeyboardButton("⛓️ ادفع الجزية للملك 💰",callback_data="pay_tribute")])
    if u["rank"] in ["resident"]: kb.insert(2,[InlineKeyboardButton("🇸🇦 اطلب الجنسية",callback_data="ask_citizenship")])
    return InlineKeyboardMarkup(kb)
def bank_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 رصيدي",callback_data="balance"),InlineKeyboardButton("💸 تحويل",callback_data="transfer")],
        [InlineKeyboardButton("🏦 ايداع",callback_data="deposit"),InlineKeyboardButton("🏧 سحب",callback_data="withdraw")],
        [InlineKeyboardButton("🐷 تحويش",callback_data="savings"),InlineKeyboardButton("💳 فيزا",callback_data="visa")],
        [InlineKeyboardButton("💰 قرض ملكي",callback_data="loan"),InlineKeyboardButton("💰 سدد قسط",callback_data="loan_pay")],
        [InlineKeyboardButton("📄 صكوك",callback_data="cert"),InlineKeyboardButton("🏦 وديعة",callback_data="dep_money")],
        [InlineKeyboardButton("🧾 فواتير",callback_data="bills"),InlineKeyboardButton("📈 اسهم",callback_data="stocks")],
        [InlineKeyboardButton("🏠 اشتري بيت",callback_data="buy_house"),InlineKeyboardButton("🚗 اشتري عربية",callback_data="buy_car")],
        [InlineKeyboardButton("🔙 رجوع",callback_data="back")],
    ])
def live_kb(): return InlineKeyboardMarkup([[InlineKeyboardButton("⏹️ انهاء الشات",callback_data="live_end")]])
def back_kb(uid):
    if str(uid)==str(KING_ID): return king_kb()
    if str(uid)==str(MR_CAT_ID): return vizier_kb()
    return user_kb(uid)
def amounts_kb(action):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("100",callback_data=f"{action}_100"),InlineKeyboardButton("500",callback_data=f"{action}_500"),InlineKeyboardButton("1000",callback_data=f"{action}_1000")],
        [InlineKeyboardButton("5000",callback_data=f"{action}_5000"),InlineKeyboardButton("10000",callback_data=f"{action}_10000"),InlineKeyboardButton("كل فلوسي",callback_data=f"{action}_all")],
        [InlineKeyboardButton("🔙 رجوع",callback_data="bank")],
    ])

# ===== START =====
async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
    try:
        u=update.effective_user; uid=str(u.id)
        if uid in states: states.pop(uid)
        user=get_user(uid,u.username or "")
        if user["banned"] and uid!=str(KING_ID):
            await update.message.reply_text(f"🚫⛓️ **اتحظرت من المملكة!**\nالسبب: {user.get('ban_reason','بأمر الملك')}",parse_mode="Markdown"); return
        if is_jailed(user):
            await update.message.reply_text(f"⛓️ **انت مسجون بأمر الملك!**\nهتطلع: {datetime.fromtimestamp(user['jailed_until']).strftime('%d/%m %H:%M')}",parse_mode="Markdown"); return
        if uid==str(KING_ID):
            await update.message.reply_text(f"👑🇸🇦 **اهلا يا خادم الحرمين - الملك**\n\n🏰 رعاياك: {len(users)}\n💰 خزينة: {data['kingdom']['treasury']:,} ج\n🛢️ سعر النفط: {data['kingdom']['oil_price']} ج\n🚫 محظورين: {data['kingdom']['banned_count']}\n💬 شات: {len(live_chats)}\n⚖️ قضايا: {len(data['courts'])}\n\nانت الملك، كله تحتك، اتحكم في كل حاجة بالزرار 👑",reply_markup=king_kb(),parse_mode="Markdown"); return
        if uid==str(MR_CAT_ID):
            await update.message.reply_text(f"🎩 **اهلا رئيس الديوان Mr cat**\nحالتك: {status_emoji()}\n💬 شات: {len(live_chats)}\n📩 تيكتات: {len([t for t in tickets.values() if t['status']=='open'])}",reply_markup=vizier_kb(),parse_mode="Markdown"); return
        txt=f"🇸🇦 **مملكة الملك** 👑\nاهلا {u.first_name} {RANKS[user['rank']]['name']}\n\n🗺️ منطقتك: {REGIONS.get(user['region'],'🏰 الرياض')}\n💰 كاش: {user['balance']:,} | 🏦 بنك: {user['bank']:,}\n🏠 بيتك: {user['house']} | 🚗 عربيتك: {user['car']}\n🛢️ ابار نفط: {user['oil_wells']}\n⚠️ تحذيرات: {user.get('warnings',0)}/3\n📜 القانون: {data['kingdom']['law']}\n🎫 ID: `{uid}`"
        if user["rank"]=="slave": txt+="\n\n⛓️ انت عبد - ادفع الجزية عشان ترجع مواطن!"
        await update.message.reply_text(txt,reply_markup=user_kb(uid),parse_mode="Markdown")
    except Exception as e: print(f"START ERR {e}")

# ===== رسايل - شات مباشر اول حاجة =====
async def on_msg(update:Update,context:ContextTypes.DEFAULT_TYPE):
    try:
        if not update.message: return
        uid=str(update.effective_user.id)
        if uid in [str(KING_ID),str(MR_CAT_ID)]:
            t=update.message.text or ""
            if t and not t.startswith("/"):
                await update.message.reply_text("👑 عشان ترد دوس على زرار الشات او التيكت - كله ازرار",parse_mode="Markdown")
            return
        user=get_user(uid,update.effective_user.username or "")
        if user["banned"]: await update.message.reply_text("🚫 محظور"); return
        if is_jailed(user): await update.message.reply_text("⛓️ انت مسجون بأمر الملك!"); return
        if is_muted(user): await update.message.reply_text("🔇 انت مكتوم بأمر الملك!"); return
        text=update.message.text or update.message.caption or ""
        if update.message.voice: text="🎤 فويس"
        if update.message.photo and not text: text="🖼️ صورة"
        st=states.get(uid,"")
        # شات مباشر
        if uid in live_chats:
            for sid in SUPPORT_IDS:
                try:
                    if update.message.photo: await context.bot.send_photo(chat_id=sid,photo=update.message.photo[-1].file_id,caption=f"💬 **شات مباشر**\nمن: @{update.effective_user.username or uid} - `{uid}` - {RANKS[user['rank']]['name']}\n\n{text}\n\n[💬 رد] - دوس من لوحة الدعم",parse_mode="Markdown")
                    elif update.message.voice:
                        await context.bot.send_voice(chat_id=sid,voice=update.message.voice.file_id); await context.bot.send_message(chat_id=sid,text=f"🎤 فويس من `{uid}`",parse_mode="Markdown")
                    else: await context.bot.send_message(chat_id=sid,text=f"💬 **شات مباشر**\nمن: @{update.effective_user.username or uid} - `{uid}` - {RANKS[user['rank']]['name']}\n\n{text}",parse_mode="Markdown")
                except: pass
            # شات الشورى - يظهر للكل
            if live_chats.get(uid,{}).get("type")=="shura":
                data["shura"].append({"user":uid,"username":update.effective_user.username or uid,"text":text,"time":datetime.now().strftime("%H:%M")}); save()
            await update.message.reply_text("✅ وصلت للملك والديوان 👀",reply_markup=live_kb()); return
        if st.startswith("transfer_to_"):
            target=st.replace("transfer_to_",""); states.pop(uid); save()
            try: amt=int(text)
            except: await update.message.reply_text("ابعت رقم"); return
            if user["balance"]<amt: await update.message.reply_text("فلوسك مش كفاية"); return
            t=get_user(target); user["balance"]-=amt; t["balance"]+=amt; save(); await update.message.reply_text(f"✅ حولت {amt:,} لـ @{t['username'] or target}"); return
        if st=="waiting_ticket":
            states.pop(uid); data["ticket_counter"]+=1; tid=str(data["ticket_counter"])
            tickets[tid]={"id":tid,"user_id":uid,"username":update.effective_user.username or "","text":text,"status":"open","created":datetime.now().strftime("%d/%m %H:%M"),"reply":""}; save()
            await update.message.reply_text(f"✅ عملت شكوى #{tid}\nالديوان هيرد عليك")
            for sid in SUPPORT_IDS:
                try: await context.bot.send_message(chat_id=sid,text=f"🎧 **شكوى جديدة #{tid}**\nمن: @{update.effective_user.username or uid} - `{uid}`\n\n{text}",parse_mode="Markdown")
                except: pass
            return
        if st=="waiting_rate":
            states.pop(uid); save()
            try: rate=int(text)
            except: await update.message.reply_text("ابعت رقم 1-5"); return
            data["ratings"].append({"user":uid,"rate":rate}); save(); await update.message.reply_text(f"شكرا {rate} ⭐"); return
        if st=="waiting_name":
            states[uid]="waiting_phone"; data.setdefault("temp",{})[uid]={"name":text}; save(); await update.message.reply_text(f"تمام يا {text}\nاكتب رقم موبايلك:"); return
        if st=="waiting_phone":
            temp=data.get("temp",{}).get(uid,{}); name=temp.get("name","عميل"); states.pop(uid)
            data["callbacks"].append({"user_id":uid,"username":update.effective_user.username or "","name":name,"phone":text,"time":datetime.now().strftime("%d/%m %H:%M"),"done":False}); save()
            await update.message.reply_text(f"✅ سجلنا طلب مكالمة يا {name}")
            for sid in SUPPORT_IDS:
                try: await context.bot.send_message(chat_id=sid,text=f"📞 **طلب مكالمة!**\n👤 {name}\n📱 {text}\n`{uid}`",parse_mode="Markdown")
                except: pass
            return
        if st=="waiting_broadcast":
            states.pop(uid); save(); cnt=0
            for uid2 in list(users.keys()):
                if not users[uid2]["banned"]:
                    if await safe_send(context.bot,int(uid2),f"📢 **خطاب ملكي 👑🇸🇦**\n\n{text}"): cnt+=1
            await update.message.reply_text(f"📢 بعت الخطاب لـ {cnt} رعية 👑"); return
        if st=="waiting_law":
            states.pop(uid); data["kingdom"]["law"]=text; save(); await update.message.reply_text(f"📜✅ القانون الجديد:\n{text}",reply_markup=king_kb()); return
        if st=="waiting_mission":
            states.pop(uid); save()
            for uid2 in list(users.keys()):
                if not users[uid2]["banned"]: await safe_send(context.bot,int(uid2),f"📋 **مهمة ملكية جديدة!**\n\n{text}\n\nدوس ✅ عملت المهمة من لوحتك عشان تاخد المكافأة")
            await update.message.reply_text("✅ نزلت المهمة لكل الرعايا"); return
        if st=="waiting_reply_ticket":
            # الوزير بيرد على تيكت - اخر تيكت اختاره
            tid=data.get("temp",{}).get(uid,{}).get("reply_ticket","")
            states.pop(uid); save()
            if tid in tickets:
                tickets[tid]["status"]="replied"; tickets[tid]["reply"]=text; save()
                await safe_send(context.bot,int(tickets[tid]["user_id"]),f"🎧 **الديوان الملكي رد عليك:**\n\n{text}")
                await update.message.reply_text(f"✅ رديت على #{tid}")
            return
        if st=="waiting_reply_live":
            target=data.get("temp",{}).get(uid,{}).get("reply_live","")
            states.pop(uid); save()
            if target: await safe_send(context.bot,int(target),f"💬 **الديوان الملكي:**\n\n{text}",reply_markup=live_kb()); await update.message.reply_text("✅ وصلت")
            return
        if st=="waiting_case_text":
            target=data.get("temp",{}).get(uid,{}).get("case_target","")
            reason=data.get("temp",{}).get(uid,{}).get("case_reason","شكوى")
            states.pop(uid); data["courts"].append({"id":str(len(data["courts"])+100),"from":uid,"to":target,"reason":reason,"text":text,"status":"open"}); save()
            await update.message.reply_text("✅ رفعت القضية - الملك هيحكم فيها 👑")
            await safe_send(context.bot,KING_ID,f"⚖️ **قضية جديدة!**\nمن: `{uid}` ضد `{target}`\nالتهمة: {reason}\nالتفاصيل: {text}\n\nدوس ⚖️ المحكمة عشان تحكم")
            return
        await update.message.reply_text("اكتب /start 👑",reply_markup=user_kb(uid) if uid not in [str(KING_ID),str(MR_CAT_ID)] else king_kb() if uid==str(KING_ID) else vizier_kb())
    except Exception as e: print(f"ON_MSG ERR {e}"); traceback.print_exc()

# ===== زرار - كله ازرار =====
async def buttons(update:Update,context:ContextTypes.DEFAULT_TYPE):
    try:
        q=update.callback_query; await q.answer(); uid=str(q.from_user.id); d=q.data; user=get_user(uid,q.from_user.username or "")
        print(f"BTN {uid} {d}")
        if user["banned"] and uid!=str(KING_ID): await safe_edit(q,"🚫 محظور"); return
        if is_jailed(user) and d not in ["back"]: await safe_edit(q,f"⛓️ انت مسجون! هتطلع {datetime.fromtimestamp(user['jailed_until']).strftime('%d/%m %H:%M')}"); return
        if is_muted(user) and d not in ["back","live_end"]: await safe_edit(q,"🔇 انت مكتوم بأمر الملك!"); return

        # ===== رجوع =====
        if d=="back":
            if uid==str(KING_ID): await safe_edit(q,"👑🇸🇦 **الملك**",reply_markup=king_kb())
            elif uid==str(MR_CAT_ID): await safe_edit(q,"🎩 **الديوان**",reply_markup=vizier_kb())
            else: await safe_edit(q,f"🇸🇦 **المملكة**\nرتبتك: {RANKS[user['rank']]['name']}",reply_markup=user_kb(uid))
            return

        # ===== المملكة =====
        if d=="kingdom":
            counts={}
            for u in users.values(): counts[u["rank"]]=counts.get(u["rank"],0)+1
            txt="🏰🇸🇦 **مملكة الملك** 👑\n\n"
            for r in reversed(RANK_ORDER): txt+=f"{RANKS[r]['name']}: {counts.get(r,0)}\n"
            txt+=f"\n💰 خزينة: {data['kingdom']['treasury']:,}\n🛢️ نفط: {data['kingdom']['oil_price']} ج\n📜 القانون: {data['kingdom']['law']}\n\nرتبتك: {RANKS[user['rank']]['name']}"
            await safe_edit(q,txt,reply_markup=king_kb() if uid==str(KING_ID) else back_kb(uid)); return
        if d=="my_rank": await safe_edit(q,f"رتبتك: **{RANKS[user['rank']]['name']}**\n\n👑 ملك > 🤴 ولي عهد > 👸 أميرة > 🎩 ديوان > 👑 أمير > 💎 شيخ > 🛡️ قائد > 👮 شرطة > 💰 وزير > 💰 تاجر > 🇸🇦 مواطن > 🧑 مقيم > ⛓️ عبد\n\nتحذيرات: {user.get('warnings',0)}/3",reply_markup=user_kb(uid)); return
        if d=="treasury": await safe_edit(q,f"💰 **خزينة المملكة**\n\n{data['kingdom']['treasury']:,} ج\n\nالجزية: {data['kingdom']['jizya']} ج\nالزكاة: {data['kingdom']['zakat']}%",reply_markup=king_kb()); return
        if d=="stats":
            open_t=len([t for t in tickets.values() if t["status"]=="open"])
            await safe_edit(q,f"📊 **احصائيات المملكة:**\n\n👥 رعايا: {len(users)}\n💬 شات: {len(live_chats)}\n📩 شكاوى: {open_t}\n⚖️ قضايا: {len(data['courts'])}\n💰 خزينة: {data['kingdom']['treasury']:,}",reply_markup=king_kb() if uid==str(KING_ID) else vizier_kb()); return
        if d=="spy":
            if uid!=str(KING_ID): return
            txt="👁️ **كاميرات المملكة - اخر رسايل الشورى:**\n\n"
            for m in data["shura"][-10:]: txt+=f"@{m['username']}: {m['text'][:40]}\n"
            await safe_edit(q,txt or "مفيش رسايل",reply_markup=king_kb()); return
        if d=="lock_kingdom":
            if uid!=str(KING_ID): return
            data["kingdom"]["locked"]=not data["kingdom"].get("locked",False); save()
            await safe_edit(q,f"{'🔒 قفلت المملكة - محدش يدخل غير العائلة' if data['kingdom']['locked'] else '☀️ فتحت المملكة'}",reply_markup=king_kb()); return
        if d=="royal_pardon":
            if uid!=str(KING_ID): return
            cnt=0
            for u in users.values():
                if u["banned"] or u["jailed_until"]>0 or u["muted_until"]>0: u["banned"]=False; u["jailed_until"]=0; u["muted_until"]=0; u["warnings"]=0; cnt+=1
            save()
            for uid2 in list(users.keys()):
                if not users[uid2]["banned"]: await safe_send(context.bot,int(uid2),"🎁👑 **عفو ملكي!**\nالملك عفا عن الكل 🇸🇦")
            await safe_edit(q,f"🎁 عفو ملكي - عفيت عن {cnt} واحد 👑",reply_markup=king_kb()); return
        if d=="national_day":
            if uid==str(KING_ID):
                for uid2 in list(users.keys()):
                    if not users[uid2]["banned"]: users[uid2]["balance"]+=5000
                save()
                for uid2 in list(users.keys()):
                    if not users[uid2]["banned"]: await safe_send(context.bot,int(uid2),"🇸🇦🎉 **اليوم الوطني!**\nالملك اداك 5000 هدية 👑")
                await safe_edit(q,"🇸🇦 وزعت 5000 على الكل - اليوم الوطني!",reply_markup=king_kb()); return
            else: await safe_edit(q,"🇸🇦 **اليوم الوطني**\nالملك بيوزع هدايا في اليوم الوطني!",reply_markup=user_kb(uid)); return
        if d=="king_broadcast":
            if uid!=str(KING_ID): return
            states[uid]="waiting_broadcast"; save(); await safe_edit(q,"📢 **خطاب ملكي**\nاكتب الخطاب اللي هيوصل لكل الرعايا:"); return
        if d=="king_users":
            if uid!=str(KING_ID): return
            # قايمة اول 12 - كل واحد ازرار تحكم
            kb=[]
            for u in list(users.values())[-12:]:
                if str(u["id"])==str(KING_ID): continue
                b="🚫" if u["banned"] else "⛓️" if is_jailed(u) else ""
                kb.append([InlineKeyboardButton(f"{RANKS[u['rank']]['name']} @{u['username'] or u['id']} {b}",callback_data=f"view_{u['id']}")])
            kb.append([InlineKeyboardButton("🔙 رجوع",callback_data="back")])
            await safe_edit(q,"👥 **كل الرعايا - دوس على واحد عشان تتحكم فيه:**",reply_markup=InlineKeyboardMarkup(kb)); return
        if d.startswith("view_"):
            if uid!=str(KING_ID): return
            tid=d.replace("view_",""); t=get_user(tid)
            kb=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔨 حظر",callback_data=f"do_ban_{tid}"),InlineKeyboardButton("✅ فك حظر",callback_data=f"do_unban_{tid}")],
                [InlineKeyboardButton("⛓️ سجن 1 ساعة",callback_data=f"do_jail1_{tid}"),InlineKeyboardButton("⛓️ سجن 1 يوم",callback_data=f"do_jail24_{tid}")],
                [InlineKeyboardButton("🔇 كتم 1 ساعة",callback_data=f"do_mute1_{tid}"),InlineKeyboardButton("💰 غرامة 500",callback_data=f"do_fine500_{tid}")],
                [InlineKeyboardButton("⚠️ تحذير",callback_data=f"do_warn_{tid}"),InlineKeyboardButton("📈 ترقية",callback_data=f"do_promote_{tid}")],
                [InlineKeyboardButton("📉 نزله عبد",callback_data=f"do_demote_{tid}"),InlineKeyboardButton("🤴 خليه ولي عهد",callback_data=f"do_crown_{tid}")],
                [InlineKeyboardButton("👑 خليه أمير",callback_data=f"do_prince_{tid}"),InlineKeyboardButton("💰 اديله 5000",callback_data=f"do_give5000_{tid}")],
                [InlineKeyboardButton("🔙 رجوع",callback_data="king_users")],
            ])
            await safe_edit(q,f"👤 **@{t['username'] or t['id']}**\nرتبة: {RANKS[t['rank']]['name']}\n💰 فلوس: {t['balance']:,} | بنك: {t['bank']:,}\n🗺️ منطقة: {REGIONS.get(t['region'],'')}\n⚠️ تحذيرات: {t.get('warnings',0)}\n🚫 محظور: {'ايوه' if t['banned'] else 'لا'}\n\nاختار عقاب او مكافأة 👑",reply_markup=kb); return
        # ===== افعال الملك - كلها ازرار =====
        if d.startswith("do_"):
            if uid!=str(KING_ID): return
            parts=d.split("_"); action=parts[1]; tid=parts[2]
            t=get_user(tid)
            if action=="ban": t["banned"]=True; t["ban_reason"]="بأمر الملك"; data["kingdom"]["banned_count"]+=1; save(); await safe_send(context.bot,int(tid),"🚫 اتحظرت بأمر الملك 👑"); await safe_edit(q,f"🔨 حظرت @{t['username'] or tid} 👑",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع",callback_data=f"view_{tid}")]])); return
            if action=="unban": t["banned"]=False; t["ban_reason"]=""; save(); await safe_send(context.bot,int(tid),"✅ الملك فك حظرك 👑"); await safe_edit(q,f"✅ فكيت حظر @{t['username'] or tid}",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع",callback_data=f"view_{tid}")]])); return
            if action=="jail1": t["jailed_until"]=time.time()+3600; save(); await safe_send(context.bot,int(tid),"⛓️ اتسجنت 1 ساعة بأمر الملك"); await safe_edit(q,f"⛓️ سجنت @{t['username'] or tid} 1 ساعة",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع",callback_data=f"view_{tid}")]])); return
            if action=="jail24": t["jailed_until"]=time.time()+86400; save(); await safe_send(context.bot,int(tid),"⛓️ اتسجنت 1 يوم بأمر الملك"); await safe_edit(q,f"⛓️ سجنت @{t['username'] or tid} 1 يوم",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع",callback_data=f"view_{tid}")]])); return
            if action=="mute1": t["muted_until"]=time.time()+3600; save(); await safe_send(context.bot,int(tid),"🔇 اتكتمت 1 ساعة بأمر الملك"); await safe_edit(q,f"🔇 كتمت @{t['username'] or tid}",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع",callback_data=f"view_{tid}")]])); return
            if action=="fine500":
                amt=min(500,t["balance"]); t["balance"]-=amt; data["kingdom"]["treasury"]+=amt; save(); await safe_send(context.bot,int(tid),f"💰 اتغرمت {amt} ج بأمر الملك"); await safe_edit(q,f"💰 غرمت @{t['username'] or tid} {amt} ج",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع",callback_data=f"view_{tid}")]])); return
            if action=="warn":
                t["warnings"]=t.get("warnings",0)+1; save(); await safe_send(context.bot,int(tid),f"⚠️ تحذير {t['warnings']}/3 من الملك!"); await safe_edit(q,f"⚠️ حذرت @{t['username'] or tid} - {t['warnings']}/3",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع",callback_data=f"view_{tid}")]]))
                if t["warnings"]>=3: t["banned"]=True; save(); await safe_send(context.bot,int(tid),"🚫 اتحظرت - 3 تحذيرات")
                return
            if action=="promote":
                idx=RANK_ORDER.index(t["rank"])
                if idx<len(RANK_ORDER)-2: t["rank"]=RANK_ORDER[idx+1]; save(); await safe_send(context.bot,int(tid),f"📈 الملك رقاك لـ {RANKS[t['rank']]['name']}"); await safe_edit(q,f"📈 رقيت @{t['username'] or tid} لـ {RANKS[t['rank']]['name']}",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع",callback_data=f"view_{tid}")]])); return
            if action=="demote": t["rank"]="slave"; save(); await safe_send(context.bot,int(tid),"⛓️ الملك نزلك عبد!"); await safe_edit(q,f"📉 نزلت @{t['username'] or tid} عبد",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع",callback_data=f"view_{tid}")]])); return
            if action=="crown": t["rank"]="crown"; save(); await safe_send(context.bot,int(tid),"🤴 الملك خلاك ولي العهد!"); await safe_edit(q,f"🤴 @{t['username'] or tid} بقى ولي العهد",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع",callback_data=f"view_{tid}")]])); return
            if action=="prince": t["rank"]="prince"; save(); await safe_send(context.bot,int(tid),"👑 الملك خلاك أمير!"); await safe_edit(q,f"👑 @{t['username'] or tid} بقى أمير",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع",callback_data=f"view_{tid}")]])); return
            if action=="give5000": t["balance"]+=5000; save(); await safe_send(context.bot,int(tid),"🎁 الملك اداك 5000 👑"); await safe_edit(q,f"🎁 اديت @{t['username'] or tid} 5000",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع",callback_data=f"view_{tid}")]])); return
        if d.startswith("act_"):
            if uid!=str(KING_ID): return
            await safe_edit(q,"👥 دوس على واحد من الرعايا عشان تنفذ فيه:",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("👥 كل الرعايا",callback_data="king_users")],[InlineKeyboardButton("🔙 رجوع",callback_data="back")]])); return

        # ===== البنك =====
        if d=="bank": await safe_edit(q,"🏦 **البنك المركزي السعودي** 🇸🇦\n\n💰 كاش: "+f"{user['balance']:,}\n🏦 بنك: {user['bank']:,}\n🐷 تحويش: {user['savings']:,}\n💳 فيزا: {user['credit_used']:,}/{user['credit_limit']:,}",reply_markup=bank_kb()); return
        if d=="balance": await safe_edit(q,f"💰 كاش: {user['balance']:,}\n🏦 بنك: {user['bank']:,}\n🐷 تحويش: {user['savings']:,}\n💳 فيزا: {user['credit_used']:,}/{user['credit_limit']:,}\n💰 قرض: {user['loan_left']:,}\n🏠 بيت: {user['house']} | 🚗 عربية: {user['car']}\n🛢️ ابار: {user['oil_wells']}",reply_markup=bank_kb()); return
        if d=="transfer":
            kb=[]
            for u in list(users.values())[:12]:
                if str(u["id"])==uid: continue
                kb.append([InlineKeyboardButton(f"{RANKS[u['rank']]['name']} @{u['username'] or u['id']}",callback_data=f"tr_to_{u['id']}")])
            kb.append([InlineKeyboardButton("🔙 رجوع",callback_data="bank")])
            await safe_edit(q,"💸 **تحويل - اختار واحد:**",reply_markup=InlineKeyboardMarkup(kb)); return
        if d.startswith("tr_to_"):
            tid=d.replace("tr_to_",""); states[uid]=f"transfer_to_{tid}"; save(); await safe_edit(q,f"💸 هتحول لـ @{get_user(tid)['username'] or tid}\nاكتب المبلغ:"); return
        if d=="deposit": await safe_edit(q,"🏦 اختار مبلغ الايداع:",reply_markup=amounts_kb("dep")); return
        if d=="withdraw": await safe_edit(q,"🏧 اختار مبلغ السحب:",reply_markup=amounts_kb("wit")); return
        if d.startswith("dep_") or d.startswith("wit_"):
            is_dep=d.startswith("dep_"); amt_str=d.split("_")[1]
            amt=user["balance"] if amt_str=="all" else int(amt_str)
            if is_dep:
                if user["balance"]<amt: await safe_edit(q,"فلوسك مش كفاية",reply_markup=bank_kb()); return
                user["balance"]-=amt; user["bank"]+=amt; save(); await safe_edit(q,f"✅ اودعت {amt:,}",reply_markup=bank_kb()); return
            else:
                if user["bank"]<amt: await safe_edit(q,"فلوس البنك مش كفاية",reply_markup=bank_kb()); return
                user["bank"]-=amt; user["balance"]+=amt; save(); await safe_edit(q,f"✅ سحبت {amt:,}",reply_markup=bank_kb()); return
        if d=="savings": await safe_edit(q,f"🐷 تحويشك: {user['savings']:,}",reply_markup=amounts_kb("sav")); return
        if d.startswith("sav_"):
            amt_str=d.split("_")[1]; amt=user["balance"] if amt_str=="all" else int(amt_str)
            if user["balance"]<amt: await safe_edit(q,"فلوسك مش كفاية",reply_markup=bank_kb()); return
            user["balance"]-=amt; user["savings"]+=amt; save(); await safe_edit(q,f"🐷 حوشت {amt:,}",reply_markup=bank_kb()); return
        if d=="visa":
            if not user["credit_card"]:
                num=f"4000 {random.randint(1000,9999)} {random.randint(1000,9999)} {random.randint(1000,9999)}"; user["credit_card"]=num; user["credit_limit"]=100000 if user["rank"]=="king" else 50000 if user["rank"] in ["crown","prince"] else 20000 if user["rank"] in ["sheikh","minister"] else 5000; save()
            await safe_edit(q,f"💳 فيزتك: `{user['credit_card']}`\nالحد: {user['credit_limit']:,}",reply_markup=bank_kb()); return
        if d=="loan":
            if user["loan_left"]>0: await safe_edit(q,f"💰 عليك: {user['loan_left']:,} - القسط: {user['loan_pay']:,}",reply_markup=bank_kb())
            else: await safe_edit(q,"💰 اختار مبلغ القرض:",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("1000",callback_data="loan_1000"),InlineKeyboardButton("5000",callback_data="loan_5000"),InlineKeyboardButton("10000",callback_data="loan_10000")],[InlineKeyboardButton("🔙 رجوع",callback_data="bank")]]))
            return
        if d.startswith("loan_"):
            amt=int(d.split("_")[1]); total=int(amt*1.2); pay=total//3; user["loan_left"]=total; user["loan_pay"]=pay; user["loan_installments"]=3; user["balance"]+=amt; save(); await safe_edit(q,f"💰 خدت قرض {amt:,} - هتسدد {total:,} على 3 اقساط",reply_markup=bank_kb()); return
        if d=="loan_pay":
            if user["loan_left"]<=0: await safe_edit(q,"مفيش قرض ✅",reply_markup=bank_kb()); return
            if user["balance"]<user["loan_pay"]: await safe_edit(q,"فلوسك مش كفاية",reply_markup=bank_kb()); return
            user["balance"]-=user["loan_pay"]; user["loan_left"]-=user["loan_pay"]; user["loan_installments"]-=1
            if user["loan_left"]<=0: user["loan_left"]=0
            save(); await safe_edit(q,f"✅ سددت قسط\nالمتبقي: {user['loan_left']:,}",reply_markup=bank_kb()); return
        if d=="cert": await safe_edit(q,"📄 اختار مبلغ الصك:",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("1000",callback_data="cert_1000"),InlineKeyboardButton("5000",callback_data="cert_5000"),InlineKeyboardButton("10000",callback_data="cert_10000")],[InlineKeyboardButton("🔙 رجوع",callback_data="bank")]])); return
        if d.startswith("cert_"):
            amt=int(d.split("_")[1])
            if user["balance"]<amt: await safe_edit(q,"فلوسك مش كفاية",reply_markup=bank_kb()); return
            user["balance"]-=amt; user["certificates"].append({"amount":amt}); save(); await safe_edit(q,f"📄 عملت صك {amt:,} - ربح 20%",reply_markup=bank_kb()); return
        if d=="dep_money": await safe_edit(q,"🏦 اختار مبلغ الوديعة:",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("1000",callback_data="depM_1000"),InlineKeyboardButton("5000",callback_data="depM_5000"),InlineKeyboardButton("10000",callback_data="depM_10000")],[InlineKeyboardButton("🔙 رجوع",callback_data="bank")]])); return
        if d.startswith("depM_"):
            amt=int(d.split("_")[1])
            if user["balance"]<amt: await safe_edit(q,"فلوسك مش كفاية",reply_markup=bank_kb()); return
            user["balance"]-=amt; user["deposits"].append({"amount":amt}); save(); await safe_edit(q,f"🏦 وديعة {amt:,} - فايدة 15%",reply_markup=bank_kb()); return
        if d=="bills":
            b=user["bills"]; total=b["electric"]+b["water"]+b["internet"]
            if total==0: b["electric"]=random.randint(50,200); b["water"]=random.randint(30,100); b["internet"]=random.randint(100,300); save(); total=b["electric"]+b["water"]+b["internet"]
            await safe_edit(q,f"🧾 **فواتيرك:**\n⚡ {b['electric']:,} | 💧 {b['water']:,} | 🌐 {b['internet']:,}\nالاجمالي: {total:,}",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💳 ادفع",callback_data="bills_pay")],[InlineKeyboardButton("🔙 رجوع",callback_data="bank")]])); return
        if d=="bills_pay":
            b=user["bills"]; total=b["electric"]+b["water"]+b["internet"]
            if user["balance"]<total: await safe_edit(q,"فلوسك مش كفاية",reply_markup=bank_kb()); return
            user["balance"]-=total; user["bills"]={"electric":0,"water":0,"internet":0}; save(); await safe_edit(q,f"✅ دفعت {total:,}",reply_markup=bank_kb()); return
        if d=="stocks":
            await safe_edit(q,f"📈 **سوق الاسهم**\n\n🛢️ ارامكو: {user['stocks']['aramco']} سهم\n🏙️ نيوم: {user['stocks']['neom']} سهم\n🏦 بنك: {user['stocks']['bank']} سهم\n\nسعر النفط: {data['kingdom']['oil_price']} ج",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🛢️ اشتري ارامكو 1000",callback_data="stock_aramco"),InlineKeyboardButton("🏙️ اشتري نيوم 1000",callback_data="stock_neom")],[InlineKeyboardButton("💰 بيع الكل",callback_data="stock_sell")],[InlineKeyboardButton("🔙 رجوع",callback_data="bank")]])); return
        if d.startswith("stock_"):
            if d=="stock_sell":
                total=(user['stocks']['aramco']+user['stocks']['neom']+user['stocks']['bank'])*1200; user['stocks']={"aramco":0,"neom":0,"bank":0}; user["balance"]+=total; save(); await safe_edit(q,f"💰 بعت الاسهم وخدت {total:,}",reply_markup=bank_kb()); return
            which=d.split("_")[1]
            if user["balance"]<1000: await safe_edit(q,"فلوسك مش كفاية",reply_markup=bank_kb()); return
            user["balance"]-=1000; user['stocks'][which]+=1; save(); await safe_edit(q,f"📈 اشتريت سهم {which}",reply_markup=bank_kb()); return
        if d=="buy_house":
            await safe_edit(q,"🏠 **اشتري بيت:**",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏚️ شقة - 5000",callback_data="house_5000"),InlineKeyboardButton("🏠 بيت - 20000",callback_data="house_20000")],[InlineKeyboardButton("🏰 قصر - 100000",callback_data="house_100000")],[InlineKeyboardButton("🔙 رجوع",callback_data="bank")]])); return
        if d.startswith("house_"):
            amt=int(d.split("_")[1])
            if user["balance"]<amt: await safe_edit(q,"فلوسك مش كفاية",reply_markup=bank_kb()); return
            user["balance"]-=amt; user["house"]="🏚️ شقة" if amt==5000 else "🏠 بيت" if amt==20000 else "🏰 قصر"
            if amt==100000 and user["rank"] in ["citizen","resident"]: user["rank"]="trader"
            save(); await safe_edit(q,f"🏠 اشتريت {user['house']} 👑",reply_markup=bank_kb()); return
        if d=="buy_car":
            await safe_edit(q,"🚗 **اشتري عربية:**",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🚗 كامري - 10000",callback_data="car_10000"),InlineKeyboardButton("🚙 لاند كروزر - 50000",callback_data="car_50000")],[InlineKeyboardButton("🏎️ لامبورجيني - 200000",callback_data="car_200000")],[InlineKeyboardButton("🔙 رجوع",callback_data="bank")]])); return
        if d.startswith("car_"):
            amt=int(d.split("_")[1])
            if user["balance"]<amt: await safe_edit(q,"فلوسك مش كفاية",reply_markup=bank_kb()); return
            user["balance"]-=amt; user["car"]="🚗 كامري" if amt==10000 else "🚙 لاند كروزر" if amt==50000 else "🏎️ لامبورجيني"; save(); await safe_edit(q,f"🚗 اشتريت {user['car']} 🔥",reply_markup=bank_kb()); return

        # ===== ارامكو ونيوم =====
        if d=="aramco":
            await safe_edit(q,f"🛢️ **ارامكو المملكة**\n\nسعر النفط: {data['kingdom']['oil_price']} ج\nابارك: {user['oil_wells']}\n\nكل بئر بيكسب 500 كل يوم",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⛏️ اشتغل في ارامكو +300",callback_data="work_aramco")],[InlineKeyboardButton("🛢️ بيع 100 برميل",callback_data="sell_oil")],[InlineKeyboardButton("🔙 رجوع",callback_data="back")]])); return
        if d=="work_aramco":
            r=random.randint(200,400); user["balance"]+=r; save(); await safe_edit(q,f"🛢️ اشتغلت في ارامكو وخدت {r} ج",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⛏️ اشتغل تاني",callback_data="work_aramco")],[InlineKeyboardButton("🔙 رجوع",callback_data="back")]])); return
        if d=="sell_oil":
            if uid!=str(KING_ID):
                await safe_edit(q,"🛢️ بس الملك اللي يبيع النفط!",reply_markup=back_kb(uid)); return
            gain=100*data['kingdom']['oil_price']; data['kingdom']['treasury']+=gain; data['kingdom']['oil_price']=random.randint(60,120); save(); await safe_edit(q,f"🛢️ بعت 100 برميل وخدت {gain:,} للخزينة 👑\nسعر النفط الجديد: {data['kingdom']['oil_price']}",reply_markup=king_kb()); return
        if d=="neom":
            await safe_edit(q,"🏙️ **نيوم - مشروع الملك**\n\nاستثمر 1000 وخد 1300 بعد شوية",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏗️ استثمر 1000",callback_data="invest_neom")],[InlineKeyboardButton("🔙 رجوع",callback_data="back")]])); return
        if d=="invest_neom":
            if user["balance"]<1000: await safe_edit(q,"فلوسك مش كفاية",reply_markup=back_kb(uid)); return
            user["balance"]-=1000; user["balance"]+=1300; save(); await safe_edit(q,"🏙️ استثمرت في نيوم وخدت 1300 👑",reply_markup=back_kb(uid)); return
        if d=="market":
            await safe_edit(q,"🛒 **سوق المملكة**",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⚔️ سيف - 500",callback_data="buy_sword"),InlineKeyboardButton("🛡️ درع - 500",callback_data="buy_shield")],[InlineKeyboardButton("🐎 حصان - 2000",callback_data="buy_horse")],[InlineKeyboardButton("🔙 رجوع",callback_data="back")]])); return
        if d.startswith("buy_"):
            item=d.replace("buy_",""); prices={"sword":500,"shield":500,"horse":2000}
            if item not in prices: return
            if user["balance"]<prices[item]: await safe_edit(q,"فلوسك مش كفاية",reply_markup=back_kb(uid)); return
            user["balance"]-=prices[item]; save(); await safe_edit(q,f"🛒 اشتريت {item} 👑",reply_markup=back_kb(uid)); return

        # ===== مناطق =====
        if d=="regions":
            kb=[[InlineKeyboardButton(f"{v}",callback_data=f"region_{k}")] for k,v in REGIONS.items()]
            kb.append([InlineKeyboardButton("🔙 رجوع",callback_data="back")])
            await safe_edit(q,"🗺️ **مناطق المملكة - اختار منطقتك:**",reply_markup=InlineKeyboardMarkup(kb)); return
        if d.startswith("region_"):
            reg=d.replace("region_","")
            if user["region"]==reg: await safe_edit(q,f"انت already في {REGIONS[reg]}",reply_markup=back_kb(uid)); return
            if user["balance"]<200: await safe_edit(q,"السفر 200 ج - فلوسك مش كفاية",reply_markup=back_kb(uid)); return
            user["balance"]-=200; data['kingdom']['treasury']+=200; user["region"]=reg; save(); await safe_edit(q,f"✈️ سافرت لـ {REGIONS[reg]} 👑",reply_markup=back_kb(uid)); return

        # ===== أبشر =====
        if d=="absher":
            await safe_edit(q,f"🪪 **أبشر المملكة**\n\n🪪 هوية: {'✅' if user['has_id'] else '❌'}\n🛂 جواز: {'✅' if user['has_passport'] else '❌'}\n🚗 رخصة: {'✅' if user['has_license'] else '❌'}\n🇸🇦 جنسية: {'✅ سعودي' if user['citizenship'] else '❌ مقيم'}",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🪪 طلع هوية - مجاني",callback_data="absher_id"),InlineKeyboardButton("🛂 جواز - 500",callback_data="absher_pass")],[InlineKeyboardButton("🚗 رخصة - 500",callback_data="absher_license"),InlineKeyboardButton("🇸🇦 اطلب الجنسية",callback_data="ask_citizenship")],[InlineKeyboardButton("🪪 جدد اقامة - 500",callback_data="absher_iqama")],[InlineKeyboardButton("🔙 رجوع",callback_data="back")]])); return
        if d=="absher_id": user["has_id"]=True; save(); await safe_edit(q,"🪪 طلعت الهوية الملكية ✅",reply_markup=back_kb(uid)); return
        if d=="absher_pass":
            if user["balance"]<500: await safe_edit(q,"فلوسك مش كفاية",reply_markup=back_kb(uid)); return
            user["balance"]-=500; user["has_passport"]=True; save(); await safe_edit(q,"🛂 طلعت جواز السفر ✅",reply_markup=back_kb(uid)); return
        if d=="absher_license":
            if user["balance"]<500: await safe_edit(q,"فلوسك مش كفاية",reply_markup=back_kb(uid)); return
            user["balance"]-=500; user["has_license"]=True; save(); await safe_edit(q,"🚗 طلعت الرخصة ✅",reply_markup=back_kb(uid)); return
        if d=="absher_iqama":
            if user["balance"]<500: await safe_edit(q,"فلوسك مش كفاية",reply_markup=back_kb(uid)); return
            user["balance"]-=500; data['kingdom']['treasury']+=500; save(); await safe_edit(q,"🪪 جددت الاقامة ✅",reply_markup=back_kb(uid)); return
        if d=="ask_citizenship":
            await safe_edit(q,"🇸🇦 طلبت الجنسية - الملك هيوافق او يرفض",reply_markup=back_kb(uid))
            await safe_send(context.bot,KING_ID,f"🇸🇦 **طلب جنسية!**\nمن: @{user['username'] or uid} - `{uid}`\n\nدوس على اسمه من 👥 كل الرعايا واديله الجنسية لو عايز")
            return

        # ===== حكومة =====
        if d=="ministries":
            if uid!=str(KING_ID): await safe_edit(q,"🏛️ مجلس الوزراء - بس الملك يشوفه",reply_markup=back_kb(uid)); return
            await safe_edit(q,"🏛️ **مجلس الوزراء**\n\nاختار وزارة عشان تعين وزيرها:",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💰 وزارة المالية",callback_data="ministry_finance"),InlineKeyboardButton("🛡️ الداخلية",callback_data="ministry_interior")],[InlineKeyboardButton("⚖️ العدل",callback_data="ministry_justice"),InlineKeyboardButton("🛢️ الطاقة",callback_data="ministry_energy")],[InlineKeyboardButton("🔙 رجوع",callback_data="back")]])); return
        if d.startswith("ministry_"):
            await safe_edit(q,"👑 عشان تعين وزير، دوس على واحد من الرعايا واعمله ترقية وزير 👑",reply_markup=king_kb()); return
        if d=="gov_user":
            await safe_edit(q,"🏛️ **حكومة المملكة**\n\n💰 المالية - البنك والخزينة\n🛡️ الداخلية - الشرطة والسجن\n⚖️ العدل - المحكمة\n🛢️ الطاقة - النفط\n\nلو عندك شكوى دوس 📩 شكوى",reply_markup=back_kb(uid)); return

        # ===== جزية =====
        if d=="pay_tribute":
            today=datetime.now().strftime("%Y-%m-%d")
            if user["tribute_paid"]==today: await safe_edit(q,"دفعت الجزية النهاردة",reply_markup=user_kb(uid)); return
            amt=data['kingdom']['jizya']
            if user["balance"]<amt: await safe_edit(q,f"الجزية {amt} ج - فلوسك مش كفاية",reply_markup=user_kb(uid)); return
            user["balance"]-=amt; data['kingdom']['treasury']+=amt; user["tribute_paid"]=today; save()
            await safe_edit(q,f"⛓️✅ دفعت الجزية {amt} ج للملك 👑",reply_markup=user_kb(uid))
            await safe_send(context.bot,KING_ID,f"⛓️ العبد `{uid}` دفع الجزية {amt} ج 👑"); return

        # ===== كازينو وعجلة =====
        if d=="casino":
            await safe_edit(q,"🎰 **كازينو الرياض**\nالملك بياخد عمولة من كل لعبة 👑",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎰 العب 100",callback_data="casino_100"),InlineKeyboardButton("🎰 العب 500",callback_data="casino_500")],[InlineKeyboardButton("🎰 العب 1000",callback_data="casino_1000")],[InlineKeyboardButton("🔙 رجوع",callback_data="back")]])); return
        if d.startswith("casino_"):
            amt=int(d.split("_")[1])
            if user["balance"]<amt: await safe_edit(q,"فلوسك مش كفاية",reply_markup=back_kb(uid)); return
            user["balance"]-=amt
            if random.random()<0.4: win=amt*2; user["balance"]+=win; data['kingdom']['treasury']+=amt; save(); await safe_edit(q,f"🎰🎉 كسبت {win:,}!",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎰 العب تاني",callback_data="casino")],[InlineKeyboardButton("🔙 رجوع",callback_data="back")]]))
            else: data['kingdom']['treasury']+=amt; save(); await safe_edit(q,f"🎰 خسرت {amt} - جرب تاني",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎰 العب تاني",callback_data="casino")],[InlineKeyboardButton("🔙 رجوع",callback_data="back")]]))
            return
        if d=="wheel":
            today=datetime.now().strftime("%Y-%m-%d")
            if user["daily_last"]==today and user.get("wheel_done")==today: await safe_edit(q,"لفيت العجلة النهاردة",reply_markup=back_kb(uid)); return
            user["wheel_done"]=today; r=random.choice([100,200,500,1000,0,0]); user["balance"]+=r; save(); await safe_edit(q,f"🎡 لفيت العجلة وكسبت {r} ج!",reply_markup=back_kb(uid)); return
        if d=="daily":
            today=datetime.now().strftime("%Y-%m-%d")
            if user["daily_last"]==today: await safe_edit(q,"خدت هديتك النهاردة 🎁",reply_markup=back_kb(uid)); return
            r=random.randint(100,500)*(2 if user["vip"] else 1); user["balance"]+=r; user["daily_last"]=today; user["coins"]+=1; save(); await safe_edit(q,f"🎁 خدت {r:,} + 1 كوين!",reply_markup=back_kb(uid)); return
        if d=="top":
            s=sorted(users.values(),key=lambda x: x["balance"]+x["bank"]+x["savings"],reverse=True)[:10]; txt="🏆 **اغنى 10 في المملكة:**\n\n"
            for i,u in enumerate(s,1): txt+=f"{i}. {RANKS[u['rank']]['name']} @{u['username'] or u['id']} - {u['balance']+u['bank']+u['savings']:,} ج\n"
            await safe_edit(q,txt,reply_markup=back_kb(uid)); return

        # ===== شات =====
        if d=="live_start":
            if uid in states: states.pop(uid)
            if data.get("operator_status")=="offline" and uid!=str(KING_ID): await safe_edit(q,"🔴 الديوان اوفلاين.\nاعمل شكوى او اطلب مكالمة.",reply_markup=back_kb(uid)); return
            if uid in live_chats: await safe_edit(q,"انت already في شات مباشر 💬 ابعت رسالتك.",reply_markup=live_kb()); return
            if data.get("operator_status")=="busy" and uid!=str(KING_ID):
                if uid not in data["queue"]: data["queue"].append(uid); save()
                await safe_edit(q,f"🟡 الديوان مشغول.\n⏳ رقمك: {data['queue'].index(uid)+1}",reply_markup=back_kb(uid)); return
            live_chats[uid]={"started":datetime.now().strftime("%H:%M"),"username":q.from_user.username or "","type":"live"}; save()
            await safe_edit(q,"💬 **انت في شات مباشر مع الديوان** 🟢\nابعت نص / صورة / فويس - هيوصل للملك والديوان على طول.",reply_markup=live_kb())
            for sid in SUPPORT_IDS:
                try: await context.bot.send_message(chat_id=sid,text=f"🔴 **رعية دخلت شات مباشر!**\nمن: @{q.from_user.username or uid} - `{uid}` - {RANKS[user['rank']]['name']}\n\nدوس 💬 شاتات مباشرة عشان ترد",parse_mode="Markdown")
                except: pass
            return
        if d=="live_king":
            live_chats[uid]={"started":datetime.now().strftime("%H:%M"),"username":q.from_user.username or "","type":"king"}; save()
            await safe_edit(q,"👑 **انت في شات مع الملك**\nابعت رسالتك - الملك هيشوفها.",reply_markup=live_kb())
            await safe_send(context.bot,KING_ID,f"👑 **حد عايز يكلمك يا ملك!**\nمن: @{q.from_user.username or uid} - `{uid}`")
            return
        if d=="live_end":
            if uid in live_chats: del live_chats[uid]; save()
            if uid in data.get("queue",[]): data["queue"].remove(uid); save()
            await safe_edit(q,"⏹️ انهيت المحادثة 💙",reply_markup=back_kb(uid)); return
        if d=="live_active":
            if int(uid) not in SUPPORT_IDS: return
            if not live_chats: await safe_edit(q,"مفيش شاتات ✅",reply_markup=vizier_kb() if uid==str(MR_CAT_ID) else king_kb()); return
            kb=[]
            for cid,info in live_chats.items():
                kb.append([InlineKeyboardButton(f"💬 @{info.get('username','')} - `{cid}`",callback_data=f"reply_live_{cid}")])
            kb.append([InlineKeyboardButton("🔙 رجوع",callback_data="back")])
            await safe_edit(q,"💬 **شاتات مباشرة - دوس على واحد عشان ترد:**",reply_markup=InlineKeyboardMarkup(kb)); return
        if d.startswith("reply_live_"):
            tid=d.replace("reply_live_",""); data.setdefault("temp",{})[uid]={"reply_live":tid}; states[uid]="waiting_reply_live"; save()
            await safe_edit(q,f"💬 هترد على `{tid}`\nاكتب ردك في رسالة:")
            return
        if d=="shura":
            txt="👥 **مجلس الشورى**\n\nاخر الرسايل:\n\n"
            for m in data["shura"][-5:]: txt+=f"@{m['username']}: {m['text'][:50]}\n"
            txt+="\nدوس 💬 ادخل الشورى عشان تتكلم"
            await safe_edit(q,txt,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💬 ادخل الشورى",callback_data="shura_join")],[InlineKeyboardButton("🔙 رجوع",callback_data="back")]])); return
        if d=="shura_join":
            live_chats[uid]={"started":datetime.now().strftime("%H:%M"),"username":q.from_user.username or "","type":"shura"}; save()
            await safe_edit(q,"👥 **دخلت مجلس الشورى**\nابعت رسالتك - الكل هيشوفها والملك هيشوفها.",reply_markup=live_kb()); return

        # ===== تيكتات وقضايا =====
        if d=="new_ticket": states[uid]="waiting_ticket"; save(); await safe_edit(q,"📩 اكتب شكواك في رسالة واحدة:"); return
        if d=="my_tickets":
            my=[t for t in tickets.values() if t["user_id"]==uid]
            if not my: await safe_edit(q,"مفيش شكاوى",reply_markup=back_kb(uid)); return
            txt="📋 **شكاويك:**\n\n"
            for t in my[-5:]: txt+=f"#{t['id']} - {t['status']} - {t['text'][:50]}\n"
            await safe_edit(q,txt,reply_markup=back_kb(uid)); return
        if d=="support_open":
            if int(uid) not in SUPPORT_IDS: return
            open_t=[t for t in tickets.values() if t["status"]=="open"]
            if not open_t: await safe_edit(q,"مفيش شكاوى ✅",reply_markup=vizier_kb()); return
            kb=[]
            for t in open_t[-8:]: kb.append([InlineKeyboardButton(f"#{t['id']} - @{t['username']} - {t['text'][:30]}",callback_data=f"reply_ticket_{t['id']}")])
            kb.append([InlineKeyboardButton("🔙 رجوع",callback_data="back")])
            await safe_edit(q,"📋 **شكاوى - دوس على واحدة عشان ترد:**",reply_markup=InlineKeyboardMarkup(kb)); return
        if d.startswith("reply_ticket_"):
            tid=d.replace("reply_ticket_",""); data.setdefault("temp",{})[uid]={"reply_ticket":tid}; states[uid]="waiting_reply_ticket"; save()
            await safe_edit(q,f"💬 هترد على تيكت #{tid}\nاكتب ردك:")
            return
        if d=="quick_replies":
            await safe_edit(q,"💬 **ردود جاهزة - دوس عشان تبعت:**",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("اهلا بيك، هنحل مشكلتك حالا",callback_data="quick_1")],[InlineKeyboardButton("ابعتلي التفاصيل",callback_data="quick_2")],[InlineKeyboardButton("تم حل مشكلتك ✅",callback_data="quick_3")],[InlineKeyboardButton("🔙 رجوع",callback_data="back")]])); return
        if d.startswith("quick_"):
            await safe_edit(q,"اختار شات او تيكت من القايمة عشان تبعت الرد الجاهز",reply_markup=vizier_kb()); return
        if d=="file_case":
            kb=[]
            for u in list(users.values())[:10]:
                if str(u["id"])==uid: continue
                kb.append([InlineKeyboardButton(f"@{u['username'] or u['id']} - {RANKS[u['rank']]['name']}",callback_data=f"case_to_{u['id']}")])
            kb.append([InlineKeyboardButton("🔙 رجوع",callback_data="back")])
            await safe_edit(q,"⚖️ **ارفع قضية - اختار المتهم:**",reply_markup=InlineKeyboardMarkup(kb)); return
        if d.startswith("case_to_"):
            tid=d.replace("case_to_",""); data.setdefault("temp",{})[uid]={"case_target":tid}
            await safe_edit(q,"⚖️ اختار التهمة:",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🥷 سرقة",callback_data="case_reason_سرقة"),InlineKeyboardButton("🤬 سب",callback_data="case_reason_سب")],[InlineKeyboardButton("💰 نصب",callback_data="case_reason_نصب"),InlineKeyboardButton("👑 اهانة الملك",callback_data="case_reason_اهانة الملك")]])); return
        if d.startswith("case_reason_"):
            reason=d.replace("case_reason_",""); data.setdefault("temp",{}).setdefault(uid,{})["case_reason"]=reason; states[uid]="waiting_case_text"; save()
            await safe_edit(q,f"⚖️ التهمة: {reason}\nاكتب تفاصيل القضية:"); return
        if d=="courts":
            if not data["courts"]: await safe_edit(q,"مفيش قضايا ✅",reply_markup=king_kb() if uid==str(KING_ID) else back_kb(uid)); return
            kb=[]
            for c in data["courts"][-8:]:
                if c["status"]=="open": kb.append([InlineKeyboardButton(f"قضية #{c['id']} - {c['reason']} - `{c['from']}` ضد `{c['to']}`",callback_data=f"judge_{c['id']}")])
            kb.append([InlineKeyboardButton("🔙 رجوع",callback_data="back")])
            await safe_edit(q,"⚖️ **قضايا مفتوحة - دوس عشان تحكم:**",reply_markup=InlineKeyboardMarkup(kb)); return
        if d.startswith("judge_"):
            if uid!=str(KING_ID): await safe_edit(q,"بس الملك اللي يحكم 👑",reply_markup=back_kb(uid)); return
            cid=d.replace("judge_",""); c=next((x for x in data["courts"] if x["id"]==cid),None)
            if not c: return
            await safe_edit(q,f"⚖️ **قضية #{cid}**\nمن: `{c['from']}` ضد `{c['to']}`\nالتهمة: {c['reason']}\nالتفاصيل: {c['text']}\n\nاحكم:",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ براءة",callback_data=f"verdict_{cid}_free"),InlineKeyboardButton("💰 غرامة",callback_data=f"verdict_{cid}_fine")],[InlineKeyboardButton("⛓️ سجن",callback_data=f"verdict_{cid}_jail"),InlineKeyboardButton("🔨 حظر",callback_data=f"verdict_{cid}_ban")],[InlineKeyboardButton("🔙 رجوع",callback_data="courts")]])); return
        if d.startswith("verdict_"):
            if uid!=str(KING_ID): return
            _,cid,verdict=d.split("_"); c=next((x for x in data["courts"] if x["id"]==cid),None)
            if not c: return
            c["status"]="closed"; t=get_user(c["to"]); save()
            if verdict=="free": await safe_send(context.bot,int(c["to"]),"⚖️ الملك حكم ببراءتك 👑")
            if verdict=="fine": t["balance"]=max(0,t["balance"]-500); data['kingdom']['treasury']+=500; save(); await safe_send(context.bot,int(c["to"]),"⚖️ الملك حكم عليك بغرامة 500")
            if verdict=="jail": t["jailed_until"]=time.time()+3600; save(); await safe_send(context.bot,int(c["to"]),"⚖️ الملك حكم عليك بسجن 1 ساعة")
            if verdict=="ban": t["banned"]=True; save(); await safe_send(context.bot,int(c["to"]),"⚖️ الملك حكم عليك بالحظر")
            await safe_edit(q,f"⚖️ حكمت في قضية #{cid} - {verdict}",reply_markup=king_kb()); return
        if d=="file_report":
            await safe_edit(q,"👮 **بلاغ - اختار اللي هتبلغ عنه:**",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("👥 كل الرعايا",callback_data="king_users")],[InlineKeyboardButton("🔙 رجوع",callback_data="back")]])); return
        if d=="request_call": states[uid]="waiting_name"; save(); await safe_edit(q,"📞 **طلب مكالمة**\nاكتب اسمك:"); return
        if d=="callback_list":
            if int(uid) not in SUPPORT_IDS: return
            cbs=[c for c in data.get("callbacks",[]) if not c["done"]]
            if not cbs: await safe_edit(q,"مفيش طلبات",reply_markup=vizier_kb()); return
            txt="📞 **طلبات مكالمات:**\n\n"
            for c in cbs[-10:]: txt+=f"👤 {c['name']} - {c['phone']} - `{c['user_id']}`\n"
            await safe_edit(q,txt,reply_markup=vizier_kb()); return
        if d=="queue_list":
            if int(uid) not in SUPPORT_IDS: return
            qlist=data.get("queue",[])
            if not qlist: await safe_edit(q,"الطابور فاضي ✅",reply_markup=vizier_kb()); return
            txt="⏳ **طابور:**\n\n"
            for i,cid in enumerate(qlist,1): txt+=f"{i}. `{cid}`\n"
            await safe_edit(q,txt,reply_markup=vizier_kb()); return
        if d=="faq": await safe_edit(q,"❓ **اسئلة:**\n\n💰 الشحن: كلم الديوان\n⏰ المواعيد: 10ص - 12م\n📜 القانون: الملك هو القانون 👑",reply_markup=back_kb(uid)); return
        if d=="rate": states[uid]="waiting_rate"; save(); await safe_edit(q,"⭐ قيمنا 1-5 - ابعت رقم:"); return
        if d=="support_stats":
            if int(uid) not in SUPPORT_IDS: return
            await safe_edit(q,f"📊 **احصائيات:**\n\n👥 رعايا: {len(users)}\n💬 شات: {len(live_chats)}\n💰 خزينة: {data['kingdom']['treasury']:,}",reply_markup=vizier_kb()); return
        if d in ["set_online","set_busy","set_offline"]:
            if int(uid) not in SUPPORT_IDS: return
            mp={"set_online":"online","set_busy":"busy","set_offline":"offline"}; data["operator_status"]=mp[d]; save(); await safe_edit(q,f"✅ حالتك: {mp[d]}",reply_markup=vizier_kb()); return
        if d=="support_panel":
            if int(uid) not in SUPPORT_IDS: return
            await safe_edit(q,"🎧 **لوحة الدعم**",reply_markup=vizier_kb() if uid==str(MR_CAT_ID) else king_kb()); return

    except Exception as e:
        print(f"BTN ERR {e}"); traceback.print_exc()
        try: await q.message.reply_text("اكتب /start 👑")
        except: pass

async def error_handler(update,context): print(f"ERROR {context.error}")
def main():
    if not TOKEN:
        print("❌ BOT_TOKEN مش موجود!"); 
        while True: time.sleep(60)
    while True:
        try:
            print("🚀 KINGDOM SAUDI BOT STARTING...")
            app=ApplicationBuilder().token(TOKEN).build()
            app.add_handler(CommandHandler("start",start))
            app.add_handler(CallbackQueryHandler(buttons))
            app.add_handler(MessageHandler((filters.TEXT|filters.PHOTO|filters.VOICE)&~filters.COMMAND,on_msg))
            app.add_error_handler(error_handler)
            print("✅ KINGDOM SAUDI STARTED 👑🇸🇦"); app.run_polling(drop_pending_updates=True,allowed_updates=Update.ALL_TYPES)
        except Exception as e: print(f"CRASH {e}"); time.sleep(3)
if __name__=="__main__": main()
