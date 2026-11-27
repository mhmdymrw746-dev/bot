# 👑 TRAN BOT - FULL VERSION - كل الانظمة
import os, time, random, threading, requests, json
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN") or "حط_التوكن_هنا"
OWNER = "TRAN_5"
SUPPORT = ["cat_max_10", "MOON_104"]
DATA_FILE = "data.json"

def load():
    try:
        with open(DATA_FILE) as f: return json.load(f)
    except: return {"users": {}, "tickets": {}, "auction": []}
def save(d):
    with open(DATA_FILE, "w") as f: json.dump(d, f)
db = load()

def get_user(uid, name=""):
    uid=str(uid)
    if uid not in db["users"]:
        db["users"][uid]={"name":name,"cash":1000,"bank":0,"health":100,"happy":100,"energy":100,
        "job":"بدون شغل","car":"مفيش","house":"مفيش","married":"اعزب","partner":None,
        "kids":0,"level":1,"xp":0,"vip":False,"company":None,"farm":0,"restaurant":0,"hotel":0,
        "land":0,"stock":0,"jail":0,"wanted":0,"gang":None,"army":False,"mafia":False,
        "edu":0,"passport":False,"visa_card":False,"pet":None,"warns":0,"banned":False,
        "coupon":0,"gifts":0,"titles":[],"cars":[],"houses":[],"business":0,"crypto":0}
        save(db)
    return db["users"][uid]

# --- سيرفر يصحي نفسه ---
app_flask=Flask(__name__)
@app_flask.route('/')
def home(): return "TRAN BOT شغال 👑🔥 - كل الانظمة"
def run_flask():
    app_flask.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
def self_ping():
    url=os.environ.get("RENDER_EXTERNAL_URL") or "https://اسم-بوتك.onrender.com"
    while True:
        time.sleep(840)
        try: requests.get(url,timeout=10); print("✅ صحيت نفسي")
        except: pass

def KB(rows): return InlineKeyboardMarkup(rows)
def BACK(): return KB([[InlineKeyboardButton("🔙 رجوع",callback_data="back")]])

def main_menu():
    return KB([
        [InlineKeyboardButton("👤 بروفايلي",callback_data="profile"),InlineKeyboardButton("💼 شغلي",callback_data="job_menu")],
        [InlineKeyboardButton("🏦 البنك",callback_data="bank"),InlineKeyboardButton("🏠 بيتي",callback_data="home_menu")],
        [InlineKeyboardButton("🛒 المتجر",callback_data="shop"),InlineKeyboardButton("🎰 العب واكسب",callback_data="play_menu")],
        [InlineKeyboardButton("👥 صحابي",callback_data="friends"),InlineKeyboardButton("💍 عيلتي",callback_data="family")],
        [InlineKeyboardButton("🏢 شركتي",callback_data="company"),InlineKeyboardButton("🌾 مزرعتي",callback_data="farm")],
        [InlineKeyboardButton("🍔 مطعمي",callback_data="restaurant"),InlineKeyboardButton("🏨 فندقي",callback_data="hotel")],
        [InlineKeyboardButton("⚔️ عصابة / حرب",callback_data="gang_menu"),InlineKeyboardButton("🏫 تعليم / جيش",callback_data="edu_menu")],
        [InlineKeyboardButton("✈️ سفر",callback_data="travel"),InlineKeyboardButton("📈 بورصة",callback_data="stock")],
        [InlineKeyboardButton("🎁 هدايا / كوبون",callback_data="gift_menu"),InlineKeyboardButton("💎 VIP",callback_data="vip")],
        [InlineKeyboardButton("🛎️ خدمة عملاء",callback_data="support")],
    ])

