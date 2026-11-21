import os, json, time, random, traceback, datetime, urllib.request
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ===== البوت بيصحي نفسه كل 5 دقايق - مش بيقف =====
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers(); self.wfile.write(b"Bot is alive!")
    def log_message(self, *a): pass
def keep_alive():
    try:
        port = int(os.environ.get("PORT", 10000))
        Thread(target=HTTPServer(("0.0.0.0", port), Handler).serve_forever, daemon=True).start()
    except: pass
keep_alive()
def self_ping():
    while True:
        time.sleep(300)
        url = os.environ.get("RENDER_EXTERNAL_URL")
        if url:
            try: urllib.request.urlopen(url, timeout=10); print(f"✅ Ping {time.strftime('%H:%M:%S')}")
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
settings = load_json("settings.json", {"maintenance": False, "banned": [], "lottery": [], "jackpot": 5000, "daily_challenge": None, "clans": {}, "auction": []})
def save(): save_json("data.json", data)
def save_settings(): save_json("settings.json", settings)
pending = {}

def user(uid):
    uid = str(uid)
    if uid not in data:
        data[uid] = {"money":500,"name":"مستخدم","level":1,"xp":0,"vip":False,"vip_until":0,"weapons":[],"daily":0,"spin":0,"gift":0,"streak":0,"score":0,"codes":[],"items":[],"portfolio":{},"bank":0,"bank_current":0,"bank_saving":0,"bank_history":[],"certificates":[],"credit_limit":2000,"credit_used":0,"iban":"","overdraft":0,"steal":0,"lottery_tickets":0,"loans":[],"invest":0,"invest_time":0,"gold_box":0,"last_challenge":0,"pets":[],"clan":None,"wins":0,"losses":0,"gold_spin":0,"guess_num":0}
        save()
    defaults = {"money":500,"level":1,"xp":0,"vip":False,"vip_until":0,"weapons":[],"daily":0,"spin":0,"gift":0,"streak":0,"score":0,"codes":[],"items":[],"portfolio":{},"bank":0,"bank_current":0,"bank_saving":0,"bank_history":[],"certificates":[],"credit_limit":2000,"credit_used":0,"iban":"","overdraft":0,"steal":0,"lottery_tickets":0,"loans":[],"invest":0,"invest_time":0,"gold_box":0,"last_challenge":0,"pets":[],"clan":None,"wins":0,"losses":0,"gold_spin":0,"guess_num":0,"name":"مستخدم"}
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
    lvl=u["xp"]//100+1
    if lvl>u["level"]:
        u["level"]=lvl; bonus=lvl*100; u["money"]+=bonus
        try: bot.send_message(uid, f"🎉 مستوى جديد! وصلت {lvl} 🔥\n🎁 هدية: +{bonus}")
        except: pass
    save(); return amount
def get_rank(money):
    if money >= 500000: return "👑 إمبراطور"
    if money >= 200000: return "💎 ملياردير"
    if money >= 100000: return "🏆 مليونير"
    if money >= 50000: return "💰 غني جدا"
    if money >= 20000: return "🤑 غني"
    if money >= 5000: return "🙂 متوسط"
    if money >= 1000: return "🌱 عادي"
    return "🥺 فقير"
def add_history(uid_str, text):
    uu = user(int(uid_str))
    h = uu.get("bank_history", [])
    h.append(f"{time.strftime('%d/%m %H:%M')} - {text}")
    uu["bank_history"] = h[-20:]
    save()

MARKET = {"btc":{"name":"₿ بيتكوين","price":800},"eth":{"name":"Ξ ايثريوم","price":300},"gold":{"name":"🥇 ذهب","price":150},"usd":{"name":"💵 دولار","price":70},"oil":{"name":"🛢️ بترول","price":120},"diamond":{"name":"💎 الماس","price":2000}}
def update_market_loop():
    while True:
        time.sleep(30)
        try:
            for k in MARKET: MARKET[k]["price"]=max(20, MARKET[k]["price"]+random.randint(-40,60))
        except: pass
Thread(target=update_market_loop, daemon=True).start()
def portfolio_value(u): return sum(qty*MARKET[k]["price"] for k,qty in u.get("portfolio",{}).items() if k in MARKET)
PETS = {"dragon":("🐉 تنين",2000,200),"lion":("🦁 أسد",1000,100),"eagle":("🦅 نسر",500,50),"cat":("🐱 قطة",200,20)}
STORE_OLD = {"bg":("🎨 خلفية موبايل",50),"song":("🎵 اغنية MP3",100),"netflix":("🎬 نتفليكس يوم",200),"pubg":("🎮 ببجي 60 شدة",500),"title":("💎 لقب اسطوري",2000)}
WEAPONS = {"w1":("🔪 سكينة",100,5),"w2":("🔫 مسدس",300,15),"w3":("💣 قنبلة",600,30),"w4":("🚀 بازوكا",1200,60),"w5":("⚔️ سيف اسطوري",2500,120),"w6":("👑 سلاح الإمبراطور",10000,300)}
TASKS=[("سؤال سريع",50),("حظك اليوم",80),("مهمة كلمة السر",150),("تحدي الذاكرة",100)]
CODES={"WELCOME100":500,"MEGA500":2000,"BOSS1000":5000,"ADI2026":10000,"DRAGON":3000}
def power(u): return sum(WEAPONS[w][2] for w in u.get("weapons",[]) if w in WEAPONS) + sum(PETS[p][2] for p in u.get("pets",[]) if p in PETS)
def pet_income(u): return sum(PETS[p][2] for p in u.get("pets",[]) if p in PETS)
def lvl_emoji(l):
    if l>=15: return "👑"
    if l>=10: return "💎"
    if l>=5: return "⭐"
    return "🌱"

def menu(uid):
    m=InlineKeyboardMarkup(row_width=2)
    m.add(
        InlineKeyboardButton("🎮 العب واكسب", callback_data="play"),
        InlineKeyboardButton("📈 تداول", callback_data="trade"),
        InlineKeyboardButton("🏦 البنك الحقيقي", callback_data="bank"),
        InlineKeyboardButton("💎 استثمار", callback_data="invest"),
        InlineKeyboardButton("🐉 حيواناتي", callback_data="pets"),
        InlineKeyboardButton("⚔️ قتال PvP", callback_data="pvp"),
        InlineKeyboardButton("👑 كلان", callback_data="clan"),
        InlineKeyboardButton("🏛️ مزاد", callback_data="auction"),
        InlineKeyboardButton("🛒 المتجر", callback_data="shop"),
        InlineKeyboardButton("👤 بروفايلي", callback_data="me"),
        InlineKeyboardButton("🏆 الأبطال", callback_data="top"),
        InlineKeyboardButton("🎰 كازينو", callback_data="casino"),
        InlineKeyboardButton("🎯 تحدي اليوم", callback_data="challenge"),
        InlineKeyboardButton("🎡 عجلة ذهبية", callback_data="goldspin"),
        InlineKeyboardButton("🧧 ظرف أحمر", callback_data="red"),
        InlineKeyboardButton("💰 فلوسي", callback_data="balance"),
    )
    if is_owner(uid): m.add(InlineKeyboardButton("👑 لوحة الأونر 🔥🔥", callback_data="owner"))
    m.add(InlineKeyboardButton("🔄 تحديث", callback_data="home"))
    return m
def play_menu(uid):
    m=InlineKeyboardMarkup(row_width=2)
    m.add(
        InlineKeyboardButton("📋 المهام", callback_data="tasks"),
        InlineKeyboardButton("🎡 عجلة الحظ", callback_data="spin"),
        InlineKeyboardButton("🎲 لعبة الحظ", callback_data="gamble"),
        InlineKeyboardButton("🎁 صندوق", callback_data="gift"),
        InlineKeyboardButton("📦 صندوق ذهبي", callback_data="goldbox"),
        InlineKeyboardButton("🔢 خمن الرقم", callback_data="guess"),
        InlineKeyboardButton("📅 يومية", callback_data="daily"),
        InlineKeyboardButton("🎁 أكواد", callback_data="codes"),
        InlineKeyboardButton("🏆 مسابقة", callback_data="contest"),
        InlineKeyboardButton("🥷 سرقة", callback_data="steal"),
        InlineKeyboardButton("🎯 مهمة سرية", callback_data="secret"),
        InlineKeyboardButton("💸 قروض (5)", callback_data="loan"),
        InlineKeyboardButton("🔥 سلسلة", callback_data="streak"),
    )
    m.add(InlineKeyboardButton("🔙 رجوع", callback_data="home"))
    return m
def casino_menu(uid):
    m=InlineKeyboardMarkup(row_width=2)
    m.add(InlineKeyboardButton("🎰 سلوت", callback_data="slot"),InlineKeyboardButton("🎲 نرد", callback_data="dice"),InlineKeyboardButton("🃏 ورق", callback_data="cards"),InlineKeyboardButton("💎 يانصيب", callback_data="lottery"))
    m.add(InlineKeyboardButton("🔙 رجوع", callback_data="home"))
    return m
def shop_menu(uid):
    m=InlineKeyboardMarkup()
    m.add(InlineKeyboardButton("🔫 أسلحة", callback_data="weapons"))
    m.add(InlineKeyboardButton("🐉 متجر الحيوانات", callback_data="petshop"))
    m.add(InlineKeyboardButton("👑 VIP - 1000 (×3)", callback_data="vip"))
    m.add(InlineKeyboardButton("🛍️ متجر قديم", callback_data="old_shop"))
    m.add(InlineKeyboardButton("🔙 رجوع", callback_data="home"))
    return m
def trade_menu(uid):
    u=user(uid); m=InlineKeyboardMarkup()
    for k,v in MARKET.items():
        qty=u.get("portfolio",{}).get(k,0)
        m.add(InlineKeyboardButton(f"{v['name']} - {v['price']} | معاك: {qty}", callback_data=f"coin_{k}"))
    m.add(InlineKeyboardButton("💼 محفظتي", callback_data="my_portfolio"))
    m.add(InlineKeyboardButton("🔄 تحديث", callback_data="trade"))
    m.add(InlineKeyboardButton("🔙 رجوع", callback_data="home"))
    return m
def owner_menu():
    m=InlineKeyboardMarkup(row_width=2)
    m.add(
        InlineKeyboardButton("👥 المستخدمين", callback_data="a_users"),
        InlineKeyboardButton("📊 احصائيات", callback_data="a_stats"),
        InlineKeyboardButton("💰 مبلغ مخصوص لحد", callback_data="a_custom"),
        InlineKeyboardButton("💰 مبلغ مخصوص للكل", callback_data="a_custom_all"),
        InlineKeyboardButton("📢 بث", callback_data="a_bc"),
        InlineKeyboardButton("🎁 هدية للكل", callback_data="a_gift_all"),
        InlineKeyboardButton("🔍 بحث ID", callback_data="a_search"),
        InlineKeyboardButton("🛠️ صيانة", callback_data="a_maint"),
        InlineKeyboardButton("🏆 انهي المسابقة", callback_data="a_end"),
        InlineKeyboardButton("💰 ادي الكل", callback_data="a_all_money"),
        InlineKeyboardButton("🎰 سحب يانصيب", callback_data="a_lottery_draw"),
        InlineKeyboardButton("💥 انفجار", callback_data="a_pump"),
        InlineKeyboardButton("📉 انهيار", callback_data="a_crash"),
        InlineKeyboardButton("👑 VIP للكل", callback_data="a_vip_all"),
        InlineKeyboardButton("🐉 حيوان للكل", callback_data="a_pet_all"),
        InlineKeyboardButton("🎯 تحدي جديد", callback_data="a_new_challenge"),
        InlineKeyboardButton("🧹 فك حظر الكل", callback_data="a_clear_ban"),
        InlineKeyboardButton("💎 فلوس لنفسك", callback_data="a_self"),
        InlineKeyboardButton("🏆 بطولة أسبوعية", callback_data="a_weekly"),
    )
    m.add(InlineKeyboardButton("🔙 رجوع", callback_data="home"))
    return m

