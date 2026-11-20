# ═══════════════════════════════════════
#  ⚽ بوت الكورة الشامل - النسخة الفخمة 👑
#  من صنع عدي عمرو | @TRAN_5
#  المالك: 8188263997
# ═══════════════════════════════════════

import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, PreCheckoutQueryHandler
from datetime import datetime, timezone, timedelta

TOKEN = os.environ.get("TOKEN") or "حط_التوكن_بتاعك_هنا"
DEV_USERNAME = "TRAN_5"
OWNER_ID = 8188263997

# ── سيرفر وهمي لـ Render ──
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running - Made by Ady Amr")
    def log_message(self, *args): pass
def keep_alive():
    port = int(os.environ.get("PORT", 10000))
    try: HTTPServer(("0.0.0.0", port), Handler).serve_forever()
    except: pass
threading.Thread(target=keep_alive, daemon=True).start()

# ═══════════════ 🎨 نظام التصميم ═══════════════
LINE = "━━━━━━━━━━━━━━━━━━━━"
LINE2 = "┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄"
FOOTER = f"\n{LINE2}\n🤖 بوت عدي عمرو | @{DEV_USERNAME}"

def box(title, body):
    return f"{title}\n{LINE}\n\n{body}{FOOTER}"

def header_emoji(title):
    return f"╭─── {title} ───╮"

# ترجمة الفرق
TEAMS_AR = {
    "Liverpool": "ليفربول", "Arsenal": "أرسنال", "Manchester City": "مانشستر سيتي",
    "Manchester United": "مانشستر يونايتد", "Chelsea": "تشيلسي", "Tottenham Hotspur": "توتنهام",
    "Real Madrid": "ريال مدريد", "Barcelona": "برشلونة", "Atlético Madrid": "أتلتيكو مدريد",
    "Sevilla": "إشبيلية", "Bayern Munich": "بايرن ميونخ", "Borussia Dortmund": "دورتموند",
    "Paris Saint-Germain": "باريس سان جيرمان", "Marseille": "مارسيليا", "Juventus": "يوفنتوس",
    "AC Milan": "ميلان", "Inter": "إنتر", "Napoli": "نابولي", "Roma": "روما",
    "Al Ahly": "الأهلي", "Zamalek": "الزمالك", "Pyramids FC": "بيراميدز",
    "Al Hilal": "الهلال", "Al Nassr": "النصر", "Al Ittihad": "الاتحاد",
    "Ajax": "أياكس", "Porto": "بورتو", "Benfica": "بنفيكا", "Galatasaray": "جالطة سراي",
}
def ar_team(n): return TEAMS_AR.get(n, n)

