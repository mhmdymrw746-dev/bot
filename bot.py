import os, json, time, random, traceback
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- سيرفر عشان Render يشوفه شغال ---
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers(); self.wfile.write(b"Bot is running!")
    def log_message(self, *a): pass
def keep_alive():
    port = int(os.environ.get("PORT", 10000))
    try:
        server = HTTPServer(("0.0.0.0", port), Handler)
        Thread(target=server.serve_forever, daemon=True).start()
        print(f"Web server on {port}")
    except Exception as e:
        print("Web server error:", e)
keep_alive()

TOKEN = os.environ.get("TOKEN")
if not TOKEN:
    print("❌ مفيش TOKEN في Render!")
    raise SystemExit("Set TOKEN env")

OWNER_ID = int(os.environ.get("OWNER_ID", "8188263997"))
bot = telebot.TeleBot(TOKEN, parse_mode=None)

DATA_FILE = "data.json"
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f: return json.load(f)
        except: return {}
    return {}
def save_data():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e: print("Save error", e)
data = load_data()

def get_user(uid):
    uid = str(uid)
    if uid not in data:
        data[uid] = {"money": 0, "daily": 0, "gift": 0, "spin": 0, "name": "مستخدم", "level": 1, "xp": 0, "streak": 0, "vip": False, "weapons": [], "contest_score": 0, "used_codes": []}
        save_data()
    for k,v in [("vip",False),("weapons",[]),("contest_score",0),("used_codes",[]),("xp",0),("level",1),("streak",0),("daily",0),("gift",0),("spin",0)]:
        if k not in data[uid]: data[uid][k]=v
    return data[uid]
def is_owner(uid): return int(uid) == OWNER_ID
def is_vip(u): return u.get("vip", False)
def vip_mult(u): return 2 if is_vip(u) else 1
def add_money(uid, amount):
    u = get_user(uid)
    amount = amount * vip_mult(u)
    u["money"] += amount; u["xp"] += amount//10; u["contest_score"] = u.get("contest_score",0) + amount
    new_level = u["xp"] // 100 + 1
    if new_level > u["level"]:
        u["level"] = new_level
        try: bot.send_message(int(uid), f"🎉 مبروك وصلت مستوى {new_level}!")
        except: pass
    save_data(); return amount

STORE = {"1": {"name": "🎨 خلفية موبايل", "price": 50},"2": {"name": "🎵 اغنية MP3", "price": 100},"3": {"name": "🎬 نتفليكس يوم", "price": 200},"4": {"name": "🎮 ببجي 60 شدة", "price": 500},"5": {"name": "⭐ VIP - فلوس الضعف", "price": 1000},"6": {"name": "💎 لقب اسطوري", "price": 2000}}
WEAPONS = {"w1": {"name": "🔪 سكينة", "price": 100, "bonus": 5},"w2": {"name": "🔫 مسدس", "price": 300, "bonus": 15},"w3": {"name": "💣 قنبلة", "price": 600, "bonus": 30},"w4": {"name": "🚀 بازوكا", "price": 1200, "bonus": 60},"w5": {"name": "⚔️ سيف اسطوري", "price": 2500, "bonus": 120}}
TASKS = [{"name": "سؤال سريع", "reward": 20},{"name": "حظك اليوم", "reward": 30},{"name": "مهمة كلمة السر", "reward": 50},{"name": "تحدي الذاكرة", "reward": 40}]
GIFT_CODES = {"WELCOME100": 100, "MEGA500": 500, "BOSS1000": 1000}

