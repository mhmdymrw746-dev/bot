# ============================================================
# BOT FINAL MERGED - V3 + FIX + 1000 LINE - NO ERRORS
# مدمج: القديم + تصليح اليانصيب + انظمة جديدة 700 سطر
# ============================================================
import os, json, time, random, traceback, datetime, urllib.request, math
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers(); self.wfile.write(b"Bot is alive MERGED!")
    def log_message(self, *a): pass
def keep_alive():
    try:
        port = int(os.environ.get("PORT", 10000))
        Thread(target=HTTPServer(("0.0.0.0", port), Handler).serve_forever, daemon=True).start()
    except: pass
keep_alive()
def self_ping():
    while True:
        time.sleep(240)
        url = os.environ.get("RENDER_EXTERNAL_URL")
        if url:
            try: urllib.request.urlopen(url, timeout=10)
            except: pass
Thread(target=self_ping, daemon=True).start()
TOKEN = os.environ.get("TOKEN")
OWNER_ID = int(os.environ.get("OWNER_ID", "8188263997"))
bot = telebot.TeleBot(TOKEN)

def load_json(f, default):
    if os.path.exists(f):
        try:
            with open(f, encoding="utf-8") as x: return json.load(x)
        except: return default
    return default
def save_json(f, d):
    try:
        with open(f+".tmp", "w", encoding="utf-8") as x: json.dump(d, x, ensure_ascii=False, indent=2)
        os.replace(f+".tmp", f)
    except: pass
data = load_json("data.json", {})
settings = load_json("settings.json", {"maintenance": False, "banned": [], "lottery": [], "jackpot": 10000, "clans": {}, "auction": [], "last_lottery": 0, "total_users": 0})
def save(): save_json("data.json", data)
def save_settings(): save_json("settings.json", settings)
pending = {}

# ========== توليد مميزات مبتخلصش ==========
WEAPONS = {}
for i in range(1, 101):
    WEAPONS[f"w{i}"] = (f"{['🔪','🔫','💣','🚀','⚔️','🏹','🗡️','🔨','🪓','💎'][i%10]} سلاح {i}", i*100, i*5)
PETS = {}
PET_NAMES = ["🐉 تنين","🦁 أسد","🦅 نسر","🐱 قطة","🐶 كلب","🐯 نمر","🦊 ثعلب","🐺 ذئب","🦄 يونيكورن","🐲 دراجون","🦖 ديناصور","🐘 فيل","🦒 زرافة","🐻 دب","🦁 أسد ذهبي"]
for i in range(1, 101):
    PETS[f"pet{i}"] = (f"{PET_NAMES[i%len(PET_NAMES)]} {i}", 100+i*50, 10+i*5)
HOUSES = {}
for i in range(1, 101): HOUSES[f"h{i}"] = (f"🏠 بيت {i}", 10000+i*5000, 100+i*100)
CARS = {}
for i in range(1, 101): CARS[f"c{i}"] = (f"{['🚕','🚗','🏎️','🚙','🚌','🚚','🏍️','🚁','✈️','🛥️'][i%10]} عربية {i}", 5000+i*3000, 50+i*50)
BUSINESS = {}
for i in range(1, 101): BUSINESS[f"b{i}"] = (f"{['🏪 محل','🍔 مطعم','☕ قهوة','🏢 شركة','🏥 مستشفى','🏫 مدرسة','🏨 فندق','🎮 سايبر','💈 صالون','🏦 بنك'][i%10]} {i}", 5000+i*2000, 100+i*80)
TASKS = []
for i in range(1, 501): TASKS.append((f"مهمة {i}", 50 + (i%10)*50))
CODES = {}
for i in range(1, 101): CODES[f"CODE{i}"] = 500*i
CODES.update({"WELCOME100":500,"MEGA500":2000,"BOSS1000":5000,"ADI2026":10000,"DRAGON":3000,"HOUSE2026":20000,"VIP999":50000,"MILLION":100000})
MARKET = {}
for i in range(1, 51): MARKET[f"coin{i}"] = {"name": f"{['₿ بيتكوين','Ξ ايثريوم','🥇 ذهب','💵 دولار','🛢️ بترول','💎 الماس','🪙 دوج','🐶 شيبا','📈 سهم','🏦 بنك'][i%10]} {i}", "price": 50+i*30}
MARKET.update({"btc":{"name":"₿ بيتكوين","price":800},"eth":{"name":"Ξ ايثريوم","price":300},"gold":{"name":"🥇 ذهب","price":150}})

def update_market_loop():
    while True:
        time.sleep(30)
        try:
            for k in MARKET: MARKET[k]["price"]=max(20, MARKET[k]["price"]+random.randint(-40,60))
        except: pass
Thread(target=update_market_loop, daemon=True).start()
def auto_lottery():
    while True:
        time.sleep(3600)
        try:
            if time.time() - settings.get("last_lottery",0) > 86400 and settings.get("lottery"):
                winner=random.choice(settings["lottery"]); prize=settings.get("jackpot",10000); w=user(int(winner)); w["money"]+=prize; settings["lottery"]=[]; settings["jackpot"]=10000; settings["last_lottery"]=int(time.time()); save(); save_settings()
                for k in list(data.keys()):
                    try: bot.send_message(int(k), f"💎 سحب اليانصيب اليومي!\n🏆 الفايز: {w.get('name')} كسب {prize}!")
                    except: pass
        except: pass
Thread(target=auto_lottery, daemon=True).start()

def user(uid):
    uid = str(uid)
    if uid not in data:
        data[uid] = {"money":500,"name":"مستخدم","level":1,"xp":0,"vip":False,"vip_until":0,"weapons":[],"daily":0,"spin":0,"gift":0,"streak":0,"score":0,"codes":[],"items":[],"portfolio":{},"bank":0,"bank_current":0,"bank_saving":0,"bank_history":[],"certificates":[],"credit_limit":5000,"credit_used":0,"iban":"","overdraft":0,"steal":0,"lottery_tickets":0,"loans":[],"invest":0,"gold_box":0,"last_challenge":0,"pets":[],"clan":None,"wins":0,"losses":0,"gold_spin":0,"guess_num":0,"house":None,"car":None,"business":None,"staking":0,"vip_daily":0,"clan_war_cd":0,"job":None,"job_time":0,"married":None,"energy":100,"last_energy":0,"quiz_score":0,"roulette_cd":0,"blackjack_cd":0}
        save()
    defaults = {"money":500,"level":1,"xp":0,"vip":False,"vip_until":0,"weapons":[],"daily":0,"spin":0,"gift":0,"streak":0,"score":0,"codes":[],"items":[],"portfolio":{},"bank":0,"bank_current":0,"bank_saving":0,"bank_history":[],"certificates":[],"credit_limit":5000,"credit_used":0,"iban":"","overdraft":0,"steal":0,"lottery_tickets":0,"loans":[],"invest":0,"gold_box":0,"last_challenge":0,"pets":[],"clan":None,"wins":0,"losses":0,"gold_spin":0,"guess_num":0,"name":"مستخدم","house":None,"car":None,"business":None,"staking":0,"vip_daily":0,"clan_war_cd":0,"job":None,"job_time":0,"married":None,"energy":100,"last_energy":0,"quiz_score":0,"roulette_cd":0,"blackjack_cd":0}
    for k,v in defaults.items():
        if k not in data[uid]: data[uid][k]=v
    if data[uid].get("vip_until",0) and time.time() > data[uid]["vip_until"] and data[uid]["vip_until"]!=0:
        data[uid]["vip"]=False; data[uid]["vip_until"]=0
    return data[uid]
def is_owner(uid): return int(uid)==OWNER_ID
def is_banned(uid): return str(uid) in settings.get("banned",[])
def is_vip(u): return u.get("vip",False)
def add(uid, amount):
    u=user(uid); mult = 3 if is_vip(u) else 1; amount = amount * mult
    u["money"]+=amount; u["xp"]+=amount//5; u["score"]+=amount
    if u.get("loans"):
        now2 = int(time.time())
        for ln in u.get("loans",[]):
            days2 = (now2 - ln.get("time", now2)) // 86400
            if days2 >= 3 and u["money"] > 0:
                cut = min(int(amount * 0.50), u["money"])
                if cut>0:
                    u["money"] -= cut; ln["amount"] = max(0, ln["amount"] - cut)
                    try: bot.send_message(uid, f"🏦 البنك خصم {cut} غصب عشان القرض متأخر {days2} يوم!")
                    except: pass
                break
    lvl=u["xp"]//100+1
    if lvl>u["level"]:
        u["level"]=lvl; bonus=lvl*200; u["money"]+=bonus
        try: bot.send_message(uid, f"🎉 مستوى جديد! وصلت {lvl} 🔥\n🎁 هدية: +{bonus}")
        except: pass
    save(); return amount
def get_rank(money):
    if money >= 1000000: return "👑 إمبراطور الكون"
    if money >= 500000: return "👑 إمبراطور"
    if money >= 200000: return "💎 ملياردير"
    if money >= 100000: return "🏆 مليونير"
    if money >= 50000: return "💰 غني جدا"
    if money >= 20000: return "🤑 غني"
    if money >= 5000: return "🙂 متوسط"
    if money >= 1000: return "🌱 عادي"
    return "🥺 فقير"
def add_history(uid_str, text):
    uu = user(int(uid_str)); h = uu.get("bank_history", [])
    h.append(f"{time.strftime('%d/%m %H:%M')} - {text}"); uu["bank_history"] = h[-20:]; save()
def check_loan_penalty(u):
    loans = u.get("loans", [])
    if not loans: return None
    now = int(time.time()); msg=None
    for ln in loans:
        days = (now - ln.get("time", now)) // 86400
        if days >= 7: msg="🔒 محظور"
        elif days >= 3: msg="🚨 متأخر 3 أيام"
        elif days >= 1: msg="⏰ متأخر يوم"
    return msg
def get_loan_pay_amount(ln):
    now = int(time.time()); days = (now - ln.get("time", now)) // 86400
    if days >= 7: rate=0.50
    elif days >= 3: rate=0.30
    elif days >= 1: rate=0.20
    else: rate=0.10
    return int(ln["amount"]*(1+rate)), rate, days
def portfolio_value(u): return sum(qty*MARKET[k]["price"] for k,qty in u.get("portfolio",{}).items() if k in MARKET)
def power(u): return sum(WEAPONS[w][2] for w in u.get("weapons",[]) if w in WEAPONS) + sum(PETS[p][2] for p in u.get("pets",[]) if p in PETS)
def pet_income(u): return sum(PETS[p][2] for p in u.get("pets",[]) if p in PETS)
def daily_income(u):
    total = pet_income(u)
    if u.get("house") in HOUSES: total += HOUSES[u["house"]][2]
    if u.get("car") in CARS: total += CARS[u["car"]][2]
    if u.get("business") in BUSINESS: total += BUSINESS[u["business"]][2]
    if u.get("job"): total += 500
    return total
def lvl_emoji(l):
    if l>=20: return "👑"
    if l>=15: return "💎"
    if l>=10: return "⭐"
    if l>=5: return "🌟"
    return "🌱"
def total_wealth(u): return u["money"]+portfolio_value(u)+u.get("bank",0)+u.get("bank_current",0)+u.get("bank_saving",0)+u.get("invest",0)+sum(c["amount"] for c in u.get("certificates",[]))+u.get("staking",0)
JOBS = {"doctor":("👨‍⚕️ دكتور",2000),"engineer":("👨‍💻 مهندس",1500),"teacher":("👨‍🏫 مدرس",1000),"police":("👮 شرطة",1200),"chef":("👨‍🍳 طباخ",800),"driver":("🚕 سواق",600),"singer":("🎤 مغني",3000),"football":("⚽ لاعب كورة",5000)}

# ===== الانظمة الجديدة المدمجة - 700 سطر =====
def get_energy(uid):
    u = user(uid); now = int(time.time()); passed = (now - u.get("last_energy", now)) // 60
    if passed > 0:
        u["energy"] = min(100, u.get("energy", 100) + passed); u["last_energy"] = now; save()
    return u.get("energy", 100)
def use_energy(uid, amount):
    u = user(uid)
    if u.get("energy", 100) < amount: return False
    u["energy"] -= amount; u["last_energy"] = int(time.time()); save(); return True
LUCKY_NUMBERS = {}
def get_lucky_number(uid):
    today = datetime.date.today().isoformat()
    if uid not in LUCKY_NUMBERS or LUCKY_NUMBERS[uid].get("date") != today:
        LUCKY_NUMBERS[uid] = {"date": today, "num": random.randint(1, 100)}
    return LUCKY_NUMBERS[uid]["num"]