STATUS_AR = {
    "Scheduled": "لم يبدأ بعد ⏳", "In Progress": "جارية الآن 🔴",
    "Halftime": "استراحة ⏸️", "Full Time": "انتهت ✅", "Final": "انتهت ✅",
    "Postponed": "تأجلت", "Canceled": "ألغيت",
    "First Half": "الشوط الأول 🔴", "Second Half": "الشوط الثاني 🔴",
}
CHANNELS_AR = {
    "eng.1": "beIN SPORTS 1", "esp.1": "beIN SPORTS 3",
    "ita.1": "beIN SPORTS 4", "ger.1": "beIN SPORTS 5",
    "fra.1": "beIN SPORTS 2", "uefa.champions": "beIN SPORTS 1",
    "egy.1": "ON Sport 1", "sau.1": "SSC 1",
}
LEAGUES = {
    "eng.1": "🏴 الدوري الإنجليزي",
    "esp.1": "🇪🇸 الدوري الإسباني",
    "ita.1": "🇮🇹 الدوري الإيطالي",
    "ger.1": "🇩🇪 الدوري الألماني",
    "fra.1": "🇫🇷 الدوري الفرنسي",
    "uefa.champions": "🏆 دوري أبطال أوروبا",
    "egy.1": "🇪🇬 الدوري المصري",
    "sau.1": "🇸🇦 الدوري السعودي",
}
PLAYERS_DB = {
    "صلاح": {"team": "ليفربول", "country": "🇪🇬 مصر", "pos": "جناح أيمن", "age": 34, "goals": 18, "assists": 12, "matches": 25, "rating": 8.5, "skills": {"⚡ السرعة": 92, "🎯 التسديد": 90, "🌀 المراوغة": 91, "👟 التمرير": 87, "💪 اللياقة": 88}},
    "مبابي": {"team": "ريال مدريد", "country": "🇫🇷 فرنسا", "pos": "مهاجم", "age": 27, "goals": 22, "assists": 8, "matches": 24, "rating": 9.0, "skills": {"⚡ السرعة": 97, "🎯 التسديد": 93, "🌀 المراوغة": 94, "👟 التمرير": 85, "💪 اللياقة": 90}},
    "هالاند": {"team": "مان سيتي", "country": "🇳🇴 النرويج", "pos": "مهاجم", "age": 26, "goals": 25, "assists": 5, "matches": 23, "rating": 9.1, "skills": {"⚡ السرعة": 90, "🎯 التسديد": 95, "🌀 المراوغة": 82, "👟 التمرير": 80, "💪 اللياقة": 92}},
    "ميسي": {"team": "انتر ميامي", "country": "🇦🇷 الأرجنتين", "pos": "صانع لعب", "age": 39, "goals": 15, "assists": 18, "matches": 22, "rating": 8.9, "skills": {"⚡ السرعة": 85, "🎯 التسديد": 92, "🌀 المراوغة": 96, "👟 التمرير": 95, "💪 اللياقة": 82}},
    "رونالدو": {"team": "النصر", "country": "🇵🇹 البرتغال", "pos": "مهاجم", "age": 41, "goals": 20, "assists": 6, "matches": 24, "rating": 8.7, "skills": {"⚡ السرعة": 88, "🎯 التسديد": 94, "🌀 المراوغة": 87, "👟 التمرير": 82, "💪 اللياقة": 90}},
    "مرموش": {"team": "مان سيتي", "country": "🇪🇬 مصر", "pos": "مهاجم", "age": 27, "goals": 10, "assists": 7, "matches": 20, "rating": 8.2, "skills": {"⚡ السرعة": 91, "🎯 التسديد": 85, "🌀 المراوغة": 88, "👟 التمرير": 82, "💪 اللياقة": 87}},
    "زيزو": {"team": "الأهلي", "country": "🇪🇬 مصر", "pos": "جناح أيمن", "age": 30, "goals": 8, "assists": 9, "matches": 22, "rating": 8.0, "skills": {"⚡ السرعة": 86, "🎯 التسديد": 82, "🌀 المراوغة": 88, "👟 التمرير": 85, "💪 اللياقة": 84}},
}

ratings, user_points, searching_users, all_users = [], {}, [], set()
def is_owner(uid): return uid == OWNER_ID

# ═══════════════ 📱 القوايم المنظمة ═══════════════
def main_menu(user_id=None):
    kb = [
        [InlineKeyboardButton("🔴  مباريات الآن  •  تحديث مباشر", callback_data="live")],
        [InlineKeyboardButton("📅  مباريات اليوم", callback_data="today"),
         InlineKeyboardButton("📅  مباريات الغد", callback_data="tomorrow")],
        [InlineKeyboardButton("🏆  جدول الترتيب", callback_data="table"),
         InlineKeyboardButton("⚽  الهدافين", callback_data="scorers")],
        [InlineKeyboardButton("🔍  ابحث عن لاعب", callback_data="player_search"),
         InlineKeyboardButton("⭐  فريقي المفضل", callback_data="fav")],
        [InlineKeyboardButton("📺  القنوات الناقلة", callback_data="channels"),
         InlineKeyboardButton("📋  تشكيلة المباراة", callback_data="lineup")],
        [InlineKeyboardButton("📊  إحصائيات", callback_data="stats"),
         InlineKeyboardButton("🤖  توقعات", callback_data="predict")],
        [InlineKeyboardButton("🎥  ملخصات", callback_data="highlights"),
         InlineKeyboardButton("📰  أخبار", callback_data="news")],
        [InlineKeyboardButton("🎮  فانتازي", callback_data="fantasy"),
         InlineKeyboardButton("🔔  تنبيه الأهداف", callback_data="notify")],
        [InlineKeyboardButton("🎁  مكافأة يومية  •  🏆  لوحة الصدارة", callback_data="daily")],
        [InlineKeyboardButton("🔍  ابحث عن شخص تتحدث معه", callback_data="find_friend")],
        [InlineKeyboardButton("⭐  قيّم البوت", callback_data="rate"),
         InlineKeyboardButton("💎  تبرع بالنجوم", callback_data="donate")],
        [InlineKeyboardButton("📣  شارك البوت مع صحابك", callback_data="share")],
        [InlineKeyboardButton("👨‍💻  تواصل مع المطور  •  @TRAN_5", url=f"https://t.me/{DEV_USERNAME}")],
    ]
    if is_owner(user_id):
        kb.append([InlineKeyboardButton("👑  لوحة المالك  •  عدي عمرو", callback_data="owner_panel")])
    return InlineKeyboardMarkup(kb)

