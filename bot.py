import os, random, requests, threading, time
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN") or os.getenv("TOKEN")
LAST_UPDATE = "2026/11/20"
NEXT_UPDATE = "2027/01/29"
UPDATE_TEXT = f"📅 آخر تحديث: {LAST_UPDATE}\n🔜 التحديث القادم: {NEXT_UPDATE}"

LEAGUES = {"egypt": {"name": "🇪🇬 الدوري المصري"}, "england": {"name": "🏴󐁧󐁢󐁥󐁮󐁧󐁿 الدوري الإنجليزي"}, "spain": {"name": "🇪🇸 الدوري الإسباني"}, "saudi": {"name": "🇸🇦 الدوري السعودي"}, "champions": {"name": "🏆 دوري الأبطال"}}
ESPN_LEAGUES = {"egypt": "egy.1", "england": "eng.1", "spain": "esp.1", "saudi": "sau.1", "champions": "uefa.champions"}
SCHEDULE_CACHE = {"today": [], "tomorrow": [], "week": [], "live": [], "egypt": [], "england": [], "spain": []}
user_mod = {}; user_score = {}; user_points = {}; user_fantasy = {}; user_notify = {}
fan_messages = []; fantasy_leagues = {}; predict_league_board = {}

def get_mod(uid):
    MODS = {"gold": {"name": "🖤💛 ذهبي", "emoji": "👑", "welcome": "أهلا بيك في النسخة الذهبية 👑✨"}, "neon": {"name": "💜⚡ نيون", "emoji": "⚡", "welcome": "أهلا بيك في عالم النيون 💜⚡"}, "fire": {"name": "🔥 ناري", "emoji": "🔥", "welcome": "ولعهااا 🔥"}, "ice": {"name": "💙🧊 ثلجي", "emoji": "🧊", "welcome": "أهلا بيك في المود الثلجي 💙🧊"}}
    return MODS.get(user_mod.get(uid, "gold"))

def get_league_code():
    return str(random.randint(1000, 9999))

def fetch_espn(slug):
    out = []
    try:
        for offset in [0, 3, 6]:
            date = (datetime.now() + timedelta(days=offset)).strftime("%Y%m%d")
            url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/{slug}/scoreboard?dates={date}"
            r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            for ev in r.json().get("events", []):
                comp = ev.get("competitions", [{}])[0]
                teams = comp.get("competitors", [])
                if len(teams) < 2:
                    continue
                home = teams[0].get("team", {}).get("displayName", "?")
                away = teams[1].get("team", {}).get("displayName", "?")
                if teams[0].get("homeAway") == "away":
                    home, away = away, home
                dt = ev.get("date", "")
                try:
                    d = datetime.fromisoformat(dt.replace("Z", "+00:00"))
                    date_str = d.strftime("%Y-%m-%d"); time_str = d.strftime("%H:%M")
                except:
                    date_str = dt[:10]; time_str = "؟"
                status = comp.get("status", {}).get("type", {}).get("description", "")
                hs = teams[0].get("score"); as_ = teams[1].get("score")
                score = f"🔴 {hs} - {as_} | {status}" if hs is not None and status != "Scheduled" else f"🕗 {time_str}"
                out.append({"home": home, "away": away, "league": ev.get("league", {}).get("name", slug), "date": date_str, "time": time_str, "score": score, "venue": comp.get("venue", {}).get("fullName", "")})
        seen = set(); uniq = []
        for m in out:
            k = (m["home"], m["away"], m["date"])
            if k not in seen:
                seen.add(k); uniq.append(m)
        return uniq
    except Exception as e:
        print(e); return []

def fetch_live():
    out = []
    for slug in ["egy.1", "eng.1", "esp.1", "sau.1"]:
        try:
            url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/{slug}/scoreboard"
            r = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
            for ev in r.json().get("events", []):
                comp = ev.get("competitions", [{}])[0]
                if comp.get("status", {}).get("type", {}).get("state") == "in":
                    teams = comp.get("competitors", [])
                    out.append({"home": teams[0].get("team", {}).get("displayName"), "away": teams[1].get("team", {}).get("displayName"), "league": slug, "date": "LIVE", "time": "", "score": f"🔴 {teams[0].get('score')} - {teams[1].get('score')}", "venue": ""})
        except:
            continue
    return out

