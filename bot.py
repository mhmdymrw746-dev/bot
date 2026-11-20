import os, random, requests
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

TOKEN = os.getenv("BOT_TOKEN")

# ========== الموقع اللي بنسحب منه ⚽ ==========
# TheSportsDB - مجاني ومن غير مفتاح
# لو الموقع وقع، البوت هيرجع للمواعيد القديمة تلقائي
LEAGUES = {
    "egypt": {"id": "4597", "name": "🇪🇬 الدوري المصري", "emoji": "🇪🇬"},
    "england": {"id": "4328", "name": "🏴󐁧󐁢󐁥󐁮󐁧󐁿 الدوري الإنجليزي", "emoji": "🏴󐁧󐁢󐁥󐁮󐁧󐁿"},
    "spain": {"id": "4335", "name": "🇪🇸 الدوري الإسباني", "emoji": "🇪🇸"},
    "champions": {"id": "4480", "name": "🏆 دوري الأبطال", "emoji": "🏆"},
    "italy": {"id": "4332", "name": "🇮🇹 الدوري الإيطالي", "emoji": "🇮🇹"},
    "germany": {"id": "4331", "name": "🇩🇪 الدوري الألماني", "emoji": "🇩🇪"},
    "saudi": {"id": "4839", "name": "🇸🇦 الدوري السعودي", "emoji": "🇸🇦"},
}

# مواعيد احتياطية لو النت وقع
FALLBACK = {
    "egypt": [("⚽ الأهلي 🆚 الزمالك", "🕗 8:00 م | 📺 ON Time")],
    "england": [("⚽ ليفربول 🆚 مان سيتي", "🕙 10:00 م | 📺 beIN")],
    "spain": [("⚽ ريال مدريد 🆚 برشلونة", "🕙 10:00 م | 📺 beIN")],
    "champions": [("⚽ ريال مدريد 🆚 بايرن", "🕙 10:00 م")],
    "italy": [("⚽ إنتر 🆚 ميلان", "🕙 9:45 م")],
    "germany": [("⚽ بايرن 🆚 دورتموند", "🕢 7:30 م")],
    "saudi": [("⚽ الهلال 🆚 النصر", "🕗 8:00 م")],
}

# كاش عشان منضربش الموقع كل ثانية
CACHE = {}
CACHE_TIME = {}

def fetch_from_site(league_id):
    """بيسحب الماتشات الجاية من الموقع"""
    try:
        # 1. الماتشات الجاية
        url = f"https://www.thesportsdb.com/api/v1/json/3/eventsnextleague.php?id={league_id}"
        r = requests.get(url, timeout=10)
        data = r.json()
        events = data.get("events", []) or []
        result = []
        for e in events[:8]:
            home = e.get("strHomeTeam", "?")
            away = e.get("strAwayTeam", "?")
            date = e.get("dateEvent", "")
            time = e.get("strTime", "")[:5] if e.get("strTime") else ""
            status = e.get("strStatus", "")
            venue = e.get("strVenue", "")
            score_home = e.get("intHomeScore")
            score_away = e.get("intAwayScore")
            if score_home is not None and score_away is not None:
                score = f" | 🔴 {score_home} - {score_away} {status}"
            else:
                score = ""
            result.append((f"⚽ {home} 🆚 {away}", f"🗓️ {date} | 🕗 {time}{score}\n🏟️ {venue}"))
        if result:
            return result
    except Exception as ex:
        print(f"Site error: {ex}")
    return []

def fetch_live():
    """بيسحب الماتشات اللي شغالة دلوقتي"""
    try:
        r = requests.get("https://www.thesportsdb.com/api/v1/json/3/livescore.php?l=4328&l=4335&l=4480&l=4597&s=Soccer", timeout=10)
        data = r.json()
        events = data.get("events", []) or []
        result = []
        for e in events[:10]:
            home = e.get("strHomeTeam"); away = e.get("strAwayTeam")
            sh = e.get("intHomeScore"); sa = e.get("intAwayScore")
            prog = e.get("strProgress", "")
            result.append((f"🔴 LIVE {home} {sh} - {sa} {away}", f"⏱️ الدقيقة: {prog} | 🏆 {e.get('strLeague')}"))
        return result
    except:
        return []

def get_matches(league_key):
    # لو لسه جايبينها من أقل من 5 دقايق، رجع الكاش
    now = datetime.now()
    if league_key in CACHE and (now - CACHE_TIME.get(league_key, now)).seconds < 300:
        return CACHE[league_key]
    live = fetch_from_site(LEAGUES[league_key]["id"])
    if not live:
        live = FALLBACK.get(league_key, [])
    CACHE[league_key] = live
    CACHE_TIME[league_key] = now
    return live

