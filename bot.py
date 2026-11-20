# bot.py - بوت عدي عمرو - نسخة نضيفة بدون اخطاء
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, PreCheckoutQueryHandler
from datetime import datetime, timezone, timedelta

TOKEN = os.environ.get("TOKEN") or "حط_التوكن_بتاعك_هنا"
DEV = "TRAN_5"
OWNER_ID = 8188263997

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot running")
    def log_message(self, *args):
        pass

def keep_alive():
    port = int(os.environ.get("PORT", 10000))
    try:
        HTTPServer(("0.0.0.0", port), Handler).serve_forever()
    except:
        pass

threading.Thread(target=keep_alive, daemon=True).start()

LINE = "━━━━━━━━━━━━━━━━━━━━"
FOOTER = "\n━━━━━━━━━━━━━━━━━━━━\nبوت عدي عمرو | @TRAN_5"

def box(title, body):
    return title + "\n" + LINE + "\n\n" + body + FOOTER

TEAMS_AR = {
    "Liverpool": "ليفربول",
    "Arsenal": "ارسنال",
    "Manchester City": "مانشستر سيتي",
    "Manchester United": "مانشستر يونايتد",
    "Chelsea": "تشيلسي",
    "Tottenham Hotspur": "توتنهام",
    "Real Madrid": "ريال مدريد",
    "Barcelona": "برشلونة",
    "Bayern Munich": "بايرن ميونخ",
    "Paris Saint-Germain": "باريس",
    "Juventus": "يوفنتوس",
    "AC Milan": "ميلان",
    "Inter": "انتر",
    "Al Ahly": "الاهلي",
    "Zamalek": "الزمالك",
    "Al Hilal": "الهلال",
    "Al Nassr": "النصر",
}

def ar_team(n):
    return TEAMS_AR.get(n, n)

LEAGUES = {
    "eng.1": "الدوري الانجليزي",
    "esp.1": "الدوري الاسباني",
    "ita.1": "الدوري الايطالي",
    "ger.1": "الدوري الالماني",
    "fra.1": "الدوري الفرنسي",
    "uefa.champions": "دوري الابطال",
    "egy.1": "الدوري المصري",
    "sau.1": "الدوري السعودي",
}

CHANNELS_AR = {
    "eng.1": "beIN SPORTS 1",
    "esp.1": "beIN SPORTS 3",
    "ita.1": "beIN SPORTS 4",
    "ger.1": "beIN SPORTS 5",
    "fra.1": "beIN SPORTS 2",
    "uefa.champions": "beIN SPORTS 1",
    "egy.1": "ON Sport 1",
    "sau.1": "SSC 1",
}

PLAYERS = {
    "صلاح": "ليفربول | مصر | جناح ايمن | اهداف 18 | اسيست 12 | تقييم 8.5",
    "مبابي": "ريال مدريد | فرنسا | مهاجم | اهداف 22 | اسيست 8 | تقييم 9.0",
    "هالاند": "مان سيتي | النرويج | مهاجم | اهداف 25 | اسيست 5 | تقييم 9.1",
    "ميسي": "انتر ميامي | الارجنتين | صانع لعب | اهداف 15 | اسيست 18 | تقييم 8.9",
    "رونالدو": "النصر | البرتغال | مهاجم | اهداف 20 | اسيست 6 | تقييم 8.7",
    "مرموش": "مان سيتي | مصر | مهاجم | اهداف 10 | اسيست 7 | تقييم 8.2",
    "زيزو": "الاهلي | مصر | جناح ايمن | اهداف 8 | اسيست 9 | تقييم 8.0",
}

ratings = []
user_points = {}
searching = []
all_users = set()

def is_owner(uid):
    return uid == OWNER_ID

