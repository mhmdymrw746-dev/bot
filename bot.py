import os,random,requests,threading,time
from datetime import datetime,timedelta
from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import Application,CommandHandler,CallbackQueryHandler,ContextTypes,MessageHandler,filters
TOKEN=os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN") or os.getenv("TOKEN")
LAST="2026/11/20";NEXT="2027/01/29"
UT=f"📅 آخر تحديث: {LAST}\n🔜 القادم: {NEXT}"
CACHE={"today":[],"tomorrow":[],"week":[],"live":[]}
pts={};modd={};score={};fant={};chat=[];leagues={};pleague={}
def getmod(u):
 M={"gold":("👑","أهلا بيك في الذهبي 👑"),"neon":("⚡","أهلا بيك في النيون 💜"),"fire":("🔥","ولعهااا 🔥"),"ice":("🧊","أهلا بيك في الثلجي 💙")}
 return M.get(modd.get(u,"gold"))
def espn(slug):
 o=[]
 try:
  for off in [0,3,6]:
   d=(datetime.now()+timedelta(days=off)).strftime("%Y%m%d")
   r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{slug}/scoreboard?dates={d}",timeout=10,headers={"User-Agent":"Mozilla/5.0"})
   for ev in r.json().get("events",[]):
    c=ev.get("competitions",[{}])[0];t=c.get("competitors",[])
    if len(t)<2: continue
    h=t[0].get("team",{}).get("displayName","?");a=t[1].get("team",{}).get("displayName","?")
    if t[0].get("homeAway")=="away": h,a=a,h
    dt=ev.get("date","")
    try: dd=datetime.fromisoformat(dt.replace("Z","+00:00"));ds=dd.strftime("%Y-%m-%d")
    except: ds=dt[:10]
    st=c.get("status",{}).get("type",{}).get("description","");hs=t[0].get("score");as_=t[1].get("score")
    sc=f"🔴 {hs} - {as_}" if hs is not None and st!="Scheduled" else "🕗 قريبا"
    o.append({"h":h,"a":a,"lg":ev.get("league",{}).get("name",slug),"date":ds,"sc":sc})
 except: pass
 return o
def upd():
 e=espn("egy.1")+espn("eng.1")+espn("esp.1")
 td=datetime.now().strftime("%Y-%m-%d");tm=(datetime.now()+timedelta(days=1)).strftime("%Y-%m-%d")
 if not e: e=[{"h":"الجونة","a":"الزمالك","lg":"الدوري المصري","date":"2026-11-23","sc":"🕗 17:00"},{"h":"الأهلي","a":"بيراميدز","lg":"الدوري المصري","date":"2026-11-23","sc":"🕗 20:00"},{"h":"سموحة","a":"البنك الأهلي","lg":"الدوري المصري","date":"2026-11-24","sc":"🕗 17:00"},{"h":"المصري","a":"بترول أسيوط","lg":"الدوري المصري","date":"2026-11-24","sc":"🕗 20:00"}]
 CACHE.update({"today":[x for x in e if x["date"]==td],"tomorrow":[x for x in e if x["date"]==tm],"week":e,"live":[]})
def fmt(t,l):
 s=f"{t}\n{UT}\n\n"
 if not l: return s+"مفيش ماتشات ⚽"
 for m in l: s+=f"⚽ {m['h']} 🆚 {m['a']}\n🏆 {m['lg']} | {m['sc']} | 📅 {m['date']}\n\n"
 return s
