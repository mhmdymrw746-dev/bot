import os, time, random, threading, requests, json
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN") or "حط_التوكن_هنا"
DATA_FILE = "data.json"

def load():
    try:
        with open(DATA_FILE) as f:
            return json.load(f)
    except:
        return {"users": {}, "tickets": {}}

def save(d):
    with open(DATA_FILE, "w") as f:
        json.dump(d, f)

db = load()

def get_user(uid, name=""):
    uid = str(uid)
    if uid not in db["users"]:
        db["users"][uid] = {"name": name, "cash": 1000, "bank": 0, "health": 100, "happy": 100, "energy": 100, "job": "بدون شغل", "car": "مفيش", "house": "مفيش", "married": "اعزب", "kids": 0, "level": 1, "xp": 0, "vip": False, "company": None, "farm": 0, "restaurant": 0, "hotel": 0, "stock": 0, "wanted": 0, "gang": None, "edu": 0, "passport": False, "visa_card": False, "pet": None, "warns": 0, "banned": False}
        save(db)
    return db["users"][uid]

app_flask = Flask(__name__)

@app_flask.route("/")
def home():
    return "TRAN BOT شغال"

def run_flask():
    app_flask.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

def self_ping():
    url = os.environ.get("RENDER_EXTERNAL_URL") or "https://اسم-بوتك.onrender.com"
    while True:
        time.sleep(840)
        try:
            requests.get(url, timeout=10)
            print("صحيت نفسي")
        except:
            pass

def KB(rows):
    return InlineKeyboardMarkup(rows)

def BACK():
    return KB([[InlineKeyboardButton("رجوع", callback_data="back")]])