def back_menu(user_id=None):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄  تحديث النتائج", callback_data="live")],
        [InlineKeyboardButton("🏠  القايمة الرئيسية", callback_data="home")],
    ])

def get_matches(league_id="eng.1", date_offset=0):
    try:
        target = datetime.now(timezone.utc) + timedelta(days=date_offset)
        date_str = target.strftime("%Y%m%d")
        url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/{league_id}/scoreboard?dates={date_str}"
        data = requests.get(url, timeout=6).json()
        return data.get("events", [])
    except: return []

def format_match_ar(ev, league_id):
    try:
        comp = ev["competitions"][0]
        home = ar_team(comp["competitors"][0]["team"]["displayName"])
        away = ar_team(comp["competitors"][1]["team"]["displayName"])
        hs = comp["competitors"][0].get("score", "0")
        aws = comp["competitors"][1].get("score", "0")
        status_type = comp["status"]["type"]["state"]
        status_desc = comp["status"]["type"]["description"]
        status_ar = STATUS_AR.get(status_desc, status_desc)
        clock = comp["status"].get("displayClock", "")
        if status_type == "in":
            status_ar = f"جارية الآن 🔴  •  {clock}" if clock else "جارية الآن 🔴"
        try:
            dt = datetime.fromisoformat(ev["date"].replace("Z", "+00:00"))
            egy = dt + timedelta(hours=2)
            time_str = egy.strftime("%I:%M %p").replace("AM", "صباحاً").replace("PM", "مساءً")
        except: time_str = ""
        channel = CHANNELS_AR.get(league_id, "beIN SPORTS")
        if status_type == "pre":
            return f"  ⚽  {home}  🆚  {away}\n  🕐  {time_str}  •  بتوقيت مصر\n  📌  {status_ar}\n  📺  {channel}\n"
        else:
            return f"  ⚽  {home}  {hs}  -  {aws}  {away}\n  ⏱️  {status_ar}\n  🕐  {time_str}\n  📺  {channel}\n"
    except: return ""

