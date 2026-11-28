# -*- coding: utf-8 -*-
# 👑 مملكة الملك - الكود النهائي الضخم - كل الازرار شغالة
# الملك: 8188263997 | العملة: ريال ﷼ | الشعب: 1,000,000

import random, time, threading, json, os, traceback
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.environ.get("BOT_TOKEN") or "حط_التوكن_بتاعك_هنا"
bot = telebot.TeleBot(TOKEN, parse_mode=None)

KING_ID = 8188263997

DB_FILE = "kingdom.json"
if os.path.exists(DB_FILE):
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            DB = json.load(f)
    except:
        DB = None
else:
    DB = None

if not DB:
    DB = {
        "treasury": 999999999999999,
        "population": 1000000,
        "births_today": 0, "deaths_today": 0, "marriages_today": 0,
        "oil_price": 80, "inflation": 0,
        "king_balance": 1000000000,
        "king_crown_level": 1,
        "king_throne": "🪑 عرش خشب",
        "king_palace": [],
        "regions": {"الرياض": 350000, "جدة": 200000, "مكة": 150000, "المدينة": 100000, "الدمام": 120000, "القصيم": 50000, "أبها": 30000},
        "users": {}, "banned": [], "jailed": [],
        "news": [], "zombie_count": 0, "moon_colony": 0,
        "market": {"gold": 250, "oil": 80, "bitcoin": 90000},
        "lottery_pot": 10000000,
    }

def save():
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(DB, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Save error: {e}")

def get_user(uid, name="مواطن"):
    uid = str(uid)
    if uid not in DB["users"]:
        DB["users"][uid] = {
            "name": name, "balance": 100000, "role": "مواطن",
            "region": random.choice(list(DB["regions"].keys())),
            "house": "🏠 بيت", "car": "🚗 كامري", "wife": "لا",
            "kids": 0, "job": random.choice(["تاجر","عسكري","عامل نفط","شيخ","مواطن","صياد","مزارع"]),
            "level": 1, "hasanat": 0, "is_king": False,
            "last_daily": 0, "title": "مواطن", "xp": 0,
            "gold": 0, "oil": 0, "bitcoin": 0, "horse": "لا",
            "energy": 100, "health": 100, "hunger": 0,
            "married_to": None, "crimes": 0, "jail_until": 0,
            "last_work": 0, "last_steal": 0, "last_rob": 0,
            "last_fish": 0, "last_hunt": 0,
        }
        save()
    # لو ناقصه حاجة قديمة زودها
    for k,v in [("gold",0),("oil",0),("bitcoin",0),("xp",0),("energy",100),("health",100),("married_to",None),("crimes",0),("last_work",0),("last_steal",0)]:
        if k not in DB["users"][uid]:
            DB["users"][uid][k]=v
    return DB["users"][uid]

def is_king(uid):
    return str(uid) == str(KING_ID) or DB["users"].get(str(uid), {}).get("is_king", False)

def fmt(n):
    try: return f"{int(n):,} ﷼"
    except: return f"{n} ﷼"

def pop_text():
    regions = "\n".join([f"{'🏰' if k=='الرياض' else '🌊' if k=='جدة' else '🕌' if k in ['مكة','المدينة'] else '🛢️' if k=='الدمام' else '🌴' if k=='القصيم' else '🏔️'} {k}: {v:,}" for k,v in DB["regions"].items()])
    return f"👥 سكان المملكة: {DB['population']:,}\n{regions}\n👶 اتولدوا: +{DB['births_today']} | 💀 ماتوا: -{DB['deaths_today']} | 💍 اتجوزوا: {DB['marriages_today']}\n💰 الخزينة: {fmt(DB['treasury'])}\n🛢️ النفط: {DB['oil_price']} ﷼ | 📈 التضخم: {DB['inflation']}%\n🕒 اخر تحديث: {time.strftime('%H:%M:%S')}"

# ===== دالة سحرية - دي اللي كانت ناقصة وبتخلي الازرار تشتغل =====
def safe_edit(c, text, kb=None):
    try:
        bot.edit_message_text(text, c.message.chat.id, c.message.message_id, reply_markup=kb)
    except Exception as e:
        # لو التعديل فشل (نفس الرسالة او غلطة) ابعت رسالة جديدة
        try:
            bot.send_message(c.message.chat.id, text, reply_markup=kb)
        except Exception as e2:
            print(f"safe_edit fail: {e} / {e2}")

def safe_answer(c, text):
    try:
        bot.answer_callback_query(c.id, text, show_alert=False)
    except:
        try: bot.send_message(c.message.chat.id, text)
        except: pass

def main_kb(uid):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🏰 المملكة", callback_data="kingdom"),
        InlineKeyboardButton("👥 كل الرعايا - 1M", callback_data="people"),
        InlineKeyboardButton("💰 محفظتي", callback_data="wallet"),
        InlineKeyboardButton("🏦 البنك المركزي", callback_data="bank"),
        InlineKeyboardButton("🛒 المتجر الملكي", callback_data="shop"),
        InlineKeyboardButton("🎰 الكازينو", callback_data="casino"),
        InlineKeyboardButton("⚔️ الحرب", callback_data="war"),
        InlineKeyboardButton("🕌 الحج والعمرة", callback_data="hajj"),
        InlineKeyboardButton("🏰 قصر الملك", callback_data="palace"),
        InlineKeyboardButton("📊 عداد الشعب LIVE", callback_data="live"),
        InlineKeyboardButton("📰 جريدة المملكة", callback_data="news"),
        InlineKeyboardButton("🎁 هدية يومية", callback_data="daily"),
        InlineKeyboardButton("💼 شغل", callback_data="work"),
        InlineKeyboardButton("🦈 سرقة", callback_data="steal_menu"),
        InlineKeyboardButton("💍 جواز", callback_data="marry_menu"),
        InlineKeyboardButton("🎣 صيد", callback_data="fish"),
        InlineKeyboardButton("🏇 سباق", callback_data="games"),
        InlineKeyboardButton("📈 البورصة", callback_data="stock"),
        InlineKeyboardButton("🏆 ترتيب الاغنياء", callback_data="rich"),
    )
    if is_king(uid):
        kb.add(
            InlineKeyboardButton("👑 لوحة الملك", callback_data="king_panel"),
            InlineKeyboardButton("🔥 تحكم جماعي", callback_data="mass"),
            InlineKeyboardButton("📜 مرسوم ملكي", callback_data="decree"),
            InlineKeyboardButton("🖨️ اطبع ريال", callback_data="print_money"),
            InlineKeyboardButton("🚁 ارمي فلوس من الطيارة", callback_data="rain_money"),
            InlineKeyboardButton("💣 امسح منطقة", callback_data="wipe"),
            InlineKeyboardButton("🚨 انقلاب / طوارئ", callback_data="emergency"),
            InlineKeyboardButton("🎁 وزع على الكل 100K", callback_data="king_give_all"),
        )
    kb.add(
        InlineKeyboardButton("🌙 رمضان / العيد", callback_data="ramadan"),
        InlineKeyboardButton("🚀 الفضاء", callback_data="space"),
        InlineKeyboardButton("🧟 زومبي", callback_data="zombie"),
        InlineKeyboardButton("🐉 تنين", callback_data="dragon"),
        InlineKeyboardButton("🏴‍☠️ قراصنة وكنز", callback_data="pirate"),
        InlineKeyboardButton("🧙 سحر", callback_data="magic"),
        InlineKeyboardButton("💧 حنفية الفلوس", callback_data="tap"),
        InlineKeyboardButton("🌧️ مطر فلوس", callback_data="rain_event"),
        InlineKeyboardButton("🌳 شجرة الفلوس", callback_data="tree"),
        InlineKeyboardButton("🪙 اكسر ذهب من الشارع", callback_data="gold_street"),
        InlineKeyboardButton("🔄 حدث العداد", callback_data="refresh"),
        InlineKeyboardButton("🏠 القايمة الرئيسية", callback_data="back"),
    )
    return kb

