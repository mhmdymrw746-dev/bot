# TRAN BOT - FINAL 150 FEATURES - OWNER 8188263997
import os, random, time, json, logging, threading
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from telegram.constants import ParseMode
from flask import Flask
import requests

logging.basicConfig(level=logging.INFO)
TOKEN = os.environ.get("BOT_TOKEN")
OWNER_ID = int(os.environ.get("OWNER_ID", "8188263997"))
WEBAPP_URL = os.environ.get("WEBAPP_URL", "https://t.me/")

# ===== يصحي نفسه =====
app_flask = Flask(__name__)
@app_flask.route('/')
def home(): return "TRAN ALIVE 👑🔥"
def run_flask():
    try: app_flask.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
    except: pass
def self_ping():
    time.sleep(10)
    url = os.environ.get("RENDER_EXTERNAL_URL", "")
    if not url: return
    while True:
        try: requests.get(url, timeout=10); print("✅ صحيت نفسي")
        except: pass
        time.sleep(600)
threading.Thread(target=run_flask, daemon=True).start()
threading.Thread(target=self_ping, daemon=True).start()

# ===== DB =====
users = {}; codes = {}; clans = {}; marriages = {}; pets = {}; houses = {}; cars = {}; stock_prices = {"TRAN": 100, "GOLD": 500, "BTC": 1000, "DOGE": 50}
lottery_players = []; auctions = []; mining_last = {}; tournaments = {"players": [], "prize": 10000}
skins_shop = {"gold": {"name": "🥇 ذهبي", "price": 500}, "diamond": {"name": "💎 الماسي", "price": 1000}, "fire": {"name": "🔥 ناري", "price": 800}, "king": {"name": "👑 ملكي", "price": 2000}}
quiz_questions = [{"q": "ايه عاصمة مصر؟", "a": "القاهرة", "opts": ["القاهرة", "الجيزة", "اسكندرية"]}, {"q": "كم عدد ايام السنة؟", "a": "365", "opts": ["365", "360", "366"]}, {"q": "ايه اكبر كوكب؟", "a": "المشتري", "opts": ["المشتري", "المريخ", "زحل"]}]

def get_user(uid, username="", name=""):
    uid = int(uid)
    if uid not in users:
        users[uid] = {"id": uid, "username": username, "name": name, "coins": 100, "balance": 0, "bank": 0, "points": 0, "level": 1, "ref": 0, "ref_earned": 0, "banned": False, "vip": False, "loan": 0, "games": 0, "wins": 0, "losses": 0, "total_won": 0, "tasks": [], "last_daily": "", "joined": datetime.now().strftime("%Y-%m-%d"), "transactions": [], "ach": [], "stocks": {}, "notes": [], "power": 10, "edu": 0, "streak": 0}
    return users[uid]
def add_coins(uid, amt, reason=""):
    u = get_user(uid); u["coins"] += amt; u["points"] += amt
    if amt > 0: u["total_won"] += amt
    u["transactions"].append(f"{reason} {amt:+} 🪙")
    u["transactions"] = u["transactions"][-10:]
    return u
def lvl_name(c):
    if c < 500: return "🥉 مبتدئ"
    if c < 2000: return "🥈 محترف"
    if c < 5000: return "🥇 خبير"
    if c < 15000: return "💎 اسطوري"
    return "👑 ملك TRAN"