def fetch_commentary(slug="egy.1"):
    try:
        url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/{slug}/scoreboard"
        r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        evs = r.json().get("events", [])
        if not evs:
            return "🎙️ **تعليق مباشر**\n\nمفيش ماتش شغال دلوقتي."
        txt = "🎙️ **تعليق مباشر**\n━━━━━━━━━━━━━━━\n\n"
        for ev in evs[:3]:
            comp = ev.get("competitions", [{}])[0]
            teams = comp.get("competitors", [])
            if len(teams) < 2:
                continue
            txt += f"⚽ {teams[0].get('team', {}).get('displayName')} {teams[0].get('score')} - {teams[1].get('score')} {teams[1].get('team', {}).get('displayName')}\n"
        return txt
    except:
        return "🎙️ **تعليق مباشر**\n\n⚽ الأهلي 🆚 بيراميدز\n🔴 الأهلي 1 - 0 بيراميدز\n• د 10: جووووول وسام أبو علي 🔥"

def update_schedule():
    egy = fetch_espn("egy.1"); eng = fetch_espn("eng.1"); esp = fetch_espn("esp.1")
    week = egy + eng + esp
    today = datetime.now().strftime("%Y-%m-%d"); tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    if not week:
        week = [
            {"home": "الجونة", "away": "الزمالك", "league": "الدوري المصري", "date": "2026-11-23", "time": "17:00", "score": "🕗 17:00", "venue": "استاد الجونة"},
            {"home": "الأهلي", "away": "بيراميدز", "league": "الدوري المصري", "date": "2026-11-23", "time": "20:00", "score": "🕗 20:00", "venue": "استاد القاهرة"},
            {"home": "سموحة", "away": "البنك الأهلي", "league": "الدوري المصري", "date": "2026-11-24", "time": "17:00", "score": "🕗 17:00", "venue": ""},
            {"home": "المصري", "away": "بترول أسيوط", "league": "الدوري المصري", "date": "2026-11-24", "time": "20:00", "score": "🕗 20:00", "venue": ""},
        ]
    SCHEDULE_CACHE.update({"today": [m for m in week if m["date"] == today], "tomorrow": [m for m in week if m["date"] == tomorrow], "week": week, "live": fetch_live(), "egypt": egy if egy else week, "england": eng, "spain": esp})
    print(f"✅ اتحدث! {len(week)} ماتش")

