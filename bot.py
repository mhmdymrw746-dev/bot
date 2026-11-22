import os, json, random, time, threading
from datetime import datetime
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

# ===== سيرفر عشان البوت مينامش =====
app_web = Flask(__name__)
@app_web.route('/')
def home():
    return "Bot WAR by Ady is Alive 👑"
def run_web():
    app_web.run(host="0.0.0.0", port=10000)
threading.Thread(target=run_web, daemon=True).start()

TOKEN = os.environ.get("TOKEN") or "PUT_YOUR_TOKEN_HERE"
OWNER_ID = 8188263997
# الاونر: عدي
ADMIN_ID = 8188263997
VODAFONE_NUMBER = "01118093542"

DB_FILE = "db.json"
def load_db():
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f: return json.load(f)
    except: return {"users": {}, "codes": {}, "pending": {}, "rooms": []}
def save_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f: json.dump(db, f, ensure_ascii=False, indent=2)
def get_user(db, uid, name=""):
    uid = str(uid)
    if uid not in db["users"]:
        db["users"][uid] = {"name": name, "points": 20, "vip": False, "banned": False, "invited": 0, "state": None, "last_daily": "", "wins": 0, "games": 0, "last_wheel": 0, "last_box": 0}
    return db["users"][uid]

# ================= الحساسيات - كل التليفونات =================
SENS = {
    "samsung": {"title": "📱 سامسونج", "items": {
        "A12 / A13 / A14 / A15": "🎯 حساسية A12 / A13 / A14 / A15\n\nعام: 190\nنقطة حمراء: 185\n2x: 180\n4x: 175\nقناص: 120\nزر اطلاق: 55\nDPI: 650\nجيروسكوب: 180",
        "A16 / A17 / A25 / A26": "🎯 حساسية A16 / A17 / A25 / A26\n\nعام: 195\nنقطة حمراء: 190\n2x: 185\n4x: 180\nقناص: 125\nزر اطلاق: 53\nDPI: 680\nجيروسكوب: 185",
        "A34 / A35 / A54 / A55": "🎯 حساسية A34 / A35 / A54 / A55\n\nعام: 200\nنقطة حمراء: 195\n2x: 190\n4x: 185\nقناص: 130\nزر اطلاق: 50\nDPI: 700\nجيروسكوب: 190",
        "A05 / A06 / A32 / A33": "🎯 حساسية A05 / A06 / A32\n\nعام: 198\nنقطة حمراء: 194\n2x: 190\n4x: 185\nقناص: 128\nزر اطلاق: 54\nDPI: 690\nجيروسكوب: 188",
        "S21 / S22 / S23 / S24": "🎯 حساسية S21 / S22 / S23 / S24\n\nعام: 185\nنقطة حمراء: 180\n2x: 175\n4x: 170\nقناص: 110\nزر اطلاق: 52\nDPI: 600\nجيروسكوب: 170",
        "S23 / S24 / S25 Ultra": "🎯 حساسية Ultra 👑\n\nعام: 180\nنقطة حمراء: 175\n2x: 170\n4x: 165\nقناص: 105\nزر اطلاق: 48\nDPI: 580\nجيروسكوب: 165",
        "M33 / M34 / M54 / M55": "🎯 حساسية M33 / M34 / M54\n\nعام: 192\nنقطة حمراء: 188\n2x: 184\n4x: 180\nقناص: 122\nزر اطلاق: 57\nDPI: 660\nجيروسكوب: 182",
        "Z Flip / Z Fold 5 / 6": "🎯 حساسية Z Flip / Fold\n\nعام: 175\nنقطة حمراء: 170\n2x: 165\n4x: 160\nقناص: 110\nزر اطلاق: 48\nDPI: 580\nجيروسكوب: 165",
        "F15 / F34 / F54 / F55": "🎯 حساسية F15 / F34 / F54\n\nعام: 194\nنقطة حمراء: 190\n2x: 186\n4x: 182\nقناص: 124\nزر اطلاق: 56\nDPI: 670\nجيروسكوب: 186",
    }},
    "xiaomi": {"title": "📱 شاومي / بوكو", "items": {
        "Redmi 10 / 12 / 13 / 14C": "🎯 حساسية Redmi 10 / 12 / 13\n\nعام: 195\nنقطة حمراء: 190\n2x: 185\n4x: 180\nقناص: 125\nزر اطلاق: 58\nDPI: 680\nجيروسكوب: 188",
        "Redmi Note 11 / 12 / 13 / 14": "🎯 حساسية Note 11 / 12 / 13 / 14\n\nعام: 190\nنقطة حمراء: 188\n2x: 182\n4x: 178\nقناص: 120\nزر اطلاق: 55\nDPI: 660\nجيروسكوب: 180",
        "Redmi Note Pro 11 / 12 / 13": "🎯 حساسية Note Pro\n\nعام: 198\nنقطة حمراء: 195\n2x: 190\n4x: 185\nقناص: 130\nزر اطلاق: 50\nDPI: 700\nجيروسكوب: 192",
        "Poco X3 / X5 / X6 / X7": "🎯 حساسية Poco X 🔥\n\nعام: 200\nنقطة حمراء: 200\n2x: 195\n4x: 190\nقناص: 135\nزر اطلاق: 48\nDPI: 720\nجيروسكوب: 195",
        "Poco F5 / F6 / M5 / M6": "🎯 حساسية Poco F / M\n\nعام: 196\nنقطة حمراء: 192\n2x: 188\n4x: 184\nقناص: 128\nزر اطلاق: 52\nDPI: 690\nجيروسكوب: 186",
        "Mi 11 / 12 / 13 / 14": "🎯 حساسية Mi\n\nعام: 185\nنقطة حمراء: 180\n2x: 175\n4x: 170\nقناص: 112\nزر اطلاق: 50\nDPI: 620\nجيروسكوب: 175",
        "Redmi 13C / 14C / A3": "🎯 حساسية Redmi 13C / 14C\n\nعام: 200\nنقطة حمراء: 196\n2x: 192\n4x: 188\nقناص: 132\nزر اطلاق: 60\nDPI: 700\nجيروسكوب: 194",
    }},
    "oppo": {"title": "📱 اوبو / ريلمي", "items": {
        "Oppo A53 / A54 / A57 / A78": "🎯 حساسية Oppo A\n\nعام: 185\nنقطة حمراء: 180\n2x: 175\n4x: 170\nقناص: 115\nزر اطلاق: 60\nDPI: 620\nجيروسكوب: 175",
        "Oppo A18 / A38 / A58 / A60": "🎯 حساسية Oppo A18 / A58\n\nعام: 190\nنقطة حمراء: 186\n2x: 182\n4x: 178\nقناص: 118\nزر اطلاق: 59\nDPI: 640\nجيروسكوب: 182",
        "Oppo Reno 7 / 8 / 11 / 12": "🎯 حساسية Oppo Reno\n\nعام: 195\nنقطة حمراء: 192\n2x: 188\n4x: 182\nقناص: 126\nزر اطلاق: 52\nDPI: 680\nجيروسكوب: 188",
        "Realme C51 / C53 / C55 / C67": "🎯 حساسية Realme C\n\nعام: 192\nنقطة حمراء: 188\n2x: 184\n4x: 178\nقناص: 122\nزر اطلاق: 56\nDPI: 640\nجيروسكوب: 184",
        "Realme C61 / C63 / Note 50": "🎯 حساسية Realme C61 / Note 50\n\nعام: 194\nنقطة حمراء: 190\n2x: 186\n4x: 182\nقناص: 124\nزر اطلاق: 55\nDPI: 650\nجيروسكوب: 186",
        "Realme 11 / 12 / 13 Pro": "🎯 حساسية Realme Pro\n\nعام: 198\nنقطة حمراء: 195\n2x: 190\n4x: 185\nقناص: 130\nزر اطلاق: 50\nDPI: 700\nجيروسكوب: 192",
    }},
    "infinix": {"title": "📱 انفنكس / تكنو", "items": {
        "Hot 30 / 40 / 50": "🎯 حساسية Hot 30 / 40 / 50\n\nعام: 200\nنقطة حمراء: 195\n2x: 190\n4x: 185\nقناص: 132\nزر اطلاق: 60\nDPI: 700\nجيروسكوب: 192",
        "Hot 40 / 50 Pro": "🎯 حساسية Hot Pro\n\nعام: 202\nنقطة حمراء: 198\n2x: 194\n4x: 190\nقناص: 135\nزر اطلاق: 58\nDPI: 710\nجيروسكوب: 195",
        "Note 30 / 40 / 50": "🎯 حساسية Note 30 / 40\n\nعام: 195\nنقطة حمراء: 192\n2x: 188\n4x: 180\nقناص: 126\nزر اطلاق: 55\nDPI: 680\nجيروسكوب: 186",
        "Infinix GT 20 Pro": "🎯 حساسية GT 20 Pro 🔥 تليفون جيمينج\n\nعام: 205\nنقطة حمراء: 200\n2x: 196\n4x: 192\nقناص: 140\nزر اطلاق: 52\nDPI: 730\nجيروسكوب: 200",
        "Tecno Spark / Camon / Pova": "🎯 حساسية Tecno\n\nعام: 198\nنقطة حمراء: 194\n2x: 190\n4x: 185\nقناص: 128\nزر اطلاق: 60\nDPI: 690\nجيروسكوب: 190",
        "Itel S23 / P55 / A70": "🎯 حساسية Itel\n\nعام: 193\nنقطة حمراء: 189\n2x: 185\n4x: 181\nقناص: 124\nزر اطلاق: 61\nDPI: 650\nجيروسكوب: 186",
    }},
    "iphone": {"title": "📱 ايفون / ايباد", "items": {
        "iPhone 11 / 12 / 13": "🎯 حساسية iPhone 11 / 12 / 13\n\nعام: 175\nنقطة حمراء: 170\n2x: 165\n4x: 160\nقناص: 100\nزر اطلاق: 48\nجيروسكوب: 165\nDPI: الايفون مفيهوش DPI",
        "iPhone 14 / 15 / 16": "🎯 حساسية iPhone 14 / 15 / 16\n\nعام: 180\nنقطة حمراء: 175\n2x: 170\n4x: 165\nقناص: 105\nزر اطلاق: 50\nجيروسكوب: 170",
        "iPhone Pro Max": "🎯 حساسية Pro Max 👑\n\nعام: 178\nنقطة حمراء: 172\n2x: 168\n4x: 162\nقناص: 102\nزر اطلاق: 46\nجيروسكوب: 168",
        "iPad / Tablet": "🎯 حساسية iPad\n\nعام: 160\nنقطة حمراء: 155\n2x: 150\n4x: 145\nقناص: 95\nزر اطلاق: 45\nجيروسكوب: 150\n💡 العب 4 صوابع",
        "Samsung Tab / Xiaomi Pad": "🎯 حساسية التابلت\n\nعام: 165\nنقطة حمراء: 160\n2x: 155\n4x: 150\nقناص: 98\nزر اطلاق: 48\nDPI: 550\nجيروسكوب: 155",
    }},
    "other": {"title": "📱 هواوي / فيفو / هونر / ون بلس", "items": {
        "Huawei Nova / Y9": "🎯 حساسية Huawei\n\nعام: 188\nنقطة حمراء: 184\n2x: 180\n4x: 175\nقناص: 118\nزر اطلاق: 58\nDPI: 630\nجيروسكوب: 180",
        "Vivo Y27 / V29 / V30": "🎯 حساسية Vivo\n\nعام: 190\nنقطة حمراء: 186\n2x: 182\n4x: 178\nقناص: 120\nزر اطلاق: 55\nDPI: 650\nجيروسكوب: 182",
        "Honor X8 / X9 / 90 / 200": "🎯 حساسية Honor\n\nعام: 192\nنقطة حمراء: 188\n2x: 184\n4x: 180\nقناص: 122\nزر اطلاق: 54\nDPI: 660\nجيروسكوب: 184",
        "OnePlus 11 / 12 / Nord": "🎯 حساسية OnePlus\n\nعام: 182\nنقطة حمراء: 178\n2x: 174\n4x: 168\nقناص: 110\nزر اطلاق: 48\nDPI: 600\nجيروسكوب: 170",
        "Google Pixel 7 / 8 / 9": "🎯 حساسية Pixel\n\nعام: 180\nنقطة حمراء: 176\n2x: 172\n4x: 168\nقناص: 108\nزر اطلاق: 50\nDPI: 620\nجيروسكوب: 172",
    }},
}