# ========== باقي البوت ==========
MODS = {
    "gold": {"name": "🖤💛 ذهبي", "emoji": "👑", "welcome": "أهلا بيك في النسخة الذهبية 👑✨"},
    "neon": {"name": "💜⚡ نيون", "emoji": "⚡", "welcome": "أهلا بيك في عالم النيون 💜⚡"},
    "fire": {"name": "🔥 ناري", "emoji": "🔥", "welcome": "ولعهااا 🔥"},
    "ice": {"name": "💙🧊 ثلجي", "emoji": "🧊", "welcome": "أهلا بيك في المود الثلجي 💙🧊"},
}
user_mod = {}; user_score = {}
def get_mod(uid): return MODS.get(user_mod.get(uid, "gold"))

PLAYERS = {
    "salah": "🇪🇬 **محمد صلاح** 👑\n🏟️ ليفربول | 📍 جناح أيمن\n⚡ سرعة 93 | 🎯 فينيش 95\n💪 المميز: بيقطع لجوه ويشوط بالشمال\n🏆 أبطال + دوري إنجليزي",
    "messi": "🇦🇷 **ميسي** 🐐\n🏟️ إنتر ميامي | 📍 صانع لعب\n⚡ مهارة 99 | 🎯 تمرير 98\n🏆 كاس عالم 2022 + 8 كرات ذهبية",
    "ronaldo": "🇵🇹 **رونالدو** 👑\n🏟️ النصر | 📍 مهاجم\n⚡ قوة 98 | 🎯 راسيات 99\n🏆 5 كرات ذهبية + 5 أبطال",
    "haaland": "🇳🇴 **هالاند** 🤖\n🏟️ مان سيتي | 📍 مهاجم\n⚡ سرعة 95 | 🎯 فينيش 99",
    "mbappe": "🇫🇷 **مبابي** 🚀\n🏟️ ريال مدريد | 📍 مهاجم\n⚡ سرعة 99 | 🎯 فينيش 94",
    "bellingham": "🏴󐁧󐁢󐁥󐁮󐁧󐁿 **بيلينجهام** 💎\n🏟️ ريال مدريد | 📍 وسط هجومي\n⚡ مهارة 92 | 🎯 تمرير 93",
    "vinicius": "🇧🇷 **فينيسيوس** ⚡\n🏟️ ريال مدريد | 📍 جناح أيسر\n⚡ سرعة 97 | 👟 مراوغة 96",
    "pedri": "🇪🇸 **بيدري** 🧠\n🏟️ برشلونة | 📍 وسط\n⚡ تمرير 96 | 👁️ رؤية 95",
}
PRO_QUIZ = [
    {"q": "🧠 مين أكتر لاعب سجل في تاريخ دوري الأبطال؟", "opts": ["ميسي", "رونالدو", "بنزيما", "هالاند"], "ans": 1},
    {"q": "🧠 امتى بيتحسب التسلل؟", "opts": ["لما يعدي نص الملعب", "لما يكون أقرب للجون من آخر مدافع وقت التمرير", "لما يلمسها بإيده", "لما يرجع لورا"], "ans": 1},
    {"q": "🧠 مين فاز بكاس العالم 2022؟", "opts": ["فرنسا", "البرازيل", "الأرجنتين", "إنجلترا"], "ans": 2},
    {"q": "🧠 يعني إيه خطة 4-3-3؟", "opts": ["4 دفاع 3 وسط 3 هجوم", "4 هجوم 3 دفاع", "4 حراس", "4 مهاجمين"], "ans": 0},
    {"q": "🧠 مين أكتر فريق كسب دوري أبطال؟", "opts": ["برشلونة", "ميلان", "ريال مدريد", "بايرن"], "ans": 2},
]
BASICS = {
    "positions": "📚 **مراكز اللاعيبة**\n🧤 حارس | 🛡️ مدافع | ⚙️ وسط | ⚽ مهاجم",
    "offside": "📚 **التسلل**\n❌ متسلل لو كنت أقرب للجون من آخر مدافع وقت التمرير\n✅ مش متسلل لو من الخصم / في نص ملعبك / من رمية تماس",
    "rules": "📚 **قواعد**\n⏱️ 90 دقيقة | 🟨 إنذارين = طرد | ⚽ مينفعش إيدك إلا الحارس",
    "tips": "📚 **تبقى محترف**\n1. ارفع راسك قبل التمرير\n2. اتحرك من غير كورة\n3. أول لمسة أهم حاجة\n4. اتمرن على رجلك الضعيفة",
    "formations": "📚 **التشكيلات**\n🔥 4-3-3 هجومي | 🛡️ 4-4-2 متوازن | 🧠 4-2-3-1 سيطرة",
    "tactics": "📚 **الخطط**\n🔥 ضغط عالي | 🚌 الباص | 🎯 استحواذ | ⚡ مرتدات",
    "training": "📚 **تمارين في البيت**\n🏃 جري 10 دقايق | 🦶 كنترول 50 مرة | 🎯 تمرير على الحيطة 100 مرة",
}
DAILY_TIPS = [
    "💡 نصيحة اليوم: أول لمسة هي اللي بتفرق بين لاعب عادي ومحترف.",
    "💡 نصيحة اليوم: متجريش ورا الكورة، اجري في المساحة الفاضية.",
    "💡 نصيحة اليوم: اللاعب المحترف بيعرف هيعمل ايه قبل ما الكورة توصله.",
]