def back_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🔙 رجوع للقايمة", callback_data="back"))
    kb.add(InlineKeyboardButton("🏠 القايمة الرئيسية", callback_data="back"))
    return kb

def population_loop():
    while True:
        time.sleep(10)
        try:
            births = random.randint(5, 15)
            deaths = random.randint(2, 5)
            region = random.choice(list(DB["regions"].keys()))
            DB["regions"][region] += births - deaths
            DB["population"] += births - deaths
            DB["births_today"] += births
            DB["deaths_today"] += deaths
            if random.random() < 0.3:
                DB["marriages_today"] += random.randint(1, 10)
            oil_income = random.randint(5000, 15000)
            DB["treasury"] += oil_income + random.randint(1000, 5000)
            DB["market"]["gold"] = max(100, DB["market"]["gold"] + random.randint(-5, 5))
            DB["market"]["bitcoin"] = max(1000, DB["market"]["bitcoin"] + random.randint(-1000, 1000))
            if random.random() < 0.1:
                DB["zombie_count"] += random.randint(1, 5)
            DB["news"].append(random.choice([
                f"👶 اتولد {births} عيل جديد في {region}",
                f"💀 مات {deaths} مواطنين في {region}",
                f"💍 {random.randint(1,5)} جوازات جديدة في {region}",
                f"🛢️ النفط غلي - الخزينة زادت {oil_income:,} ﷼",
                f"🌧️ مطر فلوس في {region}!",
                f"📰 1000 مواطن في {region} اشتروا عربيات جديدة",
                f"⚔️ 200 عسكري جديد انضموا للجيش",
                f"🧟 {random.randint(1,10)} زومبي جديد ظهر في {region}",
                f"💰 تاجر في {region} كسب 1M ﷼",
            ]))
            DB["news"] = DB["news"][-20:]
            save()
        except Exception as e:
            print(f"pop loop: {e}")

threading.Thread(target=population_loop, daemon=True).start()

@bot.message_handler(commands=['start','help','menu'])
def start(m):
    try:
        u = get_user(m.from_user.id, m.from_user.first_name)
        if str(m.from_user.id) == str(KING_ID):
            u["is_king"] = True; u["role"] = "👑 الملك"; u["balance"] = max(u["balance"], 1000000000); save()
        bot.send_message(m.chat.id,
            f"👑🇸🇦 اهلا بيك في مملكة الملك - اغنى دولة في العالم!\n\n{pop_text()}\n\n💰 معاك: {fmt(u['balance'])}\n🎖️ رتبتك: {u['role']}\n🏰 منطقتك: {u['region']}\n⭐ مستواك: {u['level']} | XP: {u['xp']}\n\nدوس على اي زرار تحت 👇 كل الازرار شغالة!",
            reply_markup=main_kb(m.from_user.id))
    except Exception as e:
        print(f"start error: {e}")
        bot.send_message(m.chat.id, "اهلا بيك يا ملك 👑 دوس /start تاني")

@bot.message_handler(func=lambda m: True)
def any_msg(m):
    # لو كتب اي كلمة غير /start رجعه للقايمة
    try:
        txt = (m.text or "").lower()
        if "فلوس" in txt or "راتب" in txt:
            u = get_user(m.from_user.id, m.from_user.first_name)
            u["balance"] += 1000; save()
            bot.send_message(m.chat.id, "خدت 1000 ﷼ عشان طلبت فلوس 💰", reply_markup=main_kb(m.from_user.id))
        elif txt in ["هاي","hi","السلام عليكم","سلام"]:
            bot.send_message(m.chat.id, "هلا والله يا غني 👑💰", reply_markup=main_kb(m.from_user.id))
        else:
            bot.send_message(m.chat.id, "دوس على الازرار تحت 👇", reply_markup=main_kb(m.from_user.id))
    except: pass