async def start(update,context):
    u=update.effective_user; user=get_user(u.id,u.first_name)
    if user["banned"]:
        await update.message.reply_text("🚫 انت مبند من البوت"); return
    txt=f"""👑 أهلاً بيك في عالم TRAN 👑

👤 {user['name']} | 🏆 لفل {user['level']} | XP {user['xp']}
💰 كاش: {user['cash']} | 🏦 بنك: {user['bank']}
❤️ صحة: {user['health']} | 😊 سعادة: {user['happy']} | ⚡ طاقة: {user['energy']}
💼 {user['job']} | 🚗 {user['car']} | 🏠 {user['house']}
💍 {user['married']} | 👶 عيال: {user['kids']} | 💎 VIP: {'✅' if user['vip'] else '❌'}
⚠️ تحذيرات: {user['warns']} | 🚔 مطلوب: {user['wanted']}

دوس على أي زرار 👇"""
    if update.message: await update.message.reply_text(txt,reply_markup=main_menu())
    else: await update.callback_query.edit_message_text(txt,reply_markup=main_menu())
   async def buttons(update,context):
    q=update.callback_query; await q.answer(); uid=str(q.from_user.id)
    user=get_user(uid,q.from_user.first_name); d=q.data
    if user["banned"]: await q.edit_message_text("🚫 مبند"); return
    if d=="back": await start(update,context); return

    # --- بروفايل ---
    if d=="profile":
        txt=f"👤 {user['name']}\n💰 {user['cash']} | 🏦 {user['bank']}\n❤️ {user['health']} | 😊 {user['happy']} | ⚡ {user['energy']}\n💼 {user['job']}\n🚗 {user['car']} | 🏠 {user['house']}\n💍 {user['married']} | 👶 {user['kids']}\n🏢 شركه: {user['company']} | 🌾 مزرعه: {user['farm']}\n🏆 لفل {user['level']} | 💎 VIP {user['vip']}\n🎖️ القاب: {', '.join(user['titles']) or 'مفيش'}"
        await q.edit_message_text(txt,reply_markup=BACK())

    # --- البنك الكامل ---
    elif d=="bank":
        interest=int(user['bank']*0.05)
        txt=f"🏦 بنك TRAN\n💰 كاش {user['cash']} | 🏦 بنك {user['bank']}\n📈 فايدة اليوم {interest} (5%)\n💳 فيزا: {'✅' if user['visa_card'] else '❌'}"
        await q.edit_message_text(txt,reply_markup=KB([
            [InlineKeyboardButton("💰 إيداع 1000",callback_data="dep_1000"),InlineKeyboardButton("💸 سحب 1000",callback_data="wit_1000")],
            [InlineKeyboardButton("💰 إيداع الكل",callback_data="dep_all"),InlineKeyboardButton("💸 سحب الكل",callback_data="wit_all")],
            [InlineKeyboardButton("📈 خد الفايدة",callback_data="interest"),InlineKeyboardButton("💳 فيزا 500",callback_data="visa")],
            [InlineKeyboardButton("🏦 قرض 10000",callback_data="loan"),InlineKeyboardButton("📜 شهادة 5000",callback_data="cert")],
            [InlineKeyboardButton("🎁 حصالة",callback_data="piggy"),InlineKeyboardButton("💎 حساب VIP",callback_data="vip_bank")],
            [InlineKeyboardButton("🔙 رجوع",callback_data="back")]]))
    elif d.startswith("dep_"):
        amt=user['cash'] if "all" in d else 1000
        if user['cash']>=amt and amt>0: user['cash']-=amt; user['bank']+=amt; save(db); await q.edit_message_text(f"✅ حطيت {amt} | بنكك {user['bank']}",reply_markup=BACK())
        else: await q.edit_message_text("❌ معكش فلوس",reply_markup=BACK())
    elif d.startswith("wit_"):
        amt=user['bank'] if "all" in d else 1000
        if user['bank']>=amt and amt>0: user['bank']-=amt; user['cash']+=amt; save(db); await q.edit_message_text(f"✅ سحبت {amt} | كاشك {user['cash']}",reply_markup=BACK())
        else: await q.edit_message_text("❌ معكش في البنك",reply_markup=BACK())
    elif d=="interest":
        intr=int(user['bank']*0.05)
        if intr>0: user['bank']+=intr; save(db); await q.edit_message_text(f"🎉 فايدة {intr} | بنكك {user['bank']}",reply_markup=BACK())
        else: await q.edit_message_text("❌ حط فلوس الاول",reply_markup=BACK())
    elif d=="visa":
        if user['cash']>=500: user['cash']-=500; user['visa_card']=True; save(db); await q.edit_message_text("💳 مبروك فيزا! محدش يسرقك",reply_markup=BACK())
        else: await q.edit_message_text("❌ محتاج 500",reply_markup=BACK())
    elif d=="loan":
        user['cash']+=10000; save(db); await q.edit_message_text("🏦 قرض 10000 | سدده في 7 ايام",reply_markup=BACK())
    elif d=="cert":
        if user['cash']>=5000: user['cash']-=5000; user['bank']+=7000; save(db); await q.edit_message_text("📜 شهادة! دفعت 5000 وخدت 7000 في البنك",reply_markup=BACK())
        else: await q.edit_message_text("❌ محتاج 5000",reply_markup=BACK())
    elif d=="piggy":
        user['bank']+=500; save(db); await q.edit_message_text("🎁 حصالتك ادتك 500!",reply_markup=BACK())
    elif d=="vip_bank":
        if user['vip']: user['bank']+=2000; save(db); await q.edit_message_text("💎 بونص VIP 2000!",reply_markup=BACK())
        else: await q.edit_message_text("❌ لازم تبقى VIP الاول",reply_markup=BACK())

    # --- شغل + شركه + مزرعه + مطعم + فندق ---
    elif d=="job_menu":
        await q.edit_message_text("💼 اختار شغلك:",reply_markup=KB([
            [InlineKeyboardButton("💼 اشتغل",callback_data="work"),InlineKeyboardButton("🎓 ادرس",callback_data="study")],
            [InlineKeyboardButton("🏢 اعمل شركة",callback_data="make_company"),InlineKeyboardButton("📈 استثمر",callback_data="invest")],
            [InlineKeyboardButton("🔙 رجوع",callback_data="back")]]))
    elif d=="work":
        jobs=[("يوتيوبر",2000),("لاعب كورة",3000),("دكتور",5000),("تاجر",4000),("مدرس",2500),("مهندس",4500)]
        j,s=random.choice(jobs); user['cash']+=s; user['job']=j; user['xp']+=10; user['energy']-=10; save(db)
        await q.edit_message_text(f"💼 اشتغلت {j} وكسبت {s} | كاشك {user['cash']}",reply_markup=BACK())
    elif d=="study":
        user['edu']+=1; user['xp']+=20; save(db); await q.edit_message_text(f"🎓 درست! مستواك التعليمي {user['edu']} | XP زاد",reply_markup=BACK())
    elif d=="make_company":
        if user['cash']>=20000: user['cash']-=20000; user['company']="شركة TRAN"; save(db); await q.edit_message_text("🏢 مبروك عملت شركة! كل يوم هتكسب",reply_markup=BACK())
        else: await q.edit_message_text("❌ محتاج 20000",reply_markup=BACK())
    elif d=="invest":
        win=random.randint(-2000,5000); user['cash']+=win; save(db); await q.edit_message_text(f"📈 استثمرت وكسبت {win} | كاشك {user['cash']}",reply_markup=BACK())
    elif d=="company":
        profit=random.randint(1000,5000) if user['company'] else 0
        user['cash']+=profit; save(db); await q.edit_message_text(f"🏢 شركتك: {user['company'] or 'مفيش'}\nربح اليوم: {profit} | كاشك {user['cash']}",reply_markup=BACK())
    elif d=="farm":
        if user['cash']>=10000 and user['farm']==0: user['cash']-=10000; user['farm']=1; save(db); await q.edit_message_text("🌾 اشتريت مزرعة!",reply_markup=BACK())
        elif user['farm']>0:
            harvest=random.randint(1000,3000); user['cash']+=harvest; save(db); await q.edit_message_text(f"🌾 حصدت وكسبت {harvest}",reply_markup=BACK())
        else: await q.edit_message_text("❌ محتاج 10000 للمزرعة",reply_markup=BACK())
    elif d=="restaurant":
        if user['cash']>=15000 and user['restaurant']==0: user['cash']-=15000; user['restaurant']=1; save(db); await q.edit_message_text("🍔 فتحت مطعم!",reply_markup=BACK())
        elif user['restaurant']>0: p=random.randint(1000,4000); user['cash']+=p; save(db); await q.edit_message_text(f"🍔 مطعمك كسب {p} النهاردة",reply_markup=BACK())
        else: await q.edit_message_text("❌ محتاج 15000",reply_markup=BACK())
    elif d=="hotel":
        if user['cash']>=50000 and user['hotel']==0: user['cash']-=50000; user['hotel']=1; save(db); await q.edit_message_text("🏨 فتحت فندق!",reply_markup=BACK())
        elif user['hotel']>0: p=random.randint(3000,8000); user['cash']+=p; save(db); await q.edit_message_text(f"🏨 فندقك كسب {p}",reply_markup=BACK())
        else: await q.edit_message_text("❌ محتاج 50000",reply_markup=BACK())

    # --- بيتي + متجر + سفر + حيوان ---
    elif d=="home_menu":
        await q.edit_message_text("🏠 بيتك:",reply_markup=KB([
            [InlineKeyboardButton("🏠 اشتري بيت",callback_data="buy_house"),InlineKeyboardButton("🚗 اشتري عربية",callback_data="buy_car")],
            [InlineKeyboardButton("🐶 حيوان أليف",callback_data="pet"),InlineKeyboardButton("🛋️ اثاث",callback_data="furniture")],
            [InlineKeyboardButton("🔙 رجوع",callback_data="back")]]))
    elif d=="buy_house":
        if user['cash']>=100000: user['cash']-=100000; user['house']="فيلا"; save(db); await q.edit_message_text("🎉 اشتريت فيلا!",reply_markup=BACK())
        else: await q.edit_message_text("❌ محتاج 100000",reply_markup=BACK())
    elif d=="buy_car":
        if user['cash']>=50000: user['cash']-=50000; user['car']="BMW"; save(db); await q.edit_message_text("🎉 اشتريت BMW!",reply_markup=BACK())
        else: await q.edit_message_text("❌ محتاج 50000",reply_markup=BACK())
    elif d=="pet":
        pets=["كلب","قطة","حصان"]; p=random.choice(pets); user['pet']=p; save(db); await q.edit_message_text(f"🐶 جبت {p}!",reply_markup=BACK())
    elif d=="furniture":
        if user['cash']>=2000: user['cash']-=2000; user['happy']+=20; save(db); await q.edit_message_text("🛋️ جبت اثاث جديد! سعادتك زادت",reply_markup=BACK())
        else: await q.edit_message_text("❌ محتاج 2000",reply_markup=BACK())
    elif d=="shop":
        await q.edit_message_text("🛒 المتجر:",reply_markup=KB([
            [InlineKeyboardButton("🚗 عربيات",callback_data="buy_car"),InlineKeyboardButton("🏠 بيوت",callback_data="buy_house")],
            [InlineKeyboardButton("🔫 سلاح 5000",callback_data="buy_gun"),InlineKeyboardButton("👕 ملابس 1000",callback_data="buy_clothes")],
            [InlineKeyboardButton("💍 مجوهرات 10000",callback_data="buy_jewel"),InlineKeyboardButton("🎁 هدية 500",callback_data="buy_gift")],
            [InlineKeyboardButton("🔙 رجوع",callback_data="back")]]))
    elif d=="buy_gun":
        if user['cash']>=5000: user['cash']-=5000; save(db); await q.edit_message_text("🔫 اشتريت سلاح! دلوقتي تقدر تحارب",reply_markup=BACK())
        else: await q.edit_message_text("❌ محتاج 5000",reply_markup=BACK())
    elif d=="buy_clothes":
        if user['cash']>=1000: user['cash']-=1000; user['happy']+=10; save(db); await q.edit_message_text("👕 لبس جديد! سعادتك زادت",reply_markup=BACK())
        else: await q.edit_message_text("❌ محتاج 1000",reply_markup=BACK())
    elif d=="buy_jewel":
        if user['cash']>=10000: user['cash']-=10000; save(db); await q.edit_message_text("💍 اشتريت مجوهرات فاخرة!",reply_markup=BACK())
        else: await q.edit_message_text("❌ محتاج 10000",reply_markup=BACK())
    elif d=="buy_gift":
        if user['cash']>=500: user['cash']-=500; user['gifts']+=1; save(db); await q.edit_message_text("🎁 اشتريت هدية!",reply_markup=BACK())
        else: await q.edit_message_text("❌ محتاج 500",reply_markup=BACK())
    elif d=="travel":
        await q.edit_message_text("✈️ سفر:",reply_markup=KB([
            [InlineKeyboardButton("🇪🇬 مصر 1000",callback_data="travel_eg"),InlineKeyboardButton("🇸🇦 السعودية 3000",callback_data="travel_sa")],
            [InlineKeyboardButton("🇦🇪 دبي 5000",callback_data="travel_dubai"),InlineKeyboardButton("🇺🇸 امريكا 10000",callback_data="travel_usa")],
            [InlineKeyboardButton("🛂 جواز سفر 2000",callback_data="passport"),InlineKeyboardButton("🔙 رجوع",callback_data="back")]]))
    elif d.startswith("travel_"):
        costs={"travel_eg":1000,"travel_sa":3000,"travel_dubai":5000,"travel_usa":10000}
        c=costs[d]
        if not user['passport'] and d!="travel_eg": await q.edit_message_text("❌ لازم جواز سفر الاول!",reply_markup=BACK())
        elif user['cash']>=c: user['cash']-=c; user['happy']+=30; save(db); await q.edit_message_text(f"✈️ سافرت! سعادتك زادت | كاشك {user['cash']}",reply_markup=BACK())
        else: await q.edit_message_text("❌ معكش فلوس",reply_markup=BACK())
    elif d=="passport":
        if user['cash']>=2000: user['cash']-=2000; user['passport']=True; save(db); await q.edit_message_text("🛂 طلعت جواز سفر!",reply_markup=BACK())
        else: await q.edit_message_text("❌ محتاج 2000",reply_markup=BACK())

    # --- العب واكسب ---
    elif d=="play_menu":
        await q.edit_message_text("🎰 العب واكسب:",reply_markup=KB([
            [InlineKeyboardButton("🎰 كازينو",callback_data="casino"),InlineKeyboardButton("🏇 سباق",callback_data="race")],
            [InlineKeyboardButton("🗺️ كنز",callback_data="treasure"),InlineKeyboardButton("🎁 حظي اليوم",callback_data="luck")],
            [InlineKeyboardButton("🎯 مهمة اليوم",callback_data="mission"),InlineKeyboardButton("📋 مهامي",callback_data="mission")],
            [InlineKeyboardButton("🔙 رجوع",callback_data="back")]]))
    elif d=="casino":
        win=random.randint(-2000,5000); user['cash']+=win; save(db); await q.edit_message_text(f"🎰 كازينو: {win} | كاشك {user['cash']}",reply_markup=BACK())
    elif d=="race":
        win=random.choice([0,1000,5000,10000]); user['cash']+=win; save(db); await q.edit_message_text(f"🏇 سباق: كسبت {win}",reply_markup=BACK())
    elif d=="treasure":
        win=random.choice([0,0,2000,10000,50000]); user['cash']+=win; save(db); await q.edit_message_text(f"🗺️ كنز: لقيت {win}!",reply_markup=BACK())
    elif d=="luck":
        msgs=["اليوم حظك حلو هتكسب","خلي بالك من السرقة","حد بيحبك","هتلاقي فلوس في الشارع"]; m=random.choice(msgs); user['cash']+=500; save(db); await q.edit_message_text(f"🎁 حظك: {m} | خدت 500",reply_markup=BACK())
    elif d=="mission":
        user['cash']+=1000; user['xp']+=15; save(db); await q.edit_message_text("🎯 خلصت مهمة! +1000 +15 XP",reply_markup=BACK())

    # --- عيلة وصحاب ---
    elif d=="friends":
        await q.edit_message_text("👥 صحابي - ابعت لصاحبك يوزرك وخليه يدوس /start",reply_markup=BACK())
    elif d=="family":
        await q.edit_message_text("💍 عيلتك:",reply_markup=KB([
            [InlineKeyboardButton("💍 اتجوز",callback_data="marry"),InlineKeyboardButton("💔 طلق",callback_data="divorce")],
            [InlineKeyboardButton("👶 خلف عيل",callback_data="baby"),InlineKeyboardButton("👨‍👩‍👦 عيلتي",callback_data="my_family")],
            [InlineKeyboardButton("🔙 رجوع",callback_data="back")]]))
    elif d=="marry":
        if user['married']=="اعزب": user['married']="متجوز"; user['happy']+=30; save(db); await q.edit_message_text("💍 مبروك اتجوزت! ❤️",reply_markup=BACK())
        else: await q.edit_message_text("❌ انت متجوز اصلا!",reply_markup=BACK())
    elif d=="divorce":
        if user['married']!="اعزب": user['married']="اعزب"; user['cash']=int(user['cash']/2); save(db); await q.edit_message_text("💔 اطلقت وخسرت نص فلوسك!",reply_markup=BACK())
        else: await q.edit_message_text("❌ انت اعزب اصلا",reply_markup=BACK())
    elif d=="baby":
        if user['married']!="اعزب": user['kids']+=1; save(db); await q.edit_message_text(f"👶 مبروك جالك عيل! عندك {user['kids']} عيال",reply_markup=BACK())
        else: await q.edit_message_text("❌ لازم تتجوز الاول!",reply_markup=BACK())
    elif d=="my_family":
        await q.edit_message_text(f"👨‍👩‍👦 عيلتك: {user['married']} | عيال: {user['kids']}",reply_markup=BACK())

    # --- عصابة وحرب وجيش ومافيا ---
    elif d=="gang_menu":
        await q.edit_message_text("⚔️ عصابة / حرب:",reply_markup=KB([
            [InlineKeyboardButton("⚔️ اعمل عصابة",callback_data="make_gang"),InlineKeyboardButton("⚔️ حرب",callback_data="war")],
            [InlineKeyboardButton("🔫 اسرق حد",callback_data="steal"),InlineKeyboardButton("🚔 سلم نفسك",callback_data="surrender")],
            [InlineKeyboardButton("🔙 رجوع",callback_data="back")]]))
    elif d=="make_gang":
        user['gang']="عصابة TRAN"; save(db); await q.edit_message_text("⚔️ عملت عصابة TRAN!",reply_markup=BACK())
    elif d=="war":
        win=random.choice([True,False])
        if win: user['cash']+=5000; user['xp']+=20; save(db); await q.edit_message_text("⚔️ كسبت الحرب! +5000",reply_markup=BACK())
        else: user['cash']-=2000; user['health']-=20; save(db); await q.edit_message_text("⚔️ خسرت الحرب! -2000 وصحة -20",reply_markup=BACK())
    elif d=="steal":
        if random.random()<0.5: user['cash']+=3000; save(db); await q.edit_message_text("🔫 سرقت 3000!",reply_markup=BACK())
        else: user['wanted']+=1; user['jail']=1; save(db); await q.edit_message_text("🚔 اتمسكت! مطلوب +1 واتسجنت",reply_markup=BACK())
    elif d=="surrender":
        user['wanted']=0; user['jail']=0; save(db); await q.edit_message_text("🚔 سلمت نفسك واتصالحت",reply_markup=BACK())
    elif d=="edu_menu":
        await q.edit_message_text("🏫 تعليم / جيش:",reply_markup=KB([
            [InlineKeyboardButton("🎓 ادرس",callback_data="study"),InlineKeyboardButton("🪖 ادخل الجيش",callback_data="army")],
            [InlineKeyboardButton("🕵️ مافيا",callback_data="mafia"),InlineKeyboardButton("🔙 رجوع",callback_data="back")]]))
    elif d=="army":
        user['army']=True; user['xp']+=30; save(db); await q.edit_message_text("🪖 دخلت الجيش! بقيت قوي",reply_markup=BACK())
    elif d=="mafia":
        user['mafia']=True; save(db); await q.edit_message_text("🕵️ دخلت المافيا! خلي بالك",reply_markup=BACK())

    # --- بورصة + مزاد + هدايا + VIP ---
    elif d=="stock":
        change=random.randint(-3000,6000); user['cash']+=change; user['stock']+=change; save(db); await q.edit_message_text(f"📈 بورصة: {change} | كاشك {user['cash']}",reply_markup=BACK())
    elif d=="gift_menu":
        await q.edit_message_text("🎁 هدايا:",reply_markup=KB([
            [InlineKeyboardButton("🎁 خد هدية",callback_data="get_gift"),InlineKeyboardButton("🎟️ كوبون",callback_data="coupon")],
            [InlineKeyboardButton("🔙 رجوع",callback_data="back")]]))
    elif d=="get_gift":
        g=random.randint(500,2000); user['cash']+=g; save(db); await q.edit_message_text(f"🎁 هدية {g}!",reply_markup=BACK())
    elif d=="coupon":
        user['cash']+=1000; save(db); await q.edit_message_text("🎟️ كوبون 1000!",reply_markup=BACK())
    elif d=="vip":
        if user['cash']>=50000: user['cash']-=50000; user['vip']=True; user['titles'].append("VIP 👑"); save(db); await q.edit_message_text("💎 بقيت VIP! مبروك 👑",reply_markup=BACK())
        else: await q.edit_message_text("❌ VIP محتاج 50000",reply_markup=BACK())

    # --- خدمة عملاء ---
    elif d=="support":
        await q.edit_message_text("🛎️ خدمة عملاء TRAN\nالدعم: @cat_max_10 @MOON_104\nالاونر: @TRAN_5",reply_markup=KB([
            [InlineKeyboardButton("🛎️ اطلب دعم",callback_data="ask_support")],
            [InlineKeyboardButton("🔙 رجوع",callback_data="back")]]))
    elif d=="ask_support":
        tid=str(random.randint(1000,9999)); db["tickets"][tid]={"user":uid,"status":"open","support":None}; save(db)
        print(f"تذكرة {tid} من {uid}")
        await q.edit_message_text(f"✅ تذكرتك #{tid} اتبعتت\nاللي يقبل الاول هيكلمك",reply_markup=BACK())
    elif d.startswith("accept_"):
        tid=d.split("_")[1]; t=db["tickets"].get(tid)
        if t and t["status"]=="open": t["status"]="taken"; t["support"]=uid; save(db); await q.edit_message_text(f"✅ قبلت التذكرة #{tid} كلم العميل")
        else: await q.edit_message_text("❌ اتاخدت خلاص")
    else:
        await q.edit_message_text("🚧 جاية قريب",reply_markup=BACK())

def main():
    threading.Thread(target=run_flask,daemon=True).start()
    threading.Thread(target=self_ping,daemon=True).start()
    app=Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start",start))
    app.add_handler(CallbackQueryHandler(buttons))
    print("👑 TRAN BOT FULL شغال ومش هينام")
    app.run_polling()
if __name__=="__main__": main()     