def main_keyboard(mod):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"{mod['emoji']} القائمة الرئيسية 📋", callback_data="menu")],
        [InlineKeyboardButton("🔴 ماتشات لايف NOW", callback_data="live")],
        [InlineKeyboardButton("⚽ الكورة ومواعيدها 🏆", callback_data="football")],
        [InlineKeyboardButton("⭐ اللاعيبة", callback_data="players")],
        [InlineKeyboardButton("🧠 أسئلة المحترفين", callback_data="quiz_start"), InlineKeyboardButton("📚 مبادئ الكورة", callback_data="basics")],
        [InlineKeyboardButton("⚔️ قارن", callback_data="compare"), InlineKeyboardButton("💡 نصيحة اليوم", callback_data="tip")],
        [InlineKeyboardButton("🎨 تغيير المود", callback_data="mods")],
    ])
def football_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔴 لايف دلوقتي", callback_data="live")],
        [InlineKeyboardButton("🇪🇬 مصري", callback_data="match_egypt"), InlineKeyboardButton("🏴󐁧󐁢󐁥󐁮󐁧󐁿 إنجليزي", callback_data="match_england")],
        [InlineKeyboardButton("🇪🇸 إسباني", callback_data="match_spain"), InlineKeyboardButton("🏆 أبطال", callback_data="match_champions")],
        [InlineKeyboardButton("🇮🇹 إيطالي", callback_data="match_italy"), InlineKeyboardButton("🇩🇪 ألماني", callback_data="match_germany")],
        [InlineKeyboardButton("🇸🇦 سعودي", callback_data="match_saudi")],
        [InlineKeyboardButton("🔄 تحديث", callback_data="football"), InlineKeyboardButton("🔙 رجوع", callback_data="menu")],
    ])
def players_keyboard():
    keys = list(PLAYERS.keys())
    btns = [[InlineKeyboardButton(f"⭐ {k}", callback_data=f"player_{k}") for k in keys[i:i+2]] for i in range(0, len(keys), 2)]
    btns.append([InlineKeyboardButton("🔙 رجوع", callback_data="menu")])
    return InlineKeyboardMarkup(btns)
def basics_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📍 المراكز", callback_data="basic_positions"), InlineKeyboardButton("🚩 التسلل", callback_data="basic_offside")],
        [InlineKeyboardButton("📜 القواعد", callback_data="basic_rules"), InlineKeyboardButton("💡 محترف", callback_data="basic_tips")],
        [InlineKeyboardButton("📐 التشكيلات", callback_data="basic_formations"), InlineKeyboardButton("🧠 الخطط", callback_data="basic_tactics")],
        [InlineKeyboardButton("🏋️ تمارين", callback_data="basic_training")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="menu")],
    ])
def mods_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🖤💛 ذهبي", callback_data="set_gold"), InlineKeyboardButton("💜⚡ نيون", callback_data="set_neon")],
        [InlineKeyboardButton("🔥 ناري", callback_data="set_fire"), InlineKeyboardButton("💙🧊 ثلجي", callback_data="set_ice")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="menu")],
    ])
def format_matches(title, lst):
    txt = f"{title}\n━━━━━━━━━━━━━━━\n🌐 بتتحدث من الموقع تلقائي\n━━━━━━━━━━━━━━━\n\n"
    if not lst: txt += "مفيش ماتشات دلوقتي، جرب بعد شوية ⚽\n"
    for m, d in lst: txt += f"{m}\n{d}\n\n"
    return txt + "━━━━━━━━━━━━━━━\n🔄 دوس تحديث عشان تجيب الجديد"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mod = get_mod(update.effective_user.id)
    text = f"{mod['welcome']}\n\n👋 أهلا بيك يا {update.effective_user.first_name} !\n⚽ كورة لايف من الموقع + ⭐ لاعيبة + 🧠 أسئلة + 📚 مبادئ\n🎨 المود: {mod['name']}\n\n👇 اختار:"
    if update.message: await update.message.reply_text(text, reply_markup=main_keyboard(mod))
    else: await update.callback_query.edit_message_text(text, reply_markup=main_keyboard(mod))