def main_menu(uid):
    u = get_user(uid)
    m = InlineKeyboardMarkup(row_width=2)
    m.add(
        InlineKeyboardButton("📋 المهام", callback_data="tasks"),
        InlineKeyboardButton("🛒 المتجر", callback_data="store"),
        InlineKeyboardButton("🔫 محل الأسلحة", callback_data="weapons"),
        InlineKeyboardButton("🏆 مسابقة", callback_data="contest"),
        InlineKeyboardButton("👑 VIP", callback_data="vip"),
        InlineKeyboardButton("💰 فلوسي", callback_data="balance"),
        InlineKeyboardButton("🎁 يومية", callback_data="daily"),
        InlineKeyboardButton("🎡 عجلة الحظ", callback_data="spin"),
        InlineKeyboardButton("🎲 لعبة الحظ", callback_data="gamble"),
        InlineKeyboardButton("🏆 الاغنياء", callback_data="top"),
        InlineKeyboardButton("👤 بروفايلي", callback_data="profile"),
        InlineKeyboardButton("🎁 هدية", callback_data="gift"),
        InlineKeyboardButton("👥 دعوة", callback_data="invite"),
        InlineKeyboardButton("🎁 كود هدية", callback_data="code"),
    )
    if is_owner(uid):
        m.add(InlineKeyboardButton("👑 لوحة الاونر", callback_data="owner"))
    m.add(InlineKeyboardButton("🔄 تحديث", callback_data="back"))
    return m

@bot.message_handler(commands=['start'])
def start(message):
    u = get_user(message.from_user.id)
    u["name"] = message.from_user.first_name or "مستخدم"
    if len(message.text.split()) > 1:
        try:
            inviter = message.text.split()[1]
            if inviter != str(message.from_user.id) and inviter in data:
                add_money(int(inviter), 50)
                bot.send_message(int(inviter), f"🎉 صاحبك دخل! خدت +50")
        except: pass
    save_data()
    vip = " 👑 VIP" if is_vip(u) else ""
    bot.send_message(message.chat.id, f"اهلا {u['name']}{vip} 🔥\n💰 {u['money']} | مستوى {u['level']}\n\nدوس 👇", reply_markup=main_menu(message.from_user.id))

@bot.message_handler(commands=['owner'])
def owner_cmd(message):
    if not is_owner(message.from_user.id):
        bot.send_message(message.chat.id, "انت مش الاونر ❌"); return
    bot.send_message(message.chat.id, "👑 لوحة الاونر", reply_markup=main_menu(message.from_user.id))