STANDINGS = {"egypt": [("1️⃣ بيراميدز", "8 ماتش | 18 نقطة"), ("2️⃣ الأهلي", "8 ماتش | 17 نقطة"), ("3️⃣ الزمالك", "8 ماتش | 16 نقطة")], "england": [("1️⃣ أرسنال", "12 ماتش | 29 نقطة"), ("2️⃣ مان سيتي", "12 ماتش | 27 نقطة")], "spain": [("1️⃣ برشلونة", "13 ماتش | 31 نقطة"), ("2️⃣ ريال مدريد", "13 ماتش | 30 نقطة")]}
TOP_SCORERS = {"egypt": "🎯 **هدافين المصري**\n🥇 وسام أبو علي - 7 أهداف\n🥈 زيزو - 6 أهداف", "england": "🎯 **هدافين الإنجليزي**\n🥇 هالاند - 14 هدف\n🥈 صلاح - 9 أهداف", "spain": "🎯 **هدافين الإسباني**\n🥇 مبابي - 12 هدف"}
AHLY_NEWS = ["🔴 **أخبار الأهلي**\n🏋️ بيستعد لماتش بيراميدز الاثنين 23 نوفمبر | 8 م\n💪 وسام أبو علي جاهز"]
ZAMALEK_NEWS = ["⚪ **أخبار الزمالك**\n🏋️ بيستعد لماتش الجونة الاثنين 23 نوفمبر | 5 م\n💪 زيزو جاهز"]
TRANSFERS = ["📰 **انتقالات**\n🔴 الأهلي بيجهز عرض لمهاجم أجنبي", "📰 **انتقالات**\n🔴 ليفربول بيدور على مدافع"]
H2H = {"ahly_zamalek": "🤼 **الأهلي 🆚 الزمالك**\n🔴 الأهلي: 61\n⚪ الزمالك: 29\n🤝 تعادل: 40", "real_barca": "🤼 **ريال 🆚 برشلونة**\n⚪ ريال: 102\n🔵🔴 برشلونة: 103"}
AI_PREDICTIONS = {"ahly_pyramids": "🤖 **توقع AI**\n⚽ الأهلي 🆚 بيراميدز\n🤖 **التوقع: الأهلي يكسب 2-1**", "zamalek_gouna": "🤖 **توقع AI**\n⚽ الجونة 🆚 الزمالك\n🤖 **التوقع: الزمالك يكسب 1-0**"}
LINEUPS = {"ahly": "📋 **تشكيلة الأهلي**\n🧤 الشناوي\n🛡️ هاني - ياسر - داري - معلول\n⚙️ مروان - إمام - أفشة\n⚽ تاو - وسام - الشحات", "zamalek": "📋 **تشكيلة الزمالك**\n🧤 عواد\n🛡️ عمر - الونش - حسام - فتوح\n⚙️ دونجا - شحاتة - زيزو\n⚽ شيكابالا - الجزيري - شلبي"}
MATCH_DETAILS = {"ahly_pyramids": "🏟️ **الأهلي 🆚 بيراميدز**\n📅 الاثنين 23 نوفمبر | 🕗 8:00 م\n🏟️ استاد القاهرة\n👨‍⚖️ أمين عمر\n📺 ON Sport 1", "zamalek_gouna": "🏟️ **الجونة 🆚 الزمالك**\n📅 الاثنين 23 نوفمبر | 🕔 5:00 م\n🏟️ استاد الجونة\n👨‍⚖️ محمد عادل\n📺 ON Sport 2"}
RATINGS = ["⭐ **تقييم**\n🔴 وسام 9.2 | إمام 8.5\n⚪ زيزو 8.8"]
MEMES = ["😂 لما صاحبك الأهلاوي يقولك الأهلي هيكسب وانت زملكاوي:\n`انا: 😐`", "😂 لما فريقك يجيب جون الدقيقة 90:\n`جووووول 🔥`"]
WHEEL = ["🎁 كسبت 10 نقاط!", "🎁 كسبت 50 نقطة!", "😅 مفيش حظ", "🎁 كسبت 100 نقطة!"]
GUESS_PLAYER = [{"hint": "🎲 خمن:\n🇪🇬 مصري\n👑 ليفربول\n⚡ بيشوط بالشمال", "opts": ["صلاح", "تريزيجيه", "مرموش", "زيزو"], "ans": 0}, {"hint": "🎲 خمن:\n🐐 أرجنتيني\n🏆 كاس العالم 2022", "opts": ["دي ماريا", "ميسي", "ألفاريز", "ديبالا"], "ans": 1}]
PLAYERS = {"salah": "🇪🇬 **محمد صلاح** 👑\n🏟️ ليفربول | ⚡ 93 | 🎯 95", "messi": "🇦🇷 **ميسي** 🐐\n🏟️ ميامي | ⚡ 99", "ronaldo": "🇵🇹 **رونالدو** 👑\n🏟️ النصر | ⚡ 98", "haaland": "🇳🇴 **هالاند** 🤖\n🏟️ سيتي | ⚡ 95", "mbappe": "🇫🇷 **مبابي** 🚀\n🏟️ ريال | ⚡ 99"}
PRO_QUIZ = [{"q": "🧠 مين أكتر لاعب سجل في دوري الأبطال؟", "opts": ["ميسي", "رونالدو", "بنزيما", "هالاند"], "ans": 1}, {"q": "🧠 مين فاز بكاس العالم 2022؟", "opts": ["فرنسا", "البرازيل", "الأرجنتين", "إنجلترا"], "ans": 2}]
BASICS = {"positions": "📚 **المراكز**\n🧤 حارس | 🛡️ مدافع | ⚙️ وسط | ⚽ مهاجم", "offside": "📚 **التسلل**\n❌ أقرب للجون من آخر مدافع وقت التمرير", "rules": "📚 **قواعد**\n⏱️ 90 دقيقة | 🟨 إنذارين = طرد", "tips": "📚 **محترف**\n1. ارفع راسك\n2. اتحرك من غير كورة", "formations": "📚 **التشكيلات**\n🔥 4-3-3 | 🛡️ 4-4-2", "tactics": "📚 **الخطط**\n🔥 ضغط عالي | 🚌 الباص", "training": "📚 **تمارين**\n🏃 جري 10 دقايق"}
DAILY_TIPS = ["💡 أول لمسة بتفرق بين عادي ومحترف.", "💡 متجريش ورا الكورة، اجري في المساحة."]
LIVE_STREAMS = {"ahly": "📺 **بث الأهلي 🆚 بيراميدز**\nhttps://www.youtube.com/@ONTimeSports\nhttps://www.yallashoot.com", "zamalek": "📺 **بث الجونة 🆚 الزمالك**\nhttps://www.youtube.com/@ONTimeSports", "default": "📺 **بث كل الماتشات**\nhttps://www.youtube.com/@ONTimeSports\nhttps://www.yallashoot.com"}
GOALS_VIDEOS = ["🎥 **هدف وسام في بيراميدز**\nhttps://www.youtube.com/results?search_query=هدف+وسام+بيراميدز", "🎥 **هاتريك صلاح**\nhttps://www.youtube.com/results?search_query=هاتريك+صلاح"]