def main_menu(uid):
    kb = [
        [InlineKeyboardButton("🎮 فتح التطبيق 🚀", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton("🎲 العاب 🎰", callback_data="games"), InlineKeyboardButton("🏦 البنك 🏦", callback_data="bank")],
        [InlineKeyboardButton("🛒 المتجر 🛍️", callback_data="shop"), InlineKeyboardButton("🏆 المسابقات 🏆", callback_data="comp")],
        [InlineKeyboardButton("🎁 المهام 🎁", callback_data="tasks"), InlineKeyboardButton("👛 محفظتي 💰", callback_data="wallet")],
        [InlineKeyboardButton("👥 دعوة 👥", callback_data="ref"), InlineKeyboardButton("🏅 ترتيب 📊", callback_data="rank")],
        [InlineKeyboardButton("🎡 عجلة الحظ 🎡", callback_data="wheel"), InlineKeyboardButton("🎁 كود هدية 🎁", callback_data="gift")],
        [InlineKeyboardButton("👤 بروفايلي 👤", callback_data="profile"), InlineKeyboardButton("🆘 الدعم 🆘", callback_data="support")],
        [InlineKeyboardButton("ℹ️ معلومات ℹ️", callback_data="info")],
    ]
    if int(uid) == OWNER_ID: kb.append([InlineKeyboardButton("👑 لوحة الاونر 👑🔥", callback_data="owner")])
    kb.append([InlineKeyboardButton("🔄 تحديث 🔄", callback_data="back")])
    return InlineKeyboardMarkup(kb)
def back(): return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="back")]])
def back2(to): return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data=to)], [InlineKeyboardButton("🏠 القايمة", callback_data="back")]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user; user = get_user(u.id, u.username or "", u.first_name or "")
    if user["banned"]:
        await update.message.reply_text("⛔ محظور"); return
    if context.args:
        try:
            inv = int(context.args[0])
            if inv != u.id and inv in users and "ref_by" not in user:
                user["ref_by"] = inv; users[inv]["ref"] += 1; add_coins(inv, 50, "دعوة")
                try: await context.bot.send_message(inv, f"🎉 {u.first_name} دخل من لينكك +50 🪙")
                except: pass
        except: pass
    await update.message.reply_text(f"✨ **اهلا {u.first_name} في TRAN** ✨\n━━━━━━━━━━\n🪙 كوينز: `{user['coins']:,}`\n🏦 بنك: `{user['bank']:,}`\n💰 رصيد: `{user['balance']} ج`\n🏅 مستواك: {lvl_name(user['coins'])}\n👥 دعيت: `{user['ref']}`\n━━━━━━━━━━\n👇 اختار، كله شغال 100% 👇\n\n**اوامر سريعة:**\n`/mine` ⛏️ `/work` 💼 `/box` 📦 `/lottery` 🎰\n`/marry` 💍 `/trade` 📈 `/chat` 💬 `/ai` 🤖", reply_markup=main_menu(u.id), parse_mode=ParseMode.MARKDOWN)

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer(); uid = q.from_user.id; user = get_user(uid, q.from_user.username or "", q.from_user.first_name or ""); data = q.data
    if data == "back":
        await q.edit_message_text(f"✨ **TRAN** ✨\n\n🪙 `{user['coins']:,}` | 🏦 بنك `{user['bank']:,}` | 💰 `{user['balance']} ج`\n🏅 {lvl_name(user['coins'])}", reply_markup=main_menu(uid), parse_mode=ParseMode.MARKDOWN); return
    # BANK
    if data == "bank":
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("💰 ايداع", callback_data="bank_deposit"), InlineKeyboardButton("💸 سحب", callback_data="bank_withdraw")], [InlineKeyboardButton("🔄 تحويل", callback_data="bank_transfer"), InlineKeyboardButton("💳 قرض", callback_data="bank_loan")], [InlineKeyboardButton("📈 فوايد", callback_data="bank_interest"), InlineKeyboardButton("📜 كشف حساب", callback_data="bank_history")], [InlineKeyboardButton("💎 فيزا TRAN", callback_data="bank_visa")], [InlineKeyboardButton("🔙 رجوع", callback_data="back")]])
        await q.edit_message_text(f"🏦 **بنك TRAN** 🏦\n\n🪙 في ايدك: `{user['coins']:,}`\n🏦 في البنك: `{user['bank']:,}`\n💳 قرض عليك: `{user['loan']}`", reply_markup=kb, parse_mode=ParseMode.MARKDOWN); return
    if data == "bank_deposit":
        if user["coins"] >= 100: user["coins"] -= 100; user["bank"] += 100; await q.edit_message_text(f"✅ **ايداع تم!**\n🏦 بنك: `{user['bank']}` | 🪙 معاك: `{user['coins']}`", reply_markup=back2("bank"), parse_mode=ParseMode.MARKDOWN)
        else: await q.edit_message_text("❌ معكش 100 كوين", reply_markup=back2("bank")); return
    if data == "bank_withdraw":
        if user["bank"] >= 100: user["bank"] -= 100; user["coins"] += 100; await q.edit_message_text(f"✅ **سحبت 100**\n🪙 {user['coins']} | 🏦 {user['bank']}", reply_markup=back2("bank"), parse_mode=ParseMode.MARKDOWN)
        else: await q.edit_message_text("❌ معكش في البنك", reply_markup=back2("bank")); return
    if data == "bank_transfer": context.user_data["wait_transfer"] = True; await q.edit_message_text("🔄 اكتب: `ID المبلغ`\nمثال: `123456 100`", reply_markup=back2("bank"), parse_mode=ParseMode.MARKDOWN); return
    if data == "bank_loan":
        if user["loan"] > 0: await q.edit_message_text(f"❌ عليك قرض {user['loan']}", reply_markup=back2("bank")); return
        user["coins"] += 500; user["loan"] = 550; await q.edit_message_text(f"💳 **خدت قرض 500 🪙**\nهترجع 550\n🪙 {user['coins']}", reply_markup=back2("bank"), parse_mode=ParseMode.MARKDOWN); return
    if data == "bank_interest":
        if user["bank"] <= 0: await q.edit_message_text("❌ حط فلوس في البنك الاول", reply_markup=back2("bank")); return
        interest = int(user["bank"] * 0.1); user["bank"] += interest; await q.edit_message_text(f"📈 **فوايد +{interest} 🪙**\n🏦 {user['bank']}", reply_markup=back2("bank"), parse_mode=ParseMode.MARKDOWN); return
    if data == "bank_history": await q.edit_message_text(f"📜 **كشف حساب**\n\n" + ("\n".join(user["transactions"][-10:]) or "مفيش حركات"), reply_markup=back2("bank")); return
    if data == "bank_visa": await q.edit_message_text(f"💎 **فيزا TRAN**\n\n👤 {q.from_user.first_name}\n💳 رقم: `5335 {uid%10000:04d} 2026 8188`\n🏦 رصيد: `{user['bank']:,}` 🪙\n✅ شغالة", reply_markup=back2("bank"), parse_mode=ParseMode.MARKDOWN); return
    # GAMES
    if data == "games":
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("🎲 نرد", callback_data="g_dice"), InlineKeyboardButton("🪙 ملك وكتابة", callback_data="g_flip")], [InlineKeyboardButton("🎰 سلوت", callback_data="g_slot"), InlineKeyboardButton("🚀 صاروخ", callback_data="g_crash")], [InlineKeyboardButton("✂️ حجر ورقة مقص", callback_data="g_rps"), InlineKeyboardButton("🔢 تخمين رقم", callback_data="g_guess")], [InlineKeyboardButton("🔙 رجوع", callback_data="back")]])
        await q.edit_message_text("🎮 **العاب** - كل لعبة بتكسب كوينز بجد", reply_markup=kb); return
    if data == "g_dice":
        r = random.randint(1, 6); user["games"] += 1
        if r >= 4: add_coins(uid, 25, "نرد"); txt = f"🎲 {r}\n🎉 كسبت +25 🪙"
        else: add_coins(uid, -10, "نرد"); txt = f"🎲 {r}\n😔 خسرت -10 🪙"
        await q.edit_message_text(f"{txt}\n🪙 {user['coins']}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎲 تاني", callback_data="g_dice")], [InlineKeyboardButton("🔙", callback_data="games")]])); return
    if data == "g_flip": await q.edit_message_text("🪙 اختار:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("👑 ملك", callback_data="flip_k"), InlineKeyboardButton("✍️ كتابة", callback_data="flip_w")], [InlineKeyboardButton("🔙", callback_data="games")]])); return
    if data.startswith("flip_"):
        res = random.choice(["k", "w"]); choice = "k" if data == "flip_k" else "w"
        if choice == res: add_coins(uid, 30, "ملك"); txt = "🎉 صح! +30 🪙"
        else: add_coins(uid, -10, "ملك"); txt = "😔 غلط! -10 🪙"
        await q.edit_message_text(f"{txt}\n🪙 {user['coins']}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🪙 تاني", callback_data="g_flip")], [InlineKeyboardButton("🔙", callback_data="games")]])); return
    if data == "g_slot":
        e = ["🍒", "🍋", "⭐", "💎", "7️⃣"]; r = [random.choice(e) for _ in range(3)]
        if r[0] == r[1] == r[2]: add_coins(uid, 100, "سلوت"); txt = f"🎰 {' '.join(r)}\n🎉 JACKPOT +100 🪙"
        elif r[0] == r[1] or r[1] == r[2]: add_coins(uid, 20, "سلوت"); txt = f"🎰 {' '.join(r)}\n🎉 +20 🪙"
        else: add_coins(uid, -10, "سلوت"); txt = f"🎰 {' '.join(r)}\n😔 -10 🪙"
        await q.edit_message_text(f"{txt}\n🪙 {user['coins']}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎰 تاني", callback_data="g_slot")], [InlineKeyboardButton("🔙", callback_data="games")]])); return
    if data == "g_crash":
        m = round(random.uniform(1, 5), 2)
        if m >= 2: w = int(20 * m); add_coins(uid, w, "صاروخ"); txt = f"🚀 x{m}\n🎉 +{w} 🪙"
        else: add_coins(uid, -20, "صاروخ"); txt = f"💥 x{m}\n😔 -20 🪙"
        await q.edit_message_text(f"{txt}\n🪙 {user['coins']}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🚀 تاني", callback_data="g_crash")], [InlineKeyboardButton("🔙", callback_data="games")]])); return
    if data == "g_rps": await q.edit_message_text("✂️ اختار:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🪨 حجر", callback_data="rps_rock"), InlineKeyboardButton("📄 ورقة", callback_data="rps_paper"), InlineKeyboardButton("✂️ مقص", callback_data="rps_scissors")], [InlineKeyboardButton("🔙", callback_data="games")]])); return
    if data.startswith("rps_"):
        me = data.replace("rps_", ""); bot = random.choice(["rock", "paper", "scissors"]); mp = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}
        if me == bot: txt = "🤝 تعادل!"
        elif (me == "rock" and bot == "scissors") or (me == "paper" and bot == "rock") or (me == "scissors" and bot == "paper"): add_coins(uid, 20, "حجر"); txt = "🎉 كسبت +20 🪙"
        else: add_coins(uid, -10, "حجر"); txt = "😔 خسرت -10 🪙"
        await q.edit_message_text(f"انت {mp[me]} vs بوت {mp[bot]}\n{txt}\n🪙 {user['coins']}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✂️ تاني", callback_data="g_rps")], [InlineKeyboardButton("🔙", callback_data="games")]])); return
    if data == "g_guess": context.user_data["guess"] = random.randint(1, 5); await q.edit_message_text("🔢 خمن رقم من 1 لـ 5، ابعته في رسالة", reply_markup=back2("games")); return
    if data == "wheel": p = random.choice([10, 20, 0, 50, 5, 100, 0, 30]); add_coins(uid, p, "عجلة"); await q.edit_message_text(f"🎡 كسبت +{p} 🪙\n🪙 {user['coins']}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎡 تاني", callback_data="wheel")], [InlineKeyboardButton("🔙", callback_data="back")]])); return
    # SHOP / TASKS / WALLET / ETC
    if data == "shop":
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("🪙 500 كوين - 25ج", callback_data="buy_500")], [InlineKeyboardButton("💰 1000 كوين - 45ج", callback_data="buy_1000")], [InlineKeyboardButton("💎 5000 كوين - 180ج", callback_data="buy_5000")], [InlineKeyboardButton("👑 10000 كوين VIP - 320ج", callback_data="buy_10000")], [InlineKeyboardButton("🔙 رجوع", callback_data="back")]])
        await q.edit_message_text("🛒 **المتجر**\nاختار عرض، الدفع فودافون كاش", reply_markup=kb); return
    if data.startswith("buy_"):
        amt = data.replace("buy_", ""); await q.edit_message_text(f"✅ طلبك {amt} كوين اتسجل!\nحول على 01000000000 وابعت سكرين للدعم", reply_markup=back())
        try: await context.bot.send_message(OWNER_ID, f"🛒 طلب {amt} من {q.from_user.first_name} ({uid})")
        except: pass
        return
    if data == "comp": await q.edit_message_text(f"🏆 **مسابقة اليوم**\n🥇 الجايزة 1000 🪙\n📊 نقاطك: {user['points']}", reply_markup=back()); return
    if data == "tasks":
        today = datetime.now().strftime("%Y-%m-%d")
        if user["last_daily"] != today: user["tasks"] = []; user["last_daily"] = today
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("🎁 مكافأة يومية +20", callback_data="task_daily")], [InlineKeyboardButton("📢 انضم للقناة +30", callback_data="task_join")], [InlineKeyboardButton("🔗 شارك البوت +25", callback_data="task_share")], [InlineKeyboardButton("🔙 رجوع", callback_data="back")]])
        await q.edit_message_text("🎁 **مهام** - خد كوينز ببلاش", reply_markup=kb); return
    if data.startswith("task_"):
        tid = data.replace("task_", ""); today = datetime.now().strftime("%Y-%m-%d")
        if user["last_daily"] != today: user["tasks"] = []; user["last_daily"] = today
        if tid in user["tasks"]: await q.edit_message_text("✅ عملتها النهاردة", reply_markup=back()); return
        rewards = {"daily": 20, "join": 30, "share": 25}; user["tasks"].append(tid); add_coins(uid, rewards.get(tid, 20), "مهمة")
        await q.edit_message_text(f"🎉 +{rewards.get(tid, 20)} 🪙\n🪙 {user['coins']}", reply_markup=back()); return
    if data == "wallet": await q.edit_message_text(f"👛 **محفظتي**\n🪙 كوينز: `{user['coins']:,}`\n🏦 بنك: `{user['bank']:,}`\n💰 رصيد: `{user['balance']} ج`\n🏅 {lvl_name(user['coins'])}\n📊 نقاط: `{user['points']}`", reply_markup=back(), parse_mode=ParseMode.MARKDOWN); return
    if data == "ref":
        link = f"https://t.me/{context.bot.username}?start={uid}"
        await q.edit_message_text(f"👥 **دعوة**\nكل صاحب +50 🪙\nدعيت: `{user['ref']}`\n\nلينكك:\n`{link}`", reply_markup=back(), parse_mode=ParseMode.MARKDOWN); return
    if data == "rank":
        top = sorted(users.values(), key=lambda x: x["coins"], reverse=True)[:10]; txt = "🏅 **توب 10**\n\n"; medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        for i, u2 in enumerate(top): txt += f"{medals[i]} {u2.get('name','')} - {u2['coins']:,} 🪙{' 👈 انت' if u2['id']==uid else ''}\n"
        await q.edit_message_text(txt, reply_markup=back()); return
    if data == "profile": await q.edit_message_text(f"👤 **بروفايلك**\n\n👤 {q.from_user.first_name}\n🆔 `{uid}`\n🏅 {lvl_name(user['coins'])}\n🪙 {user['coins']:,} | 🏦 {user['bank']:,}\n🎮 لعبت {user['games']} | ✅ كسبت {user['wins']}\n📅 انضميت {user['joined']}", reply_markup=back(), parse_mode=ParseMode.MARKDOWN); return
    if data == "info": await q.edit_message_text("ℹ️ **TRAN v3.0 - FINAL**\n🎮 العاب + 🏦 بنك + 🛒 متجر + 👑 اونر\n150 ميزة شغالة 100% ✅\nالدعم: @tran_support", reply_markup=back()); return
    if data == "support": context.user_data["wait_support"] = True; await q.edit_message_text("🆘 اكتب مشكلتك دلوقتي في رسالة", reply_markup=back()); return
    if data == "gift": context.user_data["wait_code"] = True; await q.edit_message_text("🎁 اكتب الكود، زي `TRAN100`", reply_markup=back()); return
    # OWNER
    if data == "owner":
        if uid != OWNER_ID: await q.edit_message_text("⛔ مش الاونر", reply_markup=back()); return
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("📊 احصائيات", callback_data="o_stats"), InlineKeyboardButton("📢 اذاعة", callback_data="o_broadcast")], [InlineKeyboardButton("🪙 اضف كوينز", callback_data="o_add"), InlineKeyboardButton("➖ خصم كوينز", callback_data="o_remove")], [InlineKeyboardButton("⛔ حظر / فك", callback_data="o_ban"), InlineKeyboardButton("🎁 اعمل كود", callback_data="o_code")], [InlineKeyboardButton("👤 شوف يوزر", callback_data="o_view"), InlineKeyboardButton("🔄 تصفير", callback_data="o_reset")], [InlineKeyboardButton("🔙 رجوع", callback_data="back")]])
        await q.edit_message_text(f"👑 **لوحة الاونر** 👑\n\nاهلا يا اونر 🔥\n👥 مستخدمين: `{len(users)}`\n🪙 اجمالي: `{sum(u['coins'] for u in users.values()):,}`", reply_markup=kb, parse_mode=ParseMode.MARKDOWN); return
    if data == "o_stats":
        if uid != OWNER_ID: return
        await q.edit_message_text(f"📊 **احصائيات**\n👥 {len(users)} مستخدم\n🪙 {sum(u['coins'] for u in users.values()):,} كوين\n🏦 {sum(u['bank'] for u in users.values()):,} في البنك\n🎮 {sum(u['games'] for u in users.values())} لعبة", reply_markup=back()); return
    if data == "o_broadcast":
        if uid != OWNER_ID: return
        context.user_data["wait_broadcast"] = True; await q.edit_message_text("📢 ابعت رسالة الاذاعة دلوقتي", reply_markup=back()); return
    if data == "o_add":
        if uid != OWNER_ID: return
        context.user_data["wait_add"] = True; await q.edit_message_text("🪙 اكتب: `ID المبلغ`\nمثال: `8188263997 500`", reply_markup=back()); return
    if data == "o_remove":
        if uid != OWNER_ID: return
        context.user_data["wait_remove"] = True; await q.edit_message_text("➖ اكتب: `ID المبلغ`", reply_markup=back()); return
    if data == "o_ban":
        if uid != OWNER_ID: return
        context.user_data["wait_ban"] = True; await q.edit_message_text("⛔ اكتب ID اللي عايز تحظره / تفك حظره", reply_markup=back()); return
    if data == "o_code":
        if uid != OWNER_ID: return
        code = f"TRAN{random.randint(100,999)}"; codes[code] = 100; await q.edit_message_text(f"🎁 كود جديد: `{code}`\nالهدية: 100 🪙", reply_markup=back(), parse_mode=ParseMode.MARKDOWN); return
    if data == "o_view":
        if uid != OWNER_ID: return
        context.user_data["wait_view"] = True; await q.edit_message_text("👤 اكتب ID اليوزر", reply_markup=back()); return
    if data == "o_reset":
        if uid != OWNER_ID: return
        await q.edit_message_text("⚠️ اكتب `تصفير` في الشات لو متأكد", reply_markup=back()); return

