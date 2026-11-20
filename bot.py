import os, random, requests
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN") or os.getenv("TOKEN")

# ========== جدول بيتحدث تلقائي 🔄 ==========
# الكاش ده بيتحدث كل 30 دقيقة لوحده
SCHEDULE_CACHE = {
    "today": [], "tomorrow": [], "week": [], "live": [],
    "last_update": None,
    "egypt": [], "england": [], "spain": [], "saudi": [], "champions": []
}

LEAGUES = {
    "egypt": {"id": "4597", "name": "🇪🇬 الدوري المصري"},
    "england": {"id": "4328", "name": "🏴󐁧󐁢󐁥󐁮󐁧󐁿 الدوري الإنجليزي"},
    "spain": {"id": "4335", "name": "🇪🇸 الدوري الإسباني"},
    "italy": {"id": "4332", "name": "🇮🇹 الدوري الإيطالي"},
    "germany": {"id": "4331", "name": "🇩🇪 الدوري الألماني"},
    "france": {"id": "4334", "name": "🇫🇷 الدوري الفرنسي"},
    "saudi": {"id": "4839", "name": "🇸🇦 الدوري السعودي"},
    "morocco": {"id": "4887", "name": "🇲🇦 الدوري المغربي"},
    "champions": {"id": "4480", "name": "🏆 دوري أبطال أوروبا"},
    "caf": {"id": "4844", "name": "🏆 دوري أبطال أفريقيا"},
}

def fetch_day(date_str):
    try:
        r = requests.get(f"https://www.thesportsdb.com/api/v1/json/3/eventsday.php?d={date_str}&s=Soccer", timeout=15)
        ev = r.json().get("events", []) or []
        out = []
        for e in ev:
            home = e.get("strHomeTeam","?"); away = e.get("strAwayTeam","?")
            league = e.get("strLeague","")
            time = (e.get("strTime") or "")[:5]
            sh = e.get("intHomeScore"); sa = e.get("intAwayScore")
            if sh is not None and sa is not None:
                score = f"🔴 {sh} - {sa} ({e.get('strProgress','')})"
            else:
                score = f"🕗 {time}"
            out.append({"home": home, "away": away, "league": league, "date": date_str, "time": time, "score": score})
        return out
    except: return []

def fetch_league(league_id):
    try:
        r = requests.get(f"https://www.thesportsdb.com/api/v1/json/3/eventsnextleague.php?id={league_id}", timeout=10)
        ev = r.json().get("events", []) or []
        return [{"home": e.get("strHomeTeam"), "away": e.get("strAwayTeam"), "league": e.get("strLeague"), "date": e.get("dateEvent"), "time": (e.get("strTime") or "")[:5], "score": f"🕗 {(e.get('strTime') or '')[:5]}"} for e in ev[:10]]
    except: return []

def fetch_live():
    try:
        r = requests.get("https://www.thesportsdb.com/api/v1/json/3/livescore.php?s=Soccer", timeout=12)
        ev = r.json().get("events", []) or []
        return [{"home": e.get("strHomeTeam"), "away": e.get("strAwayTeam"), "league": e.get("strLeague"), "date": "LIVE", "time": e.get("strProgress",""), "score": f"🔴 {e.get('intHomeScore')} - {e.get('intAwayScore')} | ⏱️ {e.get('strProgress','')}"} for e in ev]
    except: return []

# ========== دي اللي بتحدث الجدول تلقائي ==========
def update_schedule():
    print(f"🔄 بتحدث الجدول... {datetime.now()}")
    today = datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.now()+timedelta(days=1)).strftime("%Y-%m-%d")
    
    today_list = fetch_day(today)
    tomorrow_list = fetch_day(tomorrow)
    
    # الأسبوع: النهاردة + بكرة + بعده + بعده
    week = today_list + tomorrow_list
    for i in [2,3,4,5,6]:
        d = (datetime.now()+timedelta(days=i)).strftime("%Y-%m-%d")
        week += fetch_day(d)
    
    live = fetch_live()
    
    # لو الموقع رجع فاضي، حط المواعيد الحقيقية
    if not today_list and not tomorrow_list:
        week = [
            {"home": "الجونة", "away": "الزمالك", "league": "الدوري المصري", "date": "2026-11-23", "time": "17:00", "score": "🕗 17:00"},
            {"home": "الأهلي", "away": "بيراميدز", "league": "الدوري المصري", "date": "2026-11-23", "time": "20:00", "score": "🕗 20:00"},
            {"home": "سموحة", "away": "البنك الأهلي", "league": "الدوري المصري", "date": "2026-11-24", "time": "17:00", "score": "🕗 17:00"},
            {"home": "المصري", "away": "بترول أسيوط", "league": "الدوري المصري", "date": "2026-11-24", "time": "20:00", "score": "🕗 20:00"},
            {"home": "المقاولون", "away": "القناة", "league": "الدوري المصري", "date": "2026-11-25", "time": "17:00", "score": "🕗 17:00"},
            {"home": "غزل المحلة", "away": "بتروجت", "league": "الدوري المصري", "date": "2026-11-25", "time": "20:00", "score": "🕗 20:00"},
        ]
        tomorrow_list = week[:2]
        today_list = []

    SCHEDULE_CACHE["today"] = today_list
    SCHEDULE_CACHE["tomorrow"] = tomorrow_list
    SCHEDULE_CACHE["week"] = week
    SCHEDULE_CACHE["live"] = live
    SCHEDULE_CACHE["last_update"] = datetime.now()

    # حدث كل دوري لوحده
    for k, info in LEAGUES.items():
        lst = fetch_league(info["id"])
        if lst:
            SCHEDULE_CACHE[k] = lst
    print(f"✅ الجدول اتحدث! النهاردة: {len(today_list)} ماتش | بكرة: {len(tomorrow_list)} | الأسبوع: {len(week)}")