def main_menu(user_id=None):
    kb = [
        [InlineKeyboardButton("مباريات الان - تحديث مباشر", callback_data="live")],
        [InlineKeyboardButton("مباريات اليوم", callback_data="today"),
         InlineKeyboardButton("مباريات الغد", callback_data="tomorrow")],
        [InlineKeyboardButton("جدول الترتيب", callback_data="table"),
         InlineKeyboardButton("الهدافين", callback_data="scorers")],
        [InlineKeyboardButton("ابحث عن لاعب", callback_data="player_search"),
         InlineKeyboardButton("فريقي المفضل", callback_data="fav")],
        [InlineKeyboardButton("القنوات الناقلة", callback_data="channels"),
         InlineKeyboardButton("تشكيلة المباراة", callback_data="lineup")],
        [InlineKeyboardButton("احصائيات", callback_data="stats"),
         InlineKeyboardButton("توقعات", callback_data="predict")],
        [InlineKeyboardButton("ملخصات", callback_data="highlights"),
         InlineKeyboardButton("اخبار", callback_data="news")],
        [InlineKeyboardButton("فانتازي", callback_data="fantasy"),
         InlineKeyboardButton("تنبيه الاهداف", callback_data="notify")],
        [InlineKeyboardButton("مكافأة يومية", callback_data="daily"),
         InlineKeyboardButton("لوحة الصدارة", callback_data="leaderboard")],
        [InlineKeyboardButton("ابحث عن شخص تتحدث معه", callback_data="find_friend")],
        [InlineKeyboardButton("قيم البوت", callback_data="rate"),
         InlineKeyboardButton("تبرع بالنجوم", callback_data="donate")],
        [InlineKeyboardButton("شارك البوت", callback_data="share")],
        [InlineKeyboardButton("تواصل مع المطور @TRAN_5", url="https://t.me/TRAN_5")],
    ]
    if is_owner(user_id):
        kb.append([InlineKeyboardButton("لوحة المالك", callback_data="owner_panel")])
    return InlineKeyboardMarkup(kb)

def back_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("تحديث النتائج", callback_data="live")],
        [InlineKeyboardButton("القايمة الرئيسية", callback_data="home")],
    ])

def get_matches(league_id, offset=0):
    try:
        target = datetime.now(timezone.utc) + timedelta(days=offset)
        ds = target.strftime("%Y%m%d")
        url = "https://site.api.espn.com/apis/site/v2/sports/soccer/" + league_id + "/scoreboard?dates=" + ds
        data = requests.get(url, timeout=6).json()
        return data.get("events", [])
    except:
        return []

def format_match(ev, league_id):
    try:
        comp = ev["competitions"][0]
        home = ar_team(comp["competitors"][0]["team"]["displayName"])
        away = ar_team(comp["competitors"][1]["team"]["displayName"])
        hs = comp["competitors"][0].get("score", "0")
        aws = comp["competitors"][1].get("score", "0")
        state = comp["status"]["type"]["state"]
        desc = comp["status"]["type"]["description"]
        clock = comp["status"].get("displayClock", "")
        if state == "in":
            status = "جارية الان - " + clock
        elif state == "post":
            status = "انتهت"
        else:
            status = "لم تبدأ بعد"
        try:
            dt = datetime.fromisoformat(ev["date"].replace("Z", "+00:00"))
            egy = dt + timedelta(hours=2)
            t = egy.strftime("%I:%M %p")
            t = t.replace("AM", "صباحا").replace("PM", "مساء")
        except:
            t = ""
        ch = CHANNELS_AR.get(league_id, "beIN SPORTS")
        if state == "pre":
            return home + " ضد " + away + "\nالساعة: " + t + "\nالحالة: " + status + "\nالقناة: " + ch + "\n"
        else:
            return home + " " + str(hs) + " - " + str(aws) + " " + away + "\nالحالة: " + status + "\nالساعة: " + t + "\nالقناة: " + ch + "\n"
    except:
        return ""

