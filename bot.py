# 👑 WAR BOT - الكود النهائي - الاونر عدي
# OWNER_ID: 8188263997 - كل حاجة مفتوحة ليه
import logging, random, json, os, threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("TOKEN")
OWNER_ID = 8188263997
ADMIN_USERNAME = "@TRAN_5"

logging.basicConfig(level=logging.INFO)

# سيرفر يصحي نفسه
app_flask = Flask(__name__)
@app_flask.route('/')
def home():
    return "WAR BOT صاحي 👑 - الاونر عدي"
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)
threading.Thread(target=run_flask, daemon=True).start()

DATA_FILE = "war_data.json"
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {"users": {}, "codes": {}, "banned": []}
def save_data(d):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
db = load_data()

def get_user(uid, username=""):
    uid = str(uid)
    if uid not in db["users"]:
        db["users"][uid] = {"name": username, "points": 0, "vip": False, "legend": False, "is_owner": (int(uid)==OWNER_ID)}
        save_data(db)
    return db["users"][uid]

def get_rank(points):
    if points >= 300: return "👑 ملك WAR"
    if points >= 150: return "🥇 قائد WAR"
    if points >= 50: return "🥈 فارس WAR"
    return "🥉 مواطن WAR"

SENS = {
    "samsung": {"title": "📱 سامسونج", "items": {
        "A12 / A13 / A14 / A15": "عام: 190\nنقطة حمراء: 185\n2x: 180\n4x: 175\nزر اطلاق: 55\nDPI: 650",
        "A52 / A53 / A54 / S21 / S22": "عام: 200\nنقطة حمراء: 195\n2x: 190\n4x: 185\nزر اطلاق: 50\nDPI: 700",
        "S23 / S24 / S25 Ultra": "عام: 185\nنقطة حمراء: 180\n2x: 175\n4x: 170\nزر اطلاق: 52\nDPI: 600",
        "A05 / A06 / A35 / A55": "عام: 198\nنقطة حمراء: 194\n2x: 190\n4x: 185\nزر اطلاق: 54\nDPI: 690",
        "M33 / M34 / M54": "عام: 192\nنقطة حمراء: 188\n2x: 184\n4x: 180\nزر اطلاق: 57\nDPI: 660",
    }},
    "xiaomi": {"title": "📱 شاومي", "items": {
        "Redmi 10 / 12 / 13": "عام: 195\nنقطة حمراء: 190\n2x: 185\n4x: 180\nزر اطلاق: 58\nDPI: 680",
        "Poco X3 / X5 / X6": "عام: 200\nنقطة حمراء: 200\n2x: 195\n4x: 190\nزر اطلاق: 48\nDPI: 720",
        "Redmi Note 11 / 12 / 13 Pro": "عام: 190\nنقطة حمراء: 188\n2x: 182\n4x: 178\nزر اطلاق: 55\nDPI: 660",
        "Redmi 14C / Note 14": "عام: 196\nنقطة حمراء: 192\n2x: 188\n4x: 184\nزر اطلاق: 56\nDPI: 670",
    }},
    "oppo": {"title": "📱 اوبو", "items": {
        "A53 / A54 / A57 / A78": "عام: 185\nنقطة حمراء: 180\n2x: 175\n4x: 170\nزر اطلاق: 60\nDPI: 620",
        "Reno 7 / 8 / 11": "عام: 195\nنقطة حمراء: 192\n2x: 188\n4x: 182\nزر اطلاق: 52\nDPI: 680",
        "A18 / A38 / A58 / A60": "عام: 190\nنقطة حمراء: 186\n2x: 182\n4x: 178\nزر اطلاق: 59\nDPI: 640",
    }},
    "realme": {"title": "📱 ريلمي", "items": {
        "C51 / C53 / C55 / C67": "عام: 192\nنقطة حمراء: 188\n2x: 184\n4x: 178\nزر اطلاق: 56\nDPI: 640",
        "Realme 11 / 12 Pro": "عام: 198\nنقطة حمراء: 195\n2x: 190\n4x: 185\nزر اطلاق: 50\nDPI: 700",
        "Note 50 / C61 / 13": "عام: 194\nنقطة حمراء: 190\n2x: 186\n4x: 182\nزر اطلاق: 55\nDPI: 650",
    }},
    "infinix": {"title": "📱 انفنكس", "items": {
        "Hot 30 / 40 / 50": "عام: 200\nنقطة حمراء: 195\n2x: 190\n4x: 185\nزر اطلاق: 60\nDPI: 700",
        "Note 30 / 40": "عام: 195\nنقطة حمراء: 192\n2x: 188\n4x: 180\nزر اطلاق: 55\nDPI: 680",
        "Hot 50 Pro / Smart 8 / Zero 30": "عام: 202\nنقطة حمراء: 198\n2x: 194\n4x: 190\nزر اطلاق: 58\nDPI: 710",
    }},
    "iphone": {"title": "📱 ايفون", "items": {
        "iPhone 11 / 12 / 13": "عام: 175\nنقطة حمراء: 170\n2x: 165\n4x: 160\nزر اطلاق: 48\nDPI: الايفون مفيهوش DPI",
        "iPhone 14 / 15 / 16 Pro Max": "عام: 180\nنقطة حمراء: 175\n2x: 170\n4x: 165\nزر اطلاق: 50\nDPI: الايفون مفيهوش DPI",
    }},
    "other": {"title": "📱 هواوي / فيفو / تكنو", "items": {
        "Huawei Nova / Y": "عام: 188\nنقطة حمراء: 184\n2x: 180\n4x: 175\nزر اطلاق: 58\nDPI: 630",
        "Vivo Y / V": "عام: 190\nنقطة حمراء: 186\n2x: 182\n4x: 178\nزر اطلاق: 55\nDPI: 650",
        "Tecno Spark / Camon": "عام: 198\nنقطة حمراء: 194\n2x: 190\n4x: 185\nزر اطلاق: 60\nDPI: 690",
    }},
}
WEAPONS = {
    "MP40 / UMP": "عام: 195\nاحمر: 190\nزر: 55 - للرش",
    "M1887 / M1014 شوتجن": "عام: 185\nاحمر: 180\nزر: 70 - زر كبير للسرعة",
    "AK / SCAR / M4": "عام: 190\nاحمر: 185\nزر: 55",
    "AWM / Kar98 سنايبر": "عام: 160\nاحمر: 155\nزر: 60 - هادية للهيد",
    "Desert Eagle / USP": "عام: 200\nاحمر: 200\nزر: 45",
}