def kb_main(u):
 e,_=getmod(u);p=pts.get(u,0)
 k=[]
 k.append([InlineKeyboardButton(f"{e} القائمة | ⭐ {p}",callback_data="menu")])
 k.append([InlineKeyboardButton("📅 جدول",callback_data="schedule")])
 k.append([InlineKeyboardButton("🔴 لايف",callback_data="live"),InlineKeyboardButton("🌍 كل العالم",callback_data="week")])
 k.append([InlineKeyboardButton("🤖 توقع AI",callback_data="ai"),InlineKeyboardButton("📋 تشكيلة",callback_data="lineup")])
 k.append([InlineKeyboardButton("🏟️ تفاصيل",callback_data="details"),InlineKeyboardButton("⭐ تقييم",callback_data="rate")])
 k.append([InlineKeyboardButton("🔴 أخبار الأهلي",callback_data="ahly"),InlineKeyboardButton("⚪ أخبار الزمالك",callback_data="zamalek")])
 k.append([InlineKeyboardButton("📊 ترتيب",callback_data="stand"),InlineKeyboardButton("🎯 هدافين",callback_data="top")])
 k.append([InlineKeyboardButton("⚔️ قارن",callback_data="cmp"),InlineKeyboardButton("🤼 مواجهات",callback_data="h2h")])
 k.append([InlineKeyboardButton("🏆 فانتازي",callback_data="fant"),InlineKeyboardButton("🔮 توقع",callback_data="pred")])
 k.append([InlineKeyboardButton("🎲 خمن",callback_data="guess"),InlineKeyboardButton("🎰 عجلة",callback_data="wheel")])
 k.append([InlineKeyboardButton("😂 ميمز",callback_data="meme"),InlineKeyboardButton("📰 انتقالات",callback_data="trans")])
 k.append([InlineKeyboardButton("⭐ اللاعيبة",callback_data="players"),InlineKeyboardButton("🧠 تحدي",callback_data="quiz")])
 k.append([InlineKeyboardButton("📚 مبادئ",callback_data="basic"),InlineKeyboardButton("💡 نصيحة",callback_data="tip")])
 k.append([InlineKeyboardButton("📺 بث ✅",callback_data="stream"),InlineKeyboardButton("🎥 أهداف ✅",callback_data="goals")])
 k.append([InlineKeyboardButton("👥 فانتازي جماعي ✅",callback_data="fleague"),InlineKeyboardButton("💬 شات ✅",callback_data="chat")])
 k.append([InlineKeyboardButton("🏆 دوري توقعات ✅",callback_data="pleague"),InlineKeyboardButton("🎙️ تعليق ✅",callback_data="comm")])
 k.append([InlineKeyboardButton(f"📅 {LAST} | 🔜 {NEXT}",callback_data="schedule")])
 return InlineKeyboardMarkup(k)
def back(): return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القايمة",callback_data="menu")]])
async def start(up,ctx):
 u=up.effective_user.id;e,w=getmod(u)
 t=f"{w}\n\n👋 أهلا بيك يا {up.effective_user.first_name} !\n🌍 كل الماتشات + 🤖 AI + 📺 بث + 💬 شات\n⭐ {pts.get(u,0)}\n\n{UT}\n\n👇 اختار:"
 if up.message: await up.message.reply_text(t,reply_markup=kb_main(u))
 else: await up.callback_query.edit_message_text(t,reply_markup=kb_main(u))