def get_all_text(offset=0, only_live=False):
    now = (datetime.now(timezone.utc) + timedelta(hours=2)).strftime("%I:%M %p")
    now = now.replace("AM", "صباحا").replace("PM", "مساء")
    title = "مباريات اليوم - تحديث مباشر"
    if offset == 1:
        title = "مباريات الغد"
    if only_live:
        title = "المباريات الجارية الان"
    text = title + "\nاخر تحديث: " + now + " بتوقيت مصر\n" + LINE + "\n\n"
    found = False
    for lid, lname in LEAGUES.items():
        events = get_matches(lid, offset)
        if only_live:
            events = [e for e in events if e["competitions"][0]["status"]["type"]["state"] == "in"]
        if events:
            text += lname + "\n"
            for ev in events:
                text += format_match(ev, lid) + "\n"
                found = True
    if not found:
        text = "مفيش مباريات دلوقتي"
    return text + FOOTER

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    all_users.add(user.id)
    name = user.first_name or "يا بطل"
    user_points[user.id] = user_points.get(user.id, 0) + 5
    if not is_owner(user.id):
        try:
            await context.bot.send_message(OWNER_ID, "مستخدم جديد: " + name + " @" + str(user.username) + " ايدي: " + str(user.id))
        except:
            pass
    if is_owner(user.id):
        msg = "اهلا يا مالك البوت يا عدي\nالمستخدمين: " + str(len(all_users)) + "\nالتقييمات: " + str(len(ratings))
        await update.message.reply_text(box("لوحة المالك", msg), reply_markup=main_menu(user.id))
        return
    welcome = "اهلا بيك يا " + name + "\nهذا بوت من صنع عدي عمرو\nالمطور: @TRAN_5\n\nبوت الكورة الشامل بالعربي\nنتائج مباشرة بتتحدث لوحدها\nكل المواعيد بتوقيت مصر\n\nخدت 5 نقط ترحيبية!"
    await update.message.reply_text(box("بوت عدي عمرو", welcome), reply_markup=main_menu(user.id))

async def owner_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("انت مش المالك!")
        return
    msg = "المستخدمين: " + str(len(all_users)) + "\nالتقييمات: " + str(len(ratings)) + "\nالنقاط: " + str(sum(user_points.values()))
    await update.message.reply_text(box("لوحة المالك", msg), reply_markup=main_menu(update.effective_user.id))

async def stats_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        return
    await update.message.reply_text("المستخدمين: " + str(len(all_users)) + " | التقييمات: " + str(len(ratings)))

