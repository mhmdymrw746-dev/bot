# ===== BOT TRAN - الاونر @TRAN_5 👑 - لريندر =====
import os, random, time, threading, requests
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# ===== الاعدادات =====
OWNER_ID = "8188263997"
OWNER_USER = "@TRAN_5"
BANK_NAME = "بنك TRAN 👑"
TAX = 0.05

SUPPORT_TEAM = [
    {"id": "SUPPORT_1", "user": "@cat_max_10", "name": "Mr cat", "shift": "صبح", "online": True, "solved": 0, "rating": 5},
    {"id": "SUPPORT_2", "user": "@MOON_104", "name": "تيتو", "shift": "ليل", "online": True, "solved": 0, "rating": 5},
]

# ===== الداتا =====
users = {}  # {user_id: {...}}
tickets = {}  # {id: {...}}
ticket_count = 0
logs = []
families = {}

def get_user(uid, name="بطل"):
    if uid not in users:
        users[uid] = {
            "name": name, "money": 1000, "bank": 0, "level": 1, "xp": 0,
            "job": "عاطل", "married": None, "family": None, "items": [],
            "car": None, "house": None, "plane": False, "warns": 0,
            "banned": False, "last_daily": 0, "debt": 0, "pet": None
        }
    return users[uid]

def is_owner(uid):
    return OWNER_ID in str(uid) or "TRAN_5" in str(uid)

def is_support(uid):
    return any(s["user"] in str(uid) or s["id"] in str(uid) for s in SUPPORT_TEAM)

def fmt(n):
    return f"{int(n):,}"

# ===== القوايم =====
def main_menu(is_own=False, is_sup=False):
    m = f"""🏦 *{BANK_NAME}*
أهلا يا بطل 👑 اختار:

💰 فلوسك: /فلوسي
🎰 كازينو | 🥷 سرقة | 💼 شغل
🏦 بنك | 💸 تحويل | 🎁 هدية
🏠 عقارات | 🚗 عربيتي | ✈️ طيارة
👨‍👩‍👧 عيلتي | 💍 اتجوز | 📋 مهامي
🏆 التوب | 🆘 دعم البوت
"""
    if is_own:
        m += "\n👑 *لوحة الاونر:* /اونر"
    if is_sup:
        m += "\n🆘 *لوحة الدعم:* /دعم"
    return m

OWNER_MENU = """
👑 *لوحة الاونر @TRAN_5*
[ 💰 ادي فلوس للكل ] /ادي_للكل 1000
[ 💸 اسحب من الكل ] /اسحب_من_الكل 500
[ 🎁 هدية للكل ] /هدية_للكل
[ 📢 اعلان للكل ] /اعلان
[ 👀 مين سرق مين ] /سجل
[ 📊 احصائيات ] /احصائيات
[ 🔥 حدث خاص ] /حدث
[ 🏆 مسابقة ] /مسابقة
[ 🚫 حظر ] /حظر @حد
[ ✅ فك ] /فك @حد
[ 👥 فريق الدعم ] /فريق_الدعم
[ ⏰ صحي البوت ] /صحيني
[ 🟢 البوت شغال؟ ] /حالة
[ 🔄 ريستارت ] /ريستارت
[ 🔙 رجوع ] /قايمة
"""

SUPPORT_MENU = """
🆘 *لوحة الدعم*
[ 🟢 انا موجود ] /موجود
[ 🔴 انا مشغول ] /مشغول
[ 📩 التذاكر ] /تذاكر
[ ✅ اقبل ] /اقبل 1
[ 💰 تعويض ] /تعويض 1 1000
[ ✅ قفل ] /قفل 1
[ 🔄 انقل ] /انقل 1
"""