@bot.message_handler(commands=['start'])
def start(msg):
    if settings.get("maintenance") and not is_owner(msg.from_user.id):
        bot.send_message(msg.chat.id, "🛠️ البوت في الصيانة.. ارجع كمان شوية"); return
    if is_banned(msg.from_user.id):
        bot.send_message(msg.chat.id, "🚫 انت محظور"); return
    u=user(msg.from_user.id); u["name"]=msg.from_user.first_name or "مستخدم"
    if not u.get("iban"):
        u["iban"] = f"EG{random.randint(1000,9999)}{msg.from_user.id}{random.randint(100,999)}"
        save()
    if len(msg.text.split())>1:
        inv=msg.text.split()[1]
        if inv!=str(msg.from_user.id) and inv in data:
            add(int(inv),150)
            try: bot.send_message(int(inv), "🎉 صاحبك دخل! خدت +150 🔥")
            except: pass
    if u.get("pets"):
        inc = pet_income(u); u["money"]+=inc
        try: bot.send_message(msg.chat.id, f"🐉 حيواناتك جابتلك +{inc} وانت نايم!")
        except: pass
    save(); vip=" 👑 VIP ×3" if is_vip(u) else ""
    rank=get_rank(u["money"]+portfolio_value(u)+u.get("bank",0)+u.get("bank_current",0)+u.get("bank_saving",0))
    bot.send_message(msg.chat.id, f"┏━━━━━━━━━━━━━━┓\n┃ 🎮 أهلاً {u['name']}{vip}\n┃ {rank}\n┃ 💰 {u['money']} جنيه\n┃ 🏦 بنك: جاري {u.get('bank_current',0)} | توفير {u.get('bank_saving',0)}\n┃ 🏧 IBAN: {u.get('iban')}\n┃ {lvl_emoji(u['level'])} مستوى {u['level']} | ⭐ {u['xp']} XP\n┃ ⚡ قوة +{power(u)}\n┃ 🐉 حيوانات: {len(u.get('pets',[]))} | دخل +{pet_income(u)}/يوم\n┃ 📈 محفظة: {portfolio_value(u)}\n┗━━━━━━━━━━━━━━┛\n\nاختار 👇", reply_markup=menu(msg.from_user.id))

@bot.message_handler(commands=['give','take','giveall','takeall','money','ping','id','rank','owner','admin'])
def owner_cmd(msg):
    txt = msg.text.split(); cmd = txt[0].replace("/","")
    if cmd=="ping": bot.send_message(msg.chat.id, "✅ البوت شغال وبيصحي نفسه كل 5 دقايق!"); return
    if cmd=="id": bot.send_message(msg.chat.id, f"🆔 ID: `{msg.from_user.id}`", parse_mode="Markdown"); return
    if cmd=="rank":
        u=user(msg.from_user.id); total=u["money"]+portfolio_value(u)+u.get("bank",0); bot.send_message(msg.chat.id, f"👑 رتبتك: {get_rank(total)}\n💰 ثروتك: {total}"); return
    if not is_owner(msg.from_user.id):
        bot.send_message(msg.chat.id, "❌ انت مش الأونر"); return
    if cmd=="money":
        amt = int(txt[1]) if len(txt)>1 and txt[1].isdigit() else 100000
        u=user(msg.from_user.id); u["money"]+=amt; save(); bot.send_message(msg.chat.id, f"💰 اديت لنفسك +{amt}\n💰 معاك {u['money']}"); return
    if cmd=="give":
        if len(txt)<3: bot.send_message(msg.chat.id, "❌ اكتب:\n`/give ID المبلغ`\nمثال: `/give 123456 50000`", parse_mode="Markdown"); return
        tid, amt = txt[1], txt[2]
        if not amt.isdigit(): bot.send_message(msg.chat.id, "❌ المبلغ لازم رقم"); return
        amt=int(amt)
        if tid not in data: bot.send_message(msg.chat.id, "❌ مفيش حد بالـ ID ده"); return
        target=user(int(tid)); target["money"]+=amt; save()
        bot.send_message(msg.chat.id, f"✅ اديت {target.get('name')} +{amt}\n💰 بقى معاه {target['money']}")
        try: bot.send_message(int(tid), f"🎁 الأونر اداك +{amt} جنيه! 🔥")
        except: pass
        return
    if cmd=="take":
        if len(txt)<3: bot.send_message(msg.chat.id, "❌ اكتب: `/take ID المبلغ`", parse_mode="Markdown"); return
        tid, amt = txt[1], txt[2]
        if not amt.isdigit(): bot.send_message(msg.chat.id, "❌ المبلغ لازم رقم"); return
        amt=int(amt)
        if tid not in data: bot.send_message(msg.chat.id, "❌ مفيش حد بالـ ID ده"); return
        target=user(int(tid)); target["money"]=max(0, target["money"]-amt); save()
        bot.send_message(msg.chat.id, f"✅ سحبت من {target.get('name')} -{amt}\n💰 بقى معاه {target['money']}"); return
    if cmd=="giveall":
        if len(txt)<2 or not txt[1].isdigit(): bot.send_message(msg.chat.id, "❌ اكتب: `/giveall المبلغ`", parse_mode="Markdown"); return
        amt=int(txt[1])
        for k in data: data[k]["money"]+=amt
        save(); bot.send_message(msg.chat.id, f"✅ اديت {amt} لكل الناس ({len(data)})"); return
    if cmd=="takeall":
        if len(txt)<2 or not txt[1].isdigit(): bot.send_message(msg.chat.id, "❌ اكتب: `/takeall المبلغ`", parse_mode="Markdown"); return
        amt=int(txt[1])
        for k in data: data[k]["money"]=max(0, data[k]["money"]-amt)
        save(); bot.send_message(msg.chat.id, f"✅ سحبت {amt} من الكل"); return
    if cmd in ["owner","admin"]:
        bot.send_message(msg.chat.id, "👑 لوحة الأونر 🔥🔥", reply_markup=owner_menu()); return

@bot.message_handler(func=lambda m: m.text and is_owner(m.from_user.id))
def owner_text(msg):
    uid = msg.from_user.id; txt = msg.text.strip()
    if uid in pending:
        p = pending[uid]
        if p.get("action")=="wait_transfer_id":
            if txt not in data: bot.send_message(msg.chat.id, "❌ مفيش حد بالـ ID ده"); return
            pending[uid]={"action":"wait_transfer_amt", "target":txt}
            bot.send_message(msg.chat.id, f"✅ هتحول لـ {data[txt].get('name')}\nاكتب المبلغ"); return
        if p.get("action")=="wait_transfer_amt":
            if not txt.isdigit(): bot.send_message(msg.chat.id, "❌ اكتب رقم بس"); return
            amt=int(txt); tid=p["target"]; uu=user(uid); fee=5
            if uu["money"]<amt+fee: bot.send_message(msg.chat.id, f"❌ محتاج {amt+fee}"); return
            uu["money"]-=amt+fee; target=user(int(tid)); target["money"]+=amt; save(); del pending[uid]
            bot.send_message(msg.chat.id, f"✅ حولت {amt} لـ {target.get('name')}\n💸 رسوم: {fee}")
            try: bot.send_message(int(tid), f"🔄 جالك تحويل {amt} من {uu['name']}!")
            except: pass
            return
        if txt.isdigit():
            amt = int(txt)
            if amt <= 0 or amt > 100000000: bot.send_message(msg.chat.id, "❌ اكتب رقم بين 1 و 100 مليون"); return
            if p["action"] == "custom_all":
                for k in data: data[k]["money"]+=amt
                save(); del pending[uid]; bot.send_message(msg.chat.id, f"✅ اديت {amt} لكل الناس ({len(data)}) 🔥", reply_markup=owner_menu()); return
            if p["action"] == "custom_one":
                tid = p["target"]
                if tid not in data: del pending[uid]; bot.send_message(msg.chat.id, "❌ الشخص ده مش موجود"); return
                target=user(int(tid)); target["money"]+=amt; save(); del pending[uid]
                bot.send_message(msg.chat.id, f"✅ اديت {target.get('name')} +{amt}\n💰 بقى معاه {target['money']}", reply_markup=owner_menu())
                try: bot.send_message(int(tid), f"🎁 الأونر اداك +{amt} جنيه! 🔥")
                except: pass
                return
            if p["action"] == "custom_take":
                tid = p["target"]; target=user(int(tid)); target["money"]=max(0, target["money"]-amt); save(); del pending[uid]
                bot.send_message(msg.chat.id, f"✅ سحبت من {target.get('name')} -{amt}", reply_markup=owner_menu()); return
            if p["action"] == "custom_bank":
                tid = p["target"]; target=user(int(tid)); target["bank_saving"]=target.get("bank_saving",0)+amt; save(); del pending[uid]
                bot.send_message(msg.chat.id, f"✅ حطيت {target.get('name')} {amt} في التوفير", reply_markup=owner_menu()); return
        if p["action"] == "wait_id" and txt.isdigit():
            if txt not in data: bot.send_message(msg.chat.id, "❌ مفيش حد بالـ ID ده"); return
            pending[uid] = {"target": txt, "action": "custom_one"}
            bot.send_message(msg.chat.id, f"✅ لقيت {data[txt].get('name')} - معاه {data[txt].get('money')}\n\nدلوقتي اكتب المبلغ\nمثال: `50000`"); return
        bot.send_message(msg.chat.id, "❌ اكتب رقم بس\nمثال: `50000`"); return
    if txt.isdigit() and txt in data:
        tid = txt; info=user(int(tid))
        m=InlineKeyboardMarkup(row_width=3)
        m.add(InlineKeyboardButton("💰 مبلغ مخصوص ➕", callback_data=f"custom_{tid}"), InlineKeyboardButton("💸 اسحب مبلغ ➖", callback_data=f"ctake_{tid}"))
        m.add(InlineKeyboardButton("➕1000", callback_data=f"add_{tid}_1000"), InlineKeyboardButton("➕10000", callback_data=f"add_{tid}_10000"), InlineKeyboardButton("💎 1M", callback_data=f"add_{tid}_1000000"))
        m.add(InlineKeyboardButton("➖1000", callback_data=f"sub_{tid}_1000"), InlineKeyboardButton("💥 تصفير", callback_data=f"zero_{tid}"), InlineKeyboardButton("👑 VIP", callback_data=f"gv_{tid}"))
        m.add(InlineKeyboardButton("👑 VIP اسبوع", callback_data=f"gv7_{tid}"), InlineKeyboardButton("❌ شيل VIP", callback_data=f"rmvip_{tid}"), InlineKeyboardButton("🚫 حظر", callback_data=f"ban_{tid}"))
        m.add(InlineKeyboardButton("✅ فك حظر", callback_data=f"unban_{tid}"), InlineKeyboardButton("🔫 سلاح", callback_data=f"givew_{tid}"), InlineKeyboardButton("🐉 تنين", callback_data=f"givepet_{tid}_dragon"))
        m.add(InlineKeyboardButton("🏦 حط في بنكه", callback_data=f"cbank_{tid}"), InlineKeyboardButton("🙏 سامحه في القروض", callback_data=f"forgive_{tid}"), InlineKeyboardButton("📋 كشف حسابه", callback_data=f"a_statement_{tid}"))
        m.add(InlineKeyboardButton("🔙 لوحة", callback_data="owner"))
        bot.send_message(msg.chat.id, f"👤 {info.get('name')}\n🆔 {tid}\n💰 {info['money']}\n🏦 توفير: {info.get('bank_saving',0)} | جاري: {info.get('bank_current',0)}\n⭐ مستوى {info['level']}\n👑 VIP: {'✅' if is_vip(info) else '❌'}\n💸 قروض: {len(info.get('loans',[]))}", reply_markup=m); return
    if txt.isdigit() and txt not in data:
        bot.send_message(msg.chat.id, "❌ مفيش حد بالـ ID ده"); return