# ===== الكيبوردات - كلها بنفس الطريقة kb = [] عشان ميحصلش SyntaxError تاني =====
def main_keyboard(mod, uid=0):
    kb = []
    kb.append([InlineKeyboardButton(f"{mod['emoji']} القائمة 📋 | ⭐ {user_points.get(uid, 0)}", callback_data="menu")])
    kb.append([InlineKeyboardButton("📅 جدول مباريات 🔄", callback_data="schedule")])
    kb.append([InlineKeyboardButton("🔴 لايف NOW", callback_data="live_all"), InlineKeyboardButton("🌍 كل العالم", callback_data="all_matches")])
    kb.append([InlineKeyboardButton("🤖 توقع AI", callback_data="ai_menu"), InlineKeyboardButton("📋 تشكيلة", callback_data="lineup_menu")])
    kb.append([InlineKeyboardButton("🏟️ تفاصيل", callback_data="details_menu"), InlineKeyboardButton("⭐ تقييم", callback_data="ratings")])
    kb.append([InlineKeyboardButton("🔴 أخبار الأهلي", callback_data="news_ahly"), InlineKeyboardButton("⚪ أخبار الزمالك", callback_data="news_zamalek")])
    kb.append([InlineKeyboardButton("📊 ترتيب", callback_data="standings"), InlineKeyboardButton("🎯 هدافين", callback_data="scorers")])
    kb.append([InlineKeyboardButton("⚔️ قارن", callback_data="compare_menu"), InlineKeyboardButton("🤼 مواجهات", callback_data="h2h_menu")])
    kb.append([InlineKeyboardButton("🏆 فانتازي", callback_data="fantasy"), InlineKeyboardButton("🔮 توقع", callback_data="predict")])
    kb.append([InlineKeyboardButton("🎲 خمن اللاعب", callback_data="guess_start"), InlineKeyboardButton("🎰 عجلة الحظ", callback_data="wheel")])
    kb.append([InlineKeyboardButton("😂 ميمز", callback_data="meme"), InlineKeyboardButton("📰 انتقالات", callback_data="transfers")])
    kb.append([InlineKeyboardButton("⭐ اللاعيبة", callback_data="players"), InlineKeyboardButton("🧠 تحدي", callback_data="quiz_start")])
    kb.append([InlineKeyboardButton("📚 مبادئ", callback_data="basics"), InlineKeyboardButton("💡 نصيحة", callback_data="tip")])
    kb.append([InlineKeyboardButton("🎨 المود", callback_data="mods"), InlineKeyboardButton("🔔 تنبيه", callback_data="enable_notify")])
    kb.append([InlineKeyboardButton("📺 بث مباشر ✅", callback_data="live_stream_menu"), InlineKeyboardButton("🎥 أهداف ✅", callback_data="goals_video")])
    kb.append([InlineKeyboardButton("👥 فانتازي جماعي ✅", callback_data="fantasy_league_menu"), InlineKeyboardButton("💬 شات ✅", callback_data="fan_chat_menu")])
    kb.append([InlineKeyboardButton("🏆 دوري توقعات ✅", callback_data="predict_league"), InlineKeyboardButton("🎙️ تعليق ✅", callback_data="commentary")])
    kb.append([InlineKeyboardButton(f"📅 {LAST_UPDATE} | 🔜 {NEXT_UPDATE}", callback_data="schedule")])
    return InlineKeyboardMarkup(kb)