PACKAGES = {
    "p1": {"label": "💎 100 نقطة - 20ج", "points": 100, "price": 20, "vip": False},
    "p2": {"label": "💎 300 نقطة - 50ج", "points": 300, "price": 50, "vip": False},
    "p3": {"label": "💎 700 نقطة - 100ج", "points": 700, "price": 100, "vip": False},
    "p4": {"label": "👑 VIP شهر - 100ج", "points": 0, "price": 100, "vip": True},
    "p5": {"label": "👑 VIP + 500 نقطة - 150ج", "points": 500, "price": 150, "vip": True},
    "p6": {"label": "👑 VIP دائم + 1000 نقطة - 250ج", "points": 1000, "price": 250, "vip": True},
}
SHOP = {
    "s1": {"label": "🎯 حساسية مخصوصة ليك - 50 نقطة", "cost": 50},
    "s2": {"label": "🎡 لفة عجلة زيادة - 20 نقطة", "cost": 20},
    "s3": {"label": "👑 ترقية VIP اسبوع - 200 نقطة", "cost": 200},
}

def main_kb(uid):
    db = load_db(); u = get_user(db, uid)
    kb = [
        [InlineKeyboardButton("🎯 حساسيات التليفونات", callback_data="sens")],
        [InlineKeyboardButton(f"👤 حسابي | 💎 {u['points']} نقطة | {'👑 VIP' if u['vip'] else 'عادي'}", callback_data="profile")],
        [InlineKeyboardButton("🎡 عجلة الحظ", callback_data="wheel"), InlineKeyboardButton("🎁 صندوق", callback_data="box")],
        [InlineKeyboardButton("🎲 لعبة حظ", callback_data="game"), InlineKeyboardButton("🎁 هدية يومية", callback_data="daily")],
        [InlineKeyboardButton("🏆 المتصدرين", callback_data="top"), InlineKeyboardButton("🛒 المتجر", callback_data="shop")],
        [InlineKeyboardButton("💳 شحن - فودافون كاش", callback_data="charge")],
        [InlineKeyboardButton("🎁 دعوة صحابك +10", callback_data="invite"), InlineKeyboardButton("🔑 استبدال كود", callback_data="redeem_info")],
        [InlineKeyboardButton("🏟️ رومات وبطولات", callback_data="rooms"), InlineKeyboardButton("💬 كلم عدي", callback_data="support")],
    ]
    if uid == OWNER_ID:
        kb.append([InlineKeyboardButton("👑 لوحة الاونر عدي", callback_data="admin")])
    return InlineKeyboardMarkup(kb)