def main_kb(uid):
    kb = [
        [InlineKeyboardButton("🎁 جرب مجاناً", callback_data="free")],
        [InlineKeyboardButton("👑 VIP الملكي - 30ج", callback_data="vip"), InlineKeyboardButton("💎 LEGEND - 120ج", callback_data="legend")],
        [InlineKeyboardButton("🎯 حساسية WAR", callback_data="sens_home"), InlineKeyboardButton("🔫 حساسية الاسلحة", callback_data="weapons")],
        [InlineKeyboardButton("🏠 رومات مخصصة", callback_data="rooms"), InlineKeyboardButton("🏆 بطولات", callback_data="tournaments")],
        [InlineKeyboardButton("🎬 فيديوهات ملكية", callback_data="videos"), InlineKeyboardButton("🧠 نصايح المحترفين", callback_data="tips")],
        [InlineKeyboardButton("👕 سكنات وشخصيات", callback_data="skins"), InlineKeyboardButton("💰 شحن وجواهر", callback_data="charge")],
        [InlineKeyboardButton("🎰 عجلة الحظ", callback_data="wheel"), InlineKeyboardButton("🎁 صندوق الكنز", callback_data="chest")],
        [InlineKeyboardButton("🔍 بدور على سكواد", callback_data="squad"), InlineKeyboardButton("🧪 اختبار حساسيتي", callback_data="test_sens")],
        [InlineKeyboardButton("🏆 ابطال المملكة", callback_data="leaders"), InlineKeyboardButton("📜 دستور WAR", callback_data="rules")],
        [InlineKeyboardButton("🔗 لينك دعوتي", callback_data="invite"), InlineKeyboardButton("📊 احصائياتي", callback_data="mystats")],
        [InlineKeyboardButton("📞 تواصل مع الملك", url=f"https://t.me/{ADMIN_USERNAME.replace('@','')}")],
    ]
    if int(uid) == OWNER_ID:
        kb.insert(0, [InlineKeyboardButton("👑 لوحة الاونر عدي - كل حاجة مفتوحة", callback_data="owner_panel")])
    return InlineKeyboardMarkup(kb)