async def send_quiz(q, uid):
    idx = user_score.get(uid, {}).get("idx", 0); score = user_score.get(uid, {}).get("score", 0)
    if idx >= len(PRO_QUIZ):
        txt = f"🏁 خلصت! ⭐ نتيجتك: {score}/{len(PRO_QUIZ)}\n"
        txt += "🏆 محترف بجد!" if score >= 4 else "📚 راجع المبادئ"
        await q.edit_message_text(txt, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔁 تاني", callback_data="quiz_start")],[InlineKeyboardButton("🔙 القايمة", callback_data="menu")]])); return
    item = PRO_QUIZ[idx]
    kb = InlineKeyboardMarkup([[InlineKeyboardButton(opt, callback_data=f"quiz_ans_{i}")] for i, opt in enumerate(item["opts"])])
    await q.edit_message_text(f"🧠 سؤال {idx+1}/{len(PRO_QUIZ)} | ⭐ {score}\n\n{item['q']}", reply_markup=kb)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer(); uid = q.from_user.id; mod = get_mod(uid); data = q.data
    if data == "menu": await start(update, context); return
    if data == "mods": await q.edit_message_text("🎨 اختار المود 👇", reply_markup=mods_keyboard()); return
    if data.startswith("set_"):
        user_mod[uid] = data.replace("set_", ""); mod = get_mod(uid)
        await q.edit_message_text(f"✅ تم! المود: {mod['name']}", reply_markup=main_keyboard(mod)); return
    if data == "live":
        await q.edit_message_text("⏳ بجيب الماتشات اللايف من الموقع...")
        live = fetch_live()
        await q.edit_message_text(format_matches("🔴⚽ ماتشات لايف دلوقتي", live), reply_markup=football_keyboard()); return
    if data == "football": await q.edit_message_text("⚽🏆 قسم الكورة - بتتحدث من الموقع تلقائي 🌐\nاختار الدوري 👇", reply_markup=football_keyboard()); return
    if data.startswith("match_"):
        key = data.replace("match_", "")
        if key in LEAGUES:
            await q.edit_message_text("⏳ بجيب المواعيد من الموقع...")
            lst = get_matches(key)
            await q.edit_message_text(format_matches(f"{LEAGUES[key]['name']} - مواعيد محدثة 🌐", lst), reply_markup=football_keyboard()); return
    if data == "players": await q.edit_message_text("⭐ اختار اللاعب 👇", reply_markup=players_keyboard()); return
    if data.startswith("player_"): await q.edit_message_text(PLAYERS.get(data.replace("player_", ""), ""), reply_markup=players_keyboard()); return
    if data == "quiz_start": user_score[uid] = {"idx": 0, "score": 0}; await send_quiz(q, uid); return
    if data.startswith("quiz_ans_"):
        chosen = int(data.replace("quiz_ans_", "")); st = user_score.get(uid, {"idx": 0, "score": 0})
        correct = PRO_QUIZ[st["idx"]]["ans"]
        fb = "✅ صح! 🔥" if chosen == correct else f"❌ غلط! الصح: {PRO_QUIZ[st['idx']]['opts'][correct]}"
        if chosen == correct: st["score"] += 1
        st["idx"] += 1; user_score[uid] = st
        await q.edit_message_text(f"{fb}\n\nدوس التالي 👇", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("➡️ اللي بعده", callback_data="quiz_next")]])); return
    if data == "quiz_next": await send_quiz(q, uid); return
    if data == "basics": await q.edit_message_text("📚 مبادئ الكورة 👇", reply_markup=basics_keyboard()); return
    if data.startswith("basic_"): await q.edit_message_text(BASICS.get(data.replace("basic_", ""), ""), reply_markup=basics_keyboard()); return
    if data == "tip": await q.edit_message_text(f"{random.choice(DAILY_TIPS)}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💡 نصيحة تانية", callback_data="tip")],[InlineKeyboardButton("🔙 القايمة", callback_data="menu")]])); return
    if data == "compare": await q.edit_message_text("⚔️ اكتبلي في الشات: `قارن صلاح ومبابي`", reply_markup=main_keyboard(mod)); return

async def txt_h(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mod = get_mod(update.effective_user.id)
    await update.message.reply_text(f"{mod['emoji']} وصلت: {update.message.text} ✅\nجرب /start", reply_markup=main_keyboard(mod))

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("matches", start))
    app.add_handler(CommandHandler("live", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, txt_h))
    print("Bot running LIVE from site ⚽🌐")
    app.run_polling()
if __name__ == "__main__":
    main()