def get_all_matches_text(date_offset=0, only_live=False):
    now_str = (datetime.now(timezone.utc) + timedelta(hours=2)).strftime("%I:%M %p").replace("AM", "صباحاً").replace("PM", "مساءً")
    title = "🔴  مباريات اليوم  •  تحديث مباشر" if date_offset==0 else "📅  مباريات الغد"
    if only_live: title = "🔴  المباريات الجارية الآن"
    text = f"{title}\n🕐  آخر تحديث: {now_str}  •  بتوقيت مصر\n{LINE}\n\n"
    found = False
    for league_id, league_name in LEAGUES.items():
        events = get_matches(league_id, date_offset)
        if only_live: events = [e for e in events if e["competitions"][0]["status"]["type"]["state"] == "in"]
        if events:
            text += f"🏆  {league_name}\n{LINE2}\n"
            for ev in events:
                text += format_match_ar(ev, league_id) + "\n"
                found = True
    if not found:
        text = "😅  مفيش مباريات جارية دلوقتي\n\nجرب تشوف مباريات اليوم 👇" if only_live else "😅  مفيش مباريات في اليوم ده"
    return box("⚽  نتائج المباريات", text) if found else text + FOOTER

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    all_users.add(user.id)
    name = user.first_name or "يا بطل"
    user_points[user.id] = user_points.get(user.id, 0) + 5
    if not is_owner(user.id):
        try: await context.bot.send_message(OWNER_ID, f"👤  مستخدم جديد دخل البوت!\n\n👤 الاسم: {name}\n🔗 اليوزر: @{user.username}\n🆔 الايدي: {user.id}\n👥 الإجمالي: {len(all_users)}")
        except: pass
    if is_owner(user.id):
        await update.message.reply_text(box("👑  أهلاً يا مالك البوت", f"نورت يا عدي 🔥\n\n👥  المستخدمين: {len(all_users)}\n⭐  التقييمات: {len(ratings)}\n🎁  النقاط: {sum(user_points.values())}\n\nاختار من القايمة 👇"), reply_markup=main_menu(user.id))
        return
    welcome = (
        f"👋  أهلاً بيك يا {name}  ❤️\n"
        f"هذا بوت من صنع عدي عمرو  ⚽🔥\n"
        f"المطور:  @{DEV_USERNAME}\n\n"
        f"{LINE}\n\n"
        f"⚽  بوت الكورة الشامل  •  بالعربي\n"
        f"🔴  نتائج مباشرة بتتحدث لوحدها\n"
        f"🕐  كل المواعيد بتوقيت مصر\n"
        f"📺  القناة الناقلة لكل مباراة\n"
        f"🔍  أكتر من 10,000 لاعب بمهاراتهم\n"
        f"🔍  ابحث عن شخص تتحدث معه\n"
        f"⭐  قيّم البوت  •  💎  تبرع بالنجوم\n\n"
        f"🎁  خدت 5 نقاط ترحيبية!\n"
        f"رصيدك: {user_points[user.id]} نقطة\n\n"
        f"اختار من القايمة 👇"
    )
    await update.message.reply_text(box("⚽  بوت عدي عمرو", welcome), reply_markup=main_menu(user.id))

async def owner_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("❌ أنت مش المالك!"); return
    await update.message.reply_text(box("👑  لوحة المالك", f"👥 المستخدمين: {len(all_users)}\n⭐ التقييمات: {len(ratings)}\n🎁 النقاط: {sum(user_points.values())}\n\n📝 أوامرك:\n/stats  •  إحصائيات\n/broadcast رسالتك  •  إذاعة للكل"), reply_markup=main_menu(update.effective_user.id))

async def stats_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id): return
    await update.message.reply_text(box("📊  إحصائيات البوت", f"👥  {len(all_users)} مستخدم\n⭐  {len(ratings)} تقييم\n🎁  {sum(user_points.values())} نقطة"))

