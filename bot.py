import os, json, time, random, traceback, datetime
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers(); self.wfile.write(b"Bot is running!")
    def log_message(self, *a): pass
def keep_alive():
    try:
        port = int(os.environ.get("PORT", 10000))
        Thread(target=HTTPServer(("0.0.0.0", port), Handler).serve_forever, daemon=True).start()
    except: pass
keep_alive()

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
settings = load_json("settings.json", {"maintenance": False, "banned": [], "lottery": [], "jackpot": 1000})
def save(): save_json("data.json", data)
def save_settings(): save_json("settings.json", settings)

def user(uid):
    uid = str(uid)
    if uid not in data:
        data[uid] = {"money":100,"name":"مستخدم","level":1,"xp":0,"vip":False,"weapons":[],"daily":0,"spin":0,"gift":0,"streak":0,"score":0,"codes":[],"items":[],"portfolio":{},"bank":0,"bank_time":0,"steal":0,"lottery_tickets":0}
        save()
    defaults = {"money":100,"level":1,"xp":0,"vip":False,"weapons":[],"daily":0,"spin":0,"gift":0,"streak":0,"score":0,"codes":[],"items":[],"portfolio":{},"bank":0,"bank_time":0,"steal":0,"lottery_tickets":0,"name":"مستخدم"}
    for k,v in defaults.items():
        if k not in data[uid]: data[uid][k]=v
    return data[uid]
def is_owner(uid): return int(uid)==OWNER_ID
def is_banned(uid): return str(uid) in settings.get("banned",[])
def is_vip(u): return u.get("vip",False)
def add(uid, amount):
    u=user(uid)
    if is_vip(u): amount*=2
    u["money"]+=amount; u["xp"]+=amount//10; u["score"]+=amount
    lvl=u["xp"]//100+1
    if lvl>u["level"]:
        u["level"]=lvl
        try: bot.send_message(uid, f"🎉 مستوى جديد! وصلت {lvl} 🔥")
        except: pass
    save(); return amount

# رتب حسب الفلوس
def get_rank(money):
    if money >= 100000: return "👑 ملياردير"
    if money >= 50000: return "💎 مليونير"
    if money >= 20000: return "🏆 غني جدا"
    if money >= 10000: return "💰 غني"
    if money >= 5000: return "🤑 متوسط"
    if money >= 1000: return "🙂 عادي"
    return "🥺 فقير"

MARKET = {"btc":{"name":"₿ بيتكوين","price":500},"eth":{"name":"Ξ ايثريوم","price":200},"gold":{"name":"🥇 ذهب","price":100},"usd":{"name":"💵 دولار","price":50},"oil":{"name":"🛢️ بترول","price":80}}
def update_market():
    for k in MARKET: MARKET[k]["price"]=max(10, MARKET[k]["price"]+random.randint(-15,20))
    Thread(target=lambda: (time.sleep(30), update_market()), daemon=True).start()
update_market()
def portfolio_value(u): return sum(qty*MARKET[k]["price"] for k,qty in u.get("portfolio",{}).items() if k in MARKET)

STORE_OLD = {"bg":("🎨 خلفية موبايل",50),"song":("🎵 اغنية MP3",100),"netflix":("🎬 نتفليكس يوم",200),"pubg":("🎮 ببجي 60 شدة",500),"title":("💎 لقب اسطوري",2000)}
WEAPONS = {"w1":("🔪 سكينة",100,5),"w2":("🔫 مسدس",300,15),"w3":("💣 قنبلة",600,30),"w4":("🚀 بازوكا",1200,60),"w5":("⚔️ سيف اسطوري",2500,120)}
TASKS=[("سؤال سريع",20),("حظك اليوم",30),("مهمة كلمة السر",50),("تحدي الذاكرة",40)]
CODES={"WELCOME100":100,"MEGA500":500,"BOSS1000":1000}
def power(u): return sum(WEAPONS[w][2] for w in u.get("weapons",[]) if w in WEAPONS)
def lvl_emoji(l):
    if l>=10: return "👑"
    if l>=5: return "💎"
    if l>=3: return "⭐"
    return "🌱"

def menu(uid):
    m=InlineKeyboardMarkup(row_width=2)
    m.add(
        InlineKeyboardButton("🎮 العب واكسب", callback_data="play"),
        InlineKeyboardButton("📈 تداول", callback_data="trade"),
        InlineKeyboardButton("🏦 البنك", callback_data="bank"),
        InlineKeyboardButton("🛒 المتجر", callback_data="shop"),
        InlineKeyboardButton("👤 بروفايلي", callback_data="me"),
        InlineKeyboardButton("🏆 الأبطال", callback_data="top"),
        InlineKeyboardButton("🎰 كازينو", callback_data="casino"),
        InlineKeyboardButton("💰 فلوسي", callback_data="balance"),
    )
    if is_owner(uid): m.add(InlineKeyboardButton("👑 لوحة الأونر 🔥", callback_data="owner"))
    m.add(InlineKeyboardButton("🔄 تحديث", callback_data="home"))
    return m

def play_menu(uid):
    m=InlineKeyboardMarkup(row_width=2)
    m.add(
        InlineKeyboardButton("📋 المهام", callback_data="tasks"),
        InlineKeyboardButton("🎡 عجلة الحظ", callback_data="spin"),
        InlineKeyboardButton("🎲 لعبة الحظ", callback_data="gamble"),
        InlineKeyboardButton("🎁 صندوق", callback_data="gift"),
        InlineKeyboardButton("📅 يومية", callback_data="daily"),
        InlineKeyboardButton("🎁 أكواد", callback_data="codes"),
        InlineKeyboardButton("🏆 مسابقة", callback_data="contest"),
        InlineKeyboardButton("🥷 سرقة", callback_data="steal"),
        InlineKeyboardButton("🎯 مهمة سرية", callback_data="secret"),
        InlineKeyboardButton("🔥 سلسلة", callback_data="streak"),
    )
    m.add(InlineKeyboardButton("🔙 رجوع", callback_data="home"))
    return m