async def btn(up,ctx):
 q=up.callback_query;await q.answer();u=q.from_user.id;d=q.data;e,_=getmod(u)
 if d=="menu": await start(up,ctx);return
 if d=="schedule": await q.edit_message_text(f"📅 جدول\n\n{UT}",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📅 النهاردة",callback_data="today")],[InlineKeyboardButton("📅 بكرة",callback_data="tom")],[InlineKeyboardButton("📅 الأسبوع",callback_data="week")],[InlineKeyboardButton("🔙 القايمة",callback_data="menu")]]));return
 if d=="today": await q.edit_message_text(fmt("📅 النهاردة",CACHE["today"]),reply_markup=back());return
 if d=="tom": await q.edit_message_text(fmt("📅 بكرة",CACHE["tomorrow"]),reply_markup=back());return
 if d=="week": await q.edit_message_text(fmt("📅 الأسبوع",CACHE["week"]),reply_markup=back());return
 if d=="live": await q.edit_message_text(fmt("🔴 لايف",CACHE["live"]),reply_markup=back());return
 if d=="ai": await q.edit_message_text("🤖 توقع AI\n⚽ الأهلي 🆚 بيراميدز\n🤖 الأهلي يكسب 2-1\n📈 45% | 30% | 25%",reply_markup=back());return
 if d=="lineup": await q.edit_message_text("📋 تشكيلة الأهلي\n🧤 الشناوي\n🛡️ هاني - ياسر - داري - معلول\n⚙️ مروان - إمام - أفشة\n⚽ تاو - وسام - الشحات",reply_markup=back());return
 if d=="details": await q.edit_message_text("🏟️ الأهلي 🆚 بيراميدز\n📅 23 نوفمبر | 8 م\n🏟️ استاد القاهرة\n👨‍⚖️ أمين عمر\n📺 ON Sport",reply_markup=back());return
 if d=="rate": await q.edit_message_text("⭐ تقييم\n🔴 وسام 9.2 | إمام 8.5\n⚪ زيزو 8.8",reply_markup=back());return
 if d=="ahly": await q.edit_message_text("🔴 أخبار الأهلي\n🏋️ بيستعد لبيراميدز 23 نوفمبر 8 م\n💪 وسام جاهز",reply_markup=back());return
 if d=="zamalek": await q.edit_message_text("⚪ أخبار الزمالك\n🏋️ بيستعد للجونة 23 نوفمبر 5 م\n💪 زيزو جاهز",reply_markup=back());return
 if d=="stand": await q.edit_message_text("📊 ترتيب المصري\n1️⃣ بيراميدز 18\n2️⃣ الأهلي 17\n3️⃣ الزمالك 16",reply_markup=back());return
 if d=="top": await q.edit_message_text("🎯 هدافين\n🥇 وسام 7\n🥈 زيزو 6",reply_markup=back());return
 if d=="cmp": await q.edit_message_text("⚔️ ميسي 🆚 رونالدو\n🐐 ميسي مهارة 99\n👑 رونالدو قوة 98",reply_markup=back());return
 if d=="h2h": await q.edit_message_text("🤼 الأهلي 🆚 الزمالك\n🔴 الأهلي 61 | ⚪ الزمالك 29 | 🤝 40",reply_markup=back());return
 if d=="fant": await q.edit_message_text(f"🏆 فانتازي\nفريقك: {fant.get(u,[])}\n⭐ {pts.get(u,0)}",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("➕ صلاح",callback_data="f_salah")],[InlineKeyboardButton("🔙 القايمة",callback_data="menu")]]));return
 if d=="f_salah": fant[u]=fant.get(u,[])+["صلاح"];await q.edit_message_text("✅ ضفت صلاح!",reply_markup=back());return
 if d=="pred": await q.edit_message_text("🔮 توقع الأهلي 🆚 بيراميدز",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔴 الأهلي",callback_data="p_ahly")],[InlineKeyboardButton("🤝 تعادل",callback_data="p_draw")]]));return
 if d.startswith("p_"): pts[u]=pts.get(u,0)+10;pleague[u]=pts[u];await q.edit_message_text(f"✅ +10 نقاط ⭐ {pts[u]}",reply_markup=kb_main(u));return
 if d=="guess": await q.edit_message_text("🎲 خمن: 🇪🇬 مصري 👑 ليفربول",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("صلاح",callback_data="g_ok")],[InlineKeyboardButton("زيزو",callback_data="g_no")]]));return
 if d=="g_ok": pts[u]=pts.get(u,0)+5;await q.edit_message_text(f"✅ صح! +5 ⭐ {pts[u]}",reply_markup=back());return
 if d=="g_no": await q.edit_message_text("❌ غلط! الصح صلاح",reply_markup=back());return
 if d=="wheel": r=random.choice(["🎁 10 نقاط!","🎁 50 نقطة!","🎁 100 نقطة!","😅 مفيش حظ"]);pts[u]=pts.get(u,0)+(10 if "10" in r else 50 if "50" in r else 100 if "100" in r else 0);await q.edit_message_text(f"🎰 {r}\n⭐ {pts[u]}",reply_markup=back());return
 if d=="meme": await q.edit_message_text(random.choice(["😂 لما فريقك يجيب جون الدقيقة 90: جووووول 🔥","😂 لما الحكم يحسب جزاء ضدك: يا حكم يا ظالم 😭"]),reply_markup=back());return
 if d=="trans": await q.edit_message_text("📰 انتقالات\n🔴 الأهلي بيجهز عرض لمهاجم أجنبي",reply_markup=back());return
 if d=="players": await q.edit_message_text("⭐ صلاح 👑\n🏟️ ليفربول | ⚡ 93 | 🎯 95\n⭐ ميسي 🐐\n🏟️ ميامي | ⚡ 99\n⭐ هالاند 🤖\n🏟️ سيتي | ⚡ 95",reply_markup=back());return
 if d=="quiz": await q.edit_message_text("🧠 مين فاز بكاس العالم 2022؟",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("الأرجنتين",callback_data="q_ok")],[InlineKeyboardButton("فرنسا",callback_data="q_no")]]));return
 if d=="q_ok": pts[u]=pts.get(u,0)+10;await q.edit_message_text(f"✅ صح! +10 ⭐ {pts[u]}",reply_markup=back());return
 if d=="q_no": await q.edit_message_text("❌ غلط! الصح الأرجنتين",reply_markup=back());return
 if d=="basic": await q.edit_message_text("📚 مبادئ\n🧤 حارس | 🛡️ مدافع | ⚙️ وسط | ⚽ مهاجم\n❌ التسلل: أقرب للجون من آخر مدافع",reply_markup=back());return
 if d=="tip": await q.edit_message_text("💡 أول لمسة بتفرق بين عادي ومحترف.",reply_markup=back());return
 if d=="stream": await q.edit_message_text("📺 بث مباشر\nhttps://www.youtube.com/@ONTimeSports\nhttps://www.yallashoot.com",reply_markup=back());return
 if d=="goals": await q.edit_message_text("🎥 هدف وسام في بيراميدز\nhttps://www.youtube.com/results?search_query=هدف+وسام+بيراميدز",reply_markup=back());return
 if d=="comm": await q.edit_message_text("🎙️ تعليق\n⚽ الأهلي 1 - 0 بيراميدز\n• د 10: جوووول وسام 🔥",reply_markup=back());return
 if d=="fleague": await q.edit_message_text("👥 فانتازي جماعي\nاكتب: دخول 1234\nأو اعمل دوري:",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("➕ اعمل دوري",callback_data="mkleague")],[InlineKeyboardButton("🔙 القايمة",callback_data="menu")]]));return
 if d=="mkleague": c=str(random.randint(1000,9999));leagues[c]={"m":{u:pts.get(u,0)}};await q.edit_message_text(f"✅ عملت دوري!\n🔑 الكود: {c}\nابعته لصحابك",reply_markup=back());return
 if d=="chat":
  t="💬 شات جماهير\n"
  if not chat: t+="لسه فاضي، اكتب: اهلي: يلا يا أهلي"
  else:
   for m in chat[-10:]: t+=f"{m}\n"
  await q.edit_message_text(t,reply_markup=back());return
 if d=="pleague":
  pleague[u]=pts.get(u,0);t="🏆 دوري التوقعات\n"
  for i,(uu,pp) in enumerate(sorted(pleague.items(),key=lambda x:x[1],reverse=True)[:10],1): t+=f"{i}️⃣ {str(uu)[-4:]} - {pp}\n"
  await q.edit_message_text(t,reply_markup=back());return