# ===== محرك البوت - هنا كل الأوامر =====
def handle_message(user_id, name, text):
    global ticket_count
    text = text.strip()
    low = text.lower()
    u = get_user(user_id, name)
    owner = is_owner(user_id)
    sup = is_support(user_id)

    if u["banned"] and not owner:
        return "انت محظور يا معلم 🚫 كلم الدعم"

    # ===== قايمة =====
    if low in ["قايمة", "/قايمة", "menu", "hi", "هاي", "السلام عليكم"]:
        return main_menu(owner, sup)
    if low == "/اونر" and owner:
        return OWNER_MENU
    if low == "/اونر" and not owner:
        return "انت كداب يا معلم، الاونر الحقيقي @TRAN_5 بس 😂👑"
    if low == "/دعم" and (sup or owner):
        return SUPPORT_MENU

    # ===== فلوس =====
    if low in ["/فلوسي", "/رصيد"]:
        return f"""💰 *فلوسك يا {name}*
كاش: {fmt(u['money'])}
بنك: {fmt(u['bank'])}
مستوى: {u['level']} | XP: {u['xp']}
شغل: {u['job']}
عيلة: {u['family'] or 'مفيش'}
متجوز: {u['married'] or 'لا'}
ديون: {fmt(u['debt'])}"""
    if low == "/يومية":
        now = time.time()
        if now - u["last_daily"] < 86400:
            return "خدت اليومية خلاص، تعالى بكرة 😂"
        u["last_daily"] = now; u["money"] += 1000
        return "خدت 1000 يومية 🎁💰"
    if low.startswith("/تحويل"):
        try:
            amt = int(text.split()[1])
        except:
            return "اكتب: /تحويل 500 @حد"
        if u["money"] < amt:
            return "فلوسك مش كفاية 😭"
        tax = int(amt * TAX); u["money"] -= amt
        return f"تم تحويل {fmt(amt-tax)} (ضريبة {fmt(tax)}) ✅"
    if low == "/بنك":
        return "🏦 *البنك*\n/ايداع 1000\n/سحب 500\n/قرض 5000\n/سدد"
    if low.startswith("/ايداع"):
        try: a = int(text.split()[1])
        except: return "اكتب /ايداع 1000"
        if u["money"] < a: return "ممعكش 😭"
        u["money"] -= a; u["bank"] += a
        return f"حطيت {fmt(a)} في البنك ✅"
    if low.startswith("/سحب"):
        try: a = int(text.split()[1])
        except: return "اكتب /سحب 500"
        if u["bank"] < a: return "البنك مفهوش 😭"
        u["bank"] -= a; u["money"] += a
        return f"سحبت {fmt(a)} ✅"
    if low.startswith("/قرض"):
        try: a = int(text.split()[1])
        except: a = 5000
        u["money"] += a; u["debt"] += a
        return f"خدت قرض {fmt(a)}، سدده بـ /سدد 💸"
    if low == "/سدد":
        if not u["debt"]: return "معليكش ديون"
        if u["money"] < u["debt"]: return "فلوسك مش كفاية تسدد 😭"
        u["money"] -= u["debt"]; u["debt"] = 0
        return "سددت ديونك ✅"

    # ===== سرقة / كازينو / شغل =====
    if low in ["/سرقة", "/اسرق"]:
        if random.random() < 0.5:
            win = random.randint(200, 1200); u["money"] += win
            logs.append(f"{name} سرق {win}")
            return f"سرقت {fmt(win)} 🥷🔥"
        else:
            u["money"] = max(0, u["money"]-300)
            return "اتمسكت! اتخصم منك 300 واتسجنت 😂🚨"
    if low in ["/كازينو", "/قمار"]:
        if u["money"] < 100: return "ممعكش فلوس للكازينو 😭"
        if random.random() < 0.45:
            u["money"] += 500; return "كسبت 500 في الكازينو 🎰🔥"
        else:
            u["money"] -= 200; return "خسرت 200 🎰😭"
    if low == "/شغل":
        jobs = [("دليفري", 300), ("مبرمج", 800), ("حرامي", 1000), ("تاجر", 600)]
        j, amt = random.choice(jobs)
        u["money"] += amt; u["xp"] += 10
        if u["xp"] >= 100: u["level"] += 1; u["xp"] = 0
        return f"اشتغلت {j} وكسبت {fmt(amt)} 💼"
    if low == "/توب":
        top = sorted(users.values(), key=lambda x: x["money"]+x["bank"], reverse=True)[:5]
        t = "🏆 *التوب 5* 👑\n"
        for i, x in enumerate(top):
            t += f"{i+1}. {x['name']} - {fmt(x['money']+x['bank'])}\n"
        return t
    if low == "/مهامي":
        return "📋 *مهامك النهاردة:*\n1. اسرق مرة /اسرق\n2. العب كازينو /كازينو\n3. ابعت هدية /هدية\nخلصهم وخد 2000 🎁"
    if low == "/عربيتي":
        return f"عربيتك: {u['car']} 🚗😎" if u["car"] else "معندكش عربية، اشتري بـ /اشتري عربية"
    if low.startswith("/اشتري"):
        if "عربية" in text:
            if u["money"] < 15000: return "معكش 😭"
            u["money"] -= 15000; u["car"] = "لمبرجيني"
            return "مبروك اشتريت لمبرجيني 😎🔥"
        if "شقة" in text:
            if u["money"] < 20000: return "معكش 😭"
            u["money"] -= 20000; u["house"] = "شقة"
            return "مبروك اشتريت شقة 🏠🔥"
        if "طيارة" in text:
            if u["money"] < 100000: return "معكش 😭"
            u["money"] -= 100000; u["plane"] = True
            return "مبروك اشتريت طيارة ✈️ يا كابتن 👨‍✈️"
    if low.startswith("/اتجوز"):
        return f"مبرووووك {name} اتجوز 🎉❤️🎂\nالمتجوزين فلوسهم مشتركة"
    if low == "/طلق":
        return "لا حول ولا قوة، الطلاق مش حلو 😭"
    if low.startswith("/اعمل_عيلة"):
        n = text.split()[1] if len(text.split()) > 1 else "TRAN"
        u["family"] = n
        families.setdefault(n, []).append(name)
        return f"عملت عيلة {n} 👑🔥"
    if low.startswith("/عيلة"):
        return f"👨‍👩‍👧 *عيلتك:* {u['family'] or 'مفيش، اعمل عيلة بـ /اعمل_عيلة TRAN'}"

    # ===== الدعم =====
    if low in ["/دعم", "دعم", "دعم البوت"]:
        return """🆘 *دعم البوت*
عندك مشكلة؟ اكتب:
 /مشكلة فلوسي راحت
 /مشكلة حد سرقني
 /مشكلة البوت مش شغال
 /مشكلة حد شتمني
 /مشكلة عندي فكرة"""
    if low.startswith("/مشكلة"):
        ticket_count += 1; tid = ticket_count
        prob = text.replace("/مشكلة", "").strip() or "مشكلة عامة"
        tickets[tid] = {"user": user_id, "name": name, "problem": prob, "status": "مفتوحة", "support": None}
        # هنا البوت هيبعت اشعار للاونر والدعم - في الواتساب هيتبعت رسالة
        notif = f"🔔 حد عايز دعم!\n👤 {name}\n🎫 تذكرة #{tid}\n📝 {prob}\nمين هيقبل؟ /اقبل {tid}\n@TRAN_5 @cat_max_10 @MOON_104"
        print(notif)
        return f"تم يا بطل، بعتنا مشكلتك للدعم ❤️✅\nرقم تذكرتك: #{tid}\nالدعم هيكلمك بسرعة\n---\n[اشعار راح للاونر والدعم]:\n{notif}"
    if low.startswith("/تذاكر") and (sup or owner):
        open_t = [(k, v) for k, v in tickets.items() if v["status"] == "مفتوحة"]
        if not open_t: return "مفيش تذاكر مفتوحة ✅"
        t = "📩 *التذاكر المفتوحة:*\n"
        for k, v in open_t: t += f"#{k} - {v['name']}: {v['problem']}\n"
        return t + "\nاقبل بـ /اقبل رقم"
    if low.startswith("/اقبل") and (sup or owner):
        try: tid = int(text.split()[1])
        except: return "اكتب /اقبل رقم"
        tk = tickets.get(tid)
        if not tk: return "مفيش تذكرة بالرقم ده"
        if tk["support"]: return f"خلاص {tk['support']} قبلها"
        tk["support"] = name; tk["status"] = "مقبولة"
        return f"✅ انت قبلت تذكرة #{tid}\nكلم {tk['name']} دلوقتي ❤️\nاوامر: /تعويض {tid} 1000 - /قفل {tid} - /انقل {tid}"
    if low.startswith("/قفل") and (sup or owner):
        try: tid = int(text.split()[1])
        except: return "اكتب /قفل رقم"
        if tid in tickets:
            tickets[tid]["status"] = "مقفولة"
            for s in SUPPORT_TEAM:
                if s["name"] == name: s["solved"] += 1
            return f"قفلت تذكرة #{tid} ✅\nقيم الدعم بـ ⭐ من 1-5"
    if low.startswith("/تعويض") and (sup or owner):
        try:
            _, tid, amt = text.split(); tid = int(tid); amt = int(amt)
        except: return "اكتب /تعويض رقم مبلغ"
        tk = tickets.get(tid)
        if tk:
            get_user(tk["user"])["money"] += amt
            return f"ديت {tk['name']} تعويض {fmt(amt)} ✅"
    if low.startswith("/انقل") and (sup or owner):
        try: tid = int(text.split()[1])
        except: return "اكتب /انقل رقم"
        if tid in tickets:
            tickets[tid]["support"] = None; tickets[tid]["status"] = "مفتوحة"
            return f"نقلت تذكرة #{tid} للدعم التاني 🔄"
    if low == "/موجود" and sup:
        return "تمام انت دلوقتي موجود 🟢 والبوت هيبعتلك تذاكر"
    if low == "/مشغول" and sup:
        return "تمام انت مشغول 🔴 البوت هيودي التذاكر للتاني"
    if low == "/فريق_الدعم" and owner:
        t = "👥 *فريق الدعم:*\n"
        for s in SUPPORT_TEAM:
            t += f"{s['name']} {s['user']} - شيفت {s['shift']} - حل {s['solved']} مشكلة - تقييم {s['rating']}⭐\n"
        return t

    # ===== الاونر =====
    if owner:
        if low.startswith("/ادي_للكل"):
            try: a = int(text.split()[1])
            except: a = 1000
            for x in users.values(): x["money"] += a
            return f"ديت للكل {fmt(a)} 🎁👑"
        if low.startswith("/اسحب_من_الكل"):
            try: a = int(text.split()[1])
            except: a = 500
            for x in users.values(): x["money"] = max(0, x["money"]-a)
            return f"سحبت من الكل {fmt(a)} 💸"
        if low == "/هدية_للكل":
            for x in users.values(): x["money"] += 1000
            return "الاونر @TRAN_5 بعتلكم هدية 1000، قولوله شكرا ❤️👑"
        if low == "/سجل":
            return "👀 *سجل السرقة:*\n" + ("\n".join(logs[-10:]) or "مفيش سرقة")
        if low == "/احصائيات":
            total = sum(x["money"]+x["bank"] for x in users.values())
            return f"📊 *احصائيات البنك*\nعدد الناس: {len(users)}\nفلوس البنك: {fmt(total)}\nتذاكر: {ticket_count}"
        if low == "/مسابقة":
            return "🏆 *مسابقة فورية!* أول واحد يكتب 'انا' يكسب 5000 🔥"
        if low == "/حدث":
            return "🔥 *حدث خاص!* النهاردة كل السرقة ×2 والضرايب 0% - من الاونر @TRAN_5 👑"
        if low == "/صحيني":
            return "انا صاحي يا اونر، أمرني 👑😎"
        if low == "/حالة":
            return "شغال 100% يا اونر، نمت 0 دقيقة النهاردة 🟢👑"
        if low == "/ريستارت":
            return "بعمل ريستارت وهرجع في 10 ثواني 🔄"
        if low.startswith("/حظر"):
            return "حظرت الشخص 🚫"
        if low.startswith("/فك"):
            return "فكيت الحظر ✅"
        if low.startswith("/اعلان"):
            return f"📢 *اعلان من الاونر @TRAN_5:* {text.replace('/اعلان','')}"

    # ===== رد ذكي =====
    if "زعلان" in low:
        return "مالك يا بطل؟ تعال العب وهنفرفشك 😂❤️ /كازينو"
    if "فرحان" in low:
        return "فرحان ليه؟ فرحنا معاك 🎉"
    if low == "انا":
        return "كسبت المسابقة 5000! 🎉🔥" if random.random() < 0.3 else "اهلا بيك 😂"

    return "مش فاهم يا بطل 😂 اكتب /قايمة"

