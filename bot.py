# TRAN BOT - FINAL FIXED v6.0 - OWNER 8188263997
import os, random, time, logging, threading
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from flask import Flask
import requests

logging.basicConfig(level=logging.INFO)
TOKEN = os.environ.get("BOT_TOKEN")
OWNER_ID = int(os.environ.get("OWNER_ID", "8188263997"))

app_flask = Flask(__name__)
@app_flask.route('/')
def home(): return "TRAN ALIVE"
def run_flask():
    try: app_flask.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
    except: pass
def self_ping():
    time.sleep(10)
    url = os.environ.get("RENDER_EXTERNAL_URL", "")
    if not url: return
    while True:
        try: requests.get(url, timeout=10)
        except: pass
        time.sleep(600)
threading.Thread(target=run_flask, daemon=True).start()
threading.Thread(target=self_ping, daemon=True).start()

users={}; codes={}; clans={}; marriages={}; pets={}; houses={}; cars={}; jailed={}
stock_prices={"TRAN":100,"GOLD":500,"BTC":1000,"DOGE":50}
lottery_players=[]; auctions=[]; mining_last={}; tournaments={"players":[],"prize":10000}
skins_shop={"gold":{"name":"ذهبي","price":500},"diamond":{"name":"الماسي","price":1000},"fire":{"name":"ناري","price":800},"king":{"name":"ملكي","price":2000}}
quiz_q=[{"q":"ايه عاصمة مصر؟","a":"القاهرة","opts":["القاهرة","الجيزة","اسكندرية"]},{"q":"كم عدد ايام السنة؟","a":"365","opts":["365","360","366"]},{"q":"ايه اكبر كوكب؟","a":"المشتري","opts":["المشتري","المريخ","زحل"]}]
words=["اسد","قطة","كلب","سيارة","بيت","شمس","قمر","بحر"]

def get_user(uid, username="", name=""):
    uid=int(uid)
    if uid not in users:
        users[uid]={"id":uid,"username":username,"name":name,"coins":100,"balance":0,"bank":0,"points":0,"level":1,"ref":0,"banned":False,"vip":False,"loan":0,"games":0,"wins":0,"losses":0,"total_won":0,"tasks":[],"last_daily":"","joined":datetime.now().strftime("%Y-%m-%d"),"transactions":[],"stocks":{},"notes":[],"power":10,"edu":0,"streak":0,"skin":"عادي","title":"","insured":False,"mafia":"","wanted":0}
    return users[uid]
def add_coins(uid, amt, reason=""):
    u=get_user(uid); u["coins"]+=amt; u["points"]+=amt
    if amt>0: u["total_won"]+=amt
    u["transactions"].append(f"{reason} {amt:+}")
    u["transactions"]=u["transactions"][-10:]
    return u
def lvl_name(c):
    if c<500: return "مبتدئ"
    if c<2000: return "محترف"
    if c<5000: return "خبير"
    if c<15000: return "اسطوري"
    return "ملك TRAN"

def main_menu(uid):
    kb=[
        [InlineKeyboardButton("العاب", callback_data="games"), InlineKeyboardButton("البنك", callback_data="bank")],
        [InlineKeyboardButton("المتجر", callback_data="shop"), InlineKeyboardButton("المسابقات", callback_data="comp")],
        [InlineKeyboardButton("المهام", callback_data="tasks"), InlineKeyboardButton("محفظتي", callback_data="wallet")],
        [InlineKeyboardButton("دعوة", callback_data="ref"), InlineKeyboardButton("ترتيب", callback_data="rank")],
        [InlineKeyboardButton("عجلة الحظ", callback_data="wheel"), InlineKeyboardButton("كود هدية", callback_data="gift")],
        [InlineKeyboardButton("بروفايلي", callback_data="profile"), InlineKeyboardButton("الدعم", callback_data="support")],
        [InlineKeyboardButton("مافيا", callback_data="mafia_menu"), InlineKeyboardButton("معلومات", callback_data="info")],
    ]
    if int(uid)==OWNER_ID: kb.append([InlineKeyboardButton("لوحة الاونر", callback_data="owner")])
    kb.append([InlineKeyboardButton("تحديث", callback_data="back")])
    return InlineKeyboardMarkup(kb)