def casino_menu(uid):
    m=InlineKeyboardMarkup(row_width=2)
    m.add(
        InlineKeyboardButton("🎰 سلوت ماشين", callback_data="slot"),
        InlineKeyboardButton("🎲 تحدي النرد", callback_data="dice"),
        InlineKeyboardButton("🃏 لعبة الورق", callback_data="cards"),
        InlineKeyboardButton("💎 يانصيب", callback_data="lottery"),
    )
    m.add(InlineKeyboardButton("🔙 رجوع", callback_data="home"))
    return m

def shop_menu(uid):
    m=InlineKeyboardMarkup()
    m.add(InlineKeyboardButton("🔫 محل الأسلحة", callback_data="weapons"))
    m.add(InlineKeyboardButton("👑 VIP - 1000", callback_data="vip"))
    m.add(InlineKeyboardButton("🛍️ متجر قديم", callback_data="old_shop"))
    m.add(InlineKeyboardButton("🔙 رجوع", callback_data="home"))
    return m

def trade_menu(uid):
    u=user(uid); m=InlineKeyboardMarkup()
    for k,v in MARKET.items():
        qty=u.get("portfolio",{}).get(k,0)
        m.add(InlineKeyboardButton(f"{v['name']} - {v['price']} | معاك: {qty}", callback_data=f"coin_{k}"))
    m.add(InlineKeyboardButton("💼 محفظتي", callback_data="my_portfolio"))
    m.add(InlineKeyboardButton("🔄 تحديث الأسعار", callback_data="trade"))
    m.add(InlineKeyboardButton("🔙 رجوع", callback_data="home"))
    return m

def owner_menu():
    m=InlineKeyboardMarkup(row_width=2)
    m.add(
        InlineKeyboardButton("👥 المستخدمين", callback_data="a_users"),
        InlineKeyboardButton("📊 احصائيات", callback_data="a_stats"),
        InlineKeyboardButton("📢 بث رسالة", callback_data="a_bc"),
        InlineKeyboardButton("🎁 كود للكل", callback_data="a_gift_all"),
        InlineKeyboardButton("🔍 بحث بال ID", callback_data="a_search"),
        InlineKeyboardButton("🛠️ صيانة", callback_data="a_maint"),
        InlineKeyboardButton("🏆 انهي المسابقة", callback_data="a_end"),
        InlineKeyboardButton("💰 ادي الكل فلوس", callback_data="a_all_money"),
        InlineKeyboardButton("🎰 سحب اليانصيب", callback_data="a_lottery_draw"),
        InlineKeyboardButton("💥 انفجار أسعار", callback_data="a_pump"),
    )
    m.add(InlineKeyboardButton("🔙 رجوع", callback_data="home"))
    return m

@bot.message_handler(commands=['start'])
def start(msg):
    if settings.get("maintenance") and not is_owner(msg.from_user.id):
        bot.send_message(msg.chat.id, "🛠️ البوت في الصيانة دلوقتي.. ارجع كمان شوية"); return
    if is_banned(msg.from_user.id):
        bot.send_message(msg.chat.id, "🚫 انت محظور من البوت"); return
    u=user(msg.from_user.id); u["name"]=msg.from_user.first_name or "مستخدم"
    if len(msg.text.split())>1:
        inv=msg.text.split()[1]
        if inv!=str(msg.from_user.id) and inv in data:
            add(int(inv),50)
            try: bot.send_message(int(inv), "🎉 صاحبك دخل! خدت +50")
            except: pass
    save(); vip=" 👑 VIP" if is_vip(u) else ""
    rank=get_rank(u["money"]+portfolio_value(u)+u.get("bank",0))
    bot.send_message(msg.chat.id, f"┏━━━━━━━━━━━━━━┓\n┃ 🎮 أهلاً {u['name']}{vip}\n┃ {rank}\n┃ 💰 {u['money']} جنيه\n┃ 🏦 بنك: {u.get('bank',0)}\n┃ {lvl_emoji(u['level'])} مستوى {u['level']} | ⭐ {u['xp']} XP\n┃ ⚡ قوة +{power(u)}\n┃ 📈 محفظة: {portfolio_value(u)}\n┗━━━━━━━━━━━━━━┛\n\nاختار 👇", reply_markup=menu(msg.from_user.id))

@bot.message_handler(commands=['owner','admin','id','rank'])
def owner_cmd(msg):
    if msg.text.startswith("/id"):
        bot.send_message(msg.chat.id, f"🆔 ID بتاعك: `{msg.from_user.id}`", parse_mode="Markdown"); return
    if msg.text.startswith("/rank"):
        u=user(msg.from_user.id); total=u["money"]+portfolio_value(u)+u.get("bank",0)
        bot.send_message(msg.chat.id, f"👑 رتبتك: {get_rank(total)}\n💰 ثروتك الكلية: {total}"); return
    if not is_owner(msg.from_user.id):
        bot.send_message(msg.chat.id, "❌ انت مش الأونر"); return
    bot.send_message(msg.chat.id, "👑 لوحة الأونر 🔥", reply_markup=owner_menu())