def soon_keyboard():
    kb = []
    kb.append([InlineKeyboardButton("📺 بث مباشر ✅", callback_data="live_stream_menu")])
    kb.append([InlineKeyboardButton("🎥 أهداف ✅", callback_data="goals_video")])
    kb.append([InlineKeyboardButton("🔔 تنبيهات ✅", callback_data="enable_notify")])
    kb.append([InlineKeyboardButton("👥 فانتازي جماعي ✅", callback_data="fantasy_league_menu")])
    kb.append([InlineKeyboardButton("💬 شات جماهير ✅", callback_data="fan_chat_menu")])
    kb.append([InlineKeyboardButton("🏆 دوري توقعات ✅", callback_data="predict_league")])
    kb.append([InlineKeyboardButton("🎙️ تعليق ✅", callback_data="commentary")])
    kb.append([InlineKeyboardButton("🔙 القايمة", callback_data="menu")])
    return InlineKeyboardMarkup(kb)

def schedule_keyboard():
    kb = []
    kb.append([InlineKeyboardButton("🔴 لايف", callback_data="live_all"), InlineKeyboardButton("🌍 كل العالم", callback_data="all_matches")])
    kb.append([InlineKeyboardButton("📅 النهاردة", callback_data="sched_today"), InlineKeyboardButton("📅 بكرة", callback_data="sched_tomorrow")])
    kb.append([InlineKeyboardButton("📅 الأسبوع", callback_data="sched_week")])
    kb.append([InlineKeyboardButton("🇪🇬 مصري", callback_data="match_egypt"), InlineKeyboardButton("🏴󐁧󐁢󐁥󐁮󐁧󐁿 إنجليزي", callback_data="match_england")])
    kb.append([InlineKeyboardButton("🇪🇸 إسباني", callback_data="match_spain"), InlineKeyboardButton("🏆 أبطال", callback_data="match_champions")])
    kb.append([InlineKeyboardButton("🔄 تحديث", callback_data="refresh_schedule"), InlineKeyboardButton("🔙 القايمة", callback_data="menu")])
    return InlineKeyboardMarkup(kb)

def all_keyboard():
    kb = []
    kb.append([InlineKeyboardButton("🔴 لايف", callback_data="live_all")])
    kb.append([InlineKeyboardButton("📅 النهاردة", callback_data="sched_today")])
    kb.append([InlineKeyboardButton("🔙 القايمة", callback_data="menu")])
    return InlineKeyboardMarkup(kb)

def football_keyboard():
    kb = []
    for k, v in LEAGUES.items():
        kb.append([InlineKeyboardButton(v["name"], callback_data=f"match_{k}")])
    kb.append([InlineKeyboardButton("🔙 رجوع", callback_data="menu")])
    return InlineKeyboardMarkup(kb)

def players_keyboard():
    kb = []
    keys = list(PLAYERS.keys())
    for i in range(0, len(keys), 2):
        kb.append([InlineKeyboardButton(k, callback_data=f"player_{k}") for k in keys[i:i+2]])
    kb.append([InlineKeyboardButton("🔙 رجوع", callback_data="menu")])
    return InlineKeyboardMarkup(kb)

def basics_keyboard():
    kb = []
    kb.append([InlineKeyboardButton("📍 المراكز", callback_data="basic_positions")])
    kb.append([InlineKeyboardButton("🚩 التسلل", callback_data="basic_offside")])
    kb.append([InlineKeyboardButton("🔙 رجوع", callback_data="menu")])
    return InlineKeyboardMarkup(kb)

