# -*- coding: utf-8 -*-
# 👑 مملكة الملك - الكود النهائي - اغنى دولة في العالم
# الملك: 8188263997 | العملة: ريال ﷼ | الشعب: 1,000,000

import random, time, threading, json, os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# التوكن من Render Environment - مش من الكود
TOKEN = os.environ.get("BOT_TOKEN") or "حط_التوكن_بتاعك_هنا"
bot = telebot.TeleBot(TOKEN)

KING_ID = 8188263997  # 👑 الملك - انت

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
        "treasury": 999999999999,
        "population": 1000000,
        "births_today": 0,
        "deaths_today": 0,
        "marriages_today": 0,
        "oil_price": 80,
        "inflation": 0,
        "king_balance": 1000000000,
        "king_crown_level": 1,
        "king_throne": "🪑 عرش خشب",
        "king_palace": [],
        "regions": {
            "الرياض": 350000, "جدة": 200000, "مكة": 150000,
            "المدينة": 100000, "الدمام": 120000, "القصيم": 50000, "أبها": 30000
        },
        "users": {},
        "banned": [], "jailed": [],
        "news": [],
        "zombie_count": 0,
        "moon_colony": 0,
        "last_rain": 0,
    }

def save():
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(DB, f, ensure_ascii=False, indent=2)
    except: pass

def get_user(uid, name="مواطن"):
    uid = str(uid)
    if uid not in DB["users"]:
        DB["users"][uid] = {
            "name": name, "balance": 100000, "role": "مواطن",
            "region": random.choice(list(DB["regions"].keys())),
            "house": "🏠 بيت", "car": "🚗 كامري", "wife": "لا",
            "kids": 0, "job": random.choice(["تاجر","عسكري","عامل نفط","شيخ","مواطن"]),
            "level": 1, "hasanat": 0, "is_king": False,
            "last_daily": 0, "title": "مواطن"
        }
        save()
    return DB["users"][uid]

def is_king(uid):
    return str(uid) == str(KING_ID) or DB["users"].get(str(uid), {}).get("is_king")

def fmt(n):
    return f"{int(n):,} ﷼"

def pop_text():
    regions = "\n".join([f"{'🏰' if k=='الرياض' else '🌊' if k=='جدة' else '🕌' if k in ['مكة','المدينة'] else '🛢️' if k=='الدمام' else '🌴' if k=='القصيم' else '🏔️'} {k}: {v:,}" for k,v in DB["regions"].items()])
    return f"👥 سكان المملكة: {DB['population']:,}\n{regions}\n👶 اتولدوا: +{DB['births_today']} | 💀 ماتوا: -{DB['deaths_today']} | 💍 اتجوزوا: {DB['marriages_today']}\n💰 الخزينة: {fmt(DB['treasury'])}\n🛢️ النفط: {DB['oil_price']} ﷼ | 📈 التضخم: {DB['inflation']}%\n🕒 اخر تحديث: {time.strftime('%H:%M:%S')}"

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
    )
    if is_king(uid):
        kb.add(
            InlineKeyboardButton("👑 لوحة الملك - تحكم في المليون", callback_data="king_panel"),
            InlineKeyboardButton("🔥 تحكم جماعي", callback_data="mass"),
            InlineKeyboardButton("📜 مرسوم ملكي", callback_data="decree"),
            InlineKeyboardButton("🖨️ اطبع ريال", callback_data="print_money"),
            InlineKeyboardButton("🚁 ارمي فلوس من الطيارة", callback_data="rain_money"),
            InlineKeyboardButton("💣 امسح منطقة", callback_data="wipe"),
            InlineKeyboardButton("🚨 انقلاب / طوارئ", callback_data="emergency"),
        )
    kb.add(
        InlineKeyboardButton("🎮 العاب", callback_data="games"),
        InlineKeyboardButton("🌙 رمضان / العيد", callback_data="ramadan"),
        InlineKeyboardButton("🚀 الفضاء", callback_data="space"),
        InlineKeyboardButton("🧟 زومبي", callback_data="zombie"),
        InlineKeyboardButton("🐉 تنين", callback_data="dragon"),
        InlineKeyboardButton("🏴‍☠️ قراصنة وكنز", callback_data="pirate"),
        InlineKeyboardButton("🧙 سحر", callback_data="magic"),
        InlineKeyboardButton("💧 حنفية الفلوس", callback_data="tap"),
        InlineKeyboardButton("🌧️ مطر فلوس", callback_data="rain_event"),
        InlineKeyboardButton("🌳 شجرة الفلوس", callback_data="tree"),
        InlineKeyboardButton("🔄 حدث العداد", callback_data="refresh"),
    )
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
            DB["treasury"] += oil_income
            DB["treasury"] += random.randint(1000, 5000)
            # زومبي يزيد لوحده
            if random.random() < 0.1:
                DB["zombie_count"] += random.randint(1, 5)
            events = [
                f"👶 اتولد {births} عيل جديد في {region}",
                f"💀 مات {deaths} مواطنين في {region}",
                f"💍 {random.randint(1,5)} جوازات جديدة في {region}",
                f"🛢️ النفط غلي - الخزينة زادت {oil_income:,} ﷼",
                f"🌧️ مطر فلوس في {region}!",
                f"📰 1000 مواطن في {region} اشتروا عربيات جديدة",
                f"⚔️ 200 عسكري جديد انضموا للجيش",
                f"🧟 {random.randint(1,10)} زومبي جديد ظهر في {region}",
            ]
            DB["news"].append(random.choice(events))
            DB["news"] = DB["news"][-20:]
            save()
        except: pass

