import os,random,requests,threading,time
from datetime import datetime,timedelta
from http.server import BaseHTTPRequestHandler,HTTPServer
from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import Application,CommandHandler,CallbackQueryHandler,ContextTypes,MessageHandler,filters
TOKEN=os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN") or os.getenv("TOKEN")
API_KEY=os.getenv("API_FOOTBALL_KEY") or os.getenv("FOOTBALL_API_KEY") or ""
LAST="2026/11/20";NEXT="2027/01/29"
UT=f"📅 آخر تحديث: {LAST}\n🔜 القادم: {NEXT}"
CACHE={"today":[],"tomorrow":[],"week":[],"live":[]}
pts={};modd={};score={};fant={};chat=[];leagues={};pleague={};daily={};quiz_idx={}
BANNER="🔥━━━━━━━━━━━━━━━🔥\n⚽  KORA BOT  ⚽\n🔥━━━━━━━━━━━━━━━🔥"
HYPE=["🔥🔥🔥 ولعهااااااااا 🔥🔥🔥","⚡⚡ ايه الحماس ده كله ⚡⚡","🚀 انت مولع الدنيا النهاردة!","👑 ملك الكورة وصل!","💥 جوووووووووول!"]
GOAL=["🎉🎉🎉 GOAAAAAL! 🎉🎉🎉\n⚽🔥⚽🔥⚽\nانت أسطورة!","🔥🔥🔥 ايه الجون ده! 🔥🔥🔥\n🏆 انت نجم الماتش!","💥💥 BOOOOM! 💥💥\nجون عالمي!"]
QUIZ=[("🧠 مين فاز بكاس العالم 2022؟",["🇦🇷 الأرجنتين","🇫🇷 فرنسا"],0),("🧠 مين هداف الدوري الإنجليزي التاريخي؟",["🏴󐁧󐁢󐁥󐁮󐁧󐁿 آلان شيرر","🏴󐁧󐁢󐁥󐁮󐁧󐁿 روني"],0),("🧠 مين كسب دوري الأبطال 2024؟",["👑 ريال مدريد","💙 السيتي"],0),("🧠 مين صاحب الكرة الذهبية 2023؟",["🐐 ميسي","🤖 هالاند"],0)]
GUESS=[("🎲 خمن: 🇪🇬 مصري 👑 ليفربول",["👑 صلاح","⚪ زيزو"],0),("🎲 خمن: 🇦🇷 أرجنتيني 🐐 ميامي",["🐐 ميسي","🇦🇷 ديبالا"],0),("🎲 خمن: 🇳🇴 نرويجي 🤖 سيتي",["🤖 هالاند","🇳🇴 أوديجارد"],0)]
MEMES=["😂 لما فريقك يجيب جون الدقيقة 90: جووووول 🔥","😂 لما الحكم يحسب جزاء ضدك: يا حكم يا ظالم 😭","😂 لما تقول هتذاكر وتتفرج على ماتش واحد بس","😂 صاحبك اللي بيشجع الفريق اللي كسبان امبارح بس"]
TIPS=["💡 أول لمسة بتفرق بين عادي ومحترف.","💡 اتفرج على تحركات اللاعب من غير كورة.","💡 الفانتازي عايز صبر مش حظ.","💡 الكورة 90 دقيقة، متحتفلش بدري."]
def keep():
 class H(BaseHTTPRequestHandler):
  def do_GET(self): self.send_response(200);self.end_headers();self.wfile.write(b"Bot running")
  def log_message(self,*a): pass
 try: HTTPServer(("0.0.0.0",int(os.getenv("PORT",10000))),H).serve_forever()
 except: pass
def getmod(u):
 M={"gold":("👑","👑 أهلا بيك في الذهبي 👑\n✨ انت ملك الكورة هنا ✨"),"neon":("⚡","⚡ أهلا بيك في النيون 💜\n🌌 عالم تاني من الحماس"),"fire":("🔥","🔥🔥 ولعهااااا 🔥🔥\n💥 انت نار النهاردة!"),"ice":("🧊","🧊 أهلا بيك في الثلجي 💙\n❄️ بارد ورايق زي الكبار")}
 return M.get(modd.get(u,"gold"))
