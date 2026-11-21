from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")
def keep_alive():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    Thread(target=server.serve_forever, daemon=True).start()
keep_alive()
# ==========================================
# بوت المهام والمتجر - النسخة النهائية V8 🔥
# الأونر: 8188263997
# كل حاجة: مهام + متجر + بنك + شغل + سرقة + تحويل + دعوة + كوبون + ترتيب + تداول + رافعة + شارت + جماعي + حرب + مزاد + سوق سوداء + حجر ورقة مقص
# التداول: 60% خسارة / 40% مكسب - سري
# ==========================================
import telebot, random, json, os, time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import date

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)
OWNER_ID = 8188263997

# ========== حفظ البيانات ==========
FILE = "بيانات_البوت.json"
def تحميل():
    if os.path.exists(FILE):
        with open(FILE, 'r', encoding='utf-8') as f: return json.load(f)
    return {"فلوس": {}, "بنك": {}, "سلسلة": {}, "اخر_دخول": {}, "اكواد": {}, "محظورين": [], "ادمنز": [], "كوبونات": {}, "اخر_شغل": {}, "حماية": {}, "اسماء": {}}
def حفظ():
    with open(FILE, 'w', encoding='utf-8') as f:
        json.dump({"فلوس": فلوس, "بنك": بنك, "سلسلة": سلسلة, "اخر_دخول": اخر_دخول, "اكواد": اكواد, "محظورين": محظورين, "ادمنز": ادمنز, "كوبونات": كوبونات, "اخر_شغل": اخر_شغل, "حماية": حماية, "اسماء": اسماء}, f, ensure_ascii=False)

d = تحميل()
فلوس = d.get("فلوس", {}); بنك = d.get("بنك", {}); سلسلة = d.get("سلسلة", {}); اخر_دخول = d.get("اخر_دخول", {})
اكواد = d.get("اكواد", {}); محظورين = d.get("محظورين", []); ادمنز = d.get("ادمنز", []); كوبونات = d.get("كوبونات", {})
اخر_شغل = d.get("اخر_شغل", {}); حماية = d.get("حماية", {}); اسماء = d.get("اسماء", {})

# ========== المتجر ==========
المتجر = {
    "1": {"الاسم": "🎨 خلفية موبايل", "السعر": 50, "الوصف": "خلفية جامدة"},
    "2": {"الاسم": "🎵 أغنية MP3", "السعر": 100, "الوصف": "أي أغنية"},
    "3": {"الاسم": "😂 باكدج ميمز 20 ميم", "السعر": 150, "الوصف": "ضحك للصبح"},
    "4": {"الاسم": "🎬 نتفليكس يوم", "السعر": 200, "الوصف": "يوم كامل"},
    "5": {"الاسم": "🎮 ببجي 60 شدة", "السعر": 500, "الوصف": "اشحن وادعيلي"},
    "6": {"الاسم": "🔥 فري فاير 100 جوهرة", "السعر": 500, "الوصف": "جواهر"},
    "7": {"الاسم": "💎 روبلكس 400", "السعر": 800, "الوصف": "روبوكس"},
    "8": {"الاسم": "📱 رقم وهمي", "السعر": 300, "الوصف": "فعل بيه أي حاجة"},
    "9": {"الاسم": "⭐ VIP أسبوع", "السعر": 1000, "الوصف": "فلوسك تتضاعف"},
    "10": {"الاسم": "👑 VIP شهر", "السعر": 3000, "الوصف": "انت الملك"},
    "11": {"الاسم": "🎁 صندوق مفاجآت", "السعر": 250, "الوصف": "ممكن تكسب 5000!"},
    "12": {"الاسم": "🛡️ حماية من السرقة 24س", "السعر": 200, "الوصف": "محدش يسرقك"},
    "13": {"الاسم": "💰 تذكرة بنك ذهبية", "السعر": 1500, "الوصف": "فايدة أعلى"},
    "14": {"الاسم": "🎲 5 لفات عجلة", "السعر": 300, "الوصف": "5 لفات"},
    "15": {"الاسم": "🏆 لقب أسطورة", "السعر": 5000, "الوصف": "لقب دائم"},
}

الشغلانات = [("👨‍🍳 طباخ", 80), ("🚗 سواق", 100), ("💻 مبرمج", 150), ("📸 مصور", 90), ("🎤 مغني", 200), ("⚽ لاعب كورة", 300)]
الاسئلة = [("عاصمة مصر ايه؟", "القاهرة"), ("كام لاعب في فريق الكورة؟", "11"), ("أكبر نادي في مصر؟", "الأهلي"), ("1+1 كام؟", "2"), ("لون السماء ايه؟", "أزرق")]
مهام_عشوائية = [("📸 ابعت صورة لقطتك", 60), ("😂 ابعت نكتة", 40), ("🎤 غني أغنية", 80), ("🏃 اعمل 10 ضغط", 50), ("📚 اقرا صفحة من كتاب", 70), ("💧 اشرب 3 كوبايات مية", 30), ("🎨 ارسم أي حاجة", 90), ("📞 كلم صاحبك وقوله بحبك", 100)]

def مهمة_النهاردة():
    return مهام_عشوائية[date.today().day % len(مهام_عشوائية)]

# ========== التداول ==========
عملات_التداول = {
    "BTC": {"الاسم": "₿ بيتكوين", "السعر": 65000},
    "GOLD": {"الاسم": "🥇 ذهب", "السعر": 2600},
    "USD": {"الاسم": "💵 دولار", "السعر": 48},
    "ETH": {"الاسم": "Ξ ايثيريوم", "السعر": 3200},
    "PUBG": {"الاسم": "🎮 ببجي كوين", "السعر": 15},
}
اسعار_حية = {k: v["السعر"] for k, v in عملات_التداول.items()}
تاريخ_اسعار = {k: [v["السعر"]] for k, v in عملات_التداول.items()}
def حدث_السعر(عملة):
    تغير = random.uniform(-0.05, 0.05)
    اسعار_حية[عملة] = max(1, int(اسعار_حية[عملة] * (1 + تغير)))
    تاريخ_اسعار[عملة].append(اسعار_حية[عملة])
    if len(تاريخ_اسعار[عملة]) > 10: تاريخ_اسعار[عملة] = تاريخ_اسعار[عملة][-10:]
    return اسعار_حية[عملة]
def ارسم_شارت(عملة):
    اسعار = تاريخ_اسعار[عملة]
    if len(اسعار) < 2: return "📊 ─────"
    شارت = ""
    اقل = min(اسعار); اعلى = max(اسعار)
    if اعلى == اقل: return "📊 ──────────"
    for سعر in اسعار:
        مستوى = int((سعر - اقل) / (اعلى - اقل) * 8) if اعلى != اقل else 4
        سطر = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█", "🚀"]
        شارت += سطر[مستوى]
    سهم = "📈 طالع 🔥" if اسعار[-1] > اسعار[-2] else "📉 نازل 😢" if اسعار[-1] < اسعار[-2] else "➡️ ثابت"
    return f"📊 {شارت}\n{سهم} السعر: {اسعار[-1]}"

جولة_جماعية = {"شغالة": False, "عملة": "BTC", "مشاركين": {}, "وقت_البداية": 0}
مزاد_حالي = {"شغال": False, "الحاجة": "", "اعلى_سعر": 0, "الفايز": None}
سوق_سوداء = {"1": {"الاسم": "💎 نتفليكس شهر كامل", "السعر": 800}, "2": {"الاسم": "🔥 ببجي 1500 شدة", "السعر": 3000}, "3": {"الاسم": "👑 تاج الملك", "السعر": 10000}}

# ========== دوال مساعدة ==========
def هات_فلوس(uid):
    uid=str(uid)
    if uid not in فلوس: فلوس[uid]=100
    return فلوس[uid]
def هات_بنك(uid):
    uid=str(uid)
    if uid not in بنك: بنك[uid]=0
    return بنك[uid]
def هات_مستوى(uid):
    ف=هات_فلوس(uid)+هات_بنك(uid)
    if ف<200: return "🥉 مبتدئ"
    elif ف<1000: return "🥈 محترف"
    elif f<5000: return "🥇 أسطورة"
    elif f<20000: return "💎 ماسي"
    else: return "👑 ملك البوت"
def هو_اونر(uid): return int(uid)==OWNER_ID
def هو_ادمن(uid): return int(uid)==OWNER_ID or str(uid) in ادمنز
def اسم_الشخص(uid): return اسماء.get(str(uid), f"ID {uid}")