@bot.callback_query_handler(func=lambda c: True)
def btn(call):
    uid=call.from_user.id; u=user(uid); cid=call.message.chat.id; d=call.data
    try: bot.answer_callback_query(call.id)
    except: pass
    try:
        if settings.get("maintenance") and not is_owner(uid) and d not in ["home"]:
            bot.send_message(cid, "🛠️ البوت في الصيانة"); return
        if is_banned(uid) and not is_owner(uid):
            bot.send_message(cid, "🚫 انت محظور"); return
        if d=="home": bot.send_message(cid, f"🏠 الرئيسية\n💰 معاك {u['money']} | مستوى {u['level']}", reply_markup=menu(uid)); return
        if d=="balance":
            total=u["money"]+portfolio_value(u)+u.get("bank",0)+u.get("bank_current",0)+u.get("bank_saving",0)+u.get("invest",0)+sum(c["amount"] for c in u.get("certificates",[]))
            bot.send_message(cid, f"💰 ثروتك الكلية: {total}\n━━━━━━━━━━\n💵 كاش: {u['money']}\n🏦 جاري: {u.get('bank_current',0)}\n💰 توفير: {u.get('bank_saving',0)}\n📜 شهادات: {sum(c['amount'] for c in u.get('certificates',[]))}\n📈 محفظة: {portfolio_value(u)}\n💎 استثمار: {u.get('invest',0)}\n🐉 دخل حيوانات: +{pet_income(u)}\n👑 رتبتك: {get_rank(total)}\n⭐ XP: {u['xp']} | مستوى {u['level']}", reply_markup=menu(uid)); return
        if d=="play": bot.send_message(cid, f"🎮 العب واكسب\n💰 معاك {u['money']}", reply_markup=play_menu(uid)); return
        if d=="casino": bot.send_message(cid, f"🎰 الكازينو\n💰 معاك {u['money']}\n🎰 الجاكبوت: {settings.get('jackpot',5000)}", reply_markup=casino_menu(uid)); return
        if d=="shop": bot.send_message(cid, f"🛒 المتجر\n💰 معاك {u['money']}", reply_markup=shop_menu(uid)); return
        if d=="me":
            w=", ".join([WEAPONS[x][0] for x in u.get("weapons",[]) if x in WEAPONS]) or "مفيش"
            pets=", ".join([PETS[x][0] for x in u.get("pets",[]) if x in PETS]) or "مفيش"
            total=u["money"]+portfolio_value(u)+u.get("bank",0)+u.get("bank_current",0)+u.get("bank_saving",0)+u.get("invest",0)
            bot.send_message(cid, f"👤 بروفايلك\n━━━━━━━━━━\n📛 {u['name']}\n🆔 {uid}\n🏧 IBAN: {u.get('iban')}\n{get_rank(total)}\n💰 كاش: {u['money']}\n🏦 جاري: {u.get('bank_current',0)} | توفير: {u.get('bank_saving',0)}\n📈 محفظة: {portfolio_value(u)}\n💎 ثروة كلية: {total}\n{lvl_emoji(u['level'])} مستوى {u['level']} | XP {u['xp']}\n🔥 سلسلة {u.get('streak',0)}\n🏆 نقاط {u.get('score',0)}\n🔫 {w}\n🐉 {pets} (+{pet_income(u)}/يوم)\n💳 فيزا: {u.get('credit_used',0)}/{u.get('credit_limit',2000)}\n💸 قروض: {len(u.get('loans',[]))}/5\n👑 VIP: {'✅ ×3' if is_vip(u) else '❌'}", reply_markup=menu(uid)); return
        if d=="top":
            top=sorted(data.items(), key=lambda x: x[1].get('money',0)+portfolio_value(x[1])+x[1].get('bank',0)+x[1].get('bank_current',0)+x[1].get('bank_saving',0)+x[1].get('invest',0), reverse=True)[:10]
            txt="🏆 ترتيب الأغنياء\n━━━━━━━━━━\n"; medals=["🥇","🥈","🥉","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
            for i,(k,v) in enumerate(top):
                total=v.get('money',0)+portfolio_value(v)+v.get('bank',0)+v.get('bank_current',0)+v.get('bank_saving',0)+v.get('invest',0)
                txt+=f"{medals[i]} {v.get('name','?')} — {total} 💰 | {get_rank(total)}\n"
            bot.send_message(cid, txt, reply_markup=menu(uid)); return
        if d=="invite":
            try: username=bot.get_me().username
            except: username="bot"
            bot.send_message(cid, f"👥 ابعت لصاحبك:\nhttps://t.me/{username}?start={uid}\nلو دخل هتاخد +150 🔥", reply_markup=menu(uid)); return
        if d=="streak": bot.send_message(cid, f"🔥 سلسلتك: {u.get('streak',0)} يوم", reply_markup=play_menu(uid)); return
        if d=="pets":
            pets=", ".join([PETS[x][0] for x in u.get("pets",[]) if x in PETS]) or "مفيش"
            m=InlineKeyboardMarkup(); m.add(InlineKeyboardButton("🛒 اشتري حيوان", callback_data="petshop")); m.add(InlineKeyboardButton("💰 اجمع دخل", callback_data="collect_pet")); m.add(InlineKeyboardButton("🔙", callback_data="home"))
            bot.send_message(cid, f"🐉 حيواناتك\n{pets}\n💰 دخل يومي: +{pet_income(u)}", reply_markup=m); return
        if d=="petshop":
            m=InlineKeyboardMarkup()
            for k,(name,price,inc) in PETS.items():
                owned=" ✅ معاك" if k in u.get("pets",[]) else f" — {price}"
                m.add(InlineKeyboardButton(f"{name} | دخل +{inc}/يوم{owned}", callback_data=f"buypet_{k}"))
            m.add(InlineKeyboardButton("🔙", callback_data="pets")); bot.send_message(cid, f"🐉 متجر الحيوانات\n💰 معاك {u['money']}", reply_markup=m); return
        if d.startswith("buypet_"):
            k=d.replace("buypet_",""); name,price,inc=PETS[k]
            if k in u.get("pets",[]): bot.send_message(cid, "معاك ده ✅", reply_markup=shop_menu(uid)); return
            if u["money"]>=price: u["money"]-=price; u["pets"].append(k); save(); bot.send_message(cid, f"🎉 اشتريت {name}!", reply_markup=menu(uid))
            else: bot.send_message(cid, "❌ فلوسك مش كفاية", reply_markup=shop_menu(uid))
            return
        if d=="collect_pet":
            inc=pet_income(u)
            if inc==0: bot.send_message(cid, "❌ معندكش حيوانات", reply_markup=menu(uid)); return
            u["money"]+=inc; save(); bot.send_message(cid, f"🐉 جمعت +{inc}", reply_markup=menu(uid)); return
        if d=="pvp":
            m=InlineKeyboardMarkup()
            others=[(k,v) for k,v in data.items() if k!=str(uid) and v.get("money",0)>100][:10]
            if not others: bot.send_message(cid, "❌ مفيش حد تحاربه", reply_markup=menu(uid)); return
            for k,v in others: m.add(InlineKeyboardButton(f"⚔️ {v.get('name')} - قوة {power(v)}", callback_data=f"fight_{k}"))
            m.add(InlineKeyboardButton("🔙", callback_data="home")); bot.send_message(cid, f"⚔️ اختار حد تحاربه\n⚡ قوتك: {power(u)}", reply_markup=m); return
        if d.startswith("fight_"):
            tid=d.replace("fight_",""); enemy=user(int(tid)); my_p=power(u)+random.randint(0,50); en_p=power(enemy)+random.randint(0,50)
            if my_p>=en_p:
                win=min(500, enemy["money"]//2); enemy["money"]-=win; u["money"]+=win; u["wins"]=u.get("wins",0)+1; save()
                bot.send_message(cid, f"🎉 كسبت! خدت {win} من {enemy.get('name')}", reply_markup=menu(uid))
            else:
                lose=min(200, u["money"]//4); u["money"]=max(0,u["money"]-lose); enemy["money"]+=lose; save()
                bot.send_message(cid, f"😢 خسرت! خسرت {lose}", reply_markup=menu(uid))
            return
        if d=="clan":
            clans=settings.get("clans",{})
            if u.get("clan") and u["clan"] in clans:
                c=clans[u["clan"]]; m=InlineKeyboardMarkup(); m.add(InlineKeyboardButton("💰 خد +500", callback_data="clan_bonus")); m.add(InlineKeyboardButton("🚪 اخرج", callback_data="clan_leave")); m.add(InlineKeyboardButton("🔙", callback_data="home"))
                bot.send_message(cid, f"👑 كلان {c['name']}\n👥 {len(c.get('members',[]))} عضو", reply_markup=m); return
            m=InlineKeyboardMarkup()
            for cid2,c in list(clans.items())[:10]: m.add(InlineKeyboardButton(f"👑 {c['name']} - {len(c.get('members',[]))} عضو", callback_data=f"join_{cid2}"))
            m.add(InlineKeyboardButton("➕ اعمل كلان - 1000", callback_data="create_clan")); m.add(InlineKeyboardButton("🔙", callback_data="home"))
            bot.send_message(cid, "👑 الكلانات", reply_markup=m); return
        if d=="create_clan":
            if u["money"]<1000: bot.send_message(cid, "❌ محتاج 1000", reply_markup=menu(uid)); return
            u["money"]-=1000; clan_id=str(uid); settings.setdefault("clans",{})[clan_id]={"name":f"كلان {u['name']}","leader":str(uid),"leader_name":u["name"],"members":[str(uid)]}; u["clan"]=clan_id; save(); save_settings(); bot.send_message(cid, f"🎉 عملت كلان {u['name']}!", reply_markup=menu(uid)); return
        if d.startswith("join_"):
            cid2=d.replace("join_","")
            if cid2 in settings.get("clans",{}):
                settings["clans"][cid2].setdefault("members",[]).append(str(uid)); u["clan"]=cid2; save(); save_settings(); bot.send_message(cid, f"✅ دخلت كلان {settings['clans'][cid2]['name']}", reply_markup=menu(uid))
            return
        if d=="clan_bonus": got=add(uid, 500); bot.send_message(cid, f"👑 مكافأة +{got}", reply_markup=menu(uid)); return
        if d=="clan_leave":
            if u.get("clan") in settings.get("clans",{}):
                try: settings["clans"][u["clan"]]["members"].remove(str(uid))
                except: pass
            u["clan"]=None; save(); save_settings(); bot.send_message(cid, "🚪 خرجت من الكلان", reply_markup=menu(uid)); return
        if d=="auction":
            auc=settings.get("auction",[])
            if not auc: bot.send_message(cid, "🏛️ المزاد فاضي", reply_markup=menu(uid)); return
            m=InlineKeyboardMarkup()
            for i,item in enumerate(auc[:10]): m.add(InlineKeyboardButton(f"{item['name']} - {item['price']} من {item['seller_name']}", callback_data=f"buyauc_{i}"))
            m.add(InlineKeyboardButton("➕ اعرض سلاحي", callback_data="sell_auction")); m.add(InlineKeyboardButton("🔙", callback_data="home"))
            bot.send_message(cid, "🏛️ المزاد", reply_markup=m); return
        if d=="sell_auction":
            if not u.get("weapons"): bot.send_message(cid, "❌ معندكش سلاح", reply_markup=menu(uid)); return
            m=InlineKeyboardMarkup()
            for w in u.get("weapons",[]): m.add(InlineKeyboardButton(f"بيع {WEAPONS[w][0]} - 500", callback_data=f"listauc_{w}"))
            m.add(InlineKeyboardButton("🔙", callback_data="home")); bot.send_message(cid, "اختر سلاح:", reply_markup=m); return
        if d.startswith("listauc_"):
            w=d.replace("listauc_",""); u["weapons"].remove(w); settings.setdefault("auction",[]).append({"weapon":w,"name":WEAPONS[w][0],"price":500,"seller":str(uid),"seller_name":u["name"]}); save(); save_settings(); bot.send_message(cid, f"✅ عرضت {WEAPONS[w][0]} بـ 500", reply_markup=menu(uid)); return
        if d.startswith("buyauc_"):
            idx=int(d.replace("buyauc_","")); auc=settings.get("auction",[])
            if idx>=len(auc): bot.send_message(cid, "❌ اتباع خلاص", reply_markup=menu(uid)); return
            item=auc[idx]
            if u["money"]<item["price"]: bot.send_message(cid, "❌ فلوسك مش كفاية", reply_markup=menu(uid)); return
            u["money"]-=item["price"]; u["weapons"].append(item["weapon"]); seller=user(int(item["seller"])); seller["money"]+=item["price"]; settings["auction"].pop(idx); save(); save_settings(); bot.send_message(cid, f"✅ اشتريت {item['name']}", reply_markup=menu(uid)); return
        if d=="goldspin":
            today=datetime.date.today().isoformat()
            if u.get("gold_spin")==today: bot.send_message(cid, "❌ لعبت النهاردة.. تعالى بكرة", reply_markup=menu(uid)); return
            u["gold_spin"]=today; win=random.choice([500,1000,2000,5000,10000]); u["money"]+=win; save(); bot.send_message(cid, f"🎡 العجلة الذهبية!\n🎉 +{win} 🔥", reply_markup=menu(uid)); return
        if d=="red":
            m=InlineKeyboardMarkup()
            others=[(k,v) for k,v in data.items() if k!=str(uid)][:10]
            for k,v in others: m.add(InlineKeyboardButton(f"🧧 ابعت 200 لـ {v.get('name')}", callback_data=f"red_{k}"))
            m.add(InlineKeyboardButton("🔙", callback_data="home")); bot.send_message(cid, "🧧 ابعت ظرف أحمر", reply_markup=m); return
        if d.startswith("red_"):
            tid=d.replace("red_","")
            if u["money"]<200: bot.send_message(cid, "❌ محتاج 200", reply_markup=menu(uid)); return
            u["money"]-=200; target=user(int(tid)); target["money"]+=300; save(); bot.send_message(cid, f"🧧 بعت ظرف لـ {target.get('name')}", reply_markup=menu(uid))
            try: bot.send_message(int(tid), f"🧧 {u['name']} بعتلك ظرف! +300")
            except: pass
            return
        if d=="guess":
            u["guess_num"]=random.randint(1,5); save()
            m=InlineKeyboardMarkup(row_width=5)
            for i in range(1,6): m.add(InlineKeyboardButton(f"{i}", callback_data=f"guess_{i}"))
            m.add(InlineKeyboardButton("🔙", callback_data="play")); bot.send_message(cid, "🔢 خمن رقم من 1 لـ 5 - لو صح +2000!", reply_markup=m); return
        if d.startswith("guess_"):
            pick=int(d.replace("guess_","")); target=u.get("guess_num",0)
            if pick==target: got=add(uid, 2000); bot.send_message(cid, f"🎉 صح! +{got} 🔥", reply_markup=play_menu(uid))
            else: bot.send_message(cid, f"😢 غلط.. الرقم كان {target}", reply_markup=play_menu(uid))
            return
        # ===== البنك الحقيقي =====
        if d=="bank":
            m=InlineKeyboardMarkup(row_width=2)
            m.add(InlineKeyboardButton("💵 حساب جاري", callback_data="bank_current"))
            m.add(InlineKeyboardButton("💰 حساب توفير 25%", callback_data="bank_saving"))
            m.add(InlineKeyboardButton("📜 شهادات استثمار", callback_data="certs"))
            m.add(InlineKeyboardButton("💳 بطاقة ائتمان (فيزا)", callback_data="credit"))
            m.add(InlineKeyboardButton("🔄 تحويل فلوس (انستا باي)", callback_data="transfer"))
            m.add(InlineKeyboardButton("💰 وديعة 100%", callback_data="deposit_box"))
            m.add(InlineKeyboardButton("📋 كشف حساب", callback_data="statement"))
            m.add(InlineKeyboardButton("🏧 سحب على المكشوف", callback_data="overdraft"))
            m.add(InlineKeyboardButton("🔙 رجوع", callback_data="home"))
            total_bank = u.get("bank",0)+u.get("bank_current",0)+u.get("bank_saving",0)+sum(c["amount"] for c in u.get("certificates",[]))
            bot.send_message(cid, f"🏦 البنك المركزي 🔥\n━━━━━━━━━━\n👤 {u['name']}\n🏧 IBAN: `{u.get('iban','-')}`\n━━━━━━━━━━\n💵 كاش: {u['money']}\n💵 جاري: {u.get('bank_current',0)}\n💰 توفير: {u.get('bank_saving',0)} (25%)\n📜 شهادات: {sum(c['amount'] for c in u.get('certificates',[]))}\n💳 فيزا: {u.get('credit_used',0)}/{u.get('credit_limit',2000)}\n🏧 مكشوف: {u.get('overdraft',0)}\n💎 إجمالي في البنك: {total_bank}", reply_markup=m, parse_mode="Markdown"); return
        if d=="bank_current":
            m=InlineKeyboardMarkup(row_width=2)
            m.add(InlineKeyboardButton("➕ ايداع 500 جاري", callback_data="cur_dep_500"))
            m.add(InlineKeyboardButton("➕ ايداع 5000 جاري", callback_data="cur_dep_5000"))
            m.add(InlineKeyboardButton("➕ ايداع الكل", callback_data="cur_dep_all"))
            m.add(InlineKeyboardButton("➖ سحب 500 جاري", callback_data="cur_with_500"))
            m.add(InlineKeyboardButton("➖ سحب الكل", callback_data="cur_with_all"))
            m.add(InlineKeyboardButton("🔙 بنك", callback_data="bank"))
            bot.send_message(cid, f"💵 حساب جاري\n💵 فيه: {u.get('bank_current',0)}\n💰 كاش: {u['money']}\n\nالجاري من غير فايدة بس تسحب في أي وقت", reply_markup=m); return
        if d.startswith("cur_dep_"):
            amt = u["money"] if d=="cur_dep_all" else int(d.replace("cur_dep_",""))
            if u["money"]<amt or amt<=0: bot.send_message(cid, "❌ فلوسك مش كفاية", reply_markup=menu(uid)); return
            u["money"]-=amt; u["bank_current"]=u.get("bank_current",0)+amt; save(); add_history(uid, f"ايداع جاري +{amt}")
            bot.send_message(cid, f"✅ حطيت {amt} في الجاري\n💵 في الجاري: {u['bank_current']}", reply_markup=menu(uid)); return
        if d.startswith("cur_with_"):
            amt = u.get("bank_current",0) if d=="cur_with_all" else int(d.replace("cur_with_",""))
            if u.get("bank_current",0)<amt or amt<=0: bot.send_message(cid, "❌ مفيش في الجاري كفاية", reply_markup=menu(uid)); return
            u["bank_current"]-=amt; u["money"]+=amt; save(); add_history(uid, f"سحب جاري -{amt}")
            bot.send_message(cid, f"✅ سحبت {amt}", reply_markup=menu(uid)); return
        if d=="bank_saving":
            profit = int(u.get("bank_saving",0)*0.25)
            m=InlineKeyboardMarkup(row_width=2)
            m.add(InlineKeyboardButton("➕ ايداع 500 توفير", callback_data="sav_dep_500"))
            m.add(InlineKeyboardButton("➕ ايداع 5000 توفير", callback_data="sav_dep_5000"))
            m.add(InlineKeyboardButton("➕ ايداع الكل توفير", callback_data="sav_dep_all"))
            m.add(InlineKeyboardButton("➖ سحب 500 توفير", callback_data="sav_with_500"))
            m.add(InlineKeyboardButton("➖ سحب الكل", callback_data="sav_with_all"))
            m.add(InlineKeyboardButton(f"📈 خد الفايدة +{profit} (25%)", callback_data="interest"))
            m.add(InlineKeyboardButton("🔙 بنك", callback_data="bank"))
            bot.send_message(cid, f"💰 حساب توفير\n💰 فيه: {u.get('bank_saving',0)}\n📈 فايدتك: {profit} (25%)\n💵 كاش: {u['money']}", reply_markup=m); return
        if d.startswith("sav_dep_"):
            amt = u["money"] if d=="sav_dep_all" else int(d.replace("sav_dep_",""))
            if u["money"]<amt or amt<=0: bot.send_message(cid, "❌ فلوسك مش كفاية", reply_markup=menu(uid)); return
            u["money"]-=amt; u["bank_saving"]=u.get("bank_saving",0)+amt; save(); add_history(uid, f"ايداع توفير +{amt}")
            bot.send_message(cid, f"✅ حطيت {amt} في التوفير\n📈 هتاخد {int(amt*0.25)} فايدة", reply_markup=menu(uid)); return
        if d.startswith("sav_with_"):
            amt = u.get("bank_saving",0) if d=="sav_with_all" else int(d.replace("sav_with_",""))
            if u.get("bank_saving",0)<amt or amt<=0: bot.send_message(cid, "❌ مفيش في التوفير كفاية", reply_markup=menu(uid)); return
            u["bank_saving"]-=amt; u["money"]+=amt; save(); add_history(uid, f"سحب توفير -{amt}")
            bot.send_message(cid, f"✅ سحبت {amt}", reply_markup=menu(uid)); return
        if d=="interest":
            if u.get("bank_saving",0)<=0 and u.get("bank",0)<=0: bot.send_message(cid, "❌ حط فلوس في التوفير الأول", reply_markup=menu(uid)); return
            base = u.get("bank_saving",0) + u.get("bank",0)
            profit=int(base*0.25); u["money"]+=profit; save(); add_history(uid, f"فايدة توفير +{profit}")
            bot.send_message(cid, f"📈 خدت فايدة +{profit} 🔥", reply_markup=menu(uid)); return
        if d=="certs":
            m=InlineKeyboardMarkup(row_width=1)
            m.add(InlineKeyboardButton("📜 شهادة 3 شهور - 40% - 1000", callback_data="cert_1000_40"))
            m.add(InlineKeyboardButton("📜 شهادة 6 شهور - 70% - 5000", callback_data="cert_5000_70"))
            m.add(InlineKeyboardButton("📜 شهادة سنة - 150% - 20000", callback_data="cert_20000_150"))
            m.add(InlineKeyboardButton("💰 فك الشهادات وخد فلوسك + الفايدة", callback_data="cert_break"))
            m.add(InlineKeyboardButton("🔙 بنك", callback_data="bank"))
            certs_txt = ""
            for i,c in enumerate(u.get("certificates",[])):
                certs_txt += f"{i+1}. {c['amount']} - فايدة {c['rate']}% - هتاخد {int(c['amount']*(1+c['rate']/100))}\n"
            if not certs_txt: certs_txt = "مفيش شهادات"
            bot.send_message(cid, f"📜 شهادات الاستثمار\n━━━━━━━━━━\n{certs_txt}\n💰 كاش: {u['money']}", reply_markup=m); return
        if d.startswith("cert_") and d!="cert_break":
            _,amt,rate=d.split("_"); amt=int(amt); rate=int(rate)
            if u["money"]<amt: bot.send_message(cid, f"❌ محتاج {amt}", reply_markup=menu(uid)); return
            u["money"]-=amt; u.setdefault("certificates",[]).append({"amount":amt,"rate":rate,"time":int(time.time())}); save(); add_history(uid, f"شهادة {amt} بفايدة {rate}%")
            bot.send_message(cid, f"✅ عملت شهادة {amt} بفايدة {rate}%\nلما تفكها هتاخد {int(amt*(1+rate/100))}", reply_markup=menu(uid)); return
        if d=="cert_break":
            certs=u.get("certificates",[])
            if not certs: bot.send_message(cid, "❌ معندكش شهادات", reply_markup=menu(uid)); return
            total=sum(int(c["amount"]*(1+c["rate"]/100)) for c in certs)
            u["money"]+=total; u["certificates"]=[]; save(); add_history(uid, f"فك شهادات +{total}")
            bot.send_message(cid, f"💰 فكيت كل الشهادات!\n✅ خدت {total} 🔥", reply_markup=menu(uid)); return
        if d=="credit":
            limit=u.get("credit_limit",2000); used=u.get("credit_used",0); avail=limit-used
            m=InlineKeyboardMarkup(row_width=2)
            m.add(InlineKeyboardButton("🛒 اشتري بالفيزا 500", callback_data="cc_buy_500"))
            m.add(InlineKeyboardButton("🛒 اشتري بالفيزا 1000", callback_data="cc_buy_1000"))
            m.add(InlineKeyboardButton("💳 سدد الفيزا", callback_data="cc_pay"))
            m.add(InlineKeyboardButton("⬆️ زود حد الفيزا - 5000", callback_data="cc_upgrade"))
            m.add(InlineKeyboardButton("🔙 بنك", callback_data="bank"))
            bot.send_message(cid, f"💳 بطاقة ائتمان (فيزا)\n💳 الحد: {limit}\n💳 مستخدم: {used}\n💳 متاح: {avail}\n💰 كاش: {u['money']}", reply_markup=m); return
        if d.startswith("cc_buy_"):
            amt=int(d.replace("cc_buy_",""))
            avail=u.get("credit_limit",2000)-u.get("credit_used",0)
            if amt>avail: bot.send_message(cid, f"❌ حد الفيزا مش كفاية.. متاح {avail}", reply_markup=menu(uid)); return
            u["credit_used"]=u.get("credit_used",0)+amt; u["money"]+=amt; save(); add_history(uid, f"شراء فيزا +{amt}")
            bot.send_message(cid, f"✅ اشتريت بالفيزا {amt}\n💳 مستخدم: {u['credit_used']}/{u['credit_limit']}", reply_markup=menu(uid)); return
        if d=="cc_pay":
            used=u.get("credit_used",0)
            if used<=0: bot.send_message(cid, "✅ الفيزا متسددة", reply_markup=menu(uid)); return
            if u["money"]<used: bot.send_message(cid, f"❌ محتاج {used} عشان تسدد", reply_markup=menu(uid)); return
            u["money"]-=used; u["credit_used"]=0; save(); add_history(uid, f"سداد فيزا -{used}")
            bot.send_message(cid, f"✅ سددت الفيزا {used}", reply_markup=menu(uid)); return
        if d=="cc_upgrade":
            if u["money"]<5000: bot.send_message(cid, "❌ محتاج 5000 عشان تزود الحد", reply_markup=menu(uid)); return
            u["money"]-=5000; u["credit_limit"]=u.get("credit_limit",2000)+2000; save()
            bot.send_message(cid, f"✅ زودت حد الفيزا!\n💳 الحد الجديد: {u['credit_limit']}", reply_markup=menu(uid)); return
        if d=="transfer":
            pending[uid]={"action":"wait_transfer_id"}
            bot.send_message(cid, "🔄 تحويل فلوس - زي انستا باي\n\nابعت ID الشخص اللي عايز تحوله\n\nرسوم التحويل: 5 جنيه", reply_markup=menu(uid)); return
        if d=="deposit_box":
            m=InlineKeyboardMarkup()
            m.add(InlineKeyboardButton("💰 وديعة 1000 - خد 2000", callback_data="wd_1000"))
            m.add(InlineKeyboardButton("💰 وديعة 5000 - خد 10000", callback_data="wd_5000"))
            m.add(InlineKeyboardButton("🔙 بنك", callback_data="bank"))
            bot.send_message(cid, f"💰 الوديعة\nحط فلوس وسيبها وخد ضعفها!\n💵 كاش: {u['money']}", reply_markup=m); return
        if d.startswith("wd_"):
            amt=int(d.replace("wd_",""))
            if u["money"]<amt: bot.send_message(cid, "❌ فلوسك مش كفاية", reply_markup=menu(uid)); return
            u["money"]-=amt; u.setdefault("certificates",[]).append({"amount":amt,"rate":100,"time":int(time.time())}); save(); add_history(uid, f"وديعة {amt}")
            bot.send_message(cid, f"✅ عملت وديعة {amt}\nلما تفكها هتاخد {amt*2}", reply_markup=menu(uid)); return
        if d=="statement":
            hist=u.get("bank_history",[])
            if not hist: bot.send_message(cid, "📋 كشف حسابك فاضي.. لسه معملتش عمليات", reply_markup=menu(uid)); return
            txt="📋 كشف حسابك - آخر 20 عملية\n━━━━━━━━━━\n" + "\n".join(hist)
            bot.send_message(cid, txt, reply_markup=menu(uid)); return
        if d=="overdraft":
            if u.get("overdraft",0)>=1000: bot.send_message(cid, "❌ وصلت لحد المكشوف 1000", reply_markup=menu(uid)); return
            m=InlineKeyboardMarkup(); m.add(InlineKeyboardButton("🏧 اسحب 500 على المكشوف", callback_data="od_500")); m.add(InlineKeyboardButton("✅ سدد المكشوف", callback_data="od_pay")); m.add(InlineKeyboardButton("🔙 بنك", callback_data="bank"))
            bot.send_message(cid, f"🏧 سحب على المكشوف\nعليك مكشوف: {u.get('overdraft',0)}/1000\n💰 كاش: {u['money']}", reply_markup=m); return
        if d.startswith("od_") and d!="od_pay":
            amt=int(d.replace("od_",""))
            if u.get("overdraft",0)+amt>1000: bot.send_message(cid, "❌ هتعدي حد المكشوف", reply_markup=menu(uid)); return
            u["money"]+=amt; u["overdraft"]=u.get("overdraft",0)+amt; save(); add_history(uid, f"مكشوف +{amt}")
            bot.send_message(cid, f"✅ سحبت {amt} على المكشوف", reply_markup=menu(uid)); return
        if d=="od_pay":
            od=u.get("overdraft",0)
            if od<=0: bot.send_message(cid, "✅ معليكش مكشوف", reply_markup=menu(uid)); return
            if u["money"]<od: bot.send_message(cid, f"❌ محتاج {od} عشان تسدد", reply_markup=menu(uid)); return
            u["money"]-=od; u["overdraft"]=0; save(); add_history(uid, f"سداد مكشوف -{od}")
            bot.send_message(cid, f"✅ سددت المكشوف {od}", reply_markup=menu(uid)); return
        # ===== قروض 5 =====
        if d=="loan":
            loans = u.get("loans",[]); total_loan = sum(x["amount"] for x in loans)
            m=InlineKeyboardMarkup(row_width=2)
            m.add(InlineKeyboardButton("💸 قرض 1000", callback_data="take_1000"))
            m.add(InlineKeyboardButton("💸 قرض 5000", callback_data="take_5000"))
            m.add(InlineKeyboardButton("💸 قرض 10000", callback_data="take_10000"))
            m.add(InlineKeyboardButton("💸 قرض 50000", callback_data="take_50000"))
            m.add(InlineKeyboardButton("💸 قرض 100000 🔥", callback_data="take_100000"))
            if loans:
                for i,ln in enumerate(loans):
                    m.add(InlineKeyboardButton(f"✅ سدد قرض {i+1} - {ln['amount']} (+10%)", callback_data=f"pay_{i}"))
                m.add(InlineKeyboardButton("💥 سدد الكل", callback_data="pay_all"))
            m.add(InlineKeyboardButton("🔙", callback_data="home"))
            txt = f"💸 القروض\n💰 معاك {u['money']}\n📋 عندك {len(loans)}/5 قروض\n💸 إجمالي عليك: {total_loan}\n\nتقدر تاخد لحد 5 قروض مع بعض!\nكل قرض عليه 10% فايدة"
            bot.send_message(cid, txt, reply_markup=m); return
        if d.startswith("take_"):
            loans = u.get("loans",[])
            if len(loans)>=5: bot.send_message(cid, "❌ عندك 5 قروض! سدد واحد الأول", reply_markup=menu(uid)); return
            amt=int(d.replace("take_","")); u["money"]+=amt; loans.append({"amount": amt, "time": int(time.time())}); u["loans"]=loans; save()
            bot.send_message(cid, f"✅ خدت قرض {amt} 🔥\n📋 بقى عندك {len(loans)}/5\n💰 معاك {u['money']}\nهتسدد {int(amt*1.1)}", reply_markup=menu(uid)); return
        if d.startswith("pay_") and d!="pay_all":
            idx=int(d.replace("pay_","")); loans=u.get("loans",[])
            if idx>=len(loans): bot.send_message(cid, "❌ القرض ده مش موجود", reply_markup=menu(uid)); return
            ln=loans[idx]; pay_amount=int(ln["amount"]*1.1)
            if u["money"]<pay_amount: bot.send_message(cid, f"❌ محتاج {pay_amount} عشان تسدد", reply_markup=menu(uid)); return
            u["money"]-=pay_amount; loans.pop(idx); u["loans"]=loans; save()
            bot.send_message(cid, f"✅ سددت قرض {ln['amount']}\n💰 معاك {u['money']}\n📋 فاضل {len(loans)} قرض", reply_markup=menu(uid)); return
        if d=="pay_all":
            loans=u.get("loans",[])
            if not loans: bot.send_message(cid, "❌ معليكش قروض", reply_markup=menu(uid)); return
            total=int(sum(x["amount"]*1.1 for x in loans))
            if u["money"]<total: bot.send_message(cid, f"❌ محتاج {total} عشان تسدد الكل", reply_markup=menu(uid)); return
            u["money"]-=total; u["loans"]=[]; save()
            bot.send_message(cid, f"✅ سددت كل القروض! 🎉\n💸 دفعت {total}", reply_markup=menu(uid)); return
        if d=="invest":
            m=InlineKeyboardMarkup(row_width=2)
            m.add(InlineKeyboardButton("💎 استثمر 1000", callback_data="inv_1000"), InlineKeyboardButton("💎 استثمر 5000", callback_data="inv_5000"), InlineKeyboardButton("💎 استثمر 20000", callback_data="inv_20000"))
            m.add(InlineKeyboardButton("💰 اسحب", callback_data="inv_out")); m.add(InlineKeyboardButton("🔙", callback_data="home"))
            bot.send_message(cid, f"💎 الاستثمار\n💎 استثمارك: {u.get('invest',0)}\n💵 كاش: {u['money']}", reply_markup=m); return
        if d.startswith("inv_") and d!="inv_out":
            amt=int(d.replace("inv_",""))
            if u["money"]<amt: bot.send_message(cid, "❌ فلوسك مش كفاية", reply_markup=menu(uid)); return
            u["money"]-=amt; u["invest"]=u.get("invest",0)+amt; save(); bot.send_message(cid, f"✅ استثمرت {amt} - هتاخد +50%", reply_markup=menu(uid)); return
        if d=="inv_out":
            if u.get("invest",0)<=0: bot.send_message(cid, "❌ معندكش استثمار", reply_markup=menu(uid)); return
            profit=int(u.get("invest",0)*0.5); total=u.get("invest",0)+profit; u["money"]+=total; u["invest"]=0; save(); bot.send_message(cid, f"💎 سحبت {total} (الأصل + {profit})", reply_markup=menu(uid)); return
        if d=="goldbox":
            if u["money"]<200: bot.send_message(cid, "❌ محتاج 200", reply_markup=play_menu(uid)); return
            u["money"]-=200; win=random.choice([100,300,500,1000,2000,5000]); u["money"]+=win; save(); bot.send_message(cid, f"📦 الصندوق الذهبي! +{win}", reply_markup=play_menu(uid)); return
        if d=="challenge":
            today = datetime.date.today().isoformat()
            if u.get("last_challenge")==today: bot.send_message(cid, "✅ عملت تحدي النهاردة", reply_markup=menu(uid)); return
            u["last_challenge"]=today; got=add(uid, 2000); bot.send_message(cid, f"🎯 تحدي اليوم! +{got} 🔥", reply_markup=menu(uid)); return
        if d=="slot":
            if u["money"]<50: bot.send_message(cid, "❌ محتاج 50", reply_markup=casino_menu(uid)); return
            u["money"]-=50; fruits=["🍎","🍌","🍇","🍓","🍒","💎","7️⃣"]; r=[random.choice(fruits) for _ in range(3)]
            txt=f"🎰 {' | '.join(r)}\n\n"
            if r[0]==r[1]==r[2]:
                if r[0]=="💎": win=5000; txt+=f"💎💎💎 جاكبوت +{win}"
                elif r[0]=="7️⃣": win=2000; txt+=f"7️⃣7️⃣7️⃣ +{win}"
                else: win=500; txt+=f"🎉 3 زي بعض +{win}"
                u["money"]+=win; settings["jackpot"]=settings.get("jackpot",5000)+50
            elif r[0]==r[1] or r[1]==r[2] or r[0]==r[2]: win=150; u["money"]+=win; txt+=f"✅ 2 زي بعض +{win}"
            else: txt+="😢 مفيش حاجة"
            save(); save_settings(); bot.send_message(cid, txt+f"\n💰 معاك {u['money']}", reply_markup=casino_menu(uid)); return
        if d=="dice":
            if u["money"]<50: bot.send_message(cid, "❌ محتاج 50", reply_markup=casino_menu(uid)); return
            u["money"]-=50; me=random.randint(1,6); bot_dice=random.randint(1,6)
            if me>bot_dice: u["money"]+=150; res=f"🎉 كسبت! {me} - {bot_dice} +150"
            elif me<bot_dice: res=f"😢 خسرت! {me} - {bot_dice}"
            else: u["money"]+=50; res=f"🤝 تعادل!"
            save(); bot.send_message(cid, f"🎲 {res}\n💰 {u['money']}", reply_markup=casino_menu(uid)); return
        if d=="cards":
            if u["money"]<50: bot.send_message(cid, "❌ محتاج 50", reply_markup=casino_menu(uid)); return
            u["money"]-=50
            m=InlineKeyboardMarkup(row_width=3)
            for i in range(3): m.add(InlineKeyboardButton(f"🃏 كارت {i+1}", callback_data=f"pick_{i}"))
            m.add(InlineKeyboardButton("🔙", callback_data="casino")); bot.send_message(cid, "🃏 اختار كارت.. واحد فيه 500!", reply_markup=m); return
        if d.startswith("pick_"):
            win_card=random.randint(0,2); pick=int(d.replace("pick_",""))
            if pick==win_card: u["money"]+=500; save(); bot.send_message(cid, f"🎉 الكارت الصح! +500", reply_markup=casino_menu(uid))
            else: save(); bot.send_message(cid, f"😢 غلط.. كان الكارت {win_card+1}", reply_markup=casino_menu(uid))
            return
        if d=="lottery":
            m=InlineKeyboardMarkup(); m.add(InlineKeyboardButton("🎟️ تذكرة - 50", callback_data="buy_ticket")); m.add(InlineKeyboardButton("🔙", callback_data="casino"))
            bot.send_message(cid, f"💎 اليانصيب\n🎟️ تذكرتك: {u.get('lottery_tickets',0)}\n🏆 الجايزة: {settings.get('jackpot',5000)}", reply_markup=m); return
        if d=="buy_ticket":
            if u["money"]<50: bot.send_message(cid, "❌ محتاج 50", reply_markup=casino_menu(uid)); return
            u["money"]-=50; u["lottery_tickets"]=u.get("lottery_tickets",0)+1; settings.setdefault("lottery",[]).append(str(uid)); settings["jackpot"]=settings.get("jackpot",5000)+50; save(); save_settings(); bot.send_message(cid, f"✅ اشتريت تذكرة!", reply_markup=casino_menu(uid)); return
        if d=="steal":
            now=int(time.time())
            if now-u.get("steal",0)<20: bot.send_message(cid, f"⏳ استنى {20-(now-u.get('steal',0))} ث", reply_markup=play_menu(uid)); return
            others=[k for k in data.keys() if k!=str(uid) and data[k].get("money",0)>100]
            if not others: bot.send_message(cid, "❌ مفيش حد تسرقه", reply_markup=play_menu(uid)); return
            victim=random.choice(others); v=data[victim]; u["steal"]=now
            if random.random()<0.6:
                steal_amt=random.randint(50, min(300, v["money"]//2)); v["money"]-=steal_amt; u["money"]+=steal_amt; save()
                bot.send_message(cid, f"🥷 سرقت {steal_amt} من {v.get('name')} 😈", reply_markup=play_menu(uid))
            else:
                fine=50; u["money"]=max(0,u["money"]-fine); save(); bot.send_message(cid, f"🚨 اتقفشت! غرامة {fine}", reply_markup=play_menu(uid))
            return
        if d=="secret": got=add(uid, 500); bot.send_message(cid, f"🎯 مهمة سرية! +{got}", reply_markup=play_menu(uid)); return
        if d=="trade": bot.send_message(cid, f"📈 البورصة\n💰 معاك {u['money']}", reply_markup=trade_menu(uid)); return
        if d=="my_portfolio":
            pf=u.get("portfolio",{})
            if not pf or sum(pf.values())==0: bot.send_message(cid, "💼 محفظتك فاضية", reply_markup=trade_menu(uid)); return
            txt="💼 محفظتك\n━━━━━━━━━━\n"; total=0
            for k,qty in pf.items():
                if qty>0 and k in MARKET: val=qty*MARKET[k]["price"]; total+=val; txt+=f"{MARKET[k]['name']} | {qty} × {MARKET[k]['price']} = {val}\n"
            txt+=f"━━━━━━━━━━\nإجمالي: {total}"
            bot.send_message(cid, txt, reply_markup=trade_menu(uid)); return
        if d.startswith("coin_"):
            k=d.replace("coin_",""); info=MARKET[k]; qty=u.get("portfolio",{}).get(k,0)
            m=InlineKeyboardMarkup(row_width=2); m.add(InlineKeyboardButton(f"🟢 اشتري 1 - {info['price']}", callback_data=f"buy_{k}_1"), InlineKeyboardButton(f"🟢 اشتري 5 - {info['price']*5}", callback_data=f"buy_{k}_5")); m.add(InlineKeyboardButton(f"🔴 بيع 1", callback_data=f"sell_{k}_1"), InlineKeyboardButton(f"🔴 بيع الكل", callback_data=f"sell_{k}_all")); m.add(InlineKeyboardButton("🔙 بورصة", callback_data="trade"))
            bot.send_message(cid, f"{info['name']}\n💲 السعر: {info['price']}\n📦 معاك: {qty}", reply_markup=m); return
        if d.startswith("buy_"):
            _,k,amt=d.split("_"); amt=int(amt); price=MARKET[k]["price"]*amt
            if u["money"]<price: bot.send_message(cid, f"❌ محتاج {price}", reply_markup=trade_menu(uid)); return
            u["money"]-=price; u["portfolio"][k]=u["portfolio"].get(k,0)+amt; save(); bot.send_message(cid, f"✅ اشتريت {amt} {MARKET[k]['name']}", reply_markup=trade_menu(uid)); return
        if d.startswith("sell_"):
            _,k,amt=d.split("_"); have=u.get("portfolio",{}).get(k,0)
            if have<=0: bot.send_message(cid, "❌ معكش", reply_markup=trade_menu(uid)); return
            amt=have if amt=="all" else min(int(amt), have); gain=MARKET[k]["price"]*amt; u["money"]+=gain; u["portfolio"][k]-=amt; save(); bot.send_message(cid, f"✅ بعت {amt} بـ {gain}", reply_markup=trade_menu(uid)); return
        if d=="tasks":
            m=InlineKeyboardMarkup()
            for i,(name,rew) in enumerate(TASKS): m.add(InlineKeyboardButton(f"{name} +{rew+power(u)}", callback_data=f"t_{i}"))
            m.add(InlineKeyboardButton("🔙", callback_data="play")); bot.send_message(cid, "📋 اختار مهمة:", reply_markup=m); return
        if d.startswith("t_"):
            i=int(d.split("_")[1])
            if i==0:
                m=InlineKeyboardMarkup(row_width=2); m.add(InlineKeyboardButton("3", callback_data="wrong"), InlineKeyboardButton("4 ✅", callback_data="right_50"), InlineKeyboardButton("5", callback_data="wrong"), InlineKeyboardButton("6", callback_data="wrong")); bot.send_message(cid, "🧠 2+2 = كام؟", reply_markup=m)
            elif i==3:
                m=InlineKeyboardMarkup(row_width=2); m.add(InlineKeyboardButton("🍎", callback_data="wrong"), InlineKeyboardButton("🍌", callback_data="right_100"), InlineKeyboardButton("🍇", callback_data="wrong"), InlineKeyboardButton("🍓", callback_data="wrong")); bot.send_message(cid, "🍌 اختار موز", reply_markup=m)
            else: got=add(uid, TASKS[i][1]+power(u)); bot.send_message(cid, f"✅ خدت +{got}", reply_markup=play_menu(uid))
            return
        if d.startswith("right_"): got=add(uid, int(d.split("_")[1])+power(u)); bot.send_message(cid, f"✅ صح! +{got}", reply_markup=play_menu(uid)); return
        if d=="wrong": bot.send_message(cid, "❌ غلط", reply_markup=play_menu(uid)); return
        if d=="daily":
            now=int(time.time())
            if now-u.get("daily",0)<5: bot.send_message(cid, "⏳ استنى شوية", reply_markup=play_menu(uid))
            else: u["streak"]+=1; got=add(uid, (500 if is_vip(u) else 100)+u["streak"]*10); u["daily"]=now; save(); bot.send_message(cid, f"📅 يومية +{got} 🔥", reply_markup=play_menu(uid))
            return
        if d=="gift":
            now=int(time.time())
            if now-u.get("gift",0)<5: bot.send_message(cid, "⏳ استنى 5 ث", reply_markup=play_menu(uid))
            else: got=add(uid, 1000 if is_vip(u) else random.choice([50,100,200,500,1000])); u["gift"]=now; save(); bot.send_message(cid, f"🎁 +{got} 🔥", reply_markup=play_menu(uid))
            return
        if d=="spin":
            now=int(time.time())
            if now-u.get("spin",0)<5: bot.send_message(cid, "⏳ العجلة كل 5 ث", reply_markup=play_menu(uid))
            else: r=random.choice([0,50,100,200,500,1000,2000,5000]); u["spin"]=now; save(); got=add(uid,r) if r>0 else 0; bot.send_message(cid, f"🎡 +{got} 🔥" if r>0 else "😢 صفر", reply_markup=play_menu(uid))
            return
        if d=="gamble":
            m=InlineKeyboardMarkup(row_width=2); m.add(InlineKeyboardButton("🪙 ملك - 50", callback_data="g_1"), InlineKeyboardButton("🪙 كتابة - 50", callback_data="g_2")); m.add(InlineKeyboardButton("🔙", callback_data="play")); bot.send_message(cid, f"🎲 معاك {u['money']}\nراهن 50 تكسب 150", reply_markup=m); return
        if d.startswith("g_"):
            if u["money"]<50: bot.send_message(cid, "❌ فلوسك مش كفاية", reply_markup=play_menu(uid)); return
            u["money"]-=50
            if random.choice([True,False]): u["money"]+=150; save(); bot.send_message(cid, f"🎉 كسبت +150", reply_markup=play_menu(uid))
            else: save(); bot.send_message(cid, f"😢 خسرت 50", reply_markup=play_menu(uid))
            return
        if d=="codes":
            m=InlineKeyboardMarkup(row_width=2)
            for c in CODES: m.add(InlineKeyboardButton(c, callback_data=f"code_{c}"))
            m.add(InlineKeyboardButton("🔙", callback_data="play")); bot.send_message(cid, "🎁 اختار كود:", reply_markup=m); return
        if d.startswith("code_"):
            c=d.replace("code_","")
            if c in u.get("codes",[]): bot.send_message(cid, "❌ استخدمته", reply_markup=play_menu(uid)); return
            u["codes"].append(c); got=add(uid, CODES[c]); bot.send_message(cid, f"🎉 +{got} 🔥", reply_markup=play_menu(uid)); return
        if d=="contest":
            top=sorted(data.items(), key=lambda x: x[1].get('score',0), reverse=True)[:5]
            txt="🏆 مسابقة اليوم - أعلى نقاط يكسب 5000\n━━━━━━━━━━\n"
            for i,(k,v) in enumerate(top): txt+=f"{i+1}. {v.get('name','?')} — {v.get('score',0)}\n"
            txt+=f"\nنقطك: {u.get('score',0)}"
            bot.send_message(cid, txt, reply_markup=play_menu(uid)); return
        if d=="weapons":
            m=InlineKeyboardMarkup()
            for k,(name,price,bonus) in WEAPONS.items():
                owned=" ✅" if k in u.get("weapons",[]) else f" — {price}"
                m.add(InlineKeyboardButton(f"{name} +{bonus}{owned}", callback_data=f"bw_{k}"))
            m.add(InlineKeyboardButton("🔙", callback_data="shop")); bot.send_message(cid, f"🔫 أسلحة\n⚡ قوتك +{power(u)}", reply_markup=m); return
        if d.startswith("bw_"):
            k=d.replace("bw_",""); name,price,bonus=WEAPONS[k]
            if k in u.get("weapons",[]): bot.send_message(cid, "معاك ده ✅", reply_markup=shop_menu(uid)); return
            if u["money"]>=price: u["money"]-=price; u["weapons"].append(k); save(); bot.send_message(cid, f"🎉 اشتريت {name}", reply_markup=shop_menu(uid))
            else: bot.send_message(cid, "❌ فلوسك مش كفاية", reply_markup=shop_menu(uid))
            return
        if d=="old_shop":
            m=InlineKeyboardMarkup()
            for k,(name,price) in STORE_OLD.items(): m.add(InlineKeyboardButton(f"{name} — {price}", callback_data=f"old_{k}"))
            m.add(InlineKeyboardButton("🔙", callback_data="shop")); bot.send_message(cid, "🛍️ المتجر القديم", reply_markup=m); return
        if d.startswith("old_"):
            k=d.replace("old_",""); name,price=STORE_OLD[k]
            if u["money"]>=price: u["money"]-=price; u["items"].append(name); save(); bot.send_message(cid, f"🎉 اشتريت {name}", reply_markup=shop_menu(uid))
            else: bot.send_message(cid, "❌ فلوسك مش كفاية", reply_markup=shop_menu(uid))
            return
        if d=="vip":
            if is_vip(u): bot.send_message(cid, "انت VIP أصلاً 👑 ×3", reply_markup=shop_menu(uid)); return
            m=InlineKeyboardMarkup(); m.add(InlineKeyboardButton("👑 اشتري VIP - 1000", callback_data="buy_vip")); m.add(InlineKeyboardButton("🔙", callback_data="shop")); bot.send_message(cid, "👑 VIP\n✅ كل حاجة ×3\nالسعر 1000", reply_markup=m); return
        if d=="buy_vip":
            if u["money"]>=1000: u["money"]-=1000; u["vip"]=True; u["vip_until"]=0; save(); bot.send_message(cid, "🎉 بقيت VIP 👑 ×3", reply_markup=shop_menu(uid))
            else: bot.send_message(cid, "❌ فلوسك مش كفاية", reply_markup=shop_menu(uid))
            return
        # ===== الأونر =====
        if d=="owner":
            if not is_owner(uid): bot.send_message(cid, "❌ انت مش الأونر"); return
            total_money=sum(v.get('money',0) for v in data.values())
            bot.send_message(cid, f"👑 لوحة الأونر 🔥🔥\n━━━━━━━━━━\n👥 {len(data)} مستخدم\n💰 فلوس الكل: {total_money}\n⭐ VIP: {sum(1 for v in data.values() if v.get('vip'))}\n🚫 محظورين: {len(settings.get('banned',[]))}\n🛠️ صيانة: {'🔴 مقفول' if settings.get('maintenance') else '🟢 شغال'}\n🎰 جاكبوت: {settings.get('jackpot',5000)}\n💎 ثروتك: {u['money']}\n━━━━━━━━━━\n\n💡 عشان تدي مبلغ مخصوص بسرعة اكتب:\n`/give ID المبلغ`", reply_markup=owner_menu(), parse_mode="Markdown"); return
        if d=="a_custom":
            if not is_owner(uid): return
            pending[uid]={"action":"wait_id"}
            bot.send_message(cid, "💰 مبلغ مخصوص لحد\n\nابعت ID الشخص", reply_markup=owner_menu()); return
        if d=="a_custom_all":
            if not is_owner(uid): return
            pending[uid]={"action":"custom_all"}
            bot.send_message(cid, "💰 مبلغ مخصوص للكل\n\nاكتب المبلغ\nمثال: `5000`", reply_markup=owner_menu()); return
        if d.startswith("custom_"):
            if not is_owner(uid): return
            tid=d.replace("custom_",""); pending[uid]={"target":tid, "action":"custom_one"}; info=user(int(tid))
            bot.send_message(cid, f"💰 هتدي {info.get('name')} كام؟\nمعاه: {info['money']}\n\nاكتب المبلغ بس\nمثال: `75000`"); return
        if d.startswith("ctake_"):
            if not is_owner(uid): return
            tid=d.replace("ctake_",""); pending[uid]={"target":tid, "action":"custom_take"}; info=user(int(tid))
            bot.send_message(cid, f"💸 هتسحب من {info.get('name')} كام؟\nمعاه: {info['money']}\n\nاكتب المبلغ بس"); return
        if d.startswith("cbank_"):
            if not is_owner(uid): return
            tid=d.replace("cbank_",""); pending[uid]={"target":tid, "action":"custom_bank"}
            bot.send_message(cid, f"🏦 هتحط في بنك {data[tid].get('name')} كام؟\n\nاكتب المبلغ بس"); return
        if d=="a_stats":
            if not is_owner(uid): return
            if not data: bot.send_message(cid, "مفيش حد", reply_markup=owner_menu()); return
            richest=max(data.items(), key=lambda x: x[1].get('money',0)); top_score=max(data.items(), key=lambda x: x[1].get('score',0))
            bot.send_message(cid, f"📊 احصائيات\n👥 {len(data)}\n💰 إجمالي: {sum(v.get('money',0) for v in data.values())}\n🏦 بنوك: {sum(v.get('bank_saving',0)+v.get('bank_current',0) for v in data.values())}\n🥇 أغنى واحد: {richest[1].get('name')} - {richest[1].get('money')}\n🏆 أكتر نقاط: {top_score[1].get('name')} - {top_score[1].get('score')}", reply_markup=owner_menu()); return
        if d=="a_users":
            if not is_owner(uid): return
            m=InlineKeyboardMarkup()
            for k,v in list(data.items())[:25]: m.add(InlineKeyboardButton(f"{v.get('name','?')} {'👑' if v.get('vip') else ''} — {v.get('money',0)}", callback_data=f"a_u_{k}"))
            m.add(InlineKeyboardButton("🔙", callback_data="owner")); bot.send_message(cid, "👥 دوس على واحد:", reply_markup=m); return
        if d.startswith("a_u_"):
            if not is_owner(uid): return
            t=d.replace("a_u_",""); info=user(int(t))
            m=InlineKeyboardMarkup(row_width=2)
            m.add(InlineKeyboardButton("💰 مبلغ مخصوص ➕", callback_data=f"custom_{t}"), InlineKeyboardButton("💸 اسحب مبلغ ➖", callback_data=f"ctake_{t}"))
            m.add(InlineKeyboardButton("➕1000", callback_data=f"add_{t}_1000"), InlineKeyboardButton("➕10000", callback_data=f"add_{t}_10000"))
            m.add(InlineKeyboardButton("💎 1M", callback_data=f"add_{t}_1000000"), InlineKeyboardButton("💥 تصفير", callback_data=f"zero_{t}"))
            m.add(InlineKeyboardButton("👑 VIP", callback_data=f"gv_{t}"), InlineKeyboardButton("👑 VIP اسبوع", callback_data=f"gv7_{t}"))
            m.add(InlineKeyboardButton("❌ شيل VIP", callback_data=f"rmvip_{t}"), InlineKeyboardButton("🚫 حظر", callback_data=f"ban_{t}"))
            m.add(InlineKeyboardButton("✅ فك حظر", callback_data=f"unban_{t}"), InlineKeyboardButton("🔫 سلاح", callback_data=f"givew_{t}"))
            m.add(InlineKeyboardButton("🐉 تنين", callback_data=f"givepet_{t}_dragon"), InlineKeyboardButton("🏦 حط في بنكه", callback_data=f"cbank_{t}"))
            m.add(InlineKeyboardButton("🙏 سامحه في القروض", callback_data=f"forgive_{t}"), InlineKeyboardButton("📋 كشف حسابه", callback_data=f"a_statement_{t}"))
            m.add(InlineKeyboardButton("🔙", callback_data="a_users"))
            bot.send_message(cid, f"👤 {info.get('name')}\n🆔 {t}\n💰 {info['money']}\n🏦 توفير {info.get('bank_saving',0)} | جاري {info.get('bank_current',0)}\n⭐ {info['level']}\n👑 {'✅' if is_vip(info) else '❌'}", reply_markup=m); return
        if d.startswith("forgive_"):
            if not is_owner(uid): return
            t=d.replace("forgive_",""); info=user(int(t)); info["loans"]=[]; save()
            bot.send_message(cid, f"✅ سامحت {info.get('name')} في كل قروضه 🙏", reply_markup=owner_menu())
            try: bot.send_message(int(t), "🎉 الأونر سامحك في كل قروضك!")
            except: pass
            return
        if d.startswith("a_statement_"):
            if not is_owner(uid): return
            t=d.replace("a_statement_",""); info=user(int(t)); hist=info.get("bank_history",[])
            txt=f"📋 كشف حساب {info.get('name')}\n" + ("\n".join(hist) if hist else "فاضي")
            bot.send_message(cid, txt, reply_markup=owner_menu()); return
        if d.startswith("givepet_"):
            if not is_owner(uid): return
            _,t,pet=d.split("_",2); info=user(int(t))
            if pet not in info["pets"]: info["pets"].append(pet); save()
            bot.send_message(cid, f"✅ اديت {info.get('name')} {PETS[pet][0]}", reply_markup=owner_menu()); return
        if d.startswith("givew_"):
            if not is_owner(uid): return
            t=d.replace("givew_","")
            m=InlineKeyboardMarkup()
            for k,(name,price,bonus) in WEAPONS.items(): m.add(InlineKeyboardButton(f"{name} +{bonus}", callback_data=f"dogive_{t}_{k}"))
            m.add(InlineKeyboardButton("🔙", callback_data=f"a_u_{t}")); bot.send_message(cid, "🔫 اختار سلاح:", reply_markup=m); return
        if d.startswith("dogive_"):
            if not is_owner(uid): return
            _,t,k=d.split("_",2); info=user(int(t))
            if k not in info["weapons"]: info["weapons"].append(k); save()
            bot.send_message(cid, f"✅ اديت {info.get('name')} {WEAPONS[k][0]}", reply_markup=owner_menu()); return
        if d.startswith("zero_"):
            if not is_owner(uid): return
            t=d.replace("zero_",""); info=user(int(t)); info["money"]=0; info["score"]=0; info["portfolio"]={}; info["bank"]=0; info["bank_current"]=0; info["bank_saving"]=0; info["invest"]=0; info["certificates"]=[]; save(); bot.send_message(cid, f"💥 صفرت {info.get('name')}", reply_markup=owner_menu()); return
        if d.startswith("rmvip_"):
            if not is_owner(uid): return
            t=d.replace("rmvip_",""); info=user(int(t)); info["vip"]=False; info["vip_until"]=0; save(); bot.send_message(cid, f"❌ شلت VIP من {info.get('name')}", reply_markup=owner_menu()); return
        if d.startswith("gv7_"):
            if not is_owner(uid): return
            t=d.replace("gv7_",""); info=user(int(t)); info["vip"]=True; info["vip_until"]=int(time.time())+7*24*3600; save(); bot.send_message(cid, f"✅ اديت {info.get('name')} VIP اسبوع", reply_markup=owner_menu()); return
        if d.startswith("ban_"):
            if not is_owner(uid): return
            t=d.replace("ban_","")
            if t not in settings["banned"]: settings["banned"].append(t); save_settings()
            bot.send_message(cid, f"🚫 حظرت {t}", reply_markup=owner_menu()); return
        if d.startswith("unban_"):
            if not is_owner(uid): return
            t=d.replace("unban_","")
            if t in settings["banned"]: settings["banned"].remove(t); save_settings()
            bot.send_message(cid, f"✅ فكيت حظر {t}", reply_markup=owner_menu()); return
        if d.startswith("gv_"):
            if not is_owner(uid): return
            t=d.replace("gv_",""); info=user(int(t)); info["vip"]=True; info["vip_until"]=0; save(); bot.send_message(cid, f"✅ {info.get('name')} بقى VIP دائم", reply_markup=owner_menu()); return
        if d.startswith("add_") or d.startswith("sub_"):
            if not is_owner(uid): return
            _,t,amt=d.split("_"); amt=int(amt); info=user(int(t))
            if d.startswith("add_"): info["money"]+=amt
            else: info["money"]=max(0, info["money"]-amt)
            save(); bot.send_message(cid, f"✅ بقى معاه {info['money']}", reply_markup=owner_menu()); return
        if d=="a_search":
            if not is_owner(uid): return
            pending[uid]={"action":"wait_id"}
            bot.send_message(cid, "🔍 ابعت ID الشخص", reply_markup=owner_menu()); return
        if d=="a_maint":
            if not is_owner(uid): return
            m=InlineKeyboardMarkup(row_width=2); btn_text="🟢 فتح البوت" if settings.get("maintenance") else "🔴 قفل البوت"; m.add(InlineKeyboardButton(btn_text, callback_data="toggle_maint")); m.add(InlineKeyboardButton("💥 تصفير الكل", callback_data="reset_all")); m.add(InlineKeyboardButton("🔙", callback_data="owner")); bot.send_message(cid, f"🛠️ الصيانة\nالحالة: {'🔴 مقفول' if settings.get('maintenance') else '🟢 شغال'}", reply_markup=m); return
        if d=="toggle_maint":
            if not is_owner(uid): return
            settings["maintenance"]=not settings.get("maintenance",False); save_settings(); bot.send_message(cid, f"{'🔴 قفلت البوت' if settings['maintenance'] else '🟢 فتحت البوت'}", reply_markup=owner_menu()); return
        if d=="reset_all":
            if not is_owner(uid): return
            m=InlineKeyboardMarkup(row_width=2); m.add(InlineKeyboardButton("✅ أيوه صفر الكل", callback_data="confirm_reset"), InlineKeyboardButton("❌ لا", callback_data="owner")); bot.send_message(cid, "⚠️ متأكد؟ هتصفر فلوس الكل!", reply_markup=m); return
        if d=="confirm_reset":
            if not is_owner(uid): return
            for k in data:
                if k!=str(OWNER_ID): data[k]["money"]=0; data[k]["score"]=0; data[k]["portfolio"]={}; data[k]["bank"]=0; data[k]["bank_current"]=0; data[k]["bank_saving"]=0; data[k]["invest"]=0; data[k]["certificates"]=[]
            save(); bot.send_message(cid, "💥 صفرت الكل (ما عدا انت)", reply_markup=owner_menu()); return
        if d=="a_self":
            if not is_owner(uid): return
            m=InlineKeyboardMarkup(row_width=2); m.add(InlineKeyboardButton("💰 مبلغ مخصوص لنفسك", callback_data="self_custom")); m.add(InlineKeyboardButton("💰 100K", callback_data="self_100000"), InlineKeyboardButton("💎 1M", callback_data="self_1000000"), InlineKeyboardButton("👑 VIP لنفسك", callback_data="self_vip")); m.add(InlineKeyboardButton("🔙", callback_data="owner")); bot.send_message(cid, "💎 فلوس لنفسك:", reply_markup=m); return
        if d=="self_custom":
            if not is_owner(uid): return
            pending[uid]={"target":str(uid), "action":"custom_one"}
            bot.send_message(cid, "💰 هتدي لنفسك كام؟\nاكتب المبلغ بس\nمثال: `999999`"); return
        if d.startswith("self_"):
            if not is_owner(uid): return
            if d=="self_vip": u["vip"]=True; u["vip_until"]=0; save(); bot.send_message(cid, "✅ بقيت VIP دائم", reply_markup=owner_menu()); return
            amt=int(d.replace("self_","")); u["money"]+=amt; save(); bot.send_message(cid, f"✅ اديت لنفسك {amt}\n💰 معاك {u['money']}", reply_markup=owner_menu()); return
        if d=="a_vip_all":
            if not is_owner(uid): return
            for k in data: data[k]["vip"]=True; data[k]["vip_until"]=0
            save(); bot.send_message(cid, f"✅ اديت VIP للكل ({len(data)})", reply_markup=owner_menu()); return
        if d=="a_pet_all":
            if not is_owner(uid): return
            for k in data:
                if "dragon" not in data[k].get("pets",[]): data[k].setdefault("pets",[]).append("dragon")
            save(); bot.send_message(cid, f"✅ اديت تنين للكل 🐉", reply_markup=owner_menu()); return
        if d=="a_weekly":
            if not is_owner(uid): return
            if not data: bot.send_message(cid, "مفيش حد", reply_markup=owner_menu()); return
            w=max(data.items(), key=lambda x: x[1].get('score',0)); wid,winfo=w; winfo["money"]+=50000; winfo["score"]=0; save()
            for k in data:
                if k!=wid: data[k]["score"]=0
            save()
            try: bot.send_message(int(wid), "🏆 كسبت البطولة! +50000 🔥")
            except: pass
            bot.send_message(cid, f"🏆 بطل الأسبوع: {winfo.get('name')} +50000", reply_markup=owner_menu()); return
        if d=="a_clear_ban":
            if not is_owner(uid): return
            settings["banned"]=[]; save_settings(); bot.send_message(cid, "✅ فكيت حظر الكل", reply_markup=owner_menu()); return
        if d=="a_new_challenge":
            if not is_owner(uid): return
            for k in data: data[k]["last_challenge"]=0
            save(); bot.send_message(cid, "✅ عملت تحدي جديد", reply_markup=owner_menu()); return
        if d=="a_all_money":
            if not is_owner(uid): return
            m=InlineKeyboardMarkup(row_width=2); m.add(InlineKeyboardButton("➕1000 للكل", callback_data="all_1000"), InlineKeyboardButton("➕10000 للكل", callback_data="all_10000"), InlineKeyboardButton("💰 مبلغ مخصوص للكل", callback_data="a_custom_all")); m.add(InlineKeyboardButton("🔙", callback_data="owner")); bot.send_message(cid, "💰 ادي الكل:", reply_markup=m); return
        if d.startswith("all_"):
            if not is_owner(uid): return
            amt=int(d.replace("all_",""))
            for k in data: data[k]["money"]+=amt
            save(); bot.send_message(cid, f"✅ اديت {amt} للكل", reply_markup=owner_menu()); return
        if d=="a_gift_all":
            if not is_owner(uid): return
            m=InlineKeyboardMarkup(row_width=2); m.add(InlineKeyboardButton("🎁 1000 للكل", callback_data="giftall_1000"), InlineKeyboardButton("🎁 10000 للكل", callback_data="giftall_10000")); m.add(InlineKeyboardButton("🔙", callback_data="owner")); bot.send_message(cid, "🎁 هدية للكل:", reply_markup=m); return
        if d.startswith("giftall_"):
            if not is_owner(uid): return
            amt=int(d.replace("giftall_","")); c=0
            for k in list(data.keys()):
                try: bot.send_message(int(k), f"🎁 هدية من الأونر! +{amt} 🔥"); data[k]["money"]+=amt; c+=1
                except: pass
            save(); bot.send_message(cid, f"✅ بعت لـ {c}", reply_markup=owner_menu()); return
        if d=="a_bc":
            if not is_owner(uid): return
            m=InlineKeyboardMarkup(row_width=2); m.add(InlineKeyboardButton("🎉 مسابقة!", callback_data="bc_1"), InlineKeyboardButton("🔥 خصم!", callback_data="bc_2"), InlineKeyboardButton("👋 ارجع العب", callback_data="bc_3"), InlineKeyboardButton("📈 البورصة ولعت", callback_data="bc_4"), InlineKeyboardButton("💎 هدية", callback_data="bc_5")); m.add(InlineKeyboardButton("🔙", callback_data="owner")); bot.send_message(cid, "📢 اختار رسالة:", reply_markup=m); return
        if d.startswith("bc_"):
            if not is_owner(uid): return
            texts={"bc_1":"🎉 مسابقة جديدة! ادخل والعب وخد 5000","bc_2":"🔥 خصم في المتجر!","bc_3":"👋 ارجع العب وخد فلوس","bc_4":"📈 البورصة ولعت! الحق اشتري وبيع","bc_5":"💎 الأونر بيوزع هدايا! ادخل بسرعة"}
            c=0
            for k in list(data.keys()):
                try: bot.send_message(int(k), f"📢 من الأونر:\n\n{texts[d]}"); c+=1
                except: pass
            bot.send_message(cid, f"✅ بعت لـ {c}", reply_markup=owner_menu()); return
        if d=="a_end":
            if not is_owner(uid): return
            if not data: bot.send_message(cid, "مفيش حد", reply_markup=owner_menu()); return
            w=max(data.items(), key=lambda x: x[1].get('score',0)); wid,winfo=w; winfo["money"]+=5000; winfo["score"]=0; save()
            for k in data:
                if k!=wid: data[k]["score"]=0
            save()
            try: bot.send_message(int(wid), "🏆 كسبت المسابقة! +5000")
            except: pass
            bot.send_message(cid, f"🏆 الفايز: {winfo.get('name')} +5000", reply_markup=owner_menu()); return
        if d=="a_lottery_draw":
            if not is_owner(uid): return
            lot=settings.get("lottery",[])
            if not lot: bot.send_message(cid, "❌ مفيش حد اشترى تذاكر", reply_markup=owner_menu()); return
            winner=random.choice(lot); prize=settings.get("jackpot",5000); winfo=user(int(winner)); winfo["money"]+=prize; winfo["lottery_tickets"]=0; save()
            settings["lottery"]=[]; settings["jackpot"]=5000; save_settings()
            for k in data:
                try: bot.send_message(int(k), f"💎 نتيجة اليانصيب!\n🏆 الفايز: {winfo.get('name')} كسب {prize}!")
                except: pass
            bot.send_message(cid, f"🏆 الفايز: {winfo.get('name')} +{prize}", reply_markup=owner_menu()); return
        if d=="a_pump":
            if not is_owner(uid): return
            for k in MARKET: MARKET[k]["price"]+=random.randint(100,300)
            bot.send_message(cid, f"💥 فجرت الأسعار!\n" + "\n".join([f"{v['name']}: {v['price']}" for v in MARKET.values()]), reply_markup=owner_menu())
            for k in list(data.keys()):
                try: bot.send_message(int(k), "📈💥 البورصة ولعت! الحق بيع!")
                except: pass
            return
        if d=="a_crash":
            if not is_owner(uid): return
            for k in MARKET: MARKET[k]["price"]=max(20, MARKET[k]["price"]-random.randint(50,150))
            bot.send_message(cid, f"📉 انهيار!\n" + "\n".join([f"{v['name']}: {v['price']}" for v in MARKET.values()]), reply_markup=owner_menu())
            for k in list(data.keys()):
                try: bot.send_message(int(k), "📉 البورصة وقعت! الحق اشتري رخيص!")
                except: pass
            return
    except Exception as e:
        print("Error:", e, traceback.format_exc())
        try: bot.send_message(cid, "حصل مشكلة.. دوس تاني", reply_markup=menu(uid))
        except: pass

print("Bot FINAL is running - Self ping every 5 min ✅")
while True:
    try: bot.infinity_polling(timeout=60, long_polling_timeout=60, skip_pending=True)
    except Exception as e:
        print(f"Restarting... {e}"); time.sleep(3)