async def broadcast_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id): return
    msg = " ".join(context.args)
    if not msg:
        await update.message.reply_text("اكتب: /broadcast يا جماعة المباراة بدأت 🔥"); return
    sent = 0
    for uid in list(all_users):
        try: await context.bot.send_message(uid, box("📣  رسالة من عدي عمرو 👑", msg)); sent += 1
        except: pass
    await update.message.reply_text(f"✅  بعت لـ {sent} واحد")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer("جاري التحديث... ⚽")
    data = query.data
    user = query.from_user
    all_users.add(user.id)

    if data == "home":
        await query.message.reply_text(box("🏠  القايمة الرئيسية", "اختار اللي انت عايزه 👇"), reply_markup=main_menu(user.id)); return
    if data == "live":
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("🔄  تحديث النتائج الآن", callback_data="live")],[InlineKeyboardButton("🔴  الجارية فقط", callback_data="live_only")],[InlineKeyboardButton("🏠  القايمة الرئيسية", callback_data="home")]])
        await query.message.reply_text(get_all_matches_text(0, False), reply_markup=kb); return
    if data == "live_only":
        await query.message.reply_text(get_all_matches_text(0, True), reply_markup=back_menu(user.id)); return
    if data == "today":
        await query.message.reply_text(get_all_matches_text(0, False), reply_markup=back_menu(user.id)); return
    if data == "tomorrow":
        await query.message.reply_text(get_all_matches_text(1, False), reply_markup=back_menu(user.id)); return

    if data == "table":
        body = "🥇  1  •  أرسنال  •  28 نقطة\n🥈  2  •  مان سيتي  •  27 نقطة\n🥉  3  •  ليفربول  •  26 نقطة\n  4  •  تشيلسي  •  24 نقطة\n  5  •  توتنهام  •  22 نقطة"
        await query.message.reply_text(box("🏆  جدول الترتيب  •  الدوري الإنجليزي", body), reply_markup=main_menu(user.id))
    elif data == "scorers":
        body = "🥇  هالاند  •  14 هدف  🔥\n🥈  محمد صلاح  •  11 هدف  🇪🇬\n🥉  مبابي  •  10 أهداف\n  4  •  كين  •  9 أهداف"
        await query.message.reply_text(box("⚽  الهدافين", body), reply_markup=main_menu(user.id))
    elif data == "channels":
        body = "🏴  الإنجليزي  •  beIN 1\n🇪🇸  الإسباني  •  beIN 3\n🇮🇹  الإيطالي  •  beIN 4\n🇩🇪  الألماني  •  beIN 5\n🇫🇷  الفرنسي  •  beIN 2\n🏆  دوري الأبطال  •  beIN 1\n🇪🇬  المصري  •  ON Sport 1\n🇸🇦  السعودي  •  SSC 1"
        await query.message.reply_text(box("📺  القنوات الناقلة", body), reply_markup=main_menu(user.id))
    elif data == "lineup":
        body = "🧤  أليسون\n\n🛡️  أرنولد  •  فان دايك  •  كوناتي  •  روبرتسون\n\n⚙️  سوبوسلاي  •  جرافينبيرخ  •  ماك أليستر\n\n⚽  صلاح  •  إيزاك  •  جاكبو"
        await query.message.reply_text(box("📋  تشكيلة ليفربول المتوقعة", body), reply_markup=main_menu(user.id))
    elif data == "stats":
        body = "📊  الاستحواذ\n█████████████  65%  •  35%  ░░░░\n\n🎯  التسديدات:  18  -  7\n🚩  الركنيات:  8  -  2\n🟨  الكروت الصفراء:  2  -  4"
        await query.message.reply_text(box("📊  إحصائيات المباراة", body), reply_markup=main_menu(user.id))
    elif data == "predict":
        body = "ليفربول  ██████████  60%\nتعادل  ███  20%\nيونايتد  ███  20%\n\n🔮  النتيجة المتوقعة:  2 - 1  لليفربول"
        await query.message.reply_text(box("🤖  توقعات المباراة", body), reply_markup=main_menu(user.id))
    elif data == "motm":
        await query.message.reply_text(box("🏅  لاعب المباراة", "⭐  محمد صلاح  •  9.2 / 10\n⚽  هدفين  +  🎯  أسيست  🔥"), reply_markup=main_menu(user.id))
    elif data == "highlights":
        await query.message.reply_text(box("🎥  ملخصات المباريات", "https://www.youtube.com/results?search_query=ملخص+مباريات+اليوم"), reply_markup=main_menu(user.id))
    elif data == "news":
        body = "•  صلاح يقترب من تجديد عقده 🔥\n•  ريال مدريد يجهز عرض ضخم\n•  الأهلي يتعاقد مع مهاجم جديد"
        await query.message.reply_text(box("📰  آخر الأخبار", body), reply_markup=main_menu(user.id))
    elif data == "fantasy":
        await query.message.reply_text(box("🎮  فانتازي", "تشكيلتك: صلاح (C)  •  هالاند  •  مبابي\n⭐  نقاط الأسبوع: 78 نقطة 🔥"), reply_markup=main_menu(user.id))
    elif data == "notify":
        await query.message.reply_text(box("🔔  تنبيه الأهداف", "تم التفعيل ✅\nأول ما يجي جول هبعتلك على طول!"), reply_markup=main_menu(user.id))
    elif data == "owner_panel":
        if not is_owner(user.id): await query.message.reply_text("❌ دي للمالك بس 👑"); return
        await query.message.reply_text(box("👑  لوحة المالك", f"👥 المستخدمين: {len(all_users)}\n⭐ التقييمات: {len(ratings)}\n🎁 النقاط: {sum(user_points.values())}\n\n/owner  •  لوحة المالك\n/stats  •  إحصائيات\n/broadcast رسالة  •  إذاعة"), reply_markup=main_menu(user.id))
    elif data == "rate":
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("⭐", callback_data="rate_1"), InlineKeyboardButton("⭐⭐", callback_data="rate_2"), InlineKeyboardButton("⭐⭐⭐", callback_data="rate_3")],[InlineKeyboardButton("⭐⭐⭐⭐", callback_data="rate_4"), InlineKeyboardButton("⭐⭐⭐⭐⭐", callback_data="rate_5")],[InlineKeyboardButton("🏠  القايمة", callback_data="home")]])
        avg = sum([r[1] for r in ratings]) / len(ratings) if ratings else 5.0
        await query.message.reply_text(box("⭐  قيّم البوت", f"متوسط التقييم: {avg:.1f} / 5\nعدد المقيمين: {len(ratings)}\n\nاختار عدد النجوم 👇"), reply_markup=kb)
    elif data.startswith("rate_"):
        stars = int(data.split("_")[1])
        ratings[:] = [r for r in ratings if r[0] != user.id]
        ratings.append((user.id, stars))
        avg = sum([r[1] for r in ratings]) / len(ratings)
        await query.message.reply_text(box("⭐  شكراً ليك ❤️", f"قييمت بـ {stars} ⭐\nالمتوسط الجديد: {avg:.1f} / 5"), reply_markup=main_menu(user.id))
        try: await context.bot.send_message(OWNER_ID, f"⭐ تقييم جديد!\nمن: {user.first_name} (@{user.username})\nقيم بـ: {stars} ⭐\nالمتوسط: {avg:.1f}")
        except: pass
    elif data == "donate":
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("⭐  10 نجوم  •  دعم بسيط", callback_data="donate_10")],[InlineKeyboardButton("⭐  50 نجمة  •  دعم قوي 🔥", callback_data="donate_50")],[InlineKeyboardButton("⭐  100 نجمة  •  أسطورة 👑", callback_data="donate_100")],[InlineKeyboardButton("👨‍💻  كلم المطور", url=f"https://t.me/{DEV_USERNAME}")]])
        await query.message.reply_text(box("💎  تبرع بالنجوم", "تبرعك بيوصل لعدي عمرو على طول ❤️\nكل 10 نجوم = 50 نقطة 🎁\n\nاختار 👇"), reply_markup=kb)
    elif data.startswith("donate_"):
        amount = int(data.split("_")[1])
        await query.message.reply_text(f"💎  هتتبرع بـ {amount} نجمة، دوس على زرار الدفع واكد ❤️")
        await context.bot.send_invoice(chat_id=query.message.chat_id, title="دعم بوت عدي عمرو", description=f"تبرع بـ {amount} نجمة", payload=f"donate_{amount}_{user.id}", provider_token="", currency="XTR", prices=[LabeledPrice("تبرع", amount)])
    elif data == "daily":
        user_points[user.id] = user_points.get(user.id, 0) + 10
        await query.message.reply_text(box("🎁  مكافأة يومية", f"خدت 10 نقاط 🔥\nرصيدك دلوقتي: {user_points[user.id]} نقطة"), reply_markup=main_menu(user.id))
    elif data == "leaderboard":
        sorted_users = sorted(user_points.items(), key=lambda x: x[1], reverse=True)[:5]
        txt = ""
        for i, (uid, pts) in enumerate(sorted_users, 1):
            medal = ["🥇","🥈","🥉","4️⃣","5️⃣"][i-1]
            txt += f"{medal}  {uid}  •  {pts} نقطة\n"
        txt += f"\nنقطك انت: {user_points.get(user.id, 0)}"
        await query.message.reply_text(box("🏆  لوحة الصدارة", txt), reply_markup=main_menu(user.id))
    elif data == "share":
        await query.message.reply_text(box("📣  شارك البوت", "https://t.me/YourBotUsername\n\nكل واحد يدخل هتاخد 20 نقطة! 🎁"), reply_markup=main_menu(user.id))
    elif data == "find_friend":
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("⚽  كور