# ===== سيرفر ريندر =====
@app.route("/")
def home():
    return "البوت شغال يا اونر 👑🟢 - TRAN BOT"

@app.route("/ping")
def ping():
    return "pong - انا صاحي 😎"

@app.route("/health")
def health():
    return jsonify({"status": "online", "users": len(users), "tickets": ticket_count, "owner": OWNER_USER})

@app.route("/webhook", methods=["POST"])
def webhook():
    # ده اللي الواتساب هيبعت عليه - او استخدمه مع اي منصة
    data = request.get_json() or {}
    user_id = data.get("from", "unknown")
    name = data.get("name", "بطل")
    text = data.get("text", "")
    reply = handle_message(user_id, name, text)
    return jsonify({"reply": reply})

@app.route("/test")
def test():
    # جرب البوت من المتصفح: /test?msg=/فلوسي&user=123
    msg = request.args.get("msg", "/قايمة")
    user = request.args.get("user", "test123")
    name = request.args.get("name", "بطل")
    return handle_message(user, name, msg)

# ===== صحي نفسك كل 4 دقايق - عشان ريندر مينيموش =====
def keep_alive():
    url = os.environ.get("RENDER_EXTERNAL_URL", "https://bot-tran.onrender.com")
    while True:
        try:
            requests.get(f"{url}/ping", timeout=10)
            print(f"صحيت نفسي ✅ {datetime.now()}")
        except Exception as e:
            print(f"نمت شوية: {e}")
        time.sleep(240)  # 4 دقايق

threading.Thread(target=keep_alive, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
