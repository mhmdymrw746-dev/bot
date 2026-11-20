‏import os
‏import threading
‏import requests
‏import random
‏from http.server import BaseHTTPRequestHandler, HTTPServer
‏from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
‏from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, PreCheckoutQueryHandler
‏from datetime import datetime, timezone, timedelta
‏
‏TOKEN = os.environ.get("TOKEN")
‏OWNER_ID = 8188263997
‏
‏class H(BaseHTTPRequestHandler):
‏    def do_GET(self):
‏        self.send_response(200)
‏        self.end_headers()
‏        self.wfile.write(b"ok")
‏    def log_message(self, *a):
‏        pass
‏
‏def keep():
‏    p = int(os.environ.get("PORT", 10000))
‏    try:
‏        HTTPServer(("0.0.0.0", p), H).serve_forever()
‏    except:
‏        pass
‏
‏threading.Thread(target=keep, daemon=True).start()
‏
‏ratings = []
‏points = {}
‏searching = []
‏all_users = set()
‏notify_users = set()
‏predictions = {}
‏
‏LEAGUES = {}
‏LEAGUES["eng.1"] = "الدوري الانجليزي"
‏LEAGUES["esp.1"] = "الدوري الاسباني"
‏LEAGUES["ita.1"] = "الدوري الايطالي"
‏LEAGUES["ger.1"] = "الدوري الالماني"
‏LEAGUES["fra.1"] = "الدوري الفرنسي"
‏LEAGUES["uefa.champions"] = "دوري ابطال اوروبا"
‏LEAGUES["egy.1"] = "الدوري المصري"
‏LEAGUES["sau.1"] = "الدوري السعودي"
‏
‏TEAMS = {}
‏TEAMS["Liverpool"] = "ليفربول"
‏TEAMS["Arsenal"] = "ارسنال"
‏TEAMS["Manchester City"] = "مانشستر سيتي"
‏TEAMS["Manchester United"] = "مانشستر يونايتد"
‏TEAMS["Chelsea"] = "تشيلسي"
‏TEAMS["Real Madrid"] = "ريال مدريد"
‏TEAMS["Barcelona"] = "برشلونة"
‏TEAMS["Bayern Munich"] = "بايرن ميونخ"
‏TEAMS["Paris Saint-Germain"] = "باريس سان جيرمان"
‏TEAMS["Al Ahly"] = "الاهلي"
‏TEAMS["Zamalek"] = "الزمالك"
‏TEAMS["Al Hilal"] = "الهلال"
‏TEAMS["Al Nassr"] = "النصر"
‏
‏PLAYERS = {}
‏PLAYERS["صلاح"] = "ليفربول | مصر | اهداف 18 | تقييم 8.5"
‏PLAYERS["مبابي"] = "ريال مدريد | فرنسا | اهداف 22 | تقييم 9.0"
‏PLAYERS["هالاند"] = "مان سيتي | النرويج | اهداف 25 | تقييم 9.1"
‏PLAYERS["ميسي"] = "انتر ميامي | الارجنتين | اهداف 15 | تقييم 8.9"
‏PLAYERS["رونالدو"] = "النصر | البرتغال | اهداف 20 | تقييم 8.7"
‏PLAYERS["مرموش"] = "مان سيتي | مصر | اهداف 10 | تقييم 8.2"
‏PLAYERS["زيزو"] = "الاهلي | مصر | اهداف 8 | تقييم 8.0"
‏
‏QUIZ = []
‏QUIZ.append(["مين اكتر لاعب سجل اهداف في كاس العالم؟", "كلوزه", "رونالدو", "ميسي", "مبابي", "كلوزه"])
‏QUIZ.append(["فين فريق الاهلي بيلعب؟", "القاهرة", "الجيزة", "اسكندرية", "اسوان", "القاهرة"])
‏QUIZ.append(["كم مرة ريال مدريد خد الابطال؟", "15", "14", "13", "12", "15"])
‏QUIZ.append(["مين هداف الدوري الانجليزي دلوقتي؟", "هالاند", "صلاح", "مبابي", "كين", "هالاند"])
‏QUIZ.append(["منتخب مصر خد امم افريقيا كام مرة؟", "7", "6", "5", "4", "7"])
‏
‏def ar_team(n):
‏    if n in TEAMS:
‏        return TEAMS[n]
‏    return n
‏
‏def get_avg():
‏    if len(ratings) == 0:
‏        return 0
‏    total = 0
‏    for r in ratings:
‏        total = total + r[1]
‏    return total / len(ratings)
‏
‏def get_count(stars):
‏    c = 0
‏    for r in ratings:
‏        if r[1] == stars:
‏            c = c + 1
‏    return c
‏
‏def box(title, body):
‏    t = "=== "
‏    t = t + title
‏    t = t + " ===\n\n"
‏    t = t + body
‏    t = t + "\n\n--------------\n"
‏    t = t + "بوت عدي عمرو | @TRAN_5"
‏    return t
‏
‏def ratings_text():
‏    avg = get_avg()
‏    body = ""
‏    if len(ratings) == 0:
‏        body = "لسه مفيش تقييمات\nكن اول واحد يقيم"
‏        return box("تقييمات البوت", body)
‏    body = body + "المتوسط: "
‏    body = body + str(round(avg, 1))
‏    body = body + " من 5\n"
‏    body = body + "عدد المقيمين: "
‏    body = body + str(len(ratings))
‏    body = body + "\n\n"
‏    body = body + "التوزيع:\n"
‏    body = body + "5 نجوم: "
‏    body = body + str(get_count(5))
‏    body = body + "\n"
‏    body = body + "4 نجوم: "
‏    body = body + str(get_count(4))
‏    body = body + "\n"
‏    body = body + "3 نجوم: "
‏    body = body + str(get_count(3))
‏    body = body + "\n"
‏    body = body + "نجمتين: "
‏    body = body + str(get_count(2))
‏    body = body + "\n"
‏    body = body + "نجمة: "
‏    body = body + str(get_count(1))
‏    body = body + "\n\n"
‏    body = body + "اخر التقييمات:\n"
‏    last = ratings[-5:]
‏    for r in last:
‏        s_txt = ""
‏        for i in range(r[1]):
‏            s_txt = s_txt + "*"
‏        body = body + s_txt
‏        body = body + " من "
‏        body = body + str(r[2])
‏        body = body + "\n"
‏    return box("تقييمات البوت", body)
‏
‏def users_text():
‏    body = ""
‏    body = body + "جرب البوت: "
‏    body = body + str(len(all_users))
‏    body = body + " واحد\n"
‏    body = body + "قيم البوت: "
‏    body = body + str(len(ratings))
‏    body = body + " واحد\n"
‏    body = body + "مفعل التنبيه: "
‏    body = body + str(len(notify_users))
‏    body = body + " واحد\n\n"
‏    if len(all_users) >= 100:
‏        body = body + "البوت مكسر الدنيا! +100 واحد"
‏    elif len(all_users) >= 50:
‏        body = body + "قربنا نوصل 100!"
‏    elif len(all_users) >= 10:
‏        body = body + "البوت بيكبر كل يوم!"
‏    else:
‏        body = body + "لسه في البداية، شارك البوت!"
‏    return box("عدد مجربين البوت", body)
‏
‏def channels_text():
‏    body = ""
‏    body = body + "القنوات الناقلة\n"
‏    body = body + "------------\n\n"
‏    body = body + "beIN SPORTS\n"
‏    body = body + "beIN 1 - انجليزي + ابطال\n"
‏    body = body + "beIN 2 - فرنسي\n"
‏    body = body + "beIN 3 - اسباني\n"
‏    body = body + "beIN 4 - ايطالي\n"
‏    body = body + "beIN 5 - الماني\n\n"
‏    body = body + "ON Sport\n"
‏    body = body + "ON 1 - الدوري المصري\n"
‏    body = body + "ON 2 - الدوري المصري\n\n"
‏    body = body + "SSC\n"
‏    body = body + "SSC 1 - الدوري السعودي\n"
‏    body = body + "SSC 2 - الدوري السعودي\n\n"
‏    body = body + "الترددات:\n"
‏    body = body + "beIN: 11013 افقي\n"
‏    body = body + "ON: 11861 عمودي\n"
‏    body = body + "SSC: 12523 عمودي"
‏    return box("القنوات الناقلة", body)
‏
‏def menu(uid):
‏    kb = []
‏    kb.append([InlineKeyboardButton("مباريات الان", callback_data="live")])
‏    kb.append([InlineKeyboardButton("ماتش اليوم", callback_data="match_day")])
‏    kb.append([InlineKeyboardButton("مباريات اليوم", callback_data="today")])
‏    kb.append([InlineKeyboardButton("مباريات الغد", callback_data="tomorrow")])
‏    kb.append([InlineKeyboardButton("القنوات الناقلة", callback_data="channels")])
‏    kb.append([InlineKeyboardButton("مسابقة يومية", callback_data="quiz")])
‏    kb.append([InlineKeyboardButton("توقع واكسب 50 نقطة", callback_data="predict_game")])
‏    kb.append([InlineKeyboardButton("جرب حظك", callback_data="luck")])
‏    kb.append([InlineKeyboardButton("تنبيه الاهداف", callback_data="notify")])
‏    kb.append([InlineKeyboardButton("افضل لاعب اليوم", callback_data="best_player")])
‏    kb.append([InlineKeyboardButton("جدول الترتيب", callback_data="table")])
‏    kb.append([InlineKeyboardButton("الهدافين", callback_data="scorers")])
‏    kb.append([InlineKeyboardButton("ابحث عن لاعب", callback_data="player")])
‏    kb.append([InlineKeyboardButton("فريقي المفضل", callback_data="fav")])
‏    kb.append([InlineKeyboardButton("اخبار", callback_data="news")])
‏    kb.append([InlineKeyboardButton("فانتازي", callback_data="fantasy")])
‏    kb.append([InlineKeyboardButton("مكافأة يومية", callback_data="daily")])
‏    kb.append([InlineKeyboardButton("لوحة الصدارة", callback_data="top")])
‏    kb.append([InlineKeyboardButton("ابحث عن شخص", callback_data="find")])
‏    kb.append([InlineKeyboardButton("التقييمات", callback_data="ratings")])
‏    kb.append([InlineKeyboardButton("قيم البوت", callback_data="rate")])
‏    kb.append([InlineKeyboardButton("عدد مجربين البوت", callback_data="users")])
‏    kb.append([InlineKeyboardButton("تبرع بالنجوم", callback_data="donate")])
‏    kb.append([InlineKeyboardButton("شارك البوت", callback_data="share")])
‏    kb.append([InlineKeyboardButton("تواصل مع المطور", url="https://t.me/TRAN_5")])
‏    if uid == OWNER_ID:
‏        kb.append([InlineKeyboardButton("لوحة المالك", callback_data="owner")])
‏    return InlineKeyboardMarkup(kb)
‏
‏def back():
‏    kb = []
‏    kb.append([InlineKeyboardButton("تحديث", callback_data="live")])
‏    kb.append([InlineKeyboardButton("القايمة", callback_data="home")])
‏    return InlineKeyboardMarkup(kb)
‏
‏def get_matches(lid, off):
‏    try:
‏        d = datetime.now(timezone.utc) + timedelta(days=off)
‏        ds = d.strftime("%Y%m%d")
‏        u = "https://site.api.espn.com/apis/site/v2/sports/soccer/"
‏        u = u + lid + "/scoreboard?dates=" + ds
‏        j = requests.get(u, timeout=6).json()
‏        return j.get("events", [])
‏    except:
‏        return []
‏
‏def get_channel(lid):
‏    if lid == "egy.1":
‏        return "ON Sport 1"
‏    if lid == "sau.1":
‏        return "SSC 1"
‏    if lid == "esp.1":
‏        return "beIN 3"
‏    if lid == "ita.1":
‏        return "beIN 4"
‏    if lid == "ger.1":
‏        return "beIN 5"
‏    if lid == "fra.1":
‏        return "beIN 2"
‏    return "beIN 1"
‏
‏def fmt(ev, lid):
‏    try:
‏        c = ev["competitions"][0]
‏        h = c["competitors"][0]["team"]["displayName"]
‏        a = c["competitors"][1]["team"]["displayName"]
‏        h = ar_team(h)
‏        a = ar_team(a)
‏        hs = c["competitors"][0].get("score", "0")
‏        aw = c["competitors"][1].get("score", "0")
‏        st = c["status"]["type"]["state"]
‏        clock = c["status"].get("displayClock", "")
‏        if st == "in":
‏            s = "جارية الان " + clock
‏        elif st == "post":
‏            s = "انتهت"
‏        else:
‏            s = "لم تبدأ بعد"
‏        try:
‏            dt = datetime.fromisoformat(ev["date"].replace("Z", "+00:00"))
‏            egy = dt + timedelta(hours=2)
‏            t = egy.strftime("%I:%M %p")
‏            t = t.replace("AM", "صباحا")
‏            t = t.replace("PM", "مساء")
‏        except:
‏            t = ""
‏        ch = get_channel(lid)
‏        line = h + " " + str(hs)
‏        line = line + " - " + str(aw)
‏        line = line + " " + a + "\n"
‏        line = line + s + " | " + t + "\n"
‏        line = line + "القناة: " + ch + "\n"
‏        line = line + "------------\n"
‏        return line
‏    except:
‏        return ""
‏
‏def all_text(off, only_live):
‏    t = "مباريات اليوم\n"
‏    if off == 1:
‏        t = "مباريات الغد\n"
‏    if only_live:
‏        t = "المباريات الجارية الان\n"
‏    now = datetime.now(timezone.utc) + timedelta(hours=2)
‏    now_s = now.strftime("%I:%M %p")
‏    now_s = now_s.replace("AM", "صباحا")
‏    now_s = now_s.replace("PM", "مساء")
‏    t = t + "اخر تحديث: "
‏    t = t + now_s
‏    t = t + " بتوقيت مصر\n"
‏    t = t + "--------------\n\n"
‏    for lid in LEAGUES:
‏        name = LEAGUES[lid]
‏        evs = get_matches(lid, off)
‏        if only_live:
‏            new_evs = []
‏            for e in evs:
‏                st2 = e["competitions"][0]["status"]["type"]["state"]
‏                if st2 == "in":
‏                    new_evs.append(e)
‏            evs = new_evs
‏        if evs:
‏            t = t + name + "\n"
‏            t = t + "------------\n"
‏            for e in evs:
‏                t = t + fmt(e, lid)
‏    if t == "مباريات اليوم\n":
‏        t = "مفيش مباريات دلوقتي"
‏    t = t + "\nبوت عدي عمرو | @TRAN_5"
‏    return t
‏
‏async def start(update, context):
‏    u = update.effective_user
‏    is_new = u.id not in all_users
‏    all_users.add(u.id)
‏    if u.id not in points:
‏        points[u.id] = 5
‏    else:
‏        points[u.id] = points[u.id] + 5
‏    if is_new and u.id != OWNER_ID:
‏        try:
‏            msg = "مستخدم جديد جرب البوت!\nالاسم: "
‏            msg = msg + str(u.first_name)
‏            msg = msg + "\nاليوزر: @"
‏            msg = msg + str(u.username)
‏            msg = msg + "\nاجمالي: "
‏            msg = msg + str(len(all_users))
‏            await context.bot.send_message(OWNER_ID, msg)
‏        except:
‏            pass
‏    body = ""
‏    body = body + "اهلا بيك يا " + str(u.first_name) + "\n"
‏    body = body + "هذا بوت من صنع عدي عمرو\n"
‏    body = body + "المطور: @TRAN_5\n\n"
‏    body = body + "مميزات البوت:\n"
‏    body = body + "نتائج مباشرة بتتحدث\n"
‏    body = body + "القناة الناقلة لكل مباراة\n"
‏    body = body + "مسابقة يومية و توقع واكسب\n"
‏    body = body + "مواعيد بتوقيت مصر\n"
‏    body = body + "جرب البوت: "
‏    body = body + str(len(all_users))
‏    body = body + " واحد\n"
‏    body = body + "تقييم البوت: "
‏    body = body + str(round(get_avg(), 1))
‏    body = body + " من 5\n\n"
‏    body = body + "خدت 5 نقط\nرصيدك: "
‏    body = body + str(points[u.id])
‏    txt = box("بوت عدي عمرو", body)
‏    await update.message.reply_text(txt, reply_markup=menu(u.id))
‏
‏async def owner_cmd(update, context):
‏    if update.effective_user.id != OWNER_ID:
‏        await update.message.reply_text("انت مش المالك")
‏        return
‏    body = "اللي جربوا: "
‏    body = body + str(len(all_users))
‏    body = body + "\nالتقييمات: "
‏    body = body + str(len(ratings))
‏    body = body + "\nالمتوسط: "
‏    body = body + str(round(get_avg(), 1))
‏    body = body + "\nالتنبيهات: "
‏    body = body + str(len(notify_users))
‏    txt = box("لوحة المالك", body)
‏    await update.message.reply_text(txt, reply_markup=menu(OWNER_ID))
‏
‏async def stats_cmd(update, context):
‏    if update.effective_user.id != OWNER_ID:
‏        return
‏    txt = "اللي جربوا: "
‏    txt = txt + str(len(all_users))
‏    txt = txt + " | التقييمات: "
‏    txt = txt + str(len(ratings))
‏    await update.message.reply_text(txt)
‏
‏async def broadcast_cmd(update, context):
‏    if update.effective_user.id != OWNER_ID:
‏        return
‏    msg = " ".join(context.args)
‏    if not msg:
‏        await update.message.reply_text("اكتب: /broadcast رسالتك")
‏        return
‏    sent = 0
‏    for uid in list(all_users):
‏        try:
‏            m2 = "رسالة من عدي عمرو\n\n" + msg
‏            await context.bot.send_message(uid, m2)
‏            sent = sent + 1
‏        except:
‏            pass
‏    await update.message.reply_text("بعت لـ " + str(sent) + " واحد")
‏
‏async def btn(update, context):
‏    q = update.callback_query
‏    await q.answer()
‏    d = q.data
‏    u = q.from_user
‏    all_users.add(u.id)
‏    if d == "home":
‏        await q.message.reply_text("القايمة الرئيسية", reply_markup=menu(u.id))
‏        return
‏    if d == "live":
‏        kb = []
‏        kb.append([InlineKeyboardButton("تحديث الان", callback_data="live")])
‏        kb.append([InlineKeyboardButton("الجارية فقط", callback_data="liveonly")])
‏        kb.append([InlineKeyboardButton("القايمة", callback_data="home")])
‏        txt = all_text(0, False)
‏        await q.message.reply_text(txt, reply_markup=InlineKeyboardMarkup(kb))
‏        return
‏    if d == "liveonly":
‏        txt = all_text(0, True)
‏        await q.message.reply_text(txt, reply_markup=back())
‏        return
‏    if d == "today":
‏        txt = all_text(0, False)
‏        await q.message.reply_text(txt, reply_markup=back())
‏        return
‏    if d == "tomorrow":
‏        txt = all_text(1, False)
‏        await q.message.reply_text(txt, reply_markup=back())
‏        return
‏    if d == "match_day":
‏        body = "ماتش اليوم\n\n"
‏        body = body + "ليفربول ضد تشيلسي\n"
‏        body = body + "الساعة: 6:30 مساء بتوقيت مصر\n"
‏        body = body + "القناة: beIN 1\n"
‏        body = body + "الملعب: انفيلد\n"
‏        body = body + "توقعنا: فوز ليفربول 2-1\n\n"
‏        body = body + "توقع انت كمان واكسب 50 نقطة!"
‏        kb = []
‏        kb.append([InlineKeyboardButton("توقع النتيجة", callback_data="predict_game")])
‏        kb.append([InlineKeyboardButton("القايمة", callback_data="home")])
‏        txt = box("ماتش اليوم", body)
‏        await q.message.reply_text(txt, reply_markup=InlineKeyboardMarkup(kb))
‏    elif d == "quiz":
‏        qq = random.choice(QUIZ)
‏        context.user_data["quiz_ans"] = qq[5]
‏        kb = []
‏        kb.append([InlineKeyboardButton(qq[1], callback_data="quiz_ans_0")])
‏        kb.append([InlineKeyboardButton(qq[2], callback_data="quiz_ans_1")])
‏        kb.append([InlineKeyboardButton(qq[3], callback_data="quiz_ans_2")])
‏        kb.append([InlineKeyboardButton(qq[4], callback_data="quiz_ans_3")])
‏        context.user_data["quiz_opts"] = [qq[1], qq[2], qq[3], qq[4]]
‏        body = "سؤال اليوم\n\n"
‏        body = body + qq[0]
‏        body = body + "\n\nلو جاوبت صح هتاخد 30 نقطة!"
‏        txt = box("مسابقة يومية", body)
‏        await q.message.reply_text(txt, reply_markup=InlineKeyboardMarkup(kb))
‏    elif d.startswith("quiz_ans_"):
‏        idx = int(d.split("_")[2])
‏        opts = context.user_data.get("quiz_opts", [])
‏        ans = context.user_data.get("quiz_ans", "")
‏        if idx < len(opts) and opts[idx] == ans:
‏            if u.id not in points:
‏                points[u.id] = 30
‏            else:
‏                points[u.id] = points[u.id] + 30
‏            body = "صح يا بطل!\nخدت 30 نقطة\nرصيدك: "
‏            body = body + str(points[u.id])
‏            txt = box("اجابة صح", body)
‏            await q.message.reply_text(txt, reply_markup=menu(u.id))
‏        else:
‏            body = "غلط\nالاجابة الصح: "
‏            body = body + ans
‏            txt = box("اجابة غلط", body)
‏            await q.message.reply_text(txt, reply_markup=menu(u.id))
‏    elif d == "predict_game":
‏        kb = []
‏        kb.append([InlineKeyboardButton("ليفربول هيكسب", callback_data="pred_home")])
‏        kb.append([InlineKeyboardButton("تعادل", callback_data="pred_draw")])
‏        kb.append([InlineKeyboardButton("تشيلسي هيكسب", callback_data="pred_away")])
‏        body = "توقع واكسب\n\nماتش اليوم: ليفربول ضد تشيلسي\nلو توقعت صح هتاخد 50 نقطة"
‏        txt = box("توقع واكسب", body)
‏        await q.message.reply_text(txt, reply_markup=InlineKeyboardMarkup(kb))
‏    elif d.startswith("pred_"):
‏        predictions[u.id] = d
‏        body = "تم تسجيل توقعك!\n"
‏        body = body + "لو صح هتاخد 50 نقطة اول ما الماتش يخلص"
‏        txt = box("تم التوقع", body)
‏        await q.message.reply_text(txt, reply_markup=menu(u.id))
‏    elif d == "luck":
‏        num = random.randint(1, 10)
‏        if num >= 8:
‏            win = random.randint(10, 50)
‏            if u.id not in points:
‏                points[u.id] = win
‏            else:
‏                points[u.id] = points[u.id] + win
‏            body = "يا بختك!\nكسبت "
‏            body = body + str(win)
‏            body = body + " نقطة\nرصيدك: "
‏            body = body + str(points[u.id])
‏            txt = box("جرب حظك", body)
‏            await q.message.reply_text(txt, reply_markup=menu(u.id))
‏        elif num >= 5:
‏            body = "حظك متوسط\nجرب تاني كمان ساعة!"
‏            txt = box("جرب حظك", body)
‏            await q.message.reply_text(txt, reply_markup=menu(u.id))
‏        else:
‏            body = "معلش محصلش نصيب\nجرب تاني!"
‏            txt = box("جرب حظك", body)
‏            await q.message.reply_text(txt, reply_markup=menu(u.id))
‏    elif d == "notify":
‏        if u.id in notify_users:
‏            notify_users.remove(u.id)
‏            body = "قفلت تنبيه الاهداف"
‏            txt = box("تنبيه الاهداف", body)
‏            await q.message.reply_text(txt, reply_markup=menu(u.id))
‏        else:
‏            notify_users.add(u.id)
‏            body = "فعلت تنبيه الاهداف!\nاول ما يجي جول هبعتلك على طول"
‏            txt = box("تنبيه الاهداف", body)
‏            await q.message.reply_text(txt, reply_markup=menu(u.id))
‏    elif d == "best_player":
‏        players_list = ["صلاح - ليفربول - سجل هدفين وعمل اسيست", "هالاند - مان سيتي - هاتريك", "مبابي - ريال مدريد - هدفين"]
‏        best = random.choice(players_list)
‏        body = "افضل لاعب اليوم\n\n"
‏        body = body + best
‏        body = body + "\n\nتقييمه: 9.5 من 10"
‏        txt = box("افضل لاعب", body)
‏        await q.message.reply_text(txt, reply_markup=menu(u.id))
‏    elif d == "channels":
‏        kb = []
‏        kb.append([InlineKeyboardButton("beIN SPORTS", callback_data="ch_bein")])
    if w == "find_person":
        if "TRAN" in t.upper():
            txt = box("لقيته!", "المطور عدي عمرو @TRAN_5")
            await update.message.reply_text(txt)
        elif "عدي" in t:
            txt = box("لقيته!", "المطور عدي عمرو @TRAN_5")
            await update.message.reply_text(txt)
        else:
            txt = box("جاري البحث", "بدور على " + t)
            await update.message.reply_text(txt)
        context.user_data["w"] = None
        return
    await update.message.reply_text("اكتب /start", reply_markup=menu(u.id))

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("owner", owner_cmd))
    app.add_handler(CommandHandler("stats", stats_cmd))
    app.add_handler(CommandHandler("broadcast", broadcast_cmd))
    app.add_handler(CallbackQueryHandler(btn))
    app.add_handler(PreCheckoutQueryHandler(precheckout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, pay_ok))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, txt_h))
    app.run_polling()

if __name__ == "__main__":
    main()
