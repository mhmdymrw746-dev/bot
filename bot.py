# TRAN BANK PRO - FULL FINAL + SUPPORT
import os, random, time, threading
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from flask import Flask
import requests

TOKEN = os.environ.get("BOT_TOKEN")
OWNER_ID = int(os.environ.get("OWNER_ID", "8188263997"))

# ===== خدمة العملاء =====
# 7125945857 = Mr cat
# 7737976057 = تيتو
SUPPORT_IDS = [8188263997, 7125945857, 7737976057]
SUPPORT_INFO = {
    7125945857: {"name": "Mr cat", "username": "@cat_max_10", "phone": "+20 115 5973454"},
    7737976057: {"name": "تيتو", "username": "@MOON_104", "phone": "+20 111 8093542"},
}
def is_support(uid):
    return int(uid) in SUPPORT_IDS

app_flask = Flask(__name__)
@app_flask.route('/')
def home(): return "TRAN BANK PRO ALIVE"
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

users = {}
checks = {}
joint_accounts = {}
tickets = {}
ticket_counter = [100]

RATES = {"EGP":1, "USD":50, "EUR":55, "GOLD":100, "BTC":2000}
BILLS = {"نت":100, "كهربا":150, "شحن":50, "غاز":80, "مياه":60}

def get_user(uid, username="", name=""):
    uid=int(uid)
    if uid not in users:
        users[uid]={"id":uid,"username":username,"name":name,"cash":1000,"bank":0,"savings":0,"loan":0,"loan_due":0,"loan_left":0,"loan_total":0,"points":0,"banned":False,"vip":False,"insured":False,"credit_limit":1000,"credit_used":0,"card_num":f"5335 {random.randint(1000,9999)} {random.randint(1000,9999)} {random.randint(1000,9999)}","credit_num":f"4111 {random.randint(1000,9999)} {random.randint(1000,9999)} {random.randint(1000,9999)}","history":[],"last_interest":"","last_daily":"","certs":[],"deposits":[],"loan_history":[],"daily_withdraw":0,"daily_date":"","joint":None,"currency":"EGP"}
    return users[uid]

def add_h(uid, txt):
    u=get_user(uid); u["history"].append(f"{datetime.now().strftime('%d/%m %H:%M')} - {txt}"); u["history"]=u["history"][-20:]

def main_menu(uid):
    kb=[
        [InlineKeyboardButton("💰 رصيدي", callback_data="balance"), InlineKeyboardButton("🏦 البنك", callback_data="bank")],
        [InlineKeyboardButton("💳 فيزا", callback_data="visa"), InlineKeyboardButton("📜 كشف حساب", callback_data="history")],
        [InlineKeyboardButton("🏆 شهادات", callback_data="certs"), InlineKeyboardButton("💸 وديعة", callback_data="deposit_acc")],
        [InlineKeyboardButton("💰 قرض", callback_data="loan"), InlineKeyboardButton("💳 كريديت", callback_data="credit")],
        [InlineKeyboardButton("💱 عملات", callback_data="currency"), InlineKeyboardButton("🧾 فواتير", callback_data="bills")],
        [InlineKeyboardButton("✉️ شيك", callback_data="check_menu"), InlineKeyboardButton("👨‍👩‍👧 حساب مشترك", callback_data="joint")],
        [InlineKeyboardButton("🏧 ATM", callback_data="atm"), InlineKeyboardButton("🐷 تحويش", callback_data="saving")],
        [InlineKeyboardButton("🎁 هدية يومية", callback_data="daily"), InlineKeyboardButton("🏆 الاغنياء", callback_data="top")],
        [InlineKeyboardButton("☎️ خدمة العملاء", callback_data="support_menu"), InlineKeyboardButton("❓ اسئلة شائعة", callback_data="faq")],
        [InlineKeyboardButton("🎲 حظ", callback_data="luck"), InlineKeyboardButton("🛡️ تأمين", callback_data="insurance")],
        [InlineKeyboardButton("💎 VIP", callback_data="vip"), InlineKeyboardButton("🎫 تيكتاتي", callback_data="my_tickets")],
    ]
    if is_support(uid):
        kb.append([InlineKeyboardButton("🎧 لوحة خدمة العملاء", callback_data="support_panel")])
    if int(uid)==OWNER_ID:
        kb.append([InlineKeyboardButton("👑 لوحة الاونر", callback_data="owner")])
    kb.append([InlineKeyboardButton("🔄 تحديث", callback_data="back")])
    return InlineKeyboardMarkup(kb)