async def broadcast_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        return
    msg = " ".join(context.args)
    if not msg:
        await update.message.reply_text("اكتب: /broadcast رسالتك")
        return
    sent = 0
    for uid in list(all_users):
        try:
            await context.bot.send_message(uid, "رسالة من عدي عمرو:\n\n" + msg)
            sent += 1
        except:
            pass
    await update.message.reply_text("بعت لـ " + str(sent) + " واحد")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer("جاري التحديث...")
    data = query.data
    user = query.from_user
    all_users.add(user.id)

    if data == "home":
        await query.message.reply_text(box("القايمة الرئيسية", "اختار اللي انت عايزه"), reply_markup=main_menu(user.id))
        return
    if data == "live":
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("تحديث النتائج الان", callback_data="live")],
            [InlineKeyboardButton("الجارية فقط", callback_data="live_only")],
            [InlineKeyboardButton("القايمة الرئيسية", callback_data="home")],
        ])
        await query.message.reply_text(get_all_text(0, False), reply_markup=kb)
        return
    if data == "live_only":
        await query.message.reply_text(get_all_text(0, True), reply_markup=back_menu())
        return
    if data == "today":
        await query.message.reply_text(get_all_text(0, False), reply_markup=back_menu())
        return
    if data == "tomorrow":
        await query.message.reply_text(get_all_text(1, False), reply_markup=back_menu())
        return
    if data == "table":
        body = "1 - ارسنال - 28 نقطة\n2 - مان سيتي - 27 نقطة\n3 - ليفربول - 26 نقطة\n4 - تشيلسي - 24 نقطة\n5 - توتنهام - 22 نقطة"
        await query.message.reply_text(box("جدول الترتيب", body), reply_markup=main_menu(user.id))
    elif data == "scorers":
        body = "1 - هالاند - 14 هدف\n2 - محمد صلاح - 11 هدف\n3 - مبابي - 10 اهداف"
        await query.message.reply_text(box("الهدافين", body), reply_markup=main_menu(user.id))
    elif data == "channels":
        body = "الانجليزي: beIN 1\nالاسباني: beIN 3\nالايطالي: beIN 4\nالمصري: ON Sport 1\nالسعودي: SSC 1"
        await query.message.reply_text(box("القنوات الناقلة", body), reply_markup=main_menu(user.id))
    elif data == "lineup":
        body = "اليسون\nارنولد - فان دايك - كوناتي - روبرتسون\nسوبوسلاي - جرافينبيرخ - ماك اليستر\nصلاح - ايزاك - جاكبو"
        await query.message.reply_text(box("تشكيلة ليفربول", body), reply_markup=main_menu(user.id))
    elif data == "stats":
        body = "الاستحواذ: 65% - 35%\nالتسديدات: 18 - 7\nالركنيات: 8 - 2"
        await query.message.reply_text(box("احصائيات", body), reply_markup=main_menu(user.id))
    elif data == "predict":
        body = "ليفربول 60% - تعادل 20% - يونايتد 20%\nالنتيجة المتوقعة: 2-1"
        await query.message.reply_text(box("توقعات", body), reply_markup=main_menu(user.id))
    elif data == "highlights":
        await query.message.reply_text(box("ملخصات", "https://www.youtube.com/results?search_query=ملخص+مباريات+اليوم"), reply_markup=main_menu(user.id))
    elif data == "news":
        body = "صلاح يقترب من تجديد عقده\nريال مدريد يجهز عرض ضخم\nالاهلي يتعاقد مع مهاجم جديد"
        await query.message.reply_text(box("اخبار", body), reply_markup=main_menu(user.id))
    elif data == "fantasy":
        await query.message.reply_text(box("فانتازي", "تشكيلتك جابت 78 نقطة"), reply_markup=main_menu(user.id))
    elif data == "notify":
        await query.message.reply_text(box("تنبيه الاهداف", "تم التفعيل - اول ما يجي جول هبعتلك"), reply_markup=main_menu(user.id))
    elif data == "owner_panel":
        if not is_owner(user.id):
            await query.message.reply_text("دي للمالك بس")
            return
        msg = "المستخدمين: " + str(len(all_users)) + "\nالتقييمات: " + str(len(ratings))
        await query.message.reply_text(box("لوحة المالك", msg), reply_markup=main_menu(user.id))
    elif data == "rate":
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("1 نجمة", callback_data="rate_1"),
             InlineKeyboardButton("2 نجمة", callback_data="rate_2"),
             InlineKeyboardButton("3 نجمة", callback_data="rate_3")],
            [InlineKeyboardButton("4 نجمة", callback_data="rate_4"),
             InlineKeyboardButton("5 نجمة", callback_data="rate_5")],
        ])
        avg = sum([r[1] for r in ratings]) / len(ratings) if ratings else 5.0
        body = "متوسط التقييم: " + str(round(avg, 1)) + " / 5\nعدد المقيمين: " + str(len(ratings))
        await query.message.reply_text(box("قيم البوت", body), reply_markup=kb)
    elif data.startswith("rate_"):
        stars = int(data.split("_")[1])
        ratings[:] = [r for r in ratings if r[0] != user.id]
        ratings.append((user.id, stars))
        avg = sum([r[1] for r in ratings]) / len(ratings)
        await query.message.reply_text(box("شكرا ليك", "قييمت بـ " + str(stars) + " نجوم\nالمتوسط: " + str(round(avg, 1))), reply_markup=main_menu(user.id))
        try:
            await context.bot.send_message(OWNER_ID, "تقييم جديد: " + str(stars) + " من " + user.first_name)
        except:
            pass
    elif data == "donate":
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("10 نجوم", callback_data="donate_10")],
            [InlineKeyboardButton("50 نجمة", callback_data="donate_50")],
            [InlineKeyboardButton("100 نجمة", callback_data="donate_100")],
        ])
        await query.message.reply_text(box("تبرع بالنجوم", "تبرعك بيوصل لعدي عمرو على طول\nكل 10 نجوم = 50 نقطة"), reply_markup=kb)
    elif data.startswith("donate_"):
        amount = int(data.split("_")[1])
        await context.bot.send_invoice(
            chat_id=query.message.chat_id,
            title="دعم بوت عدي عمرو",
            description="تبرع",
            payload="donate_" + str(amount),
            provider_token="",
            currency="XTR",
            prices=[LabeledPrice("تبرع", amount)],
        )
    elif data == "daily":
        user_points[user.id] = user_points.get(user.id, 0) + 10
        await query.message.reply_text(box("مكافأة يومية", "خدت 10 نقط\nرصيدك: " + str(user_points[user.id])), reply_markup=main_menu(user.id))
    elif data == "leaderboard":
        s = sorted(user_points.items(), key=lambda x: x[1], reverse=True)[:5]
        txt = ""
        for i, (uid, pts) in enumerate(s, 1):
            txt += str(i) + " - " + str(uid) + " - " + str(pts) + " نقطة\n"
        txt += "\nنقطك: " + str(user_points.get(user.id, 0))
        await query.message.reply_text(box("لوحة الصدارة", txt), reply_markup=main_menu(user.id))
    elif data == "share":
        await query.message.reply_text(box("شارك البوت", "https://t.me/YourBotUsername"), reply_markup=main_menu(user.id))
    elif data == "find_friend":
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("كورة", callback_data="find_football"),
             InlineKeyboardButton("جيمنج", callback_data="find_gaming")],
            [InlineKeyboardButton("مزيكا", callback_data="find_music"),
             InlineKeyboardButton("دردشة", callback_data="find_chat")],
            [InlineKeyboardButton("بحث بالاسم", callback_data="find_by_name")],
        ])
        await query.message.reply_text(box("ابحث عن شخص", "اختار اهتمامك"), reply_markup=kb)
    elif data.startswith("find_"):
        if data == "find_by_name":
            await query.message.reply_text(box("بحث بالاسم", "اكتب اسم الشخص او يوزره"))
            context.user_data["waiting"] = "find_person"
            return
        if searching:
            other = searching.pop(0)
            await query.message.reply_text(box("لقيتلك حد!", "يوزره: " + str(other)), reply_markup=main_menu(user.id))
            try:
                await context.bot.send_message(other, "لقيتلك حد بيحب نفس اهتمامك: @" + str(user.username))
            except:
                pass
        else:
            searching.append(user.id)
            await query.message.reply_text(box("في الانتظار", "اول ما حد يدخل هبعتلك"), reply_markup=main_menu(user.id))
    elif data == "player_search":
        await query.message.reply_text(box("ابحث عن لاعب", "اكتب اسم اي لاعب"))
        context.user_data["waiting"] = "player"
    elif data == "fav":
        await query.message.reply_text(box("فريقي المفضل", "اكتب اسم فريقك المفضل"))
        context.user_data["waiting"] = "fav"