def main_menu():
    return KB([
        [InlineKeyboardButton("بروفايلي", callback_data="profile"), InlineKeyboardButton("شغلي", callback_data="job_menu")],
        [InlineKeyboardButton("البنك", callback_data="bank"), InlineKeyboardButton("بيتي", callback_data="home_menu")],
        [InlineKeyboardButton("المتجر", callback_data="shop"), InlineKeyboardButton("العب واكسب", callback_data="play_menu")],
        [InlineKeyboardButton("عيلتي", callback_data="family"), InlineKeyboardButton("شركتي", callback_data="company")],
        [InlineKeyboardButton("مزرعتي", callback_data="farm"), InlineKeyboardButton("مطعمي", callback_data="restaurant")],
        [InlineKeyboardButton("فندقي", callback_data="hotel"), InlineKeyboardButton("عصابة", callback_data="gang_menu")],
        [InlineKeyboardButton("تعليم", callback_data="edu_menu"), InlineKeyboardButton("سفر", callback_data="travel")],
        [InlineKeyboardButton("بورصة", callback_data="stock"), InlineKeyboardButton("VIP", callback_data="vip")],
        [InlineKeyboardButton("هدايا", callback_data="gift_menu"), InlineKeyboardButton("خدمة عملاء", callback_data="support")],
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    user = get_user(u.id, u.first_name)
    txt = f"اهلا بيك في عالم TRAN\n{user['name']} | لفل {user['level']}\nكاش: {user['cash']} | بنك: {user['bank']}\nصحة: {user['health']} | سعادة: {user['happy']}\nشغل: {user['job']}\nدوس على اي زرار"
    if update.message:
        await update.message.reply_text(txt, reply_markup=main_menu())
    else:
        await update.callback_query.edit_message_text(txt, reply_markup=main_menu())

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = str(q.from_user.id)
    user = get_user(uid, q.from_user.first_name)
    d = q.data
    if d == "back":
        await start(update, context)
        return
    if d == "profile":
        txt = f"بروفايلك\n{user['name']}\nكاش {user['cash']} | بنك {user['bank']}\nصحة {user['health']} | شغل {user['job']}\nعربية {user['car']} | بيت {user['house']}\nحالة {user['married']} | عيال {user['kids']}\nVIP {user['vip']}"
        await q.edit_message_text(txt, reply_markup=BACK())
    elif d == "bank":
        interest = int(user["bank"] * 0.05)
        txt = f"بنك TRAN\nكاش {user['cash']} | بنك {user['bank']}\nفايدة اليوم {interest}"
        await q.edit_message_text(txt, reply_markup=KB([
            [InlineKeyboardButton("ايداع 1000", callback_data="dep_1000"), InlineKeyboardButton("سحب 1000", callback_data="wit_1000")],
            [InlineKeyboardButton("ايداع الكل", callback_data="dep_all"), InlineKeyboardButton("سحب الكل", callback_data="wit_all")],
            [InlineKeyboardButton("خد الفايدة", callback_data="interest"), InlineKeyboardButton("فيزا 500", callback_data="visa")],
            [InlineKeyboardButton("قرض 10000", callback_data="loan"), InlineKeyboardButton("شهادة 5000", callback_data="cert")],
            [InlineKeyboardButton("رجوع", callback_data="back")]
        ]))
    elif d.startswith("dep_"):
        amt = user["cash"] if "all" in d else 1000
        if user["cash"] >= amt and amt > 0:
            user["cash"] -= amt
            user["bank"] += amt
            save(db)
            await q.edit_message_text(f"حطيت {amt} | بنكك {user['bank']}", reply_markup=BACK())
        else:
            await q.edit_message_text("معكش فلوس", reply_markup=BACK())
    elif d.startswith("wit_"):
        amt = user["bank"] if "all" in d else 1000
        if user["bank"] >= amt and amt > 0:
            user["bank"] -= amt
            user["cash"] += amt
            save(db)
            await q.edit_message_text(f"سحبت {amt} | كاشك {user['cash']}", reply_markup=BACK())
        else:
            await q.edit_message_text("معكش في البنك", reply_markup=BACK())
    elif d == "interest":
        intr = int(user["bank"] * 0.05)
        if intr > 0:
            user["bank"] += intr
            save(db)
            await q.edit_message_text(f"فايدة {intr} | بنكك {user['bank']}", reply_markup=BACK())
        else:
            await q.edit_message_text("حط فلوس الاول", reply_markup=BACK())
    elif d == "visa":
        if user["cash"] >= 500:
            user["cash"] -= 500
            user["visa_card"] = True
            save(db)
            await q.edit_message_text("مبروك فيزا", reply_markup=BACK())
        else:
            await q.edit_message_text("محتاج 500", reply_markup=BACK())
    elif d == "loan":
        user["cash"] += 10000
        save(db)
        await q.edit_message_text("خدت قرض 10000", reply_markup=BACK())
    elif d == "cert":
        if user["cash"] >= 5000:
            user["cash"] -= 5000
            user["bank"] += 7000
            save(db)
            await q.edit_message_text("شهادة! خدت 7000 في البنك", reply_markup=BACK())
        else:
            await q.edit_message_text("محتاج 5000", reply_markup=BACK())
    elif d == "job_menu":
        await q.edit_message_text("اختار شغلك", reply_markup=KB([
            [InlineKeyboardButton("اشتغل", callback_data="work"), InlineKeyboardButton("ادرس", callback_data="study")],
            [InlineKeyboardButton("اعمل شركة", callback_data="make_company"), InlineKeyboardButton("استثمر", callback_data="invest")],
            [InlineKeyboardButton("رجوع", callback_data="back")]
        ]))
    elif d == "work":
        jobs = [("يوتيوبر", 2000), ("لاعب كورة", 3000), ("دكتور", 5000), ("تاجر", 4000)]
        j, s = random.choice(jobs)
        user["cash"] += s
        user["job"] = j
        user["xp"] += 10
        save(db)
        await q.edit_message_text(f"اشتغلت {j} وكسبت {s}", reply_markup=BACK())
    elif d == "study":
        user["edu"] += 1
        user["xp"] += 20
        save(db)
        await q.edit_message_text(f"درست! مستواك {user['edu']}", reply_markup=BACK())
    elif d == "make_company":
        if user["cash"] >= 20000:
            user["cash"] -= 20000
            user["company"] = "شركة TRAN"
            save(db)
            await q.edit_message_text("مبروك عملت شركة", reply_markup=BACK())
        else:
            await q.edit_message_text("محتاج 20000", reply_markup=BACK())
    elif d == "invest":
        win = random.randint(-2000, 5000)
        user["cash"] += win
        save(db)
        await q.edit_message_text(f"استثمرت وكسبت {win}", reply_markup=BACK())
    elif d == "company":
        profit = random.randint(1000, 5000) if user["company"] else 0
        user["cash"] += profit
        save(db)
        await q.edit_message_text(f"شركتك {user['company'] or 'مفيش'} ربح {profit}", reply_markup=BACK())
    elif d == "farm":
        if user["farm"] == 0 and user["cash"] >= 10000:
            user["cash"] -= 10000
            user["farm"] = 1
            save(db)
            await q.edit_message_text("اشتريت مزرعة", reply_markup=BACK())
        elif user["farm"] > 0:
            h = random.randint(1000, 3000)
            user["cash"] += h
            save(db)
            await q.edit_message_text(f"حصدت وكسبت {h}", reply_markup=BACK())
        else:
            await q.edit_message_text("محتاج 10000", reply_markup=BACK())
    elif d == "restaurant":
        if user["restaurant"] == 0 and user["cash"] >= 15000:
            user["cash"] -= 15000
            user["restaurant"] = 1
            save(db)
            await q.edit_message_text("فتحت مطعم", reply_markup=BACK())
        elif user["restaurant"] > 0:
            p = random.randint(1000, 4000)
            user["cash"] += p
            save(db)
            await q.edit_message_text(f"مطعمك كسب {p}", reply_markup=BACK())
        else:
            await q.edit_message_text("محتاج 15000", reply_markup=BACK())
    elif d == "hotel":
        if user["hotel"] == 0 and user["cash"] >= 50000:
            user["cash"] -= 50000
            user["hotel"] = 1
            save(db)
            await q.edit_message_text("فتحت فندق", reply_markup=BACK())
        elif user["hotel"] > 0:
            p = random.randint(3000, 8000)
            user["cash"] += p
            save(db)
            await q.edit_message_text(f"فندقك كسب {p}", reply_markup=BACK())
        else:
            await q.edit_message_text("محتاج 50000", reply_markup=BACK())
    elif d == "home_menu":
        await q.edit_message_text("بيتك", reply_markup=KB([
            [InlineKeyboardButton("اشتري بيت", callback_data="buy_house"), InlineKeyboardButton("اشتري عربية", callback_data="buy_car")],
            [InlineKeyboardButton("حيوان اليف", callback_data="pet"), InlineKeyboardButton("رجوع", callback_data="back")]
        ]))
    elif d == "buy_house":
        if user["cash"] >= 100000:
            user["cash"] -= 100000
            user["house"] = "فيلا"
            save(db)
            await q.edit_message_text("اشتريت فيلا", reply_markup=BACK())
        else:
            await q.edit_message_text("محتاج 100000", reply_markup=BACK())
    elif d == "buy_car":
        if user["cash"] >= 50000:
            user["cash"] -= 50000
            user["car"] = "BMW"
            save(db)
            await q.edit_message_text("اشتريت BMW", reply_markup=BACK())
        else:
            await q.edit_message_text("محتاج 50000", reply_markup=BACK())
    elif d == "pet":
        p = random.choice(["كلب", "قطة", "حصان"])
        user["pet"] = p
        save(db)
        await q.edit_message_text(f"جبت {p}", reply_markup=BACK())
    elif d == "shop":
        await q.edit_message_text("المتجر", reply_markup=KB([
            [InlineKeyboardButton("عربية", callback_data="buy_car"), InlineKeyboardButton("بيت", callback_data="buy_house")],
            [InlineKeyboardButton("سلاح 5000", callback_data="buy_gun"), InlineKeyboardButton("ملابس 1000", callback_data="buy_clothes")],
            [InlineKeyboardButton("رجوع", callback_data="back")]
        ]))
    elif d == "buy_gun":
        if user["cash"] >= 5000:
            user["cash"] -= 5000
            save(db)
            await q.edit_message_text("اشتريت سلاح", reply_markup=BACK())
        else:
            await q.edit_message_text("محتاج 5000", reply_markup=BACK())
    elif d == "buy_clothes":
        if user["cash"] >= 1000:
            user["cash"] -= 1000
            user["happy"] += 10
            save(db)
            await q.edit_message_text("لبس جديد", reply_markup=BACK())
        else:
            await q.edit_message_text("محتاج 1000", reply_markup=BACK())
    elif d == "play_menu":
        await q.edit_message_text("العب واكسب", reply_markup=KB([
            [InlineKeyboardButton("كازينو", callback_data="casino"), InlineKeyboardButton("سباق", callback_data="race")],
            [InlineKeyboardButton("كنز", callback_data="treasure"), InlineKeyboardButton("حظي", callback_data="luck")],
            [InlineKeyboardButton("مهمة", callback_data="mission"), InlineKeyboardButton("رجوع", callback_data="back")]
        ]))
    elif d == "casino":
        win = random.randint(-2000, 5000)
        user["cash"] += win
        save(db)
        await q.edit_message_text(f"كازينو {win}", reply_markup=BACK())
    elif d == "race":
        win = random.choice([0, 1000, 5000, 10000])
        user["cash"] += win
        save(db)
        await q.edit_message_text(f"سباق كسبت {win}", reply_markup=BACK())
    elif d == "treasure":
        win = random.choice([0, 0, 2000, 10000, 50000])
        user["cash"] += win
        save(db)
        await q.edit_message_text(f"كنز لقيت {win}", reply_markup=BACK())
    elif d == "luck":
        user["cash"] += 500
        save(db)
        await q.edit_message_text("حظك حلو خدت 500", reply_markup=BACK())
    elif d == "mission":
        user["cash"] += 1000
        user["xp"] += 15
        save(db)
        await q.edit_message_text("خلصت مهمة +1000", reply_markup=BACK())
    elif d == "family":
        await q.edit_message_text("عيلتك", reply_markup=KB([
            [InlineKeyboardButton("اتجوز", callback_data="marry"), InlineKeyboardButton("طلق", callback_data="divorce")],
            [InlineKeyboardButton("خلف عيل", callback_data="baby"), InlineKeyboardButton("رجوع", callback_data="back")]
        ]))
    elif d == "marry":
        if user["married"] == "اعزب":
            user["married"] = "متجوز"
            user["happy"] += 30
            save(db)
            await q.edit_message_text("مبروك اتجوزت", reply_markup=BACK())
        else:
            await q.edit_message_text("انت متجوز اصلا", reply_markup=BACK())
    elif d == "divorce":
        if user["married"] != "اعزب":
            user["married"] = "اعزب"
            user["cash"] = int(user["cash"] / 2)
            save(db)
            await q.edit_message_text("اطلقت وخسرت نص فلوسك", reply_markup=BACK())
        else:
            await q.edit_message_text("انت اعزب اصلا", reply_markup=BACK())
    elif d == "baby":
        if user["married"] != "اعزب":
            user["kids"] += 1
            save(db)
            await q.edit_message_text(f"مبروك جالك عيل عندك {user['kids']}", reply_markup=BACK())
        else:
            await q.edit_message_text("لازم تتجوز الاول", reply_markup=BACK())
    elif d == "gang_menu":
        await q.edit_message_text("عصابة", reply_markup=KB([
            [InlineKeyboardButton("اعمل عصابة", callback_data="make_gang"), InlineKeyboardButton("حرب", callback_data="war")],
            [InlineKeyboardButton("اسرق", callback_data="steal"), InlineKeyboardButton("رجوع", callback_data="back")]
        ]))
    elif d == "make_gang":
        user["gang"] = "عصابة TRAN"
        save(db)
        await q.edit_message_text("عملت عصابة TRAN", reply_markup=BACK())
    elif d == "war":
        if random.choice([True, False]):
            user["cash"] += 5000
            save(db)
            await q.edit_message_text("كسبت الحرب +5000", reply_markup=BACK())
        else:
            user["cash"] -= 2000
            user["health"] -= 20
            save(db)
            await q.edit_message_text("خسرت الحرب", reply_markup=BACK())
    elif d == "steal":
        if random.random() < 0.5:
            user["cash"] += 3000
            save(db)
            await q.edit_message_text("سرقت 3000", reply_markup=BACK())
        else:
            user["wanted"] += 1
            save(db)
            await q.edit_message_text("اتمسكت مطلوب +1", reply_markup=BACK())
    elif d == "edu_menu":
        await q.edit_message_text("تعليم", reply_markup=KB([
            [InlineKeyboardButton("ادرس", callback_data="study"), InlineKeyboardButton("جيش", callback_data="army")],
            [InlineKeyboardButton("رجوع", callback_data="back")]
        ]))
    elif d == "army":
        user["xp"] += 30
        save(db)
        await q.edit_message_text("دخلت الجيش", reply_markup=BACK())
    elif d == "travel":
        await q.edit_message_text("سفر", reply_markup=KB([
            [InlineKeyboardButton("مصر 1000", callback_data="travel_eg"), InlineKeyboardButton("دبي 5000", callback_data="travel_dubai")],
            [InlineKeyboardButton("جواز سفر 2000", callback_data="passport"), InlineKeyboardButton("رجوع", callback_data="back")]
        ]))
    elif d.startswith("travel_"):
        c = 1000 if d == "travel_eg" else 5000
        if user["cash"] >= c:
            user["cash"] -= c
            user["happy"] += 30
            save(db)
            await q.edit_message_text("سافرت", reply_markup=BACK())
        else:
            await q.edit_message_text("معكش فلوس", reply_markup=BACK())
    elif d == "passport":
        if user["cash"] >= 2000:
            user["cash"] -= 2000
            user["passport"] = True
            save(db)
            await q.edit_message_text("طلعت جواز سفر", reply_markup=BACK())
        else:
            await q.edit_message_text("محتاج 2000", reply_markup=BACK())
    elif d == "stock":
        ch = random.randint(-3000, 6000)
        user["cash"] += ch
        save(db)
        await q.edit_message_text(f"بورصة {ch}", reply_markup=BACK())
    elif d == "gift_menu":
        await q.edit_message_text("هدايا", reply_markup=KB([
            [InlineKeyboardButton("خد هدية", callback_data="get_gift"), InlineKeyboardButton("كوبون", callback_data="coupon")],
            [InlineKeyboardButton("رجوع", callback_data="back")]
        ]))
    elif d == "get_gift":
        g = random.randint(500, 2000)
        user["cash"] += g
        save(db)
        await q.edit_message_text(f"هدية {g}", reply_markup=BACK())
    elif d == "coupon":
        user["cash"] += 1000
        save(db)
        await q.edit_message_text("كوبون 1000", reply_markup=BACK())
    elif d == "vip":
        if user["cash"] >= 50000:
            user["cash"] -= 50000
            user["vip"] = True
            save(db)
            await q.edit_message_text("بقيت VIP", reply_markup=BACK())
        else:
            await q.edit_message_text("VIP محتاج 50000", reply_markup=BACK())
    elif d == "support":
        await q.edit_message_text("خدمة عملاء\nالدعم @cat_max_10 @MOON_104\nالاونر @TRAN_5", reply_markup=KB([
            [InlineKeyboardButton("اطلب دعم", callback_data="ask_support")],
            [InlineKeyboardButton("رجوع", callback_data="back")]
        ]))
    elif d == "ask_support":
        tid = str(random.randint(1000, 9999))
        db["tickets"][tid] = {"user": uid, "status": "open", "support": None}
        save(db)
        await q.edit_message_text(f"تذكرتك #{tid} اتبعتت", reply_markup=BACK())
    elif d.startswith("accept_"):
        tid = d.split("_")[1]
        t = db["tickets"].get(tid)
        if t and t["status"] == "open":
            t["status"] = "taken"
            t["support"] = uid
            save(db)
            await q.edit_message_text(f"قبلت التذكرة #{tid}", reply_markup=BACK())
        else:
            await q.edit_message_text("اتاخدت خلاص", reply_markup=BACK())
    else:
        await q.edit_message_text("جاية قريب", reply_markup=BACK())

def main():
    threading.Thread(target=run_flask, daemon=True).start()
    threading.Thread(target=self_ping, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    print("TRAN BOT شغال")
    app.run_polling()

if __name__ == "__main__":
    main()