@bot.callback_query_handler(func=lambda c: True)
def callbacks(c):
    uid = c.from_user.id
    try:
        u = get_user(uid, c.from_user.first_name)
        d = c.data or ""
        print(f"CALLBACK: {uid} -> {d}")
        # رد فوري عشان الزرار ميعلقش
        try: bot.answer_callback_query(c.id)
        except: pass

        # ===== القايمة =====
        if d == "back":
            safe_edit(c, f"👑 مملكة الملك\n\n{pop_text()}\n\nدوس على اي زرار 👇", main_kb(uid)); return
        if d == "refresh":
            safe_edit(c, f"🔄 العداد اتحدث!\n\n{pop_text()}", main_kb(uid)); return
        if d == "treasury":
            safe_edit(c, f"💰 الخزينة\n\n{fmt(DB['treasury'])}\nبتزيد كل 10 ثواني 💰", back_kb()); return
        if d == "kingdom":
            kb = InlineKeyboardMarkup(); kb.add(InlineKeyboardButton("👥 عداد الشعب", callback_data="people"), InlineKeyboardButton("💰 الخزينة", callback_data="treasury"), InlineKeyboardButton("🔙 رجوع", callback_data="back"))
            safe_edit(c, f"🏰 المملكة - اغنى دولة في العالم\n\n{pop_text()}\n\n👑 الملك: اغنى ملك\n🏰 القصر: {', '.join(DB['king_palace']) or 'قصر ملكي'}\n👑 التاج: مستوى {DB['king_crown_level']}\n🪑 العرش: {DB['king_throne']}\n🌧️ مطر فلوس كل اسبوع - الشوارع ذهب", kb); return
        if d == "people":
            kb = InlineKeyboardMarkup(row_width=2)
            kb.add(InlineKeyboardButton("🏰 الرياض", callback_data="reg_الرياض"), InlineKeyboardButton("🌊 جدة", callback_data="reg_جدة"), InlineKeyboardButton("🕌 مكة", callback_data="reg_مكة"), InlineKeyboardButton("🛢️ الدمام", callback_data="reg_الدمام"), InlineKeyboardButton("💰 الاغنى 100", callback_data="rich"), InlineKeyboardButton("📊 جراف الشعب", callback_data="graph"), InlineKeyboardButton("📺 بث مباشر", callback_data="live"), InlineKeyboardButton("🔙 رجوع", callback_data="back"))
            safe_edit(c, f"👥 كل الرعايا - 1,000,000\n\n{pop_text()}", kb); return
        if d.startswith("reg_"):
            r = d.replace("reg_","")
            safe_edit(c, f"🏰 {r}\n\n👥 السكان: {DB['regions'].get(r,0):,}\n💰 دخل المنطقة: {DB['regions'].get(r,0)*2:,} ﷼", back_kb()); return
        if d == "rich":
            # ترتيب حقيقي من المستخدمين
            users = sorted(DB["users"].values(), key=lambda x: x.get("balance",0), reverse=True)[:10]
            txt = "🏆 ترتيب الاغنياء:\n\n"
            for i, x in enumerate(users, 1):
                txt += f"{i}. {x.get('name','مواطن')} - {fmt(x.get('balance',0))}\n"
            if not users: txt += "لسه مفيش حد، انت اول واحد!"
            txt += f"\n💰 الخزينة: {fmt(DB['treasury'])}"
            safe_edit(c, txt, back_kb()); return
        if d == "live":
            live = "\n".join(DB["news"][-8:]) or "لا اخبار"
            kb = InlineKeyboardMarkup(); kb.add(InlineKeyboardButton("🔄 حدث", callback_data="live"), InlineKeyboardButton("🔙 رجوع", callback_data="back"))
            safe_edit(c, f"📺 بث مباشر\n\n{pop_text()}\n\n📺 اخر احداث:\n{live}", kb); return
        if d == "graph":
            safe_edit(c, f"📊 جراف الشعب\n\n1M ┤        ╱╲\n   │      ╱  ╲\n   │    ╱    ╲\n   │  ╱      ╲\n999k┤╱        ╲___\n   └──────────────\n🏆 اعلى: {DB['population']+5000:,} | 👥 الحالي: {DB['population']:,}", back_kb()); return

        # ===== محفظة / شغل / سرقة / جواز =====
        if d == "wallet":
            kb = InlineKeyboardMarkup(); kb.add(InlineKeyboardButton("💰 خد راتبك 5000 ﷼", callback_data="salary"), InlineKeyboardButton("🎁 هدية يومية", callback_data="daily"), InlineKeyboardButton("💼 اشتغل", callback_data="work"), InlineKeyboardButton("🔙 رجوع", callback_data="back"))
            safe_edit(c, f"💰 محفظتك\n\n👤 {u['name']}\n💰 معاك: {fmt(u['balance'])}\n🎖️ رتبتك: {u['role']} - {u['title']}\n🏰 منطقتك: {u['region']}\n🏠 بيتك: {u['house']}\n🚗 عربيتك: {u['car']}\n💍 مراتك: {u['wife']} | 👶 عيالك: {u['kids']}\n💼 شغلك: {u['job']}\n⭐ حسناتك: {u['hasanat']} | XP: {u['xp']}\n🥇 ذهب: {u['gold']} | 🛢️ نفط: {u['oil']} | ₿ بيتكوين: {u['bitcoin']}\n❤️ صحتك: {u['health']} | ⚡ طاقتك: {u['energy']}", kb); return
        if d == "salary":
            u["balance"] += 5000; u["xp"] += 10; save(); safe_answer(c, "خدت 5000 ﷼ راتب 💰"); safe_edit(c, f"💰 خدت راتبك 5000 ﷼!\n\nمعاك دلوقتي: {fmt(u['balance'])}", main_kb(uid)); return
        if d == "daily":
            now = time.time()
            if now - u["last_daily"] < 86400:
                safe_answer(c, "خدت هديتك النهاردة، تعالا بكرا 🎁"); return
            gift = random.choice([10000, 5000, 20000, 1000, 50000, 100000])
            u["balance"] += gift; u["last_daily"] = now; u["xp"] += 20; save()
            safe_edit(c, f"🎁 هدية يومية! كسبت {fmt(gift)} من الملك الغني 👑\n\nمعاك: {fmt(u['balance'])}", main_kb(uid)); return
        if d == "work":
            now = time.time()
            if now - u.get("last_work",0) < 60:
                safe_answer(c, "استنى دقيقة واشتغل تاني 💼"); return
            jobs = {"تاجر": (3000,8000), "عسكري": (2000,5000), "عامل نفط": (5000,12000), "شيخ": (1000,3000), "مواطن": (500,2000), "صياد": (1000,4000), "مزارع": (1000,3500)}
            lo, hi = jobs.get(u["job"], (500,3000))
            gain = random.randint(lo, hi)
            u["balance"] += gain; u["xp"] += 15; u["last_work"] = now; u["energy"] = max(0, u["energy"]-5); save()
            safe_edit(c, f"💼 اشتغلت كـ {u['job']} وكسبت {fmt(gain)}!\n\nمعاك: {fmt(u['balance'])} | ⚡ طاقتك: {u['energy']}", main_kb(uid)); return
        if d == "steal_menu":
            kb = InlineKeyboardMarkup(row_width=2)
            kb.add(InlineKeyboardButton("🦈 اسرق واحد عشوائي", callback_data="steal"), InlineKeyboardButton("🏦 اسرق البنك", callback_data="rob_bank"), InlineKeyboardButton("🏠 اسرق بيت", callback_data="rob_house"), InlineKeyboardButton("🔙 رجوع", callback_data="back"))
            safe_edit(c, f"🦈 السرقة\n\n💰 معاك: {fmt(u['balance'])}\nخلي بالك لو اتمسكت هتتسجن!", kb); return
        if d == "steal":
            now = time.time()
            if now - u.get("last_steal",0) < 30:
                safe_answer(c, "استنى 30 ثانية قبل ما تسرق تاني 🦈"); return
            u["last_steal"] = now
            if random.random() < 0.5:
                gain = random.randint(1000, 10000); u["balance"] += gain; u["crimes"] += 1; save()
                safe_edit(c, f"🦈 سرقت {fmt(gain)} ومحدش شافك! 😂\n\nمعاك: {fmt(u['balance'])}", main_kb(uid))
            else:
                fine = random.randint(500, 2000); u["balance"] = max(0, u["balance"]-fine); u["crimes"] += 1; save()
                safe_edit(c, f"🚨 اتمسكت! دفعت غرامة {fmt(fine)}\n\nمعاك: {fmt(u['balance'])}", main_kb(uid))
            return
        if d == "rob_bank":
            if random.random() < 0.3:
                gain = random.randint(50000, 200000); u["balance"] += gain; save()
                safe_edit(c, f"🏦 سرقت البنك! كسبت {fmt(gain)}! 🎉🎉\n\nمعاك: {fmt(u['balance'])}", main_kb(uid))
            else:
                safe_edit(c, "🚨 البنك مسكك! خسرت 5000 ﷼ غرامة", main_kb(uid)); u["balance"] = max(0, u["balance"]-5000); save()
            return
        if d == "rob_house":
            gain = random.randint(500, 5000); u["balance"] += gain; save()
            safe_edit(c, f"🏠 سرقت بيت وكسبت {fmt(gain)}!", main_kb(uid)); return
        if d == "marry_menu":
            kb = InlineKeyboardMarkup(row_width=2)
            kb.add(InlineKeyboardButton("💍 اتجوز - 10,000 ﷼", callback_data="marry"), InlineKeyboardButton("👶 خلف عيل - 5000 ﷼", callback_data="have_kid"), InlineKeyboardButton("💔 طلق", callback_data="divorce"), InlineKeyboardButton("🔙 رجوع", callback_data="back"))
            safe_edit(c, f"💍 الجواز\n\n💍 مراتك: {u['wife']}\n👶 عيالك: {u['kids']}\n💰 معاك: {fmt(u['balance'])}", kb); return
        if d == "marry":
            if u["wife"] != "لا":
                safe_answer(c, "انت متجوز اصلا! 💍"); return
            if u["balance"] < 10000:
                safe_answer(c, "لازم 10000 ﷼ عشان تتجوز"); return
            names = ["نورة","ريم","سارة","منيرة","حصة","لطيفة","الجوهرة","فاطمة"]
            u["balance"] -= 10000; u["wife"] = random.choice(names); u["kids"] = 0; DB["marriages_today"] += 1; save()
            safe_edit(c, f"💍 اتجوزت {u['wife']}! مبروك 🎉🎉\n\nمعاك: {fmt(u['balance'])}", main_kb(uid)); return
        if d == "have_kid":
            if u["wife"] == "لا":
                safe_answer(c, "اتجوز الاول! 💍"); return
            u["kids"] += 1; u["balance"] += 2000; save()
            safe_edit(c, f"👶 جالك عيل جديد! بقى عندك {u['kids']} عيال 🎉\n\nالدولة ادتك 2000 ﷼ هدية", main_kb(uid)); return
        if d == "divorce":
            if u["wife"] == "لا":
                safe_answer(c, "انت مش متجوز اصلا"); return
            u["wife"] = "لا"; u["kids"] = 0; save()
            safe_edit(c, "💔 طلقت.. رجعت عازب 😂", main_kb(uid)); return
        if d == "fish":
            gain = random.randint(500, 5000); u["balance"] += gain; save()
            safe_edit(c, f"🎣 اصطدت سمكة وبعتها بـ {fmt(gain)}!\n\nمعاك: {fmt(u['balance'])}", main_kb(uid)); return

        # ===== فلوس مجانية =====
        if d == "tap":
            gain = random.randint(50, 200); u["balance"] += gain; save(); safe_answer(c, f"فتحت الحنفية ونزل {gain} ﷼! 💧💰"); safe_edit(c, f"💧 الحنفية نزلت {gain} ﷼!\n\nمعاك: {fmt(u['balance'])}", main_kb(uid)); return
        if d == "rain_event":
            gain = random.randint(1000, 5000); u["balance"] += gain; save(); safe_edit(c, f"🌧️ مطر فلوس! جمعت {fmt(gain)}\n\nمعاك: {fmt(u['balance'])}", main_kb(uid)); return
        if d == "tree":
            gain = random.randint(1000, 2000); u["balance"] += gain; save(); safe_edit(c, f"🌳 قطفت من شجرة الفلوس {fmt(gain)}\n\nمعاك: {fmt(u['balance'])}", main_kb(uid)); return
        if d == "gold_street":
            gain = random.randint(500, 2000); u["balance"] += gain; u["gold"] += 1; save(); safe_edit(c, f"🪙 كسرت حتة ذهب من الشارع! كسبت {fmt(gain)} + 1 ذهب\n\nمعاك: {fmt(u['balance'])}", main_kb(uid)); return

        # ===== بنك =====
        if d == "bank":
            kb = InlineKeyboardMarkup(row_width=2)
            kb.add(InlineKeyboardButton("💰 حط 10,000 وخد 20,000", callback_data="bank_put"), InlineKeyboardButton("🏦 خد قرض 10M ببلاش", callback_data="bank_loan"), InlineKeyboardButton("💱 حول دولار لريال", callback_data="bank_exchange"), InlineKeyboardButton("🥇 اشتري ذهب", callback_data="buy_gold"), InlineKeyboardButton("🔙 رجوع", callback_data="back"))
            safe_edit(c, f"🏦 البنك المركزي السعودي\n\n💰 فلوسك: {fmt(u['balance'])}\n📈 الفايدة: 100%\n💰 الخزينة: {fmt(DB['treasury'])}\n🥇 سعر الذهب: {DB['market']['gold']} ﷼", kb); return
        if d == "bank_put":
            if u["balance"] >= 10000: u["balance"] += 10000; save(); safe_answer(c, "حطيت 10000 وخدت 20000! 💰")
            else: safe_answer(c, "معاكش 10000 ﷼")
            return
        if d == "bank_loan": u["balance"] += 10000000; save(); safe_answer(c, "خدت قرض 10M ببلاش! 🎉"); return
        if d == "bank_exchange": u["balance"] += 375; save(); safe_answer(c, "100 دولار = 375 ﷼ 💱"); return
        if d == "buy_gold":
            if u["balance"] >= DB["market"]["gold"]: u["balance"] -= DB["market"]["gold"]; u["gold"] += 1; save(); safe_answer(c, "اشتريت 1 ذهب 🥇")
            else: safe_answer(c, "معاكش فلوس للذهب")
            return

        # ===== بورصة =====
        if d == "stock":
            kb = InlineKeyboardMarkup(row_width=2)
            kb.add(InlineKeyboardButton("🥇 اشتري ذهب", callback_data="buy_gold"), InlineKeyboardButton("₿ اشتري بيتكوين", callback_data="buy_btc"), InlineKeyboardButton("🛢️ اشتري نفط", callback_data="buy_oil"), InlineKeyboardButton("💰 بيع الكل", callback_data="sell_all"), InlineKeyboardButton("🔙 رجوع", callback_data="back"))
            safe_edit(c, f"📈 البورصة\n\n🥇 الذهب: {DB['market']['gold']} ﷼ - معاك: {u['gold']}\n🛢️ النفط: {DB['market']['oil']} ﷼ - معاك: {u['oil']}\n₿ بيتكوين: {DB['market']['bitcoin']} ﷼ - معاك: {u['bitcoin']}\n💰 فلوسك: {fmt(u['balance'])}", kb); return
        if d == "buy_btc":
            if u["balance"] >= 1000: u["balance"] -= 1000; u["bitcoin"] += 1; save(); safe_answer(c, "اشتريت بيتكوين ₿")
            else: safe_answer(c, "معاكش فلوس")
            return
        if d == "buy_oil":
            if u["balance"] >= DB["market"]["oil"]: u["balance"] -= DB["market"]["oil"]; u["oil"] += 1; save(); safe_answer(c, "اشتريت نفط 🛢️")
            else: safe_answer(c, "معاكش فلوس")
            return
        if d == "sell_all":
            gain = u["gold"]*DB["market"]["gold"] + u["oil"]*DB["market"]["oil"] + u["bitcoin"]*1000
            u["balance"] += gain; u["gold"]=0; u["oil"]=0; u["bitcoin"]=0; save()
            safe_edit(c, f"💰 بعت كل حاجة وكسبت {fmt(gain)}!\n\nمعاك: {fmt(u['balance'])}", main_kb(uid)); return

        # ===== متجر =====
        if d == "shop":
            kb = InlineKeyboardMarkup(row_width=2)
            for txt, cb in [("🚗 لامبورجيني - 5M", "buy_lambo"),("🚗 رولز رويس - 10M","buy_rolls"),("🚗 بوغاتي - 50M","buy_bugatti"),("🏠 فيلا - 10M","buy_villa"),("🏰 قصر - 100M","buy_palace"),("🏝️ جزيرة - 500M","buy_island"),("⌚ رولكس - 1M","buy_rolex"),("💎 تاج الماس - 10M","buy_crown"),("🚁 طيارة - 100M","buy_plane"),("🌙 بيت على القمر - 1B","buy_moon"),("🐎 حصان عربي - 500K","buy_horse"),("🦅 صقر - 200K","buy_falcon")]:
                kb.add(InlineKeyboardButton(txt, callback_data=cb))
            kb.add(InlineKeyboardButton("🔙 رجوع", callback_data="back"))
            safe_edit(c, f"🛒 المتجر الملكي\n\n💰 معاك: {fmt(u['balance'])}\nكل حاجة للاغنياء بس 👑", kb); return
        if d.startswith("buy_"):
            prices = {"buy_lambo":5000000,"buy_rolls":10000000,"buy_bugatti":50000000,"buy_villa":10000000,"buy_palace":100000000,"buy_island":500000000,"buy_rolex":1000000,"buy_crown":10000000,"buy_plane":100000000,"buy_moon":1000000000,"buy_horse":500000,"buy_falcon":200000}
            names = {"buy_lambo":"🚗 لامبورجيني","buy_rolls":"🚗 رولز رويس","buy_bugatti":"🚗 بوغاتي","buy_villa":"🏠 فيلا","buy_palace":"🏰 قصر","buy_island":"🏝️ جزيرة","buy_rolex":"⌚ رولكس","buy_crown":"💎 تاج الماس","buy_plane":"🚁 طيارة","buy_moon":"🌙 بيت على القمر","buy_horse":"🐎 حصان عربي","buy_falcon":"🦅 صقر"}
            p = prices.get(d, 0)
            if u["balance"] >= p:
                u["balance"] -= p; DB["treasury"] += p
                if d in ["buy_villa","buy_palace","buy_island","buy_moon"]: u["house"] = names[d]
                elif d == "buy_horse": u["horse"] = "🐎 حصان عربي"
                else: u["car"] = names[d]
                save(); safe_answer(c, f"اشتريت {names[d]}! 🎉"); safe_edit(c, f"🎉 اشتريت {names[d]}!\n\nمعاك: {fmt(u['balance'])}", main_kb(uid))
            else: safe_answer(c, "معاكش فلوس كفاية، خد قرض من البنك 😂")
            return

        # ===== كازينو =====
        if d == "casino":
            kb = InlineKeyboardMarkup(row_width=2)
            kb.add(InlineKeyboardButton("🎰 العب - رهان 1M", callback_data="casino_play"), InlineKeyboardButton("🎰 يانصيب - 100M", callback_data="lottery"), InlineKeyboardButton("🎲 راهن ⬆️", callback_data="bet_up"), InlineKeyboardButton("🎲 راهن ⬇️", callback_data="bet_down"), InlineKeyboardButton("🎰 عجلة المليار", callback_data="wheel_billion"), InlineKeyboardButton("🔙 رجوع", callback_data="back"))
            safe_edit(c, f"🎰 كازينو المليونيرات\n\n💰 معاك: {fmt(u['balance'])}\n🏆 جايزة اليانصيب: {fmt(DB['lottery_pot'])}", kb); return
        if d == "casino_play":
            if u["balance"] < 1000000: safe_answer(c, "لازم يبقى معاك 1M عشان تلعب"); return
            if random.random() < 0.45: u["balance"] += 10000000; save(); safe_edit(c, f"🎉 كسبت 10M ﷼!\n\nمعاك: {fmt(u['balance'])}", main_kb(uid))
            else: u["balance"] += 1000000; save(); safe_edit(c, f"خسرت 1M بس خدت 2M هدية 😂\n\nمعاك: {fmt(u['balance'])}", main_kb(uid))
            return
        if d == "lottery":
            if random.random() < 0.2: u["balance"] += 100000000; save(); safe_edit(c, f"🎉 كسبت اليانصيب 100M!\n\nمعاك: {fmt(u['balance'])}", main_kb(uid))
            else: safe_answer(c, "ماكسبتش، حاول تاني")
            return
        if d == "wheel_billion":
            if random.random() < 0.1: u["balance"] += 1000000000; save(); safe_edit(c, "🎉 كسبت عجلة المليار! 1B ﷼!", main_kb(uid))
            else: u["balance"] += 10000; save(); safe_answer(c, "كسبت 10000 ﷼ من العجلة 🎰")
            return
        if d in ["bet_up","bet_down"]:
            if random.random() < 0.5: u["balance"] += 2000; save(); safe_answer(c, "كسبت الرهان 2000 ﷼ 🎲")
            else: safe_answer(c, "خسرت الرهان")
            return

        # ===== حرب / حج / قصر / اخبار / العاب =====
        if d == "war":
            kb = InlineKeyboardMarkup(row_width=2)
            kb.add(InlineKeyboardButton("⚔️ اهجم على مملكة الظلام", callback_data="war_dark"), InlineKeyboardButton("⚔️ حرب الرياض ضد جدة", callback_data="war_regions"), InlineKeyboardButton("🕊️ صلح", callback_data="war_peace"), InlineKeyboardButton("🔙 رجوع", callback_data="back"))
            safe_edit(c, "⚔️ الحرب العالمية\n\n🏰 مملكتك: 1M - جيش 200k\n🏴 مملكة الظلام: 500k\n🏳️ مملكة النور: 300k", kb); return
        if d == "war_dark":
            if random.random() < 0.6: u["balance"] += 50000; DB["treasury"] += 1000000; DB["king_crown_level"] += 1; save(); safe_edit(c, f"🎉 كسبنا الحرب! +50000 ﷼\n\nمعاك: {fmt(u['balance'])}", main_kb(uid))
            else: safe_answer(c, "خسرنا الحرب، حاول تاني")
            return
        if d == "war_regions": safe_answer(c, "الرياض كسبت جدة! ⚔️"); return
        if d == "war_peace": u["balance"] += 10000; save(); safe_answer(c, "عملت صلح وكسبت 10000 ﷼ 🕊️"); return

        if d == "hajj":
            kb = InlineKeyboardMarkup(); kb.add(InlineKeyboardButton("🕋 اعمل حج", callback_data="do_hajj"), InlineKeyboardButton("🕌 اعمل عمرة", callback_data="do_umrah"), InlineKeyboardButton("🔙 رجوع", callback_data="back"))
            safe_edit(c, f"🕋 الحج والعمرة\n\n⭐ حسناتك: {u['hasanat']}\n🕋 الحج: 100k بيحجوا كل سنة", kb); return
        if d in ["do_hajj","do_umrah"]: u["hasanat"] += 1000; u["balance"] += 5000; save(); safe_edit(c, f"🕋 تقبل الله! +1000 حسنة و +5000 ﷼\n\nمعاك: {fmt(u['balance'])}", main_kb(uid)); return

        if d == "palace":
            kb = InlineKeyboardMarkup(row_width=2)
            kb.add(InlineKeyboardButton("🛏️ اوضة نوم", callback_data="palace_room"), InlineKeyboardButton("🏊 حمام سباحة", callback_data="palace_pool"), InlineKeyboardButton("🎮 اوضة العاب", callback_data="palace_game"), InlineKeyboardButton("🚁 مهبط طيارات", callback_data="palace_heli"), InlineKeyboardButton("💎 خزنة سرية", callback_data="palace_vault"), InlineKeyboardButton("🦁 حديقة حيوان", callback_data="palace_zoo"), InlineKeyboardButton("🔙 رجوع", callback_data="back"))
            safe_edit(c, f"🏰 قصر الملك\n\nاوض القصر: {', '.join(DB['king_palace']) or 'لسه فاضي'}\n💰 معاك: {fmt(u['balance'])}", kb); return
        if d.startswith("palace_"):
            names = {"palace_room":"🛏️ اوضة نوم","palace_pool":"🏊 حمام سباحة","palace_game":"🎮 اوضة العاب","palace_heli":"🚁 مهبط طيارات","palace_vault":"💎 خزنة سرية","palace_zoo":"🦁 حديقة حيوان"}
            if names[d] not in DB["king_palace"]: DB["king_palace"].append(names[d]); save()
            safe_answer(c, f"اشتريت {names[d]} للقصر! 🎉"); return

        if d == "news":
            news = "\n".join(DB["news"][-10:]) or "لا اخبار"
            safe_edit(c, f"📰 جريدة المملكة\n\n{news}\n\n{pop_text()}", back_kb()); return

        if d == "games":
            kb = InlineKeyboardMarkup(row_width=2)
            kb.add(InlineKeyboardButton("🏇 سباق خيول", callback_data="game_horse"), InlineKeyboardButton("🎰 عجلة الحظ", callback_data="game_wheel"), InlineKeyboardButton("💣 القنبلة", callback_data="game_bomb"), InlineKeyboardButton("🦅 صيد الصقور", callback_data="game_falcon"), InlineKeyboardButton("🎯 قنص", callback_data="game_snipe"), InlineKeyboardButton("⚽ دوري كورة", callback_data="game_soccer"), InlineKeyboardButton("🏇 سباق الهجن", callback_data="game_camel"), InlineKeyboardButton("🧩 لغز الملك", callback_data="game_puzzle"), InlineKeyboardButton("🔙 رجوع", callback_data="back"))
            safe_edit(c, "🎮 العاب المملكة\n\nكل لعبة تكسبك فلوس 👑", kb); return
        if d.startswith("game_"):
            win = random.randint(500, 10000); u["balance"] += win; save(); safe_edit(c, f"🎉 كسبت {fmt(win)} في اللعبة!\n\nمعاك: {fmt(u['balance'])}", main_kb(uid)); return

        if d == "ramadan":
            kb = InlineKeyboardMarkup(); kb.add(InlineKeyboardButton("🌙 خد فطار 5000 ﷼", callback_data="iftar"), InlineKeyboardButton("🎉 خد عيدية 50,000 ﷼", callback_data="eid"), InlineKeyboardButton("🔙 رجوع", callback_data="back"))
            safe_edit(c, "🌙 رمضان والعيد\n\nفي العيد: كل واحد ياخد 50,000 ﷼ عيدية", kb); return
        if d == "iftar": u["balance"] += 5000; save(); safe_edit(c, f"🌙 خدت فطار 5000 ﷼\n\nمعاك: {fmt(u['balance'])}", main_kb(uid)); return
        if d == "eid": u["balance"] += 50000; save(); safe_edit(c, f"🎉 خدت عيدية 50,000 ﷼\n\nمعاك: {fmt(u['balance'])}", main_kb(uid)); return

        if d == "space":
            kb = InlineKeyboardMarkup(); kb.add(InlineKeyboardButton("🚀 ابني صاروخ - 1M", callback_data="build_rocket"), InlineKeyboardButton("🌙 مستعمرة القمر", callback_data="moon"), InlineKeyboardButton("👽 اتكلم مع كائنات", callback_data="alien"), InlineKeyboardButton("🔙 رجوع", callback_data="back"))
            safe_edit(c, f"🚀 وكالة الفضاء السعودية\n\n🌙 مستعمرة القمر: {DB['moon_colony']} مواطن", kb); return
        if d == "build_rocket":
            if u["balance"] >= 1000000: u["balance"] -= 1000000; DB["moon_colony"] += 10000; save(); safe_edit(c, "🚀 اطلقت الصاروخ! 10k سافروا القمر 🌙", main_kb(uid))
            else: safe_answer(c, "لازم 1M عشان تبني صاروخ")
            return
        if d == "moon": u["balance"] += 10000; save(); safe_edit(c, f"🌙 سافرت القمر ورجعت بـ 10000 ﷼\n\nمعاك: {fmt(u['balance'])}", main_kb(uid)); return
        if d == "alien": u["balance"] += 1000000; save(); safe_edit(c, "👽 اتصاحبت على الكائنات وخدت 1M!", main_kb(uid)); return

        if d == "zombie":
            kb = InlineKeyboardMarkup(); kb.add(InlineKeyboardButton("🔫 اقتل زومبي", callback_data="kill_zombie"), InlineKeyboardButton("💉 اعمل علاج", callback_data="cure_zombie"), InlineKeyboardButton("🔙 رجوع", callback_data="back"))
            safe_edit(c, f"🧟 وباء الزومبي\n\n🧟 عدد الزومبي: {DB['zombie_count']}\n🔫 كل زومبي تقتله تاخد 1000 ﷼", kb); return
        if d == "kill_zombie": u["balance"] += 1000; DB["zombie_count"] = max(0, DB["zombie_count"]-1); save(); safe_answer(c, "قتلت زومبي! +1000 ﷼ 🔫🧟"); return
        if d == "cure_zombie": DB["zombie_count"] = 0; save(); safe_answer(c, "عالجت كل الزومبي! 💉"); return

        if d == "dragon":
            kb = InlineKeyboardMarkup(); kb.add(InlineKeyboardButton("🐉 اطلق التنين", callback_data="release_dragon"), InlineKeyboardButton("🥚 لاقي بيضة تنين", callback_data="dragon_egg"), InlineKeyboardButton("🔙 رجوع", callback_data="back"))
            safe_edit(c, "🐉 تنين المملكة\n\nالتنين بيحرق منطقة كاملة وتاخد فلوسهم 🔥", kb); return
        if d == "release_dragon": u["balance"] += 50000; save(); safe_edit(c, f"🐉 التنين حرق منطقة وخدت 50000 ﷼!\n\nمعاك: {fmt(u['balance'])}", main_kb(uid)); return
        if d == "dragon_egg": u["balance"] += 100000; save(); safe_edit(c, f"🥚 لقيت بيضة تنين! بعتها بـ 100k\n\nمعاك: {fmt(u['balance'])}", main_kb(uid)); return

        if d == "pirate":
            kb = InlineKeyboardMarkup(); kb.add(InlineKeyboardButton("🗺️ دور على الكنز", callback_data="treasure"), InlineKeyboardButton("⚔️ حارب القراصنة", callback_data="fight_pirate"), InlineKeyboardButton("🔙 رجوع", callback_data="back"))
            safe_edit(c, "🏴‍☠️ قراصنة وكنز\n\nالكنز فيه 1M ﷼", kb); return
        if d == "treasure":
            if random.random() < 0.3: u["balance"] += 1000000; save(); safe_edit(c, f"🗺️ لقيت الكنز! 1M ﷼!\n\nمعاك: {fmt(u['balance'])}", main_kb(uid))
            else: safe_answer(c, "مالقيتش الكنز، حاول تاني")
            return
        if d == "fight_pirate": u["balance"] += 10000; save(); safe_answer(c, "حاربت القراصنة وكسبت 10000 ﷼ ⚔️"); return

        if d == "magic":
            kb = InlineKeyboardMarkup(row_width=2)
            kb.add(InlineKeyboardButton("🧙 اعمل سحر", callback_data="magic_spell"), InlineKeyboardButton("🔮 اسأل الكورة", callback_data="magic_ball"), InlineKeyboardButton("❤️ جرعة حب", callback_data="magic_love"), InlineKeyboardButton("💰 جرعة فلوس", callback_data="magic_money"), InlineKeyboardButton("👻 جرعة اختفاء", callback_data="magic_ghost"), InlineKeyboardButton("🔙 رجوع", callback_data="back"))
            safe_edit(c, "🧙 سحر وشعوذة\n\nالسحر ممكن يكسبك 1M وممكن يخسرك 😂", kb); return
        if d == "magic_spell":
            if random.random() < 0.5: u["balance"] += 1000000; save(); safe_edit(c, f"🧙 السحر نجح! +1M ﷼\n\nمعاك: {fmt(u['balance'])}", main_kb(uid))
            else: u["balance"] = max(1000, u["balance"]//2); save(); safe_edit(c, "🧙 السحر فشل! خسرت نص فلوسك 😂", main_kb(uid))
            return
        if d == "magic_ball": safe_answer(c, random.choice(["ايوه بيحبك ❤️", "لا بيكرهك 😂", "الملك احسن ملك 👑"])); return
        if d in ["magic_love","magic_money","magic_ghost"]: u["balance"] += 5000; save(); safe_answer(c, "شربت الجرعة! +5000 ﷼ 🧪"); return

        # ===== الملك =====
        if d == "king_panel":
            if not is_king(uid): safe_answer(c, "انت مش الملك! 👑"); return
            kb = InlineKeyboardMarkup(row_width=2)
            kb.add(InlineKeyboardButton("💰 خد راتبك 100M", callback_data="king_salary"), InlineKeyboardButton("🎁 وزع 1 مليار", callback_data="king_give_billion"), InlineKeyboardButton("🎁 وزع على الكل 100K", callback_data="king_give_all"), InlineKeyboardButton("👥 شوف الشعب", callback_data="people"), InlineKeyboardButton("📊 تقرير الملك", callback_data="king_report"), InlineKeyboardButton("🎭 تنكر كمواطن", callback_data="king_disguise"), InlineKeyboardButton("🤪 وضع المجنون", callback_data="king_crazy"), InlineKeyboardButton("🔙 رجوع", callback_data="back"))
            safe_edit(c, f"👑 لوحة الملك\n\n{pop_text()}\n\n💰 ثروتك: {fmt(u['balance'])}", kb); return
        if d == "king_salary":
            if not is_king(uid): return
            u["balance"] += 100000000; save(); safe_edit(c, f"👑 خدت راتبك الملكي 100M ﷼!\n\nمعاك: {fmt(u['balance'])}", main_kb(uid)); return
        if d == "king_give_billion":
            if not is_king(uid): return
            DB["treasury"] -= 1000000000
            for k in DB["users"]: DB["users"][k]["balance"] += 1000
            save(); safe_answer(c, "وزعت 1 مليار على الشعب! 🎁💰"); return
        if d == "king_give_all":
            if not is_king(uid): return
            for k in DB["users"]: DB["users"][k]["balance"] += 100000
            save(); safe_edit(c, "🎁 وزعت 100K على كل واحد!", main_kb(uid)); return
        if d == "king_report":
            safe_edit(c, f"📊 تقرير الملك اليومي\n\n{pop_text()}\n\n💰 دخل النهاردة: 12,500,000 ﷼\n👥 ناس جديدة: +5000\n💍 جوازات: 1000", back_kb()); return
        if d == "king_disguise": safe_answer(c, "تنكرت كمواطن احمد! محدش عارف انك الملك 🎭"); return
        if d == "king_crazy": safe_answer(c, "فعلت وضع المجنون! 🤪"); return

        if d == "mass":
            if not is_king(uid): return
            kb = InlineKeyboardMarkup(row_width=2)
            kb.add(InlineKeyboardButton("💰 ارفع الجزية", callback_data="mass_tax_up"), InlineKeyboardButton("📉 نزل الجزية", callback_data="mass_tax_down"), InlineKeyboardButton("💰 اجمع الزكاة - 5M", callback_data="mass_zakat"), InlineKeyboardButton("🎁 وزع هدية على الكل", callback_data="mass_gift"), InlineKeyboardButton("✅ فك حظر الكل", callback_data="mass_unban"), InlineKeyboardButton("⛓️ اسجن المتمردين", callback_data="mass_jail"), InlineKeyboardButton("📢 خطاب للكل", callback_data="mass_msg"), InlineKeyboardButton("🔙 رجوع", callback_data="back"))
            safe_edit(c, "🔥 تحكم جماعي في المليون\n\nدوس زرار واحد - يتنفذ على المليون كلهم", kb); return
        if d.startswith("mass_"):
            if not is_king(uid): return
            if d == "mass_zakat": DB["treasury"] += 5000000; save(); safe_answer(c, "جمعت الزكاة 5M ﷼ 💰")
            elif d == "mass_gift":
                for k in DB["users"]: DB["users"][k]["balance"] += 10000
                save(); safe_answer(c, "وزعت 10000 ﷼ على الكل 🎁")
            elif d == "mass_unban": DB["banned"] = []; save(); safe_answer(c, "فكيت حظر الكل ✅")
            elif d == "mass_jail": safe_answer(c, "سجنت كل المتمردين ⛓️")
            elif d == "mass_msg": safe_answer(c, "بعت خطاب للمليون كلهم 📢")
            else: safe_answer(c, "تم تنفيذ المرسوم على المليون 🔥")
            return

        if d == "decree":
            if not is_king(uid): return
            kb = InlineKeyboardMarkup(row_width=2)
            kb.add(InlineKeyboardButton("📜 الجزية 500", callback_data="decree_tax"), InlineKeyboardButton("📜 العبيد يبقوا مواطنين", callback_data="decree_free"), InlineKeyboardButton("📜 المواطنين يبقوا عبيد 😂", callback_data="decree_slave"), InlineKeyboardButton("📜 ممنوع السرقة", callback_data="decree_nosteal"), InlineKeyboardButton("🔙 رجوع", callback_data="back"))
            safe_edit(c, "📜 مرسوم ملكي\n\nاكتب مرسوم مرة واحدة، يمشي على المليون", kb); return
        if d.startswith("decree_"):
            if not is_king(uid): return
            if d == "decree_free":
                for k in DB["users"]:
                    if DB["users"][k]["role"] == "⛓️ عبد": DB["users"][k]["role"] = "مواطن"
                save(); safe_answer(c, "كل العبيد بقوا مواطنين! 🎉")
            elif d == "decree_slave":
                for k in DB["users"]:
                    if not DB["users"][k].get("is_king"): DB["users"][k]["role"] = "⛓️ عبد"
                save(); safe_answer(c, "كل المواطنين بقوا عبيد 😂⛓️")
            else: safe_answer(c, "تم اصدار المرسوم الملكي 📜")
            return

        if d == "print_money":
            if not is_king(uid): return
            kb = InlineKeyboardMarkup(); kb.add(InlineKeyboardButton("🖨️ اطبع 100,000 ﷼", callback_data="print_100k"), InlineKeyboardButton("🖨️ اطبع 1M ﷼", callback_data="print_1m"), InlineKeyboardButton("🖨️ اطبع 1 مليار ﷼", callback_data="print_1b"), InlineKeyboardButton("🔙 رجوع", callback_data="back"))
            safe_edit(c, "🖨️ اطبع ريال\n\nخلي بالك: لو طبعت كتير التضخم هيزيد 😂", kb); return
        if d.startswith("print_"):
            if not is_king(uid): return
            amounts = {"print_100k":100000,"print_1m":1000000,"print_1b":1000000000}
            DB["treasury"] += amounts[d]; DB["inflation"] += 1; save(); safe_answer(c, f"طبعت {amounts[d]:,} ﷼! التضخم بقى {DB['inflation']}% 🖨️"); return

        if d == "rain_money":
            if not is_king(uid): return
            for k in DB["users"]: DB["users"][k]["balance"] += 5000
            save(); safe_answer(c, "رميت فلوس من الطيارة! الكل خد 5000 ﷼ 🚁💰"); return

        if d == "wipe":
            if not is_king(uid): return
            kb = InlineKeyboardMarkup(row_width=2)
            for r in DB["regions"]: kb.add(InlineKeyboardButton(f"💣 امسح {r}", callback_data=f"wipe_{r}"))
            kb.add(InlineKeyboardButton("🔙 رجوع", callback_data="back"))
            safe_edit(c, "💣 امسح منطقة كاملة\n\nكل اللي فيها هيتحظروا وفلوسهم تروح للخزينة", kb); return
        if d.startswith("wipe_"):
            if not is_king(uid): return
            r = d.replace("wipe_","")
            gain = DB["regions"].get(r,0)*10
            DB["treasury"] += gain; DB["population"] -= DB["regions"].get(r,0); DB["regions"][r] = 0; save(); safe_answer(c, f"مسحت {r}! وخدت {gain:,} ﷼ 💣"); return

        if d == "emergency":
            if not is_king(uid): return
            kb = InlineKeyboardMarkup(); kb.add(InlineKeyboardButton("🚨 اعلن حالة طوارئ", callback_data="em_on"), InlineKeyboardButton("💣 انقلاب! اقمعه", callback_data="coup_stop"), InlineKeyboardButton("🔙 رجوع", callback_data="back"))
            safe_edit(c, "🚨 طوارئ وانقلاب\n\nلو الشعب عمل انقلاب، دوس اقمعه!", kb); return
        if d == "em_on": safe_answer(c, "اعلنت حالة طوارئ! 🚨"); return
        if d == "coup_stop": safe_answer(c, "قمعت الانقلاب! العرش لسه بتاعك 👑⚔️"); return

        # لو زرار مش متعرف عليه - رجعه للقايمة بدل ما يقف
        safe_answer(c, "تمام يا ملك 👑")
        safe_edit(c, f"👑 مملكة الملك\n\n{pop_text()}", main_kb(uid))

    except Exception as e:
        print(f"CALLBACK ERROR {c.data}: {e}")
        traceback.print_exc()
        try:
            bot.send_message(c.message.chat.id, "حصلت غلطة صغيرة، دوس /start تاني 👑", reply_markup=main_kb(uid))
        except: pass

if __name__ == "__main__":
    print("Bot is running... 👑")
    try: bot.delete_webhook(drop_pending_updates=True)
    except: pass
    time.sleep(2)
    while True:
        try:
            bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)
            break
        except Exception as e:
            print(f"Polling error: {e} - retry in 10s...")
            time.sleep(10)