threading.Thread(target=population_loop, daemon=True).start()

@bot.message_handler(commands=['start'])
def start(m):
    u = get_user(m.from_user.id, m.from_user.first_name)
    if str(m.from_user.id) == str(KING_ID):
        u["is_king"] = True
        u["role"] = "👑 الملك"
        u["balance"] = max(u["balance"], 1000000000)
        save()
    bot.send_message(m.chat.id,
        f"👑🇸🇦 اهلا بيك في **مملكة الملك** - اغنى دولة في العالم!\n\n{pop_text()}\n\n💰 معاك: {fmt(u['balance'])}\n🎖️ رتبتك: {u['role']}\n🏰 منطقتك: {u['region']}\n\nكل حاجة بالريال ﷼، الشوارع من ذهب والحنفيات بتنزل فلوس 😂",
        reply_markup=main_kb(m.from_user.id), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda c: True)
def callbacks(c):
    uid = c.from_user.id
    u = get_user(uid, c.from_user.first_name)
    d = c.data
    try: bot.answer_callback_query(c.id)
    except: pass

    if d == "back":
        bot.edit_message_text(f"👑 مملكة الملك\n\n{pop_text()}", c.message.chat.id, c.message.message_id, reply_markup=main_kb(uid)); return
    if d == "refresh":
        bot.edit_message_text(f"🔄 العداد اتحدث!\n\n{pop_text()}", c.message.chat.id, c.message.message_id, reply_markup=main_kb(uid)); return
    if d == "treasury":
        kb = InlineKeyboardMarkup(); kb.add(InlineKeyboardButton("🔙 رجوع", callback_data="back"))
        bot.edit_message_text(f"💰 **الخزينة**\n\n{fmt(DB['treasury'])}\nبتزيد كل 10 ثواني من النفط والذهب والزكاة 💰", c.message.chat.id, c.message.message_id, reply_markup=kb); return

    if d == "kingdom":
        kb = InlineKeyboardMarkup(); kb.add(InlineKeyboardButton("👥 عداد الشعب", callback_data="people"), InlineKeyboardButton("💰 الخزينة", callback_data="treasury"), InlineKeyboardButton("🔙 رجوع", callback_data="back"))
        bot.edit_message_text(f"🏰 **المملكة - اغنى دولة في العالم**\n\n{pop_text()}\n\n👑 الملك: اغنى ملك - ثروته {fmt(DB['king_balance'])}\n🏰 القصر: {', '.join(DB['king_palace']) or 'قصر ملكي'}\n👑 التاج: مستوى {DB['king_crown_level']}\n🪑 العرش: {DB['king_throne']}\n🌧️ مطر فلوس كل اسبوع - الشوارع ذهب", c.message.chat.id, c.message.message_id, reply_markup=kb, parse_mode="Markdown"); return

    if d == "people":
        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton("🏰 الرياض", callback_data="reg_الرياض"),
            InlineKeyboardButton("🌊 جدة", callback_data="reg_جدة"),
            InlineKeyboardButton("🕌 مكة", callback_data="reg_مكة"),
            InlineKeyboardButton("🛢️ الدمام", callback_data="reg_الدمام"),
            InlineKeyboardButton("💰 الاغنى 100", callback_data="rich"),
            InlineKeyboardButton("⛓️ المسجونين", callback_data="jailed"),
            InlineKeyboardButton("🚫 المحظورين", callback_data="banned"),
            InlineKeyboardButton("📊 جراف الشعب", callback_data="graph"),
            InlineKeyboardButton("📺 بث مباشر", callback_data="live"),
            InlineKeyboardButton("🔙 رجوع", callback_data="back"),
        )
        bot.edit_message_text(f"👥 **كل الرعايا - 1,000,000**\n\n{pop_text()}", c.message.chat.id, c.message.message_id, reply_markup=kb, parse_mode="Markdown"); return

    if d.startswith("reg_"):
        r = d.replace("reg_","")
        kb = InlineKeyboardMarkup(); kb.add(InlineKeyboardButton("🔙 رجوع", callback_data="people"))
        bot.edit_message_text(f"🏰 **{r}**\n\n👥 السكان: {DB['regions'].get(r,0):,}\n💰 دخل المنطقة: {DB['regions'].get(r,0)*2:,} ﷼", c.message.chat.id, c.message.message_id, reply_markup=kb); return
    if d in ["rich","jailed","banned","search","active"]:
        kb = InlineKeyboardMarkup(); kb.add(InlineKeyboardButton("🔙 رجوع", callback_data="people"))
        bot.edit_message_text(f"👥 **{d}**\n\n{pop_text()}\n\nالقائمة دي بتتجدد كل 10 ثواني 🔥", c.message.chat.id, c.message.message_id, reply_markup=kb); return

    if d == "live":
        live = "\n".join(DB["news"][-8:]) or "لا اخبار"
        kb = InlineKeyboardMarkup(); kb.add(InlineKeyboardButton("🔄 حدث", callback_data="live"), InlineKeyboardButton("🔙 رجوع", callback_data="back"))
        bot.edit_message_text(f"📺 **بث مباشر - حياة المليون**\n\n{pop_text()}\n\n📺 اخر احداث:\n{live}\n\nالعداد بيتجدد كل 10 ثواني لوحده 🔥", c.message.chat.id, c.message.message_id, reply_markup=kb); return
    if d == "graph":
        kb = InlineKeyboardMarkup(); kb.add(InlineKeyboardButton("🔙 رجوع", callback_data="back"))
        bot.edit_message_text(f"📊 **جراف الشعب**\n\n1M ┤        ╱╲\n   │      ╱  ╲\n   │    ╱    ╲\n   │  ╱      ╲\n999k┤╱        ╲___\n   └──────────────\n🏆 اعلى: {DB['population']+5000:,} | 📉 اقل: {DB['population']-2000:,} | 👥 الحالي: {DB['population']:,}", c.message.chat.id, c.message.message_id, reply_markup=kb); return

    if d == "wallet":
        kb = InlineKeyboardMarkup(); kb.add(InlineKeyboardButton("💰 خد راتبك 5000 ﷼", callback_data="salary"), InlineKeyboardButton("🎁 هدية يومية", callback_data="daily"), InlineKeyboardButton("🔙 رجوع", callback_data="back"))
        bot.edit_message_text(f"💰 **محفظتك**\n\n👤 {u['name']}\n💰 معاك: {fmt(u['balance'])}\n🎖️ رتبتك: {u['role']} - {u['title']}\n🏰 منطقتك: {u['region']}\n🏠 بيتك: {u['house']}\n🚗 عربيتك: {u['car']}\n💍 مراتك: {u['wife']} | 👶 عيالك: {u['kids']}\n💼 شغلك: {u['job']}\n⭐ حسناتك: {u['hasanat']}", c.message.chat.id, c.message.message_id, reply_markup=kb); return
    if d == "salary":
        u["balance"] += 5000; DB["treasury"] -= 5000; save(); bot.answer_callback_query(c.id, "خدت 5000 ﷼ راتب من الدولة الغنية 💰"); return
    if d == "daily":
        now = time.time()
        if now - u["last_daily"] < 86400:
            bot.answer_callback_query(c.id, "خدت هديتك النهاردة، تعالا بكرا 🎁"); return
        gift = random.choice([10000, 5000, 20000, 1000, 50000])
        if random.random() < 0.1:
            bot.edit_message_text(f"💣 انفجر فيك الصندوق! خسرت 1000 ﷼ بس خدت 5000 علاج 😂", c.message.chat.id, c.message.message_id, reply_markup=main_kb(uid)); u["balance"] += 4000
        else:
            u["balance"] += gift
            bot.edit_message_text(f"🎁 هدية يومية! كسبت {fmt(gift)} من الملك الغني 👑", c.message.chat.id, c.message.message_id, reply_markup=main_kb(uid))
        u["last_daily"] = now; save(); return

    if d == "tap":
        gain = random.randint(50, 200); u["balance"] += gain; save(); bot.answer_callback_query(c.id, f"فتحت الحنفية ونزل {gain} ﷼! 💧💰"); return
    if d == "rain_event":
        gain = random.randint(1000, 5000); u["balance"] += gain; save(); bot.answer_callback_query(c.id, f"مطر فلوس! جمعت {gain} ﷼ 🌧️💰"); return
    if d == "tree":
        gain = random.randint(1000, 2000); u["balance"] += gain; save(); bot.answer_callback_query(c.id, f"قطفت من شجرة الفلوس {gain} ﷼ 🌳💰"); return

    if d == "bank":
        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton("💰 حط 10,000 ﷼ - هتاخد 20,000", callback_data="bank_put"),
            InlineKeyboardButton("🏦 خد قرض 10M ببلاش", callback_data="bank_loan"),
            InlineKeyboardButton("💱 حول دولار لريال", callback_data="bank_exchange"),
            InlineKeyboardButton("🔙 رجوع", callback_data="back"),
        )
        bot.edit_message_text(f"🏦 **البنك المركزي السعودي**\n\n💰 فلوسك: {fmt(u['balance'])}\n📈 الفايدة: 100% - البنك غني 😂\n💰 الخزينة: {fmt(DB['treasury'])}", c.message.chat.id, c.message.message_id, reply_markup=kb); return
    if d == "bank_put":
        if u["balance"] >= 10000: u["balance"] += 10000; save(); bot.answer_callback_query(c.id, "حطيت 10000 وخدت 20000! 💰")
        else: bot.answer_callback_query(c.id, "معاكش 10000 ﷼")
        return
    if d == "bank_loan":
        u["balance"] += 10000000; save(); bot.answer_callback_query(c.id, "خدت قرض 10M ببلاش! 🎉"); return
    if d == "bank_exchange":
        u["balance"] += 375; save(); bot.answer_callback_query(c.id, "100 دولار = 375 ﷼ 💱"); return

    if d == "shop":
        kb = InlineKeyboardMarkup(row_width=2)
        items = [
            ("🚗 لامبورجيني - 5M ﷼", "buy_lambo"),
            ("🚗 رولز رويس - 10M ﷼", "buy_rolls"),
            ("🚗 بوغاتي - 50M ﷼", "buy_bugatti"),
            ("🏠 فيلا - 10M ﷼", "buy_villa"),
            ("🏰 قصر - 100M ﷼", "buy_palace"),
            ("🏝️ جزيرة - 500M ﷼", "buy_island"),
            ("⌚ رولكس ذهب - 1M ﷼", "buy_rolex"),
            ("💎 تاج الماس - 10M ﷼", "buy_crown"),
            ("🚁 طيارة خاصة - 100M ﷼", "buy_plane"),
            ("🌙 بيت على القمر - 1B ﷼", "buy_moon"),
        ]
        for txt, cb in items: kb.add(InlineKeyboardButton(txt, callback_data=cb))
        kb.add(InlineKeyboardButton("🔙 رجوع", callback_data="back"))
        bot.edit_message_text(f"🛒 **المتجر الملكي - بالريال ﷼**\n\n💰 معاك: {fmt(u['balance'])}\nكل حاجة للاغنياء بس 👑", c.message.chat.id, c.message.message_id, reply_markup=kb); return
    if d.startswith("buy_"):
        prices = {"buy_lambo":5000000,"buy_rolls":10000000,"buy_bugatti":50000000,"buy_villa":10000000,"buy_palace":100000000,"buy_island":500000000,"buy_rolex":1000000,"buy_crown":10000000,"buy_plane":100000000,"buy_moon":1000000000}
        names = {"buy_lambo":"🚗 لامبورجيني","buy_rolls":"🚗 رولز رويس","buy_bugatti":"🚗 بوغاتي","buy_villa":"🏠 فيلا","buy_palace":"🏰 قصر","buy_island":"🏝️ جزيرة","buy_rolex":"⌚ رولكس","buy_crown":"💎 تاج الماس","buy_plane":"🚁 طيارة","buy_moon":"🌙 بيت على القمر"}
        p = prices.get(d, 0)
        if u["balance"] >= p:
            u["balance"] -= p; DB["treasury"] += p
            if "villa" in d or "palace" in d or "island" in d or "moon" in d: u["house"] = names[d]
            else: u["car"] = names[d]
            save(); bot.answer_callback_query(c.id, f"اشتريت {names[d]}! مبروك يا غني 🎉")
        else: bot.answer_callback_query(c.id, "معاكش فلوس كفاية، خد قرض من البنك 😂")
        return

    if d == "casino":
        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton("🎰 العب - رهان 1M ﷼", callback_data="casino_play"),
            InlineKeyboardButton("🎰 يانصيب - الجايزة 100M", callback_data="lottery"),
            InlineKeyboardButton("🎲 راهن على العداد ⬆️", callback_data="bet_up"),
            InlineKeyboardButton("🎲 راهن على العداد ⬇️", callback_data="bet_down"),
            InlineKeyboardButton("🎰 عجلة المليار", callback_data="wheel_billion"),
            InlineKeyboardButton("🔙 رجوع", callback_data="back"),
        )
        bot.edit_message_text(f"🎰 **كازينو المليونيرات**\n\n💰 معاك: {fmt(u['balance'])}\nالرهان يبدأ من 1M ﷼", c.message.chat.id, c.message.message_id, reply_markup=kb); return
    if d == "casino_play":
        if u["balance"] < 1000000: bot.answer_callback_query(c.id, "لازم يبقى معاك 1M عشان تلعب"); return
        if random.random() < 0.45: u["balance"] += 10000000; save(); bot.answer_callback_query(c.id, "كسبت 10M ﷼! 🎉🎉")
        else: u["balance"] += 1000000; save(); bot.answer_callback_query(c.id, "خسرت 1M بس خدت 2M هدية 😂 الدولة غنية")
        return
    if d == "lottery":
        if random.random() < 0.2: u["balance"] += 100000000; save(); bot.answer_callback_query(c.id, "كسبت اليانصيب 100M! 🎉🎉🎉")
        else: bot.answer_callback_query(c.id, "ماكسبتش، حاول تاني")
        return
    if d == "wheel_billion":
        if random.random() < 0.1: u["balance"] += 1000000000; save(); bot.answer_callback_query(c.id, "كسبت عجلة المليار! 1B ﷼! 🎉🎉🎉")
        else: u["balance"] += 10000; save(); bot.answer_callback_query(c.id, "كسبت 10000 ﷼ من العجلة 🎰")
        return
    if d in ["bet_up","bet_down"]:
        if random.random() < 0.5: u["balance"] += 2000; save(); bot.answer_callback_query(c.id, "كسبت الرهان 2000 ﷼ 🎲")
        else: bot.answer_callback_query(c.id, "خسرت الرهان")
        return

    if d == "war":
        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton("⚔️ اهجم على مملكة الظلام", callback_data="war_dark"),
            InlineKeyboardButton("⚔️ حرب الرياض ضد جدة", callback_data="war_regions"),
            InlineKeyboardButton("🕊️ صلح", callback_data="war_peace"),
            InlineKeyboardButton("🤝 تحالف", callback_data="war_ally"),
            InlineKeyboardButton("🔙 رجوع", callback_data="back"),
        )
        bot.edit_message_text(f"⚔️ **الحرب العالمية**\n\n🏰 مملكتك: 1M - جيش 200k\n🏴 مملكة الظلام: 500k\n🏳️ مملكة النور: 300k\n🏴‍☠️ مملكة القراصنة: 200k", c.message.chat.id, c.message.message_id, reply_markup=kb); return
    if d == "war_dark":
        if random.random() < 0.6: u["balance"] += 50000; DB["treasury"] += 1000000; DB["king_crown_level"] += 1; save(); bot.answer_callback_query(c.id, "كسبنا الحرب! +50000 ﷼ والتاج زاد 🎉")
        else: bot.answer_callback_query(c.id, "خسرنا الحرب، حاول تاني")
        return
    if d == "war_regions": bot.answer_callback_query(c.id, "الرياض كسبت جدة! ⚔️"); return
    if d in ["war_peace","war_ally"]: u["balance"] += 10000; save(); bot.answer_callback_query(c.id, "عملت صلح وكسبت 10000 ﷼ 🕊️"); return

    if d == "hajj":
        kb = InlineKeyboardMarkup(); kb.add(InlineKeyboardButton("🕋 اعمل حج - 500 ﷼", callback_data="do_hajj"), InlineKeyboardButton("🕌 اعمل عمرة - 500 ﷼", callback_data="do_umrah"), InlineKeyboardButton("🔙 رجوع", callback_data="back"))
        bot.edit_message_text(f"🕋 **الحج والعمرة**\n\n🕋 الحج: 100k بيحجوا كل سنة\n🕌 العمرة: 10k كل اسبوع\n⭐ حسناتك: {u['hasanat']}", c.message.chat.id, c.message.message_id, reply_markup=kb); return
    if d in ["do_hajj","do_umrah"]: u["hasanat"] += 1000; u["balance"] += 5000; save(); bot.answer_callback_query(c.id, "تقبل الله! +1000 حسنة و +5000 ﷼ 🕋"); return

    if d == "palace":
        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton("🛏️ اوضة نوم - 100k", callback_data="palace_room"),
            InlineKeyboardButton("🏊 حمام سباحة - 200k", callback_data="palace_pool"),
            InlineKeyboardButton("🎮 اوضة العاب - 50k", callback_data="palace_game"),
            InlineKeyboardButton("🚁 مهبط طيارات - 500k", callback_data="palace_heli"),
            InlineKeyboardButton("💎 خزنة سرية - 1M", callback_data="palace_vault"),
            InlineKeyboardButton("🦁 حديقة حيوان - 300k", callback_data="palace_zoo"),
            InlineKeyboardButton("🔙 رجوع", callback_data="back"),
        )
        bot.edit_message_text(f"🏰 **قصر الملك**\n\nاوض القصر: {', '.join(DB['king_palace']) or 'لسه فاضي'}\n💰 معاك: {fmt(u['balance'])}", c.message.chat.id, c.message.message_id, reply_markup=kb); return
    if d.startswith("palace_"):
        names = {"palace_room":"🛏️ اوضة نوم","palace_pool":"🏊 حمام سباحة","palace_game":"🎮 اوضة العاب","palace_heli":"🚁 مهبط طيارات","palace_vault":"💎 خزنة سرية","palace_zoo":"🦁 حديقة حيوان"}
        if names[d] not in DB["king_palace"]: DB["king_palace"].append(names[d]); save()
        bot.answer_callback_query(c.id, f"اشتريت {names[d]} للقصر! 🎉"); return

    if d == "news":
        news = "\n".join(DB["news"][-10:]) or "لا اخبار"
        kb = InlineKeyboardMarkup(); kb.add(InlineKeyboardButton("🔙 رجوع", callback_data="back"))
        bot.edit_message_text(f"📰 **جريدة المملكة**\n\n{news}\n\n{pop_text()}", c.message.chat.id, c.message.message_id, reply_markup=kb); return

    if d == "games":
        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton("🏇 سباق خيول", callback_data="game_horse"),
            InlineKeyboardButton("🎰 عجلة الحظ", callback_data="game_wheel"),
            InlineKeyboardButton("💣 القنبلة", callback_data="game_bomb"),
            InlineKeyboardButton("🦅 صيد الصقور", callback_data="game_falcon"),
            InlineKeyboardButton("🎯 قنص", callback_data="game_snipe"),
            InlineKeyboardButton("⚽ دوري كورة", callback_data="game_soccer"),
            InlineKeyboardButton("🏇 سباق الهجن", callback_data="game_camel"),
            InlineKeyboardButton("🧩 لغز الملك", callback_data="game_puzzle"),
            InlineKeyboardButton("🔙 رجوع", callback_data="back"),
        )
        bot.edit_message_text("🎮 **العاب المملكة**\n\nكل لعبة تكسبك فلوس 👑", c.message.chat.id, c.message.message_id, reply_markup=kb); return
    if d.startswith("game_"):
        win = random.randint(500, 10000); u["balance"] += win; save(); bot.answer_callback_query(c.id, f"كسبت {win:,} ﷼ في اللعبة! 🎉"); return

    if d == "ramadan":
        kb = InlineKeyboardMarkup(); kb.add(InlineKeyboardButton("🌙 خد فطار 5000 ﷼", callback_data="iftar"), InlineKeyboardButton("🎉 خد عيدية 50,000 ﷼", callback_data="eid"), InlineKeyboardButton("🔙 رجوع", callback_data="back"))
        bot.edit_message_text("🌙 **رمضان والعيد**\n\nفي رمضان: الجزية تتلغي والكل ياخد هدية\nفي العيد: كل واحد ياخد 50,000 ﷼ عيدية", c.message.chat.id, c.message.message_id, reply_markup=kb); return
    if d == "iftar": u["balance"] += 5000; save(); bot.answer_callback_query(c.id, "خدت فطار 5000 ﷼ 🌙"); return
    if d == "eid": u["balance"] += 50000; save(); bot.answer_callback_query(c.id, "خدت عيدية 50,000 ﷼ 🎉"); return

    if d == "space":
        kb = InlineKeyboardMarkup(); kb.add(InlineKeyboardButton("🚀 ابني صاروخ - 1M", callback_data="build_rocket"), InlineKeyboardButton("🌙 مستعمرة القمر", callback_data="moon"), InlineKeyboardButton("👽 اتكلم مع كائنات", callback_data="alien"), InlineKeyboardButton("🔙 رجوع", callback_data="back"))
        bot.edit_message_text(f"🚀 **وكالة الفضاء السعودية**\n\n🌙 مستعمرة القمر: {DB['moon_colony']} مواطن", c.message.chat.id, c.message.message_id, reply_markup=kb); return
    if d == "build_rocket":
        if u["balance"] >= 1000000: u["balance"] -= 1000000; DB["moon_colony"] += 10000; save(); bot.answer_callback_query(c.id, "اطلقت الصاروخ! 10k سافروا القمر 🚀🌙")
        else: bot.answer_callback_query(c.id, "لازم 1M عشان تبني صاروخ")
        return
    if d == "moon": u["balance"] += 10000; save(); bot.answer_callback_query(c.id, "سافرت القمر ورجعت بـ 10000 ﷼ 🌙"); return
    if d == "alien": u["balance"] += 1000000; save(); bot.answer_callback_query(c.id, "اتصاحبت على الكائنات وخدت 1M 👽"); return

    if d == "zombie":
        kb = InlineKeyboardMarkup(); kb.add(InlineKeyboardButton("🔫 اقتل زومبي - 1000 ﷼", callback_data="kill_zombie"), InlineKeyboardButton("💉 اعمل علاج", callback_data="cure_zombie"), InlineKeyboardButton("🔙 رجوع", callback_data="back"))
        bot.edit_message_text(f"🧟 **وباء الزومبي**\n\n🧟 عدد الزومبي: {DB['zombie_count']}\n🔫 كل زومبي تقتله تاخد 1000 ﷼", c.message.chat.id, c.message.message_id, reply_markup=kb); return
    if d == "kill_zombie": u["balance"] += 1000; DB["zombie_count"] = max(0, DB["zombie_count"]-1); save(); bot.answer_callback_query(c.id, "قتلت زومبي! +1000 ﷼ 🔫🧟"); return
    if d == "cure_zombie": DB["zombie_count"] = 0; save(); bot.answer_callback_query(c.id, "عالجت كل الزومبي! 💉"); return

    if d == "dragon":
        kb = InlineKeyboardMarkup(); kb.add(InlineKeyboardButton("🐉 اطلق التنين", callback_data="release_dragon"), InlineKeyboardButton("🥚 لاقي بيضة تنين", callback_data="dragon_egg"), InlineKeyboardButton("🔙 رجوع", callback_data="back"))
        bot.edit_message_text("🐉 **تنين المملكة**\n\nالتنين بيحرق منطقة كاملة وتاخد فلوسهم 🔥", c.message.chat.id, c.message.message_id, reply_markup=kb); return
    if d == "release_dragon": u["balance"] += 50000; save(); bot.answer_callback_query(c.id, "التنين حرق منطقة وخدت 50000 ﷼ 🐉🔥"); return
    if d == "dragon_egg": u["balance"] += 100000; save(); bot.answer_callback_query(c.id, "لقيت بيضة تنين! بعتها بـ 100k 🥚🐉"); return

    if d == "pirate":
        kb = InlineKeyboardMarkup(); kb.add(InlineKeyboardButton("🗺️ دور على الكنز", callback_data="treasure"), InlineKeyboardButton("⚔️ حارب القراصنة", callback_data="fight_pirate"), InlineKeyboardButton("🔙 رجوع", callback_data="back"))
        bot.edit_message_text("🏴‍☠️ **قراصنة وكنز**\n\nالكنز فيه 1M ﷼", c.message.chat.id, c.message.message_id, reply_markup=kb); return
    if d == "treasure":
        if random.random() < 0.3: u["balance"] += 1000000; save(); bot.answer_callback_query(c.id, "لقيت الكنز! 1M ﷼! 🗺️💰")
        else: bot.answer_callback_query(c.id, "مالقيتش الكنز، حاول تاني")
        return
    if d == "fight_pirate": u["balance"] += 10000; save(); bot.answer_callback_query(c.id, "حاربت القراصنة وكسبت 10000 ﷼ ⚔️🏴‍☠️"); return

    if d == "magic":
        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton("🧙 اعمل سحر", callback_data="magic_spell"),
            InlineKeyboardButton("🔮 اسأل الكورة", callback_data="magic_ball"),
            InlineKeyboardButton("❤️ جرعة حب", callback_data="magic_love"),
            InlineKeyboardButton("💰 جرعة فلوس", callback_data="magic_money"),
            InlineKeyboardButton("👻 جرعة اختفاء", callback_data="magic_ghost"),
            InlineKeyboardButton("🔙 رجوع", callback_data="back"),
        )
        bot.edit_message_text("🧙 **سحر وشعوذة**\n\nالسحر ممكن يكسبك 1M وممكن يخسرك 😂", c.message.chat.id, c.message.message_id, reply_markup=kb); return
    if d == "magic_spell":
        if random.random() < 0.5: u["balance"] += 1000000; save(); bot.answer_callback_query(c.id, "السحر نجح! +1M ﷼ 🧙")
        else: u["balance"] = max(1000, u["balance"]//2); save(); bot.answer_callback_query(c.id, "السحر فشل! خسرت نص فلوسك 😂")
        return
    if d == "magic_ball": bot.answer_callback_query(c.id, random.choice(["ايوه بيحبك ❤️", "لا بيكرهك 😂", "الملك احسن ملك 👑"])); return
    if d in ["magic_love","magic_money","magic_ghost"]: u["balance"] += 5000; save(); bot.answer_callback_query(c.id, "شربت الجرعة! +5000 ﷼ 🧪"); return

    if d == "king_panel":
        if not is_king(uid): bot.answer_callback_query(c.id, "انت مش الملك! 👑"); return
        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton("💰 خد راتبك 100M ﷼", callback_data="king_salary"),
            InlineKeyboardButton("🎁 وزع 1 مليار على الشعب", callback_data="king_give_billion"),
            InlineKeyboardButton("👥 شوف الشعب", callback_data="people"),
            InlineKeyboardButton("📊 تقرير الملك", callback_data="king_report"),
            InlineKeyboardButton("🎭 تنكر كمواطن", callback_data="king_disguise"),
            InlineKeyboardButton("🤪 وضع المجنون", callback_data="king_crazy"),
            InlineKeyboardButton("🔙 رجوع", callback_data="back"),
        )
        bot.edit_message_text(f"👑 **لوحة الملك - تتحكم في المليون**\n\n{pop_text()}\n\n💰 ثروتك: {fmt(u['balance'])}", c.message.chat.id, c.message.message_id, reply_markup=kb); return
    if d == "king_salary":
        if not is_king(uid): return
        u["balance"] += 100000000; save(); bot.answer_callback_query(c.id, "خدت راتبك الملكي 100M ﷼ 👑"); return
    if d == "king_give_billion":
        if not is_king(uid): return
        DB["treasury"] -= 1000000000
        for k in DB["users"]: DB["users"][k]["balance"] += 1000
        save(); bot.answer_callback_query(c.id, "وزعت 1 مليار على الشعب! 🎁💰"); return
    if d == "king_report":
        kb = InlineKeyboardMarkup(); kb.add(InlineKeyboardButton("🔙 رجوع", callback_data="back"))
        bot.edit_message_text(f"📊 **تقرير الملك اليومي**\n\n{pop_text()}\n\n💰 دخل النهاردة: 12,500,000 ﷼\n👥 ناس جديدة: +5000\n💍 جوازات: 1000\n⚔️ سرقات: 300\n⛓️ مسجونين: 1500", c.message.chat.id, c.message.message_id, reply_markup=kb); return
    if d == "king_disguise": bot.answer_callback_query(c.id, "تنكرت كمواطن احمد! محدش عارف انك الملك 🎭"); return
    if d == "king_crazy": bot.answer_callback_query(c.id, "فعلت وضع المجنون! كل القوانين اتلغت 1 ساعة 🤪"); return

    if d == "mass":
        if not is_king(uid): return
        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton("💰 ارفع الجزية على الكل", callback_data="mass_tax_up"),
            InlineKeyboardButton("📉 نزل الجزية", callback_data="mass_tax_down"),
            InlineKeyboardButton("💰 اجمع الزكاة - 5M", callback_data="mass_zakat"),
            InlineKeyboardButton("🎁 وزع هدية على الكل", callback_data="mass_gift"),
            InlineKeyboardButton("🔨 احظر كل العبيد", callback_data="mass_ban"),
            InlineKeyboardButton("✅ فك حظر الكل", callback_data="mass_unban"),
            InlineKeyboardButton("⛓️ اسجن كل المتمردين", callback_data="mass_jail"),
            InlineKeyboardButton("📢 ابعت خطاب للكل", callback_data="mass_msg"),
            InlineKeyboardButton("🔙 رجوع", callback_data="back"),
        )
        bot.edit_message_text(f"🔥 **تحكم جماعي في المليون**\n\nدوس زرار واحد - يتنفذ على المليون كلهم", c.message.chat.id, c.message.message_id, reply_markup=kb); return
    if d.startswith("mass_"):
        if not is_king(uid): return
        if d == "mass_zakat": DB["treasury"] += 5000000; save(); bot.answer_callback_query(c.id, "جمعت الزكاة 5M ﷼ من المليون 💰")
        elif d == "mass_gift":
            for k in DB["users"]: DB["users"][k]["balance"] += 10000
            save(); bot.answer_callback_query(c.id, "وزعت 10000 ﷼ على الكل 🎁")
        elif d == "mass_ban": bot.answer_callback_query(c.id, "حظرت كل العبيد 🔨")
        elif d == "mass_unban": DB["banned"] = []; save(); bot.answer_callback_query(c.id, "فكيت حظر الكل ✅")
        elif d == "mass_jail": bot.answer_callback_query(c.id, "سجنت كل المتمردين ⛓️")
        elif d == "mass_msg": bot.answer_callback_query(c.id, "بعت خطاب للمليون كلهم 📢")
        else: bot.answer_callback_query(c.id, "تم تنفيذ المرسوم على المليون 🔥")
        return

    if d == "decree":
        if not is_king(uid): return
        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton("📜 الجزية بقت 500 على الكل", callback_data="decree_tax"),
            InlineKeyboardButton("📜 كل العبيد يبقوا مواطنين", callback_data="decree_free"),
            InlineKeyboardButton("📜 كل المواطنين ينزلوا عبيد 😂", callback_data="decree_slave"),
            InlineKeyboardButton("📜 ممنوع السرقة", callback_data="decree_nosteal"),
            InlineKeyboardButton("🔙 رجوع", callback_data="back"),
        )
        bot.edit_message_text("📜 **مرسوم ملكي**\n\nاكتب مرسوم مرة واحدة، يمشي على المليون", c.message.chat.id, c.message.message_id, reply_markup=kb); return
    if d.startswith("decree_"):
        if not is_king(uid): return
        if d == "decree_free":
            for k in DB["users"]:
                if DB["users"][k]["role"] == "⛓️ عبد": DB["users"][k]["role"] = "مواطن"
            save(); bot.answer_callback_query(c.id, "كل العبيد بقوا مواطنين! 🎉")
        elif d == "decree_slave":
            for k in DB["users"]:
                if not DB["users"][k].get("is_king"): DB["users"][k]["role"] = "⛓️ عبد"
            save(); bot.answer_callback_query(c.id, "كل المواطنين بقوا عبيد 😂⛓️")
        else: bot.answer_callback_query(c.id, "تم اصدار المرسوم الملكي 📜")
        return

    if d == "print_money":
        if not is_king(uid): return
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("🖨️ اطبع 100,000 ﷼", callback_data="print_100k"), InlineKeyboardButton("🖨️ اطبع 1M ﷼", callback_data="print_1m"), InlineKeyboardButton("🖨️ اطبع 1 مليار ﷼", callback_data="print_1b"), InlineKeyboardButton("🔙 رجوع", callback_data="back"))
        bot.edit_message_text("🖨️ **اطبع ريال**\n\nخلي بالك: لو طبعت كتير التضخم هيزيد 😂", c.message.chat.id, c.message.message_id, reply_markup=kb); return
    if d.startswith("print_"):
        if not is_king(uid): return
        amounts = {"print_100k":100000,"print_1m":1000000,"print_1b":1000000000}
        DB["treasury"] += amounts[d]; DB["inflation"] += 1; save(); bot.answer_callback_query(c.id, f"طبعت {amounts[d]:,} ﷼! التضخم بقى {DB['inflation']}% 🖨️"); return

    if d == "rain_money":
        if not is_king(uid): return
        for k in DB["users"]: DB["users"][k]["balance"] += 5000
        save(); bot.answer_callback_query(c.id, "رميت فلوس من الطيارة! الكل خد 5000 ﷼ 🚁💰"); return

    if d == "wipe":
        if not is_king(uid): return
        kb = InlineKeyboardMarkup(row_width=2)
        for r in DB["regions"]: kb.add(InlineKeyboardButton(f"💣 امسح {r}", callback_data=f"wipe_{r}"))
        kb.add(InlineKeyboardButton("🔙 رجوع", callback_data="back"))
        bot.edit_message_text("💣 **امسح منطقة كاملة**\n\nكل اللي فيها هيتحظروا وفلوسهم تروح للخزينة", c.message.chat.id, c.message.message_id, reply_markup=kb); return
    if d.startswith("wipe_"):
        if not is_king(uid): return
        r = d.replace("wipe_","")
        gain = DB["regions"].get(r,0)*10
        DB["treasury"] += gain; DB["population"] -= DB["regions"].get(r,0); DB["regions"][r] = 0; save(); bot.answer_callback_query(c.id, f"مسحت {r}! وخدت {gain:,} ﷼ 💣"); return

    if d == "emergency":
        if not is_king(uid): return
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("🚨 اعلن حالة طوارئ", callback_data="em_on"), InlineKeyboardButton("💣 انقلاب! اقمعه", callback_data="coup_stop"), InlineKeyboardButton("🔙 رجوع", callback_data="back"))
        bot.edit_message_text("🚨 **طوارئ وانقلاب**\n\nلو الشعب عمل انقلاب، دوس اقمعه في 5 دقايق والا هتخسر العرش 1 ساعة!", c.message.chat.id, c.message.message_id, reply_markup=kb); return
    if d == "em_on": bot.answer_callback_query(c.id, "اعلنت حالة طوارئ! الكل اتكتم 🚨"); return
    if d == "coup_stop": bot.answer_callback_query(c.id, "قمعت الانقلاب! العرش لسه بتاعك 👑⚔️"); return

    bot.answer_callback_query(c.id, "تمام يا ملك 👑")


if __name__ == "__main__":
    print("Bot is running... 👑")
    # بيمسح اي نسخة قديمة وبيستنى
    try:
        bot.delete_webhook(drop_pending_updates=True)
        print("Webhook deleted - old instance killed")
    except Exception as e:
        print(f"Webhook delete: {e}")
    
    time.sleep(5)
    
    # لو حصل 409 يستنى 10 ثواني ويحاول تاني مش يموت
    while True:
        try:
            bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)
            break
        except Exception as e:
            print(f"Polling error: {e} - retry in 10s...")
            time.sleep(10)