def back(): return InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data="back")]])
def back2(to): return InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data=to)],[InlineKeyboardButton("القايمة", callback_data="back")]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        u=update.effective_user; user=get_user(u.id, u.username or "", u.first_name or "")
        if user["banned"]:
            await update.message.reply_text("محظور"); return
        if context.args:
            try:
                inv=int(context.args[0])
                if inv!=u.id and inv in users and "ref_by" not in user:
                    user["ref_by"]=inv; users[inv]["ref"]+=1; add_coins(inv,50,"دعوة")
                    try: await context.bot.send_message(inv, f"{u.first_name} دخل من لينكك +50")
                    except: pass
            except: pass
        txt=f"اهلا {u.first_name} في TRAN\n\nكوينز: {user['coins']}\nبنك: {user['bank']}\nرصيد: {user['balance']} ج\nمستواك: {lvl_name(user['coins'])}\nدعيت: {user['ref']}\nمافيا: {user.get('mafia') or 'مفيش'}\n\nاختار من القايمة تحت\n\nاوامر سريعة:\n/mine تعدين\n/work شغل\n/box صندوق\n/lottery يانصيب\n/marry جواز\n/trade تداول\n/chat شات\n/ai ذكاء اصطناعي\n/steal سرقة\n/mafia مافيا"
        await update.message.reply_text(txt, reply_markup=main_menu(u.id))
    except Exception as e:
        print(f"START ERROR: {e}")
        try: await update.message.reply_text("اهلا بيك في TRAN اختار من القايمة", reply_markup=main_menu(update.effective_user.id))
        except Exception as e2: print(f"START ERROR2: {e2}")

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q=update.callback_query
    try: await q.answer()
    except: pass
    uid=q.from_user.id; user=get_user(uid, q.from_user.username or "", q.from_user.first_name or ""); data=q.data
    try:
        if data=="back":
            await q.edit_message_text(f"TRAN\n\nكوينز: {user['coins']} | بنك: {user['bank']} | رصيد: {user['balance']} ج\nمستواك: {lvl_name(user['coins'])}", reply_markup=main_menu(uid)); return
        if data=="bank":
            kb=InlineKeyboardMarkup([[InlineKeyboardButton("ايداع", callback_data="bank_deposit"), InlineKeyboardButton("سحب", callback_data="bank_withdraw")],[InlineKeyboardButton("تحويل", callback_data="bank_transfer"), InlineKeyboardButton("قرض", callback_data="bank_loan")],[InlineKeyboardButton("فوايد", callback_data="bank_interest"), InlineKeyboardButton("كشف حساب", callback_data="bank_history")],[InlineKeyboardButton("فيزا TRAN", callback_data="bank_visa")],[InlineKeyboardButton("رجوع", callback_data="back")]])
            await q.edit_message_text(f"بنك TRAN\n\nفي ايدك: {user['coins']}\nفي البنك: {user['bank']}\nقرض عليك: {user['loan']}\nتامين: {'نعم' if user.get('insured') else 'لا'}", reply_markup=kb); return
        if data=="bank_deposit":
            if user["coins"]>=100: user["coins"]-=100; user["bank"]+=100; await q.edit_message_text(f"ايداع تم!\nبنك: {user['bank']} | معاك: {user['coins']}", reply_markup=back2("bank"))
            else: await q.edit_message_text("معكش 100 كوين", reply_markup=back2("bank")); return
        if data=="bank_withdraw":
            if user["bank"]>=100: user["bank"]-=100; user["coins"]+=100; await q.edit_message_text(f"سحبت 100\nمعاك: {user['coins']} | بنك: {user['bank']}", reply_markup=back2("bank"))
            else: await q.edit_message_text("معكش في البنك", reply_markup=back2("bank")); return
        if data=="bank_transfer": context.user_data["wait_transfer"]=True; await q.edit_message_text("اكتب: ID المبلغ\nمثال: 123456 100", reply_markup=back2("bank")); return
        if data=="bank_loan":
            if user["loan"]>0: await q.edit_message_text(f"عليك قرض {user['loan']}", reply_markup=back2("bank")); return
            user["coins"]+=500; user["loan"]=550; await q.edit_message_text(f"خدت قرض 500\nهترجع 550\nمعاك: {user['coins']}", reply_markup=back2("bank")); return
        if data=="bank_interest":
            if user["bank"]<=0: await q.edit_message_text("حط فلوس في البنك الاول", reply_markup=back2("bank")); return
            interest=int(user["bank"]*0.1); user["bank"]+=interest; await q.edit_message_text(f"فوايد +{interest}\nبنك: {user['bank']}", reply_markup=back2("bank")); return
        if data=="bank_history": await q.edit_message_text("كشف حساب\n\n" + ("\n".join(user["transactions"][-10:]) or "مفيش حركات"), reply_markup=back2("bank")); return
        if data=="bank_visa": await q.edit_message_text(f"فيزا TRAN\n\n{ q.from_user.first_name}\nرقم: 5335 {uid%10000:04d} 2026 8188\nرصيد: {user['bank']} \nشغالة", reply_markup=back2("bank")); return
        if data=="mafia_menu":
            kb=InlineKeyboardMarkup([[InlineKeyboardButton("انضم للمافيا", callback_data="mafia_join"), InlineKeyboardButton("اسرق", callback_data="mafia_steal")],[InlineKeyboardButton("سجن", callback_data="mafia_jail"), InlineKeyboardButton("محكمة", callback_data="mafia_court")],[InlineKeyboardButton("رجوع", callback_data="back")]])
            await q.edit_message_text(f"عالم المافيا\n\nمطلوب: {user.get('wanted',0)}\nمافيا: {user.get('mafia') or 'مفيش'}\n\nاسرق، اهرب، ولو اتمسكت هتدخل السجن!", reply_markup=kb); return
        if data=="mafia_join":
            if user.get("mafia"): await q.edit_message_text(f"انت في مافيا {user['mafia']} خلاص", reply_markup=back2("mafia_menu")); return
            user["mafia"]=random.choice(["مافيا TRAN","مافيا الصقور","مافيا الثعابين"]); add_coins(uid,200,"مافيا"); await q.edit_message_text(f"انضميت لـ {user['mafia']}!\nخدت +200", reply_markup=back2("mafia_menu")); return
        if data=="mafia_steal":
            if random.random()<0.3: user["wanted"]+=1; jailed[uid]=True; await q.edit_message_text(f"اتمسكت!\nمطلوب: {user['wanted']}\nاطلع بـ /free", reply_markup=back2("mafia_menu")); return
            stolen=random.randint(20,200); add_coins(uid,stolen,"سرقة"); await q.edit_message_text(f"سرقت! +{stolen}\nمعاك: {user['coins']}", reply_markup=back2("mafia_menu")); return
        if data=="mafia_jail": jailed[uid]=True; await q.edit_message_text("دخلت السجن!\nاطلع بـ /free", reply_markup=back2("mafia_menu")); return
        if data=="mafia_court":
            if user.get("wanted",0)==0: await q.edit_message_text("انت بريء!", reply_markup=back2("mafia_menu")); return
            if random.random()<0.5: user["wanted"]=0; jailed.pop(uid,None); await q.edit_message_text("براءة!", reply_markup=back2("mafia_menu"))
            else: await q.edit_message_text("ادانة! غرامة 300", reply_markup=back2("mafia_menu")); return
        if data=="games":
            kb=InlineKeyboardMarkup([[InlineKeyboardButton("نرد", callback_data="g_dice"), InlineKeyboardButton("ملك وكتابة", callback_data="g_flip")],[InlineKeyboardButton("سلوت", callback_data="g_slot"), InlineKeyboardButton("صاروخ", callback_data="g_crash")],[InlineKeyboardButton("حجر ورقة مقص", callback_data="g_rps"), InlineKeyboardButton("تخمين رقم", callback_data="g_guess")],[InlineKeyboardButton("رجوع", callback_data="back")]])
            await q.edit_message_text("العاب - كل لعبة بتكسب كوينز", reply_markup=kb); return
        if data=="g_dice":
            r=random.randint(1,6); user["games"]+=1
            if r>=4: add_coins(uid,25,"نرد"); txt=f"النرد: {r}\nكسبت +25"
            else: add_coins(uid,-10,"نرد"); txt=f"النرد: {r}\nخسرت -10"
            await q.edit_message_text(f"{txt}\nمعاك: {user['coins']}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("تاني", callback_data="g_dice")],[InlineKeyboardButton("رجوع", callback_data="games")]])); return
        if data=="g_flip": await q.edit_message_text("اختار:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ملك", callback_data="flip_k"), InlineKeyboardButton("كتابة", callback_data="flip_w")],[InlineKeyboardButton("رجوع", callback_data="games")]])); return
        if data.startswith("flip_"):
            res=random.choice(["k","w"]); choice="k" if data=="flip_k" else "w"
            if choice==res: add_coins(uid,30,"ملك"); txt="صح! +30"
            else: add_coins(uid,-10,"ملك"); txt="غلط! -10"
            await q.edit_message_text(f"{txt}\nمعاك: {user['coins']}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("تاني", callback_data="g_flip")],[InlineKeyboardButton("رجوع", callback_data="games")]])); return
        if data=="g_slot":
            e=["🍒","🍋","⭐","💎","7"]; r=[random.choice(e) for _ in range(3)]
            if r[0]==r[1]==r[2]: add_coins(uid,100,"سلوت"); txt=f"{' '.join(r)}\nJACKPOT +100"
            elif r[0]==r[1] or r[1]==r[2]: add_coins(uid,20,"سلوت"); txt=f"{' '.join(r)}\n+20"
            else: add_coins(uid,-10,"سلوت"); txt=f"{' '.join(r)}\n-10"
            await q.edit_message_text(f"{txt}\nمعاك: {user['coins']}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("تاني", callback_data="g_slot")],[InlineKeyboardButton("رجوع", callback_data="games")]])); return
        if data=="g_crash":
            m=round(random.uniform(1,5),2)
            if m>=2: w=int(20*m); add_coins(uid,w,"صاروخ"); txt=f"صاروخ x{m}\n+{w}"
            else: add_coins(uid,-20,"صاروخ"); txt=f"انفجر x{m}\n-20"
            await q.edit_message_text(f"{txt}\nمعاك: {user['coins']}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("تاني", callback_data="g_crash")],[InlineKeyboardButton("رجوع", callback_data="games")]])); return
        if data=="g_rps": await q.edit_message_text("اختار:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("حجر", callback_data="rps_rock"), InlineKeyboardButton("ورقة", callback_data="rps_paper"), InlineKeyboardButton("مقص", callback_data="rps_scissors")],[InlineKeyboardButton("رجوع", callback_data="games")]])); return
        if data.startswith("rps_"):
            me=data.replace("rps_",""); bot=random.choice(["rock","paper","scissors"]); mp={"rock":"حجر","paper":"ورقة","scissors":"مقص"}
            if me==bot: txt="تعادل!"
            elif (me=="rock" and bot=="scissors") or (me=="paper" and bot=="rock") or (me=="scissors" and bot=="paper"): add_coins(uid,20,"حجر"); txt="كسبت +20"
            else: add_coins(uid,-10,"حجر"); txt="خسرت -10"
            await q.edit_message_text(f"انت {mp[me]} vs بوت {mp[bot]}\n{txt}\nمعاك: {user['coins']}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("تاني", callback_data="g_rps")],[InlineKeyboardButton("رجوع", callback_data="games")]])); return
        if data=="g_guess": context.user_data["guess"]=random.randint(1,5); await q.edit_message_text("خمن رقم من 1 لـ 5، ابعته في رسالة", reply_markup=back2("games")); return
        if data=="wheel": p=random.choice([10,20,0,50,5,100,0,30]); add_coins(uid,p,"عجلة"); await q.edit_message_text(f"كسبت +{p}\nمعاك: {user['coins']}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("تاني", callback_data="wheel")],[InlineKeyboardButton("رجوع", callback_data="back")]])); return
        if data=="shop":
            kb=InlineKeyboardMarkup([[InlineKeyboardButton("500 كوين - 25ج", callback_data="buy_500")],[InlineKeyboardButton("1000 كوين - 45ج", callback_data="buy_1000")],[InlineKeyboardButton("5000 كوين - 180ج", callback_data="buy_5000")],[InlineKeyboardButton("10000 كوين VIP - 320ج", callback_data="buy_10000")],[InlineKeyboardButton("رجوع", callback_data="back")]])
            await q.edit_message_text("المتجر\nاختار عرض، الدفع فودافون كاش", reply_markup=kb); return
        if data.startswith("buy_"):
            amt=data.replace("buy_",""); await q.edit_message_text(f"طلبك {amt} كوين اتسجل!\nحول على 01000000000 وابعت سكرين للدعم", reply_markup=back())
            try: await context.bot.send_message(OWNER_ID, f"طلب {amt} من {q.from_user.first_name} ({uid})")
            except: pass
            return
        if data=="comp": await q.edit_message_text(f"مسابقة اليوم\nالجايزة 1000\nنقاطك: {user['points']}", reply_markup=back()); return
        if data=="tasks":
            today=datetime.now().strftime("%Y-%m-%d")
            if user["last_daily"]!=today: user["tasks"]=[]; user["last_daily"]=today
            kb=InlineKeyboardMarkup([[InlineKeyboardButton("مكافأة يومية +20", callback_data="task_daily")],[InlineKeyboardButton("انضم للقناة +30", callback_data="task_join")],[InlineKeyboardButton("شارك البوت +25", callback_data="task_share")],[InlineKeyboardButton("رجوع", callback_data="back")]])
            await q.edit_message_text("مهام - خد كوينز ببلاش", reply_markup=kb); return
        if data.startswith("task_"):
            tid=data.replace("task_",""); today=datetime.now().strftime("%Y-%m-%d")
            if user["last_daily"]!=today: user["tasks"]=[]; user["last_daily"]=today
            if tid in user["tasks"]: await q.edit_message_text("عملتها النهاردة", reply_markup=back()); return
            rewards={"daily":20,"join":30,"share":25}; user["tasks"].append(tid); add_coins(uid,rewards.get(tid,20),"مهمة")
            await q.edit_message_text(f"+{rewards.get(tid,20)}\nمعاك: {user['coins']}", reply_markup=back()); return
        if data=="wallet": await q.edit_message_text(f"محفظتي\nكوينز: {user['coins']}\nبنك: {user['bank']}\nرصيد: {user['balance']} ج\nمستواك: {lvl_name(user['coins'])}\nنقاط: {user['points']}\nسكن: {user.get('skin')}\nلقب: {user.get('title') or 'مفيش'}", reply_markup=back()); return
        if data=="ref":
            link=f"https://t.me/{context.bot.username}?start={uid}"
            await q.edit_message_text(f"دعوة\nكل صاحب +50\nدعيت: {user['ref']}\n\nلينكك:\n{link}", reply_markup=back()); return
        if data=="rank":
            top=sorted(users.values(), key=lambda x: x["coins"], reverse=True)[:10]; txt="توب 10\n\n"; medals=["1","2","3","4","5","6","7","8","9","10"]
            for i,u2 in enumerate(top): txt+=f"{medals[i]}- {u2.get('name','')} - {u2['coins']} {'انت' if u2['id']==uid else ''}\n"
            await q.edit_message_text(txt, reply_markup=back()); return
        if data=="profile": await q.edit_message_text(f"بروفايلك\n\n{u.first_name} {user.get('title','')}\nID: {uid}\nمستواك: {lvl_name(user['coins'])}\nكوينز: {user['coins']} | بنك: {user['bank']}\nسكن: {user.get('skin')}\nمافيا: {user.get('mafia') or 'مفيش'}\nمتجوز: {'نعم' if uid in marriages else 'لا'}\nلعبت {user['games']} | كسبت {user['wins']}\nانضميت {user['joined']}", reply_markup=back()); return
        if data=="info": await q.edit_message_text("TRAN v6.0 FINAL\nالعاب + بنك + متجر + اونر + مافيا\nجواز + كلان + تداول + ذكاء اصطناعي\n150+ ميزة شغالة", reply_markup=back()); return
        if data=="support": context.user_data["wait_support"]=True; await q.edit_message_text("اكتب مشكلتك دلوقتي في رسالة", reply_markup=back()); return
        if data=="gift": context.user_data["wait_code"]=True; await q.edit_message_text("اكتب الكود، زي TRAN100", reply_markup=back()); return
        if data=="owner":
            if uid!=OWNER_ID: await q.edit_message_text("مش الاونر", reply_markup=back()); return
            kb=InlineKeyboardMarkup([[InlineKeyboardButton("احصائيات", callback_data="o_stats"), InlineKeyboardButton("اذاعة", callback_data="o_broadcast")],[InlineKeyboardButton("اضف كوينز", callback_data="o_add"), InlineKeyboardButton("خصم كوينز", callback_data="o_remove")],[InlineKeyboardButton("حظر / فك", callback_data="o_ban"), InlineKeyboardButton("اعمل كود", callback_data="o_code")],[InlineKeyboardButton("شوف يوزر", callback_data="o_view"), InlineKeyboardButton("تصفير", callback_data="o_reset")],[InlineKeyboardButton("رجوع", callback_data="back")]])
            await q.edit_message_text(f"لوحة الاونر\n\nاهلا يا اونر\nمستخدمين: {len(users)}\nاجمالي: {sum(u['coins'] for u in users.values())}", reply_markup=kb); return
        if data=="o_stats":
            if uid!=OWNER_ID: return
            await q.edit_message_text(f"احصائيات\nمستخدمين: {len(users)}\nكوينز: {sum(u['coins'] for u in users.values())}\nبنك: {sum(u['bank'] for u in users.values())}\nالعاب: {sum(u['games'] for u in users.values())}", reply_markup=back()); return
        if data=="o_broadcast":
            if uid!=OWNER_ID: return
            context.user_data["wait_broadcast"]=True; await q.edit_message_text("ابعت رسالة الاذاعة دلوقتي", reply_markup=back()); return
        if data=="o_add":
            if uid!=OWNER_ID: return
            context.user_data["wait_add"]=True; await q.edit_message_text("اكتب: ID المبلغ\nمثال: 8188263997 500", reply_markup=back()); return
        if data=="o_remove":
            if uid!=OWNER_ID: return
            context.user_data["wait_remove"]=True; await q.edit_message_text("اكتب: ID المبلغ", reply_markup=back()); return
        if data=="o_ban":
            if uid!=OWNER_ID: return
            context.user_data["wait_ban"]=True; await q.edit_message_text("اكتب ID اللي عايز تحظره / تفك حظره", reply_markup=back()); return
        if data=="o_code":
            if uid!=OWNER_ID: return
            code=f"TRAN{random.randint(100,999)}"; codes[code]=100; await q.edit_message_text(f"كود جديد: {code}\nالهدية: 100", reply_markup=back()); return
        if data=="o_view":
            if uid!=OWNER_ID: return
            context.user_data["wait_view"]=True; await q.edit_message_text("اكتب ID اليوزر", reply_markup=back()); return
        if data=="o_reset":
            if uid!=OWNER_ID: return
            await q.edit_message_text("اكتب تصفير في الشات لو متأكد", reply_markup=back()); return
    except Exception as e:
        print(f"BUTTON ERROR: {e} - {data}")
        try: await q.edit_message_text("حصل ايرور، دوس تحديث", reply_markup=main_menu(uid))
        except: pass

async def cmd_mine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; u=get_user(uid); now=time.time()
    if now-mining_last.get(uid,0)<3600: await update.message.reply_text(f"لسه بتعدن! فاضل {int((3600-(now-mining_last.get(uid,0)))/60)} دقيقة"); return
    mining_last[uid]=now; mined=random.randint(30,150)*(2 if u.get("vip") else 1); add_coins(uid,mined,"تعدين"); await update.message.reply_text(f"عدنت! +{mined}\nمعاك: {u['coins']}")
async def cmd_work(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; u=get_user(uid); job=random.choice(["طباخ","مبرمج","سواق","دكتور","مغني","لاعب كورة"]); salary=random.randint(50,200)*(2 if u.get("vip") else 1); add_coins(uid,salary,"شغل"); await update.message.reply_text(f"اشتغلت {job}!\n+{salary}\nمعاك: {u['coins']}")
async def cmd_box(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; u=get_user(uid); today=datetime.now().strftime("%Y-%m-%d")
    if u.get("last_box")==today: await update.message.reply_text("فتحت الصندوق النهاردة، تعالى بكرة"); return
    u["last_box"]=today; prize=random.choice([10,20,50,100,200,500,0])
    if prize==0: await update.message.reply_text("الصندوق فاضي!")
    else: add_coins(uid,prize,"صندوق"); await update.message.reply_text(f"فتحت الصندوق! +{prize}\nمعاك: {u['coins']}")
async def cmd_lottery(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; u=get_user(uid)
    if uid in lottery_players: await update.message.reply_text("دخلت خلاص"); return
    if u["coins"]<20: await update.message.reply_text("محتاج 20 كوين"); return
    u["coins"]-=20; lottery_players.append(uid); await update.message.reply_text(f"دخلت اليانصيب!\nلاعبين: {len(lottery_players)}\nاكتب /lottery_draw")
async def cmd_lottery_draw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(lottery_players)<2: await update.message.reply_text("محتاج 2 على الاقل"); return
    w=random.choice(lottery_players); prize=len(lottery_players)*20; add_coins(w,prize,"يانصيب"); await update.message.reply_text(f"الفايز باليانصيب!\n{w}\nخد {prize}"); lottery_players.clear()
async def cmd_marry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; u=get_user(uid)
    if uid in marriages: await update.message.reply_text(f"انت متجوز {marriages[uid]} خلاص!"); return
    if not context.args: await update.message.reply_text("اكتب: /marry ID الشريك\nالجواز بـ 500 وبيجيب +100 كل يوم"); return
    try:
        partner=int(context.args[0])
        if partner==uid: await update.message.reply_text("مينفعش تتجوز نفسك!"); return
        if partner in marriages: await update.message.reply_text("متجوز!"); return
        if u["coins"]<500: await update.message.reply_text("الجواز بـ 500"); return
        u["coins"]-=500; marriages[uid]=partner; marriages[partner]=uid; add_coins(partner,200,"جواز"); await update.message.reply_text(f"مبروك الجواز!\nانت و {partner} بقيتوا متجوزين!\nهدية 200")
        try: await context.bot.send_message(partner, f"{update.effective_user.first_name} اتجوزك! خدت 200")
        except: pass
    except: await update.message.reply_text("اكتب: /marry ID")
async def cmd_divorce(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id
    if uid not in marriages: await update.message.reply_text("انت مش متجوز اصلا"); return
    p=marriages.pop(uid)
    if p in marriages: marriages.pop(p)
    await update.message.reply_text("اتطلقت! بقيت سنجل")
async def cmd_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id
    if not context.args: await update.message.reply_text("اكتب: /chat رسالتك"); return
    msg=" ".join(context.args); sent=0
    for x in list(users.keys()):
        if x==uid: continue
        try: await context.bot.send_message(x, f"{update.effective_user.first_name}:\n\n{msg}"); sent+=1
        except: pass
    await update.message.reply_text(f"وصلت لـ {sent} واحد")
async def cmd_trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for k in stock_prices: stock_prices[k]=max(10, stock_prices[k]+random.randint(-20,30))
    txt="بورصة TRAN\n\n" + "\n".join([f"{k}: {v}" for k,v in stock_prices.items()]) + "\n\nاشتري: /buy_stock TRAN 5\nبيع: /sell_stock TRAN 5\nنصيحة: /smart"
    await update.message.reply_text(txt)
async def cmd_buy_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; u=get_user(uid)
    if len(context.args)<2: await update.message.reply_text("اكتب: /buy_stock TRAN 5"); return
    sym=context.args[0].upper(); qty=int(context.args[1]); price=stock_prices.get(sym,0)*qty
    if u["coins"]<price: await update.message.reply_text(f"محتاج {price}"); return
    u["coins"]-=price; u.setdefault("stocks",{})[sym]=u.get("stocks",{}).get(sym,0)+qty; await update.message.reply_text(f"اشتريت {qty} {sym}!\nدفعت {price}")
async def cmd_sell_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; u=get_user(uid)
    if len(context.args)<2: await update.message.reply_text("اكتب: /sell_stock TRAN 5"); return
    sym=context.args[0].upper(); qty=int(context.args[1]); have=u.get("stocks",{}).get(sym,0)
    if have<qty: await update.message.reply_text(f"معاك {have} بس"); return
    price=stock_prices.get(sym,0)*qty; u["coins"]+=price; u["stocks"][sym]-=qty; await update.message.reply_text(f"بعت {qty} {sym}!\nخدت {price}")
async def cmd_pet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; u=get_user(uid)
    if uid not in pets:
        if not context.args or context.args[0]!="buy": await update.message.reply_text("اشتري حيوان بـ 300\nاكتب: /pet buy"); return
        if u["coins"]<300: await update.message.reply_text("محتاج 300"); return
        u["coins"]-=300; pets[uid]={"name":random.choice(["ريكس","لولو","بوبو","سيمبا"]),"level":1}; await update.message.reply_text(f"اشتريت {pets[uid]['name']}!\nأكله بـ /pet feed"); return
    pet=pets[uid]
    if context.args and context.args[0]=="feed": pet["level"]+=1; r=pet["level"]*20; add_coins(uid,r,"حيوان"); await update.message.reply_text(f"أكلت {pet['name']}!\nمستوى {pet['level']}\n+{r}")
    else: await update.message.reply_text(f"حيوانك: {pet['name']}\nمستوى {pet['level']}\nأكله بـ /pet feed")
async def cmd_house(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; u=get_user(uid)
    if uid not in houses:
        if not context.args or context.args[0]!="buy": await update.message.reply_text("اشتري بيت بـ 2000\nاكتب: /house buy\nبيجيب 100 كل يوم!"); return
        if u["coins"]<2000: await update.message.reply_text("محتاج 2000"); return
        u["coins"]-=2000; houses[uid]=True; await update.message.reply_text("اشتريت بيت!\nخد ايجار كل يوم بـ /house"); return
    u["coins"]+=100; await update.message.reply_text(f"خدت ايجار +100\nمعاك: {u['coins']}")
async def cmd_car(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; u=get_user(uid)
    if uid not in cars:
        if not context.args or context.args[0]!="buy": await update.message.reply_text("اشتري عربية بـ 5000\nاكتب: /car buy\nبتجيب 200 كل يوم!"); return
        if u["coins"]<5000: await update.message.reply_text("محتاج 5000"); return
        u["coins"]-=5000; cars[uid]=True; await update.message.reply_text("اشتريت عربية!\nاشتغل اوبر بـ /car"); return
    u["coins"]+=200; await update.message.reply_text(f"اشتغلت اوبر! +200\nمعاك: {u['coins']}")
async def cmd_gym(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; u=get_user(uid); u["power"]+=5; add_coins(uid,10,"جيم"); await update.message.reply_text(f"اتمرنت!\nقوتك {u['power']}\n+10")
async def cmd_study(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; u=get_user(uid); u["edu"]+=1; await update.message.reply_text(f"ذاكرت!\nمستواك {u['edu']}")
async def cmd_battle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; u=get_user(uid)
    if len(context.args)<2: await update.message.reply_text("اكتب: /battle ID المبلغ"); return
    try:
        target=int(context.args[0]); bet=int(context.args[1])
        if u["coins"]<bet: await update.message.reply_text("معكش كفاية"); return
        tu=get_user(target)
        if tu["coins"]<bet: await update.message.reply_text("خصمك معهوش كفاية"); return
        my=random.randint(1,100)+u["level"]*5+u.get("power",10); en=random.randint(1,100)+tu["level"]*5+tu.get("power",10)
        if my>en: u["coins"]+=bet; tu["coins"]-=bet; await update.message.reply_text(f"كسبت!\n{my} vs {en}\nخدت {bet}")
        elif my<en: u["coins"]-=bet; tu["coins"]+=bet; await update.message.reply_text(f"خسرت\n{my} vs {en}\nخسرت {bet}")
        else: await update.message.reply_text("تعادل!")
    except: await update.message.reply_text("اكتب صح")
async def cmd_gift(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; u=get_user(uid)
    if len(context.args)<2: await update.message.reply_text("اكتب: /gift ID المبلغ"); return
    try:
        t=int(context.args[0]); amt=int(context.args[1])
        if u["coins"]<amt: await update.message.reply_text("معكش كفاية"); return
        u["coins"]-=amt; get_user(t)["coins"]+=amt; await update.message.reply_text(f"بعت هدية {amt} لـ {t}")
        try: await context.bot.send_message(t, f"جاتلك هدية {amt} من {update.effective_user.first_name}")
        except: pass
    except: await update.message.reply_text("اكتب صح")
async def cmd_clan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id
    if not context.args: await update.message.reply_text("اكتب: /clan اسم الكلان\nمثال: /clan الاساطير"); return
    name=" ".join(context.args); clans.setdefault(name,{"members":[]})
    if uid not in clans[name]["members"]: clans[name]["members"].append(uid); add_coins(uid,100,"كلان"); await update.message.reply_text(f"انضميت لكلان {name}!\nاعضاء: {len(clans[name]['members'])}\n+100")
    else: await update.message.reply_text(f"انت في كلان {name} خلاص")
async def cmd_race(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; u=get_user(uid); horses=["برق","رعد","صقر","نمر"]
    if not context.args: await update.message.reply_text("اختار حصان: /race 1 لـ /race 4\nالرهان 50، لو كسبت تاخد 200"); return
    try:
        pick=int(context.args[0])-1
        if u["coins"]<50: await update.message.reply_text("محتاج 50"); return
        winner=random.randint(0,3)
        if pick==winner: add_coins(uid,200,"سباق"); await update.message.reply_text(f"الفايز: {horses[winner]}\nحصانك كسب! +200")
        else: add_coins(uid,-50,"سباق"); await update.message.reply_text(f"الفايز: {horses[winner]}\nحصانك خسر -50")
    except: await update.message.reply_text("اكتب: /race 1")
async def cmd_roulette(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; u=get_user(uid)
    if not context.args: await update.message.reply_text("اكتب: /roulette احمر او /roulette اسود"); return
    choice=context.args[0]; result=random.choice(["احمر","اسود"])
    if u["coins"]<50: await update.message.reply_text("محتاج 50"); return
    if choice==result: add_coins(uid,100,"روليت"); await update.message.reply_text(f"النتيجة: {result}\nكسبت! +100")
    else: add_coins(uid,-50,"روليت"); await update.message.reply_text(f"النتيجة: {result}\nخسرت -50")
async def cmd_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("اكتب: /ai سؤالك\nمثال: /ai ازاي اكسب كوينز؟"); return
    q_text=" ".join(context.args).lower()
    if "كوينز" in q_text or "اكسب" in q_text: ans="عشان تكسب كوينز:\n1- العب\n2- المهام\n3- ادعي صحابك\n4- عدن\n5- اشتغل\n6- بيت وعربية\n7- اسرق في المافيا"
    elif "حب" in q_text or "جواز" in q_text: ans="اتجوز بـ /marry ID\nهتاخد +100 كل يوم + هدية 200"
    elif "ازيك" in q_text or "اهلا" in q_text: ans=f"اهلا بيك يا {update.effective_user.first_name}! عايز تلعب ولا تكسب ولا تتجوز ولا تسرق؟"
    elif "بنك" in q_text: ans="البنك: ايداع، سحب، قرض 500، فوايد 10% كل يوم!"
    elif "مافيا" in q_text or "سرقة" in q_text: ans="المافيا: انضم بـ /mafia، اسرق بـ /steal، لو اتمسكت ادخل السجن واطلع بـ /free، ولو عايز براءة روح المحكمة /court"
    else: ans=f"فهمتك!\nسؤالك: {q_text}\nنصيحتي: العب كتير وادعي صحابك وهتبقى غني"
    await update.message.reply_text(ans)
async def cmd_vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; u=get_user(uid)
    if u["coins"]<1000: await update.message.reply_text("محتاج 1000 كوين عشان تبقى VIP"); return
    u["coins"]-=1000; u["vip"]=True; await update.message.reply_text("بقيت VIP!\nكل ارباحك هتتضاعف x2")
async def cmd_streak(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; u=get_user(uid); u["streak"]+=1; r=u["streak"]*10; add_coins(uid,r,"سلسلة"); await update.message.reply_text(f"سلسلة دخولك: {u['streak']} يوم\n+{r}")
async def cmd_tournament(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; u=get_user(uid)
    if uid in tournaments["players"]: await update.message.reply_text(f"انت في البطولة خلاص! {len(tournaments['players'])}"); return
    if u["coins"]<100: await update.message.reply_text("البطولة بـ 100"); return
    u["coins"]-=100; tournaments["players"].append(uid); await update.message.reply_text(f"دخلت البطولة!\nلاعبين: {len(tournaments['players'])}\nالجايزة 10000")
async def cmd_tournament_win(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(tournaments["players"])<2: await update.message.reply_text("محتاج 2 على الاقل"); return
    w=random.choice(tournaments["players"]); add_coins(w,10000,"بطولة"); await update.message.reply_text(f"الفايز بالبطولة!\n{w}\nخد 10000"); tournaments["players"].clear()
async def cmd_skins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; u=get_user(uid)
    if not context.args:
        txt="متجر السكنات\n\n" + "\n".join([f"{v['name']} - {v['price']} | /skins {k}" for k,v in skins_shop.items()]) + f"\n\nسكنك: {u.get('skin','عادي')}"
        await update.message.reply_text(txt); return
    sid=context.args[0].lower()
    if sid not in skins_shop: await update.message.reply_text("سكن مش موجود"); return
    s=skins_shop[sid]
    if u["coins"]<s["price"]: await update.message.reply_text(f"محتاج {s['price']}"); return
    u["coins"]-=s["price"]; u["skin"]=s["name"]; await update.message.reply_text(f"اشتريت {s['name']}!")
async def cmd_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q=random.choice(quiz_q); context.user_data["quiz_ans"]=q["a"]
    kb=InlineKeyboardMarkup([[InlineKeyboardButton(opt, callback_data=f"quiz_{opt}")] for opt in q["opts"]])
    await update.message.reply_text(f"سؤال ذكاء\n\n{q['q']}", reply_markup=kb)
async def cmd_inventory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; u=get_user(uid); inv=[]
    if uid in pets: inv.append(f"حيوان: {pets[uid]['name']}")
    if uid in houses: inv.append("بيت")
    if uid in cars: inv.append("عربية")
    if u.get("vip"): inv.append("VIP")
    if uid in marriages: inv.append(f"متجوز {marriages[uid]}")
    if u.get("mafia"): inv.append(f"{u['mafia']}")
    if not inv: inv.append("مخزونك فاضي")
    await update.message.reply_text("مخزونك\n\n" + "\n".join(inv))
async def cmd_analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; u=get_user(uid); rate=(u["wins"]/max(1,u["games"])*100) if u["games"] else 0
    await update.message.reply_text(f"تحليل ادائك\n\nلعبت: {u['games']}\nكسبت: {u['wins']} ({rate:.0f}%)\nكسبت: {u['total_won']}\nبنك: {u['bank']}")
async def cmd_horoscope(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"حظك اليوم\n\n{random.choice(['النهاردة يوم حظك! العب كتير','هتكسب كوينز كتير','حد بيحبك هيديك هدية','حظك حلو، جرب اليانصيب','ركز في الشغل'])}")
async def cmd_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; u=get_user(uid)
    if not context.args: await update.message.reply_text(f"لقبك: {u.get('title','مفيش')}\nغيره بـ: /title الملك"); return
    title=" ".join(context.args)
    if u["coins"]<100: await update.message.reply_text("اللقب بـ 100"); return
    u["coins"]-=100; u["title"]=title; await update.message.reply_text(f"بقى لقبك: {title}")
async def cmd_insurance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; u=get_user(uid)
    if u.get("insured"): await update.message.reply_text("انت مأمن فلوسك خلاص"); return
    if u["coins"]<200: await update.message.reply_text("التأمين بـ 200"); return
    u["coins"]-=200; u["insured"]=True; await update.message.reply_text("أمنت فلوسك!")
async def cmd_league(update: Update, context: ContextTypes.DEFAULT_TYPE):
    top=sorted(users.values(), key=lambda x: x["points"], reverse=True)[:5]; txt="الدوري الاسبوعي\n\n"
    medals=["1 - 5000","2 - 3000","3 - 1500","4 - 500","5 - 200"]
    for i,u2 in enumerate(top): txt+=f"{medals[i]} - {u2.get('name','')} | {u2['points']} نقطة\n"
    await update.message.reply_text(txt)
async def cmd_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; u=get_user(uid)
    if not context.args:
        notes=u.get("notes",[]); await update.message.reply_text("مذكراتك\n\n" + ("\n".join(notes[-5:]) if notes else "فاضية - اكتب /note انا بحب TRAN")); return
    u.setdefault("notes",[]).append(" ".join(context.args)); await update.message.reply_text("حفظت مذكرتك!")
async def cmd_auction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; u=get_user(uid)
    if not context.args:
        if not auctions: await update.message.reply_text("المزاد فاضي\nاكتب: /auction المبلغ"); return
        await update.message.reply_text("المزادات:\n\n" + "\n".join([f"{a['seller']} بيبيع {a['amount']}" for a in auctions[-5:]])); return
    try:
        amt=int(context.args[0])
        if u["coins"]<amt: await update.message.reply_text("معكش كفاية"); return
        u["coins"]-=amt; auctions.append({"seller":uid,"amount":amt}); await update.message.reply_text(f"عرضت {amt} في المزاد!")
    except: await update.message.reply_text("اكتب: /auction المبلغ")
async def cmd_smart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"ذكاء التداول\n\n{random.choice(['اشتري TRAN دلوقتي، سعره هيطلع!','بيع GOLD، سعره هينزل!','BTC رخيص دلوقتي، اشتري بسرعة!','DOGE هيطلع جامد، اشتري!','متشتريش دلوقتي، السوق خطر!'])}\n\nشوف الاسعار بـ /trade")
async def cmd_challenge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ch=random.choice(["العب 3 مرات واكسب +100","ادعي 1 صاحب واكسب +150","عدن مرة واكسب +80","اشتغل مرة واكسب +120","العب نرد 5 مرات واكسب +200"])
    await update.message.reply_text(f"تحدي اليوم\n\n{ch}\n\nخلص التحدي وخد الجايزة!\nاكتب /challenge_done لما تخلصه")
async def cmd_challenge_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; r=random.randint(80,200); add_coins(uid,r,"تحدي"); await update.message.reply_text(f"خلصت التحدي!\nخدت +{r}\nعاش يا بطل!")
async def cmd_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    w=random.choice(words); context.user_data["word"]=w; hint=w[0]+" _ "*(len(w)-1); await update.message.reply_text(f"خمن الكلمة!\n\nالكلمة: {hint}\nعدد الحروف: {len(w)}\nابعت تخمينك، لو صح تاخد +40")
async def cmd_mafia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; u=get_user(uid)
    if not u.get("mafia"): u["mafia"]=random.choice(["مافيا TRAN","مافيا الصقور","مافيا الثعابين"]); add_coins(uid,200,"مافيا"); await update.message.reply_text(f"انضميت لـ {u['mafia']}!\n+200\n\nاسرق بـ /steal، اهرب بـ /escape، شوف سجنك بـ /jail")
    else: await update.message.reply_text(f"انت في {u['mafia']} خلاص\nاسرق بـ /steal")
async def cmd_steal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; u=get_user(uid)
    if uid in jailed: await update.message.reply_text("انت في السجن! اكتب /free عشان تطلع"); return
    if random.random()<0.3: u["wanted"]+=1; jailed[uid]=True; await update.message.reply_text(f"اتمسكت!\nدخلت السجن!\nمطلوب: {u['wanted']}\nاطلع بـ /free (200) او روح المحكمة /court"); return
    stolen=random.randint(50,300); add_coins(uid,stolen,"سرقة"); await update.message.reply_text(f"سرقت! +{stolen}\nمحدش شافك\nمعاك: {u['coins']}")
async def cmd_rob(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; u=get_user(uid)
    if len(context.args)<1: await update.message.reply_text("اكتب: /rob ID\nمثال: /rob 123456"); return
    try:
        target=int(context.args[0]); tu=get_user(target)
        if tu["coins"]<50: await update.message.reply_text("الضحية معهوش فلوس"); return
        if random.random()<0.4: u["wanted"]+=1; jailed[uid]=True; await update.message.reply_text("اتمسكت وانت بتسرق صاحبك!\nدخلت السجن! /free عشان تطلع"); return
        stolen=random.randint(20,min(200,tu["coins"])); tu["coins"]-=stolen; u["coins"]+=stolen; await update.message.reply_text(f"سرقت {stolen} من {target}!\nمعاك: {u['coins']}")
        try: await context.bot.send_message(target, f"حد سرقك! خسرت {stolen}\nاللي سرقك: {update.effective_user.first_name}")
        except: pass
    except: await update.message.reply_text("اكتب: /rob ID")
async def cmd_jail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id
    if uid in jailed: await update.message.reply_text("انت في السجن!\nاطلع بـ /free (200) او استنى المحكمة /court")
    else: await update.message.reply_text("انت حر! مش في السجن")
async def cmd_free(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; u=get_user(uid)
    if uid not in jailed: await update.message.reply_text("انت مش في السجن اصلا"); return
    if u["coins"]<200: await update.message.reply_text("الكفالة 200، معكش كفاية"); return
    u["coins"]-=200; jailed.pop(uid,None); await update.message.reply_text("طلعت من السجن!\nدفعت كفالة 200\nانت حر دلوقتي")
async def cmd_court(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; u=get_user(uid)
    if u.get("wanted",0)==0: await update.message.reply_text("انت بريء! معلكش حاجة"); return
    if random.random()<0.5: u["wanted"]=0; jailed.pop(uid,None); await update.message.reply_text("براءة!\nالقاضي طلعك براءة!")
    else: await update.message.reply_text(f"ادانة!\nعليك غرامة 300\nمطلوب: {u['wanted']}")
async def cmd_escape(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id
    if uid not in jailed: await update.message.reply_text("انت مش في السجن"); return
    if random.random()<0.5: jailed.pop(uid,None); await update.message.reply_text("هربت من السجن!\nانت حر دلوقتي، بس البوليس بيدور عليك!")
    else: await update.message.reply_text("فشلت تهرب!\nالحارس مسكك، حاول تاني")
async def cmd_smuggle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; u=get_user(uid)
    if u["coins"]<100: await update.message.reply_text("التهريب محتاج 100 رأس مال"); return
    if random.random()<0.4: u["coins"]-=100; u["wanted"]+=1; await update.message.reply_text("اتمسكت وانت بتهرب!\nخسرت 100 وبقيت مطلوب!"); return
    profit=random.randint(200,500); add_coins(uid,profit,"تهريب"); await update.message.reply_text(f"هربت بضاعة!\nكسبت +{profit}\nمعاك: {u['coins']}")
async def cmd_badges(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; u=get_user(uid); badges=[]
    if u["games"]>=10: badges.append("محترف العاب")
    if u["ref"]>=5: badges.append("ملك الدعوات")
    if u["coins"]>=5000: badges.append("غني")
    if u.get("vip"): badges.append("VIP")
    if uid in marriages: badges.append("متجوز")
    if u.get("mafia"): badges.append("مافيا")
    if not badges: badges.append("مفيش اوسمة لسه، العب واكسب!")
    await update.message.reply_text("اوسمتك\n\n" + "\n".join(badges))
async def cmd_clanwar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id
    if not clans: await update.message.reply_text("مفيش كلانات، اعمل كلان الاول بـ /clan اسم"); return
    my=random.randint(50,150); en=random.randint(50,150)
    if my>en: add_coins(uid,300,"حرب كلان"); await update.message.reply_text(f"كلانك كسب الحرب!\n{my} vs {en}\n+300")
    else: await update.message.reply_text(f"كلانك خسر الحرب\n{my} vs {en}")
async def cmd_golddice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; u=get_user(uid)
    if not u.get("vip"): await update.message.reply_text("النرد الذهبي للـ VIP بس!\nاكتب /vip"); return
    r=random.randint(1,6)
    if r>=3: add_coins(uid,100,"نرد ذهبي"); await update.message.reply_text(f"النرد الذهبي: {r}\nكسبت +100!")
    else: add_coins(uid,-20,"نرد ذهبي"); await update.message.reply_text(f"النرد الذهبي: {r}\nخسرت -20")
async def cmd_randomgift(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not users: return
    w=random.choice(list(users.keys())); prize=random.randint(50,300); add_coins(w,prize,"هدية عشوائية")
    try: await context.bot.send_message(w, f"جاتلك هدية عشوائية!\n+{prize}")
    except: pass
    await update.message.reply_text(f"هدية عشوائية راحت لـ {w} +{prize}")

async def on_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        uid=update.effective_user.id; txt=(update.message.text or "").strip(); u=get_user(uid)
        if txt=="تصفير" and uid==OWNER_ID: users.clear(); await update.message.reply_text("اتصفر كله"); return
        if context.user_data.get("wait_broadcast") and uid==OWNER_ID:
            context.user_data["wait_broadcast"]=False; c=0
            for x in list(users.keys()):
                try: await context.bot.send_message(x, f"من الادارة:\n\n{txt}"); c+=1
                except: pass
            await update.message.reply_text(f"اتبعت لـ {c}"); return
        if context.user_data.get("wait_add") and uid==OWNER_ID:
            context.user_data["wait_add"]=False
            try: t,a=map(int,txt.split()); get_user(t); add_coins(t,a,"اونر"); await update.message.reply_text(f"ضفت {a} لـ {t}")
            except: await update.message.reply_text("اكتب صح: ID المبلغ")
            return
        if context.user_data.get("wait_remove") and uid==OWNER_ID:
            context.user_data["wait_remove"]=False
            try: t,a=map(int,txt.split()); get_user(t); add_coins(t,-a,"خصم"); await update.message.reply_text(f"خصمت {a} من {t}")
            except: await update.message.reply_text("اكتب صح")
            return
        if context.user_data.get("wait_ban") and uid==OWNER_ID:
            context.user_data["wait_ban"]=False
            try: t=int(txt); get_user(t); users[t]["banned"]=not users[t]["banned"]; await update.message.reply_text(f"{'حظرته' if users[t]['banned'] else 'فكيت حظره'} {t}")
            except: await update.message.reply_text("ID غلط")
            return
        if context.user_data.get("wait_view") and uid==OWNER_ID:
            context.user_data["wait_view"]=False
            try: t=int(txt); uu=get_user(t); await update.message.reply_text(f"{uu['name']}\nID: {t}\nكوينز: {uu['coins']} | بنك: {uu['bank']}\nمحظور: {uu['banned']}\nمافيا: {uu.get('mafia')}")
            except: await update.message.reply_text("مش موجود")
            return
        if context.user_data.get("wait_transfer"):
            context.user_data["wait_transfer"]=False
            try:
                t,a=map(int,txt.split())
                if u["coins"]<a: await update.message.reply_text("معكش كفاية"); return
                get_user(t); u["coins"]-=a; users[t]["coins"]+=a; await update.message.reply_text(f"حولت {a} لـ {t}")
                try: await context.bot.send_message(t, f"وصلك {a} من {update.effective_user.first_name}")
                except: pass
            except: await update.message.reply_text("اكتب: ID المبلغ")
            return
        if context.user_data.get("guess") is not None:
            n=context.user_data.pop("guess")
            try:
                g=int(txt)
                if g==n: add_coins(uid,50,"تخمين"); await update.message.reply_text(f"صح! الرقم كان {n} +50")
                else: add_coins(uid,-10,"تخمين"); await update.message.reply_text(f"غلط! الرقم كان {n} -10")
            except: await update.message.reply_text("ابعت رقم")
            return
        if context.user_data.get("word") is not None:
            w=context.user_data.pop("word")
            if txt==w: add_coins(uid,40,"كلمة"); await update.message.reply_text("صح! +40")
            else: await update.message.reply_text(f"غلط! الكلمة كانت {w}")
            return
        if context.user_data.get("wait_code"):
            context.user_data["wait_code"]=False; code=txt.upper()
            if code in codes: r=codes.pop(code); add_coins(uid,r,"كود"); await update.message.reply_text(f"خدت +{r}")
            else: await update.message.reply_text("كود غلط")
            return
        if context.user_data.get("wait_support"):
            context.user_data["wait_support"]=False; await update.message.reply_text("وصلت للاونر", reply_markup=main_menu(uid))
            try: await context.bot.send_message(OWNER_ID, f"من {update.effective_user.first_name} ({uid}):\n{txt}")
            except: pass
            return
        await update.message.reply_text("اكتب /start", reply_markup=main_menu(uid))
    except Exception as e:
        print(f"MSG ERROR: {e}")

async def on_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q=update.callback_query; await q.answer()
    if q.data.startswith("quiz_"):
        ans=q.data.replace("quiz_","")
        if ans==context.user_data.get("quiz_ans"): add_coins(q.from_user.id,40,"quiz"); await q.edit_message_text("صح! +40")
        else: await q.edit_message_text(f"غلط! الصح كان {context.user_data.get('quiz_ans')}")

def main():
    app=ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("owner", start))
    for cmd, fn in [("mine",cmd_mine),("work",cmd_work),("box",cmd_box),("lottery",cmd_lottery),("lottery_draw",cmd_lottery_draw),("marry",cmd_marry),("divorce",cmd_divorce),("chat",cmd_chat),("trade",cmd_trade),("buy_stock",cmd_buy_stock),("sell_stock",cmd_sell_stock),("pet",cmd_pet),("house",cmd_house),("car",cmd_car),("gym",cmd_gym),("study",cmd_study),("battle",cmd_battle),("gift",cmd_gift),("clan",cmd_clan),("race",cmd_race),("roulette",cmd_roulette),("ai",cmd_ai),("vip",cmd_vip),("streak",cmd_streak),("tournament",cmd_tournament),("tournament_win",cmd_tournament_win),("skins",cmd_skins),("quiz",cmd_quiz),("inventory",cmd_inventory),("analyze",cmd_analyze),("horoscope",cmd_horoscope),("title",cmd_title),("insurance",cmd_insurance),("league",cmd_league),("note",cmd_note),("auction",cmd_auction),("smart",cmd_smart),("challenge",cmd_challenge),("challenge_done",cmd_challenge_done),("word",cmd_word),("mafia",cmd_mafia),("steal",cmd_steal),("rob",cmd_rob),("jail",cmd_jail),("free",cmd_free),("court",cmd_court),("escape",cmd_escape),("smuggle",cmd_smuggle),("badges",cmd_badges),("clanwar",cmd_clanwar),("golddice",cmd_golddice),("randomgift",cmd_randomgift)]:
        app.add_handler(CommandHandler(cmd, fn))
    app.add_handler(CallbackQueryHandler(on_quiz, pattern="^quiz_"))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_msg))
    print("TRAN FINAL FIXED STARTED")
    app.run_polling()
if __name__=="__main__": main()