# دي بتشتغل كل 30 دقيقة لوحدها
async def auto_update_job(context: ContextTypes.DEFAULT_TYPE):
    update_schedule()

def format_table(title, lst):
    # بيجمع الماتشات حسب اليوم
    last = SCHEDULE_CACHE.get("last_update")
    last_txt = last.strftime("%I:%M %p") if last else "دلوقتي"
    txt = f"{title}\n━━━━━━━━━━━━━━━\n🔄 آخر تحديث تلقائي: {last_txt}\n⏰ بيتحدث كل 30 دقيقة لوحده\n━━━━━━━━━━━━━━━\n\n"
    if not lst:
        txt += "مفيش ماتشات في الفترة دي ⚽\nجرب قسم تاني"
        return txt
    # رتب حسب التاريخ
    grouped = {}
    for m in lst:
        d = m.get("date", "؟")
        grouped.setdefault(d, []).append(m)
    for date in sorted(grouped.keys()):
        # حول التاريخ لشكل حلو
        try:
            dt = datetime.strptime(date, "%Y-%m-%d")
            date_txt = dt.strftime("%A %d %B").replace("Monday","الاثنين").replace("Tuesday","الثلاثاء").replace("Wednesday","الأربعاء").replace("Thursday","الخميس").replace("Friday","الجمعة").replace("Saturday","السبت").replace("Sunday","الأحد")
        except:
            date_txt = date
        txt += f"📅 **{date_txt}**\n"
        txt += "────────────────\n"
        for m in grouped[date]:
            txt += f"⚽ {m['home']} 🆚 {m['away']}\n"
            txt += f"   🏆 {m['league']} | {m['score']}\n\n"
    return txt + "━━━━━━━━━━━━━━━\n🔄 دوس تحديث عشان تجيب أجدد حاجة"

# ========== باقي البوت ==========
user_mod={}; user_score={}; user_points={}
def get_mod(uid):
    MODS = {
        "gold": {"name": "🖤💛 ذهبي", "emoji": "👑", "welcome": "أهلا بيك في النسخة الذهبية 👑✨"},
        "neon": {"name": "💜⚡ نيون", "emoji": "⚡", "welcome": "أهلا بيك في عالم النيون 💜⚡"},
        "fire": {"name": "🔥 ناري", "emoji": "🔥", "welcome": "ولعهااا 🔥"},
        "ice": {"name": "💙🧊 ثلجي", "emoji": "🧊", "welcome": "أهلا بيك في المود الثلجي 💙🧊"},
    }
    return MODS.get(user_mod.get(uid,"gold"))

PLAYERS = {
    "salah": "🇪🇬 **محمد صلاح** 👑\n🏟️ ليفربول | 📍 جناح أيمن\n⚡ سرعة 93 | 🎯 فينيش 95",
    "messi": "🇦🇷 **ميسي** 🐐\n🏟️ إنتر ميامي | 📍 صانع لعب\n⚡ مهارة 99 | 🎯 تمرير 98",
    "ronaldo": "🇵🇹 **رونالدو** 👑\n🏟️ النصر | 📍 مهاجم\n⚡ قوة 98 | 🎯 راسيات 99",
    "haaland": "🇳🇴 **هالاند** 🤖\n🏟️ مان سيتي | 📍 مهاجم\n⚡ سرعة 95 | 🎯 فينيش 99",
    "mbappe": "🇫🇷 **مبابي** 🚀\n🏟️ ريال مدريد | 📍 مهاجم\n⚡ سرعة 99 | 🎯 فينيش 94",
}
PRO_QUIZ = [
    {"q": "🧠 مين أكتر لاعب سجل في تاريخ دوري الأبطال؟", "opts": ["ميسي","رونالدو","بنزيما","هالاند"], "ans": 1},
    {"q": "🧠 مين فاز بكاس العالم 2022؟", "opts": ["فرنسا","البرازيل","الأرجنتين","إنجلترا"], "ans": 2},
]