def owner_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👥 شوف كل الاعضاء", callback_data="owner_users")],
        [InlineKeyboardButton("🎁 اصنع كود VIP", callback_data="owner_make_code")],
        [InlineKeyboardButton("👑 ادي VIP لحد", callback_data="owner_give_vip")],
        [InlineKeyboardButton("🚫 احظر حد", callback_data="owner_ban")],
        [InlineKeyboardButton("📢 ابعت رسالة للكل", callback_data="owner_broadcast")],
        [InlineKeyboardButton("🏆 ابدأ بطولة", callback_data="owner_tournament")],
        [InlineKeyboardButton("📊 احصائيات البوت", callback_data="owner_stats")],
        [InlineKeyboardButton("⬅️ رجوع", callback_data="home")],
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    u = get_user(uid, update.effective_user.username or update.effective_user.first_name)
    if str(uid) in db["banned"]:
        await update.message.reply_text("🚫 انت محظور من مملكة WAR"); return
    if int(uid) == OWNER_ID:
        txt = f"👑 ━━━━━━━━━━━━━━ 👑\nأهلاً بيك يا اونر عدي 👑\nملك مملكة WAR\n👑 ━━━━━━━━━━━━━━ 👑\n\n🟢 البوت شغال وصاحي\n👥 الاعضاء: {len(db['users'])}\n💎 نقاطك: ∞ لا نهائية\n🏆 رتبتك: 👑 اونر WAR\n\nكل حاجة مفتوحة ليك مجاناً"
        await update.message.reply_text(txt, reply_markup=main_kb(uid)); return
    txt = f"👑 ━━━━━━━━━━━━━━ 👑\n     W E L C O M E   T O\n        ⚔️  W A R  ⚔️\n👑 ━━━━━━━━━━━━━━ 👑\n\nأهلاً بيك يا بطل 👑\nانت دخلت القصر الملكي لـ Free Fire مصر\n\n✨ هنا الملك بياخد حقه ✨\n\n🏆 رتبتك: {get_rank(u['points'])}\n💎 نقاطك: {u['points']}"
    await update.message.reply_text(txt, reply_markup=main_kb(uid))