async def txt(up,ctx):
 u=up.effective_user.id;r=up.message.text
 if r.startswith("اهلي:") or r.startswith("أهلي:"): chat.append(f"🔴 {up.effective_user.first_name}: {r.split(':',1)[1]}");await up.message.reply_text("✅ اتنشرت في شات الأهلي! 🔴",reply_markup=kb_main(u));return
 if r.startswith("زمالك:"): chat.append(f"⚪ {up.effective_user.first_name}: {r.split(':',1)[1]}");await up.message.reply_text("✅ اتنشرت في شات الزمالك! ⚪",reply_markup=kb_main(u));return
 if r.startswith("دخول"):
  c=r.replace("دخول","").strip()
  if c in leagues: leagues[c]["m"][u]=pts.get(u,0);await up.message.reply_text(f"✅ دخلت الدوري {c}!",reply_markup=kb_main(u))
  else: await up.message.reply_text("❌ الكود مش موجود",reply_markup=kb_main(u))
  return
 await up.message.reply_text(f"وصلت: {r} ✅\n{UT}",reply_markup=kb_main(u))
def main():
 if not TOKEN: print("مفيش توكن");return
 upd()
 app=Application.builder().token(TOKEN).build()
 def loop():
  while True:
   time.sleep(1800)
   try: upd()
   except: pass
 threading.Thread(target=loop,daemon=True).start()
 app.add_handler(CommandHandler("start",start))
 app.add_handler(CallbackQueryHandler(btn))
 app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,txt))
 print("Bot running")
 app.run_polling()
if __name__=="__main__": main()