@bot.message_handler(func=lambda m: m.text and m.text.isdigit() and is_owner(m.from_user.id))
def search_id(msg):
    tid = msg.text.strip()
    if tid not in data:
        bot.send_message(msg.chat.id, "❌ مفيش حد بالـ ID ده"); return
    info=user(int(tid))
    m=InlineKeyboardMarkup(row_width=3)
    m.add(InlineKeyboardButton("➕100", callback_data=f"add_{tid}_100"), InlineKeyboardButton("➕1000", callback_data=f"add_{tid}_1000"), InlineKeyboardButton("➕10000", callback_data=f"add_{tid}_10000"))
    m.add(InlineKeyboardButton("➖100", callback_data=f"sub_{tid}_100"), InlineKeyboardButton("➖1000", callback_data=f"sub_{tid}_1000"), InlineKeyboardButton("💥 تصفير", callback_data=f"zero_{tid}"))
    m.add(InlineKeyboardButton("👑 VIP", callback_data=f"gv_{tid}"), InlineKeyboardButton("❌ شيل VIP", callback_data=f"rmvip_{tid}"), InlineKeyboardButton("🚫 حظر", callback_data=f"ban_{tid}"))
    m.add(InlineKeyboardButton("🔫 اديله سلاح", callback_data=f"givew_{tid}"))
    m.add(InlineKeyboardButton("🔙 لوحة الأونر", callback_data="owner"))
    bot.send_message(msg.chat.id, f"👤 {info.get('name')}\n🆔 {tid}\n💰 {info['money']}\n🏦 بنك: {info.get('bank',0)}\n⭐ مستوى {info['level']}\n👑 VIP: {'✅' if is_vip(info) else '❌'}", reply_markup=m)

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

        if d=="home":
            bot.send_message(cid, f"🏠 الرئيسية\n💰 معاك {u['money']} | مستوى {u['level']}", reply_markup=menu(uid)); return
        if d=="balance":
            total=u["money"]+portfolio_value(u)+u.get("bank",0)
            bot.send_message(cid, f"💰 ثروتك الكلية: {total}\n━━━━━━━━━━\n💵 كاش: {u['money']}\n🏦 بنك: {u.get('bank',0)}\n📈 محفظة تداول: {portfolio_value(u)}\n👑 رتبتك: {get_rank(total)}\n⭐ XP: {u['xp']} | مستوى {u['level']}\n🏆 نقاط: {u.get('score',0)}", reply_markup=menu(uid)); return
        if d=="play":
            bot.send_message(cid, f"🎮 العب واكسب\n💰 معاك {u['money']}", reply_markup=play_menu(uid)); return
        if d=="casino":
            bot.send_message(cid, f"🎰 الكازينو\n💰 معاك {u['money']}\n🎰 الجاكبوت: {settings.get('jackpot',1000)} جنيه", reply_markup=casino_menu(uid)); return
        if d=="shop":
            bot.send_message(cid, f"🛒 المتجر\n💰 معاك {u['money']}", reply_markup=shop_menu(uid)); return
        if d=="me":
            w=", ".join([WEAPONS[x][0] for x in u.get("weapons",[]) if x in WEAPONS]) or "مفيش"
            total=u["money"]+portfolio_value(u)+u.get("bank",0)
            bot.send_message(cid, f"👤 بروفايلك\n━━━━━━━━━━\n📛 {u['name']}\n🆔 {uid}\n{get_rank(total)}\n💰 كاش: {u['money']}\n🏦 بنك: {u.get('bank',0)}\n📈 محفظة: {portfolio_value(u)}\n💎 ثروة كلية: {total}\n{lvl_emoji(u['level'])} مستوى {u['level']} | XP {u['xp']}\n🔥 سلسلة {u.get('streak',0)}\n🏆 نقاط {u.get('score',0)}\n🔫 {w}\n👑 VIP: {'✅' if is_vip(u) else '❌'}\n━━━━━━━━━━", reply_markup=menu(uid)); return
        if d=="top":
            top=sorted(data.items(), key=lambda x: x[1].get('money',0)+portfolio_value(x[1])+x[1].get('bank',0), reverse=True)[:10]
            txt="🏆 ترتيب الأغنياء\n━━━━━━━━━━\n"
            medals=["🥇","🥈","🥉","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
            for i,(k,v) in enumerate(top):
                total=v.get('money',0)+portfolio_value(v)+v.get('bank',0)
                txt+=f"{medals[i]} {v.get('name','?')} — {total} 💰 | {get_rank(total)}\n"
            bot.send_message(cid, txt, reply_markup=menu(uid)); return
        if d=="invite":
            try: username=bot.get_me().username
            except: username="bot"
            bot.send_message(cid, f"👥 ابعت لصاحبك:\nhttps://t.me/{username}?start={uid}\n\nلو دخل هتاخد +50", reply_markup=menu(uid)); return
        if d=="streak": bot.send_message(cid, f"🔥 سلسلتك: {u.get('streak',0)} يوم", reply_markup=play_menu(uid)); return

        # ===== بنك =====
        if d=="bank":
            profit = int(u.get("bank",0)*0.10) if u.get("bank",0)>0 else 0
            m=InlineKeyboardMarkup(row_width=2)
            m.add(InlineKeyboardButton("💰 ايداع 100", callback_data="dep_100"), InlineKeyboardButton("💰 ايداع 500", callback_data="dep_500"), InlineKeyboardButton("💰 ايداع الكل", callback_data="dep_all"))
            m.add(InlineKeyboardButton("💸 سحب 100", callback_data="with_100"), InlineKeyboardButton("💸 سحب الكل", callback_data="with_all"))
            m.add(InlineKeyboardButton("📈 خد الفايدة", callback_data="interest"))
            m.add(InlineKeyboardButton("🔙 رجوع", callback_data="home"))
            bot.send_message(cid, f"🏦 البنك\n━━━━━━━━━━\n💰 في البنك: {u.get('bank',0)}\n💵 كاش: {u['money']}\n📈 فايدتك الجاهزة: {profit} (10%)\n\nحط فلوسك في البنك وخد 10% فايدة!", reply_markup=m); return
        if d.startswith("dep_"):
            amt = u["money"] if d=="dep_all" else int(d.replace("dep_",""))
            if u["money"] < amt or amt<=0: bot.send_message(cid, "❌ فلوسك مش كفاية", reply_markup=menu(uid)); return
            u["money"]-=amt; u["bank"]=u.get("bank",0)+amt; save(); bot.send_message(cid, f"✅ حطيت {amt} في البنك\n🏦 في البنك: {u['bank']}", reply_markup=menu(uid)); return
        if d.startswith("with_"):
            amt = u.get("bank",0) if d=="with_all" else int(d.replace("with_",""))
            if u.get("bank",0) < amt or amt<=0: bot.send_message(cid, "❌ مفيش في البنك كفاية", reply_markup=menu(uid)); return
            u["bank"]-=amt; u["money"]+=amt; save(); bot.send_message(cid, f"✅ سحبت {amt}\n💰 معاك {u['money']}", reply_markup=menu(uid)); return
        if d=="interest":
            if u.get("bank",0)<=0: bot.send_message(cid, "❌ حط فلوس في البنك الأول", reply_markup=menu(uid)); return
            profit=int(u.get("bank",0)*0.10); u["money"]+=profit; save(); bot.send_message(cid, f"📈 خدت فايدة +{profit}\n💰 معاك {u['money']}", reply_markup=menu(uid)); return

        # ===== كازينو =====
        if d=="slot":
            if u["money"]<30: bot.send_message(cid, "❌ محتاج 30 جنيه", reply_markup=casino_menu(uid)); return
            u["money"]-=30; fruits=["🍎","🍌","🍇","🍓","🍒","💎","7️⃣"]; r=[random.choice(fruits) for _ in range(3)]
            txt=f"🎰 {' | '.join(r)}\n\n"
            if r[0]==r[1]==r[2]:
                if r[0]=="💎": win=1000; txt+=f"💎💎💎 جاكبوت!!! +{win}"
                elif r[0]=="7️⃣": win=500; txt+=f"7️⃣7️⃣7️⃣ خرافي! +{win}"
                else: win=200; txt+=f"🎉 3 زي بعض! +{win}"
                u["money"]+=win; settings["jackpot"]=settings.get("jackpot",1000)+30
            elif r[0]==r[1] or r[1]==r[2] or r[0]==r[2]:
                win=60; u["money"]+=win; txt+=f"✅ 2 زي بعض! +{win}"
            else:
                txt+="😢 مفيش حاجة.. جرب تاني"
            save(); save_settings(); bot.send_message(cid, txt+f"\n💰 معاك {u['money']}", reply_markup=casino_menu(uid)); return
        if d=="dice":
            if u["money"]<20: bot.send_message(cid, "❌ محتاج 20", reply_markup=casino_menu(uid)); return
            u["money"]-=20; me=random.randint(1,6); bot_dice=random.randint(1,6)
            if me>bot_dice: u["money"]+=50; res=f"🎉 كسبت! انت {me} - البوت {bot_dice} +50"
            elif me<bot_dice: res=f"😢 خسرت! انت {me} - البوت {bot_dice}"
            else: u["money"]+=20; res=f"🤝 تعادل! انت {me} - البوت {bot_dice} رجعت فلوسك"
            save(); bot.send_message(cid, f"🎲 تحدي النرد\n{res}\n💰 معاك {u['money']}", reply_markup=casino_menu(uid)); return
        if d=="cards":
            if u["money"]<30: bot.send_message(cid, "❌ محتاج 30", reply_markup=casino_menu(uid)); return
            u["money"]-=30
            m=InlineKeyboardMarkup(row_width=3)
            for i in range(3): m.add(InlineKeyboardButton(f"🃏 كارت {i+1}", callback_data=f"pick_{i}"))
            m.add(InlineKeyboardButton("🔙", callback_data="casino"))
            bot.send_message(cid, "🃏 اختار كارت.. واحد فيهم فيه 200!", reply_markup=m); return
        if d.startswith("pick_"):
            win_card=random.randint(0,2); pick=int(d.replace("pick_",""))
            if pick==win_card: u["money"]+=200; save(); bot.send_message(cid, f"🎉 الكارت الصح! +200\n💰 معاك {u['money']}", reply_markup=casino_menu(uid))
            else: save(); bot.send_message(cid, f"😢 الكارت غلط.. كان الكارت {win_card+1}\n💰 معاك {u['money']}", reply_markup=casino_menu(uid))
            return
        if d=="lottery":
            m=InlineKeyboardMarkup()
            m.add(InlineKeyboardButton("🎟️ اشتري تذكرة - 50", callback_data="buy_ticket"))
            m.add(InlineKeyboardButton("🔙", callback_data="casino"))
            bot.send_message(cid, f"💎 اليانصيب\n━━━━━━━━━━\n🎟️ تذكرتك: {u.get('lottery_tickets',0)}\n👥 إجمالي التذاكر: {len(settings.get('lottery',[]))}\n🏆 الجايزة: {settings.get('jackpot',1000)} جنيه\n\nاشتري تذكرة والأونر هيسحب!", reply_markup=m); return
        if d=="buy_ticket":
            if u["money"]<50: bot.send_message(cid, "❌ محتاج 50", reply_markup=casino_menu(uid)); return
            u["money"]-=50; u["lottery_tickets"]=u.get("lottery_tickets",0)+1; settings.setdefault("lottery",[]).append(str(uid)); settings["jackpot"]=settings.get("jackpot",1000)+50; save(); save_settings(); bot.send_message(cid, f"✅ اشتريت تذكرة!\n🎟️ معاك {u['lottery_tickets']} تذكرة", reply_markup=casino_menu(uid)); return

        # ===== سرقة ومهمة سرية =====
        if d=="steal":
            now=int(time.time())
            if now-u.get("steal",0)<30: bot.send_message(cid, f"⏳ استنى {30-(now-u.get('steal',0))} ثانية", reply_markup=play_menu(uid)); return
            others=[k for k in data.keys() if k!=str(uid) and data[k].get("money",0)>50]
            if not others: bot.send_message(cid, "❌ مفيش حد تسرقه", reply_markup=play_menu(uid)); return
            victim=random.choice(others); v=data[victim]
            u["steal"]=now
            if random.random()<0.5:
                steal_amt=random.randint(20, min(100, v["money"]//2)); v["money"]-=steal_amt; u["money"]+=steal_amt; save()
                bot.send_message(cid, f"🥷 سرقت {steal_amt} من {v.get('name')} 😈\n💰 معاك {u['money']}", reply_markup=play_menu(uid))
                try: bot.send_message(int(victim), f"🥷 حد سرق منك {steal_amt} جنيه! خد بالك")
                except: pass
            else:
                fine=30; u["money"]=max(0,u["money"]-fine); save(); bot.send_message(cid, f"🚨 اتقفشت! دفعت غرامة {fine}\n💰 معاك {u['money']}", reply_markup=play_menu(uid))
            return
        if d=="secret":
            day=datetime.date.today().day
            missions=[("دوس على عجلة الحظ", "spin"), ("افتح صندوق", "gift"), ("اعمل مهمة", "tasks")]
            m_name, _ = missions[day % len(missions)]
            got=add(uid, 150)
            bot.send_message(cid, f"🎯 المهمة السرية النهاردة: {m_name}\n✅ خدت +{got} عشان دخلت!\n💰 معاك {u['money']}", reply_markup=play_menu(uid)); return

        # ===== تداول =====
        if d=="trade": bot.send_message(cid, f"📈 البورصة\n💰 معاك {u['money']}", reply_markup=trade_menu(uid)); return
        if d=="my_portfolio":
            pf=u.get("portfolio",{})
            if not pf or sum(pf.values())==0: bot.send_message(cid, "💼 محفظتك فاضية", reply_markup=trade_menu(uid)); return
            txt="💼 محفظتك\n━━━━━━━━━━\n"; total=0
            for k,qty in pf.items():
                if qty>0 and k in MARKET: val=qty*MARKET[k]["price"]; total+=val; txt+=f"{MARKET[k]['name']} | {qty} × {MARKET[k]['price']} = {val}\n"
            txt+=f"━━━━━━━━━━\nإجمالي: {total}\n💰 كاش: {u['money']}"
            bot.send_message(cid, txt, reply_markup=trade_menu(uid)); return
        if d.startswith("coin_"):
            k=d.replace("coin_",""); info=MARKET[k]; qty=u.get("portfolio",{}).get(k,0)
            m=InlineKeyboardMarkup(row_width=2); m.add(InlineKeyboardButton(f"🟢 اشتري 1 - {info['price']}", callback_data=f"buy_{k}_1"), InlineKeyboardButton(f"🟢 اشتري 5 - {info['price']*5}", callback_data=f"buy_{k}_5")); m.add(InlineKeyboardButton(f"🔴 بيع 1", callback_data=f"sell_{k}_1"), InlineKeyboardButton(f"🔴 بيع الكل", callback_data=f"sell_{k}_all")); m.add(InlineKeyboardButton("🔙 بورصة", callback_data="trade"))
            bot.send_message(cid, f"{info['name']}\n💲 السعر: {info['price']}\n📦 معاك: {qty}\n💰 فلوسك: {u['money']}", reply_markup=m); return
        if d.startswith("buy_"):
            _,k,amt=d.split("_"); amt=int(amt); price=MARKET[k]["price"]*amt
            if u["money"]<price: bot.send_message(cid, f"❌ محتاج {price} ومعاك {u['money']}", reply_markup=trade_menu(uid)); return
            u["money"]-=price; u["portfolio"][k]=u["portfolio"].get(k,0)+amt; save(); bot.send_message(cid, f"✅ اشتريت {amt} {MARKET[k]['name']}", reply_markup=trade_menu(uid)); return
        if d.startswith("sell_"):
            _,k,amt=d.split("_"); have=u.get("portfolio",{}).get(k,0)
            if have<=0: bot.send_message(cid, "❌ معكش من ده", reply_markup=trade_menu(uid)); return
            amt=have if amt=="all" else min(int(amt), have); gain=MARKET[k]["price"]*amt; u["money"]+=gain; u["portfolio"][k]-=amt; u["xp"]+=amt; save(); bot.send_message(cid, f"✅ بعت {amt} بـ {gain}", reply_markup=trade_menu(uid)); return

        # ===== لعب =====
        if d=="tasks":
            m=InlineKeyboardMarkup()
            for i,(name,rew) in enumerate(TASKS): m.add(InlineKeyboardButton(f"{name} +{rew+power(u)}", callback_data=f"t_{i}"))
            m.add(InlineKeyboardButton("🔙", callback_data="play")); bot.send_message(cid, "📋 اختار مهمة:", reply_markup=m); return
        if d.startswith("t_"):
            i=int(d.split("_")[1])
            if i==0:
                m=InlineKeyboardMarkup(row_width=2); m.add(InlineKeyboardButton("3", callback_data="wrong"), InlineKeyboardButton("4 ✅", callback_data="right_20"), InlineKeyboardButton("5", callback_data="wrong"), InlineKeyboardButton("6", callback_data="wrong")); bot.send_message(cid, "🧠 2+2 = كام؟", reply_markup=m)
            elif i==3:
                m=InlineKeyboardMarkup(row_width=2); m.add(InlineKeyboardButton("🍎", callback_data="wrong"), InlineKeyboardButton("🍌", callback_data="right_40"), InlineKeyboardButton("🍇", callback_data="wrong"), InlineKeyboardButton("🍓", callback_data="wrong")); bot.send_message(cid, "🍌 اختار موز", reply_markup=m)
            else: got=add(uid, TASKS[i][1]+power(u)); bot.send_message(cid, f"✅ خدت +{got}", reply_markup=play_menu(uid))
            return
        if d.startswith("right_"): got=add(uid, int(d.split("_")[1])+power(u)); bot.send_message(cid, f"✅ صح! +{got}", reply_markup=play_menu(uid)); return
        if d=="wrong": bot.send_message(cid, "❌ غلط", reply_markup=play_menu(uid)); return
        if d=="daily":
            now=int(time.time())
            if now-u.get("daily",0)<5: bot.send_message(cid, "⏳ استنى شوية", reply_markup=play_menu(uid))
            else: u["streak"]+=1; got=add(uid, (100 if is_vip(u) else 10)+u["streak"]*2); u["daily"]=now; save(); bot.send_message(cid, f"📅 يومية +{got}\n🔥 سلسلة {u['streak']}", reply_markup=play_menu(uid))
            return
        if d=="gift":
            now=int(time.time())
            if now-u.get("gift",0)<10: bot.send_message(cid, "⏳ استنى 10 ثواني", reply_markup=play_menu(uid))
            else: got=add(uid, 200 if is_vip(u) else random.choice([5,10,15,20,50,100])); u["gift"]=now; save(); bot.send_message(cid, f"🎁 +{got}", reply_markup=play_menu(uid))
            return
        if d=="spin":
            now=int(time.time())
            if now-u.get("spin",0)<10: bot.send_message(cid, "⏳ العجلة كل 10 ثواني", reply_markup=play_menu(uid))
            else: r=random.choice([0,5,10,20,30,50,100,200]); u["spin"]=now; save(); got=add(uid,r) if r>0 else 0; bot.send_message(cid, f"🎡 +{got}" if r>0 else "😢 صفر", reply_markup=play_menu(uid))
            return
        if d=="gamble":
            m=InlineKeyboardMarkup(row_width=2); m.add(InlineKeyboardButton("🪙 ملك - 20", callback_data="g_1"), InlineKeyboardButton("🪙 كتابة - 20", callback_data="g_2")); m.add(InlineKeyboardButton("🔙", callback_data="play")); bot.send_message(cid, f"🎲 معاك {u['money']}\nراهن 20 تكسب 40", reply_markup=m); return
        if d.startswith("g_"):
            if u["money"]<20: bot.send_message(cid, "❌ فلوسك مش كفاية", reply_markup=play_menu(uid)); return
            u["money"]-=20
            if random.choice([True,False]): u["money"]+=40; save(); bot.send_message(cid, f"🎉 كسبت +40\n💰 {u['money']}", reply_markup=play_menu(uid))
            else: save(); bot.send_message(cid, f"😢 خسرت 20\n💰 {u['money']}", reply_markup=play_menu(uid))
            return
        if d=="codes":
            m=InlineKeyboardMarkup(row_width=2)
            for c in CODES: m.add(InlineKeyboardButton(c, callback_data=f"code_{c}"))
            m.add(InlineKeyboardButton("🔙", callback_data="play")); bot.send_message(cid, "🎁 اختار كود:", reply_markup=m); return
        if d.startswith("code_"):
            c=d.replace("code_","")
            if c in u.get("codes",[]): bot.send_message(cid, "❌ استخدمته", reply_markup=play_menu(uid)); return
            u["codes"].append(c); got=add(uid, CODES[c]); bot.send_message(cid, f"🎉 +{got}", reply_markup=play_menu(uid)); return
        if d=="contest":
            top=sorted(data.items(), key=lambda x: x[1].get('score',0), reverse=True)[:5]
            txt="🏆 مسابقة اليوم - أعلى نقاط يكسب 500\n━━━━━━━━━━\n"
            for i,(k,v) in enumerate(top): txt+=f"{i+1}. {v.get('name','?')} — {v.get('score',0)}\n"
            txt+=f"\nنقطك: {u.get('score',0)}"
            bot.send_message(cid, txt, reply_markup=play_menu(uid)); return

        # ===== متجر =====
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
            if is_vip(u): bot.send_message(cid, "انت VIP أصلاً 👑", reply_markup=shop_menu(uid)); return
            m=InlineKeyboardMarkup(); m.add(InlineKeyboardButton("👑 اشتري VIP - 1000", callback_data="buy_vip")); m.add(InlineKeyboardButton("🔙", callback_data="shop")); bot.send_message(cid, "👑 VIP\n✅ كل حاجة ×2\nالسعر 1000", reply_markup=m); return
        if d=="buy_vip":
            if u["money"]>=1000: u["money"]-=1000; u["vip"]=True; save(); bot.send_message(cid, "🎉 بقيت VIP 👑", reply_markup=shop_menu(uid))
            else: bot.send_message(cid, "❌ فلوسك مش كفاية", reply_markup=shop_menu(uid))
            return

        # ===== أونر =====
        if d=="owner":
            if not is_owner(uid): bot.send_message(cid, "❌ انت مش الأونر"); return
            total_money=sum(v.get('money',0) for v in data.values())
            bot.send_message(cid, f"👑 لوحة الأونر 🔥\n━━━━━━━━━━\n👥 {len(data)} مستخدم\n💰 فلوس الكل: {total_money}\n⭐ VIP: {sum(1 for v in data.values() if v.get('vip'))}\n🚫 محظورين: {len(settings.get('banned',[]))}\n🛠️ صيانة: {'🔴 مقفول' if settings.get('maintenance') else '🟢 شغال'}\n🎰 جاكبوت: {settings.get('jackpot',1000)}\n━━━━━━━━━━", reply_markup=owner_menu()); return
        if d=="a_stats":
            if not is_owner(uid): return
            if not data: bot.send_message(cid, "مفيش حد", reply_markup=owner_menu()); return
            richest=max(data.items(), key=lambda x: x[1].get('money',0))
            top_score=max(data.items(), key=lambda x: x[1].get('score',0))
            bot.send_message(cid, f"📊 احصائيات\n━━━━━━━━━━\n👥 {len(data)}\n💰 إجمالي: {sum(v.get('money',0) for v in data.values())}\n🥇 أغنى واحد: {richest[1].get('name')} - {richest[1].get('money')}\n🏆 أكتر نقاط: {top_score[1].get('name')} - {top_score[1].get('score')}\n━━━━━━━━━━", reply_markup=owner_menu()); return
        if d=="a_users":
            if not is_owner(uid): return
            m=InlineKeyboardMarkup()
            for k,v in list(data.items())[:20]:
                vip=" 👑" if v.get("vip") else ""
                m.add(InlineKeyboardButton(f"{v.get('name','?')}{vip} — {v.get('money',0)}", callback_data=f"a_u_{k}"))
            m.add(InlineKeyboardButton("🔙", callback_data="owner")); bot.send_message(cid, "👥 دوس على واحد:", reply_markup=m); return
        if d.startswith("a_u_"):
            if not is_owner(uid): return
            t=d.replace("a_u_",""); info=user(int(t))
            m=InlineKeyboardMarkup(row_width=3)
            m.add(InlineKeyboardButton("➕100", callback_data=f"add_{t}_100"), InlineKeyboardButton("➕1000", callback_data=f"add_{t}_1000"), InlineKeyboardButton("➕10000", callback_data=f"add_{t}_10000"))
            m.add(InlineKeyboardButton("➖100", callback_data=f"sub_{t}_100"), InlineKeyboardButton("➖1000", callback_data=f"sub_{t}_1000"), InlineKeyboardButton("💥 تصفير", callback_data=f"zero_{t}"))
            m.add(InlineKeyboardButton("👑 VIP", callback_data=f"gv_{t}"), InlineKeyboardButton("❌ شيل VIP", callback_data=f"rmvip_{t}"))
            m.add(InlineKeyboardButton("🚫 حظر", callback_data=f"ban_{t}"), InlineKeyboardButton("✅ فك حظر", callback_data=f"unban_{t}"))
            m.add(InlineKeyboardButton("🔫 سلاح", callback_data=f"givew_{t}"))
            m.add(InlineKeyboardButton("🔙", callback_data="a_users"))
            bot.send_message(cid, f"👤 {info.get('name')}\n🆔 {t}\n💰 {info['money']}\n⭐ {info['level']}\n👑 {'✅' if is_vip(info) else '❌'}", reply_markup=m); return
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
            t=d.replace("zero_",""); info=user(int(t)); info["money"]=0; info["score"]=0; info["portfolio"]={}; info["bank"]=0; save(); bot.send_message(cid, f"💥 صفرت {info.get('name')}", reply_markup=owner_menu()); return
        if d.startswith("rmvip_"):
            if not is_owner(uid): return
            t=d.replace("rmvip_",""); info=user(int(t)); info["vip"]=False; save(); bot.send_message(cid, f"❌ شلت VIP من {info.get('name')}", reply_markup=owner_menu()); return
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
            t=d.replace("gv_",""); info=user(int(t)); info["vip"]=True; save(); bot.send_message(cid, f"✅ {info.get('name')} بقى VIP", reply_markup=owner_menu()); return
        if d.startswith("add_") or d.startswith("sub_"):
            if not is_owner(uid): return
            _,t,amt=d.split("_"); amt=int(amt); info=user(int(t))
            if d.startswith("add_"): info["money"]+=amt
            else: info["money"]=max(0, info["money"]-amt)
            save(); bot.send_message(cid, f"✅ بقى معاه {info['money']}", reply_markup=owner_menu()); return
        if d=="a_search":
            if not is_owner(uid): return
            bot.send_message(cid, "🔍 ابعت ID الشخص\nاكتب /id عشان تعرف ID أي حد", reply_markup=owner_menu()); return
        if d=="a_maint":
            if not is_owner(uid): return
            m=InlineKeyboardMarkup(row_width=2)
            btn_text="🟢 فتح البوت" if settings.get("maintenance") else "🔴 قفل البوت (صيانة)"
            m.add(InlineKeyboardButton(btn_text, callback_data="toggle_maint"))
            m.add(InlineKeyboardButton("💥 تصفير كل الفلوس", callback_data="reset_all"))
            m.add(InlineKeyboardButton("🔙", callback_data="owner"))
            bot.send_message(cid, f"🛠️ الصيانة\nالحالة: {'🔴 مقفول' if settings.get('maintenance') else '🟢 شغال'}", reply_markup=m); return
        if d=="toggle_maint":
            if not is_owner(uid): return
            settings["maintenance"]=not settings.get("maintenance",False); save_settings()
            bot.send_message(cid, f"{'🔴 قفلت البوت' if settings['maintenance'] else '🟢 فتحت البوت'}", reply_markup=owner_menu()); return
        if d=="reset_all":
            if not is_owner(uid): return
            m=InlineKeyboardMarkup(row_width=2); m.add(InlineKeyboardButton("✅ أيوه صفر الكل", callback_data="confirm_reset"), InlineKeyboardButton("❌ لا", callback_data="owner")); bot.send_message(cid, "⚠️ متأكد؟ هتصفر فلوس الكل!", reply_markup=m); return
        if d=="confirm_reset":
            if not is_owner(uid): return
            for k in data: data[k]["money"]=0; data[k]["score"]=0; data[k]["portfolio"]={}; data[k]["bank"]=0
            save(); bot.send_message(cid, "💥 صفرت الكل", reply_markup=owner_menu()); return
        if d=="a_all_money":
            if not is_owner(uid): return
            m=InlineKeyboardMarkup(row_width=2); m.add(InlineKeyboardButton("➕100 للكل", callback_data="all_100"), InlineKeyboardButton("➕500 للكل", callback_data="all_500"), InlineKeyboardButton("➕1000 للكل", callback_data="all_1000")); m.add(InlineKeyboardButton("🔙", callback_data="owner")); bot.send_message(cid, "💰 ادي الكل:", reply_markup=m); return
        if d.startswith("all_"):
            if not is_owner(uid): return
            amt=int(d.replace("all_",""))
            for k in data: data[k]["money"]+=amt
            save(); bot.send_message(cid, f"✅ اديت {amt} للكل", reply_markup=owner_menu()); return
        if d=="a_gift_all":
            if not is_owner(uid): return
            m=InlineKeyboardMarkup(row_width=2); m.add(InlineKeyboardButton("🎁 100 للكل", callback_data="giftall_100"), InlineKeyboardButton("🎁 500 للكل", callback_data="giftall_500")); m.add(InlineKeyboardButton("🔙", callback_data="owner")); bot.send_message(cid, "🎁 هدية للكل:", reply_markup=m); return
        if d.startswith("giftall_"):
            if not is_owner(uid): return
            amt=int(d.replace("giftall_","")); c=0
            for k in list(data.keys()):
                try: bot.send_message(int(k), f"🎁 هدية من الأونر! +{amt} 🔥"); data[k]["money"]+=amt; c+=1
                except: pass
            save(); bot.send_message(cid, f"✅ بعت لـ {c}", reply_markup=owner_menu()); return
        if d=="a_bc":
            if not is_owner(uid): return
            m=InlineKeyboardMarkup(row_width=2); m.add(InlineKeyboardButton("🎉 مسابقة!", callback_data="bc_1"), InlineKeyboardButton("🔥 خصم!", callback_data="bc_2"), InlineKeyboardButton("👋 ارجع العب", callback_data="bc_3"), InlineKeyboardButton("📈 البورصة ولعت", callback_data="bc_4")); m.add(InlineKeyboardButton("🔙", callback_data="owner")); bot.send_message(cid, "📢 اختار رسالة:", reply_markup=m); return
        if d.startswith("bc_"):
            if not is_owner(uid): return
            texts={"bc_1":"🎉 مسابقة جديدة! ادخل والعب وخد 500","bc_2":"🔥 خصم في المتجر! الحق اشتري","bc_3":"👋 ارجع العب وخد فلوس","bc_4":"📈 البورصة ولعت! الحق اشتري وبيع"}
            c=0
            for k in list(data.keys()):
                try: bot.send_message(int(k), f"📢 من الأونر:\n\n{texts[d]}"); c+=1
                except: pass
            bot.send_message(cid, f"✅ بعت لـ {c}", reply_markup=owner_menu()); return
        if d=="a_end":
            if not is_owner(uid): return
            if not data: bot.send_message(cid, "مفيش حد", reply_markup=owner_menu()); return
            w=max(data.items(), key=lambda x: x[1].get('score',0)); wid,winfo=w; winfo["money"]+=500; winfo["score"]=0; save()
            for k in data:
                if k!=wid: data[k]["score"]=0
            save()
            try: bot.send_message(int(wid), "🏆 كسبت المسابقة! +500")
            except: pass
            bot.send_message(cid, f"🏆 الفايز: {winfo.get('name')} +500", reply_markup=owner_menu()); return
        if d=="a_lottery_draw":
            if not is_owner(uid): return
            lot=settings.get("lottery",[])
            if not lot: bot.send_message(cid, "❌ مفيش حد اشترى تذاكر", reply_markup=owner_menu()); return
            winner=random.choice(lot); prize=settings.get("jackpot",1000); winfo=user(int(winner)); winfo["money"]+=prize; winfo["lottery_tickets"]=0; save()
            settings["lottery"]=[]; settings["jackpot"]=1000; save_settings()
            for k in data:
                try: bot.send_message(int(k), f"💎 نتيجة اليانصيب!\n🏆 الفايز: {winfo.get('name')} كسب {prize} جنيه!")
                except: pass
            bot.send_message(cid, f"🏆 الفايز: {winfo.get('name')} +{prize}", reply_markup=owner_menu()); return
        if d=="a_pump":
            if not is_owner(uid): return
            for k in MARKET: MARKET[k]["price"]+=random.randint(50,150)
            bot.send_message(cid, f"💥 فجرت الأسعار!\n" + "\n".join([f"{v['name']}: {v['price']}" for v in MARKET.values()]), reply_markup=owner_menu())
            for k in list(data.keys()):
                try: bot.send_message(int(k), "📈💥 البورصة ولعت! الأسعار طارت! الحق بيع!")
                except: pass
            return
    except Exception as e:
        print("Error:", e, traceback.format_exc())
        try: bot.send_message(cid, "حصل مشكلة.. دوس تاني", reply_markup=menu(uid))
        except: pass

print("Bot is running...")
while True:
    try: bot.infinity_polling(timeout=60, long_polling_timeout=60, skip_pending=True)
    except: time.sleep(5)