# ===== مصادر الماتشات القوية =====
def src_apifootball():
 o=[]
 if not API_KEY: return o
 try:
  # 39=انجليزي 140=اسباني 61=فرنسي 78=الماني 135=ايطالي 2=ابطال اوروبا
  for d in [0,1,2,3]:
   dt=(datetime.now()+timedelta(days=d)).strftime("%Y-%m-%d")
   r=requests.get("https://v3.football.api-sports.io/fixtures",params={"date":dt},headers={"x-apisports-key":API_KEY},timeout=12)
   for f in r.json().get("response",[]):
    lg=f.get("league",{}).get("name","")
    # فلترة الدوريات المهمة بس عشان نوفر الطلبات
    if lg not in ["Premier League","La Liga","Serie A","Bundesliga","Ligue 1","UEFA Champions League","Egyptian Premier League","Africa Cup of Nations"]: continue
    h=f["teams"]["home"]["name"];a=f["teams"]["away"]["name"]
    st=f["fixture"]["status"]["short"];gh=f["goals"]["home"];ga=f["goals"]["away"]
    sc=f"🔴 {gh} - {ga} | {st}" if gh is not None else "🕗 قريبا"
    if st in ["1H","2H","HT","ET","P"]: sc=f"🔴 LIVE {gh} - {ga}"
    o.append({"h":h,"a":a,"lg":lg,"date":dt,"sc":sc})
   if o: break
 except: pass
 return o
def src_thesportsdb():
 o=[]
 try:
  for d in [0,1,2]:
   dt=(datetime.now()+timedelta(days=d)).strftime("%Y-%m-%d")
   # 4328=انجليزي 4335=اسباني 4332=ايطالي 4331=الماني 4334=فرنسي 4480=ابطال اوروبا
   for lid in ["4328","4335","4332","4331","4334","4480"]:
    r=requests.get(f"https://www.thesportsdb.com/api/v1/json/3/eventsday.php?d={dt}&l={lid}",timeout=10)
    for ev in r.json().get("events",[]) or []:
     h=ev.get("strHomeTeam","?");a=ev.get("strAwayTeam","?")
     hs=ev.get("intHomeScore");as_=ev.get("intAwayScore")
     sc=f"🔴 {hs} - {as_}" if hs not in [None,""] else "🕗 قريبا"
     o.append({"h":h,"a":a,"lg":ev.get("strLeague",""),"date":dt,"sc":sc})
   if o: break
 except: pass
 return o
def src_espn(slug):
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
 e=src_apifootball()
 src="API-Football 🔥" if e else ""
 if not e:
  e=src_thesportsdb();src="TheSportsDB ⚡" if e else ""
 if not e:
  e=src_espn("egy.1")+src_espn("eng.1")+src_espn("esp.1");src="ESPN 🌍" if e else ""
 td=datetime.now().strftime("%Y-%m-%d");tm=(datetime.now()+timedelta(days=1)).strftime("%Y-%m-%d")
 if not e: e=[{"h":"الجونة","a":"الزمالك","lg":"الدوري المصري","date":"2026-11-23","sc":"🕗 17:00"},{"h":"الأهلي","a":"بيراميدز","lg":"الدوري المصري","date":"2026-11-23","sc":"🕗 20:00"},{"h":"سموحة","a":"البنك الأهلي","lg":"الدوري المصري","date":"2026-11-24","sc":"🕗 17:00"},{"h":"المصري","a":"بترول أسيوط","lg":"الدوري المصري","date":"2026-11-24","sc":"🕗 20:00"}]
 print(f"Matches: {len(e)} from {src}")
 CACHE.update({"today":[x for x in e if x["date"]==td],"tomorrow":[x for x in e if x["date"]==tm],"week":e,"live":[x for x in e if "LIVE" in x["sc"] or "🔴" in x["sc"]],"src":src})