async def on_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    u = get_user(uid, q.from_user.username or "")
    data = q.data
    if data == "home":
        await q.edit_message_text(f"👑 مملكة WAR - أهلاً بيك يا بطل\nرتبتك: {get_rank(u['points'])} | نقاطك: {u['points']}", reply_markup=main_kb(uid)); return
    if data == "owner_panel":
        if int(uid) != OWNER_ID:
            await q.edit_message_text("👑 عذراً، دي للاونر عدي بس!", reply_markup=main_kb(uid)); return
        await q.edit_message_text("👑 لوحة الاونر عدي\nكل حاجة متاحة ليك مجاناً - انت المتحكم في المملكة", reply_markup=owner_kb()); return
    if data.startswith("owner_"):
        if int(uid) != OWNER_ID:
            await q.edit_message_text("ممنوع!", reply_markup=main_kb(uid)); return
        msgs = {
            "owner_users": f"👥 عدد الاعضاء: {len(db['users'])}",
            "owner_make_code": "🎁 ابعت: /makecode WAR123 VIP",
            "owner_give_vip": "👑 ابعت: /givevip @username",
            "owner_ban": "🚫 ابعت: /ban @username",
            "owner_broadcast": "📢 ابعت: /broadcast رسالتك",
            "owner_tournament": "🏆 بطولة الجمعة بدأت! ابعت /broadcast عشان تعلن",
            "owner_stats": f"📊 الاعضاء: {len(db['users'])}\nالمحظورين: {len(db['banned'])}\nالاكواد: {len(db['codes'])}",
        }
        await q.edit_message_text(msgs.get(data, "👑 لوحة الاونر"), reply_markup=owner_kb()); return
    if data == "sens_home":
        kb = [[InlineKeyboardButton(v["title"], callback_data=f"sens_{k}")] for k,v in SENS.items()]
        kb += [[InlineKeyboardButton("👑 حساسية VIP السرية", callback_data="vip_sens")], [InlineKeyboardButton("⬅️ رجوع", callback_data="home")]]
        await q.edit_message_text("🎯 حساسية WAR - اختر نوع تليفونك 👇", reply_markup=InlineKeyboardMarkup(kb)); return
    if data.startswith("sens_"):
        key = data.replace("sens_","")
        if key in SENS:
            kb = [[InlineKeyboardButton(name, callback_data=f"show_{key}_{i}")] for i,name in enumerate(SENS[key]["items"])]
            kb.append([InlineKeyboardButton("⬅️ رجوع", callback_data="sens_home")])
            await q.edit_message_text(f"{SENS[key]['title']} - اختر موديلك:", reply_markup=InlineKeyboardMarkup(kb)); return
    if data.startswith("show_"):
        _, key, idx = data.split("_")
        name = list(SENS[key]["items"].keys())[int(idx)]
        val = SENS[key]["items"][name]
        await q.edit_message_text(f"🎯 حساسية {name}\n\n{val}\n\n👑 WAR - انسخها وجربها", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ رجوع", callback_data=f"sens_{key}")]])); return
    if data == "vip_sens":
        if u["vip"] or u["legend"] or int(uid)==OWNER_ID:
            await q.edit_message_text("👑 حساسية VIP الملكية السرية\n\nعام: 200\nاحمر: 200\n2x: 195\n4x: 190\nزر: 48\nDPI: 720\n\n🔥 اقوى من المجانية بـ 30% - ممنوع التسريب", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ رجوع", callback_data="sens_home")]]))
        else:
            await q.edit_message_text("👑 عذراً، الحساسية دي للملوك فقط", reply_markup=main_kb(uid)); return
    if data == "weapons":
        kb = [[InlineKeyboardButton(k, callback_data=f"wp_{i}")] for i,k in enumerate(WEAPONS)]
        kb.append([InlineKeyboardButton("⬅️ رجوع", callback_data="home")])
        await q.edit_message_text("🔫 حساسية كل سلاح - اختر سلاحك:", reply_markup=InlineKeyboardMarkup(kb)); return
    if data.startswith("wp_"):
        name = list(WEAPONS.keys())[int(data.split("_")[1])]
        await q.edit_message_text(f"🔫 {name}\n\n{WEAPONS[name]}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ رجوع", callback_data="weapons")]])); return
    if data == "wheel":
        prizes = ["10 نقاط 🎉", "5 نقاط", "VIP يوم واحد 👑", "حظ اوفر بكرة 😅", "20 نقطة 🔥", "كود مجاني 🎁"]
        p = random.choice(prizes)
        if "نقاط" in p:
            try: u["points"] += int(p.split()[0]); save_data(db)
            except: pass
        await q.edit_message_text(f"🎰 عجلة الحظ...\n\nكسبت: {p}\nنقاطك دلوقتي: {u['points']}", reply_markup=main_kb(uid)); return
    if data == "chest":
        prizes = ["1 نقطة", "5 نقاط", "كود مجاني", "الصندوق فاضي، جرب بكرة 😅"]
        p = random.choice(prizes)
        await q.edit_message_text(f"🎁 صندوق الكنز فتح...\n\nطلعلك: {p}", reply_markup=main_kb(uid)); return
    if data == "vip":
        await q.edit_message_text(f"👑 VIP الملكي - 30ج\n\nتواصل مع الملك {ADMIN_USERNAME}\nابعت رقم العملية وهيتم تفعيلك في الحال 👑", reply_markup=main_kb(uid)); return
    if data == "legend":
        await q.edit_message_text(f"💎 LEGEND الأسطوري - 120ج\n\nتواصل مع الملك {ADMIN_USERNAME}\nكل حاجة مفتوحة + رومات خاصة + حساسية سرية", reply_markup=main_kb(uid)); return
    if data == "free":
        await q.edit_message_text("🎁 جرب مجاناً\n\nليك كود تجريبي 24 ساعة + حساسية مجانية + عجلة حظ", reply_markup=main_kb(uid)); return
    if data == "rooms":
        await q.edit_message_text("🏠 رومات WAR\n\nروم مجانية: السبت 9م\nروم VIP: 10م - 100 نقطة\nروم LEGEND: 11م - VIP اسبوع", reply_markup=main_kb(uid)); return
    if data == "tournaments":
        await q.edit_message_text("🏆 بطولات WAR\n\nيومية - 50 نقطة\nجمعة - 200 نقطة + لقب\nشهرية - VIP شهر مجاناً", reply_markup=main_kb(uid)); return
    if data == "videos":
        await q.edit_message_text("🎬 فيديوهات ملكية\n\n1- هيد شوت\n2- ظبط الحساسية في دقيقة\n3- 4 اصابع\n4- شرح DPI\n\nالـ VIP يشوفها كلها", reply_markup=main_kb(uid)); return
    if data == "tips":
        tips = ["خليك قريب من العربية للهروب من الزون", "احسن مكان برمودا: بيك", "كيلي + هاياتو + موكو للهيد شوت", "متقفش في مكان مفتوح اكتر من 3 ثواني"]
        await q.edit_message_text(f"🧠 نصيحة اليوم:\n\n{random.choice(tips)}", reply_markup=main_kb(uid)); return
    if data == "skins":
        await q.edit_message_text("👕 سكنات وشخصيات\n\nهيد: كيلي + هاياتو + موكو\nسرعة: كيلي + جوزيف\nرومات: وكونج + كرونو", reply_markup=main_kb(uid)); return
    if data == "charge":
        await q.edit_message_text("💰 شحن وجواهر\n\nاشحن مع عرض ضعف الجواهر\nاكواد مجانية كل اسبوع\n⚠️ احذر النصب - اتعامل مع الملك بس", reply_markup=main_kb(uid)); return
    if data == "squad":
        await q.edit_message_text("🔍 بدور على سكواد\n\nابعت: رانكك + كام اصبع + وقت لعبك", reply_markup=main_kb(uid)); return
    if data == "test_sens":
        await q.edit_message_text("🧪 اختبار حساسيتي\n\nابعت: نوع تليفونك + كام اصبع + جيروسكوب ولا لأ", reply_markup=main_kb(uid)); return
    if data == "leaders":
        sorted_users = sorted(db["users"].values(), key=lambda x: x["points"], reverse=True)[:5]
        txt = "🏆 ابطال المملكة:\n\n"
        for i,uu in enumerate(sorted_users,1):
            txt += f"{i}. {uu.get('name','بطل')} - {uu['points']} نقطة\n"
        await q.edit_message_text(txt, reply_markup=main_kb(uid)); return
    if data == "rules":
        await q.edit_message_text("📜 دستور WAR\n\n1- ممنوع تسريب الاكواد\n2- ممنوع الشتيمة\n3- ممنوع النصب\n4- احترم الملك", reply_markup=main_kb(uid)); return
    if data == "invite":
        await q.edit_message_text(f"🔗 لينك دعوتك:\nhttps://t.me/WAR_BOT?start={uid}\n\nكل صاحب = 10 نقاط\n5 صحاب = VIP يوم مجاناً", reply_markup=main_kb(uid)); return
    if data == "mystats":
        await q.edit_message_text(f"📊 احصائياتك\n\nالاسم: {u.get('name','')}\nالنقاط: {u['points']}\nالرتبة: {get_rank(u['points'])}\nVIP: {'✅' if u['vip'] else '❌'}\nLEGEND: {'✅' if u['legend'] else '❌'}", reply_markup=main_kb(uid)); return