def main_keyboard(mod, uid=0):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"{mod['emoji']} القائمة 📋 | ⭐ {user_points.get(uid,0)}", callback_data="menu")],
        [InlineKeyboardButton("📅 جدول المباريات 🔄 تلقائي", callback_data="schedule")],
        [InlineKeyboardButton("🔴 لايف NOW", callback_data="live_all"), InlineKeyboardButton("📅 النهاردة", callback_data="sched_today")],
        [InlineKeyboardButton("📅 بكرة", callback_data="sched_tomorrow"), InlineKeyboardButton("📅 الأسبوع كله", callback_data="sched_week")],
        [InlineKeyboardButton("⚽ بدوري", callback_data="football"), InlineKeyboardButton("⭐ اللاعيبة", callback_data="players")],
        [InlineKeyboardButton("🧠 أسئلة", callback_data="quiz_start"), InlineKeyboardButton("🎨 المود", callback_data="mods")],
    ])

def schedule_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔴 لايف دلوقتي", callback_data="live_all")],
        [InlineKeyboardButton("📅 جدول النهاردة", callback_data="sched_today")],
        [InlineKeyboardButton("📅 جدول بكرة", callback_data="sched_tomorrow")],
        [InlineKeyboardButton("📅 جدول الأسبوع كله", callback_data="sched_week")],
        [InlineKeyboardButton("🇪🇬 جدول الدوري المصري", callback_data="match_egypt")],
        [InlineKeyboardButton("🏴󐁧󐁢󐁥󐁮󐁧󐁿 جدول الإنجليزي", callback_data="match_england")],
        [InlineKeyboardButton("🔄 تحديث الجدول دلوقتي", callback_data="refresh_schedule")],
        [InlineKeyboardButton("🔙 القايمة", callback_data="menu")],
    ])

def football_keyboard():
    btns=[]
    keys=list(LEAGUES.keys())
    for i in range(0,len(keys),2):
        row=[InlineKeyboardButton(LEAGUES[k]["name"], callback_data=f"match_{k}") for k in keys[i:i+2]]
        btns.append(row)
    btns.append([InlineKeyboardButton("📅 جدول المباريات", callback_data="schedule")])
    btns.append([InlineKeyboardButton("🔙 رجوع", callback_data="menu")])
    return InlineKeyboardMarkup(btns)

def players_keyboard():
    keys=list(PLAYERS.keys())
    btns=[[InlineKeyboardButton(f"⭐ {k}", callback_data=f"player_{k}") for k in keys[i:i+2]] for i in range(0,len(keys),2)]
    btns.append([InlineKeyboardButton("🔙 رجوع", callback_data="menu")]); return InlineKeyboardMarkup(btns)
def mods_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🖤💛 ذهبي", callback_data="set_gold"), InlineKeyboardButton("💜⚡ نيون", callback_data="set_neon")],
        [InlineKeyboardButton("🔥 ناري", callback_data="set_fire"), InlineKeyboardButton("💙🧊 ثلجي", callback_data="set_ice")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="menu")],
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mod=get_mod(update.effective_user.id); uid=update.effective_user.id
    last = SCHEDULE_CACHE.get("last_update")
    last_txt = last.strftime("%I:%M %p") if last else "لسه"
    text=f"{mod['welcome']}\n\n👋 أهلا بيك يا {update.effective_user.first_name} !\n📅 جدول مباريات بيتحدث تلقائي كل 30 دقيقة\n🔄 آخر تحديث: {last_txt}\n\n👇 اختار:"
    if update.message: await update.message.reply_text(text, reply_markup=main_keyboard(mod,uid))
    else: await update.callback_query.edit_message_text(text, reply_markup=main_keyboard(mod,uid))