# ========== القوايم ==========
def قايمة_رئيسية(uid):
    m=InlineKeyboardMarkup(row_width=2)
    m.add(
        InlineKeyboardButton("📋 المهام", callback_data="مهام"),
        InlineKeyboardButton("🎯 مهمة اليوم", callback_data="مهمة_اليوم"),
        InlineKeyboardButton("🛒 المتجر", callback_data="متجر"),
        InlineKeyboardButton("🎡 عجلة الحظ", callback_data="عجلة"),
        InlineKeyboardButton("🎁 هدية يومية", callback_data="هدية"),
        InlineKeyboardButton("🏦 البنك", callback_data="بنك"),
        InlineKeyboardButton("💼 شغل", callback_data="شغل"),
        InlineKeyboardButton("🥷 سرقة", callback_data="سرقة"),
        InlineKeyboardButton("💸 تحويل", callback_data="تحويل"),
        InlineKeyboardButton("📈 تداول", callback_data="تداول"),
        InlineKeyboardButton("👥 تداول جماعي", callback_data="تداول_جماعي"),
        InlineKeyboardButton("📊 الشارت", callback_data="شارت"),
        InlineKeyboardButton("✂️ حجر ورقة مقص", callback_data="حجر"),
        InlineKeyboardButton("⚔️ حرب 1 ضد 1", callback_data="حرب"),
        InlineKeyboardButton("🏪 مزاد", callback_data="مزاد"),
        InlineKeyboardButton("💎 سوق سوداء", callback_data="سوق_سوداء"),
        InlineKeyboardButton("🏅 بطولة الأسبوع", callback_data="بطولة"),
        InlineKeyboardButton("🏆 الترتيب", callback_data="ترتيب"),
        InlineKeyboardButton("💰 فلوسي", callback_data="فلوسي"),
        InlineKeyboardButton("🎟️ كوبون", callback_data="كوبون"),
        InlineKeyboardButton("🔗 دعوة", callback_data="دعوة"),
    )
    if هو_اونر(uid):
        m.add(InlineKeyboardButton("👑 لوحة الأونر", callback_data="اونر"))
    elif هو_ادمن(uid):
        m.add(InlineKeyboardButton("🛡️ لوحة الأدمن", callback_data="ادمن"))
    m.add(InlineKeyboardButton("🔄 تحديث", callback_data="تحديث"))
    return m

def قايمة_اونر():
    m=InlineKeyboardMarkup(row_width=2)
    m.add(
        InlineKeyboardButton("💸 زود فلوس", callback_data="اونر_اختر_زود"),
        InlineKeyboardButton("💀 صفر فلوس", callback_data="اونر_اختر_صفر"),
        InlineKeyboardButton("🚫 حظر", callback_data="اونر_اختر_حظر"),
        InlineKeyboardButton("✅ فك حظر", callback_data="اونر_اختر_فك"),
        InlineKeyboardButton("📢 اذاعة", callback_data="اونر_اذاعة_اختر"),
        InlineKeyboardButton("📊 احصائيات", callback_data="اونر_احصائيات"),
        InlineKeyboardButton("🎁 هدية للكل", callback_data="اونر_هدية_كل"),
        InlineKeyboardButton("👥 اضافة أدمن", callback_data="اونر_اختر_ادمن"),
        InlineKeyboardButton("❌ حذف أدمن", callback_data="اونر_اختر_حذف_ادمن"),
        InlineKeyboardButton("🎟️ اعمل كوبون", callback_data="اونر_كوبون"),
        InlineKeyboardButton("➕ اضافة للمتجر", callback_data="اونر_اضافة"),
        InlineKeyboardButton("💰 فلوس الكل", callback_data="اونر_فلوس_الكل"),
    )
    m.add(InlineKeyboardButton("⬅️ رجوع", callback_data="تحديث"))
    return m

def قايمة_ادمن():
    m=InlineKeyboardMarkup(row_width=2)
    m.add(
        InlineKeyboardButton("💸 زود فلوس", callback_data="اونر_اختر_زود"),
        InlineKeyboardButton("🚫 حظر", callback_data="اونر_اختر_حظر"),
        InlineKeyboardButton("✅ فك حظر", callback_data="اونر_اختر_فك"),
        InlineKeyboardButton("📊 احصائيات", callback_data="اونر_احصائيات"),
    )
    m.add(InlineKeyboardButton("⬅️ رجوع", callback_data="تحديث"))
    return m

def زرار_رجوع():
    m=InlineKeyboardMarkup()
    m.add(InlineKeyboardButton("⬅️ رجوع للقايمة", callback_data="تحديث"))
    return m

def ليستة_ناس(فعل):
    m=InlineKeyboardMarkup(row_width=1)
    if فعل=="فك": اخر_ناس = محظورين[-15:]
    elif فعل=="حذف_ادمن": اخر_ناس = ادمنز
    else: اخر_ناس = list(فلوس.keys())[-15:]
    if not اخر_ناس: m.add(InlineKeyboardButton("مفيش حد", callback_data="تحديث"))
    for u in اخر_ناس:
        m.add(InlineKeyboardButton(f"{اسم_الشخص(u)} - {فلوس.get(u,0)} جنيه", callback_data=f"{فعل}_شخص_{u}"))
    m.add(InlineKeyboardButton("⬅️ رجوع", callback_data="اونر"))
    return m

# ========== START ==========
@bot.message_handler(commands=['start'])
def البداية(message):
    uid=str(message.from_user.id)
    اسماء[uid]=message.from_user.first_name
    if uid in محظورين:
        bot.send_message(message.chat.id, "🚫 انت محظور من البوت"); return
    هات_فلوس(uid)
    if uid not in اكواد: اكواد[uid]=f"INV{uid[-4:]}"
    parts=message.text.split()
    if len(parts)>1:
        كود=parts[1]
        for صاحب, كوده in اكواد.items():
            if كوده==كود and صاحب!=uid:
                فلوس[صاحب]=هات_فلوس(صاحب)+100
                try: bot.send_message(int(صاحب), f"🎉 حد دخل بكودك! +100 جنيه")
                except: pass
    حفظ()
    bot.send_message(message.chat.id,
        f"أهلاً يا بطل {message.from_user.first_name} 🔥\n\n💰 محفظتك: {هات_فلوس(uid)} جنيه\n🏦 بنكك: {هات_بنك(uid)} جنيه\n🎖️ مستواك: {هات_مستوى(uid)}\n🔥 أيام متتالية: {سلسلة.get(uid,0)}\n🔗 كودك: {اكواد[uid]}\n\nاختار من الزراير تحت 👇",
        reply_markup=قايمة_رئيسية(uid))