async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = update.message.text.strip()
    uid = update.effective_user.id
    if txt == "انا الاونر" and int(uid)==OWNER_ID:
        await update.message.reply_text("👑 أهلاً بيك يا اونر عدي", reply_markup=owner_kb()); return
    if txt.startswith("/makecode") and int(uid)==OWNER_ID:
        parts = txt.split()
        if len(parts)>=3:
            db["codes"][parts[1]] = parts[2]; save_data(db)
            await update.message.reply_text(f"✅ كود {parts[1]} اتعمل: {parts[2]}"); return
    if txt.startswith("/broadcast") and int(uid)==OWNER_ID:
        msg = txt.replace("/broadcast","").strip()
        count=0
        for uidd in list(db["users"].keys()):
            try:
                await context.bot.send_message(chat_id=int(uidd), text=f"📢 رسالة من الملك عدي 👑\n\n{msg}")
                count+=1
            except: pass
        await update.message.reply_text(f"✅ اتبعت لـ {count} عضو"); return
    if any(w in txt for w in ["سامسونج","شاومي","اوبو","ريلمي","انفنكس","ايفون"]):
        await update.message.reply_text("🤖 مدرب WAR:\nحساسيك المناسبة: عام 195، احمر 190، زر 55\nاتدرب 10 دقايق كل يوم 🔥"); return
    await update.message.reply_text("👑 ابعت /start عشان تشوف المملكة", reply_markup=main_kb(uid))

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(on_cb))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    print("WAR BOT شغال وصاحي 👑")
    app.run_polling()

if __name__ == "__main__":
    main()