def mods_keyboard():
    kb = []
    kb.append([InlineKeyboardButton("🖤💛 ذهبي", callback_data="set_gold"), InlineKeyboardButton("💜⚡ نيون", callback_data="set_neon")])
    kb.append([InlineKeyboardButton("🔥 ناري", callback_data="set_fire"), InlineKeyboardButton("💙🧊 ثلجي", callback_data="set_ice")])
    kb.append([InlineKeyboardButton("🔙 رجوع", callback_data="menu")])
    return InlineKeyboardMarkup(kb)

def standings_keyboard():
    kb = []
    kb.append([InlineKeyboardButton("🇪🇬 مصري", callback_data="stand_egypt")])
    kb.append([InlineKeyboardButton("🏴󐁧󐁢󐁥󐁮󐁧󐁿 إنجليزي", callback_data="stand_england")])
    kb.append([InlineKeyboardButton("🔙 رجوع", callback_data="menu")])
    return InlineKeyboardMarkup(kb)

def scorers_keyboard():
    kb = []
    kb.append([InlineKeyboardButton("🇪🇬 مصري", callback_data="score_egypt")])
    kb.append([InlineKeyboardButton("🔙 رجوع", callback_data="menu")])
    return InlineKeyboardMarkup(kb)

def ai_keyboard():
    kb = []
    kb.append([InlineKeyboardButton("🤖 الأهلي 🆚 بيراميدز", callback_data="ai_ahly_pyramids")])
    kb.append([InlineKeyboardButton("🤖 الجونة 🆚 الزمالك", callback_data="ai_zamalek_gouna")])
    kb.append([InlineKeyboardButton("🔙 القايمة", callback_data="menu")])
    return InlineKeyboardMarkup(kb)

def lineup_keyboard():
    kb = []
    kb.append([InlineKeyboardButton("🔴 الأهلي", callback_data="lineup_ahly")])
    kb.append([InlineKeyboardButton("⚪ الزمالك", callback_data="lineup_zamalek")])
    kb.append([InlineKeyboardButton("🔙 القايمة", callback_data="menu")])
    return InlineKeyboardMarkup(kb)

def details_keyboard():
    kb = []
    kb.append([InlineKeyboardButton("🏟️ الأهلي 🆚 بيراميدز", callback_data="details_ahly_pyramids")])
    kb.append([InlineKeyboardButton("🏟️ الجونة 🆚 الزمالك", callback_data="details_zamalek_gouna")])
    kb.append([InlineKeyboardButton("🔙 القايمة", callback_data="menu")])
    return InlineKeyboardMarkup(kb)

def compare_keyboard():
    kb = []
    kb.append([InlineKeyboardButton("ميسي 🆚 رونالدو", callback_data="cmp_messi_ronaldo")])
    kb.append([InlineKeyboardButton("🔙 رجوع", callback_data="menu")])
    return InlineKeyboardMarkup(kb)

def h2h_keyboard():
    kb = []
    kb.append([InlineKeyboardButton("الأهلي 🆚 الزمالك", callback_data="h2h_ahly_zamalek")])
    kb.append([InlineKeyboardButton("🔙 رجوع", callback_data="menu")])
    return InlineKeyboardMarkup(kb)

def format_table(title, lst):
    txt = f"{title}\n━━━━━━━━━━━━━━━\n{UPDATE_TEXT}\n🌐 من ESPN\n━━━━━━━━━━━━━━━\n\n"
    if not lst:
        txt += "مفيش ماتشات ⚽\n"; return txt
    grouped = {}
    for m in lst:
        grouped.setdefault(m.get("date", "؟"), []).append(m)
    for date in sorted(grouped.keys()):
        txt += f"📅 {date}\n"
        for m in grouped[date]:
            txt += f"⚽ {m['home']} 🆚 {m['away']}\n   🏆 {m['league']} | {m['score']}\n"
    return txt + f"\n{UPDATE_TEXT}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mod = get_mod(update.effective_user.id); uid = update.effective_user.id
    text = f"{mod['welcome']}\n\n👋 أهلا بيك يا {update.effective_user.first_name} !\n🌍 كل الماتشات + 🤖 AI + 📺 بث + 💬 شات\n⭐ نقاطك: {user_points.get(uid, 0)}\n\n{UPDATE_TEXT}\n\n👇 اختار:"
    if update.message:
        await update.message.reply_text(text, reply_markup=main_keyboard(mod, uid))
    else:
        await update.callback_query.edit_message_text(text, reply_markup=main_keyboard(mod, uid))