# ========== كل الزراير ==========
@bot.callback_query_handler(func=lambda call: True)
def الزراير(call):
    uid=str(call.from_user.id); chat_id=call.message.chat.id; data=call.data
    if uid in محظورين:
        bot.answer_callback_query(call.id, "انت محظور 🚫"); return

    if data=="تحديث":
        bot.edit_message_text(f"القايمة الرئيسية 🔥\n\n💰 محفظتك: {هات_فلوس(uid)}\n🏦 بنكك: {هات_بنك(uid)}\n🎖️ مستواك: {هات_مستوى(uid)}\n🔥 أيام: {سلسلة.get(uid,0)}", chat_id, call.message.message_id, reply_markup=قايمة_رئيسية(uid))

    elif data=="مهام":
        m=InlineKeyboardMarkup(row_width=1)
        m.add(InlineKeyboardButton("✅ خلصت مهمة +30", callback_data="خلص_مهمة"))
        m.add(InlineKeyboardButton("❓ جاوب سؤال +40", callback_data="سؤال"))
        m.add(InlineKeyboardButton("👥 دعوة صاحب +100", callback_data="دعوة"))
        m.add(InlineKeyboardButton("⬅️ رجوع", callback_data="تحديث"))
        bot.edit_message_text("📋 المهام اليومية:\n\n📅 دخول يومي: +30\n❓ سؤال صح: +40\n👥 دعوة صاحب: +100\n💼 شغل: +80 لـ 300\n\n📅 مهام أسبوعية:\n🏆 اكسب 500 في الأسبوع: +300\n👑 ادعي 5 صحاب: +500\n🔥 ادخل 7 أيام: +1000\n\nدوس واكسب 👇", chat_id, call.message.message_id, reply_markup=m)
    elif data=="خلص_مهمة":
        مك=random.choice([15,20,30,40,50,100]); فلوس[uid]=هات_فلوس(uid)+مك; حفظ()
        bot.answer_callback_query(call.id, f"+{مك} جنيه 🔥")
        bot.edit_message_text(f"عاااش 🔥 +{مك} جنيه\n💰 معاك: {فلوس[uid]}", chat_id, call.message.message_id, reply_markup=زرار_رجوع())
    elif data=="سؤال":
        س=random.choice(الاسئلة)
        m=InlineKeyboardMarkup()
        اج=[س[1],"اسكندرية","الزمالك","10","أزرق","القاهرة"]; اج=list(set(اج)); random.shuffle(اج)
        if س[1] not in اج: اج[0]=س[1]
        for ج in اج[:4]: m.add(InlineKeyboardButton(ج, callback_data=f"جواب_{ج}_{س[1]}"))
        bot.edit_message_text(f"❓ {س[0]}", chat_id, call.message.message_id, reply_markup=m)
    elif data.startswith("جواب_"):
        _, جوابك, الصح = data.split("_",2)
        if جوابك==الصح:
            فلوس[uid]=هات_فلوس(uid)+40; حفظ()
            bot.edit_message_text(f"صححح 🔥 +40 جنيه\n💰 معاك: {فلوس[uid]}", chat_id, call.message.message_id, reply_markup=زرار_رجوع())
        else: bot.edit_message_text(f"غلط 😢 الصح: {الصح}", chat_id, call.message.message_id, reply_markup=زرار_رجوع())

    elif data=="مهمة_اليوم":
        اسم_المهمة, جايزة = مهمة_النهاردة()
        m=InlineKeyboardMarkup()
        m.add(InlineKeyboardButton("✅ خلصتها", callback_data="خلص_مهمة_اليوم"))
        m.add(InlineKeyboardButton("⬅️ رجوع", callback_data="تحديث"))
        bot.edit_message_text(f"🎯 مهمة النهاردة:\n\n{اسم_المهمة}\n\nالجايزة: +{جايزة} جنيه\n\nخلصها ودوس خلصتها 👇", chat_id, call.message.message_id, reply_markup=m)
    elif data=="خلص_مهمة_اليوم":
        اسم_المهمة, جايزة = مهمة_النهاردة()
        فلوس[uid]=هات_فلوس(uid)+جايزة; حفظ()
        bot.edit_message_text(f"عاااش 🔥 خلصت: {اسم_المهمة}\n+{جايزة} جنيه\n💰 معاك: {فلوس[uid]}", chat_id, call.message.message_id, reply_markup=زرار_رجوع())

    elif data=="هدية":
        اليوم=str(date.today())
        if اخر_دخول.get(uid)==اليوم:
            bot.answer_callback_query(call.id, "خدتها النهاردة 😅"); return
        سلسلة[uid]=سلسلة.get(uid,0)+1; اخر_دخول[uid]=اليوم
        مك=30+(سلسلة[uid]*10)
        if سلسلة[uid]>=7: مك+=1000; bot.send_message(chat_id, "🔥🔥 7 أيام ورا بعض! +1000 بونص!")
        فلوس[uid]=هات_فلوس(uid)+مك; حفظ()
        bot.edit_message_text(f"🎁 هدية يوم {سلسلة[uid]}: +{مك} جنيه\n💰 معاك: {فلوس[uid]}", chat_id, call.message.message_id, reply_markup=زرار_رجوع())

    elif data=="عجلة":
        مك=random.choice([0,10,20,50,100,200,500,1000]); فلوس[uid]=هات_فلوس(uid)+مك; حفظ()
        m=InlineKeyboardMarkup(); m.add(InlineKeyboardButton("🎡 لف تاني", callback_data="عجلة")); m.add(InlineKeyboardButton("⬅️ رجوع", callback_data="تحديث"))
        bot.edit_message_text(f"🎡 كسبت +{مك} جنيه 🔥\n💰 معاك: {فلوس[uid]}" if مك else "😢 صفر... لف تاني!", chat_id, call.message.message_id, reply_markup=m)

    elif data=="بنك":
        m=InlineKeyboardMarkup(row_width=2)
        m.add(InlineKeyboardButton("➕ ايداع 100", callback_data="ايداع_100"), InlineKeyboardButton("➖ سحب 100", callback_data="سحب_100"))
        m.add(InlineKeyboardButton("➕ ايداع 500", callback_data="ايداع_500"), InlineKeyboardButton("➖ سحب 500", callback_data="سحب_500"))
        m.add(InlineKeyboardButton("➕ ايداع 1000", callback_data="ايداع_1000"), InlineKeyboardButton("➖ سحب 1000", callback_data="سحب_1000"))
        m.add(InlineKeyboardButton("⬅️ رجوع", callback_data="تحديث"))
        bot.edit_message_text(f"🏦 البنك:\n\n💰 محفظة: {هات_فلوس(uid)}\n🏦 بنك: {هات_بنك(uid)}\nالفايدة 10% كل يوم", chat_id, call.message.message_id, reply_markup=m)
    elif data.startswith("ايداع_"):
        مبلغ=int(data.split("_")[1])
        if هات_فلوس(uid)>=مبلغ:
            فلوس[uid]-=مبلغ; بنك[uid]=هات_بنك(uid)+مبلغ; حفظ(); bot.answer_callback_query(call.id, f"اودعت {مبلغ} ✅")
        else: bot.answer_callback_query(call.id, "فلوسك مش كفاية 😢")
        bot.edit_message_text(f"🏦 بنكك: {هات_بنك(uid)}\n💰 محفظتك: {هات_فلوس(uid)}", chat_id, call.message.message_id, reply_markup=زرار_رجوع())
    elif data.startswith("سحب_"):
        مبلغ=int(data.split("_")[1])
        if هات_بنك(uid)>=مبلغ:
            بنك[uid]-=مبلغ; فلوس[uid]=هات_فلوس(uid)+مبلغ; حفظ(); bot.answer_callback_query(call.id, f"سحبت {مبلغ} ✅")
        else: bot.answer_callback_query(call.id, "مفيش كفاية")
        bot.edit_message_text(f"🏦 بنكك: {هات_بنك(uid)}\n💰 محفظتك: {هات_فلوس(uid)}", chat_id, call.message.message_id, reply_markup=زرار_رجوع())

    elif data=="شغل":
        m=InlineKeyboardMarkup(row_width=1)
        for اسم, مرتب in الشغلانات: m.add(InlineKeyboardButton(f"{اسم} - {مرتب} جنيه", callback_data=f"اشتغل_{مرتب}"))
        m.add(InlineKeyboardButton("⬅️ رجوع", callback_data="تحديث"))
        bot.edit_message_text("💼 اختار شغلانة واشتغل:\nتقدر تشتغل كل 60 ثانية", chat_id, call.message.message_id, reply_markup=m)
    elif data.startswith("اشتغل_"):
        مرتب=int(data.split("_")[1]); الان=time.time()
        if الان - اخر_شغل.get(uid,0) < 60:
            bot.answer_callback_query(call.id, f"استنى {int(60-(الان-اخر_شغل[uid]))} ثانية 😅"); return
        اخر_شغل[uid]=الان; فلوس[uid]=هات_فلوس(uid)+مرتب; حفظ()
        bot.edit_message_text(f"💼 اشتغلت وخدت +{مرتب} جنيه 🔥\n💰 معاك: {فلوس[uid]}", chat_id, call.message.message_id, reply_markup=زرار_رجوع())

    elif data=="سرقة":
        m=InlineKeyboardMarkup(row_width=1)
        ضحايا=[u for u in فلوس.keys() if u!=uid][:10]
        if not ضحايا:
            bot.edit_message_text("مفيش حد تسرقه لسه 😅", chat_id, call.message.message_id, reply_markup=زرار_رجوع()); return
        for ض in ضحايا: m.add(InlineKeyboardButton(f"🥷 اسرق {اسم_الشخص(ض)} - معاه {فلوس[ض]} جنيه", callback_data=f"اسرق_{ض}"))
        m.add(InlineKeyboardButton("⬅️ رجوع", callback_data="تحديث"))
        bot.edit_message_text("🥷 اختار حد تسرقه... لو اتقفشت هتدفع غرامة 😂", chat_id, call.message.message_id, reply_markup=m)
    elif data.startswith("اسرق_"):
        ضحية=data.split("_")[1]
        if حماية.get(ضحية,0) > time.time():
            bot.edit_message_text("🛡️ ده عنده حماية! مش هتعرف تسرقه", chat_id, call.message.message_id, reply_markup=زرار_رجوع()); return
        if هات_فلوس(ضحية)<50:
            bot.edit_message_text("ده غلبان معهوش فلوس 😂", chat_id, call.message.message_id, reply_markup=زرار_رجوع()); return
        if random.choice([True,False,False]):
            مسروق=random.randint(20,100); فلوس[uid]=هات_فلوس(uid)+مسروق; فلوس[ضحية]=هات_فلوس(ضحية)-مسروق; حفظ()
            bot.edit_message_text(f"🥷 سرقت {مسروق} جنيه من {اسم_الشخص(ضحية)}! محدش شافك 😂", chat_id, call.message.message_id, reply_markup=زرار_رجوع())
        else:
            فلوس[uid]=max(0,hات_فلوس(uid)-50); حفظ()
            bot.edit_message_text("🚨 اتقفشت! دفعت غرامة 50 جنيه 😂😂", chat_id, call.message.message_id, reply_markup=زرار_رجوع())

    elif data=="تحويل":
        m=InlineKeyboardMarkup(row_width=1)
        for u in list(فلوس.keys())[:10]:
            if u!=uid: m.add(InlineKeyboardButton(f"حول لـ {اسم_الشخص(u)} - {فلوس[u]} جنيه", callback_data=f"تحويل_لـ_{u}"))
        m.add(InlineKeyboardButton("⬅️ رجوع", callback_data="تحديث"))
        bot.edit_message_text("💸 اختار حد تحول ليه:", chat_id, call.message.message_id, reply_markup=m)
    elif data.startswith("تحويل_لـ_"):
        مستلم=data.split("_")[-1]
        m=InlineKeyboardMarkup(row_width=3)
        for مبلغ in [10,50,100,500,1000]: m.add(InlineKeyboardButton(f"{مبلغ}", callback_data=f"حول_مبلغ_{مبلغ}_{مستلم}"))
        m.add(InlineKeyboardButton("⬅️ رجوع", callback_data="تحديث"))
        bot.edit_message_text(f"حول كام لـ {اسم_الشخص(مستلم)}؟", chat_id, call.message.message_id, reply_markup=m)
    elif data.startswith("حول_مبلغ_"):
        _,_,مبلغ,مستلم = data.split("_"); مبلغ=int(مبلغ)
        if هات_فلوس(uid)>=مبلغ:
            فلوس[uid]-=مبلغ; فلوس[مستلم]=هات_فلوس(مستلم)+مبلغ; حفظ()
            bot.edit_message_text(f"حولت {مبلغ} لـ {اسم_الشخص(مستلم)} ✅", chat_id, call.message.message_id, reply_markup=زرار_رجوع())
            try: bot.send_message(int(مستلم), f"💸 {اسم_الشخص(uid)} حولك {مبلغ} جنيه 🔥")
            except: pass
        else: bot.answer_callback_query(call.id, "فلوسك مش كفاية")

    elif data=="متجر":
        m=InlineKeyboardMarkup(row_width=1)
        for رقم, ح in المتجر.items(): m.add(InlineKeyboardButton(f"{ح['الاسم']} - {ح['السعر']} جنيه", callback_data=f"اشتري_{رقم}"))
        m.add(InlineKeyboardButton("⬅️ رجوع", callback_data="تحديث"))
        bot.edit_message_text(f"🛒 المتجر - معاك {هات_فلوس(uid)} جنيه\nدوس على اللي عايز تشتريه 👇", chat_id, call.message.message_id, reply_markup=m)
    elif data.startswith("اشتري_"):
        رقم=data.split("_")[1]; ح=المتجر[رقم]
        if هات_فلوس(uid)>=ح['السعر']:
            فلوس[uid]-=ح['السعر']
            if رقم=="11":
                جايزة=random.choice([50,100,250,1000,5000]); فلوس[uid]+=جايزة; حفظ()
                bot.edit_message_text(f"🎁 الصندوق طلعلك {جايزة} جنيه!", chat_id, call.message.message_id, reply_markup=زرار_رجوع())
            elif رقم=="12":
                حماية[uid]=time.time()+86400; حفظ()
                bot.edit_message_text("🛡️ اشتريت حماية 24 ساعة! محدش يقدر يسرقك", chat_id, call.message.message_id, reply_markup=زرار_رجوع())
            else:
                حفظ(); bot.edit_message_text(f"مبروك 🎉 اشتريت {ح['الاسم']}\n📝 {ح['الوصف']}\n💰 فاضل: {فلوس[uid]}\nابعتلي سكرين عشان ابعتلك الحاجة", chat_id, call.message.message_id, reply_markup=زرار_رجوع())
        else: bot.answer_callback_query(call.id, "فلوسك مش كفاية 😢 روح خلص مهام")

    elif data=="ترتيب":
        مرتب=sorted(فلوس.items(), key=lambda x: x[1], reverse=True)[:10]
        نص="🏆 أغنى 10 في البوت:\n\n"
        for i,(u,ف) in enumerate(مرتب,1): نص+=f"{i}. {اسم_الشخص(u)} - {ف} جنيه - {هات_مستوى(u)}\n"
        bot.edit_message_text(نص, chat_id, call.message.message_id, reply_markup=زرار_رجوع())
    elif data=="فلوسي":
        bot.edit_message_text(f"💰 محفظة: {هات_فلوس(uid)}\n🏦 بنك: {هات_بنك(uid)}\n🎖️ مستوى: {هات_مستوى(uid)}\n🔥 أيام متتالية: {سلسلة.get(uid,0)}\n🔗 كودك: {اكواد.get(uid,'')}", chat_id, call.message.message_id, reply_markup=زرار_رجوع())
    elif data=="دعوة":
        كود=اكواد.get(uid, f"INV{uid[-4:]}")
        bot.edit_message_text(f"🔗 كودك: {كود}\n\nابعت لصاحبك اللينك ده:\nhttps://t.me/اسم_بوتك?start={كود}\n\nكل واحد يدخل بكودك تاخد 100 جنيه 🔥", chat_id, call.message.message_id, reply_markup=زرار_رجوع())
    elif data=="كوبون":
        m=InlineKeyboardMarkup(row_width=1); m.add(InlineKeyboardButton("🎟️ استخدم كوبون", callback_data="استخدم_كوبون")); m.add(InlineKeyboardButton("⬅️ رجوع", callback_data="تحديث"))
        bot.edit_message_text("🎟️ عندك كوبون؟ دوس استخدم", chat_id, call.message.message_id, reply_markup=m)
    elif data=="استخدم_كوبون":
        bot.send_message(chat_id, "ابعت الكوبون كده: /كوبون الكود\nمثال: /كوبون HELLO100")

    # ===== حجر ورقة مقص =====
    elif data=="حجر":
        m=InlineKeyboardMarkup(row_width=3)
        m.add(InlineKeyboardButton("🪨 حجر", callback_data="لعب_حجر"), InlineKeyboardButton("📄 ورقة", callback_data="لعب_ورقة"), InlineKeyboardButton("✂️ مقص", callback_data="لعب_مقص"))
        m.add(InlineKeyboardButton("⬅️ رجوع", callback_data="تحديث"))
        bot.edit_message_text("✂️ اختار: حجر ولا ورقة ولا مقص؟\nلو كسبت تاخد 50 جنيه!", chat_id, call.message.message_id, reply_markup=m)
    elif data.startswith("لعب_"):
        اختيارك=data.replace("لعب_",""); اختيار_البوت=random.choice(["حجر","ورقة","مقص"])
        ايموجي={"حجر":"🪨","ورقة":"📄","مقص":"✂️"}
        if اختيارك==اختيار_البوت: نتيجة="تعادل 🤝"
        elif (اختيارك=="حجر" and اختيار_البوت=="مقص") or (اختيارك=="ورقة" and اختيار_البوت=="حجر") or (اختيارك=="مقص" and اختيار_البوت=="ورقة"):
            نتيجة="كسبت 🔥 +50 جنيه"; فلوس[uid]=هات_فلوس(uid)+50; حفظ()
        else:
            نتيجة="خسرت 😢 -20 جنيه"; فلوس[uid]=max(0,hات_فلوس(uid)-20); حفظ()
        bot.edit_message_text(f"انت: {ايموجي[اختيارك]} {اختيارك}\nالبوت: {ايموجي[اختيار_البوت]} {اختيار_البوت}\n\n{نتيجة}\n💰 معاك: {فلوس[uid]}", chat_id, call.message.message_id, reply_markup=زرار_رجوع())

    # ===== حرب =====
    elif data=="حرب":
        m=InlineKeyboardMarkup(row_width=1)
        for u in list(فلوس.keys())[:10]:
            if u!=uid: m.add(InlineKeyboardButton(f"⚔️ اتحدى {اسم_الشخص(u)} - {فلوس[u]} جنيه", callback_data=f"تحدي_{u}"))
        m.add(InlineKeyboardButton("⬅️ رجوع", callback_data="تحديث"))
        bot.edit_message_text("⚔️ اختار حد تتحداه:\nاللي يكسب ياخد 100 جنيه من التاني!", chat_id, call.message.message_id, reply_markup=m)
    elif data.startswith("تحدي_"):
        خصم=data.split("_")[1]; نتيجتك=random.randint(1,100); نتيجة_خصم=random.randint(1,100)
        if نتيجتك>نتيجة_خصم:
            مسروق=min(100,hات_فلوس(خصم)); فلوس[uid]=هات_فلوس(uid)+مسروق; فلوس[خصم]=هات_فلوس(خصم)-مسروق; حفظ()
            bot.edit_message_text(f"⚔️ كسبت الحرب! 🔥\nانت: {نتيجتك} VS {اسم_الشخص(خصم)}: {نتيجة_خصم}\nخدت {مسروق} جنيه منه!\n💰 معاك: {فلوس[uid]}", chat_id, call.message.message_id, reply_markup=زرار_رجوع())
            try: bot.send_message(int(خصم), f"⚔️ {اسم_الشخص(uid)} كسبك في الحرب وخد منك {مسروق} جنيه 😢")
            except: pass
        else:
            مسروق=min(100,hات_فلوس(uid)); فلوس[uid]=هات_فلوس(uid)-مسروق; فلوس[خصم]=هات_فلوس(خصم)+مسروق; حفظ()
            bot.edit_message_text(f"⚔️ خسرت الحرب 😢\nانت: {نتيجتك} VS {اسم_الشخص(خصم)}: {نتيجة_خصم}\nخسرت {مسروق} جنيه", chat_id, call.message.message_id, reply_markup=زرار_رجوع())

    # ===== مزاد =====
    elif data=="مزاد":
        if not مزاد_حالي["شغال"]:
            حاجة=random.choice(["🎬 نتفليكس شهر", "🎮 ببجي 500 شدة", "👑 لقب ملك", "💎 روبلكس 1000"])
            مزاد_حالي["شغال"]=True; مزاد_حالي["الحاجة"]=حاجة; مزاد_حالي["اعلى_سعر"]=100; مزاد_حالي["الفايز"]=None
        m=InlineKeyboardMarkup(row_width=2)
        m.add(InlineKeyboardButton(f"💸 زود 50 - {مزاد_حالي['اعلى_سعر']+50}", callback_data="مزاد_زود_50"), InlineKeyboardButton(f"💸 زود 100 - {مزاد_حالي['اعلى_سعر']+100}", callback_data="مزاد_زود_100"))
        m.add(InlineKeyboardButton("⬅️ رجوع", callback_data="تحديث"))
        bot.edit_message_text(f"🏪 المزاد:\n\nالحاجة: {مزاد_حالي['الحاجة']}\nأعلى سعر: {مزاد_حالي['اعلى_سعر']} جنيه\nالفايز الحالي: {اسم_الشخص(مزاد_حالي['الفايز']) if مزاد_حالي['الفايز'] else 'محدش'}\n\nدوس عشان تزود!", chat_id, call.message.message_id, reply_markup=m)
    elif data.startswith("مزاد_زود_"):
        زيادة=int(data.split("_")[-1]); سعر_جديد=مزاد_حالي["اعلى_سعر"]+زيادة
        if هات_فلوس(uid)<سعر_جديد:
            bot.answer_callback_query(call.id, "فلوسك مش كفاية 😢"); return
        مزاد_حالي["اعلى_سعر"]=سعر_جديد; مزاد_حالي["الفايز"]=uid
        bot.answer_callback_query(call.id, f"انت الأعلى دلوقتي بـ {سعر_جديد} 🔥")
        bot.edit_message_text(f"🏪 المزاد:\n\nالحاجة: {مزاد_حالي['الحاجة']}\nأعلى سعر: {سعر_جديد} جنيه\nالفايز: {اسم_الشخص(uid)}", chat_id, call.message.message_id, reply_markup=زرار_رجوع())

    # ===== سوق سوداء =====
    elif data=="سوق_سوداء":
        m=InlineKeyboardMarkup(row_width=1)
        for رقم, ح in سوق_سوداء.items(): m.add(InlineKeyboardButton(f"{ح['الاسم']} - {ح['السعر']} جنيه 🔥 نادر!", callback_data=f"سوداء_{رقم}"))
        m.add(InlineKeyboardButton("⬅️ رجوع", callback_data="تحديث"))
        bot.edit_message_text("💎 السوق السوداء - حاجات نادرة جداً!\nبتختفي بعد شوية، الحق اشتري!", chat_id, call.message.message_id, reply_markup=m)
    elif data.startswith("سوداء_"):
        رقم=data.split("_")[1]; ح=سوق_سوداء[رقم]
        if هات_فلوس(uid)>=ح['السعر']:
            فلوس[uid]-=ح['السعر']; حفظ()
            bot.edit_message_text(f"مبروك 🔥 اشتريت حاجة نادرة:\n{ح['الاسم']}", chat_id, call.message.message_id, reply_markup=زرار_رجوع())
        else: bot.answer_callback_query(call.id, "فلوسك مش كفاية")

    # ===== بطولة =====
    elif data=="بطولة":
        مرتب=sorted(فلوس.items(), key=lambda x: x[1], reverse=True)[:3]
        نص="🏅 بطولة الأسبوع:\n\n"; جوايز=[5000,3000,1000]
        for i,(u,ف) in enumerate(مرتب,1): نص+=f"{i}. {اسم_الشخص(u)} - {ف} جنيه - الجايزة: {جوايز[i-1]} جنيه\n"
        نص+="\nأول 3 في الترتيب هياخدوا الجوايز دي آخر الأسبوع!"
        bot.edit_message_text(نص, chat_id, call.message.message_id, reply_markup=زرار_رجوع())

    # ===== التداول =====
    elif data=="تداول":
        for ع in عملات_التداول: حدث_السعر(ع)
        m=InlineKeyboardMarkup(row_width=2)
        for كود, بيانات in عملات_التداول.items():
            سعر=اسعار_حية[كود]
            سهم="📈" if len(تاريخ_اسعار[كود])>=2 and تاريخ_اسعار[كود][-1]>تاريخ_اسعار[كود][-2] else "📉" if len(تاريخ_اسعار[كود])>=2 and تاريخ_اسعار[كود][-1]<تاريخ_اسعار[كود][-2] else "➡️"
            m.add(InlineKeyboardButton(f"{بيانات['الاسم']} {سهم} {سعر}", callback_data=f"تداول_عملة_{كود}"))
        m.add(InlineKeyboardButton("👥 تداول جماعي", callback_data="تداول_جماعي")); m.add(InlineKeyboardButton("📊 الشارت", callback_data="شارت")); m.add(InlineKeyboardButton("⬅️ رجوع", callback_data="تحديث"))
        bot.edit_message_text(f"📈 التداول 🔥\n\n💰 معاك: {هات_فلوس(uid)} جنيه\n\nالأسعار بتتغير كل شوية!\nاختار عملة 👇", chat_id, call.message.message_id, reply_markup=m)
    elif data=="شارت":
        m=InlineKeyboardMarkup(row_width=2)
        for كود, بيانات in عملات_التداول.items(): m.add(InlineKeyboardButton(f"{بيانات['الاسم']}", callback_data=f"شارت_{كود}"))
        m.add(InlineKeyboardButton("⬅️ رجوع", callback_data="تداول"))
        bot.edit_message_text("📊 اختار عملة تشوف الشارت بتاعها:", chat_id, call.message.message_id, reply_markup=m)
    elif data.startswith("شارت_"):
        عملة=data.split("_")[1]; حدث_السعر(عملة); اسم_العملة=عملات_التداول[عملة]["الاسم"]; شارت=ارسم_شارت(عملة); سعر=اسعار_حية[عملة]; اسعار=تاريخ_اسعار[عملة]; تغير=((اسعار[-1]-اسعار[0])/اسعار[0]*100) if اسعار[0]!=0 else 0
        m=InlineKeyboardMarkup(row_width=2)
        m.add(InlineKeyboardButton("🔄 تحديث الشارت", callback_data=f"شارت_{عملة}"), InlineKeyboardButton("📈 تداول في دي", callback_data=f"تداول_عملة_{عملة}"))
        m.add(InlineKeyboardButton("⬅️ رجوع", callback_data="تداول"))
        bot.edit_message_text(f"📊 شارت {اسم_العملة}\n\n{شارت}\n\n💰 السعر الحالي: {سعر}\n📊 التغير: {تغير:+.1f}%\n📈 أعلى سعر: {max(اسعار)}\n📉 أقل سعر: {min(اسعار)}\n\nتوقع هتطلع ولا هتنزل؟", chat_id, call.message.message_id, reply_markup=m)
    elif data.startswith("تداول_عملة_"):
        عملة=data.split("_")[-1]; اسم_العملة=عملات_التداول[عملة]["الاسم"]; حدث_السعر(عملة); شارت=ارسم_شارت(عملة)
        m=InlineKeyboardMarkup(row_width=3)
        m.add(InlineKeyboardButton("10", callback_data=f"تداول_مبلغ_10_{عملة}"), InlineKeyboardButton("50", callback_data=f"تداول_مبلغ_50_{عملة}"), InlineKeyboardButton("100", callback_data=f"تداول_مبلغ_100_{عملة}"), InlineKeyboardButton("500", callback_data=f"تداول_مبلغ_500_{عملة}"), InlineKeyboardButton("1000", callback_data=f"تداول_مبلغ_1000_{عملة}"), InlineKeyboardButton("5000", callback_data=f"تداول_مبلغ_5000_{عملة}"))
        m.add(InlineKeyboardButton("💰 كل فلوسي", callback_data=f"تداول_مبلغ_ALL_{عملة}")); m.add(InlineKeyboardButton("⬅️ رجوع", callback_data="تداول"))
        bot.edit_message_text(f"📈 {اسم_العملة}\n\n{شارت}\n\n💰 معاك: {هات_فلوس(uid)} جنيه\nالسعر: {اسعار_حية[عملة]}\n\nاختار المبلغ 👇", chat_id, call.message.message_id, reply_markup=m)
    elif data.startswith("تداول_مبلغ_"):
        _,_,مبلغ_نص,عملة=data.split("_")
        مبلغ=hات_فلوس(uid) if مبلغ_نص=="ALL" else int(مبلغ_نص)
        if مبلغ<=0 or هات_فلوس(uid)<مبلغ:
            bot.answer_callback_query(call.id, "فلوسك مش كفاية 😢"); return
        اسم_العملة=عملات_التداول[عملة]["الاسم"]
        m=InlineKeyboardMarkup(row_width=2)
        m.add(InlineKeyboardButton("📈 صعود", callback_data=f"تداول_اتجاه_صعود_{مبلغ}_{عملة}_1"), InlineKeyboardButton("📉 هبوط", callback_data=f"تداول_اتجاه_هبوط_{مبلغ}_{عملة}_1"))
        m.add(InlineKeyboardButton("⬅️ رجوع", callback_data="تداول"))
        bot.edit_message_text(f"📈 {اسم_العملة} - المبلغ: {مبلغ} جنيه\n\nتتوقع السعر هيطلع ولا هينزل؟", chat_id, call.message.message_id, reply_markup=m)
    elif data.startswith("تداول_اتجاه_"):
        _,_,اتجاه,مبلغ,عملة,_=data.split("_"); مبلغ=int(مبلغ); اسم_العملة=عملات_التداول[عملة]["الاسم"]
        m=InlineKeyboardMarkup(row_width=4)
        m.add(InlineKeyboardButton("x1 عادي", callback_data=f"نفذ_تداول_{اتجاه}_{مبلغ}_{عملة}_1"), InlineKeyboardButton("x2", callback_data=f"نفذ_تداول_{اتجاه}_{مبلغ}_{عملة}_2"), InlineKeyboardButton("x5 🔥", callback_data=f"نفذ_تداول_{اتجاه}_{مبلغ}_{عملة}_5"), InlineKeyboardButton("x10 😈", callback_data=f"نفذ_تداول_{اتجاه}_{مبلغ}_{عملة}_10"))
        m.add(InlineKeyboardButton("⬅️ رجوع", callback_data="تداول"))
        bot.edit_message_text(f"⚡ اختار الرافعة المالية\n\nالعملة: {اسم_العملة}\nاتجاهك: {'صعود 📈' if اتجاه=='صعود' else 'هبوط 📉'}\nالمبلغ: {مبلغ} جنيه\n\nx1 = عادية\nx2 = ضعف المكسب / ضعف الخسارة\nx5 = 5 أضعاف 🔥\nx10 = 10 أضعاف 😈 ممكن تكسب كتير أو تخسر كل حاجة!\n\nاختار 👇", chat_id, call.message.message_id, reply_markup=m)
    elif data.startswith("نفذ_تداول_"):
        _,_,اتجاه,مبلغ,عملة,رافعة=data.split("_"); مبلغ=int(مبلغ); رافعة=int(رافعة); اسم_العملة=عملات_التداول[عملة]["الاسم"]; سعر_قديم=اسعار_حية[عملة]; حدث_السعر(عملة); سعر_جديد=اسعار_حية[عملة]
        رقم_سري=random.randint(0,99); كسب=رقم_سري<40
        if كسب:
            if اتجاه=="صعود": سعر_جديد=sعر_قديم+random.randint(100,5000)
            else: سعر_جديد=max(1,sعر_قديم-random.randint(100,5000))
            نسبة_مكسب=random.choice([20,30,50,80,100]); مكسب=int(مبلغ*نسبة_مكسب/100*رافعة); فلوس[uid]=هات_فلوس(uid)+مكسب; حفظ(); شارت=ارسم_شارت(عملة)
            m=InlineKeyboardMarkup(); m.add(InlineKeyboardButton("📈 تداول تاني", callback_data="تداول")); m.add(InlineKeyboardButton("📊 شوف الشارت", callback_data=f"شارت_{عملة}")); m.add(InlineKeyboardButton("⬅️ رجوع", callback_data="تحديث"))
            bot.edit_message_text(f"🎉 كسبت! 🔥🔥🔥\n\nالعملة: {اسم_العملة}\nتوقعك: {'صعود 📈' if اتجاه=='صعود' else 'هبوط 📉'} ✅ صح\nالرافعة: x{رافعة}\nالسعر: {سعر_قديم} -> {سعر_جديد}\n{شارت}\n\nمكسبك: +{مكسب} جنيه (+{نسبة_مكسب}% x{رافعة})\n💰 بقى معاك: {فلوس[uid]} جنيه", chat_id, call.message.message_id, reply_markup=m)
        else:
            if اتجاه=="صعود": سعر_جديد=max(1,sعر_قديم-random.randint(100,5000))
            else: سعر_جديد=sعر_قديم+random.randint(100,5000)
            نسبة_خسارة=random.choice([20,30,50,80,100]); خسارة=int(مبلغ*نسبة_خسارة/100*رافعة); خسارة=min(خسارة,hات_فلوس(uid)); فلوس[uid]=max(0,hات_فلوس(uid)-خسارة); حفظ(); شارت=ارسم_شارت(عملة)
            رسالة_اضافية="\n\n😈 الرافعة x10 خطر! خسرت كتير عشان الرافعة عالية" if رافعة>=10 else "\n\n⚠️ الرافعة x5 خلت خسارتك 5 أضعاف" if رافعة>=5 else ""
            m=InlineKeyboardMarkup(); m.add(InlineKeyboardButton("📈 عوض خسارتك - تداول تاني", callback_data="تداول")); m.add(InlineKeyboardButton("⬅️ رجوع", callback_data="تحديث"))
            bot.edit_message_text(f"😢 خسرت...\n\nالعملة: {اسم_العملة}\nتوقعك: {'صعود 📈' if اتجاه=='صعود' else 'هبوط 📉'} ❌ غلط\nالرافعة: x{رافعة}\nالسعر: {سعر_قديم} -> {سعر_جديد}\n{شارت}\n\nخسارتك: -{خسارة} جنيه (-{نسبة_خسارة}% x{رافعة})\n💰 فاضل معاك: {فلوس[uid]} جنيه{رسالة_اضافية}\n\nجرب تاني، المرة الجاية تكسب 🔥", chat_id, call.message.message_id, reply_markup=m)

    # ===== تداول جماعي =====
    elif data=="تداول_جماعي":
        if جولة_جماعية["شغالة"]:
            عملة=جولة_جماعية["عملة"]; اسم_العملة=عملات_التداول[عملة]["الاسم"]; عدد=len(جولة_جماعية["مشاركين"])
            m=InlineKeyboardMarkup(row_width=2)
            m.add(InlineKeyboardButton("📈 صعود 100", callback_data="جماعي_دخول_صعود_100"), InlineKeyboardButton("📉 هبوط 100", callback_data="جماعي_دخول_هبوط_100"), InlineKeyboardButton("📈 صعود 500", callback_data="جماعي_دخول_صعود_500"), InlineKeyboardButton("📉 هبوط 500", callback_data="جماعي_دخول_هبوط_500"))
            m.add(InlineKeyboardButton("🏁 انهي الجولة (أونر)", callback_data="جماعي_انهي")); m.add(InlineKeyboardButton("⬅️ رجوع", callback_data="تداول"))
            bot.edit_message_text(f"👥 تداول جماعي شغال! 🔥\n\nالعملة: {اسم_العملة}\nعدد المشاركين: {عدد}\nالسعر الحالي: {اسعار_حية[عملة]}\n\nاختار اتجاهك وادخل الجولة 👇\nلما الأونر ينهي الجولة، اللي توقع صح هيكسب!", chat_id, call.message.message_id, reply_markup=m)
        else:
            m=InlineKeyboardMarkup(row_width=2)
            for كود, بيانات in عملات_التداول.items(): m.add(InlineKeyboardButton(f"{بيانات['الاسم']}", callback_data=f"جماعي_ابدأ_{كود}"))
            m.add(InlineKeyboardButton("⬅️ رجوع", callback_data="تداول"))
            bot.edit_message_text("👥 تداول جماعي\n\nاختار عملة وابدأ جولة جديدة!\nالكل هيدخل يتوقع صعود ولا هبوط\nواللي يكسب ياخد فلوس اللي خسر 🔥", chat_id, call.message.message_id, reply_markup=m)
    elif data.startswith("جماعي_ابدأ_"):
        عملة=data.split("_")[-1]; جولة_جماعية["شغالة"]=True; جولة_جماعية["عملة"]=عملة; جولة_جماعية["مشاركين"]={}; جولة_جماعية["وقت_البداية"]=time.time(); اسم_العملة=عملات_التداول[عملة]["الاسم"]
        m=InlineKeyboardMarkup(row_width=2); m.add(InlineKeyboardButton("📈 صعود 100", callback_data="جماعي_دخول_صعود_100"), InlineKeyboardButton("📉 هبوط 100", callback_data="جماعي_دخول_هبوط_100")); m.add(InlineKeyboardButton("🏁 انهي الجولة", callback_data="جماعي_انهي"))
        bot.edit_message_text(f"👥 بدأت جولة جماعية!\n\nالعملة: {اسم_العملة}\nالسعر: {اسعار_حية[عملة]}\n\nادخل بسرعة قبل ما الجولة تخلص!", chat_id, call.message.message_id, reply_markup=m)
    elif data.startswith("جماعي_دخول_"):
        _,_,اتجاه,مبلغ=data.split("_"); مبلغ=int(مبلغ)
        if uid in جولة_جماعية["مشاركين"]:
            bot.answer_callback_query(call.id, "دخلت الجولة دي خلاص 😅"); return
        if هات_فلوس(uid)<مبلغ:
            bot.answer_callback_query(call.id, "فلوسك مش كفاية 😢"); return
        جولة_جماعية["مشاركين"][uid]={"اتجاه": اتجاه, "مبلغ": مبلغ}
        bot.answer_callback_query(call.id, f"دخلت الجولة {اتجاه} بـ {مبلغ} 🔥")
        bot.edit_message_text(f"✅ دخلت الجولة!\n\nتوقعك: {'صعود 📈' if اتجاه=='صعود' else 'هبوط 📉'}\nالمبلغ: {مبلغ} جنيه\nعدد المشاركين: {len(جولة_جماعية['مشاركين'])}\n\nاستنى الأونر ينهي الجولة...", chat_id, call.message.message_id, reply_markup=زرار_رجوع())
    elif data=="جماعي_انهي":
        if not هو_اونر(uid) and not هو_ادمن(uid):
            bot.answer_callback_query(call.id, "الأونر بس اللي ينهي الجولة"); return
        if not جولة_جماعية["شغالة"] or not جولة_جماعية["مشاركين"]:
            bot.answer_callback_query(call.id, "مفيش جولة شغالة"); return
        عملة=جولة_جماعية["عملة"]; سعر_قديم=اسعار_حية[عملة]; حدث_السعر(عملة); سعر_جديد=اسعار_حية[عملة]
        رقم_سري=random.randint(0,99)
        if رقم_سري<40: الاتجاه_الصح="صعود"; سعر_جديد=sعر_قديم+random.randint(100,3000)
        else: الاتجاه_الصح="هبوط"; سعر_جديد=max(1,sعر_قديم-random.randint(100,3000))
        كسبانين=[]; خسرانين=[]; مجموع_الخسارة=0
        for مشارك, بيانات in جولة_جماعية["مشاركين"].items():
            if بيانات["اتجاه"]==الاتجاه_الصح: كسبانين.append(مشارك)
            else: خسرانين.append(مشارك); مجموع_الخسارة+=بيانات["مبلغ"]; فلوس[مشارك]=max(0,hات_فلوس(مشارك)-بيانات["مبلغ"])
        if كسبانين and مجموع_الخسارة>0:
            نصيب_الواحد=مجموع_الخسارة//len(كسبانين)
            for ك in كسبانين: فلوس[ك]=هات_فلوس(ك)+نصيب_الواحد+جولة_جماعية["مشاركين"][ك]["مبلغ"]//2
        حفظ()
        for مشارك in جولة_جماعية["مشاركين"]:
            try:
                if مشارك in كسبانين: bot.send_message(int(مشارك), f"🎉 كسبت في التداول الجماعي!\nالسعر طلع {الاتجاه_الصح} وانت توقعت صح 🔥\n💰 معاك: {فلوس[مشارك]}")
                else: bot.send_message(int(مشارك), f"😢 خسرت في التداول الجماعي\nالسعر طلع {الاتجاه_الصح} وانت توقعت غلط\n💰 معاك: {فلوس[مشارك]}")
            except: pass
        اسم_العملة=عملات_التداول[عملة]["الاسم"]
        bot.edit_message_text(f"🏁 انتهت الجولة الجماعية!\n\nالعملة: {اسم_العملة}\nالسعر: {سعر_قديم} -> {سعر_جديد}\nالاتجاه الصح: {الاتجاه_الصح} {'📈' if الاتجاه_الصح=='صعود' else '📉'}\n\n✅ كسبانين: {len(كسبانين)} واحد\n❌ خسرانين: {len(خسرانين)} واحد\n💰 مجموع اللي اتوزع: {مجموع_الخسارة} جنيه", chat_id, call.message.message_id, reply_markup=زرار_رجوع())
        جولة_جماعية["شغالة"]=False; جولة_جماعية["مشاركين"]={}

    # ===== الأونر والأدمن =====
    elif data=="اونر":
        if not هو_اونر(uid): bot.answer_callback_query(call.id, "مش الأونر 😂"); return
        bot.edit_message_text("👑 لوحة الأونر - أهلاً يا بوس 🔥\nاختار اللي عايز تعمله:", chat_id, call.message.message_id, reply_markup=قايمة_اونر())
    elif data=="ادمن":
        if not هو_ادمن(uid): bot.answer_callback_query(call.id, "مش أدمن"); return
        bot.edit_message_text("🛡️ لوحة الأدمن", chat_id, call.message.message_id, reply_markup=قايمة_ادمن())
    elif data=="اونر_احصائيات":
        if not هو_ادمن(uid): return
        bot.edit_message_text(f"📊 احصائيات البوت:\n\n👥 عدد الناس: {len(فلوس)}\n💰 كل الفلوس: {sum(فلوس.values())} جنيه\n🏦 كل البنك: {sum(بنك.values())} جنيه\n🚫 محظورين: {len(محظورين)}\n🛡️ أدمنز: {len(ادمنز)}\n🎟️ كوبونات: {len(كوبونات)}", chat_id, call.message.message_id, reply_markup=قايمة_اونر() if هو_اونر(uid) else قايمة_ادمن())
    elif data=="اونر_هدية_كل":
        if not هو_اونر(uid): return
        for u in فلوس: فلوس[u]=هات_فلوس(u)+100
        حفظ(); bot.answer_callback_query(call.id, "وزعت 100 على الكل 🎁")
        bot.edit_message_text("تم توزيع 100 جنيه على كل الناس 🎁", chat_id, call.message.message_id, reply_markup=قايمة_اونر())
    elif data=="اونر_فلوس_الكل":
        if not هو_اونر(uid): return
        مرتب=sorted(فلوس.items(), key=lambda x: x[1], reverse=True)[:15]
        نص="💰 فلوس الكل:\n\n"
        for u,ف in مرتب: نص+=f"{اسم_الشخص(u)} ({u}) : {ف}\n"
        bot.edit_message_text(نص, chat_id, call.message.message_id, reply_markup=قايمة_اونر())
    elif data.startswith("اونر_اختر_"):
        فعل=data.replace("اونر_اختر_","")
        عناوين={"زود":"اختار حد تزودله 💸","صفر":"اختار حد تصفره 💀","حظر":"اختار حد تحظره 🚫","فك":"اختار حد تفك حظره ✅","ادمن":"اختار حد تخليه أدمن 🛡️","حذف_ادمن":"اختار أدمن تحذفه ❌"}
        bot.edit_message_text(عناوين.get(فعل,"اختار:"), chat_id, call.message.message_id, reply_markup=ليستة_ناس(فعل))
    elif data.startswith("زود_شخص_"):
        if not هو_ادمن(uid): return
        مستلم=data.split("_")[-1]
        m=InlineKeyboardMarkup(row_width=3)
        for مبلغ in [100,500,1000,5000,10000,50000]: m.add(InlineKeyboardButton(f"+{مبلغ}", callback_data=f"زود_مبلغ_{مبلغ}_{مستلم}"))
        m.add(InlineKeyboardButton("⬅️ رجوع", callback_data="اونر"))
        bot.edit_message_text(f"تزود كام لـ {اسم_الشخص(مستلم)}؟", chat_id, call.message.message_id, reply_markup=m)
    elif data.startswith("زود_مبلغ_"):
        _,_,مبلغ,مستلم=data.split("_")
        فلوس[مستلم]=هات_فلوس(مستلم)+int(مبلغ); حفظ()
        bot.edit_message_text(f"زودت {مبلغ} لـ {اسم_الشخص(مستلم)} ✅", chat_id, call.message.message_id, reply_markup=قايمة_اونر())
        try: bot.send_message(int(مستلم), f"🎁 الأونر / الأدمن زودلك {مبلغ} جنيه 🔥")
        except: pass
    elif data.startswith("صفر_شخص_"):
        if not هو_ادمن(uid): return
        مستلم=data.split("_")[-1]; فلوس[مستلم]=0; حفظ()
        bot.edit_message_text(f"صفرت {اسم_الشخص(مستلم)} 💀", chat_id, call.message.message_id, reply_markup=قايمة_اونر())
    elif data.startswith("حظر_شخص_"):
        if not هو_ادمن(uid): return
        مستلم=data.split("_")[-1]
        if مستلم not in محظورين: محظورين.append(مستلم)
        حفظ(); bot.edit_message_text(f"حظرت {اسم_الشخص(مستلم)} 🚫", chat_id, call.message.message_id, reply_markup=قايمة_اونر())
    elif data.startswith("فك_شخص_"):
        if not هو_ادمن(uid): return
        مستلم=data.split("_")[-1]
        if مستلم in محظورين: محظورين.remove(مستلم)
        حفظ(); bot.edit_message_text(f"فكيت {اسم_الشخص(مستلم)} ✅", chat_id, call.message.message_id, reply_markup=قايمة_اونر())
    elif data.startswith("ادمن_شخص_"):
        if not هو_اونر(uid): return
        مستلم=data.split("_")[-1]
        if مستلم not in ادمنز: ادمنز.append(مستلم)
        حفظ(); bot.edit_message_text(f"بقى أدمن {اسم_الشخص(مستلم)} 🛡️", chat_id, call.message.message_id, reply_markup=قايمة_اونر())
    elif data.startswith("حذف_ادمن_شخص_"):
        if not هو_اونر(uid): return
        مستلم=data.split("_")[-1]
        if مستلم in ادمنز: ادمنز.remove(مستلم)
        حفظ(); bot.edit_message_text(f"شلت الأدمن من {اسم_الشخص(مستلم)}", chat_id, call.message.message_id, reply_markup=قايمة_اونر())
    elif data=="اونر_اذاعة_اختر":
        if not هو_اونر(uid): return
        m=InlineKeyboardMarkup(row_width=1)
        m.add(InlineKeyboardButton("📢 مسابقة جديدة!", callback_data="اذاعة_جاهزة_1")); m.add(InlineKeyboardButton("🎁 هدية للكل!", callback_data="اذاعة_جاهزة_2")); m.add(InlineKeyboardButton("🔥 تحديث جديد!", callback_data="اذاعة_جاهزة_3")); m.add(InlineKeyboardButton("💰 فلوس مجانية!", callback_data="اذاعة_جاهزة_4")); m.add(InlineKeyboardButton("⬅️ رجوع", callback_data="اونر"))
        bot.edit_message_text("اختار رسالة جاهزة:", chat_id, call.message.message_id, reply_markup=m)
    elif data.startswith("اذاعة_جاهزة_"):
        رسائل={"1":"📢 يا جماعة فيه مسابقة جديدة! ادخلوا البوت واكسبوا 🔥","2":"🎁 هدية للكل! ادخلوا خدوا هديتكم 🎁","3":"🔥 تحديث جديد في البوت! ادخلوا شوفوه","4":"💰 فلوس مجانية! ادخل البوت وخد هديتك دلوقتي"}
        نص=رسائل[data.split("_")[-1]]; عدد=0
        for u in فلوس:
            try: bot.send_message(int(u), نص); عدد+=1
            except: pass
        bot.edit_message_text(f"بعت لـ {عدد} واحد ✅", chat_id, call.message.message_id, reply_markup=قايمة_اونر())
    elif data=="اونر_كوبون":
        if not هو_اونر(uid): return
        m=InlineKeyboardMarkup(row_width=2)
        m.add(InlineKeyboardButton("كوبون 100", callback_data="اعمل_كوبون_100"), InlineKeyboardButton("كوبون 500", callback_data="اعمل_كوبون_500")); m.add(InlineKeyboardButton("كوبون 1000", callback_data="اعمل_كوبون_1000"), InlineKeyboardButton("كوبون 5000", callback_data="اعمل_كوبون_5000"))
        m.add(InlineKeyboardButton("⬅️ رجوع", callback_data="اونر"))
        bot.edit_message_text("اختار قيمة الكوبون:", chat_id, call.message.message_id, reply_markup=m)
    elif data.startswith("اعمل_كوبون_"):
        قيمة=int(data.split("_")[-1]); كود=f"COUPON{random.randint(1000,9999)}"; كوبونات[كود]=قيمة; حفظ()
        bot.edit_message_text(f"عملت كوبون 🎟️\nالكود: {كود}\nالقيمة: {قيمة} جنيه\nابعت الكود للناس", chat_id, call.message.message_id, reply_markup=قايمة_اونر())
    elif data=="اونر_اضافة":
        if not هو_اونر(uid): return
        bot.send_message(chat_id, "اكتب: /اضافة اسم_الحاجة السعر\nمثال: /اضافة شاهد 300")