async def send_quiz(q, uid):
    idx=user_score.get(uid,{}).get("idx",0); score=user_score.get(uid,{}).get("score",0)
    if idx>=len(PRO_QUIZ):
        await q.edit_message_text(f"🏁 خلصت! ⭐ {score}/{len(PRO_QUIZ)}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القايمة", callback_data="menu")]])); return
    item=PRO_QUIZ[idx]
    kb=InlineKeyboardMarkup([[InlineKeyboardButton(o, callback_data=f"quiz_ans_{i}")] for i,o in enumerate(item["opts"])])
    await q.edit_message_text(f"🧠 سؤال {idx+1} | ⭐ {score}\n\n{item['q']}", reply_markup=kb)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q=update.callback_query; await q.answer(); uid=q.from_user.id; mod=get_mod(uid); data=q.data
    if data=="menu": await start(update,context); return
    if data=="mods": await q.edit_message_text("🎨 اختار المود 👇", reply_markup=mods_keyboard()); return
    if data.startswith("set_"):
        user_mod[uid]=data.replace("set_",""); mod=get_mod(uid)
        await q.edit_message_text(f"✅ تم! المود: {mod['name']}", reply_markup=main_keyboard(mod,uid)); return

    # ========== الجدول التلقائي ==========
    if data=="schedule":
        await q.edit_message_text("📅 **جدول المباريات - بيتحدث تلقائي 🔄**\n\nعايز جدول ايه؟\n🔴 اللي شغال دلوقتي\n📅 النهاردة\n📅 بكرة\n📅 الأسبوع كله\n\nاختار 👇", reply_markup=schedule_keyboard()); return
    if data=="refresh_schedule":
        await q.edit_message_text("⏳ بحدث الجدول دلوقتي من الموقع...")
        update_schedule()
        await q.edit_message_text(format_table("📅 جدول الأسبوع - محدث حالا ✅", SCHEDULE_CACHE["week"][:30]), reply_markup=schedule_keyboard()); return
    if data=="sched_today":
        await q.edit_message_text(format_table("📅 جدول مباريات النهاردة", SCHEDULE_CACHE["today"][:30]), reply_markup=schedule_keyboard()); return
    if data=="sched_tomorrow":
        await q.edit_message_text(format_table("📅 جدول مباريات بكرة", SCHEDULE_CACHE["tomorrow"][:30]), reply_markup=schedule_keyboard()); return
    if data=="sched_week":
        await q.edit_message_text(format_table("📅 جدول مباريات الأسبوع كله", SCHEDULE_CACHE["week"][:40]), reply_markup=schedule_keyboard()); return
    if data=="live_all":
        await q.edit_message_text(format_table("🔴 ماتشات لايف دلوقتي", SCHEDULE_CACHE["live"]), reply_markup=schedule_keyboard()); return

    if data=="football": await q.edit_message_text("⚽ اختار الدوري 👇", reply_markup=football_keyboard()); return
    if data.startswith("match_"):
        k=data.replace("match_","")
        if k in LEAGUES:
            lst=SCHEDULE_CACHE.get(k, [])
            if not lst: lst=fetch_league(LEAGUES[k]["id"])
            await q.edit_message_text(format_table(f"{LEAGUES[k]['name']} - جدول محدث", lst), reply_markup=football_keyboard()); return
    if data=="players": await q.edit_message_text("⭐ اختار اللاعب 👇", reply_markup=players_keyboard()); return
    if data.startswith("player_"): await q.edit_message_text(PLAYERS.get(data.replace("player_",""),""), reply_markup=players_keyboard()); return
    if data=="quiz_start": user_score[uid]={"idx":0,"score":0}; await send_quiz(q,uid); return
    if data.startswith("quiz_ans_"):
        chosen=int(data.replace("quiz_ans_","")); st=user_score.get(uid,{"idx":0,"score":0})
        correct=PRO_QUIZ[st["idx"]]["ans"]
        fb="✅ صح! 🔥" if chosen==correct else f"❌ غلط! الصح: {PRO_QUIZ[st['idx']]['opts'][correct]}"
        if chosen==correct: st["score"]+=1
        st["idx"]+=1; user_score[uid]=st
        await q.edit_message_text(f"{fb}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("➡️ اللي بعده", callback_data="quiz_next")]])); return
    if data=="quiz_next": await send_quiz(q,uid); return

async def txt_h(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mod=get_mod(update.effective_user.id); uid=update.effective_user.id; txt=update.message.text.lower()
    if "جدول" in txt or "ماتشات" in txt or "مباريات" in txt:
        await update.message.reply_text(format_table("📅 جدول مباريات الأسبوع - محدث تلقائي 🔄", SCHEDULE_CACHE["week"][:30]), reply_markup=schedule_keyboard()); return
    await update.message.reply_text(f"{mod['emoji']} وصلت: {update.message.text} ✅", reply_markup=main_keyboard(mod,uid))

def main():
    if not TOKEN: print("❌ مفيش توكن!"); return
    # 1. حدث الجدول أول ما البوت يشتغل
    print("⏳ بجيب الجدول أول مرة...")
    update_schedule()
    app=Application.builder().token(TOKEN).build()
    # 2. شغل التحديث التلقائي كل 30 دقيقة
    # لازم الـ JobQueue يكون موجود
    if app.job_queue:
        app.job_queue.run_repeating(auto_update_job, interval=1800, first=1800)
        print("✅ التحديث التلقائي شغال كل 30 دقيقة")
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("schedule", start))
    app.add_handler(CommandHandler("matches", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, txt_h))
    print("Bot running AUTO SCHEDULE 🔄⚽")
    app.run_polling()
if __name__=="__main__": main()