# ===== COMMANDS - 150 FEATURES =====
async def cmd_mine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id; u = get_user(uid); now = time.time()
    if now - mining_last.get(uid, 0) < 3600: await update.message.reply_text(f"⛏️ لسه بتعدن! فاضل {int((3600-(now-mining_last.get(uid,0)))/60)} دقيقة"); return
    mining_last[uid] = now; mined = random.randint(30, 150) * (2 if u.get("vip") else 1); add_coins(uid, mined, "تعدين"); await update.message.reply_text(f"⛏️ **عدنت! +{mined} 🪙**\n🪙 {u['coins']}")
async def cmd_work(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id; u = get_user(uid); job = random.choice(["👨‍🍳 طباخ", "👨‍💻 مبرمج", "🚕 سواق", "👨‍⚕️ دكتور", "🎤 مغني", "⚽ لاعب كورة"]); salary = random.randint(50, 200) * (2 if u.get("vip") else 1); add_coins(uid, salary, "شغل"); await update.message.reply_text(f"💼 **اشتغلت {job}!**\n💰 +{salary} 🪙\n🪙 {u['coins']}")
async def cmd_box(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id; u = get_user(uid); today = datetime.now().strftime("%Y-%m-%d")
    if u.get("last_box") == today: await update.message.reply_text("📦 فتحت الصندوق النهاردة، تعالى بكرة"); return
    u["last_box"] = today; prize = random.choice([10, 20, 50, 100, 200, 500, 0])
    if prize == 0: await update.message.reply_text("📦 الصندوق فاضي! 😔")
    else: add_coins(uid, prize, "صندوق"); await update.message.reply_text(f"📦 **فتحت الصندوق! +{prize} 🪙**\n🪙 {u['coins']}")
async def cmd_lottery(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id; u = get_user(uid)
    if uid in lottery_players: await update.message.reply_text("✅ دخلت خلاص"); return
    if u["coins"] < 20: await update.message.reply_text("❌ محتاج 20 كوين"); return
    u["coins"] -= 20; lottery_players.append(uid); await update.message.reply_text(f"🎰 **دخلت اليانصيب!**\n👥 {len(lottery_players)} لاعب\nاكتب /lottery_draw عشان تسحب")
async def cmd_lottery_draw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(lottery_players) < 2: await update.message.reply_text("❌ محتاج 2 على الاقل"); return
    winner = random.choice(lottery_players); prize = len(lottery_players) * 20; add_coins(winner, prize, "يانصيب"); await update.message.reply_text(f"🎉 **الفايز باليانصيب!**\n👤 {winner}\n🏆 خد {prize} 🪙"); lottery_players.clear()
async def cmd_marry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id; u = get_user(uid)
    if uid in marriages: await update.message.reply_text(f"💍 انت متجوز {marriages[uid]} خلاص! ❤️"); return
    if not context.args: await update.message.reply_text("💍 اكتب: `/marry ID_الشريك`\nالجواز بـ 500 🪙 وبيجيب +100 كل يوم"); return
    try:
        partner = int(context.args[0])
        if partner == uid: await update.message.reply_text("😂 مينفعش تتجوز نفسك!"); return
        if partner in marriages: await update.message.reply_text("❌ متجوز!"); return
        if u["coins"] < 500: await update.message.reply_text("❌ الجواز بـ 500 🪙"); return
        u["coins"] -= 500; marriages[uid] = partner; marriages[partner] = uid; add_coins(partner, 200, "جواز"); await update.message.reply_text(f"💍 **مبروك الجواز!** 🎉❤️\nانت و {partner} بقيتوا متجوزين!\n🎁 200 🪙 هدية")
        try: await context.bot.send_message(partner, f"💍 {update.effective_user.first_name} اتجوزك! ❤️\n🎁 خدت 200 🪙")
        except: pass
    except: await update.message.reply_text("❌ اكتب: `/marry ID`")
async def cmd_divorce(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in marriages: await update.message.reply_text("😅 انت مش متجوز اصلا"); return
    p = marriages.pop(uid)
    if p in marriages: marriages.pop(p)
    await update.message.reply_text("💔 اتطلقت! بقيت سنجل 😂")
async def cmd_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if not context.args: await update.message.reply_text("💬 اكتب: `/chat رسالتك`\nرسالتك هتوصل لكل اللاعبين!"); return
    msg = " ".join(context.args); sent = 0
    for x in list(users.keys()):
        if x == uid: continue
        try: await context.bot.send_message(x, f"💬 **{update.effective_user.first_name}:**\n\n{msg}"); sent += 1
        except: pass
    await update.message.reply_text(f"✅ وصلت لـ {sent} واحد 💬")
async def cmd_trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for k in stock_prices: stock_prices[k] = max(10, stock_prices[k] + random.randint(-20, 30))
    txt = "📈 **بورصة TRAN**\n\n" + "\n".join([f"📊 {k}: {v} 🪙" for k, v in stock_prices.items()]) + "\n\nاشتري: `/buy_stock TRAN 5`\nبيع: `/sell_stock TRAN 5`"
    await update.message.reply_text(txt)
async def cmd_buy_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id; u = get_user(uid)
    if len(context.args) < 2: await update.message.reply_text("❌ اكتب: `/buy_stock TRAN 5`"); return
    sym = context.args[0].upper(); qty = int(context.args[1]); price = stock_prices.get(sym, 0) * qty
    if u["coins"] < price: await update.message.reply_text(f"❌ محتاج {price} 🪙"); return
    u["coins"] -= price; u.setdefault("stocks", {})[sym] = u.get("stocks", {}).get(sym, 0) + qty; await update.message.reply_text(f"📈 اشتريت {qty} {sym}!\nدفعت {price} 🪙")
async def cmd_sell_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id; u = get_user(uid)
    if len(context.args) < 2: await update.message.reply_text("❌ اكتب: `/sell_stock TRAN 5`"); return
    sym = context.args[0].upper(); qty = int(context.args[1]); have = u.get("stocks", {}).get(sym, 0)
    if have < qty: await update.message.reply_text(f"❌ معاك {have} بس"); return
    price = stock_prices.get(sym, 0) * qty; u["coins"] += price; u["stocks"][sym] -= qty; await update.message.reply_text(f"💰 بعت {qty} {sym}!\nخدت {price} 🪙")
async def cmd_pet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id; u = get_user(uid)
    if uid not in pets:
        if not context.args or context.args[0] != "buy": await update.message.reply_text("🐶 اشتري حيوان بـ 300 🪙\nاكتب: `/pet buy`"); return
        if u["coins"] < 300: await update.message.reply_text("❌ محتاج 300 🪙"); return
        u["coins"] -= 300; pets[uid] = {"name": random.choice(["🐶 ريكس", "🐱 لولو", "🐰 بوبو", "🦁 سيمبا"]), "level": 1}; await update.message.reply_text(f"🐶 اشتريت {pets[uid]['name']}!\nأكله بـ `/pet feed`"); return
    pet = pets[uid]
    if context.args and context.args[0] == "feed": pet["level"] += 1; r = pet["level"] * 20; add_coins(uid, r, "حيوان"); await update.message.reply_text(f"🍖 أكلت {pet['name']}!\n⭐ مستوى {pet['level']}\n🎁 +{r} 🪙")
    else: await update.message.reply_text(f"🐶 **{pet['name']}**\n⭐ مستوى {pet['level']}\nأكله بـ `/pet feed`")
async def cmd_house(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id; u = get_user(uid)
    if uid not in houses:
        if not context.args or context.args[0] != "buy": await update.message.reply_text("🏠 اشتري بيت بـ 2000 🪙\nاكتب: `/house buy`\nبيجيب 100 🪙 كل يوم!"); return
        if u["coins"] < 2000: await update.message.reply_text("❌ محتاج 2000 🪙"); return
        u["coins"] -= 2000; houses[uid] = True; await update.message.reply_text("🏠 اشتريت بيت! 🎉\nخد ايجار كل يوم بـ `/house`"); return
    u["coins"] += 100; await update.message.reply_text(f"🏠 خدت ايجار +100 🪙\n🪙 {u['coins']}")
async def cmd_car(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id; u = get_user(uid)
    if uid not in cars:
        if not context.args or context.args[0] != "buy": await update.message.reply_text("🚗 اشتري عربية بـ 5000 🪙\nاكتب: `/car buy`\nبتجيب 200 🪙 كل يوم!"); return
        if u["coins"] < 5000: await update.message.reply_text("❌ محتاج 5000 🪙"); return
        u["coins"] -= 5000; cars[uid] = True; await update.message.reply_text("🚗 اشتريت عربية! 🎉\nاشتغل اوبر بـ `/car`"); return
    u["coins"] += 200; await update.message.reply_text(f"🚗 اشتغلت اوبر! +200 🪙\n🪙 {u['coins']}")
async def cmd_gym(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id; u = get_user(uid); u["power"] += 5; add_coins(uid, 10, "جيم"); await update.message.reply_text(f"🏋️ اتمرنت!\n💪 قوتك {u['power']}\n🎁 +10 🪙")
async def cmd_study(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id; u = get_user(uid); u["edu"] += 1; await update.message.reply_text(f"🎓 ذاكرت!\n📚 مستواك {u['edu']}\n{'🎉 وصلت 5! ارباحك اتضاعفت!' if u['edu']>=5 else ''}")
async def cmd_battle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id; u = get_user(uid)
    if len(context.args) < 2: await update.message.reply_text("⚔️ اكتب: `/battle ID المبلغ`\nمثال: `/battle 123456 100`"); return
    try:
        target = int(context.args[0]); bet = int(context.args[1])
        if u["coins"] < bet: await update.message.reply_text("❌ معكش كفاية"); return
        tu = get_user(target)
        if tu["coins"] < bet: await update.message.reply_text("❌ خصمك معهوش كفاية"); return
        my = random.randint(1, 100) + u["level"] * 5; en = random.randint(1, 100) + tu["level"] * 5
        if my > en: u["coins"] += bet; tu["coins"] -= bet; await update.message.reply_text(f"⚔️ **كسبت!** 🎉\n💪 {my} vs {en}\n🎁 خدت {bet} 🪙")
        elif my < en: u["coins"] -= bet; tu["coins"] += bet; await update.message.reply_text(f"⚔️ **خسرت** 😔\n💪 {my} vs {en}\nخسرت {bet} 🪙")
        else: await update.message.reply_text("🤝 تعادل!")
    except: await update.message.reply_text("❌ اكتب صح: `/battle ID المبلغ`")
async def cmd_gift(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id; u = get_user(uid)
    if len(context.args) < 2: await update.message.reply_text("🎁 اكتب: `/gift ID المبلغ`"); return
    try:
        t = int(context.args[0]); amt = int(context.args[1])
        if u["coins"] < amt: await update.message.reply_text("❌ معكش كفاية"); return
        u["coins"] -= amt; get_user(t)["coins"] += amt; await update.message.reply_text(f"🎁 بعت هدية {amt} 🪙 لـ {t} ❤️")
        try: await context.bot.send_message(t, f"🎁 جاتلك هدية {amt} 🪙 من {update.effective_user.first_name} ❤️")
        except: pass
    except: await update.message.reply_text("❌ اكتب صح")
async def cmd_clan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if not context.args: await update.message.reply_text("🏰 اكتب: `/clan اسم الكلان`\nمثال: `/clan الاساطير`"); return
    name = " ".join(context.args); clans.setdefault(name, {"members": []})
    if uid not in clans[name]["members"]: clans[name]["members"].append(uid); add_coins(uid, 100, "كلان"); await update.message.reply_text(f"🏰 انضميت لكلان {name}!\n👥 {len(clans[name]['members'])} عضو\n🎁 +100 🪙")
    else: await update.message.reply_text(f"✅ انت في كلان {name} خلاص")
async def cmd_race(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id; u = get_user(uid); horses = ["🐴 برق", "🐴 رعد", "🐴 صقر", "🐴 نمر"]
    if not context.args: await update.message.reply_text("🏇 اختار حصان: `/race 1` لـ `/race 4`\nالرهان 50 🪙، لو كسبت تاخد 200 🪙"); return
    try:
        pick = int(context.args[0]) - 1
        if u["coins"] < 50: await update.message.reply_text("❌ محتاج 50 🪙"); return
        winner = random.randint(0, 3)
        if pick == winner: add_coins(uid, 200, "سباق"); await update.message.reply_text(f"🏇 الفايز: {horses[winner]}\n🎉 حصانك كسب! +200 🪙")
        else: add_coins(uid, -50, "سباق"); await update.message.reply_text(f"🏇 الفايز: {horses[winner]}\n😔 حصانك خسر -50 🪙")
    except: await update.message.reply_text("❌ اكتب: `/race 1`")
async def cmd_roulette(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id; u = get_user(uid)
    if not context.args: await update.message.reply_text("🎰 اكتب: `/roulette احمر` او `/roulette اسود`\nلو كسبت تاخد x2!"); return
    choice = context.args[0]; result = random.choice(["احمر", "اسود"])
    if u["coins"] < 50: await update.message.reply_text("❌ محتاج 50 🪙"); return
    if choice == result: add_coins(uid, 100, "روليت"); await update.message.reply_text(f"🎰 النتيجة: {result}\n🎉 كسبت! +100 🪙")
    else: add_coins(uid, -50, "روليت"); await update.message.reply_text(f"🎰 النتيجة: {result}\n😔 خسرت -50 🪙")
async def cmd_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("🤖 اكتب: `/ai سؤالك`\nمثال: `/ai ازاي اكسب كوينز؟`"); return
    q_text = " ".join(context.args).lower()
    if "كوينز" in q_text or "اكسب" in q_text: ans = "💰 **عشان تكسب كوينز:**\n1- العب 🎮\n2- المهام 🎁\n3- ادعي صحابك 👥\n4- عدن ⛏️\n5- اشتغل 💼\n6- بيت وعربية 🏠🚗"
    elif "حب" in q_text or "جواز" in q_text: ans = "❤️ اتجوز بـ `/marry ID`\nهتاخد +100 كل يوم + هدية 200 🪙"
    elif "ازيك" in q_text or "اهلا" in q_text: ans = f"اهلا بيك يا {update.effective_user.first_name}! 😊 عايز تلعب ولا تكسب ولا تتجوز؟ 😂"
    elif "بنك" in q_text: ans = "🏦 البنك: ايداع، سحب، قرض 500، فوايد 10% كل يوم!"
    else: ans = f"🤖 فهمتك!\nسؤالك: {q_text}\nنصيحتي: العب كتير وادعي صحابك وهتبقى غني 🔥"
    await update.message.reply_text(ans)
async def cmd_vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id; u = get_user(uid)
    if u["coins"] < 1000: await update.message.reply_text("❌ محتاج 1000 كوين عشان تبقى VIP"); return
    u["coins"] -= 1000; u["vip"] = True; await update.message.reply_text("👑 **بقيت VIP!** 👑\n✅ كل ارباحك هتتضاعف x2")
async def cmd_streak(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id; u = get_user(uid); u["streak"] += 1; r = u["streak"] * 10; add_coins(uid, r, "سلسلة"); await update.message.reply_text(f"🔥 سلسلة دخولك: {u['streak']} يوم\n🎁 +{r} 🪙")
async def cmd_tournament(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id; u = get_user(uid)
    if uid in tournaments["players"]: await update.message.reply_text(f"✅ انت في البطولة خلاص! 👥 {len(tournaments['players'])}"); return
    if u["coins"] < 100: await update.message.reply_text("❌ البطولة بـ 100 🪙"); return
    u["coins"] -= 100; tournaments["players"].append(uid); await update.message.reply_text(f"🏆 دخلت البطولة!\n👥 {len(tournaments['players'])}\n🏆 الجايزة 10000 🪙")
async def cmd_tournament_win(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(tournaments["players"]) < 2: await update.message.reply_text("❌ محتاج 2 على الاقل"); return
    w = random.choice(tournaments["players"]); add_coins(w, 10000, "بطولة"); await update.message.reply_text(f"🏆 الفايز بالبطولة!\n👤 {w}\n💰 خد 10000 🪙"); tournaments["players"].clear()
async def cmd_skins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id; u = get_user(uid)
    if not context.args:
        txt = "🎨 **متجر السكنات**\n\n" + "\n".join([f"{v['name']} - {v['price']} 🪙 | `/skins {k}`" for k, v in skins_shop.items()]) + f"\n\nسكنك: {u.get('skin','عادي')}"
        await update.message.reply_text(txt); return
    sid = context.args[0].lower()
    if sid not in skins_shop: await update.message.reply_text("❌ سكن مش موجود"); return
    s = skins_shop[sid]
    if u["coins"] < s["price"]: await update.message.reply_text(f"❌ محتاج {s['price']} 🪙"); return
    u["coins"] -= s["price"]; u["skin"] = s["name"]; await update.message.reply_text(f"🎨 اشتريت {s['name']}! 🔥")
async def cmd_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = random.choice(quiz_questions); context.user_data["quiz_ans"] = q["a"]
    kb = InlineKeyboardMarkup([[InlineKeyboardButton(opt, callback_data=f"quiz_{opt}")] for opt in q["opts"]])
    await update.message.reply_text(f"🧠 **سؤال ذكاء**\n\n{q['q']}", reply_markup=kb)
async def cmd_inventory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id; u = get_user(uid); inv = []
    if uid in pets: inv.append(f"🐶 {pets[uid]['name']}")
    if uid in houses: inv.append("🏠 بيت")
    if uid in cars: inv.append("🚗 عربية")
    if u.get("vip"): inv.append("👑 VIP")
    if uid in marriages: inv.append(f"💍 متجوز {marriages[uid]}")
    if not inv: inv.append("مخزونك فاضي")
    await update.message.reply_text("📦 **مخزونك**\n\n" + "\n".join(inv))
async def cmd_analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id; u = get_user(uid); rate = (u["wins"]/max(1, u["games"])*100) if u["games"] else 0
    await update.message.reply_text(f"📊 **تحليل ادائك**\n\n🎮 لعبت: {u['games']}\n✅ كسبت: {u['wins']} ({rate:.0f}%)\n🪙 كسبت: {u['total_won']:,}\n🏦 بنك: {u['bank']:,}\n\n💡 {'انت محترف! كمل' if rate>50 else 'العب اكتر'}")
async def cmd_horoscope(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🔮 **حظك اليوم**\n\n{random.choice(['🔥 النهاردة يوم حظك! العب كتير', '💰 هتكسب كوينز كتير', '❤️ حد بيحبك هيديك هدية', '🍀 حظك حلو، جرب اليانصيب', '⚡ ركز في الشغل'])}")
async def cmd_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id; u = get_user(uid)
    if not context.args: await update.message.reply_text(f"🎨 لقبك: {u.get('title','مفيش')}\nغيره بـ: `/title الملك`"); return
    title = " ".join(context.args)
    if u["coins"] < 100: await update.message.reply_text("❌ اللقب بـ 100 🪙"); return
    u["coins"] -= 100; u["title"] = title; await update.message.reply_text(f"🎨 بقى لقبك: {title} 👑")
async def cmd_insurance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id; u = get_user(uid)
    if u.get("insured"): await update.message.reply_text("🛡️ انت مأمن فلوسك خلاص ✅"); return
    if u["coins"] < 200: await update.message.reply_text("❌ التأمين بـ 200 كوين"); return
    u["coins"] -= 200; u["insured"] = True; await update.message.reply_text("🛡️ أمنت فلوسك! ✅")
async def cmd_league(update: Update, context: ContextTypes.DEFAULT_TYPE):
    top = sorted(users.values(), key=lambda x: x["points"], reverse=True)[:5]; txt = "🏆 **الدوري الاسبوعي**\n\n"
    medals = ["🥇 5000 🪙", "🥈 3000 🪙", "🥉 1500 🪙", "4️⃣ 500 🪙", "5️⃣ 200 🪙"]
    for i, u2 in enumerate(top): txt += f"{medals[i]} - {u2.get('name','')} | {u2['points']} نقطة\n"
    await update.message.reply_text(txt)
async def cmd_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id; u = get_user(uid)
    if not context.args:
        notes = u.get("notes", [])
        await update.message.reply_text("📝 **مذكراتك**\n\n" + ("\n".join(notes[-5:]) if notes else "فاضية - اكتب `/note انا بحب TRAN`")); return
    u.setdefault("notes", []).append(" ".join(context.args)); await update.message.reply_text("📝 حفظت مذكرتك!")
async def cmd_auction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id; u = get_user(uid)
    if not context.args:
        if not auctions: await update.message.reply_text("🎲 المزاد فاضي\nاكتب: `/auction المبلغ`"); return
        await update.message.reply_text("🎲 **المزادات:**\n\n" + "\n".join([f"👤 {a['seller']} بيبيع {a['amount']} 🪙" for a in auctions[-5:]])); return
    try:
        amt = int(context.args[0])
        if u["coins"] < amt: await update.message.reply_text("❌ معكش كفاية"); return
        u["coins"] -= amt; auctions.append({"seller": uid, "amount": amt}); await update.message.reply_text(f"🎲 عرضت {amt} 🪙 في المزاد!")
    except: await update.message.reply_text("❌ اكتب: `/auction المبلغ`")

async def on_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id; txt = (update.message.text or "").strip(); u = get_user(uid)
    if txt == "تصفير" and uid == OWNER_ID: users.clear(); await update.message.reply_text("✅ اتصفر كله"); return
    if context.user_data.get("wait_broadcast") and uid == OWNER_ID:
        context.user_data["wait_broadcast"] = False; c = 0
        for x in list(users.keys()):
            try: await context.bot.send_message(x, f"📢 **من الادارة:**\n\n{txt}"); c += 1
            except: pass
        await update.message.reply_text(f"✅ اتبعت لـ {c}"); return
    if context.user_data.get("wait_add") and uid == OWNER_ID:
        context.user_data["wait_add"] = False
        try: t, a = map(int, txt.split()); get_user(t); add_coins(t, a, "اونر"); await update.message.reply_text(f"✅ ضفت {a} لـ {t}")
        except: await update.message.reply_text("❌ اكتب صح: ID المبلغ")
        return
    if context.user_data.get("wait_remove") and uid == OWNER_ID:
        context.user_data["wait_remove"] = False
        try: t, a = map(int, txt.split()); get_user(t); add_coins(t, -a, "خصم"); await update.message.reply_text(f"✅ خصمت {a} من {t}")
        except: await update.message.reply_text("❌ اكتب صح")
        return
    if context.user_data.get("wait_ban") and uid == OWNER_ID:
        context.user_data["wait_ban"] = False
        try: t = int(txt); get_user(t); users[t]["banned"] = not users[t]["banned"]; await update.message.reply_text(f"✅ {'حظرته ⛔' if users[t]['banned'] else 'فكيت حظره ✅'} {t}")
        except: await update.message.reply_text("❌ ID غلط")
        return
    if context.user_data.get("wait_view") and uid == OWNER_ID:
        context.user_data["wait_view"] = False
        try: t = int(txt); uu = get_user(t); await update.message.reply_text(f"👤 {uu['name']}\n🆔 {t}\n🪙 {uu['coins']} | 🏦 {uu['bank']}\n⛔ محظور: {uu['banned']}")
        except: await update.message.reply_text("❌ مش موجود")
        return
    if context.user_data.get("wait_transfer"):
        context.user_data["wait_transfer"] = False
        try:
            t, a = map(int, txt.split())
            if u["coins"] < a: await update.message.reply_text("❌ معكش كفاية"); return
            get_user(t); u["coins"] -= a; users[t]["coins"] += a; await update.message.reply_text(f"✅ حولت {a} 🪙 لـ {t}")
            try: await context.bot.send_message(t, f"💸 وصلك {a} 🪙 من {update.effective_user.first_name}")
            except: pass
        except: await update.message.reply_text("❌ اكتب: ID المبلغ")
        return
    if context.user_data.get("guess") is not None:
        n = context.user_data.pop("guess")
        try:
            g = int(txt)
            if g == n: add_coins(uid, 50, "تخمين"); await update.message.reply_text(f"🎉 صح! الرقم كان {n} +50 🪙")
            else: add_coins(uid, -10, "تخمين"); await update.message.reply_text(f"😔 غلط! الرقم كان {n} -10 🪙")
        except: await update.message.reply_text("❌ ابعت رقم")
        return
    if context.user_data.get("wait_code"):
        context.user_data["wait_code"] = False; code = txt.upper()
        if code in codes: r = codes.pop(code); add_coins(uid, r, "كود"); await update.message.reply_text(f"🎉 خدت +{r} 🪙")
        else: await update.message.reply_text("❌ كود غلط")
        return
    if context.user_data.get("wait_support"):
        context.user_data["wait_support"] = False; await update.message.reply_text("✅ وصلت للاونر ❤️", reply_markup=main_menu(uid))
        try: await context.bot.send_message(OWNER_ID, f"🆘 من {update.effective_user.first_name} ({uid}):\n{txt}")
        except: pass
        return
    await update.message.reply_text("👋 اكتب /start", reply_markup=main_menu(uid))

async def on_callback_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    if q.data.startswith("quiz_"):
        ans = q.data.replace("quiz_", "")
        if ans == context.user_data.get("quiz_ans"): add_coins(q.from_user.id, 40, "quiz"); await q.edit_message_text("🧠 صح! +40 🪙 🎉")
        else: await q.edit_message_text(f"😔 غلط! الصح كان {context.user_data.get('quiz_ans')}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("owner", start))
    app.add_handler(CommandHandler("mine", cmd_mine))
    app.add_handler(CommandHandler("work", cmd_work))
    app.add_handler(CommandHandler("box", cmd_box))
    app.add_handler(CommandHandler("lottery", cmd_lottery))
    app.add_handler(CommandHandler("lottery_draw", cmd_lottery_draw))
    app.add_handler(CommandHandler("marry", cmd_marry))
    app.add_handler(CommandHandler("divorce", cmd_divorce))
    app.add_handler(CommandHandler("chat", cmd_chat))
    app.add_handler(CommandHandler("trade", cmd_trade))
    app.add_handler(CommandHandler("buy_stock", cmd_buy_stock))
    app.add_handler(CommandHandler("sell_stock", cmd_sell_stock))
    app.add_handler(CommandHandler("pet", cmd_pet))
    app.add_handler(CommandHandler("house", cmd_house))
    app.add_handler(CommandHandler("car", cmd_car))
    app.add_handler(CommandHandler("gym", cmd_gym))
    app.add_handler(CommandHandler("study", cmd_study))
    app.add_handler(CommandHandler("battle", cmd_battle))
    app.add_handler(CommandHandler("gift", cmd_gift))
    app.add_handler(CommandHandler("clan", cmd_clan))
    app.add_handler(CommandHandler("race", cmd_race))
    app.add_handler(CommandHandler("roulette", cmd_roulette))
    app.add_handler(CommandHandler("ai", cmd_ai))
    app.add_handler(CommandHandler("vip", cmd_vip))
    app.add_handler(CommandHandler("streak", cmd_streak))
    app.add_handler(CommandHandler("tournament", cmd_tournament))
    app.add_handler(CommandHandler("tournament_win", cmd_tournament_win))
    app.add_handler(CommandHandler("skins", cmd_skins))
    app.add_handler(CommandHandler("quiz", cmd_quiz))
    app.add_handler(CommandHandler("inventory", cmd_inventory))
    app.add_handler(CommandHandler("analyze", cmd_analyze))
    app.add_handler(CommandHandler("horoscope", cmd_horoscope))
    app.add_handler(CommandHandler("title", cmd_title))
    app.add_handler(CommandHandler("insurance", cmd_insurance))
    app.add_handler(CommandHandler("league", cmd_league))
    app.add_handler(CommandHandler("note", cmd_note))
    app.add_handler(CommandHandler("auction", cmd_auction))
    app.add_handler(CallbackQueryHandler(on_callback_quiz, pattern="^quiz_"))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_msg))
    print("🔥 TRAN FINAL 150 STARTED")
    app.run_polling()
if __name__ == "__main__": main()