def back_kb():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🏠 القايمة الرئيسية", callback_data="home")]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = load_db(); user = update.effective_user; u = get_user(db, user.id, user.first_name)
    if u["banned"]:
        await update.message.reply_text("🚫 انت محظور من البوت، كلم عدي"); return
    if context.args and context.args[0].startswith("ref_"):
        ref = context.args[0].replace("ref_", "")
        if ref != str(user.id) and ref in db["users"]:
            db["users"][ref]["points"] += 10; db["users"][ref]["invited"] += 1
            try: await context.bot.send_message(int(ref), "🎉 حد دخل من لينكك! خدت +10 نقطة 💎")
            except: pass
    save_db(db)
    await update.message.reply_text(f"👑 اهلا يا {user.first_name} في بوت عدي WAR 🔥\n\n💎 نقطك: {u['points']} | {'👑 VIP' if u['vip'] else 'عضو عادي'}\n\n🎯 حساسيات كل التليفونات\n🎡 عجلة حظ وصندوق بيدوا نقط بجد\n💳 شحن فودافون كاش بصورة تحويل\n🔑 اكواد بتدي نقط بجد\n🏆 بطولات ورومات\n\nاختار من تحت 👇", reply_markup=main_kb(user.id))

async def callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer(); data = q.data; uid = q.from_user.id
    db = load_db(); u = get_user(db, uid, q.from_user.first_name)
    if u["banned"] and data != "home":
        await q.edit_message_text("🚫 انت محظور"); return
    if data == "home":
        await q.edit_message_text("👑 بوت عدي WAR - اختار 👇", reply_markup=main_kb(uid)); return
    if data == "sens":
        kb = [[InlineKeyboardButton(v["title"], callback_data=f"brand_{k}")] for k,v in SENS.items()]
        kb.append([InlineKeyboardButton("🏠 رجوع", callback_data="home")])
        await q.edit_message_text("📱 اختار نوع تليفونك:", reply_markup=InlineKeyboardMarkup(kb)); return
    if data.startswith("brand_"):
        b = data.replace("brand_", ""); kb = [[InlineKeyboardButton(name, callback_data=f"phone_{b}_{i}")] for i,name in enumerate(SENS[b]["items"])]
        kb.append([InlineKeyboardButton("⬅️ رجوع", callback_data="sens")])
        await q.edit_message_text(f"{SENS[b]['title']}\n\nاختار موديلك:", reply_markup=InlineKeyboardMarkup(kb)); return
    if data.startswith("phone_"):
        _, b, idx = data.split("_"); name = list(SENS[b]["items"].keys())[int(idx)]; txt = SENS[b]["items"][name]
        await q.edit_message_text(txt + f"\n\n📱 موديلك: {name}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📤 شير", callback_data="invite")],[InlineKeyboardButton("🏠 رجوع", callback_data="home")]])); return
    if data == "profile":
        await q.edit_message_text(f"👤 حسابك يا {u['name']}\n\n🆔 ID: {uid}\n💎 النقط: {u['points']}\n👑 VIP: {'✅ نعم' if u['vip'] else '❌ لا'}\n🎁 دعيت: {u['invited']} واحد\n🎮 لعبت: {u['games']} مرة | كسبت: {u['wins']} مرة", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💳 شحن", callback_data="charge")],[InlineKeyboardButton("🏠 رجوع", callback_data="home")]])); return
    if data == "wheel":
        now = time.time()
        if now - u.get("last_wheel", 0) < 60 and uid != OWNER_ID:
            await q.edit_message_text(f"⏳ استنى {int(60-(now-u['last_wheel']))} ثانية ولف تاني!", reply_markup=back_kb()); return
        win = random.choice([5,5,10,10,15,20,25,0,0,50]); u["points"] += win; u["last_wheel"] = now; save_db(db)
        msg = f"🎡 عجلة الحظ...\n\n🎉 كسبت {win} نقطة!\n💎 رصيدك: {u['points']}" if win>0 else f"😅 المرة دي مجاش حاجة\n💎 رصيدك: {u['points']}"
        await q.edit_message_text(msg, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎡 لف تاني", callback_data="wheel")],[InlineKeyboardButton("🏠 رجوع", callback_data="home")]])); return
    if data == "box":
        now = time.time()
        if now - u.get("last_box", 0) < 60 and uid != OWNER_ID:
            await q.edit_message_text("⏳ استنى دقيقة وافتح صندوق تاني!", reply_markup=back_kb()); return
        win = random.choice([10,20,30,50,100]); u["points"] += win; u["last_box"] = now; save_db(db)
        await q.edit_message_text(f"🎁 فتحت الصندوق!\n\n💎 كسبت {win} نقطة\nرصيدك: {u['points']}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎁 صندوق تاني", callback_data="box")],[InlineKeyboardButton("🏠 رجوع", callback_data="home")]])); return
    if data == "game":
        kb = [[InlineKeyboardButton(f"{i}", callback_data=f"guess_{i}") for i in range(1,4)], [InlineKeyboardButton(f"{i}", callback_data=f"guess_{i}") for i in range(4,7)], [InlineKeyboardButton("🏠 رجوع", callback_data="home")]]
        await q.edit_message_text("🎲 لعبة حظ\n\nاختر رقم من 1 لـ 6، لو طلع صح تكسب 30 نقطة!\nلو غلط تخسر 5 نقط بس.", reply_markup=InlineKeyboardMarkup(kb)); return
    if data.startswith("guess_"):
        pick = int(data.replace("guess_", "")); real = random.randint(1,6); u["games"] += 1
        if pick == real:
            u["points"] += 30; u["wins"] += 1; save_db(db)
            await q.edit_message_text(f"🎉 صح! الرقم كان {real}\nكسبت +30 نقطة\nرصيدك: {u['points']}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎲 العب تاني", callback_data="game")],[InlineKeyboardButton("🏠 رجوع", callback_data="home")]]))
        else:
            u["points"] = max(0, u["points"]-5); save_db(db)
            await q.edit_message_text(f"😅 غلط! الرقم كان {real} مش {pick}\nخسرت 5 نقط\nرصيدك: {u['points']}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎲 حاول تاني", callback_data="game")],[InlineKeyboardButton("🏠 رجوع", callback_data="home")]]))
        return
    if data == "daily":
        today = datetime.now().strftime("%Y-%m-%d")
        if u.get("last_daily") == today:
            await q.edit_message_text("🎁 خدت هديتك النهاردة خلاص! تعالى بكرة.", reply_markup=back_kb()); return
        u["last_daily"] = today; u["points"] += 25; save_db(db)
        await q.edit_message_text(f"🎁 هدية يومية!\n\nخدت +25 نقطة\nرصيدك: {u['points']}", reply_markup=back_kb()); return
    if data == "top":
        users = sorted(db["users"].values(), key=lambda x: x["points"], reverse=True)[:10]
        txt = "🏆 المتصدرين - اعلى نقط:\n\n"
        for i, x in enumerate(users, 1): txt += f"{i}. {x['name']} - {x['points']} نقطة {'👑' if x['vip'] else ''}\n"
        await q.edit_message_text(txt, reply_markup=back_kb()); return
    if data == "shop":
        kb = [[InlineKeyboardButton(v["label"], callback_data=f"buy_{k}")] for k,v in SHOP.items()]
        kb.append([InlineKeyboardButton("🏠 رجوع", callback_data="home")])
        await q.edit_message_text(f"🛒 المتجر\n\nرصيدك: {u['points']} نقطة", reply_markup=InlineKeyboardMarkup(kb)); return
    if data.startswith("buy_"):
        k = data.replace("buy_", ""); item = SHOP[k]
        if u["points"] < item["cost"]:
            await q.edit_message_text(f"❌ نقطك مش كفاية! محتاج {item['cost']} وانت معاك {u['points']}", reply_markup=back_kb()); return
        u["points"] -= item["cost"]
        if k == "s3": u["vip"] = True
        if k == "s2": u["last_wheel"] = 0
        save_db(db)
        await q.edit_message_text(f"✅ اشتريت: {item['label']}\nرصيدك دلوقتي: {u['points']}", reply_markup=back_kb())
        if k == "s1":
            try: await context.bot.send_message(OWNER_ID, f"🛒 حد اشترى حساسية مخصوصة!\nمن: {u['name']} - ID: {uid}")
            except: pass
        return
    if data == "invite":
        link = f"https://t.me/{context.bot.username}?start=ref_{uid}"
        await q.edit_message_text(f"🎁 لينك الدعوة بتاعك:\n\n`{link}`\n\nكل صاحب يدخل منه = +10 نقطة ليك\nدعيت لحد دلوقتي: {u['invited']} واحد", parse_mode="Markdown", reply_markup=back_kb()); return
    if data == "redeem_info":
        u["state"] = "wait_code"; save_db(db)
        await q.edit_message_text("🔑 ابعت الكود دلوقتي، مثال:\n`WAR100`", parse_mode="Markdown", reply_markup=back_kb()); return
    if data == "rooms":
        if db["rooms"]: txt = "🏟️ الرومات المتاحة:\n\n" + "\n\n".join(db["rooms"][-5:])
        else: txt = "🏟️ مفيش رومات دلوقتي.\nتابع عدي، اول ما ينزل روم هتلاقيه هنا."
        await q.edit_message_text(txt, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 رجوع", callback_data="home")]])); return
    if data == "support":
        u["state"] = "wait_support"; save_db(db)
        await q.edit_message_text("💬 ابعت رسالتك لعدي دلوقتي، وهو هيرد عليك.", reply_markup=back_kb()); return
    if data == "charge":
        kb = [[InlineKeyboardButton(v["label"], callback_data=f"pkg_{k}")] for k,v in PACKAGES.items()]
        kb.append([InlineKeyboardButton("🏠 رجوع", callback_data="home")])
        await q.edit_message_text("💳 اختار الباقة:\n\nبعد ما تختار، حول على الرقم وابعت صورة التحويل", reply_markup=InlineKeyboardMarkup(kb)); return
    if data.startswith("pkg_"):
        pk = data.replace("pkg_", ""); p = PACKAGES[pk]; u["state"] = f"wait_receipt_{pk}"; save_db(db)
        await q.edit_message_text(f"💳 انت اخترت: {p['label']}\n\n1️⃣ حول {p['price']}ج على فودافون كاش:\n`{VODAFONE_NUMBER}`\n\n2️⃣ ابعت هنا صورة التحويل (سكرين شوت) دلوقتي\n\n⏳ عدي هيراجعها ويقبلها او يرفضها", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ الغاء", callback_data="home")]])); return
    if data.startswith("approve_") and uid == OWNER_ID:
        _, target, pk = data.split("_"); target = int(target); p = PACKAGES[pk]
        tu = get_user(db, target); tu["points"] += p["points"]
        if p.get("vip"): tu["vip"] = True
        tu["state"] = None; db["pending"].pop(str(target), None); save_db(db)
        await q.edit_message_text(f"✅ تم القبول - {p['label']} وصلت لـ {target}")
        try: await context.bot.send_message(target, f"✅ عدي قبل التحويل بتاعك! 🎉\n\nوصلك: {p['label']}\n💎 رصيدك: {tu['points']} نقطة\n👑 VIP: {'✅' if tu['vip'] else '❌'}")
        except: pass
        return
    if data.startswith("reject_") and uid == OWNER_ID:
        _, target, pk = data.split("_"); target = int(target)
        tu = get_user(db, target); tu["state"] = None; db["pending"].pop(str(target), None); save_db(db)
        await q.edit_message_text(f"❌ تم الرفض لـ {target}")
        try: await context.bot.send_message(target, "❌ عدي رفض التحويل بتاعك.\nلو حولت بجد كلم عدي وابعتله الصورة تاني.")
        except: pass
        return
    if data == "admin" and uid == OWNER_ID:
        total = len(db["users"]); pend = len(db["pending"]); vip_count = sum(1 for x in db["users"].values() if x["vip"])
        await q.edit_message_text(f"👑 لوحة عدي\n\n👥 المستخدمين: {total}\n👑 VIP: {vip_count}\n⏳ طلبات شحن معلقة: {pend}\n🔑 اكواد: {len(db['codes'])}\n\nاوامرك:\n/makecode WAR100 50\n/makecode VIP50 0 VIP\n/listcodes\n/delcode WAR100\n/ban [id]\n/unban [id]\n/addpoints [id] [نقط]\n/makevip [id]\n/remvip [id]\n/addroom الاسم | ID | باسورد\n/clearrooms\n/broadcast رسالتك", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 رجوع", callback_data="home")]])); return

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = load_db(); uid = update.effective_user.id; u = get_user(db, uid, update.effective_user.first_name)
    if u["banned"]: return
    if update.message.photo and u.get("state","").startswith("wait_receipt_"):
        pk = u["state"].replace("wait_receipt_", ""); p = PACKAGES[pk]
        photo_id = update.message.photo[-1].file_id
        db["pending"][str(uid)] = {"pkg": pk, "photo": photo_id}; save_db(db)
        await update.message.reply_text("✅ وصلت الصورة! مستني عدي يراجعها.\nهيجيلك رسالة اول ما يقبل او يرفض.")
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("✅ قبول", callback_data=f"approve_{uid}_{pk}"), InlineKeyboardButton("❌ رفض", callback_data=f"reject_{uid}_{pk}")]])
        try: await context.bot.send_photo(OWNER_ID, photo_id, caption=f"💳 طلب شحن جديد!\n\nمن: {u['name']} - ID: {uid}\nالباقة: {p['label']}\nالسعر: {p['price']}ج\nحول على: {VODAFONE_NUMBER}", reply_markup=kb)
        except: pass
        return
    if update.message.text and u.get("state") == "wait_code":
        code = update.message.text.strip().upper()
        if code in db["codes"] and not db["codes"][code].get("used"):
            c = db["codes"][code]
            if c.get("vip"): u["vip"] = True
            u["points"] += c["points"]; c["used"] = True; u["state"] = None; save_db(db)
            await update.message.reply_text(f"✅ الكود صح! 🎉\nخدت +{c['points']} نقطة\n👑 VIP: {'✅' if u['vip'] else '❌'}\nرصيدك: {u['points']}", reply_markup=main_kb(uid))
        else:
            await update.message.reply_text("❌ الكود غلط او مستخدم قبل كده")
        return
    if update.message.text and u.get("state") == "wait_support":
        u["state"] = None; save_db(db)
        await update.message.reply_text("✅ رسالتك وصلت لعدي، هيرد عليك قريب.")
        try: await context.bot.send_message(OWNER_ID, f"💬 رسالة جديدة من {u['name']} - ID: {uid}\n\n{update.message.text}\n\nللرد: /reply {uid} رسالتك")
        except: pass
        return
    if update.message.text and not update.message.text.startswith("/"):
        await update.message.reply_text("استخدم الزراير من /start 👇", reply_markup=main_kb(uid))