def fmt(t,l):
 s=f"{t}\n{UT}\n📡 المصدر: {CACHE.get('src','')}\n\n"
 if not l: return s+"مفيش ماتشات ⚽\n😴 خد راحة النهاردة"
 for m in l: s+=f"⚽ {m['h']} 🆚 {m['a']}\n🏆 {m['lg']} | {m['sc']} | 📅 {m['date']}\n━━━━━━━━━━━\n"
 return s
def kb_main(u):
 e,_=getmod(u);p=pts.get(u,0)
 k=[]
 k.append([InlineKeyboardButton(f"🔥 {e} | ⭐ {p} | ولعهااا 🔥",callback_data="menu")])
 k.append([InlineKeyboardButton("🔥 حماس 🔥",callback_data="hype"),InlineKeyboardButton("🎁 مكافأة يومية 🎁",callback_data="daily")])
 k.append([InlineKeyboardButton("👤 بروفايلي 👤",callback_data="profile"),InlineKeyboardButton("🎨 الثيم 🎨",callback_data="theme")])
 k.append([InlineKeyboardButton("🏆 ترتيب النقاط 🏆",callback_data="leader")])
 k.append([InlineKeyboardButton("📅 جدول الماتشات 📅",callback_data="schedule")])
 k.append([InlineKeyboardButton("🔴 لايف 🔴",callback_data="live"),InlineKeyboardButton("🌍 كل العالم 🌍",callback_data="week")])
 k.append([InlineKeyboardButton("🤖 توقع AI 🤖",callback_data="ai"),InlineKeyboardButton("📋 تشكيلة 📋",callback_data="lineup")])
 k.append([InlineKeyboardButton("🏟️ تفاصيل 🏟️",callback_data="details"),InlineKeyboardButton("⭐ تقييم ⭐",callback_data="rate")])
 k.append([InlineKeyboardButton("🔴 أخبار الأهلي 🔴",callback_data="ahly"),InlineKeyboardButton("⚪ أخبار الزمالك ⚪",callback_data="zamalek")])
 k.append([InlineKeyboardButton("🌍 أخبار عالمية 🌍",callback_data="world")])
 k.append([InlineKeyboardButton("📊 ترتيب 📊",callback_data="stand"),InlineKeyboardButton("🎯 هدافين 🎯",callback_data="top")])
 k.append([InlineKeyboardButton("⚔️ قارن ⚔️",callback_data="cmp"),InlineKeyboardButton("🤼 مواجهات 🤼",callback_data="h2h")])
 k.append([InlineKeyboardButton("🏆 فانتازي 🏆",callback_data="fant"),InlineKeyboardButton("🔮 توقع 🔮",callback_data="pred")])
 k.append([InlineKeyboardButton("🎲 خمن 🎲",callback_data="guess"),InlineKeyboardButton("🎰 عجلة 🎰",callback_data="wheel")])
 k.append([InlineKeyboardButton("😂 ميمز 😂",callback_data="meme"),InlineKeyboardButton("📰 انتقالات 📰",callback_data="trans")])
 k.append([InlineKeyboardButton("⭐ اللاعيبة ⭐",callback_data="players"),InlineKeyboardButton("🧠 تحدي 🧠",callback_data="quiz")])
 k.append([InlineKeyboardButton("📚 مبادئ 📚",callback_data="basic"),InlineKeyboardButton("💡 نصيحة 💡",callback_data="tip")])
 k.append([InlineKeyboardButton("📺 بث ✅",callback_data="stream"),InlineKeyboardButton("🎥 أهداف ✅",callback_data="goals")])
 k.append([InlineKeyboardButton("👥 فانتازي جماعي ✅",callback_data="fleague"),InlineKeyboardButton("💬 شات ✅",callback_data="chat")])
 k.append([InlineKeyboardButton("🏆 دوري توقعات ✅",callback_data="pleague"),InlineKeyboardButton("🎙️ تعليق ✅",callback_data="comm")])
 k.append([InlineKeyboardButton(f"📅 {LAST} | 🔜 {NEXT} | 🔥",callback_data="schedule")])
 return InlineKeyboardMarkup(k)