def back(): return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ رجوع", callback_data="back")]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        u=update.effective_user; user=get_user(u.id, u.username or "", u.first_name or "")
        if user["banned"]:
            await update.message.reply_text("انت محظور من البنك"); return
        txt=f"اهلا {u.first_name} في بنك TRAN PRO 🏦\n\n💰 كاش: {user['cash']}\n🏦 بنك: {user['bank']}\n🐷 تحويش: {user['savings']}\n📊 الكلي: {user['cash']+user['bank']+user['savings']}\n💸 قرض: {user['loan']} | متبقي {user['loan_left']} قسط\n💳 كريديت: {user['credit_used']}/{user['credit_limit']}\n⭐ نقاط: {user['points']}\n💱 عملة: {user['currency']}\n\nاختار من القايمة 👇\n\nاوامر سريعة:\n/deposit 100 - ايداع\n/withdraw 100 - سحب\n/transfer ID المبلغ - تحويل\n/balance - رصيد\n/visa - فيزا\n/top - الاغنياء"
        await update.message.reply_text(txt, reply_markup=main_menu(u.id))
    except Exception as e:
        print(f"START ERROR: {e}")
        try: await update.message.reply_text("اهلا في بنك TRAN PRO 🏦", reply_markup=main_menu(update.effective_user.id))
        except: pass

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q=update.callback_query
    try: await q.answer()
    except: pass
    uid=q.from_user.id; user=get_user(uid, q.from_user.username or "", q.from_user.first_name or ""); data=q.data
    try:
        if data=="back":
            await q.edit_message_text(f"بنك TRAN PRO 🏦\n\nكاش: {user['cash']} | بنك: {user['bank']} | تحويش: {user['savings']}\nالكلي: {user['cash']+user['bank']+user['savings']}\nقرض: {user['loan']} | كريديت: {user['credit_used']}/{user['credit_limit']}", reply_markup=main_menu(uid)); return
        if data=="balance":
            await q.edit_message_text(f"رصيدك 💰\n\nكاش: {user['cash']}\nبنك: {user['bank']}\nتحويش: {user['savings']}\nالكلي: {user['cash']+user['bank']+user['savings']}\nقرض: {user['loan']} | متبقي اقساط: {user['loan_left']}\nكريديت مستخدم: {user['credit_used']}/{user['credit_limit']}\nشهادات: {len(user['certs'])} | ودائع: {len(user['deposits'])}\nعملة: {user['currency']}\nنقاط: {user['points']}", reply_markup=back()); return
        if data=="bank":
            kb=InlineKeyboardMarkup([[InlineKeyboardButton("ايداع 100", callback_data="dep_100"), InlineKeyboardButton("ايداع 500", callback_data="dep_500")],[InlineKeyboardButton("ايداع 1000", callback_data="dep_1000"), InlineKeyboardButton("ايداع الكل", callback_data="dep_all")],[InlineKeyboardButton("سحب 100", callback_data="wd_100"), InlineKeyboardButton("سحب 500", callback_data="wd_500")],[InlineKeyboardButton("سحب 1000", callback_data="wd_1000"), InlineKeyboardButton("سحب الكل", callback_data="wd_all")],[InlineKeyboardButton("تحويل", callback_data="do_transfer"), InlineKeyboardButton("فوايد", callback_data="interest")],[InlineKeyboardButton("رجوع", callback_data="back")]])
            await q.edit_message_text(f"البنك 🏦\nكاش: {user['cash']} | بنك: {user['bank']}\nحد السحب اليومي: {user['daily_withdraw']}/5000", reply_markup=kb); return
        if data.startswith("dep_"):
            amt=user["cash"] if data=="dep_all" else int(data.replace("dep_",""))
            if user["cash"]<amt or amt<=0: await q.edit_message_text("معكش كفاية", reply_markup=back()); return
            user["cash"]-=amt; user["bank"]+=amt; user["points"]+=1; add_h(uid,f"ايداع +{amt}"); await q.edit_message_text(f"ايداع تم ✅\nبنك: {user['bank']} | كاش: {user['cash']}", reply_markup=back()); return
        if data.startswith("wd_"):
            amt=user["bank"] if data=="wd_all" else int(data.replace("wd_",""))
            today=datetime.now().strftime("%Y-%m-%d")
            if user["daily_date"]!=today: user["daily_date"]=today; user["daily_withdraw"]=0
            if user["daily_withdraw"]+amt>5000: await q.edit_message_text(f"عديت حد السحب اليومي 5000\nسحبت النهاردة: {user['daily_withdraw']}", reply_markup=back()); return
            if user["bank"]<amt: await q.edit_message_text("معكش في البنك", reply_markup=back()); return
            user["bank"]-=amt; user["cash"]+=amt; user["daily_withdraw"]+=amt; add_h(uid,f"سحب -{amt}"); await q.edit_message_text(f"سحب تم ✅\nكاش: {user['cash']} | بنك: {user['bank']}\nسحبت النهاردة: {user['daily_withdraw']}/5000", reply_markup=back()); return
        if data=="do_transfer": context.user_data["wait_transfer"]=True; await q.edit_message_text("اكتب: ID المبلغ\nمثال: 123456 100", reply_markup=back()); return
        if data=="interest":
            today=datetime.now().strftime("%Y-%m-%d")
            if user["last_interest"]==today: await q.edit_message_text("خدت فوايدك النهاردة", reply_markup=back()); return
            if user["bank"]<=0 and user["savings"]<=0: await q.edit_message_text("حط فلوس في البنك الاول", reply_markup=back()); return
            user["last_interest"]=today; ib=int(user["bank"]*0.10); isv=int(user["savings"]*0.20)
            user["bank"]+=ib; user["savings"]+=isv; add_h(uid,f"فوايد مركبة +{ib+isv}"); await q.edit_message_text(f"فوايد مركبة 📈\nبنك +{ib} | تحويش +{isv}\nالكلي +{ib+isv}\nبنك: {user['bank']}", reply_markup=back()); return
        if data=="visa": await q.edit_message_text(f"فيزا TRAN 💳\n\n{ q.from_user.first_name}\n{user['card_num']}\nانتهاء: 12/30 | CVV: {random.randint(100,999)}\nرصيد: {user['bank']}\nنوع: {'VIP 💎' if user['vip'] else 'عادية'}", reply_markup=back()); return
        if data=="history": await q.edit_message_text("كشف حساب 📜\n\n"+("\n".join(user["history"][-15:]) or "مفيش حركات"), reply_markup=back()); return
        if data=="certs":
            kb=InlineKeyboardMarkup([[InlineKeyboardButton("شهادة 500 - 7 ايام = 750", callback_data="cert_500")],[InlineKeyboardButton("شهادة 1000 - 7 ايام = 1500", callback_data="cert_1000")],[InlineKeyboardButton("شهادة 5000 - 7 ايام = 8000", callback_data="cert_5000")],[InlineKeyboardButton("فك شهاداتي", callback_data="cert_claim")],[InlineKeyboardButton("رجوع", callback_data="back")]])
            await q.edit_message_text(f"شهادات ادخار 🏆\n\nعندك: {len(user['certs'])} شهادة\nحط فلوس وخدها بفايدة كبيرة بعد 7 ايام", reply_markup=kb); return
        if data.startswith("cert_") and data!="cert_claim":
            amt=int(data.replace("cert_",""))
            if user["bank"]<amt: await q.edit_message_text("معكش في البنك كفاية", reply_markup=back()); return
            user["bank"]-=amt; user["certs"].append({"amt":amt,"until":datetime.now()+timedelta(days=7),"reward":int(amt*1.5)}); add_h(uid,f"شهادة -{amt}"); await q.edit_message_text(f"عملت شهادة {amt} ✅\nهتاخد {int(amt*1.5)} بعد 7 ايام", reply_markup=back()); return
        if data=="cert_claim":
            now=datetime.now(); claimed=0; new_certs=[]
            for c in user["certs"]:
                if now>=c["until"]: claimed+=c["reward"]
                else: new_certs.append(c)
            user["certs"]=new_certs
            if claimed==0: await q.edit_message_text("لسه مفيش شهادة خلصت، استنى 7 ايام", reply_markup=back()); return
            user["bank"]+=claimed; add_h(uid,f"فك شهادة +{claimed}"); await q.edit_message_text(f"فكيت شهاداتك ✅\nخدت +{claimed}\nبنك: {user['bank']}", reply_markup=back()); return
        if data=="deposit_acc":
            kb=InlineKeyboardMarkup([[InlineKeyboardButton("وديعة 1000 - 3 ايام = 1300", callback_data="depacc_1000")],[InlineKeyboardButton("وديعة 5000 - 3 ايام = 7000", callback_data="depacc_5000")],[InlineKeyboardButton("فك وديعتي", callback_data="depacc_claim")],[InlineKeyboardButton("رجوع", callback_data="back")]])
            await q.edit_message_text(f"وديعة ثابتة 💸\nعندك: {len(user['deposits'])} وديعة\nالوديعة بتتقفل 3 ايام", reply_markup=kb); return
        if data.startswith("depacc_") and data!="depacc_claim":
            amt=int(data.replace("depacc_",""))
            if user["bank"]<amt: await q.edit_message_text("معكش في البنك", reply_markup=back()); return
            user["bank"]-=amt; user["deposits"].append({"amt":amt,"until":datetime.now()+timedelta(days=3),"reward":int(amt*1.3)}); add_h(uid,f"وديعة -{amt}"); await q.edit_message_text(f"عملت وديعة {amt} ✅\nهتاخد {int(amt*1.3)} بعد 3 ايام", reply_markup=back()); return
        if data=="depacc_claim":
            now=datetime.now(); claimed=0; new_d=[]
            for d in user["deposits"]:
                if now>=d["until"]: claimed+=d["reward"]
                else: new_d.append(d)
            user["deposits"]=new_d
            if claimed==0: await q.edit_message_text("لسه الوديعة مخلصتش، استنى 3 ايام", reply_markup=back()); return
            user["bank"]+=claimed; add_h(uid,f"فك وديعة +{claimed}"); await q.edit_message_text(f"فكيت وديعتك +{claimed} ✅\nبنك: {user['bank']}", reply_markup=back()); return
        if data=="loan":
            kb=InlineKeyboardMarkup([[InlineKeyboardButton("قرض 500 - قسط 183 x3", callback_data="loan_500")],[InlineKeyboardButton("قرض 1000 - قسط 366 x3", callback_data="loan_1000")],[InlineKeyboardButton("قرض 5000 - قسط 1833 x3", callback_data="loan_5000")],[InlineKeyboardButton("سدد قسط", callback_data="loan_pay")],[InlineKeyboardButton("سدد الكل", callback_data="loan_payall")],[InlineKeyboardButton("سجل قروضي", callback_data="loan_hist")],[InlineKeyboardButton("رجوع", callback_data="back")]])
            await q.edit_message_text(f"القروض 💸\nعليك: {user['loan']}\nمتبقي اقساط: {user['loan_left']} / {user['loan_total']}\nالقسط: {user['loan_due']}\nالقرض بيتقسط على 3 دفعات", reply_markup=kb); return
        if data.startswith("loan_") and data not in ["loan_pay","loan_payall","loan_hist"]:
            amt=int(data.replace("loan_",""))
            if user["loan"]>0: await q.edit_message_text("عليك قرض سدده الاول", reply_markup=back()); return
            total=int(amt*1.1); user["cash"]+=amt; user["loan"]=amt; user["loan_total"]=total; user["loan_left"]=3; user["loan_due"]=total//3; add_h(uid,f"قرض +{amt}"); await q.edit_message_text(f"خدت قرض {amt} ✅\nهترجع {total} على 3 اقساط\nكل قسط {total//3}", reply_markup=back()); return
        if data=="loan_pay":
            if user["loan"]<=0: await q.edit_message_text("معلكش قروض", reply_markup=back()); return
            if user["cash"]<user["loan_due"]: await q.edit_message_text(f"محتاج {user['loan_due']} للقسط", reply_markup=back()); return
            user["cash"]-=user["loan_due"]; user["loan_left"]-=1; add_h(uid,f"سدد قسط -{user['loan_due']}")
            if user["loan_left"]<=0: user["loan_history"].append(f"قرض {user['loan']} اتسدد"); user["loan"]=0; user["loan_due"]=0; user["loan_total"]=0; await q.edit_message_text("سددت القرض كله! انت حر ✅", reply_markup=back()); return
            await q.edit_message_text(f"سددت قسط ✅\nمتبقي {user['loan_left']} اقساط", reply_markup=back()); return
        if data=="loan_payall":
            if user["loan"]<=0: await q.edit_message_text("معلكش قروض", reply_markup=back()); return
            rest=user["loan_due"]*user["loan_left"]
            if user["cash"]<rest: await q.edit_message_text(f"محتاج {rest} عشان تسدد الكل", reply_markup=back()); return
            user["cash"]-=rest; user["loan_history"].append(f"قرض {user['loan']} اتسدد كله"); user["loan"]=0; user["loan_due"]=0; user["loan_total"]=0; user["loan_left"]=0; add_h(uid,f"سدد قرض كله -{rest}"); await q.edit_message_text("سددت القرض كله! ✅", reply_markup=back()); return
        if data=="loan_hist": await q.edit_message_text("سجل قروضك 📜\n\n"+("\n".join(user["loan_history"]) or "مفيش قروض قديمة"), reply_markup=back()); return
        if data=="credit":
            kb=InlineKeyboardMarkup([[InlineKeyboardButton("اشتري بالكريديت 100", callback_data="credit_use_100"), InlineKeyboardButton("اشتري 500", callback_data="credit_use_500")],[InlineKeyboardButton("سدد الكريديت", callback_data="credit_pay")],[InlineKeyboardButton("رجوع", callback_data="back")]])
            await q.edit_message_text(f"كريديت كارد 💳\n\n{user['credit_num']}\nالحد: {user['credit_limit']}\nمستخدم: {user['credit_used']}\nالمتاح: {user['credit_limit']-user['credit_used']}\n\nاشتري بالدين وسدد بعدين", reply_markup=kb); return
        if data.startswith("credit_use_"):
            amt=int(data.replace("credit_use_",""))
            if user["credit_used"]+amt>user["credit_limit"]: await q.edit_message_text("عديت حد الكريديت", reply_markup=back()); return
            user["credit_used"]+=amt; user["cash"]+=amt; add_h(uid,f"كريديت +{amt}"); await q.edit_message_text(f"اشتريت بالكريديت +{amt} ✅\nكاش: {user['cash']}", reply_markup=back()); return
        if data=="credit_pay":
            if user["credit_used"]<=0: await q.edit_message_text("معلكش كريديت", reply_markup=back()); return
            if user["cash"]<user["credit_used"]: await q.edit_message_text(f"محتاج {user['credit_used']} عشان تسدد", reply_markup=back()); return
            user["cash"]-=user["credit_used"]; add_h(uid,f"سدد كريديت -{user['credit_used']}"); user["credit_used"]=0; await q.edit_message_text("سددت الكريديت كله! ✅", reply_markup=back()); return
        if data=="currency":
            txt="تحويل عملات 💱\n\n"+"\n".join([f"{k} = {v} كوينز" for k,v in RATES.items()])+"\n\nاختار عملتك:"
            kb=InlineKeyboardMarkup([[InlineKeyboardButton("EGP جنيه", callback_data="curr_EGP"), InlineKeyboardButton("USD دولار", callback_data="curr_USD")],[InlineKeyboardButton("EUR يورو", callback_data="curr_EUR"), InlineKeyboardButton("GOLD ذهب", callback_data="curr_GOLD")],[InlineKeyboardButton("BTC بيتكوين", callback_data="curr_BTC")],[InlineKeyboardButton("حول 100 كوينز لدولار", callback_data="convert_100")],[InlineKeyboardButton("رجوع", callback_data="back")]])
            await q.edit_message_text(txt, reply_markup=kb); return
        if data.startswith("curr_"): user["currency"]=data.replace("curr_",""); await q.edit_message_text(f"بقت عملتك: {user['currency']} ✅", reply_markup=back()); return
        if data=="convert_100":
            if user["cash"]<100: await q.edit_message_text("معكش 100", reply_markup=back()); return
            user["cash"]-=100; usd=100//RATES["USD"]; user["cash"]+=usd*2; await q.edit_message_text(f"حولت 100 كوينز\nخدت {usd} دولار = {usd*2} كوينز بونص", reply_markup=back()); return
        if data=="bills":
            kb=InlineKeyboardMarkup([[InlineKeyboardButton(f"نت - {BILLS['نت']}", callback_data="bill_نت"), InlineKeyboardButton(f"كهربا - {BILLS['كهربا']}", callback_data="bill_كهربا")],[InlineKeyboardButton(f"شحن - {BILLS['شحن']}", callback_data="bill_شحن"), InlineKeyboardButton(f"غاز - {BILLS['غاز']}", callback_data="bill_غاز")],[InlineKeyboardButton(f"مياه - {BILLS['مياه']}", callback_data="bill_مياه")],[InlineKeyboardButton("رجوع", callback_data="back")]])
            await q.edit_message_text(f"فواتير 🧾\nكاش: {user['cash']}\nادفع فاتورتك من هنا", reply_markup=kb); return
        if data.startswith("bill_"):
            b=data.replace("bill_",""); price=BILLS.get(b,100)
            if user["cash"]<price: await q.edit_message_text("معكش كفاية", reply_markup=back()); return
            user["cash"]-=price; user["points"]+=5; add_h(uid,f"فاتورة {b} -{price}"); await q.edit_message_text(f"دفعت فاتورة {b} -{price} ✅\nكاش: {user['cash']} | +5 نقاط", reply_markup=back()); return
        if data=="check_menu":
            kb=InlineKeyboardMarkup([[InlineKeyboardButton("اعمل شيك", callback_data="check_make"), InlineKeyboardButton("اصرف شيك", callback_data="check_claim")],[InlineKeyboardButton("رجوع", callback_data="back")]])
            await q.edit_message_text("الشيكات ✉️\nاعمل شيك لصاحبك، يصرفه بعد يوم وياخد فلوسه", reply_markup=kb); return
        if data=="check_make": context.user_data["wait_check"]=True; await q.edit_message_text("اكتب: ID المبلغ\nمثال: 123456 200", reply_markup=back()); return
        if data=="check_claim":
            found=False
            for code, c in list(checks.items()):
                if c["to"]==uid:
                    if datetime.now()>=c["until"]: user["cash"]+=c["amt"]; add_h(uid,f"صرفت شيك +{c['amt']}"); del checks[code]; await q.edit_message_text(f"صرفت شيك +{c['amt']} ✅\nكاش: {user['cash']}", reply_markup=back()); found=True; break
                    else: await q.edit_message_text("الشيك لسه ميعاده مجاش، استنى يوم", reply_markup=back()); found=True; break
            if not found: await q.edit_message_text("مفيش شيكات ليك", reply_markup=back()); return
        if data=="joint":
            if user.get("joint"): await q.edit_message_text(f"عندك حساب مشترك\nرصيده: {joint_accounts.get(user['joint'],{}).get('balance',0)}", reply_markup=back()); return
            context.user_data["wait_joint"]=True; await q.edit_message_text("اكتب ID صاحبك عشان تعملوا حساب مشترك", reply_markup=back()); return
        if data=="atm":
            kb=InlineKeyboardMarkup([[InlineKeyboardButton("اسحب من ATM 100 - عمولة 5", callback_data="atm_100"), InlineKeyboardButton("اسحب 500 - عمولة 10", callback_data="atm_500")],[InlineKeyboardButton("رجوع", callback_data="back")]])
            await q.edit_message_text(f"ATM 🏧\nبنك: {user['bank']}\nالسحب من ATM بعمولة بس سريع", reply_markup=kb); return
        if data.startswith("atm_"):
            amt=int(data.replace("atm_","")); fee=5 if amt==100 else 10
            if user["bank"]<amt+fee: await q.edit_message_text(f"محتاج {amt+fee} في البنك", reply_markup=back()); return
            user["bank"]-=amt+fee; user["cash"]+=amt; add_h(uid,f"ATM سحب -{amt} عمولة -{fee}"); await q.edit_message_text(f"سحبت من ATM {amt} ✅\nعمولة {fee}\nكاش: {user['cash']}", reply_markup=back()); return
        if data=="saving":
            kb=InlineKeyboardMarkup([[InlineKeyboardButton("حوش 500", callback_data="save_500"), InlineKeyboardButton("حوش 1000", callback_data="save_1000")],[InlineKeyboardButton("فك التحويش", callback_data="unsave")],[InlineKeyboardButton("رجوع", callback_data="back")]])
            await q.edit_message_text(f"تحويش 🐷\nحوشت: {user['savings']}\nبيجيب 20% كل يوم", reply_markup=kb); return
        if data.startswith("save_"):
            amt=int(data.replace("save_",""))
            if user["bank"]<amt: await q.edit_message_text("معكش في البنك", reply_markup=back()); return
            user["bank"]-=amt; user["savings"]+=amt; add_h(uid,f"تحويش +{amt}"); await q.edit_message_text(f"حوشت {amt} ✅\nتحويش: {user['savings']}", reply_markup=back()); return
        if data=="unsave":
            if user["savings"]<=0: await q.edit_message_text("مفيش تحويش", reply_markup=back()); return
            amt=user["savings"]; user["savings"]=0; user["bank"]+=amt; await q.edit_message_text(f"فكيت {amt} للبنك ✅", reply_markup=back()); return
        if data=="daily":
            today=datetime.now().strftime("%Y-%m-%d")
            if user["last_daily"]==today: await q.edit_message_text("خدتها النهاردة", reply_markup=back()); return
            user["last_daily"]=today; prize=random.randint(20,100)*(2 if user["vip"] else 1); user["cash"]+=prize; add_h(uid,f"هدية +{prize}"); await q.edit_message_text(f"هديتك +{prize} 🎁\nكاش: {user['cash']}", reply_markup=back()); return
        if data=="top":
            top=sorted(users.values(), key=lambda x: x["cash"]+x["bank"]+x["savings"], reverse=True)[:10]; txt="اغني 10 🏆\n\n"
            for i,u2 in enumerate(top): txt+=f"{i+1}- {u2.get('name','')} - {u2['cash']+u2['bank']+u2['savings']} {'<- انت' if u2['id']==uid else ''}\n"
            await q.edit_message_text(txt, reply_markup=back()); return
        if data=="luck":
            r=random.choice([0,10,20,50,100,0,30]); user["cash"]+=r; await q.edit_message_text(f"حظك +{r} 🎲\nكاش: {user['cash']}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("تاني", callback_data="luck")],[InlineKeyboardButton("رجوع", callback_data="back")]])); return
        if data=="insurance":
            if user.get("insured"): await q.edit_message_text("انت مأمن خلاص 🛡️", reply_markup=back()); return
            if user["cash"]<200: await q.edit_message_text("التأمين بـ 200", reply_markup=back()); return
            user["cash"]-=200; user["insured"]=True; await q.edit_message_text("أمنت فلوسك! 🛡️", reply_markup=back()); return
        if data=="vip":
            if user["vip"]: await q.edit_message_text("انت VIP خلاص 💎", reply_markup=back()); return
            if user["cash"]<1000: await q.edit_message_text("VIP بـ 1000\nبيضاعف كل هداياك x2", reply_markup=back()); return
            user["cash"]-=1000; user["vip"]=True; await q.edit_message_text("بقيت VIP 💎\nكل هداياك x2!", reply_markup=back()); return
        # ===== خدمة العملاء =====
        if data=="support_menu":
            kb=InlineKeyboardMarkup([[InlineKeyboardButton("👤 Mr cat - خدمة عملاء", url="https://t.me/cat_max_10")],[InlineKeyboardButton("👤 تيتو ™ - خدمة عملاء", url="https://t.me/MOON_104")],[InlineKeyboardButton("📩 اعمل تيكت جديد", callback_data="new_ticket")],[InlineKeyboardButton("🎫 تيكتاتي", callback_data="my_tickets")],[InlineKeyboardButton("⬅️ رجوع", callback_data="back")]])
            await q.edit_message_text("خدمة عملاء بنك TRAN PRO 🏦\n\n👤 Mr cat\nيوزر: @cat_max_10\nجوال: +20 115 5973454\n\n👤 تيتو ™\nيوزر: @MOON_104\nجوال: +20 111 8093542\n\nدوس على اسم اي حد وكلمه على طول\nاو اعمل تيكت وهنرد عليك", reply_markup=kb); return
        if data=="faq":
            await q.edit_message_text("اسئلة شائعة ❓\n\n1- ازاي احول فلوس؟\n/start -> البنك -> تحويل -> اكتب ID والمبلغ\n\n2- ازاي اخد قرض؟\n/start -> قرض -> اختار قرض -> سدد على 3 اقساط\n\n3- ازاي افك شهادة؟\n/start -> شهادات -> فك شهاداتي بعد 7 ايام\n\n4- ازاي ابقى VIP؟\n/start -> VIP بـ 1000، كل هداياك x2\n\n5- فلوسي راحت فين؟\n/start -> كشف حساب هتشوف كل حركاتك\n\n6- عندي مشكلة؟\n/start -> خدمة العملاء -> كلم Mr cat او تيتو", reply_markup=back()); return
        if data=="new_ticket":
            context.user_data["wait_ticket"]=True; await q.edit_message_text("اكتب مشكلتك بالتفصيل\nمثال: حولت 500 لصاحبي وموصلوش", reply_markup=back()); return
        if data=="my_tickets":
            my=[f"#{tid} - {t['msg'][:40]}\nالحالة: {t['status']}\nالرد: {t.get('reply','لسه مفيش رد')}\n---" for tid,t in tickets.items() if t['user_id']==uid]
            if not my: await q.edit_message_text("معندكش تيكتات لسه", reply_markup=back()); return
            await q.edit_message_text("تيكتاتك 🎫\n\n"+"\n".join(my), reply_markup=back()); return
        if data=="support_panel":
            if not is_support(uid): await q.edit_message_text("انت مش خدمة عملاء", reply_markup=back()); return
            open_t=len([t for t in tickets.values() if t['status']!='closed'])
            kb=InlineKeyboardMarkup([[InlineKeyboardButton(f"🎫 التيكتات المفتوحة ({open_t})", callback_data="owner_tickets")],[InlineKeyboardButton("📊 احصائيات سريعة", callback_data="support_stats")],[InlineKeyboardButton("⬅️ رجوع", callback_data="back")]])
            await q.edit_message_text(f"لوحة خدمة العملاء 🎧\n\nاهلا {q.from_user.first_name}\nتيكتات مفتوحة: {open_t}\nاجمالي تيكتات: {len(tickets)}\n\nعشان ترد:\n/reply رقم_التيكت ردك\nمثال: /reply 101 تم حل مشكلتك\n\nعشان تقفل:\n/close 101", reply_markup=kb); return
        if data=="support_stats":
            if not is_support(uid): return
            await q.edit_message_text(f"احصائيات خدمة العملاء 🎧\n\nمستخدمين: {len(users)}\nتيكتات مفتوحة: {len([t for t in tickets.values() if t['status']!='closed'])}\nتيكتات اترد عليها: {len([t for t in tickets.values() if t['status']=='اترد عليه'])}\nتيكتات اتقفلت: {len([t for t in tickets.values() if t['status']=='closed'])}\n\nفريق خدمة العملاء:\n👤 Mr cat - @cat_max_10\n👤 تيتو ™ - @MOON_104", reply_markup=back()); return
        if data=="owner_tickets":
            if not is_support(uid): return
            txt="التيكتات المفتوحة 🎫\n\n"
            for tid,t in tickets.items():
                if t['status']!='closed': txt+=f"#{tid} - {t['user_name']} ({t['user_id']}): {t['msg'][:40]} - {t['status']}\n"
            if txt=="التيكتات المفتوحة 🎫\n\n": txt="مفيش تيكتات مفتوحة"
            txt+="\n\nرد: /reply رقم_التيكت ردك\nقفل: /close رقم_التيكت"
            await q.edit_message_text(txt, reply_markup=back()); return
        # ===== الاونر =====
        if data=="owner":
            if uid!=OWNER_ID: await q.edit_message_text("مش الاونر", reply_markup=back()); return
            kb=InlineKeyboardMarkup([[InlineKeyboardButton("احصائيات", callback_data="o_stats"), InlineKeyboardButton("اذاعة", callback_data="o_broadcast")],[InlineKeyboardButton("اضف فلوس", callback_data="o_add"), InlineKeyboardButton("خصم فلوس", callback_data="o_remove")],[InlineKeyboardButton("حظر / فك", callback_data="o_ban"), InlineKeyboardButton("شوف يوزر", callback_data="o_view")],[InlineKeyboardButton("تيكتات العملاء", callback_data="owner_tickets"), InlineKeyboardButton("تصفير يوزر", callback_data="o_reset_user")],[InlineKeyboardButton("ادي VIP", callback_data="o_give_vip"), InlineKeyboardButton("شيل VIP", callback_data="o_remove_vip")],[InlineKeyboardButton("تصفير الكل", callback_data="o_reset_all")],[InlineKeyboardButton("رجوع", callback_data="back")]])
            total=sum(u["cash"]+u["bank"]+u["savings"] for u in users.values()); open_t=len([t for t in tickets.values() if t['status']!='closed'])
            await q.edit_message_text(f"لوحة الاونر 👑\n\nمستخدمين: {len(users)}\nاجمالي فلوس: {total}\nقروض: {sum(u['loan'] for u in users.values())}\nتيكتات مفتوحة: {open_t}\nشهادات: {sum(len(u['certs']) for u in users.values())}\nودائع: {sum(len(u['deposits']) for u in users.values())}", reply_markup=kb); return
        if data=="o_stats":
            if uid!=OWNER_ID: return
            await q.edit_message_text(f"احصائيات 📊\nمستخدمين: {len(users)}\nكاش: {sum(u['cash'] for u in users.values())}\nبنك: {sum(u['bank'] for u in users.values())}\nتحويش: {sum(u['savings'] for u in users.values())}\nقروض: {sum(u['loan'] for u in users.values())}\nكريديت: {sum(u['credit_used'] for u in users.values())}", reply_markup=back()); return
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
        if data=="o_view":
            if uid!=OWNER_ID: return
            context.user_data["wait_view"]=True; await q.edit_message_text("اكتب ID اليوزر", reply_markup=back()); return
        if data=="o_reset_user":
            if uid!=OWNER_ID: return
            context.user_data["wait_reset_user"]=True; await q.edit_message_text("اكتب ID اللي عايز تصفره", reply_markup=back()); return
        if data=="o_give_vip":
            if uid!=OWNER_ID: return
            context.user_data["wait_give_vip"]=True; await q.edit_message_text("اكتب ID اللي عايز تديله VIP ببلاش", reply_markup=back()); return
        if data=="o_remove_vip":
            if uid!=OWNER_ID: return
            context.user_data["wait_remove_vip"]=True; await q.edit_message_text("اكتب ID اللي عايز تشيل منه VIP", reply_markup=back()); return
        if data=="o_reset_all":
            if uid!=OWNER_ID: return
            context.user_data["wait_reset_all"]=True; await q.edit_message_text("متأكد عايز تصفر الكل؟ اكتب: ايوه", reply_markup=back()); return
    except Exception as e:
        print(f"BUTTON ERROR: {e}")
        try: await q.edit_message_text("حصل ايرور، دوس تحديث", reply_markup=main_menu(uid))
        except: pass

async def cmd_deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; u=get_user(uid)
    if not context.args: await update.message.reply_text("اكتب: /deposit 100"); return
    try:
        amt=int(context.args[0])
        if u["cash"]<amt: await update.message.reply_text("معكش كفاية"); return
        u["cash"]-=amt; u["bank"]+=amt; add_h(uid,f"ايداع +{amt}"); await update.message.reply_text(f"ايداع تم ✅ بنك: {u['bank']}")
    except: await update.message.reply_text("اكتب رقم صح")
async def cmd_withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; u=get_user(uid)
    if not context.args: await update.message.reply_text("اكتب: /withdraw 100"); return
    try:
        amt=int(context.args[0])
        if u["bank"]<amt: await update.message.reply_text("معكش في البنك"); return
        u["bank"]-=amt; u["cash"]+=amt; add_h(uid,f"سحب -{amt}"); await update.message.reply_text(f"سحب تم ✅ كاش: {u['cash']}")
    except: await update.message.reply_text("اكتب رقم صح")
async def cmd_transfer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; u=get_user(uid)
    if len(context.args)<2: await update.message.reply_text("اكتب: /transfer ID المبلغ"); return
    try:
        t=int(context.args[0]); amt=int(context.args[1])
        if u["cash"]<amt: await update.message.reply_text("معكش كفاية"); return
        get_user(t); u["cash"]-=amt; users[t]["cash"]+=amt; add_h(uid,f"حولت -{amt}"); add_h(t,f"وصلك +{amt}"); await update.message.reply_text(f"حولت {amt} لـ {t} ✅")
        try: await context.bot.send_message(t, f"وصلك {amt} من {update.effective_user.first_name} 💸")
        except: pass
    except: await update.message.reply_text("اكتب صح: /transfer ID المبلغ")
async def cmd_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; u=get_user(uid); await update.message.reply_text(f"رصيدك 💰\nكاش: {u['cash']}\nبنك: {u['bank']}\nتحويش: {u['savings']}\nالكلي: {u['cash']+u['bank']+u['savings']}")
async def cmd_visa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; u=get_user(uid); await update.message.reply_text(f"فيزا TRAN 💳\n{update.effective_user.first_name}\n{u['card_num']}\nرصيد: {u['bank']}")
async def cmd_top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    top=sorted(users.values(), key=lambda x: x["cash"]+x["bank"]+x["savings"], reverse=True)[:10]; txt="اغني 10 🏆\n\n"
    for i,u2 in enumerate(top): txt+=f"{i+1}- {u2.get('name','')} - {u2['cash']+u2['bank']+u2['savings']}\n"
    await update.message.reply_text(txt)
async def cmd_daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; u=get_user(uid); today=datetime.now().strftime("%Y-%m-%d")
    if u["last_daily"]==today: await update.message.reply_text("خدتها النهاردة"); return
    u["last_daily"]=today; prize=random.randint(20,100)*(2 if u["vip"] else 1); u["cash"]+=prize; await update.message.reply_text(f"هديتك +{prize} 🎁")
async def cmd_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_support(update.effective_user.id): await update.message.reply_text("انت مش خدمة عملاء"); return
    if len(context.args)<2: await update.message.reply_text("اكتب: /reply رقم_التيكت الرد"); return
    try:
        tid=int(context.args[0]); reply=" ".join(context.args[1:])
        if tid not in tickets: await update.message.reply_text("التيكت مش موجود"); return
        tickets[tid]["status"]="اترد عليه"; tickets[tid]["reply"]=reply; tickets[tid]["replied_by"]=update.effective_user.first_name
        await update.message.reply_text(f"رديت على #{tid} ✅")
        await context.bot.send_message(tickets[tid]["user_id"], f"رد خدمة العملاء ({update.effective_user.first_name}) على تيكت #{tid}:\n\n{reply}")
    except: await update.message.reply_text("اكتب صح")
async def cmd_close(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_support(update.effective_user.id): await update.message.reply_text("انت مش خدمة عملاء"); return
    if not context.args: await update.message.reply_text("اكتب: /close رقم_التيكت"); return
    try:
        tid=int(context.args[0]); tickets[tid]["status"]="closed"; await update.message.reply_text(f"قفلت #{tid} ✅")
        await context.bot.send_message(tickets[tid]["user_id"], f"تيكت #{tid} اتقفل، شكرا ليك! 🎧")
    except: await update.message.reply_text("التيكت مش موجود")

async def on_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        uid=update.effective_user.id; txt=(update.message.text or "").strip(); u=get_user(uid)
        if txt=="تصفير" and uid==OWNER_ID: users.clear(); await update.message.reply_text("اتصفر كله"); return
        if context.user_data.get("wait_ticket"):
            context.user_data["wait_ticket"]=False
            ticket_counter[0]+=1; tid=ticket_counter[0]
            tickets[tid]={"user_id":uid,"user_name":update.effective_user.first_name,"msg":txt,"status":"مفتوح","reply":""}
            await update.message.reply_text(f"عملت تيكت #{tid} ✅\nمشكلتك: {txt}\nالحالة: مفتوح\nخدمة العملاء هترد عليك", reply_markup=main_menu(uid))
            for sid in SUPPORT_IDS:
                try: await context.bot.send_message(sid, f"🎫 تيكت جديد #{tid}\nمن {update.effective_user.first_name} ({uid}):\n{txt}\n\nرد: /reply {tid} ردك")
                except: pass
            return
        if context.user_data.get("wait_broadcast") and uid==OWNER_ID:
            context.user_data["wait_broadcast"]=False; c=0
            for x in list(users.keys()):
                try: await context.bot.send_message(x, f"من بنك TRAN PRO 🏦:\n\n{txt}"); c+=1
                except: pass
            await update.message.reply_text(f"اتبعت لـ {c}"); return
        if context.user_data.get("wait_add") and uid==OWNER_ID:
            context.user_data["wait_add"]=False
            try: t,a=map(int,txt.split()); get_user(t); users[t]["cash"]+=a; await update.message.reply_text(f"ضفت {a} لـ {t}")
            except: await update.message.reply_text("اكتب صح")
            return
        if context.user_data.get("wait_remove") and uid==OWNER_ID:
            context.user_data["wait_remove"]=False
            try: t,a=map(int,txt.split()); get_user(t); users[t]["cash"]-=a; await update.message.reply_text(f"خصمت {a} من {t}")
            except: await update.message.reply_text("اكتب صح")
            return
        if context.user_data.get("wait_ban") and uid==OWNER_ID:
            context.user_data["wait_ban"]=False
            try: t=int(txt); get_user(t); users[t]["banned"]=not users[t]["banned"]; await update.message.reply_text(f"{'حظرته' if users[t]['banned'] else 'فكيت حظره'} {t}")
            except: await update.message.reply_text("ID غلط")
            return
        if context.user_data.get("wait_view") and uid==OWNER_ID:
            context.user_data["wait_view"]=False
            try: t=int(txt); uu=get_user(t); await update.message.reply_text(f"{uu['name']}\nID: {t}\nكاش: {uu['cash']} | بنك: {uu['bank']} | تحويش: {uu['savings']}\nقرض: {uu['loan']}\nمحظور: {uu['banned']}")
            except: await update.message.reply_text("مش موجود")
            return
        if context.user_data.get("wait_reset_user") and uid==OWNER_ID:
            context.user_data["wait_reset_user"]=False
            try: t=int(txt); get_user(t); users[t].update({"cash":1000,"bank":0,"savings":0,"loan":0,"loan_due":0,"loan_left":0,"credit_used":0,"certs":[],"deposits":[]}); await update.message.reply_text(f"صفرت {t} ✅")
            except: await update.message.reply_text("ID غلط")
            return
        if context.user_data.get("wait_give_vip") and uid==OWNER_ID:
            context.user_data["wait_give_vip"]=False
            try: t=int(txt); get_user(t); users[t]["vip"]=True; await update.message.reply_text(f"اديت VIP لـ {t} ✅")
            except: await update.message.reply_text("ID غلط")
            return
        if context.user_data.get("wait_remove_vip") and uid==OWNER_ID:
            context.user_data["wait_remove_vip"]=False
            try: t=int(txt); get_user(t); users[t]["vip"]=False; await update.message.reply_text(f"شلت VIP من {t} ✅")
            except: await update.message.reply_text("ID غلط")
            return
        if context.user_data.get("wait_reset_all") and uid==OWNER_ID:
            context.user_data["wait_reset_all"]=False
            if txt.lower() in ["ايوه","yes","نعم"]: users.clear(); tickets.clear(); await update.message.reply_text("صفرت الكل")
            else: await update.message.reply_text("اتلغى")
            return
        if context.user_data.get("wait_transfer"):
            context.user_data["wait_transfer"]=False
            try:
                t,a=map(int,txt.split())
                if u["cash"]<a: await update.message.reply_text("معكش كفاية"); return
                get_user(t); u["cash"]-=a; users[t]["cash"]+=a; add_h(uid,f"حولت -{a}"); add_h(t,f"وصلك +{a}"); await update.message.reply_text(f"حولت {a} لـ {t} ✅")
                try: await context.bot.send_message(t, f"وصلك {a} من {update.effective_user.first_name}")
                except: pass
            except: await update.message.reply_text("اكتب: ID المبلغ")
            return
        if context.user_data.get("wait_check"):
            context.user_data["wait_check"]=False
            try:
                t,a=map(int,txt.split())
                if u["cash"]<a: await update.message.reply_text("معكش كفاية"); return
                get_user(t); u["cash"]-=a; code=f"CHK{random.randint(1000,9999)}"; checks[code]={"to":t,"amt":a,"until":datetime.now()+timedelta(days=1)}; add_h(uid,f"عملت شيك -{a}"); await update.message.reply_text(f"عملت شيك {code} ✅\nلـ {t} بمبلغ {a}\nهيصرفه بعد يوم")
                try: await context.bot.send_message(t, f"جاتلك شيك {code} بمبلغ {a} من {update.effective_user.first_name}\nاصرفه بكرة من /start -> شيك -> اصرف شيك")
                except: pass
            except: await update.message.reply_text("اكتب: ID المبلغ")
            return
        if context.user_data.get("wait_joint"):
            context.user_data["wait_joint"]=False
            try:
                t=int(txt); get_user(t); key=f"{min(uid,t)}_{max(uid,t)}"; joint_accounts[key]={"balance":0,"members":[uid,t]}; u["joint"]=key; users[t]["joint"]=key; await update.message.reply_text(f"عملت حساب مشترك مع {t}! ✅")
                try: await context.bot.send_message(t, f"{update.effective_user.first_name} عمل معاك حساب مشترك!")
                except: pass
            except: await update.message.reply_text("اكتب ID صح")
            return
        await update.message.reply_text("اكتب /start", reply_markup=main_menu(uid))
    except Exception as e: print(f"MSG ERROR: {e}")

def main():
    app=ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("deposit", cmd_deposit))
    app.add_handler(CommandHandler("withdraw", cmd_withdraw))
    app.add_handler(CommandHandler("transfer", cmd_transfer))
    app.add_handler(CommandHandler("balance", cmd_balance))
    app.add_handler(CommandHandler("visa", cmd_visa))
    app.add_handler(CommandHandler("top", cmd_top))
    app.add_handler(CommandHandler("daily", cmd_daily))
    app.add_handler(CommandHandler("reply", cmd_reply))
    app.add_handler(CommandHandler("close", cmd_close))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_msg))
    print("TRAN BANK PRO STARTED")
    app.run_polling()
if __name__=="__main__": main()