async def makecode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID: return
    if len(context.args) < 2: await update.message.reply_text("اكتب: /makecode WAR100 50\nاو: /makecode VIP50 0 VIP"); return
    db = load_db(); is_vip = len(context.args) >= 3 and context.args[2].upper() == "VIP"
    db["codes"][context.args[0].upper()] = {"points": int(context.args[1]), "used": False, "vip": is_vip}; save_db(db)
    await update.message.reply_text(f"✅ عملت كود {context.args[0].upper()} بـ {context.args[1]} نقطة {'+ VIP 👑' if is_vip else ''}")
async def listcodes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID: return
    db = load_db()
    if not db["codes"]: await update.message.reply_text("مفيش اكواد"); return
    txt = "🔑 الاكواد:\n\n"
    for k,v in db["codes"].items(): txt += f"{k} - {v['points']} نقطة {'+VIP' if v.get('vip') else ''} - {'✅ مستخدم' if v['used'] else '⏳ شغال'}\n"
    await update.message.reply_text(txt)
async def delcode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID: return
    db = load_db(); db["codes"].pop(context.args[0].upper(), None); save_db(db); await update.message.reply_text("✅ اتمسح")
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID: return
    db = load_db(); t = get_user(db, int(context.args[0])); t["banned"] = True; save_db(db); await update.message.reply_text("🚫 اتحظر")