@bot.callback_query_handler(func=lambda call: True)
def all_buttons(call):
    uid = call.from_user.id; u = get_user(uid); chat_id = call.message.chat.id; d = call.data
    try: bot.answer_callback_query(call.id)
    except: pass
    try:
        if d == "back":
            bot.send_message(chat_id, f"💰 معاك: {u['money']} | مستوى {u['level']}", reply_markup=main_menu(uid)); return
        if d == "balance":
            bot.send_message(chat_id, f"💰 معاك: {u['money']}\n⭐ XP: {u['xp']} | مستوى: {u['level']}\n🏆 نقط مسابقة: {u.get('contest_score',0)}", reply_markup=main_menu(uid)); return
        if d == "profile":
            weapons = ", ".join([WEAPONS[w]["name"] for w in u.get("weapons",[]) if w in WEAPONS]) or "مفيش"
            vip_txt = "👑 VIP - بتاخد الضعف ✅" if is_vip(u) else "عادي"
            bot.send_message(chat_id, f"👤 بروفايلك\n\nاسم: {u['name']}\nID: {uid}\n💰 فلوس: {u['money']}\nمستوى: {u['level']} | XP: {u['xp']}\n🔥 سلسلة: {u.get('streak',0)}\n🏆 مسابقة: {u.get('contest_score',0)}\n🔫 اسلحتك: {weapons}\n👑 حالتك: {vip_txt}", reply_markup=main_menu(uid)); return
        if d == "vip":
            if is_vip(u):
                bot.send_message(chat_id, "انت VIP اصلا 👑\nبتاخد فلوس الضعف", reply_markup=main_menu(uid)); return
            m = InlineKeyboardMarkup(); m.add(InlineKeyboardButton("👑 اشتري VIP - 1000", callback_data="buy_vip")); m.add(InlineKeyboardButton("🔙 رجوع", callback_data="back"))
            bot.send_message(chat_id, "👑 مميزات VIP:\n\n✅ كل فلوسك ×2\n✅ اليومية 100 بدل 10\n✅ هدية 200\n✅ لقب 👑\n\nالسعر: 1000", reply_markup=m); return
        if d == "buy_vip":
            if u["money"] >= 1000:
                u["money"] -= 1000; u["vip"] = True; save_data()
                bot.send_message(chat_id, "مبروووك 🎉 بقيت VIP 👑", reply_markup=main_menu(uid))
            else:
                bot.send_message(chat_id, f"فلوسك مش كفاية 😢 محتاج 1000 ومعاك {u['money']}", reply_markup=main_menu(uid))
            return
        if d == "weapons":
            m = InlineKeyboardMarkup()
            for k, w in WEAPONS.items():
                owned = " ✅ معاك" if k in u.get("weapons",[]) else f" - {w['price']}"
                m.add(InlineKeyboardButton(f"{w['name']} +{w['bonus']}{owned}", callback_data=f"buyw_{k}"))
            m.add(InlineKeyboardButton("🔙 رجوع", callback_data="back"))
            total_bonus = sum([WEAPONS[w]["bonus"] for w in u.get("weapons",[]) if w in WEAPONS])
            bot.send_message(chat_id, f"🔫 محل الأسلحة - معاك {u['money']}\n⚡ قوتك: +{total_bonus}", reply_markup=m); return
        if d.startswith("buyw_"):
            k = d.replace("buyw_", ""); w = WEAPONS[k]
            if k in u.get("weapons",[]):
                bot.send_message(chat_id, "معاك السلاح ده اصلا ✅", reply_markup=main_menu(uid)); return
            if u["money"] >= w["price"]:
                u["money"] -= w["price"]; u["weapons"].append(k); save_data()
                bot.send_message(chat_id, f"مبرووك 🎉 اشتريت {w['name']}\n💰 فاضل: {u['money']}", reply_markup=main_menu(uid))
            else:
                bot.send_message(chat_id, f"فلوسك مش كفاية 😢", reply_markup=main_menu(uid))
            return
        if d == "contest":
            sorted_users = sorted(data.items(), key=lambda x: x[1].get('contest_score',0), reverse=True)[:5]
            txt = "🏆 مسابقة اليوم - اعلى نقط يكسب 500!\n\n"
            for i, (uid2, info) in enumerate(sorted_users):
                txt += f"{i+1}. {info.get('name','?')} - {info.get('contest_score',0)}\n"
            txt += f"\nنقطك: {u.get('contest_score',0)}"
            m = InlineKeyboardMarkup(); m.add(InlineKeyboardButton("📋 روح اعمل مهام", callback_data="tasks")); m.add(InlineKeyboardButton("🔙 رجوع", callback_data="back"))
            bot.send_message(chat_id, txt, reply_markup=m); return
        if d == "top":
            sorted_users = sorted(data.items(), key=lambda x: x[1].get('money',0), reverse=True)[:10]
            txt = "🏆 ترتيب الاغنياء:\n\n"; medals = ["🥇","🥈","🥉","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
            for i, (uid2, info) in enumerate(sorted_users):
                txt += f"{medals[i]} {info.get('name','?')} - {info.get('money',0)} 💰\n"
            bot.send_message(chat_id, txt, reply_markup=main_menu(uid)); return
        if d == "tasks":
            m = InlineKeyboardMarkup(); bonus = sum([WEAPONS[w]["bonus"] for w in u.get("weapons",[]) if w in WEAPONS])
            for i, t in enumerate(TASKS):
                m.add(InlineKeyboardButton(f"{t['name']} = +{t['reward'] + bonus}", callback_data=f"task_{i}"))
            m.add(InlineKeyboardButton("🔙 رجوع", callback_data="back"))
            bot.send_message(chat_id, f"📋 اختار مهمة - قوتك +{bonus}:", reply_markup=m); return
        if d.startswith("task_"):
            idx = int(d.split("_")[1]); task = TASKS[idx]; bonus = sum([WEAPONS[w]["bonus"] for w in u.get("weapons",[]) if w in WEAPONS]); total = task["reward"] + bonus
            if idx == 0:
                m = InlineKeyboardMarkup(row_width=2); m.add(InlineKeyboardButton("3", callback_data="ans_wrong"), InlineKeyboardButton("4 ✅", callback_data="ans_right"), InlineKeyboardButton("5", callback_data="ans_wrong"), InlineKeyboardButton("6", callback_data="ans_wrong"))
                bot.send_message(chat_id, "سؤال: كام 2 + 2 ؟", reply_markup=m)
            elif idx == 3:
                m = InlineKeyboardMarkup(row_width=2); m.add(InlineKeyboardButton("🍎 تفاحة", callback_data="mem_wrong"), InlineKeyboardButton("🍌 موز", callback_data="mem_right"), InlineKeyboardButton("🍇 عنب", callback_data="mem_wrong"), InlineKeyboardButton("🍓 فراولة", callback_data="mem_wrong"))
                bot.send_message(chat_id, "فاكر؟ انا قولت موز 🍌 اختار موز:", reply_markup=m)
            else:
                got = add_money(uid, total); bot.send_message(chat_id, f"عااش 🔥 خدت +{got}\n💰 بقى معاك: {u['money']}", reply_markup=main_menu(uid))
            return
        if d == "ans_right":
            bonus = sum([WEAPONS[w]["bonus"] for w in u.get("weapons",[]) if w in WEAPONS]); got = add_money(uid, 20 + bonus); bot.send_message(chat_id, f"صح ✅ خدت +{got}\n💰 بقى معاك: {u['money']}", reply_markup=main_menu(uid)); return
        if d == "ans_wrong":
            bot.send_message(chat_id, "غلط 😅 جرب تاني", reply_markup=main_menu(uid)); return
        if d == "mem_right":
            bonus = sum([WEAPONS[w]["bonus"] for w in u.get("weapons",[]) if w in WEAPONS]); got = add_money(uid, 40 + bonus); bot.send_message(chat_id, f"صح ✅ خدت +{got}\n💰 بقى معاك: {u['money']}", reply_markup=main_menu(uid)); return
        if d == "mem_wrong":
            bot.send_message(chat_id, "غلط 😅 دي مش موز!", reply_markup=main_menu(uid)); return
        if d == "daily":
            now = int(time.time())
            if now - u.get("daily", 0) < 5:
                bot.send_message(chat_id, "استنى شوية 😅", reply_markup=main_menu(uid))
            else:
                u["streak"] = u.get("streak",0) + 1; base = 100 if is_vip(u) else 10; reward = base + (u["streak"] * 2); got = add_money(uid, reward); u["daily"] = now; save_data()
                bot.send_message(chat_id, f"🎁 يومية +{got}\n🔥 سلسلة: {u['streak']}\n💰 بقى معاك: {u['money']}", reply_markup=main_menu(uid))
            return
        if d == "gift":
            now = int(time.time())
            if now - u.get("gift", 0) < 10:
                bot.send_message(chat_id, "استنى 10 ثواني 😅", reply_markup=main_menu(uid))
            else:
                reward = 200 if is_vip(u) else random.choice([5,10,15,20,50,100]); got = add_money(uid, reward); u["gift"] = now; save_data()
                bot.send_message(chat_id, f"🎁 فتحت صندوق! +{got}\n💰 بقى معاك: {u['money']}", reply_markup=main_menu(uid))
            return
        if d == "spin":
            now = int(time.time())
            if now - u.get("spin", 0) < 10:
                bot.send_message(chat_id, "عجلة الحظ كل 10 ثواني 😅", reply_markup=main_menu(uid))
            else:
                reward = random.choice([0,5,10,20,30,50,100,200]); u["spin"] = now
                if reward == 0:
                    save_data(); bot.send_message(chat_id, "😢 صفر جرب تاني", reply_markup=main_menu(uid))
                else:
                    got = add_money(uid, reward); save_data(); bot.send_message(chat_id, f"🎡 عجلة الحظ +{got} 🔥\n💰 بقى معاك: {u['money']}", reply_markup=main_menu(uid))
            return
        if d == "gamble":
            m = InlineKeyboardMarkup(row_width=2); m.add(InlineKeyboardButton("🪙 ملك - 20", callback_data="gamble_king"), InlineKeyboardButton("🪙 كتابة - 20", callback_data="gamble_write")); m.add(InlineKeyboardButton("🔙 رجوع", callback_data="back"))
            bot.send_message(chat_id, f"🎲 معاك {u['money']}\nلو كسبت تاخد 40:", reply_markup=m); return
        if d.startswith("gamble_"):
            if u["money"] < 20:
                bot.send_message(chat_id, "فلوسك مش كفاية 😢", reply_markup=main_menu(uid)); return
            u["money"] -= 20; win = random.choice([True, False])
            if win:
                u["money"] += 40; save_data(); bot.send_message(chat_id, f"🎉 كسبت! +40\n💰 بقى معاك: {u['money']}", reply_markup=main_menu(uid))
            else:
                save_data(); bot.send_message(chat_id, f"😢 خسرت 20\n💰 فاضل: {u['money']}", reply_markup=main_menu(uid))
            return
        if d == "code":
            m = InlineKeyboardMarkup(row_width=2); m.add(InlineKeyboardButton("WELCOME100", callback_data="code_WELCOME100"), InlineKeyboardButton("MEGA500", callback_data="code_MEGA500"), InlineKeyboardButton("BOSS1000", callback_data="code_BOSS1000")); m.add(InlineKeyboardButton("🔙 رجوع", callback_data="back"))
            bot.send_message(chat_id, "🎁 اختار كود:", reply_markup=m); return
        if d.startswith("code_"):
            code = d.replace("code_", ""); used = u.get("used_codes", [])
            if code in used:
                bot.send_message(chat_id, "استخدمته قبل كده 😅", reply_markup=main_menu(uid)); return
            used.append(code); u["used_codes"] = used; got = add_money(uid, GIFT_CODES[code])
            bot.send_message(chat_id, f"🎉 الكود صح! +{got}\n💰 بقى معاك: {u['money']}", reply_markup=main_menu(uid)); return
        if d == "store":
            m = InlineKeyboardMarkup()
            for k, item in STORE.items():
                m.add(InlineKeyboardButton(f"{item['name']} - {item['price']}", callback_data=f"buy_{k}"))
            m.add(InlineKeyboardButton("🔙 رجوع", callback_data="back"))
            bot.send_message(chat_id, f"🛒 معاك {u['money']}", reply_markup=m); return
        if d.startswith("buy_"):
            k = d.split("_")[1]; item = STORE[k]
            if k == "5":
                bot.send_message(chat_id, "ده VIP - دوس على زرار 👑 VIP", reply_markup=main_menu(uid)); return
            if u["money"] >= item["price"]:
                u["money"] -= item["price"]; save_data(); bot.send_message(chat_id, f"مبرووك 🎉 اشتريت {item['name']}\n💰 فاضل: {u['money']}", reply_markup=main_menu(uid))
            else:
                bot.send_message(chat_id, f"فلوسك مش كفاية 😢", reply_markup=main_menu(uid))
            return
        if d == "invite":
            link = f"https://t.me/{bot.get_me().username}?start={uid}"; bot.send_message(chat_id, f"👥 ابعت لصاحبك:\n{link}\n\nلو دخل هتاخد +50", reply_markup=main_menu(uid)); return
        if d == "owner":
            if not is_owner(uid):
                bot.send_message(chat_id, "انت مش الاونر ❌"); return
            m = InlineKeyboardMarkup(); m.add(InlineKeyboardButton("👥 المستخدمين", callback_data="admin_users")); m.add(InlineKeyboardButton("📢 رسالة للكل", callback_data="admin_broadcast")); m.add(InlineKeyboardButton("🏆 انهي المسابقة", callback_data="admin_end_contest")); m.add(InlineKeyboardButton("🔙 رجوع", callback_data="back"))
            bot.send_message(chat_id, f"👑 لوحة الاونر\n👥 {len(data)} مستخدم\n💰 اجمالي: {sum(v.get('money',0) for v in data.values())}", reply_markup=m); return
        if d == "admin_end_contest":
            if not is_owner(uid): return
            if len(data)==0:
                bot.send_message(chat_id, "مفيش حد", reply_markup=main_menu(uid)); return
            winner = max(data.items(), key=lambda x: x[1].get('contest_score',0)); wid, winfo = winner
            winfo["money"] += 500; winfo["contest_score"] = 0; save_data()
            for uid2 in list(data.keys()):
                if uid2 != wid: data[uid2]["contest_score"] = 0
            save_data()
            try: bot.send_message(int(wid), "🏆 مبرووك كسبت المسابقة! +500")
            except: pass
            bot.send_message(chat_id, f"🏆 المسابقة خلصت!\nالفايز: {winfo.get('name')} +500", reply_markup=main_menu(uid)); return
        if d == "admin_users":
            if not is_owner(uid): return
            m = InlineKeyboardMarkup()
            for user_id, info in list(data.items())[:20]:
                m.add(InlineKeyboardButton(f"{info.get('name','?')} - {info.get('money',0)} 💰", callback_data=f"admin_user_{user_id}"))
            m.add(InlineKeyboardButton("🔙 رجوع", callback_data="owner"))
            bot.send_message(chat_id, "دوس على واحد:", reply_markup=m); return
        if d.startswith("admin_user_"):
            if not is_owner(uid): return
            target = d.replace("admin_user_", ""); info = get_user(int(target))
            m = InlineKeyboardMarkup(row_width=3); m.add(InlineKeyboardButton("➕ 10", callback_data=f"add_{target}_10"), InlineKeyboardButton("➕ 50", callback_data=f"add_{target}_50"), InlineKeyboardButton("➕ 100", callback_data=f"add_{target}_100"), InlineKeyboardButton("➕ 1000", callback_data=f"add_{target}_1000"), InlineKeyboardButton("➖ 50", callback_data=f"sub_{target}_50"), InlineKeyboardButton("➖ 100", callback_data=f"sub_{target}_100"))
            m.add(InlineKeyboardButton("👑 اديله VIP", callback_data=f"givevip_{target}")); m.add(InlineKeyboardButton("🔙 رجوع", callback_data="admin_users"))
            bot.send_message(chat_id, f"👤 {info.get('name')}\nID: {target}\n💰 معاه: {info['money']}\nVIP: {'✅' if is_vip(info) else '❌'}", reply_markup=m); return
        if d.startswith("givevip_"):
            if not is_owner(uid): return
            target = d.replace("givevip_", ""); info = get_user(int(target)); info["vip"] = True; save_data()
            bot.send_message(chat_id, f"تم ✅ {info.get('name')} بقى VIP 👑", reply_markup=main_menu(uid)); return
        if d.startswith("add_") or d.startswith("sub_"):
            if not is_owner(uid): return
            _, target, amount = d.split("_"); amount = int(amount); info = get_user(int(target))
            if d.startswith("add_"): info["money"] += amount
            else: info["money"] = max(0, info["money"] - amount)
            save_data()
            m = InlineKeyboardMarkup(); m.add(InlineKeyboardButton("🔙 رجوع", callback_data="admin_users"))
            bot.send_message(chat_id, f"تم ✅\n💰 بقى معاه: {info['money']}", reply_markup=m); return
        if d == "admin_broadcast":
            if not is_owner(uid): return
            m = InlineKeyboardMarkup(row_width=2); m.add(InlineKeyboardButton("🎉 مسابقة جديدة!", callback_data="bc_1"), InlineKeyboardButton("🔥 خصم!", callback_data="bc_2"), InlineKeyboardButton("👋 ارجع العب", callback_data="bc_3")); m.add(InlineKeyboardButton("🔙 رجوع", callback_data="owner"))
            bot.send_message(chat_id, "اختار رسالة:", reply_markup=m); return
        if d.startswith("bc_"):
            if not is_owner(uid): return
            texts = {"bc_1": "🎉 فيه مسابقة جديدة! ادخل البوت وخد فلوس", "bc_2": "🔥 خصم في المتجر! الحق اشتري", "bc_3": "👋 ارجع العب وخد فلوس"}
            count = 0
            for user_id in list(data.keys()):
                try: bot.send_message(int(user_id), f"📢 من الاونر:\n\n{texts[d]}"); count += 1
                except: pass
            bot.send_message(chat_id, f"تم ✅ بعت لـ {count} واحد", reply_markup=main_menu(uid)); return
    except Exception as e:
        print("Button error:", e, traceback.format_exc())
        try: bot.send_message(chat_id, "حصل مشكلة صغيرة 😅 دوس تاني", reply_markup=main_menu(uid))
        except: pass

# --- تشغيل مستمر - لو وقع يقوم لوحده ---
print("Bot is starting...")
while True:
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60, skip_pending=True)
    except Exception as e:
        print("Polling crashed, restarting in 5 sec:", e)
        time.sleep(5)