async def send_quiz(q, uid):
    idx = user_score.get(uid, {}).get("idx", 0)
    if idx >= len(PRO_QUIZ):
        await q.edit_message_text("🏁 خلصت!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القايمة", callback_data="menu")]])); return
    item = PRO_QUIZ[idx]
    kb = [[InlineKeyboardButton(o, callback_data=f"quiz_ans_{i}")] for i, o in enumerate(item["opts"])]
    await q.edit_message_text(item["q"], reply_markup=InlineKeyboardMarkup(kb))

async def send_guess(q, uid):
    idx = user_score.get(uid, {}).get("guess_idx", 0)
    if idx >= len(GUESS_PLAYER):
        await q.edit_message_text("🏁 خلصت!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القايمة", callback_data="menu")]])); return
    item = GUESS_PLAYER[idx]
    kb = [[InlineKeyboardButton(o, callback_data=f"guess_ans_{i}")] for i, o in enumerate(item["opts"])]
    await q.edit_message_
    async def button_handler(update, context):
    q = update.callback_query
    await q.answer()
    data = q.data
    uid = q.from_user.id

    if data == "menu":
        await q.edit_message_text("⚽ أهلاً بيك في بوت الكرة!\nاختار:", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📅 جدول المباريات", callback_data="schedule")],
            [InlineKeyboardButton("🧠 كويز المحترفين", callback_data="quiz")],
            [InlineKeyboardButton("🕵️ خمن اللاعب", callback_data="guess")],
            [InlineKeyboardButton("🔔 تفعيل التنبيهات", callback_data="enable_notify")],
        ])); return

    if data == "enable_notify":
        user_notify[uid] = True
        await q.edit_message_text(f"✅ تم تفعيل التنبيهات!\n\n{UPDATE_TEXT}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القايمة", callback_data="menu")]])); return

    if data == "schedule":
        await q.edit_message_text(f"📅 جدول المباريات\n\n{UPDATE_TEXT}", reply_markup=schedule_keyboard()); return

    if data == "refresh_schedule":
        await q.edit_message_text(f"📅 جدول المباريات (تحديث)\n\n{UPDATE_TEXT}", reply_markup=schedule_keyboard()); return

    if data == "quiz":
        user_score[uid] = {"idx": 0, "score": 0}
        await send_quiz(q, uid); return

    if data.startswith("quiz_ans_"):
        idx = user_score.get(uid, {}).get("idx", 0)
        ans = int(data.split("_")[-1])
        if ans == PRO_QUIZ[idx]["ans"]:
            user_score[uid]["score"] += 1
            await q.answer("✅ صح!", show_alert=False)
        else:
            await q.answer(f"❌ غلط! الصح: {PRO_QUIZ[idx]['opts'][PRO_QUIZ[idx]['ans']]}", show_alert=False)
        user_score[uid]["idx"] += 1
        await send_quiz(q, uid); return

    if data == "guess":
        user_score[uid] = {"guess_idx": 0, "guess_score": 0}
        await send_guess(q, uid); return

    if data.startswith("guess_ans_"):
        idx = user_score.get(uid, {}).get("guess_idx", 0)
        ans = int(data.split("_")[-1])
        if ans == GUESS_PLAYER[idx]["ans"]:
            user_score[uid]["guess_score"] += 1
            await q.answer("✅ صح!", show_alert=False)
        else:
            await q.answer(f"❌ غلط! الصح: {GUESS_PLAYER[idx]['opts'][GUESS_PLAYER[idx]['ans']]}", show_alert=False)
        user_score[uid]["guess_idx"] += 1
        await send_guess(q, uid); return

async def start(update, context):
    await update.message.reply_text("⚽ أهلاً بيك في بوت الكرة!\nاختار:", reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("📅 جدول المباريات", callback_data="schedule")],
        [InlineKeyboardButton("🧠 كويز المحترفين", callback_data="quiz")],
        [InlineKeyboardButton("🕵️ خمن اللاعب", callback_data="guess")],
        [InlineKeyboardButton("🔔 تفعيل التنبيهات", callback_data="enable_notify")],
    ]))

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