def get_daily_shop():
    today = datetime.date.today().isoformat(); random.seed(today); items=[]
    for i in range(5):
        kind = random.choice(["weapon", "pet", "house", "car"])
        if kind == "weapon":
            k = random.choice(list(WEAPONS.keys())); items.append((WEAPONS[k][0], WEAPONS[k][1] // 2, k, "weapon"))
        elif kind == "pet":
            k = random.choice(list(PETS.keys())); items.append((PETS[k][0], PETS[k][1] // 2, k, "pet"))
        elif kind == "house":
            k = random.choice(list(HOUSES.keys())); items.append((HOUSES[k][0], HOUSES[k][1] // 2, k, "house"))
        else:
            k = random.choice(list(CARS.keys())); items.append((CARS[k][0], CARS[k][1] // 2, k, "car"))
    random.seed(); return items
def auto_bank_interest():
    while True:
        time.sleep(3600)
        try:
            for uid_str, u in list(data.items()):
                saving = u.get("bank_saving", 0)
                if saving > 0:
                    profit = int(saving * 0.05)
                    if profit > 0:
                        u["bank_saving"] += profit
                        try: bot.send_message(int(uid_str), f"🏦 فايدة تلقائية +{profit} على التوفير!")
                        except: pass
            save()
        except: pass
Thread(target=auto_bank_interest, daemon=True).start()
def auto_daily_gift():
    while True:
        time.sleep(86400)
        try:
            for uid_str in list(data.keys()):
                try:
                    u = user(int(uid_str)); u["money"] += 200; bot.send_message(int(uid_str), "🎁 هدية يومية تلقائية +200!")
                except: pass
            save()
        except: pass
Thread(target=auto_daily_gift, daemon=True).start()
WEEKLY_CHALLENGES = [("اجمع 10000 جنيه", 10000, 5000),("اكسب 5 مرات PvP", 5, 10000),("اشتري 3 حيوانات", 3, 3000),("اعمل 10 تداولات", 10, 5000),("اكسب في الكازينو 3 مرات", 3, 8000),("وصل مستوى 10", 10, 15000),("اجمع دخل 5000", 5000, 5000),("اشتري بيت", 1, 20000),("اتجوز", 1, 10000),("اعمل كلان", 1, 5000)]
RANKS = [(0, "🥺 فقير"),(1000, "🌱 عادي"),(5000, "🙂 متوسط"),(20000, "🤑 غني"),(50000, "💰 غني جدا"),(100000, "🏆 مليونير"),(200000, "💎 ملياردير"),(500000, "👑 إمبراطور"),(1000000, "👑 إمبراطور الكون"),(5000000, "🌌 أسطورة الكون"),(10000000, "🔥 إله اللعبة")]
def get_new_rank(money):
    rank = RANKS[0][1]
    for need, name in RANKS:
        if money >= need: rank = name
    return rank
def random_event(uid):
    events = [("🎉 لقيت 500 جنيه في الشارع!", 500),("💸 وقعت منك 200 جنيه!", -200),("🎁 صاحبك اداك 1000!", 1000),("🚨 البوليس خد منك 300 غرامة!", -300),("💎 لقيت الماس بـ 2000!", 2000),("🐶 كلب عضك ودفعت 100 علاج!", -100),("🏆 كسبت مسابقة +800!", 800),("📱 موبايلك اتكسر ودفعت 500!", -500)]
    txt, amount = random.choice(events); u = user(uid); u["money"] = max(0, u["money"] + amount); save(); return txt, amount
def auto_random_events():
    while True:
        time.sleep(1800)
        try:
            for uid_str in list(data.keys()):
                if random.random() < 0.3:
                    try:
                        txt, amt = random_event(int(uid_str)); bot.send_message(int(uid_str), f"🎲 حدث عشوائي!\n{txt}")
                    except: pass
        except: pass
Thread(target=auto_random_events, daemon=True).start()
BLACK_MARKET = {"bm1": ("💎 الماس مسروق", 5000, 10000),"bm2": ("🔫 سلاح نادر", 8000, 15000),"bm3": ("🐉 تنين أسود", 15000, 30000),"bm4": ("🏰 قصر مهجور", 50000, 100000),"bm5": ("🚀 صاروخ", 100000, 200000)}
def auto_auction():
    while True:
        time.sleep(7200)
        try:
            if len(settings.get("auction", [])) < 3:
                w = random.choice(list(WEAPONS.keys())); settings.setdefault("auction", []).append({"weapon": w,"name": WEAPONS[w][0] + " (نادر)","price": WEAPONS[w][1] * 2,"seller": "0","seller_name": "السوق"}); save_settings()
        except: pass
Thread(target=auto_auction, daemon=True).start()
def auto_backup():
    while True:
        time.sleep(3600)
        try: save(); save_settings(); print(f"✅ Backup {time.strftime('%H:%M:%S')}")
        except: pass
Thread(target=auto_backup, daemon=True).start()
def get_user_stats(uid):
    u = user(uid); total = total_wealth(u)
    return {"money": u["money"],"bank": u.get("bank_saving",0)+u.get("bank_current",0),"portfolio": portfolio_value(u),"total": total,"level": u["level"],"power": power(u),"rank": get_new_rank(total),"daily_income": daily_income(u)}
def streak_bonus(uid):
    s = user(uid).get("streak",0)
    if s>=30: return 10000
    if s>=14: return 5000
    if s>=7: return 2000
    if s>=3: return 500
    return 100
def notify_all(msg_text):
    c=0
    for uid_str in list(data.keys()):
        try: bot.send_message(int(uid_str), msg_text); c+=1
        except: pass
    return c

def menu(uid):
    m=InlineKeyboardMarkup(row_width=2)
    m.add(InlineKeyboardButton("🎮 العب واكسب", callback_data="play"),InlineKeyboardButton("📈 تداول 50 عملة", callback_data="trade"),InlineKeyboardButton("🏦 البنك الحقيقي", callback_data="bank"),InlineKeyboardButton("💎 استثمار", callback_data="invest"),InlineKeyboardButton("🐉 حيوانات 100", callback_data="pets"),InlineKeyboardButton("⚔️ قتال PvP", callback_data="pvp"),InlineKeyboardButton("👑 كلان", callback_data="clan"),InlineKeyboardButton("🏛️ مزاد", callback_data="auction"),InlineKeyboardButton("🏠 عقارات 100", callback_data="assets"),InlineKeyboardButton("🏪 مشروعي 100", callback_data="my_business"),InlineKeyboardButton("💼 شغلي", callback_data="job"),InlineKeyboardButton("💍 جواز", callback_data="marry"),InlineKeyboardButton("🛒 المتجر 100 سلاح", callback_data="shop"),InlineKeyboardButton("👤 بروفايلي", callback_data="me"),InlineKeyboardButton("🏆 الأبطال", callback_data="top"),InlineKeyboardButton("🎰 كازينو 10 ألعاب", callback_data="casino"),InlineKeyboardButton("🎯 تحدي اليوم", callback_data="challenge"),InlineKeyboardButton("🎡 عجلة ذهبية", callback_data="goldspin"),InlineKeyboardButton("🧧 ظرف أحمر", callback_data="red"),InlineKeyboardButton("💰 فلوسي", callback_data="balance"))
    if is_owner(uid): m.add(InlineKeyboardButton("👑 لوحة الأونر 🔥🔥", callback_data="owner"))
    m.add(InlineKeyboardButton("🔄 تحديث", callback_data="home")); return m
def play_menu(uid):
    m=InlineKeyboardMarkup(row_width=2)
    m.add(InlineKeyboardButton("📋 المهام 500", callback_data="tasks"),InlineKeyboardButton("🎡 عجلة الحظ", callback_data="spin"),InlineKeyboardButton("🎲 لعبة الحظ", callback_data="gamble"),InlineKeyboardButton("🎁 صندوق", callback_data="gift"),InlineKeyboardButton("📦 صندوق ذهبي", callback_data="goldbox"),InlineKeyboardButton("🔢 خمن الرقم", callback_data="guess"),InlineKeyboardButton("📅 يومية", callback_data="daily"),InlineKeyboardButton("🎁 أكواد 100", callback_data="codes"),InlineKeyboardButton("🏆 مسابقة", callback_data="contest"),InlineKeyboardButton("🥷 سرقة", callback_data="steal"),InlineKeyboardButton("🎯 مهمة سرية", callback_data="secret"),InlineKeyboardButton("💸 قروض 5", callback_data="loan"),InlineKeyboardButton("🏠 قرض عقاري", callback_data="mortgage"),InlineKeyboardButton("🚗 تمويل سيارة", callback_data="car_loan"),InlineKeyboardButton("🎰 روليت", callback_data="roulette"),InlineKeyboardButton("🃏 بلاك جاك", callback_data="blackjack"),InlineKeyboardButton("🧠 كويز", callback_data="quiz"),InlineKeyboardButton("🎲 نرد حظ", callback_data="dice_game"),InlineKeyboardButton("💰 اجمع دخلي", callback_data="collect_all"),InlineKeyboardButton("🎁 هدية VIP", callback_data="vip_daily"),InlineKeyboardButton("🔥 سلسلة", callback_data="streak"))
    m.add(InlineKeyboardButton("🔙 رجوع", callback_data="home")); return m
def casino_menu(uid):
    m=InlineKeyboardMarkup(row_width=2)
    m.add(InlineKeyboardButton("🎰 سلوت", callback_data="slot"),InlineKeyboardButton("🎲 نرد", callback_data="dice"),InlineKeyboardButton("🃏 ورق", callback_data="cards"),InlineKeyboardButton("💎 يانصيب", callback_data="lottery"))
    m.add(InlineKeyboardButton("🎡 روليت", callback_data="roulette"),InlineKeyboardButton("🃏 بلاك جاك", callback_data="blackjack"),InlineKeyboardButton("🪙 ملك وكتابة", callback_data="gamble"),InlineKeyboardButton("🎯 تخمين", callback_data="guess"))
    m.add(InlineKeyboardButton("🔙 رجوع", callback_data="home")); return m
def shop_menu(uid):
    m=InlineKeyboardMarkup(); m.add(InlineKeyboardButton("🔫 أسلحة 100", callback_data="weapons")); m.add(InlineKeyboardButton("🐉 حيوانات 100", callback_data="petshop")); m.add(InlineKeyboardButton("👑 VIP - 1000 (×3)", callback_data="vip")); m.add(InlineKeyboardButton("🔙 رجوع", callback_data="home")); return m
def trade_menu(uid):
    u=user(uid); m=InlineKeyboardMarkup()
    for k,v in list(MARKET.items())[:15]:
        qty=u.get("portfolio",{}).get(k,0); m.add(InlineKeyboardButton(f"{v['name']} - {v['price']} | {qty}", callback_data=f"coin_{k}"))
    m.add(InlineKeyboardButton("➡️ صفحة تانية", callback_data="trade2")); m.add(InlineKeyboardButton("🪙 ستيكينج 100%", callback_data="staking")); m.add(InlineKeyboardButton("💼 محفظتي", callback_data="my_portfolio")); m.add(InlineKeyboardButton("🔙 رجوع", callback_data="home")); return m
def owner_menu():
    m=InlineKeyboardMarkup(row_width=2)
    m.add(InlineKeyboardButton("👥 المستخدمين", callback_data="a_users"),InlineKeyboardButton("📊 احصائيات", callback_data="a_stats"),InlineKeyboardButton("💰 مبلغ مخصوص لحد", callback_data="a_custom"),InlineKeyboardButton("💰 مبلغ مخصوص للكل", callback_data="a_custom_all"),InlineKeyboardButton("📢 بث", callback_data="a_bc"),InlineKeyboardButton("🎁 هدية للكل", callback_data="a_gift_all"),InlineKeyboardButton("🔍 بحث ID", callback_data="a_search"),InlineKeyboardButton("🛠️ صيانة", callback_data="a_maint"),InlineKeyboardButton("🏆 انهي المسابقة", callback_data="a_end"),InlineKeyboardButton("💰 ادي الكل", callback_data="a_all_money"),InlineKeyboardButton("🎰 سحب يانصيب", callback_data="a_lottery_draw"),InlineKeyboardButton("💥 انفجار", callback_data="a_pump"),InlineKeyboardButton("📉 انهيار", callback_data="a_crash"),InlineKeyboardButton("👑 VIP للكل", callback_data="a_vip_all"),InlineKeyboardButton("🐉 حيوان للكل", callback_data="a_pet_all"),InlineKeyboardButton("🏠 بيت للكل", callback_data="a_house_all"),InlineKeyboardButton("🚗 عربية للكل", callback_data="a_car_all"),InlineKeyboardButton("🎯 تحدي جديد", callback_data="a_new_challenge"),InlineKeyboardButton("🧹 فك حظر الكل", callback_data="a_clear_ban"),InlineKeyboardButton("💎 فلوس لنفسك", callback_data="a_self"),InlineKeyboardButton("🏆 بطولة أسبوعية", callback_data="a_weekly"),InlineKeyboardButton("💥 تصفير الكل", callback_data="reset_all"))
    m.add(InlineKeyboardButton("🔙 رجوع", callback_data="home")); return m

@bot.message_handler(commands=['start'])
def start(msg):
    if settings.get("maintenance") and not is_owner(msg.from_user.id): bot.send_message(msg.chat.id, "🛠️ صيانة"); return
    if is_banned(msg.from_user.id): bot.send_message(msg.chat.id, "🚫 محظور"); return
    u=user(msg.from_user.id); u["name"]=msg.from_user.first_name or "مستخدم"
    if not u.get("iban"): u["iban"]=f"EG{random.randint(1000,9999)}{msg.from_user.id}{random.randint(100,999)}"; save()
    if len(msg.text.split())>1:
        inv=msg.text.split()[1]
        if inv!=str(msg.from_user.id) and inv in data:
            add(int(inv),150)
            try: bot.send_message(int(inv), "🎉 صاحبك دخل! +150 🔥")
            except: pass
    inc = daily_income(u)
    if inc>0:
        u["money"]+=inc
        try: bot.send_message(msg.chat.id, f"💰 دخلك اليومي +{inc} 🔥")
        except: pass
    save(); vip=" 👑 VIP ×3" if is_vip(u) else ""; rank=get_rank(total_wealth(u))
    bot.send_message(msg.chat.id, f"┏━━━━━━━━━━━━━━┓\n┃ 🎮 أهلاً {u['name']}{vip}\n┃ {rank}\n┃ 💰 {u['money']} جنيه\n┃ 🏦 جاري {u.get('bank_current',0)} | توفير {u.get('bank_saving',0)}\n┃ 🏧 IBAN: {u.get('iban')}\n┃ {lvl_emoji(u['level'])} مستوى {u['level']} | ⭐ {u['xp']} XP\n┃ ⚡ قوة +{power(u)}\n┃ 💰 دخلك اليومي +{daily_income(u)}\n┃ 📈 ثروتك {total_wealth(u)}\n┃ 🎮 100 سلاح | 100 حيوان | 500 مهمة | 50 عملة\n┗━━━━━━━━━━━━━━┛\n\nاختار 👇", reply_markup=menu(msg.from_user.id))

@bot.message_handler(commands=['give','take','giveall','takeall','money','ping','id','rank','owner','admin'])
def owner_cmd(msg):
    txt = msg.text.split(); cmd = txt[0].replace("/","")
    if cmd=="ping": bot.send_message(msg.chat.id, "✅ شغال مدمج 1000+ سطر!"); return
    if cmd=="id": bot.send_message(msg.chat.id, f"🆔 ID: `{msg.from_user.id}`", parse_mode="Markdown"); return
    if cmd=="rank":
        u=user(msg.from_user.id); bot.send_message(msg.chat.id, f"👑 {get_rank(total_wealth(u))} ثروتك {total_wealth(u)}"); return
    if not is_owner(msg.from_user.id): bot.send_message(msg.chat.id, "❌ مش الأونر"); return
    if cmd=="money":
        amt = int(txt[1]) if len(txt)>1 and txt[1].isdigit() else 100000; u=user(msg.from_user.id); u["money"]+=amt; save(); bot.send_message(msg.chat.id, f"💰 +{amt}"); return
    if cmd=="give":
        if len(txt)<3: bot.send_message(msg.chat.id, "❌ `/give ID المبلغ`", parse_mode="Markdown"); return
        tid, amt = txt[1], txt[2]
        if not amt.isdigit(): bot.send_message(msg.chat.id, "❌ المبلغ رقم"); return
        amt=int(amt)
        if tid not in data: bot.send_message(msg.chat.id, "❌ مفيش حد"); return
        target=user(int(tid)); target["money"]+=amt; save(); bot.send_message(msg.chat.id, f"✅ اديت {target.get('name')} +{amt}")
        try: bot.send_message(int(tid), f"🎁 الأونر اداك +{amt} 🔥")
        except: pass
        return
    if cmd=="take":
        if len(txt)<3: bot.send_message(msg.chat.id, "❌ `/take ID المبلغ`", parse_mode="Markdown"); return
        tid, amt = txt[1], txt[2]
        if not amt.isdigit(): bot.send_message(msg.chat.id, "❌ المبلغ رقم"); return
        amt=int(amt)
        if tid not in data: bot.send_message(msg.chat.id, "❌ مفيش حد"); return
        target=user(int(tid)); target["money"]=max(0, target["money"]-amt); save(); bot.send_message(msg.chat.id, f"✅ سحبت -{amt}"); return
    if cmd=="giveall":
        if len(txt)<2 or not txt[1].isdigit(): bot.send_message(msg.chat.id, "❌ `/giveall المبلغ`", parse_mode="Markdown"); return
        amt=int(txt[1])
        for k in data: data[k]["money"]+=amt
        save(); bot.send_message(msg.chat.id, f"✅ اديت {amt} للكل"); return
    if cmd=="takeall":
        if len(txt)<2 or not txt[1].isdigit(): bot.send_message(msg.chat.id, "❌ `/takeall المبلغ`", parse_mode="Markdown"); return
        amt=int(txt[1])
        for k in data: data[k]["money"]=max(0, data[k]["money"]-amt)
        save(); bot.send_message(msg.chat.id, f"✅ سحبت {amt} من الكل"); return
    if cmd in ["owner","admin"]: bot.send_message(msg.chat.id, "👑 لوحة الأونر", reply_markup=owner_menu()); return

@bot.message_handler(func=lambda m: m.text and is_owner(m.from_user.id))
def owner_text(msg):
    uid = msg.from_user.id; txt = msg.text.strip()
    if uid in pending:
        p = pending[uid]
        if p.get("action")=="wait_transfer_id":
            if txt not in data: bot.send_message(msg.chat.id, "❌ مفيش حد"); return
            pending[uid]={"action":"wait_transfer_amt", "target":txt}; bot.send_message(msg.chat.id, f"✅ هتحول لـ {data[txt].get('name')} اكتب المبلغ"); return
        if p.get("action")=="wait_transfer_amt":
            if not txt.isdigit(): bot.send_message(msg.chat.id, "❌ اكتب رقم"); return
            amt=int(txt); tid=p["target"]; uu=user(uid); fee=5
            if uu["money"]<amt+fee: bot.send_message(msg.chat.id, f"❌ محتاج {amt+fee}"); return
            uu["money"]-=amt+fee; target=user(int(tid)); target["money"]+=amt; save(); del pending[uid]; bot.send_message(msg.chat.id, f"✅ حولت {amt}"); return
        if txt.isdigit():
            amt = int(txt)
            if amt <= 0 or amt > 100000000: bot.send_message(msg.chat.id, "❌ اكتب رقم بين 1 و 100 مليون"); return
            if p["action"] == "custom_all":
                for k in data: data[k]["money"]+=amt
                save(); del pending[uid]; bot.send_message(msg.chat.id, f"✅ اديت {amt} للكل", reply_markup=owner_menu()); return
            if p["action"] == "custom_one":
                tid = p["target"]
                if tid not in data: del pending[uid]; bot.send_message(msg.chat.id, "❌ مش موجود"); return
                target=user(int(tid)); target["money"]+=amt; save(); del pending[uid]; bot.send_message(msg.chat.id, f"✅ اديت {target.get('name')} +{amt}", reply_markup=owner_menu()); return
            if p["action"] == "custom_take":
                tid = p["target"]; target=user(int(tid)); target["money"]=max(0, target["money"]-amt); save(); del pending[uid]; bot.send_message(msg.chat.id, f"✅ سحبت -{amt}", reply_markup=owner_menu()); return
            if p["action"] == "custom_bank":
                tid = p["target"]; target=user(int(tid)); target["bank_saving"]=target.get("bank_saving",0)+amt; save(); del pending[uid]; bot.send_message(msg.chat.id, f"✅ حطيت {amt} في التوفير", reply_markup=owner_menu()); return
        if p["action"] == "wait_id" and txt.isdigit():
            if txt not in data: bot.send_message(msg.chat.id, "❌ مفيش حد"); return
            pending[uid] = {"target": txt, "action": "custom_one"}; bot.send_message(msg.chat.id, f"✅ لقيت {data[txt].get('name')} اكتب المبلغ"); return
        bot.send_message(msg.chat.id, "❌ اكتب رقم بس"); return
    if txt.isdigit() and txt in data:
        tid = txt; info=user(int(tid))
        m=InlineKeyboardMarkup(row_width=3)
        m.add(InlineKeyboardButton("💰 مبلغ ➕", callback_data=f"custom_{tid}"), InlineKeyboardButton("💸 اسحب ➖", callback_data=f"ctake_{tid}"))
        m.add(InlineKeyboardButton("➕1000", callback_data=f"add_{tid}_1000"), InlineKeyboardButton("➕10000", callback_data=f"add_{tid}_10000"), InlineKeyboardButton("💎 1M", callback_data=f"add_{tid}_1000000"))
        m.add(InlineKeyboardButton("💥 تصفير", callback_data=f"zero_{tid}"), InlineKeyboardButton("👑 VIP", callback_data=f"gv_{tid}"), InlineKeyboardButton("🚫 حظر", callback_data=f"ban_{tid}"))
        m.add(InlineKeyboardButton("✅ فك حظر", callback_data=f"unban_{tid}"), InlineKeyboardButton("🐉 تنين", callback_data=f"givepet_{tid}_pet1"), InlineKeyboardButton("🙏 سامحه قروض", callback_data=f"forgive_{tid}"))
        m.add(InlineKeyboardButton("🔙 لوحة", callback_data="owner"))
        bot.send_message(msg.chat.id, f"👤 {info.get('name')}\n🆔 {tid}\n💰 {info['money']}\n🏦 توفير {info.get('bank_saving',0)}", reply_markup=m); return

@bot.callback_query_handler(func=lambda c: True)
def btn(call):
    uid=call.from_user.id; u=user(uid); cid=call.message.chat.id; d=call.data
    try: bot.answer_callback_query(call.id)
    except: pass
    try:
        if settings.get("maintenance") and not is_owner(uid) and d not in ["home"]: bot.send_message(cid, "🛠️ صيانة"); return
        if is_banned(uid) and not is_owner(uid): bot.send_message(cid, "🚫 محظور"); return
        if d in ["bank","casino","slot","dice","cards"] and check_loan_penalty(u) == "🔒 محظور": bot.send_message(cid, "🔒 محظور! سدد القرض", reply_markup=menu(uid)); return
        if d=="home": bot.send_message(cid, f"🏠 الرئيسية 💰 {u['money']} | مستوى {u['level']}", reply_markup=menu(uid)); return
        if d=="balance": bot.send_message(cid, f"💰 ثروتك {total_wealth(u)}\n💵 كاش {u['money']}\n🏦 جاري {u.get('bank_current',0)} توفير {u.get('bank_saving',0)}\n📈 محفظة {portfolio_value(u)}\n💰 دخل يومي +{daily_income(u)}\n👑 {get_rank(total_wealth(u))}\n⚡ طاقتك {get_energy(uid)}/100", reply_markup=menu(uid)); return
        if d=="play": bot.send_message(cid, f"🎮 العب 💰 {u['money']}", reply_markup=play_menu(uid)); return
        if d=="casino": bot.send_message(cid, f"🎰 كازينو جاكبوت {settings.get('jackpot',10000)}", reply_markup=casino_menu(uid)); return
        if d=="shop": bot.send_message(cid, f"🛒 المتجر 💰 {u['money']}", reply_markup=shop_menu(uid)); return
        if d=="me":
            st=get_user_stats(uid); bot.send_message(cid, f"👤 {u['name']} 🆔 {uid}\n💰 {u['money']} 🏦 {st['bank']} 📈 {st['portfolio']} 💰 ثروة {st['total']}\n⭐ مستوى {u['level']} ⚡ قوة {st['power']} 🐉 {st['pets']} 🔫 {st['weapons']}\n💼 شغل {JOBS[u['job']][0] if u.get('job') in JOBS else 'مفيش'} 💍 {u.get('married') or 'لا'}\n👑 {'✅ ×3' if is_vip(u) else '❌'}", reply_markup=menu(uid)); return
        if d=="top":
            top=sorted(data.items(), key=lambda x: total_wealth(x[1]), reverse=True)[:10]; txt="🏆 الأبطال\n"
            for i,(k,v) in enumerate(top): txt+=f"{i+1}. {v.get('name')} - {total_wealth(v)}\n"
            bot.send_message(cid, txt, reply_markup=menu(uid)); return
        if d=="collect_all":
            inc=daily_income(u)
            if inc==0: bot.send_message(cid, "❌ معندكش دخل", reply_markup=menu(uid)); return
            u["money"]+=inc; save(); bot.send_message(cid, f"💰 جمعت +{inc}", reply_markup=menu(uid)); return
        if d=="vip_daily":
            if not is_vip(u): bot.send_message(cid, "❌ VIP بس", reply_markup=menu(uid)); return
            today=datetime.date.today().isoformat()
            if u.get("vip_daily")==today: bot.send_message(cid, "❌ خدتها النهاردة", reply_markup=menu(uid)); return
            u["vip_daily"]=today; u["money"]+=5000; save(); bot.send_message(cid, "🎁 VIP +5000", reply_markup=menu(uid)); return
        if d=="job":
            if u.get("job") in JOBS:
                m=InlineKeyboardMarkup(); m.add(InlineKeyboardButton("💰 اقبض", callback_data="job_pay")); m.add(InlineKeyboardButton("🚪 استقيل", callback_data="job_quit")); m.add(InlineKeyboardButton("🔙", callback_data="home")); bot.send_message(cid, f"💼 {JOBS[u['job']][0]} مرتب {JOBS[u['job']][1]}", reply_markup=m); return
            m=InlineKeyboardMarkup()
            for k,(name,sal) in JOBS.items(): m.add(InlineKeyboardButton(f"{name} - {sal}", callback_data=f"takejob_{k}"))
            m.add(InlineKeyboardButton("🔙", callback_data="home")); bot.send_message(cid, "💼 اختار شغل:", reply_markup=m); return
        if d.startswith("takejob_"):
            k=d.replace("takejob_",""); u["job"]=k; save(); bot.send_message(cid, f"🎉 اشتغلت {JOBS[k][0]}!", reply_markup=menu(uid)); return
        if d=="job_pay":
            if not u.get("job"): bot.send_message(cid, "❌ معندكش شغل", reply_markup=menu(uid)); return
            got=add(uid, JOBS[u["job"]][1]); bot.send_message(cid, f"💰 قبضت +{got}", reply_markup=menu(uid)); return
        if d=="job_quit": u["job"]=None; save(); bot.send_message(cid, "🚪 استقلت", reply_markup=menu(uid)); return
        if d=="marry":
            others=[(k,v) for k,v in data.items() if k!=str(uid)][:10]; m=InlineKeyboardMarkup()
            for k,v in others: m.add(InlineKeyboardButton(f"💍 {v.get('name')}", callback_data=f"marry_{k}"))
            m.add(InlineKeyboardButton("💔 طلق", callback_data="divorce")); m.add(InlineKeyboardButton("🔙", callback_data="home")); bot.send_message(cid, f"💍 متجوز: {u.get('married') or 'لا'} +5000 مهر!", reply_markup=m); return
        if d.startswith("marry_"):
            tid=d.replace("marry_",""); target=user(int(tid)); u["married"]=target.get("name"); target["married"]=u["name"]; u["money"]+=5000; target["money"]+=5000; save(); bot.send_message(cid, f"💍 اتجوزت {target.get('name')}! +5000", reply_markup=menu(uid)); return
        if d=="divorce": u["married"]=None; save(); bot.send_message(cid, "💔 طلقت", reply_markup=menu(uid)); return
        if d=="assets":
            m=InlineKeyboardMarkup(); m.add(InlineKeyboardButton("🏠 بيت", callback_data="buy_house")); m.add(InlineKeyboardButton("🚗 عربية", callback_data="buy_car")); m.add(InlineKeyboardButton("🏪 مشروع", callback_data="my_business")); m.add(InlineKeyboardButton("🔙", callback_data="home")); bot.send_message(cid, f"🏠 عقارات 💰 {u['money']} دخل +{daily_income(u)}", reply_markup=m); return
        if d=="buy_house":
            m=InlineKeyboardMarkup()
            for k in list(HOUSES.keys())[:10]: m.add(InlineKeyboardButton(f"{HOUSES[k][0]} +{HOUSES[k][2]}/يوم - {HOUSES[k][1]}", callback_data=f"bh_{k}"))
            m.add(InlineKeyboardButton("🔙", callback_data="assets")); bot.send_message(cid, "🏠 بيوت", reply_markup=m); return
        if d.startswith("bh_"):
            k=d.replace("bh_",""); name,price,inc=HOUSES[k]
            if u["money"]<price: bot.send_message(cid, "❌ فلوسك مش كفاية", reply_markup=menu(uid)); return
            u["money"]-=price; u["house"]=k; save(); bot.send_message(cid, f"🎉 اشتريت {name} +{inc}/يوم", reply_markup=menu(uid)); return
        if d=="buy_car":
            m=InlineKeyboardMarkup()
            for k in list(CARS.keys())[:10]: m.add(InlineKeyboardButton(f"{CARS[k][0]} +{CARS[k][2]}/يوم - {CARS[k][1]}", callback_data=f"bc_{k}"))
            m.add(InlineKeyboardButton("🔙", callback_data="assets")); bot.send_message(cid, "🚗 عربيات", reply_markup=m); return
        if d.startswith("bc_"):
            k=d.replace("bc_",""); name,price,inc=CARS[k]
            if u["money"]<price: bot.send_message(cid, "❌ فلوسك مش كفاية", reply_markup=menu(uid)); return
            u["money"]-=price; u["car"]=k; save(); bot.send_message(cid, f"🎉 اشتريت {name}", reply_markup=menu(uid)); return
        if d=="my_business":
            m=InlineKeyboardMarkup()
            for k in list(BUSINESS.keys())[:10]: m.add(InlineKeyboardButton(f"{BUSINESS[k][0]} +{BUSINESS[k][2]}/يوم - {BUSINESS[k][1]}", callback_data=f"bb_{k}"))
            m.add(InlineKeyboardButton("🔙", callback_data="home")); bot.send_message(cid, "🏪 مشاريع", reply_markup=m); return
        if d.startswith("bb_"):
            k=d.replace("bb_",""); name,price,inc=BUSINESS[k]
            if u["money"]<price: bot.send_message(cid, "❌ فلوسك مش كفاية", reply_markup=menu(uid)); return
            u["money"]-=price; u["business"]=k; save(); bot.send_message(cid, f"🎉 فتحت {name}", reply_markup=menu(uid)); return
        if d=="mortgage":
            if u.get("house"): bot.send_message(cid, "عندك بيت", reply_markup=menu(uid)); return
            m=InlineKeyboardMarkup(); m.add(InlineKeyboardButton("🏠 قرض 200000 - فيلا", callback_data="take_mortgage")); m.add(InlineKeyboardButton("🔙", callback_data="play")); bot.send_message(cid, "🏠 قرض عقاري 200000 فيلا +1500/يوم", reply_markup=m); return
        if d=="take_mortgage": u["house"]="h10"; u["loans"]=u.get("loans",[])+[{"amount":200000,"time":int(time.time())}]; save(); bot.send_message(cid, "🎉 خدت فيلا +1500/يوم", reply_markup=menu(uid)); return
        if d=="car_loan":
            if u.get("car"): bot.send_message(cid, "عندك عربية", reply_markup=menu(uid)); return
            m=InlineKeyboardMarkup(); m.add(InlineKeyboardButton("🚕 تاكسي 20000", callback_data="take_carloan")); m.add(InlineKeyboardButton("🔙", callback_data="play")); bot.send_message(cid, "🚗 تاكسي +300/يوم", reply_markup=m); return
        if d=="take_carloan": u["car"]="c1"; u["loans"]=u.get("loans",[])+[{"amount":20000,"time":int(time.time())}]; save(); bot.send_message(cid, "🎉 خدت تاكسي", reply_markup=menu(uid)); return
        if d=="pets":
            pets=", ".join([PETS[x][0] for x in u.get("pets",[])[:5] if x in PETS]) or "مفيش"; m=InlineKeyboardMarkup(); m.add(InlineKeyboardButton("🛒 اشتري", callback_data="petshop")); m.add(InlineKeyboardButton("💰 اجمع", callback_data="collect_pet")); m.add(InlineKeyboardButton("🔙", callback_data="home")); bot.send_message(cid, f"🐉 {pets} دخل +{pet_income(u)}", reply_markup=m); return
        if d=="petshop":
            m=InlineKeyboardMarkup()
            for k in list(PETS.keys())[:10]: m.add(InlineKeyboardButton(f"{PETS[k][0]} +{PETS[k][2]}/يوم - {PETS[k][1]}", callback_data=f"buypet_{k}"))
            m.add(InlineKeyboardButton("🔙", callback_data="pets")); bot.send_message(cid, "🐉 حيوانات", reply_markup=m); return
        if d.startswith("buypet_"):
            k=d.replace("buypet_",""); name,price,inc=PETS[k]
            if k in u.get("pets",[]): bot.send_message(cid, "معاك ده", reply_markup=shop_menu(uid)); return
            if u["money"]>=price: u["money"]-=price; u["pets"].append(k); save(); bot.send_message(cid, f"🎉 اشتريت {name}", reply_markup=menu(uid))
            else: bot.send_message(cid, "❌ فلوسك مش كفاية", reply_markup=shop_menu(uid))
            return
        if d=="collect_pet":
            inc=pet_income(u)
            if inc==0: bot.send_message(cid, "❌ معندكش", reply_markup=menu(uid)); return
            u["money"]+=inc; save(); bot.send_message(cid, f"🐉 +{inc}", reply_markup=menu(uid)); return
        if d=="pvp":
            m=InlineKeyboardMarkup(); others=[(k,v) for k,v in data.items() if k!=str(uid) and v.get("money",0)>100][:10]
            if not others: bot.send_message(cid, "❌ مفيش حد", reply_markup=menu(uid)); return
            for k,v in others: m.add(InlineKeyboardButton(f"⚔️ {v.get('name')} - {power(v)}", callback_data=f"fight_{k}"))
            m.add(InlineKeyboardButton("🔙", callback_data="home")); bot.send_message(cid, f"⚔️ قوتك {power(u)}", reply_markup=m); return
        if d.startswith("fight_"):
            tid=d.replace("fight_",""); enemy=user(int(tid)); my_p=power(u)+random.randint(0,50); en_p=power(enemy)+random.randint(0,50)
            if my_p>=en_p:
                win=min(500, enemy["money"]//2); enemy["money"]-=win; u["money"]+=win; save(); bot.send_message(cid, f"🎉 كسبت +{win}", reply_markup=menu(uid))
            else:
                lose=min(200, u["money"]//4); u["money"]=max(0,u["money"]-lose); enemy["money"]+=lose; save(); bot.send_message(cid, f"😢 خسرت -{lose}", reply_markup=menu(uid))
            return
        if d=="clan":
            clans=settings.get("clans",{})
            if u.get("clan") and u["clan"] in clans:
                c=clans[u["clan"]]; m=InlineKeyboardMarkup(); m.add(InlineKeyboardButton("💰 +500", callback_data="clan_bonus")); m.add(InlineKeyboardButton("⚔️ حرب 10000", callback_data="clan_war")); m.add(InlineKeyboardButton("🚪 اخرج", callback_data="clan_leave")); m.add(InlineKeyboardButton("🔙", callback_data="home")); bot.send_message(cid, f"👑 {c['name']} {len(c.get('members',[]))} عضو", reply_markup=m); return
            m=InlineKeyboardMarkup()
            for cid2,c in list(clans.items())[:10]: m.add(InlineKeyboardButton(f"👑 {c['name']}", callback_data=f"join_{cid2}"))
            m.add(InlineKeyboardButton("➕ اعمل كلان 1000", callback_data="create_clan")); m.add(InlineKeyboardButton("🔙", callback_data="home")); bot.send_message(cid, "👑 الكلانات", reply_markup=m); return
        if d=="clan_war":
            now=int(time.time())
            if now-u.get("clan_war_cd",0)<3600: bot.send_message(cid, "⏳ حرب كل ساعة", reply_markup=menu(uid)); return
            u["clan_war_cd"]=now
            if random.random()<0.6: got=add(uid,10000); bot.send_message(cid, f"🎉 كلانك كسب +{got}", reply_markup=menu(uid))
            else: bot.send_message(cid, "😢 خسرت", reply_markup=menu(uid))
            save(); return
        if d=="create_clan":
            if u["money"]<1000: bot.send_message(cid, "❌ محتاج 1000", reply_markup=menu(uid)); return
            u["money"]-=1000; cid2=str(uid); settings.setdefault("clans",{})[cid2]={"name":f"كلان {u['name']}","leader":str(uid),"members":[str(uid)]}; u["clan"]=cid2; save(); save_settings(); bot.send_message(cid, "🎉 عملت كلان", reply_markup=menu(uid)); return
        if d.startswith("join_"):
            cid2=d.replace("join_","")
            if cid2 in settings.get("clans",{}): settings["clans"][cid2].setdefault("members",[]).append(str(uid)); u["clan"]=cid2; save(); save_settings(); bot.send_message(cid, "✅ دخلت كلان", reply_markup=menu(uid))
            return
        if d=="clan_bonus": got=add(uid,500); bot.send_message(cid, f"👑 +{got}", reply_markup=menu(uid)); return
        if d=="clan_leave":
            if u.get("clan") in settings.get("clans",{}):
                try: settings["clans"][u["clan"]]["members"].remove(str(uid))
                except: pass
            u["clan"]=None; save(); save_settings(); bot.send_message(cid, "🚪 خرجت", reply_markup=menu(uid)); return
        if d=="auction":
            auc=settings.get("auction",[])
            if not auc: bot.send_message(cid, "🏛️ المزاد فاضي", reply_markup=menu(uid)); return
            m=InlineKeyboardMarkup()
            for i,item in enumerate(auc[:10]): m.add(InlineKeyboardButton(f"{item['name']} - {item['price']}", callback_data=f"buyauc_{i}"))
            m.add(InlineKeyboardButton("➕ اعرض سلاحي", callback_data="sell_auction")); m.add(InlineKeyboardButton("🔙", callback_data="home")); bot.send_message(cid, "🏛️ المزاد", reply_markup=m); return
        if d=="sell_auction":
            if not u.get("weapons"): bot.send_message(cid, "❌ معندكش سلاح", reply_markup=menu(uid)); return
            m=InlineKeyboardMarkup()
            for w in u.get("weapons",[])[:10]: m.add(InlineKeyboardButton(f"بيع {WEAPONS[w][0]} - 500", callback_data=f"listauc_{w}"))
            m.add(InlineKeyboardButton("🔙", callback_data="home")); bot.send_message(cid, "اختر سلاح", reply_markup=m); return
        if d.startswith("listauc_"):
            w=d.replace("listauc_",""); u["weapons"].remove(w); settings.setdefault("auction",[]).append({"weapon":w,"name":WEAPONS[w][0],"price":500,"seller":str(uid),"seller_name":u["name"]}); save(); save_settings(); bot.send_message(cid, "✅ عرضت في المزاد", reply_markup=menu(uid)); return
        if d.startswith("buyauc_"):
            idx=int(d.replace("buyauc_","")); auc=settings.get("auction",[])
            if idx>=len(auc): bot.send_message(cid, "❌ اتباع", reply_markup=menu(uid)); return
            item=auc[idx]
            if u["money"]<item["price"]: bot.send_message(cid, "❌ فلوسك مش كفاية", reply_markup=menu(uid)); return
            u["money"]-=item["price"]; u["weapons"].append(item["weapon"]); s=user(int(item["seller"])) if item["seller"]!="0" else u; s["money"]+=item["price"]; settings["auction"].pop(idx); save(); save_settings(); bot.send_message(cid, "✅ اشتريت", reply_markup=menu(uid)); return
        if d=="goldspin":
            today=datetime.date.today().isoformat()
            if u.get("gold_spin")==today: bot.send_message(cid, "❌ لعبت النهاردة", reply_markup=menu(uid)); return
            u["gold_spin"]=today; win=random.choice([500,1000,2000,5000,10000,50000]); u["money"]+=win; save(); bot.send_message(cid, f"🎡 +{win}", reply_markup=menu(uid)); return
        if d=="red":
            m=InlineKeyboardMarkup(); others=[(k,v) for k,v in data.items() if k!=str(uid)][:10]
            for k,v in others: m.add(InlineKeyboardButton(f"🧧 200 لـ {v.get('name')}", callback_data=f"red_{k}"))
            m.add(InlineKeyboardButton("🔙", callback_data="home")); bot.send_message(cid, "🧧 ظرف", reply_markup=m); return
        if d.startswith("red_"):
            tid=d.replace("red_","")
            if u["money"]<200: bot.send_message(cid, "❌ محتاج 200", reply_markup=menu(uid)); return
            u["money"]-=200; t=user(int(tid)); t["money"]+=300; save(); bot.send_message(cid, "🧧 بعت ظرف", reply_markup=menu(uid)); return
        if d=="guess":
            u["guess_num"]=random.randint(1,5); save(); m=InlineKeyboardMarkup(row_width=5)
            for i in range(1,6): m.add(InlineKeyboardButton(f"{i}", callback_data=f"guess_{i}"))
            m.add(InlineKeyboardButton("🔙", callback_data="play")); bot.send_message(cid, "🔢 خمن 1-5 +2000", reply_markup=m); return
        if d.startswith("guess_"):
            pick=int(d.replace("guess_","")); target=u.get("guess_num",0)
            if pick==target: got=add(uid,2000); bot.send_message(cid, f"🎉 صح +{got}", reply_markup=play_menu(uid))
            else: bot.send_message(cid, f"😢 غلط كان {target}", reply_markup=play_menu(uid))
            return
        if d=="roulette":
            if u["money"]<100: bot.send_message(cid, "❌ محتاج 100", reply_markup=casino_menu(uid)); return
            u["money"]-=100; num=random.randint(0,36); color="🔴 أحمر" if num%2==0 else "⚫ أسود"
            if num==0: u["money"]+=3600; bot.send_message(cid, f"🎡 {num} 🟢 +3600!", reply_markup=casino_menu(uid))
            elif num%2==0: u["money"]+=200; bot.send_message(cid, f"🎡 {num} {color} +200", reply_markup=casino_menu(uid))
            else: bot.send_message(cid, f"🎡 {num} {color} 😢 خسرت", reply_markup=casino_menu(uid))
            save(); return
        if d=="blackjack":
            if u["money"]<100: bot.send_message(cid, "❌ محتاج 100", reply_markup=casino_menu(uid)); return
            u["money"]-=100; me=random.randint(15,22); dealer=random.randint(15,22)
            if me>21: bot.send_message(cid, f"🃏 انت {me} - البوت {dealer} 😢 خسرت", reply_markup=casino_menu(uid))
            elif dealer>21 or me>dealer: u["money"]+=250; bot.send_message(cid, f"🃏 انت {me} - البوت {dealer} 🎉 +250", reply_markup=casino_menu(uid))
            else: bot.send_message(cid, f"🃏 انت {me} - البوت {dealer} 😢 خسرت", reply_markup=casino_menu(uid))
            save(); return
        if d=="quiz":
            q = random.choice([("عاصمة مصر؟", ["القاهرة","الجيزة","اسكندرية"], 0), ("2+2؟", ["3","4","5"], 1), ("أكبر كوكب؟", ["الأرض","المشتري","المريخ"], 1)])
            m=InlineKeyboardMarkup(row_width=1)
            for i,opt in enumerate(q[1]): m.add(InlineKeyboardButton(opt, callback_data=f"quiz_{i}_{q[2]}"))
            bot.send_message(cid, f"🧠 {q[0]}", reply_markup=m); return
        if d.startswith("quiz_"):
            _,pick,ans=d.split("_"); pick=int(pick); ans=int(ans)
            if pick==ans: got=add(uid,1000); bot.send_message(cid, f"🎉 صح +{got}", reply_markup=play_menu(uid))
            else: bot.send_message(cid, "❌ غلط", reply_markup=play_menu(uid))
            return
        if d=="dice_game":
            if u["money"]<50: bot.send_message(cid, "❌ محتاج 50", reply_markup=casino_menu(uid)); return
            u["money"]-=50; me=random.randint(1,6); b=random.randint(1,6)
            if me>b: u["money"]+=150; bot.send_message(cid, f"🎲 {me}-{b} +150", reply_markup=casino_menu(uid))
            elif me<b: bot.send_message(cid, f"🎲 {me}-{b} 😢", reply_markup=casino_menu(uid))
            else: u["money"]+=50; bot.send_message(cid, "🤝 تعادل", reply_markup=casino_menu(uid))
            save(); return
        if d=="bank":
            m=InlineKeyboardMarkup(row_width=2); m.add(InlineKeyboardButton("💵 جاري", callback_data="bank_current"),InlineKeyboardButton("💰 توفير 25%", callback_data="bank_saving"),InlineKeyboardButton("📜 شهادات", callback_data="certs"),InlineKeyboardButton("💳 فيزا", callback_data="credit"),InlineKeyboardButton("🔄 تحويل", callback_data="transfer"),InlineKeyboardButton("💰 وديعة", callback_data="deposit_box"),InlineKeyboardButton("📋 كشف حساب", callback_data="statement"),InlineKeyboardButton("🏧 مكشوف", callback_data="overdraft")); m.add(InlineKeyboardButton("🔙", callback_data="home")); total_bank=u.get("bank",0)+u.get("bank_current",0)+u.get("bank_saving",0)+sum(c["amount"] for c in u.get("certificates",[])); bot.send_message(cid, f"🏦 البنك IBAN {u.get('iban')}\n💵 كاش {u['money']} جاري {u.get('bank_current',0)} توفير {u.get('bank_saving',0)} شهادات {sum(c['amount'] for c in u.get('certificates',[]))} فيزا {u.get('credit_used',0)}/{u.get('credit_limit',5000)} إجمالي {total_bank}", reply_markup=m); return
        if d=="bank_current":
            m=InlineKeyboardMarkup(row_width=2); m.add(InlineKeyboardButton("➕ 500", callback_data="cur_dep_500"),InlineKeyboardButton("➕ 5000", callback_data="cur_dep_5000"),InlineKeyboardButton("➕ الكل", callback_data="cur_dep_all"),InlineKeyboardButton("➖ سحب 500", callback_data="cur_with_500"),InlineKeyboardButton("➖ سحب الكل", callback_data="cur_with_all"),InlineKeyboardButton("🔙 بنك", callback_data="bank")); bot.send_message(cid, f"💵 جاري {u.get('bank_current',0)}", reply_markup=m); return
        if d.startswith("cur_dep_"):
            amt=u["money"] if d=="cur_dep_all" else int(d.replace("cur_dep_",""))
            if u["money"]<amt: bot.send_message(cid, "❌ فلوسك مش كفاية", reply_markup=menu(uid)); return
            u["money"]-=amt; u["bank_current"]=u.get("bank_current",0)+amt; save(); add_history(uid, f"ايداع جاري +{amt}"); bot.send_message(cid, f"✅ حطيت {amt}", reply_markup=menu(uid)); return
        if d.startswith("cur_with_"):
            amt=u.get("bank_current",0) if d=="cur_with_all" else int(d.replace("cur_with_",""))
            if u.get("bank_current",0)<amt: bot.send_message(cid, "❌ مفيش كفاية", reply_markup=menu(uid)); return
            u["bank_current"]-=amt; u["money"]+=amt; save(); add_history(uid, f"سحب جاري -{amt}"); bot.send_message(cid, f"✅ سحبت {amt}", reply_markup=menu(uid)); return
        if d=="bank_saving":
            profit=int(u.get("bank_saving",0)*0.25); m=InlineKeyboardMarkup(row_width=2); m.add(InlineKeyboardButton("➕ 500", callback_data="sav_dep_500"),InlineKeyboardButton("➕ 5000", callback_data="sav_dep_5000"),InlineKeyboardButton("➕ الكل", callback_data="sav_dep_all"),InlineKeyboardButton("➖ سحب 500", callback_data="sav_with_500"),InlineKeyboardButton("➖ سحب الكل", callback_data="sav_with_all"),InlineKeyboardButton(f"📈 فايدة +{profit}", callback_data="interest"),InlineKeyboardButton("🔙 بنك", callback_data="bank")); bot.send_message(cid, f"💰 توفير {u.get('bank_saving',0)} فايدة {profit}", reply_markup=m); return
        if d.startswith("sav_dep_"):
            amt=u["money"] if d=="sav_dep_all" else int(d.replace("sav_dep_",""))
            if u["money"]<amt: bot.send_message(cid, "❌ فلوسك مش كفاية", reply_markup=menu(uid)); return
            u["money"]-=amt; u["bank_saving"]=u.get("bank_saving",0)+amt; save(); add_history(uid, f"ايداع توفير +{amt}"); bot.send_message(cid, f"✅ حطيت {amt}", reply_markup=menu(uid)); return
        if d.startswith("sav_with_"):
            amt=u.get("bank_saving",0) if d=="sav_with_all" else int(d.replace("sav_with_",""))
            if u.get("bank_saving",0)<amt: bot.send_message(cid, "❌ مفيش كفاية", reply_markup=menu(uid)); return
            u["bank_saving"]-=amt; u["money"]+=amt; save(); add_history(uid, f"سحب توفير -{amt}"); bot.send_message(cid, f"✅ سحبت {amt}", reply_markup=menu(uid)); return
        if d=="interest":
            if u.get("bank_saving",0)<=0: bot.send_message(cid, "❌ حط في التوفير", reply_markup=menu(uid)); return
            profit=int(u.get("bank_saving",0)*0.25); u["money"]+=profit; save(); bot.send_message(cid, f"📈 +{profit}", reply_markup=menu(uid)); return
        if d=="certs":
            m=InlineKeyboardMarkup(); m.add(InlineKeyboardButton("📜 40% - 1000", callback_data="cert_1000_40")); m.add(InlineKeyboardButton("📜 70% - 5000", callback_data="cert_5000_70")); m.add(InlineKeyboardButton("📜 150% - 20000", callback_data="cert_20000_150")); m.add(InlineKeyboardButton("💰 فك الشهادات", callback_data="cert_break")); m.add(InlineKeyboardButton("🔙 بنك", callback_data="bank")); txt="📜 شهادات\n"
            for i,c in enumerate(u.get("certificates",[])): txt+=f"{i+1}. {c['amount']} - {c['rate']}% هتاخد {int(c['amount']*(1+c['rate']/100))}\n"
            bot.send_message(cid, txt, reply_markup=m); return
        if d.startswith("cert_") and d!="cert_break":
            _,amt,rate=d.split("_"); amt=int(amt); rate=int(rate)
            if u["money"]<amt: bot.send_message(cid, "❌ محتاج", reply_markup=menu(uid)); return
            u["money"]-=amt; u.setdefault("certificates",[]).append({"amount":amt,"rate":rate,"time":int(time.time())}); save(); bot.send_message(cid, f"✅ شهادة {amt} {rate}%", reply_markup=menu(uid)); return
        if d=="cert_break":
            certs=u.get("certificates",[])
            if not certs: bot.send_message(cid, "❌ معندكش", reply_markup=menu(uid)); return
            total=sum(int(c["amount"]*(1+c["rate"]/100)) for c in certs); u["money"]+=total; u["certificates"]=[]; save(); bot.send_message(cid, f"💰 فكيت {total}", reply_markup=menu(uid)); return
        if d=="credit":
            m=InlineKeyboardMarkup(row_width=2); m.add(InlineKeyboardButton("🛒 فيزا 500", callback_data="cc_buy_500"),InlineKeyboardButton("🛒 فيزا 1000", callback_data="cc_buy_1000"),InlineKeyboardButton("💳 سدد", callback_data="cc_pay"),InlineKeyboardButton("⬆️ زود الحد 5000", callback_data="cc_upgrade"),InlineKeyboardButton("🔙 بنك", callback_data="bank")); bot.send_message(cid, f"💳 حد {u.get('credit_limit',5000)} مستخدم {u.get('credit_used',0)}", reply_markup=m); return
        if d.startswith("cc_buy_"):
            amt=int(d.replace("cc_buy_","")); avail=u.get("credit_limit",5000)-u.get("credit_used",0)
            if amt>avail: bot.send_message(cid, "❌ الحد مش كفاية", reply_markup=menu(uid)); return
            u["credit_used"]=u.get("credit_used",0)+amt; u["money"]+=amt; save(); bot.send_message(cid, f"✅ فيزا {amt}", reply_markup=menu(uid)); return
        if d=="cc_pay":
            used=u.get("credit_used",0)
            if used<=0: bot.send_message(cid, "✅ متسددة", reply_markup=menu(uid)); return
            if u["money"]<used: bot.send_message(cid, "❌ محتاج", reply_markup=menu(uid)); return
            u["money"]-=used; u["credit_used"]=0; save(); bot.send_message(cid, f"✅ سددت {used}", reply_markup=menu(uid)); return
        if d=="cc_upgrade":
            if u["money"]<5000: bot.send_message(cid, "❌ محتاج 5000", reply_markup=menu(uid)); return
            u["money"]-=5000; u["credit_limit"]=u.get("credit_limit",5000)+2000; save(); bot.send_message(cid, f"✅ الحد {u['credit_limit']}", reply_markup=menu(uid)); return
        if d=="transfer": pending[uid]={"action":"wait_transfer_id"}; bot.send_message(cid, "🔄 تحويل - ابعت ID الشخص رسوم 5", reply_markup=menu(uid)); return
        if d=="deposit_box":
            m=InlineKeyboardMarkup(); m.add(InlineKeyboardButton("💰 وديعة 1000 - 2000", callback_data="wd_1000")); m.add(InlineKeyboardButton("💰 وديعة 5000 - 10000", callback_data="wd_5000")); m.add(InlineKeyboardButton("🔙 بنك", callback_data="bank")); bot.send_message(cid, "💰 وديعة", reply_markup=m); return
        if d.startswith("wd_"):
            amt=int(d.replace("wd_",""))
            if u["money"]<amt: bot.send_message(cid, "❌ فلوسك مش كفاية", reply_markup=menu(uid)); return
            u["money"]-=amt; u.setdefault("certificates",[]).append({"amount":amt,"rate":100,"time":int(time.time())}); save(); bot.send_message(cid, f"✅ وديعة {amt}", reply_markup=menu(uid)); return
        if d=="statement":
            hist=u.get("bank_history",[])
            if not hist: bot.send_message(cid, "📋 فاضي", reply_markup=menu(uid)); return
            bot.send_message(cid, "📋 كشف حساب\n"+"\n".join(hist), reply_markup=menu(uid)); return
        if d=="overdraft":
            m=InlineKeyboardMarkup(); m.add(InlineKeyboardButton("🏧 500 مكشوف", callback_data="od_500")); m.add(InlineKeyboardButton("✅ سدد", callback_data="od_pay")); m.add(InlineKeyboardButton("🔙 بنك", callback_data="bank")); bot.send_message(cid, f"🏧 مكشوف {u.get('overdraft',0)}/1000", reply_markup=m); return
        if d.startswith("od_") and d!="od_pay":
            amt=int(d.replace("od_",""))
            if u.get("overdraft",0)+amt>1000: bot.send_message(cid, "❌ عديت الحد", reply_markup=menu(uid)); return
            u["money"]+=amt; u["overdraft"]=u.get("overdraft",0)+amt; save(); bot.send_message(cid, f"✅ {amt} مكشوف", reply_markup=menu(uid)); return
        if d=="od_pay":
            od=u.get("overdraft",0)
            if od<=0: bot.send_message(cid, "✅ معليكش", reply_markup=menu(uid)); return
            if u["money"]<od: bot.send_message(cid, "❌ محتاج", reply_markup=menu(uid)); return
            u["money"]-=od; u["overdraft"]=0; save(); bot.send_message(cid, f"✅ سددت {od}", reply_markup=menu(uid)); return
        if d=="loan":
            loans=u.get("loans",[]); total_loan=sum(x["amount"] for x in loans); penalty=check_loan_penalty(u); m=InlineKeyboardMarkup(row_width=2)
            if penalty!="🔒 محظور":
                m.add(InlineKeyboardButton("💸 1000", callback_data="take_1000")); m.add(InlineKeyboardButton("💸 5000", callback_data="take_5000")); m.add(InlineKeyboardButton("💸 10000", callback_data="take_10000")); m.add(InlineKeyboardButton("💸 50000", callback_data="take_50000")); m.add(InlineKeyboardButton("💸 100000", callback_data="take_100000"))
            if loans:
                for i,ln in enumerate(loans):
                    pa,rate,days=get_loan_pay_amount(ln); m.add(InlineKeyboardButton(f"✅ سدد {i+1} - {ln['amount']} هتدفع {pa} ({int(rate*100)}%)", callback_data=f"pay_{i}"))
                m.add(InlineKeyboardButton("💥 سدد الكل", callback_data="pay_all"))
            m.add(InlineKeyboardButton("🔙", callback_data="home")); txt=f"💸 قروض {len(loans)}/5 عليك {total_loan} معاك {u['money']}\nعقاب: يوم 20% / 3 أيام 30% + خصم / 7 أيام 50% + حظر"; bot.send_message(cid, txt, reply_markup=m); return
        if d.startswith("take_"):
            loans=u.get("loans",[])
            if check_loan_penalty(u)=="🔒 محظور": bot.send_message(cid, "🔒 محظور سدد القديم", reply_markup=menu(uid)); return
            if len(loans)>=5: bot.send_message(cid, "❌ 5 قروض سدد واحد", reply_markup=menu(uid)); return
            amt=int(d.replace("take_","")); u["money"]+=amt; loans.append({"amount":amt,"time":int(time.time())}); u["loans"]=loans; save(); bot.send_message(cid, f"✅ خدت {amt}", reply_markup=menu(uid)); return
        if d.startswith("pay_") and d!="pay_all":
            idx=int(d.replace("pay_","")); loans=u.get("loans",[])
            if idx>=len(loans): bot.send_message(cid, "❌ مش موجود", reply_markup=menu(uid)); return
            ln=loans[idx]; pa,rate,days=get_loan_pay_amount(ln)
            if u["money"]<pa:
                need=pa-u["money"]
                if u.get("bank_saving",0)>=need: u["bank_saving"]-=need; u["money"]=0; loans.pop(idx); u["loans"]=loans; save(); bot.send_message(cid, "🏦 خصم من التوفير ✅ سددت", reply_markup=menu(uid)); return
                bot.send_message(cid, f"❌ محتاج {pa} فايدة {int(rate*100)}% متأخر {days} يوم", reply_markup=menu(uid)); return
            u["money"]-=pa; loans.pop(idx); u["loans"]=loans; save(); bot.send_message(cid, f"✅ سددت {pa}", reply_markup=menu(uid)); return
        if d=="pay_all":
            loans=u.get("loans",[])
            if not loans: bot.send_message(cid, "❌ معليكش", reply_markup=menu(uid)); return
            total=sum(get_loan_pay_amount(x)[0] for x in loans)
            if u["money"]<total:
                need=total-u["money"]
                if u.get("bank_saving",0)>=need: u["bank_saving"]-=need; u["money"]=0; u["loans"]=[]; save(); bot.send_message(cid, "🏦 خصم من التوفير ✅ سددت الكل", reply_markup=menu(uid)); return
                bot.send_message(cid, f"❌ محتاج {total}", reply_markup=menu(uid)); return
            u["money"]-=total; u["loans"]=[]; save(); bot.send_message(cid, f"✅ سددت الكل {total}", reply_markup=menu(uid)); return
        if d=="invest":
            m=InlineKeyboardMarkup(row_width=2); m.add(InlineKeyboardButton("💎 1000", callback_data="inv_1000"),InlineKeyboardButton("💎 5000", callback_data="inv_5000"),InlineKeyboardButton("💎 20000", callback_data="inv_20000")); m.add(InlineKeyboardButton("💰 اسحب", callback_data="inv_out")); m.add(InlineKeyboardButton("🔙", callback_data="home")); bot.send_message(cid, f"💎 استثمار {u.get('invest',0)} كاش {u['money']}", reply_markup=m); return
        if d.startswith("inv_") and d!="inv_out":
            amt=int(d.replace("inv_",""))
            if u["money"]<amt: bot.send_message(cid, "❌ فلوسك مش كفاية", reply_markup=menu(uid)); return
            u["money"]-=amt; u["invest"]=u.get("invest",0)+amt; save(); bot.send_message(cid, f"✅ استثمرت {amt} +50%", reply_markup=menu(uid)); return
        if d=="inv_out":
            if u.get("invest",0)<=0: bot.send_message(cid, "❌ معندكش", reply_markup=menu(uid)); return
            profit=int(u.get("invest",0)*0.5); total=u.get("invest",0)+profit; u["money"]+=total; u["invest"]=0; save(); bot.send_message(cid, f"💎 سحبت {total}", reply_markup=menu(uid)); return
        if d=="goldbox":
            if u["money"]<200: bot.send_message(cid, "❌ محتاج 200", reply_markup=play_menu(uid)); return
            u["money"]-=200; win=random.choice([100,300,500,1000,2000,5000]); u["money"]+=win; save(); bot.send_message(cid, f"📦 +{win}", reply_markup=play_menu(uid)); return
        if d=="challenge":
            today=datetime.date.today().isoformat()
            if u.get("last_challenge")==today: bot.send_message(cid, "✅ عملته النهاردة", reply_markup=menu(uid)); return
            u["last_challenge"]=today; got=add(uid,2000); bot.send_message(cid, f"🎯 +{got}", reply_markup=menu(uid)); return
        if d=="slot":
            if u["money"]<50: bot.send_message(cid, "❌ محتاج 50", reply_markup=casino_menu(uid)); return
            u["money"]-=50; fruits=["🍎","🍌","🍇","🍓","🍒","💎","7️⃣"]; r=[random.choice(fruits) for _ in range(3)]; txt=f"🎰 {' | '.join(r)}\n"
            if r[0]==r[1]==r[2]:
                win=5000 if r[0]=="💎" else 2000 if r[0]=="7️⃣" else 500; u["money"]+=win; txt+=f"🎉 +{win}"; settings["jackpot"]=settings.get("jackpot",10000)+50
            elif r[0]==r[1] or r[1]==r[2] or r[0]==r[2]: u["money"]+=150; txt+="✅ +150"
            else: txt+="😢 مفيش"
            save(); save_settings(); bot.send_message(cid, txt, reply_markup=casino_menu(uid)); return
        if d=="dice":
            if u["money"]<50: bot.send_message(cid, "❌ محتاج 50", reply_markup=casino_menu(uid)); return
            u["money"]-=50; me=random.randint(1,6); bd=random.randint(1,6)
            if me>bd: u["money"]+=150; res=f"🎉 كسبت {me}-{bd} +150"
            elif me<bd: res=f"😢 خسرت {me}-{bd}"
            else: u["money"]+=50; res="🤝 تعادل"
            save(); bot.send_message(cid, res, reply_markup=casino_menu(uid)); return
        if d=="cards":
            if u["money"]<50: bot.send_message(cid, "❌ محتاج 50", reply_markup=casino_menu(uid)); return
            u["money"]-=50; m=InlineKeyboardMarkup(row_width=3)
            for i in range(3): m.add(InlineKeyboardButton(f"🃏 {i+1}", callback_data=f"pick_{i}"))
            m.add(InlineKeyboardButton("🔙", callback_data="home")); bot.send_message(cid, "🃏 اختار كارت 500", reply_markup=m); return
        if d.startswith("pick_"):
            wc=random.randint(0,2); pick=int(d.replace("pick_",""))
            if pick==wc: u["money"]+=500; save(); bot.send_message(cid, "🎉 صح +500", reply_markup=casino_menu(uid))
            else: save(); bot.send_message(cid, f"😢 غلط كان {wc+1}", reply_markup=casino_menu(uid))
            return
        if d=="lottery":
            m=InlineKeyboardMarkup(); m.add(InlineKeyboardButton("🎟️ تذكرة 50", callback_data="buy_ticket")); m.add(InlineKeyboardButton("🔙", callback_data="home")); bot.send_message(cid, f"💎 يانصيب تذكرتك {u.get('lottery_tickets',0)} جايزة {settings.get('jackpot',10000)}", reply_markup=m); return
        if d=="buy_ticket":
            if u["money"]<50: bot.send_message(cid, "❌ محتاج 50", reply_markup=casino_menu(uid)); return
            u["money"]-=50; u["lottery_tickets"]=u.get("lottery_tickets",0)+1; settings.setdefault("lottery",[]).append(str(uid)); settings["jackpot"]=settings.get("jackpot",10000)+50; save(); save_settings(); bot.send_message(cid, "✅ تذكرة", reply_markup=casino_menu(uid)); return
        if d=="steal":
            now=int(time.time())
            if now-u.get("steal",0)<20: bot.send_message(cid, f"⏳ استنى {20-(now-u.get('steal',0))}", reply_markup=play_menu(uid)); return
            others=[k for k in data.keys() if k!=str(uid) and data[k].get("money",0)>100]
            if not others: bot.send_message(cid, "❌ مفيش حد", reply_markup=play_menu(uid)); return
            victim=random.choice(others); v=data[victim]; u["steal"]=now
            if random.random()<0.6:
                sa=random.randint(50, min(300, v["money"]//2)); v["money"]-=sa; u["money"]+=sa; save(); bot.send_message(cid, f"🥷 سرقت {sa} من {v.get('name')}", reply_markup=play_menu(uid))
            else: u["money"]=max(0,u["money"]-50); save(); bot.send_message(cid, "🚨 اتقفشت -50", reply_markup=play_menu(uid))
            return
        if d=="secret": got=add(uid,500); bot.send_message(cid, f"🎯 +{got}", reply_markup=play_menu(uid)); return
        if d=="trade": bot.send_message(cid, "📈 بورصة", reply_markup=trade_menu(uid)); return
        if d=="trade2":
            m=InlineKeyboardMarkup()
            for k in list(MARKET.keys())[15:30]:
                v=MARKET[k]; qty=u.get("portfolio",{}).get(k,0); m.add(InlineKeyboardButton(f"{v['name']} - {v['price']} | {qty}", callback_data=f"coin_{k}"))
            m.add(InlineKeyboardButton("🔙 بورصة", callback_data="trade")); bot.send_message(cid, "📈 بورصة صفحة 2", reply_markup=m); return
        if d=="staking":
            m=InlineKeyboardMarkup(); m.add(InlineKeyboardButton("🪙 1000 - 2000", callback_data="stake_1000")); m.add(InlineKeyboardButton("🪙 5000 - 10000", callback_data="stake_5000")); m.add(InlineKeyboardButton("💰 اسحب", callback_data="stake_out")); m.add(InlineKeyboardButton("🔙", callback_data="trade")); bot.send_message(cid, f"🪙 ستيكينج {u.get('staking',0)}", reply_markup=m); return
        if d.startswith("stake_") and d!="stake_out":
            amt=int(d.replace("stake_",""))
            if u["money"]<amt: bot.send_message(cid, "❌ فلوسك مش كفاية", reply_markup=menu(uid)); return
            u["money"]-=amt; u["staking"]=u.get("staking",0)+amt; save(); bot.send_message(cid, f"✅ حطيت {amt} هتاخد {amt*2}", reply_markup=menu(uid)); return
        if d=="stake_out":
            if u.get("staking",0)<=0: bot.send_message(cid, "❌ معندكش", reply_markup=menu(uid)); return
            total=u.get("staking",0)*2; u["money"]+=total; u["staking"]=0; save(); bot.send_message(cid, f"🪙 سحبت {total}", reply_markup=menu(uid)); return
        if d=="my_portfolio":
            pf=u.get("portfolio",{})
            if not pf or sum(pf.values())==0: bot.send_message(cid, "💼 فاضية", reply_markup=trade_menu(uid)); return
            txt="💼 محفظتك\n"; total=0
            for k,qty in pf.items():
                if qty>0 and k in MARKET: val=qty*MARKET[k]["price"]; total+=val; txt+=f"{MARKET[k]['name']} {qty} × {MARKET[k]['price']} = {val}\n"
            bot.send_message(cid, txt+f"إجمالي {total}", reply_markup=trade_menu(uid)); return
        if d.startswith("coin_"):
            k=d.replace("coin_",""); info=MARKET[k]; qty=u.get("portfolio",{}).get(k,0); m=InlineKeyboardMarkup(row_width=2); m.add(InlineKeyboardButton(f"🟢 اشتري 1 - {info['price']}", callback_data=f"buy_{k}_1"),InlineKeyboardButton(f"🟢 اشتري 5 - {info['price']*5}", callback_data=f"buy_{k}_5")); m.add(InlineKeyboardButton("🔴 بيع 1", callback_data=f"sell_{k}_1"),InlineKeyboardButton("🔴 بيع الكل", callback_data=f"sell_{k}_all")); m.add(InlineKeyboardButton("🔙", callback_data="trade")); bot.send_message(cid, f"{info['name']} سعر {info['price']} معاك {qty}", reply_markup=m); return
        if d.startswith("buy_"):
            _,k,amt=d.split("_"); amt=int(amt); price=MARKET[k]["price"]*amt
            if u["money"]<price: bot.send_message(cid, "❌ محتاج", reply_markup=trade_menu(uid)); return
            u["money"]-=price; u["portfolio"][k]=u["portfolio"].get(k,0)+amt; save(); bot.send_message(cid, f"✅ اشتريت {amt}", reply_markup=trade_menu(uid)); return
        if d.startswith("sell_"):
            _,k,amt=d.split("_"); have=u.get("portfolio",{}).get(k,0)
            if have<=0: bot.send_message(cid, "❌ معكش", reply_markup=trade_menu(uid)); return
            amt=have if amt=="all" else min(int(amt),have); gain=MARKET[k]["price"]*amt; u["money"]+=gain; u["portfolio"][k]-=amt; save(); bot.send_message(cid, f"✅ بعت {amt} بـ {gain}", reply_markup=trade_menu(uid)); return
        if d=="tasks":
            m=InlineKeyboardMarkup()
            for i in range(10): m.add(InlineKeyboardButton(f"{TASKS[i][0]} +{TASKS[i][1]+power(u)}", callback_data=f"t_{i}"))
            m.add(InlineKeyboardButton("➡️ مهام أكتر", callback_data="tasks2")); m.add(InlineKeyboardButton("🔙", callback_data="play")); bot.send_message(cid, "📋 500 مهمة", reply_markup=m); return
        if d=="tasks2":
            m=InlineKeyboardMarkup()
            for i in range(10,20): m.add(InlineKeyboardButton(f"{TASKS[i][0]} +{TASKS[i][1]+power(u)}", callback_data=f"t_{i}"))
            m.add(InlineKeyboardButton("🔙", callback_data="play")); bot.send_message(cid, "📋 مهام 10-20", reply_markup=m); return
        if d.startswith("t_"):
            i=int(d.split("_")[1])
            if i==0:
                m=InlineKeyboardMarkup(row_width=2); m.add(InlineKeyboardButton("3", callback_data="wrong"), InlineKeyboardButton("4 ✅", callback_data="right_50"), InlineKeyboardButton("5", callback_data="wrong"), InlineKeyboardButton("6", callback_data="wrong")); bot.send_message(cid, "🧠 2+2 = كام؟", reply_markup=m)
            else: got=add(uid, TASKS[i][1]+power(u)); bot.send_message(cid, f"✅ خدت +{got}", reply_markup=play_menu(uid))
            return
        if d.startswith("right_"): got=add(uid, int(d.split("_")[1])+power(u)); bot.send_message(cid, f"✅ صح! +{got}", reply_markup=play_menu(uid)); return
        if d=="wrong": bot.send_message(cid, "❌ غلط", reply_markup=play_menu(uid)); return
        if d=="daily":
            now=int(time.time())
            if now-u.get("daily",0)<5: bot.send_message(cid, "⏳ استنى", reply_markup=play_menu(uid))
            else: u["streak"]+=1; got=add(uid,(500 if is_vip(u) else 100)+u["streak"]*10); u["daily"]=now; save(); bot.send_message(cid, f"📅 +{got}", reply_markup=play_menu(uid))
            return
        if d=="gift":
            now=int(time.time())
            if now-u.get("gift",0)<5: bot.send_message(cid, "⏳ استنى", reply_markup=play_menu(uid))
            else: got=add(uid,1000 if is_vip(u) else random.choice([50,100,200,500,1000])); u["gift"]=now; save(); bot.send_message(cid, f"🎁 +{got}", reply_markup=play_menu(uid))
            return
        if d=="spin":
            now=int(time.time())
            if now-u.get("spin",0)<5: bot.send_message(cid, "⏳ كل 5 ث", reply_markup=play_menu(uid))
            else: r=random.choice([0,50,100,200,500,1000,2000,5000]); u["spin"]=now; save(); got=add(uid,r) if r>0 else 0; bot.send_message(cid, f"🎡 +{got}" if r>0 else "😢 صفر", reply_markup=play_menu(uid))
            return
        if d=="gamble":
            m=InlineKeyboardMarkup(row_width=2); m.add(InlineKeyboardButton("🪙 ملك 50", callback_data="g_1"),InlineKeyboardButton("🪙 كتابة 50", callback_data="g_2")); m.add(InlineKeyboardButton("🔙", callback_data="play")); bot.send_message(cid, "🎲 راهن 50 تكسب 150", reply_markup=m); return
        if d.startswith("g_"):
            if u["money"]<50: bot.send_message(cid, "❌ فلوسك مش كفاية", reply_markup=play_menu(uid)); return
            u["money"]-=50
            if random.choice([True,False]): u["money"]+=150; save(); bot.send_message(cid, "🎉 +150", reply_markup=play_menu(uid))
            else: save(); bot.send_message(cid, "😢 -50", reply_markup=play_menu(uid))
            return
        if d=="codes":
            m=InlineKeyboardMarkup(row_width=2)
            for c in list(CODES.keys())[:10]: m.add(InlineKeyboardButton(c, callback_data=f"code_{c}"))
            m.add(InlineKeyboardButton("🔙", callback_data="play")); bot.send_message(cid, "🎁 100 كود", reply_markup=m); return
        if d.startswith("code_"):
            c=d.replace("code_","")
            if c in u.get("codes",[]): bot.send_message(cid, "❌ استخدمته", reply_markup=play_menu(uid)); return
            u["codes"].append(c); got=add(uid, CODES[c]); bot.send_message(cid, f"🎉 +{got}", reply_markup=play_menu(uid)); return
        if d=="contest":
            top=sorted(data.items(), key=lambda x: x[1].get('score',0), reverse=True)[:5]; txt="🏆 مسابقة - أعلى نقاط 5000\n"
            for i,(k,v) in enumerate(top): txt+=f"{i+1}. {v.get('name')} - {v.get('score',0)}\n"
            bot.send_message(cid, txt+f"نقطك {u.get('score',0)}", reply_markup=play_menu(uid)); return
        if d=="weapons":
            m=InlineKeyboardMarkup()
            for k in list(WEAPONS.keys())[:10]: m.add(InlineKeyboardButton(f"{WEAPONS[k][0]} +{WEAPONS[k][2]} - {WEAPONS[k][1]}", callback_data=f"bw_{k}"))
            m.add(InlineKeyboardButton("➡️ أسلحة أكتر", callback_data="weapons2")); m.add(InlineKeyboardButton("🔙", callback_data="shop")); bot.send_message(cid, f"🔫 100 سلاح قوتك +{power(u)}", reply_markup=m); return
        if d=="weapons2":
            m=InlineKeyboardMarkup()
            for k in list(WEAPONS.keys())[10:20]: m.add(InlineKeyboardButton(f"{WEAPONS[k][0]} +{WEAPONS[k][2]} - {WEAPONS[k][1]}", callback_data=f"bw_{k}"))
            m.add(InlineKeyboardButton("🔙", callback_data="shop")); bot.send_message(cid, "🔫 أسلحة 10-20", reply_markup=m); return
        if d.startswith("bw_"):
            k=d.replace("bw_",""); name,price,bonus=WEAPONS[k]
            if k in u.get("weapons",[]): bot.send_message(cid, "معاك ده", reply_markup=shop_menu(uid)); return
            if u["money"]>=price: u["money"]-=price; u["weapons"].append(k); save(); bot.send_message(cid, f"🎉 اشتريت {name}", reply_markup=shop_menu(uid))
            else: bot.send_message(cid, "❌ فلوسك مش كفاية", reply_markup=shop_menu(uid))
            return
        if d=="vip":
            if is_vip(u): bot.send_message(cid, "VIP أصلاً", reply_markup=shop_menu(uid)); return
            m=InlineKeyboardMarkup(); m.add(InlineKeyboardButton("👑 اشتري VIP 1000", callback_data="buy_vip")); m.add(InlineKeyboardButton("🔙", callback_data="shop")); bot.send_message(cid, "👑 VIP ×3 + هدية 5000 كل يوم", reply_markup=m); return
        if d=="buy_vip":
            if u["money"]>=1000: u["money"]-=1000; u["vip"]=True; u["vip_until"]=0; save(); bot.send_message(cid, "🎉 VIP 👑", reply_markup=shop_menu(uid))
            else: bot.send_message(cid, "❌ فلوسك مش كفاية", reply_markup=shop_menu(uid))
            return
        if d=="owner":
            if not is_owner(uid): bot.send_message(cid, "❌ مش الأونر"); return
            bot.send_message(cid, f"👑 لوحة الأونر 👥 {len(data)} 💰 {sum(v.get('money',0) for v in data.values())} جاكبوت {settings.get('jackpot',10000)}", reply_markup=owner_menu()); return
        if d=="a_custom":
            if not is_owner(uid): return
            pending[uid]={"action":"wait_id"}; bot.send_message(cid, "💰 ابعت ID", reply_markup=owner_menu()); return
        if d=="a_custom_all":
            if not is_owner(uid): return
            pending[uid]={"action":"custom_all"}; bot.send_message(cid, "💰 اكتب المبلغ للكل", reply_markup=owner_menu()); return
        if d.startswith("custom_"):
            if not is_owner(uid): return
            tid=d.replace("custom_",""); pending[uid]={"target":tid,"action":"custom_one"}; bot.send_message(cid, "💰 اكتب المبلغ"); return
        if d.startswith("ctake_"):
            if not is_owner(uid): return
            tid=d.replace("ctake_",""); pending[uid]={"target":tid,"action":"custom_take"}; bot.send_message(cid, "💸 اكتب المبلغ تسحبه"); return
        if d=="a_stats":
            if not is_owner(uid): return
            bot.send_message(cid, f"📊 👥 {len(data)} 💰 {sum(v.get('money',0) for v in data.values())} 🏠 {sum(1 for v in data.values() if v.get('house'))}", reply_markup=owner_menu()); return
        if d=="a_users":
            if not is_owner(uid): return
            m=InlineKeyboardMarkup()
            for k,v in list(data.items())[:25]: m.add(InlineKeyboardButton(f"{v.get('name')} - {v.get('money',0)}", callback_data=f"a_u_{k}"))
            m.add(InlineKeyboardButton("🔙", callback_data="owner")); bot.send_message(cid, "👥 دوس على واحد", reply_markup=m); return
        if d.startswith("a_u_"):
            if not is_owner(uid): return
            t=d.replace("a_u_",""); info=user(int(t)); m=InlineKeyboardMarkup(row_width=2); m.add(InlineKeyboardButton("💰 مبلغ", callback_data=f"custom_{t}"),InlineKeyboardButton("💸 اسحب", callback_data=f"ctake_{t}"),InlineKeyboardButton("➕1000", callback_data=f"add_{t}_1000"),InlineKeyboardButton("➕10000", callback_data=f"add_{t}_10000"),InlineKeyboardButton("💎 1M", callback_data=f"add_{t}_1000000"),InlineKeyboardButton("💥 تصفير", callback_data=f"zero_{t}"),InlineKeyboardButton("👑 VIP", callback_data=f"gv_{t}"),InlineKeyboardButton("🚫 حظر", callback_data=f"ban_{t}"),InlineKeyboardButton("✅ فك حظر", callback_data=f"unban_{t}"),InlineKeyboardButton("🐉 تنين", callback_data=f"givepet_{t}_pet1"),InlineKeyboardButton("🙏 سامحه قروض", callback_data=f"forgive_{t}")); m.add(InlineKeyboardButton("🔙", callback_data="a_users")); bot.send_message(cid, f"👤 {info.get('name')} 🆔 {t} 💰 {info['money']}", reply_markup=m); return
        if d.startswith("forgive_"):
            if not is_owner(uid): return
            t=d.replace("forgive_",""); info=user(int(t)); info["loans"]=[]; save(); bot.send_message(cid, f"✅ سامحت {info.get('name')}", reply_markup=owner_menu()); return
        if d.startswith("givepet_"):
            if not is_owner(uid): return
            _,t,pet=d.split("_",2); info=user(int(t))
            if pet not in info["pets"]: info["pets"].append(pet); save()
            bot.send_message(cid, f"✅ اديت {PETS[pet][0]}", reply_markup=owner_menu()); return
        if d.startswith("zero_"):
            if not is_owner(uid): return
            t=d.replace("zero_",""); info=user(int(t)); info["money"]=0; info["score"]=0; info["portfolio"]={}; info["bank"]=0; info["bank_current"]=0; info["bank_saving"]=0; info["invest"]=0; save(); bot.send_message(cid, f"💥 صفرت {info.get('name')}", reply_markup=owner_menu()); return
        if d.startswith("rmvip_"):
            if not is_owner(uid): return
            t=d.replace("rmvip_",""); info=user(int(t)); info["vip"]=False; save(); bot.send_message(cid, "❌ شلت VIP", reply_markup=owner_menu()); return
        if d.startswith("ban_"):
            if not is_owner(uid): return
            t=d.replace("ban_","")
            if t not in settings["banned"]: settings["banned"].append(t); save_settings()
            bot.send_message(cid, f"🚫 حظرت {t}", reply_markup=owner_menu()); return
        if d.startswith("unban_"):
            if not is_owner(uid): return
            t=d.replace("unban_","")
            if t in settings["banned"]: settings["banned"].remove(t); save_settings()
            bot.send_message(cid, f"✅ فكيت {t}", reply_markup=owner_menu()); return
        if d.startswith("gv_"):
            if not is_owner(uid): return
            t=d.replace("gv_",""); info=user(int(t)); info["vip"]=True; save(); bot.send_message(cid, "✅ VIP", reply_markup=owner_menu()); return
        if d.startswith("add_") or d.startswith("sub_"):
            if not is_owner(uid): return
            _,t,amt=d.split("_"); amt=int(amt); info=user(int(t))
            if d.startswith("add_"): info["money"]+=amt
            else: info["money"]=max(0,info["money"]-amt)
            save(); bot.send_message(cid, f"✅ بقى {info['money']}", reply_markup=owner_menu()); return
        if d=="a_maint":
            if not is_owner(uid): return
            m=InlineKeyboardMarkup(); m.add(InlineKeyboardButton("قفل/فتح", callback_data="toggle_maint")); m.add(InlineKeyboardButton("🔙", callback_data="owner")); bot.send_message(cid, f"🛠️ صيانة {settings.get('maintenance')}", reply_markup=m); return
        if d=="toggle_maint":
            if not is_owner(uid): return
            settings["maintenance"]=not settings.get("maintenance",False); save_settings(); bot.send_message(cid, "✅ غيرت الصيانة", reply_markup=owner_menu()); return
        if d=="a_self":
            if not is_owner(uid): return
            m=InlineKeyboardMarkup(); m.add(InlineKeyboardButton("💰 100K", callback_data="self_100000")); m.add(InlineKeyboardButton("💎 1M", callback_data="self_1000000")); m.add(InlineKeyboardButton("👑 VIP", callback_data="self_vip")); m.add(InlineKeyboardButton("🔙", callback_data="owner")); bot.send_message(cid, "💎 لنفسك", reply_markup=m); return
        if d.startswith("self_"):
            if not is_owner(uid): return
            if d=="self_vip": u["vip"]=True; save(); bot.send_message(cid, "✅ VIP", reply_markup=owner_menu()); return
            amt=int(d.replace("self_","")); u["money"]+=amt; save(); bot.send_message(cid, f"✅ +{amt}", reply_markup=owner_menu()); return
        if d=="a_vip_all":
            if not is_owner(uid): return
            for k in data: data[k]["vip"]=True
            save(); bot.send_message(cid, "✅ VIP للكل", reply_markup=owner_menu()); return
        if d=="a_pet_all":
            if not is_owner(uid): return
            for k in data:
                if "pet1" not in data[k].get("pets",[]): data[k].setdefault("pets",[]).append("pet1")
            save(); bot.send_message(cid, "✅ تنين للكل", reply_markup=owner_menu()); return
        if d=="a_house_all":
            if not is_owner(uid): return
            for k in data: data[k]["house"]="h1"
            save(); bot.send_message(cid, "✅ شقة للكل", reply_markup=owner_menu()); return
        if d=="a_car_all":
            if not is_owner(uid): return
            for k in data: data[k]["car"]="c1"
            save(); bot.send_message(cid, "✅ عربية للكل", reply_markup=owner_menu()); return
        if d=="a_weekly":
            if not is_owner(uid): return
            if not data: bot.send_message(cid, "مفيش حد", reply_markup=owner_menu()); return
            w=max(data.items(), key=lambda x: x[1].get('score',0)); wid,winfo=w; winfo["money"]+=50000; winfo["score"]=0; save()
            for k in data:
                if k!=wid: data[k]["score"]=0
            save(); bot.send_message(cid, f"🏆 بطل الأسبوع {winfo.get('name')} +50000", reply_markup=owner_menu()); return
        if d=="a_end":
            if not is_owner(uid): return
            if not data: bot.send_message(cid, "مفيش حد", reply_markup=owner_menu()); return
            w=max(data.items(), key=lambda x: x[1].get('score',0)); wid,winfo=w; winfo["money"]+=5000; winfo["score"]=0; save()
            for k in data:
                if k!=wid: data[k]["score"]=0
            save(); bot.send_message(cid, f"🏆 الفايز {winfo.get('name')} +5000", reply_markup=owner_menu()); return
        # ===== هنا التصليح المدمج - اليانصيب الصح =====
        if d=="a_lottery_draw":
            if not is_owner(uid): return
            lot=settings.get("lottery",[])
            if not lot: bot.send_message(cid, "❌ مفيش تذاكر", reply_markup=owner_menu()); return
            winner=random.choice(lot)
            prize=settings.get("jackpot",10000)
            winfo=user(int(winner))
            winfo["money"]+=prize
            winfo["lottery_tickets"]=0
            save()
            settings["lottery"]=[]
            settings["jackpot"]=10000
            save_settings()
            for k in data:
                try: bot.send_message(int(k), f"💎 نتيجة اليانصيب!\n🏆 الفايز: {winfo.get('name')} كسب {prize}!")
                except: pass
            bot.send_message(cid, f"🏆 الفايز: {winfo.get('name')} +{prize}", reply_markup=owner_menu()); return
        if d=="a_pump":
            if not is_owner(uid): return
            for k in MARKET: MARKET[k]["price"]+=random.randint(100,300)
            bot.send_message(cid, "💥 فجرت الأسعار", reply_markup=owner_menu()); return
        if d=="a_crash":
            if not is_owner(uid): return
            for k in MARKET: MARKET[k]["price"]=max(20, MARKET[k]["price"]-random.randint(50,150))
            bot.send_message(cid, "📉 انهيار", reply_markup=owner_menu()); return
        if d=="a_gift_all":
            if not is_owner(uid): return
            m=InlineKeyboardMarkup(); m.add(InlineKeyboardButton("🎁 1000", callback_data="giftall_1000")); m.add(InlineKeyboardButton("🎁 10000", callback_data="giftall_10000")); m.add(InlineKeyboardButton("🔙", callback_data="owner")); bot.send_message(cid, "🎁 هدية للكل", reply_markup=m); return
        if d.startswith("giftall_"):
            if not is_owner(uid): return
            amt=int(d.replace("giftall_","")); c=0
            for k in list(data.keys()):
                try: bot.send_message(int(k), f"🎁 هدية +{amt}"); data[k]["money"]+=amt; c+=1
                except: pass
            save(); bot.send_message(cid, f"✅ بعت لـ {c}", reply_markup=owner_menu()); return
        if d=="a_bc":
            if not is_owner(uid): return
            m=InlineKeyboardMarkup(); m.add(InlineKeyboardButton("🎉 مسابقة", callback_data="bc_1")); m.add(InlineKeyboardButton("👋 ارجع", callback_data="bc_3")); m.add(InlineKeyboardButton("🔙", callback_data="owner")); bot.send_message(cid, "📢 بث", reply_markup=m); return
        if d.startswith("bc_"):
            if not is_owner(uid): return
            texts={"bc_1":"🎉 مسابقة جديدة ادخل وخد 5000","bc_3":"👋 ارجع العب وخد فلوس"}
            c=0
            for k in list(data.keys()):
                try: bot.send_message(int(k), texts[d]); c+=1
                except: pass
            bot.send_message(cid, f"✅ بعت لـ {c}", reply_markup=owner_menu()); return
    except Exception as e:
        print("Error:", e, traceback.format_exc())
        try: bot.send_message(cid, "حصل مشكلة دوس تاني", reply_markup=menu(uid))
        except: pass

print("Bot FINAL MERGED - 1000+ lines - is running ✅")
while True:
    try: bot.infinity_polling(timeout=60, long_polling_timeout=60, skip_pending=True)
    except Exception as e:
        print(f"Restarting... {e}"); time.sleep(3)