async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID: return
    db = load_db(); t = get_user(db, int(context.args[0])); t["banned"] = False; save_db(db); await update.message.reply_text("✅ اتفك حظره")
async def addpoints(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID: return
    db = load_db(); t = get_user(db, int(context.args[0])); t["points"] += int(context.args[1]); save_db(db); await update.message.reply_text(f"✅ بقى معاه {t['points']} نقطة")
    try: await context.bot.send_message(int(context.args[0]), f"🎉 عدي زودلك +{context.args[1]} نقطة!\nرصيدك: {t['points']}")
    except: pass
async def makevip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID: return
    db = load_db(); t = get_user(db, int(context.args[0])); t["vip"] = True; save_db(db); await update.message.reply_text("👑 بقى VIP")
    try: await context.bot.send_message(int(context.args[0]), "👑 عدي خلاك VIP! مبروك 🎉")
    except: pass
async def remvip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID: return
    db = load_db(); t = get_user(db, int(context.args[0])); t["vip"] = False; save_db(db); await update.message.reply_text("❌ اتشال VIP")
async def addroom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID: return
    db = load_db(); db["rooms"].append(" ".join(context.args)); save_db(db); await update.message.reply_text("✅ اتضاف الروم")
async def clearrooms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID: return
    db = load_db(); db["rooms"] = []; save_db(db); await update.message.reply_text("✅ اتمسحت الرومات")
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID: return
    db = load_db(); msg = " ".join(context.args); c=0
    for uid in list(db["users"].keys()):
        try: await context.bot.send_message(int(uid), f"📢 من عدي:\n\n{msg}"); c+=1
        except: pass
    await update.message.reply_text(f"✅ اتبعتت لـ {c} واحد")
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID: return
    try: await context.bot.send_message(int(context.args[0]), f"💬 رد من عدي:\n\n{' '.join(context.args[1:])}"); await update.message.reply_text("✅ اتبعت")
    except: await update.message.reply_text("❌ مش عارف ابعتله")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("makecode", makecode))
    app.add_handler(CommandHandler("listcodes", listcodes))
    app.add_handler(CommandHandler("delcode", delcode))
    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("unban", unban))
    app.add_handler(CommandHandler("addpoints", addpoints))
    app.add_handler(CommandHandler("makevip", makevip))
    app.add_handler(CommandHandler("remvip", remvip))
    app.add_handler(CommandHandler("addroom", addroom))
    app.add_handler(CommandHandler("clearrooms", clearrooms))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("reply", reply))
    app.add_handler(CallbackQueryHandler(callbacks))
    app.add_handler(MessageHandler(filters.PHOTO | (filters.TEXT & ~filters.COMMAND), handle_msg))
    print("Bot Running - WAR by Ady")
    app.run_polling()

if __name__ == "__main__": main()