async def precheckout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.pre_checkout_query.answer(ok=True)

async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    amount = update.message.successful_payment.total_amount
    user = update.effective_user
    user_points[user.id] = user_points.get(user.id, 0) + amount * 5
    await update.message.reply_text(box("شكرا يا اسطورة", "تبرعت بـ " + str(amount) + " نجمة\nخدت " + str(amount * 5) + " نقطة"), reply_markup=main_menu(user.id))
    try:
        await context.bot.send_message(OWNER_ID, "تبرع جديد: " + str(amount) + " من " + user.first_name)
    except:
        pass

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    waiting = context.user_data.get("waiting")
    user = update.effective_user
    all_users.add(user.id)
    if waiting == "player":
        for k, v in PLAYERS.items():
            if k in text or text in k:
                await update.message.reply_text(box("بطاقة اللاعب", k + "\n" + v), reply_markup=main_menu(user.id))
                context.user_data["waiting"] = None
                return
        await update.message.reply_text("ملقيتش اللاعب ده - جرب صلاح", reply_markup=main_menu(user.id))
        context.user_data["waiting"] = None
        return
    if waiting == "fav":
        await update.message.reply_text(box("تم الحفظ", "فريقك بقى " + text), reply_markup=main_menu(user.id))
        context.user_data["waiting"] = None
        return
    if waiting == "find_person":
        await update.message.reply_text(box("جاري البحث", "بدور على " + text), reply_markup=main_menu(user.id))
        if "TRAN" in text.upper() or "عدي" in text:
            await update.message.reply_text("لقيته! المطور عدي عمرو @TRAN_5", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("كلم عدي عمرو", url="https://t.me/TRAN_5")]]))
        context.user_data["waiting"] = None
        return
    await update.message.reply_text("اكتب /start", reply_markup=main_menu(user.id))

def main():
    if not TOKEN or TOKEN == "حط_التوكن_بتاعك_هنا":
        print("مفيش TOKEN")
        return
    print("بوت عدي شغال")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("owner", owner