def back(): return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القايمة 🔙",callback_data="menu")]])
async def start(up,ctx):
 u=up.effective_user.id;e,w=getmod(u)
 t=f"{BANNER}\n\n{w}\n\n👋 أهلا بيك يا {up.effective_user.first_name} ! 🔥\n🌍 كل الماتشات + 🤖 AI + 📺 بث + 💬 شات\n⭐ نقاطك: {pts.get(u,0)} ⭐\n📡 المصدر: {CACHE.get('src','')}\n\n{UT}\n\n👇 اختار وولعها:"
 if up.message: await up.message.reply_text(t,reply_markup=kb_main(u))
 else: await up.callback_query.edit_message_text(t,reply_markup=kb_main(u))
async def btn(up,ctx):
 q=up.callback_query;await q.answer();u=q.from_user.id;d=q.data;e,_=getmod(u)
 if d=="menu": await start(up,ctx);return
 if d=="hype": await q.edit_message_text(f"{BANNER}\n\n{random.choice(HYPE)}\n\n🔥 انت جاهز للماتش الجاي؟\n⚽ الأهلي 🆚 بيراميدز\n📅 23 نوفمبر | 8 م\n🏟️ استاد القاهرة\n\n🔥🔥🔥 يلا يا أهليييي 🔥🔥🔥",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔥 ولعها أكتر 🔥",callback_data="hype")],[InlineKeyboardButton("🔙 القايمة",callback_data="menu")]]));return
 if d=="daily":
  td=datetime.now().strftime("%Y-%m-%d")
  if daily.get(u)==td: await q.edit_message_text("⏳ خدت مكافأتك النهاردة، تعالى بكرة! 🔥",reply_markup=back());return
  daily[u]=td;pts[u]=pts.get(u,0)+50;await q.edit_message_text(f"🎁🎁🎁 مبرووووك! 🎁🎁🎁\n\n🔥 خدت 50 نقطة!\n⭐ رصيدك: {pts[u]}\n\n{random.choice(HYPE)}",reply_markup=back());return
 if d=="profile": await q.edit_message_text(f"👤━━━━━━━━━━━━👤\n👤 بروفايلك يا نجم\n👤━━━━━━━━━━━━👤\n\n🆔 {u}\n⭐ نقاطك: {pts.get(u,0)} ⭐\n🏆 فريقك: {fant.get(u,[])}\n🎨 ثيمك: {modd.get(u,'gold')}\n🎁 مكافأة اليوم: {'✅ خدتها 🔥' if daily.get(u)==datetime.now().strftime('%Y-%m-%d') else '❌ لسه - دوس مكافأة يومية!'}\n\n{random.choice(HYPE)}",reply_markup=back());return
 if d=="theme": await q.edit_message_text("🎨🎨 اختار ثيمك يا نجم 🎨🎨:",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("👑 ذهبي 👑",callback_data="th_gold")],[InlineKeyboardButton("⚡ نيون ⚡",callback_data="th_neon")],[InlineKeyboardButton("🔥 ناري 🔥",callback_data="th_fire")],[InlineKeyboardButton("🧊 ثلجي 🧊",callback_data="th_ice")],[InlineKeyboardButton("🔙 القايمة",callback_data="menu")]]));return
 if d.startswith("th_"): modd[u]=d.replace("th_","");e2,w=getmod(u);await q.edit_message_text(f"{BANNER}\n\n{w}\nتم تغيير الثيم ✅🔥",reply_markup=kb_main(u));return
 if d=="leader":
  t="🏆━━━━━━━━━━━━🏆\n🏆 ترتيب النقاط 🏆\n🏆━━━━━━━━━━━━🏆\n"
  for i,(uu,pp) in enumerate(sorted(pts.items(),key=lambda x:x[1],reverse=True)[:10],1):
   med="🥇" if i==1 else "🥈" if i==2 else "🥉" if i==3 else f"{i}️⃣"
   t+=f"{med} {str(uu)[-4:]} - {pp} ⭐\n"
  if not pts: t+="لسه مفيش حد لعب! كن أول واحد 🔥"
  await q.edit_message_text(t,reply_markup=back());return
 if d=="world": await q.edit_message_text("🌍🌍 أخبار عالمية مولعة 🌍🌍\n\n🏴󐁧󐁢󐁥󐁮󐁧󐁿 ليفربول بيجهز عرض لصلاح للتجديد 🔥\n🇪🇸 ريال مدريد بيفكر في مبابي ككابتن 👑\n🇮🇹 إنتر بيقرب من الدوري 💪",reply_markup=back());return
 if d=="schedule": await q.edit_message_text(f"📅📅 جدول الماتشات 📅📅\n\n{UT}",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📅 النهاردة 🔥",callback_data="today")],[InlineKeyboardButton("📅 بكرة 📅",callback_data="tom")],[InlineKeyboardButton("📅 الأسبوع 🌍",callback_data="week")],[InlineKeyboardButton("🔙 القايمة",callback_data="menu")]]));return
 if d=="today": await q.edit_message_text(fmt("📅🔥 النهاردة 🔥📅",CACHE["today"]),reply_markup=back());return
 if d=="tom": await q.edit_message_text(fmt("📅 بكرة 📅",CACHE["tomorrow"]),reply_markup=back());return
 if d=="week": await q.edit_message_text(fmt("📅🌍 الأسبوع 🌍📅",CACHE["week"]),reply_markup=back());return
 if d=="live": await q.edit_message_text(fmt("🔴🔴 لايف 🔴🔴",CACHE["live"]),reply_markup=back());return
 if d=="ai": await q.edit_message_text("🤖🤖 توقع AI مولع 🤖🤖\n⚽ الأهلي 🆚 بيراميدز\n🤖 الأهلي يكسب 2-1 🔥\n📈 45% | 30% | 25%\n\n🔥 توقع نار!",reply_markup=back());return
 if d=="lineup": await q.edit_message_text("📋🔥 تشكيلة الأهلي النارية 🔥📋\n🧤 الشناوي 🧤\n🛡️ هاني - ياسر - داري - معلول\n⚙️ مروان - إمام - أفشة\n⚽ تاو - وسام - الشحات 🔥",reply_markup=back());return
 if d=="details": await q.edit_message_text("🏟️🔥 الأهلي 🆚 بيراميدز 🔥🏟️\n📅 23 نوفمبر | 8 م\n🏟️ استاد القاهرة\n👨‍⚖️ أمين عمر\n📺 ON Sport\n\n🔥 ماتش نار!",reply_markup=back());return
 if d=="rate": await q.edit_message_text("⭐⭐ تقييم النجوم ⭐⭐\n🔴 وسام 9.2 🔥 | إمام 8.5\n⚪ زيزو 8.8 👑",reply_markup=back());return
 if d=="ahly": await q.edit_message_text("🔴🔴 أخبار الأهلي 🔴🔴\n🏋️ بيستعد لبيراميدز 23 نوفمبر 8 م 🔥\n💪 وسام جاهز 💪\n\n🦅 يلا يا أهليييي 🦅",reply_markup=back());return
 if d=="zamalek": await q.edit_message_text("⚪⚪ أخبار الزمالك ⚪⚪\n🏋️ بيستعد للجونة 23 نوفمبر 5 م 🔥\n💪 زيزو جاهز 💪\n\n🏹 يلا يا زمالك 🏹",reply_markup=back());return
 if d=="stand": await q.edit_message_text("📊📊 ترتيب المصري 📊📊\n🥇 بيراميدز 18\n🥈 الأهلي 17 🔥\n🥉 الزمالك 16",reply_markup=back());return
 if d=="top": await q.edit_message_text("🎯🎯 هدافين 🎯🎯\n🥇 وسام 7 🔥\n🥈 زيزو 6 👑",reply_markup=back());return
 if d=="cmp": await q.edit_message_text("⚔️⚔️ ميسي 🆚 رونالدو ⚔️⚔️\n🐐 ميسي مهارة 99 🔥\n👑 رونالدو قوة 98 💪",reply_markup=back());return
 if d=="h2h": await q.edit_message_text("🤼🤼 الأهلي 🆚 الزمالك 🤼🤼\n🔴 الأهلي 61 🔥 | ⚪ الزمالك 29 | 🤝 40",reply_markup=back());return
 if d=="fant": await q.edit_message_text(f"🏆🔥 فانتازي 🔥🏆\nفريقك: {fant.get(u,[])}\n⭐ {pts.get(u,0)} ⭐",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("➕ صلاح 👑",callback_data="f_salah")],[InlineKeyboardButton("🔙 القايمة",callback_data="menu")]]));return
 if d=="f_salah": fant[u]=fant.get(u,[])+["صلاح"];await q.edit_message_text(f"✅ ضفت صلاح! 👑🔥\n{random.choice(GOAL)}",reply_markup=back());return
 if d=="pred": await q.edit_message_text("🔮🔥 توقع الأهلي 🆚 بيراميدز 🔥🔮",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔴 الأهلي 🔴",callback_data="p_ahly")],[InlineKeyboardButton("🤝 تعادل 🤝",callback_data="p_draw")]]));return
 if d.startswith("p_"): pts[u]=pts.get(u,0)+10;pleague[u]=pts[u];await q.edit_message_text(f"✅ توقعك اتسجل! 🔥\n+10 نقاط ⭐ {pts[u]}\n\n{random.choice(HYPE)}",reply_markup=kb_main(u));return
 if d=="guess":
  i=quiz_idx.get(u,0)%len(GUESS);qq,oo,aa=GUESS[i];quiz_idx[u]=i+1
  await q.edit_message_text(qq,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(oo[0],callback_data="g_ok")],[InlineKeyboardButton(oo[1],callback_data="g_no")]]));return
 if d=="g_ok": pts[u]=pts.get(u,0)+5;await q.edit_message_text(f"{random.choice(GOAL)}\n✅ صح! +5 ⭐ {pts[u]}",reply_markup=back());return
 if d=="g_no": await q.edit_message_text("❌ غلط! حاول تاني 🔥\n💪 انت تقدر!",reply_markup=back());return
 if d=="wheel": r=random.choice(["🎁 10 نقاط!","🎁 50 نقطة!","🎁 100 نقطة!","😅 مفيش حظ"]);pts[u]=pts.get(u,0)+(10 if "10" in r else 50 if "50" in r else 100 if "100" in r else 0);await q.edit_message_text(f"🎰🎰 عجلة الحظ 🎰🎰\n🎰 {r}\n⭐ {pts[u]} ⭐\n\n{random.choice(HYPE)}",reply_markup=back());return
 if d=="meme": await q.edit_message_text(random.choice(MEMES),reply_markup=back());return
 if d=="trans": await q.edit_message_text("📰📰 انتقالات مولعة 📰📰\n🔴 الأهلي بيجهز عرض لمهاجم أجنبي 🔥",reply_markup=back());return
 if d=="players": await q.edit_message_text("⭐⭐ اللاعيبة النجوم ⭐⭐\n👑 صلاح 👑\n🏟️ ليفربول | ⚡ 93 | 🎯 95 🔥\n🐐 ميسي 🐐\n🏟️ ميامي | ⚡ 99 🔥\n🤖 هالاند 🤖\n🏟️ سيتي | ⚡ 95 💪",reply_markup=back());return
 if d=="quiz":
  i=quiz_idx.get(u,0)%len(QUIZ);qq,oo,aa=QUIZ[i];quiz_idx[u]=i+1
  await q.edit_message_text(qq,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(oo[0],callback_data="q_ok")],[InlineKeyboardButton(oo[1],callback_data="q_no")]]));return
 if d=="q_ok": pts[u]=pts.get(u,0)+10;await q.edit_message_text(f"{random.choice(GOAL)}\n✅ صح! +10 ⭐ {pts[u]}",reply_markup=back());return
 if d=="q_no": await q.edit_message_text("❌ غلط! حاول تاني 🔥\n💪 انت تقدر!",reply_markup=back());return
 if d=="basic": await q.edit_message_text("📚📚 مبادئ الكورة 📚📚\n🧤 حارس | 🛡️ مدافع | ⚙️ وسط | ⚽ مهاجم\n❌ التسلل: أقرب للجون من آخر مدافع",reply_markup=back());return
 if d=="tip": await q.edit_message_text(random.choice(TIPS),reply_markup=back());return
 if d=="stream": await q.edit_message_text("📺📺 بث مباشر 🔥📺📺\nhttps://www.youtube.com/@ONTimeSports\nhttps://www.yallashoot.com",reply_markup=back());return
 if d=="goals": await q.edit_message_text("🎥🎥 هدف وسام في بيراميدز 🔥🎥🎥\nhttps://www.youtube.com/results?search_query=هدف+وسام+بيراميدز",reply_markup=back());return
 if d=="comm": await q.edit_message_text("🎙️🎙️ تعليق ناري 🎙️🎙️\n⚽ الأهلي 1 - 0 بيراميدز\n• د 10: جووووووول وسام 🔥🔥🔥",reply_markup=back());return
 if d=="fleague": await q.edit_message_text("👥👥 فانتازي جماعي 👥👥\nاكتب: دخول 1234\nأو اعمل دوري:",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("➕ اعمل دوري 🔥",callback_data="mkleague")],[InlineKeyboardButton("🔙 القايمة",callback_data="menu")]]));return
 if d=="mkleague": c=str(random.randint(1000,9999));leagues[c]={"m":{u:pts.get(u,0)}};await q.edit_message_text(f"✅ عملت دوري! 🔥\n🔑 الكود: {c}\nابعته لصحابك وولعوها 🔥",reply_markup=back());return
 if d=="chat":
  t="💬💬 شات جماهير مولع 💬💬\n"
  if not chat: t+="لسه فاضي، اكتب: اهلي: يلا يا أهلي 🔥"
  else:
   for m in chat[-10:]: t+=f"{m}\n"
  await q.edit_message_text(t,reply_markup=back());return
 if d=="pleague":
  pleague[u]=pts.get(u,0);t="🏆🏆 دوري التوقعات 🏆🏆\n"
  for i,(uu,pp) in enumerate(sorted(pleague.items(),key=lambda x:x[1],reverse=True)[:10],1): t+=f"{i}️⃣ {str(uu)[-4:]} - {pp} ⭐\n"
  await q.edit_message_text(t,reply_markup=back());return
async def txt(up,ctx):
 u=up.effective_user.id;r=up.message.text
 if r.startswith("اهلي:") or r.startswith("أهلي:"): chat.append(f"🔴 {up.effective_user.first_name}: {r.split(':',1)[1]}");await up.message.reply_text("✅ اتنشرت في شات الأهلي! 🔴🔥",reply_markup=kb_main(u));return
 if r.startswith("زمالك:"): chat.append(f"⚪ {up.effective_user.first_name}: {r.split(':',1)[1]}");await up.message.reply_text("✅ اتنشرت في شات الزمالك! ⚪🔥",reply_markup=kb_main(u));return
 if r.startswith("دخول"):
  c=r.replace("دخول","").strip()
  if c in leagues: leagues[c]["m"][u]=pts.get(u,0);await up.message.reply_text(f"✅ دخلت الدوري {c}! 🔥",reply_markup=kb_main(u))
  else: await up.message.reply_text("❌ الكود مش موجود",reply_markup=kb_main(u))
  return
 await up.message.reply_text(f"وصلت: {r} ✅🔥\n{UT}",reply_markup=kb_main(u))
def main():
 if not TOKEN: print("مفيش توكن");return
 threading.Thread(target=keep,daemon=True).start()
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