# ========== أوامر كتابة ==========
@bot.message_handler(commands=['كوبون'])
def كوبون(message):
    uid=str(message.from_user.id)
    try:
        كود=message.text.split()[1]
        if كود in كوبونات:
            قيمة=كوبونات.pop(كود); فلوس[uid]=هات_فلوس(uid)+قيمة; حفظ()
            bot.send_message(message.chat.id, f"مبروك 🎟️ الكوبون طلعلك +{قيمة} جنيه!")
        else: bot.send_message(message.chat.id, "الكوبون غلط أو استخدم قبل كده 😢")
    except: bot.send_message(message.chat.id, "اكتب: /كوبون الكود")

@bot.message_handler(commands=['اضافة'])
def اضافة(message):
    if message.from_user.id!=OWNER_ID: return
    try:
        p=message.text.split(); المتجر[str(len(المتجر)+1)]={"الاسم":p[1],"السعر":int(p[2]), "الوصف":"جديد"}
        bot.send_message(message.chat.id, f"ضفت {p[1]} ✅")
    except: bot.send_message(message.chat.id, "اكتب: /اضافة اسم سعر")

@bot.message_handler(commands=['زود','صفر','حظر','فك','اذاعة','احصائيات'])
def اوامر_قديمة(message):
    if message.from_user.id!=OWNER_ID:
        bot.send_message(message.chat.id, "انت مش الأونر 😂"); return
    bot.send_message(message.chat.id, "استخدم لوحة الأونر بالزراير أحسن 👑 دوس /start")

print("البوت V8 النهائي شغال 🔥🔥🔥")
bot.polling()
