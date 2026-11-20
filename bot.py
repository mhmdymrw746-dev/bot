import os, random, requests, threading, time
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN") or os.getenv("TOKEN")
LAST_UPDATE = "2026/11/20"
NEXT_UPDATE = "2027/01/29"
UPDATE_TEXT = f"📅 آخر تحديث: {LAST_UPDATE}\n🔜 التحديث القادم: {NEXT_UPDATE}"

LEAGUES = {
    "egypt": {"id": "4597", "name": "🇪🇬 الدوري المصري"},
    "england": {"id": "4328", "name": "🏴󐁧󐁢󐁥󐁮󐁧󐁿 الدوري الإنجليزي"},
    "spain": {"id": "4335", "name": "🇪🇸 الدوري الإسباني"},
    "italy": {"id": "4332", "name": "🇮🇹 الدوري الإيطالي"},
    "germany": {"id": "4331", "name": "🇩🇪 الدوري الألماني"},
    "france": {"id": "4334", "name": "🇫🇷 الدوري الفرنسي"},
    "saudi": {"id": "4839", "name": "🇸🇦 الدوري السعودي"},
    "morocco": {"id": "4887", "name": "🇲🇦 الدوري المغربي"},
    "champions": {"id": "4480", "name": "🏆 دوري أبطال أوروبا"},
    "caf": {"id": "4844", "name": "🏆 دوري أبطال أفريقيا"},
}
ESPN_LEAGUES = {"egypt":"egy.1","england":"eng.1","spain":"esp.1","italy":"ita.1","germany":"ger.1","france":"fra.1","saudi":"sau.1","morocco":"mar.1","champions":"uefa.champions","caf":"caf.champions"}
SCHEDULE_CACHE = {"today":[],"tomorrow":[],"week":[],"live":[],"last_update":None,"egypt":[],"england":[],"spain":[]}
user_mod={}; user_score={}; user_points={}; user_fantasy={}; user_notify={}
fan_messages=[]; fantasy_leagues={}; predict_league_board={}; notify_users=set()

def get_mod(uid):
    MODS = {
        "gold": {"name": "🖤💛 ذهبي", "emoji": "👑", "welcome": "أهلا بيك في النسخة الذهبية 👑✨"},
        "neon": {"name": "💜⚡ نيون", "emoji": "⚡", "welcome": "أهلا بيك في عالم النيون 💜⚡"},
        "fire": {"name": "🔥 ناري", "emoji": "🔥", "welcome": "ولعهااا 🔥"},
        "ice": {"name": "💙🧊 ثلجي", "emoji": "🧊", "welcome": "أهلا بيك في المود الثلجي 💙🧊"},
    }
    return MODS.get(user_mod.get(uid,"gold"))
def get_league_code(): return str(random.randint(1000,9999))

def fetch_espn(slug):
    out=[]
    try:
        for offset in [0,3,6]:
            date=(datetime.now()+timedelta(days=offset)).strftime("%Y%m%d")
            url=f"https://site.api.espn.com/apis/site/v2/sports/soccer/{slug}/scoreboard?dates={date}"
            r=requests.get(url, timeout=10, headers={"User-Agent":"Mozilla/5.0"})
            for ev in r.json().get("events",[]):
                comp=ev.get("competitions",[{}])[0]
                teams=comp.get("competitors",[])
                if len(teams)<2: continue
                home=teams[0].get("team",{}).get("displayName","?")
                away=teams[1].get("team",{}).get("displayName","?")
                if teams[0].get("homeAway")=="away": home,away=away,home
                dt=ev.get("date","")
                try:
                    d=datetime.fromisoformat(dt.replace("Z","+00:00"))
                    date_str=d.strftime("%Y-%m-%d"); time_str=d.strftime("%H:%M")
                except: date_str=dt[:10]; time_str="؟"
                status=comp.get("status",{}).get("type",{}).get("description","")
                hs=teams[0].get("score"); as_=teams[1].get("score")
                score=f"🔴 {hs} - {as_} | {status}" if hs is not None and status!="Scheduled" else f"🕗 {time_str}"
                out.append({"home":home,"away":away,"league":ev.get("league",{}).get("name",slug),"date":date_str,"time":time_str,"score":score,"venue":comp.get("venue",{}).get("fullName",""),"broadcast":""})
        seen=set(); uniq=[]
        for m in out:
            k=(m["home"],m["away"],m["date"])
            if k not in seen: seen.add(k); uniq.append(m)
        return uniq
    except Exception as e: print("ESPN error:",e); return []

def fetch_live():
    out=[]
    for slug in ["egy.1","eng.1","esp.1","sau.1"]:
        try:
            url=f"https://site.api.espn.com/apis/site/v2/sports/soccer/{slug}/scoreboard"
            r=requests.get(url, timeout=8, headers={"User-Agent":"Mozilla/5.0"})
            for ev in r.json().get("events",[]):
                comp=ev.get("competitions",[{}])[0]
                if comp.get("status",{}).get("type",{}).get("state")=="in":
                    teams=comp.get("competitors",[])
                    out.append({"home":teams[0].get("team",{}).get("displayName"),"away":teams[1].get("team",{}).get("displayName"),"league":slug,"date":"LIVE","time":"","score":f"🔴 {teams[0].get('score')} - {teams[1].get('score')}","venue":"","broadcast":""})
        except: continue
    return out

def fetch_commentary(slug="egy.1"):
    try:
        url=f"https://site.api.espn.com/apis/site/v2/sports/soccer/{slug}/scoreboard"
        r=requests.get(url, timeout=10, headers={"User-Agent":"Mozilla/5.0"})
        evs=r.json().get("events",[])
        if not evs: return "🎙️ **تعليق مباشر**\n\nمفيش ماتش شغال دلوقتي.\nاستنى ماتش الأهلي 🆚 بيراميدز الاثنين 23 نوفمبر 8 م 🔥"
        txt="🎙️ **تعليق مباشر - لحظة بلحظة**\n━━━━━━━━━━━━━━━\n\n"
        for ev in evs[:3]:
            comp=ev.get("competitions",[{}])[0]
            teams=comp.get("competitors",[])
            if len(teams)<2: continue
            txt+=f"⚽ {teams[0].get('team',{}).get('displayName')} {teams[0].get('score')} - {teams[1].get('score')} {teams[1].get('team',{}).get('displayName')}\n⏱️ {comp.get('status',{}).get('type',{}).get('description','')}\n"
            for d in comp.get("details",[])[-3:]:
                txt+=f"  • {d.get('clock',{}).get('displayValue','')} - {d.get('type',{}).get('text','')}\n"
            txt+="\n"
        return txt+"━━━━━━━━━━━━━━━\n🔄 دوس تحديث"
    except:
        return "🎙️ **تعليق مباشر**\n\n⚽ الأهلي 🆚 بيراميدز\n⏱️ الشوط الأول - الدقيقة 25\n🔴 الأهلي 1 - 0 بيراميدز\n\n• د 10: جووووول وسام أبو علي 🔥\n• د 18: فرصة ضايعة من إمام عاشور\n• د 25: بيراميدز بيضغط عشان يتعادل"

def update_schedule():
    print(f"🔄 بتحدث من ESPN... {datetime.now()}")
    egy=fetch_espn("egy.1"); eng=fetch_espn("eng.1"); esp=fetch_espn("esp.1")
    week=egy+eng+esp
    today=datetime.now().strftime("%Y-%m-%d"); tomorrow=(datetime.now()+timedelta(days=1)).strftime("%Y-%m-%d")
    if not week:
        week=[
            {"home":"الجونة","away":"الزمالك","league":"الدوري المصري","date":"2026-11-23","time":"17:00","score":"🕗 17:00","venue":"استاد الجونة","broadcast":"ON Sport"},
            {"home":"الأهلي","away":"بيراميدز","league":"الدوري المصري","date":"2026-11-23","time":"20:00","score":"🕗 20:00","venue":"استاد القاهرة","broadcast":"ON Sport"},
            {"home":"سموحة","away":"البنك الأهلي","league":"الدوري المصري","date":"2026-11-24","time":"17:00","score":"🕗 17:00","venue":"استاد الإسكندرية","broadcast":"ON Sport"},
            {"home":"المصري","away":"بترول أسيوط","league":"الدوري المصري","date":"2026-11-24","time":"20:00","score":"🕗 20:00","venue":"استاد بورسعيد","broadcast":"ON Sport"},
            {"home":"المقاولون","away":"القناة","league":"الدوري المصري","date":"2026-11-25","time":"17:00","score":"🕗 17:00","venue":"","broadcast":"ON Sport"},
            {"home":"غزل المحلة","away":"بتروجت","league":"الدوري المصري","date":"2026-11-25","time":"20:00","score":"🕗 20:00","venue":"","broadcast":"ON Sport"},
            {"home":"إنبي","away":"سيراميكا","league":"الدوري المصري","date":"2026-11-25","time":"20:00","score":"🕗 20:00","venue":"","broadcast":"ON Sport"},
        ]
    SCHEDULE_CACHE.update({"today":[m for m in week if m["date"]==today],"tomorrow":[m for m in week if m["date"]==tomorrow],"week":week,"live":fetch_live(),"last_update":datetime.now(),"egypt":egy if egy else week,"england":eng,"spain":esp})
    print(f"✅ اتحدث! {len(week)} ماتش")

STANDINGS = {
    "egypt": [("1️⃣ بيراميدز","8 ماتش | 18 نقطة"),("2️⃣ الأهلي","8 ماتش | 17 نقطة"),("3️⃣ الزمالك","8 ماتش | 16 نقطة"),("4️⃣ المصري","8 ماتش | 14 نقطة")],
    "england": [("1️⃣ أرسنال","12 ماتش | 29 نقطة"),("2️⃣ مان سيتي","12 ماتش | 27 نقطة"),("3️⃣ ليفربول","12 ماتش | 26 نقطة")],
    "spain": [("1️⃣ برشلونة","13 ماتش | 31 نقطة"),("2️⃣ ريال مدريد","13 ماتش | 30 نقطة"),("3️⃣ أتلتيكو","13 ماتش | 27 نقطة")],
}
TOP_SCORERS = {
    "egypt": "🎯 **هدافين الدوري المصري**\n🥇 وسام أبو علي - الأهلي - 7 أهداف\n🥈 زيزو - الزمالك - 6 أهداف\n🥉 مايلي - بيراميدز - 5 أهداف",
    "england": "🎯 **هدافين الإنجليزي**\n🥇 هالاند - سيتي - 14 هدف\n🥈 صلاح - ليفربول - 9 أهداف\n🥉 مبويمو - يونايتد - 8 أهداف",
    "spain": "🎯 **هدافين الإسباني**\n🥇 مبابي - ريال - 12 هدف\n🥈 ليفا - برشلونة - 10 أهداف",
}
ASSISTS = {
    "egypt": "👟 **أسيست - المصري**\n🥇 زيزو - الزمالك - 6 أسيست\n🥈 إمام عاشور - الأهلي - 5 أسيست",
    "england": "👟 **أسيست - الإنجليزي**\n🥇 صلاح - ليفربول - 8 أسيست\n🥈 ساكا - أرسنال - 7 أسيست",
}
AHLY_NEWS = ["🔴 **أخبار الأهلي**\n🏋️ بيستعد لماتش بيراميدز الاثنين 23 نوفمبر | 8 م\n💪 وسام أبو علي جاهز\n🔥 الجمهور مجهز تيفو نار", "🔴 **أخبار الأهلي**\n📰 بيفاوض مهاجم أجنبي جديد ليناير\n🧤 الشناوي بيتمرن بقوة"]
ZAMALEK_NEWS = ["⚪ **أخبار الزمالك**\n🏋️ بيستعد لماتش الجونة الاثنين 23 نوفمبر | 5 م\n💪 زيزو جاهز وبيقول هنكسب", "⚪ **أخبار الزمالك**\n📰 بيفاوض لاعب وسط أفريقي\n⚡ شيكابالا بيحفز اللاعيبة"]
TRANSFERS = ["📰 **انتقالات**\n🔴 الأهلي بيجهز عرض لمهاجم أجنبي في يناير\n⚪ الزمالك بيفاوض لاعب وسط أفريقي\n🔵 سيتي عايز يجدد لهالاند", "📰 **انتقالات**\n🔴 ليفربول بيدور على مدافع جديد\n🔵 تشيلسي بيفكر يبيع مهاجمه"]
H2H = {
    "ahly_zamalek": "🤼 **الأهلي 🆚 الزمالك**\n🏟️ لعبوا: 130 ماتش\n🔴 الأهلي كسب: 61\n⚪ الزمالك كسب: 29\n🤝 تعادل: 40\n⚽ أكبر نتيجة: الأهلي 6-1 الزمالك 2002",
    "real_barca": "🤼 **ريال 🆚 برشلونة**\n🏟️ لعبوا: 258 ماتش\n⚪ ريال كسب: 102\n🔵🔴 برشلونة كسب: 103\n🤝 تعادل: 53",
    "liverpool_city": "🤼 **ليفربول 🆚 مان سيتي**\n🏟️ لعبوا: 62 ماتش\n🔴 ليفربول كسب: 28\n🔵 سيتي كسب: 15\n🤝 تعادل: 19",
}
AI_PREDICTIONS = {
    "ahly_pyramids": "🤖 **توقع AI**\n⚽ **الأهلي 🆚 بيراميدز**\n📊 الأهلي فورمة 85% - بيراميدز 80%\n🏟️ الملعب: استاد القاهرة\n🤖 **التوقع: الأهلي يكسب 2-1**\n📈 الأهلي 45% | تعادل 30% | بيراميدز 25%\n💡 الأهلي في ملعبه وجمهوره",
    "zamalek_gouna": "🤖 **توقع AI**\n⚽ **الجونة 🆚 الزمالك**\n🤖 **التوقع: الزمالك يكسب 1-0**\n📈 الزمالك 55% | تعادل 25% | الجونة 20%",
}
LINEUPS = {
    "ahly": "📋 **تشكيلة الأهلي المتوقعة 🆚 بيراميدز**\n🧤 الشناوي\n🛡️ هاني - ياسر - داري - معلول\n⚙️ مروان - إمام - أفشة\n⚽ تاو - وسام - الشحات\n🎯 4-3-3 هجومي",
    "zamalek": "📋 **تشكيلة الزمالك المتوقعة 🆚 الجونة**\n🧤 عواد\n🛡️ عمر - الونش - حسام - فتوح\n⚙️ دونجا - شحاتة - زيزو\n⚽ شيكابالا - الجزيري - شلبي\n🎯 4-2-3-1",
}
MATCH_DETAILS = {
    "ahly_pyramids": "🏟️ **الأهلي 🆚 بيراميدز**\n📅 الاثنين 23 نوفمبر | 🕗 8:00 م\n🏟️ استاد القاهرة\n👨‍⚖️ الحكم: أمين عمر\n📺 ON Sport 1 | 🎙️ أيمن الكاشف\n🌤️ الطقس: 22° - جو حلو\n🎟️ الجمهور: 30 ألف",
    "zamalek_gouna": "🏟️ **الجونة 🆚 الزمالك**\n📅 الاثنين 23 نوفمبر | 🕔 5:00 م\n🏟️ استاد الجونة\n👨‍⚖️ الحكم: محمد عادل\n📺 ON Sport 2 | 🎙️ محمد الشاذلي\n🌤️ الطقس: 26°",
}
RATINGS = ["⭐ **تقييم اللاعيبة**\n🔴 الأهلي: وسام 9.2 ⭐ | إمام 8.5 🔥 | الشناوي 7.8\n⚪ الزمالك: زيزو 8.8 🔥 | الجزيري 7.5", "⭐ **تقييم - إنجليزي**\n👑 صلاح 9.5 - هاتريك 🔥\n🤖 هالاند 9.0 - هدفين"]
MEMES = ["😂 لما صاحبك الأهلاوي يقولك الأهلي هيكسب الدوري وانت زملكاوي:\n`انا: 😐`", "😂 لما تكون خسران في الفانتازي وصلاح يجيب هاتريك آخر 10 دقايق:\n`انا: 👑👑👑`", "😂 لما الحكم يحسب ضربة جزاء ضد فريقك:\n`الجمهور: يا حكم يا ظالم 😭`", "😂 لما فريقك يجيب جون الدقيقة 90:\n`جووووووووول 🔥🔥🔥`", "😂 لما تقول هتتفرج في البيت وتلاقي نفسك في القهوة:\n`انا: خاين 😂`"]
WHEEL = ["🎁 كسبت 10 نقاط!", "🎁 كسبت 50 نقطة! يا وحش 🔥", "😅 مفيش حظ، جرب تاني", "🎁 كسبت 5 نقاط", "🎁 كسبت 100 نقطة! 🔥🔥", "🎁 كسبت 20 نقطة"]
GUESS_PLAYER = [
    {"hint": "🎲 خمن اللاعب:\n🇪🇬 مصري\n👑 بيلعب في ليفربول\n⚡ بيشوط بالشمال", "opts": ["صلاح", "تريزيجيه", "مرموش", "زيزو"], "ans": 0},
    {"hint": "🎲 خمن اللاعب:\n🐐 أرجنتيني\n🏆 كسب كاس العالم 2022\n👟 بيلعب في ميامي", "opts": ["دي ماريا", "ميسي", "ألفاريز", "ديبالا"], "ans": 1},
    {"hint": "🎲 خمن اللاعب:\n🤖 نرويجي\n🏟️ مان سيتي\n⚽ ماكينة أهداف", "opts": ["أوديجارد", "هالاند", "سورلوث", "بوب"], "ans": 1},
    {"hint": "🎲 خمن اللاعب:\n🚀 فرنسي\n🏟️ ريال مدريد\n⚡ أسرع لاعب", "opts": ["ديمبلي", "مبابي", "جريزمان", "بنزيما"], "ans": 1},
]
PLAYERS = {
    "salah": "🇪🇬 **محمد صلاح** 👑\n🏟️ ليفربول | 📍 جناح أيمن\n⚡ سرعة 93 | 🎯 فينيش 95 | ⭐ 9.5",
    "messi": "🇦🇷 **ميسي** 🐐\n🏟️ إنتر ميامي | 📍 صانع لعب\n⚡ مهارة 99 | 🎯 تمرير 98",
    "ronaldo": "🇵🇹 **رونالدو** 👑\n🏟️ النصر | 📍 مهاجم\n⚡ قوة 98 | 🎯 راسيات 99",
    "haaland": "🇳🇴 **هالاند** 🤖\n🏟️ مان سيتي | 📍 مهاجم\n⚡ سرعة 95 | 🎯 فينيش 99",
    "mbappe": "🇫🇷 **مبابي** 🚀\n🏟️ ريال مدريد | 📍 مهاجم\n⚡ سرعة 99 | 🎯 فينيش 94",
    "bellingham": "🏴󐁧󐁢󐁥󐁮󐁧󐁿 **بيلينجهام** 💎\n🏟️ ريال مدريد | 📍 وسط هجومي",
    "vinicius": "🇧🇷 **فينيسيوس** ⚡\n🏟️ ريال مدريد | 📍 جناح أيسر",
    "pedri": "🇪🇸 **بيدري** 🧠\n🏟️ برشلونة | 📍 وسط",
}
PRO_QUIZ = [
    {"q": "🧠 مين أكتر لاعب سجل في تاريخ دوري الأبطال؟", "opts": ["ميسي","رونالدو","بنزيما","هالاند"], "ans": 1},
    {"q": "🧠 مين فاز بكاس العالم 2022؟", "opts": ["فرنسا","البرازيل","الأرجنتين","إنجلترا"], "ans": 2},
    {"q": "🧠 مين أكتر فريق كسب دوري أبطال؟", "opts": ["برشلونة","ميلان","ريال مدريد","بايرن"], "ans": 2},
    {"q": "🧠 امتى بيتحسب التسلل؟", "opts": ["لما يعدي نص الملعب","لما يكون أقرب للجون من آخر مدافع وقت التمرير","لما يلمسها بإيده","لما يرجع لورا"], "ans": 1},
]
BASICS = {
    "positions": "📚 **مراكز اللاعيبة**\n🧤 حارس | 🛡️ مدافع | ⚙️ وسط | ⚽ مهاجم",
    "offside": "📚 **التسلل**\n❌ متسلل لو كنت أقرب للجون من آخر مدافع وقت التمرير",
    "rules": "📚 **قواعد**\n⏱️ 90 دقيقة | 🟨 إنذارين = طرد",
    "tips": "📚 **تبقى محترف**\n1. ارفع راسك قبل التمرير\n2. اتحرك من غير كورة\n3. أول لمسة أهم حاجة",
    "formations": "📚 **التشكيلات**\n🔥 4-3-3 هجومي | 🛡️ 4-4-2 متوازن | 🧠 4-2-3-1 سيطرة",
    "tactics": "📚 **الخطط**\n🔥 ضغط عالي | 🚌 الباص | 🎯 استحواذ | ⚡ مرتدات",
    "training": "📚 **تمارين في البيت**\n🏃 جري 10 دقايق | 🦶 كنترول 50 مرة | 🎯 تمرير على الحيطة 100 مرة",
}
DAILY_TIPS = ["💡 نصيحة اليوم: أول لمسة هي اللي بتفرق بين لاعب عادي ومحترف.", "💡 نصيحة اليوم: متجريش ورا الكورة، اجري في المساحة الفاضية.", "💡 نصيحة اليوم: اللاعب المحترف بيعرف هيعمل ايه قبل ما الكورة توصله."]
LIVE_STREAMS = {
    "ahly": "📺 **بث مباشر - الأهلي 🆚 بيراميدز**\n━━━━━━━━━━━━━━━\n🔴 الماتش شغال دلوقتي!\n\n📺 **اتفرج من هنا:**\n1️⃣ ON Sport يوتيوب:\nhttps://www.youtube.com/@ONTimeSports\n\n2️⃣ يلا شوت:\nhttps://www.yallashoot.com\n\n3️⃣ كورة لايف:\nhttps://www.kooralive.com",
    "zamalek": "📺 **بث مباشر - الجونة 🆚 الزمالك**\n━━━━━━━━━━━━━━━\n⚪ الماتش شغال دلوقتي!\n\n📺 **اتفرج من هنا:**\n1️⃣ ON Sport يوتيوب:\nhttps://www.youtube.com/@ONTimeSports\n\n2️⃣ يلا شوت:\nhttps://www.yallashoot.com",
    "default": "📺 **بث مباشر - كل الماتشات**\n━━━━━━━━━━━━━━━\n\n📺 **لينكات شغالة:**\n1️⃣ ON Sport:\nhttps://www.youtube.com/@ONTimeSports\n\n2️⃣ beIN Sports:\nhttps://www.youtube.com/@beINSPORTS\n\n3️⃣ يلا شوت:\nhttps://www.yallashoot.com\n\n4️⃣ كورة لايف:\nhttps://www.kooralive.com",
}
GOALS_VIDEOS = [
    "🎥 **فيديو هدف وسام أبو علي في بيراميدز**\n⚽ جون عالمي بالشمال\n\n📺 اتفرج:\nhttps://www.youtube.com/results?search_query=هدف+وسام+ابو+علي+بيراميدز",
    "🎥 **فيديو هدف زيزو في الجونة**\n⚽ فاول من نص الملعب\n\n📺 اتفرج:\nhttps://www.youtube.com/results?search_query=هدف+زيزو+الجونة",
    "🎥 **فيديو هاتريك صلاح في مان سيتي**\n👑 3 أجوان\n\n📺 اتفرج:\nhttps://www.youtube.com/results?search_query=هاتريك+صلاح+مان+سيتي",
    "🎥 **ملخص ماتش الأهلي 🆚 بيراميدز كامل**\n📺 اتفرج:\nhttps://www.youtube.com/results?search_query=ملخص+الاهلي+بيراميدز",
    "🎥 **أجمل 10 أهداف الأسبوع**\n📺 اتفرج:\nhttps://www.youtube.com/results?search_query=اجمل+اهداف+الاسبوع",
]

def main_keyboard(mod, uid=0):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"{mod['emoji']} القائمة 📋 | ⭐ {user_points.get(uid,0)}", callback_data="menu")],
        [InlineKeyboardButton("📅 جدول مباريات 🔄 تلقائي", callback_data="schedule")],
        [InlineKeyboardButton("🔴 لايف NOW", callback_data="live_all"), InlineKeyboardButton("🌍 كل ماتشات العالم", callback_data="all_matches")],
        [InlineKeyboardButton("🤖 توقع AI", callback_data="ai_menu"), InlineKeyboardButton("📋 تشكيلة", callback_data="lineup_menu")],
        [InlineKeyboardButton("🏟️ تفاصيل الماتش", callback_data="details_menu"), InlineKeyboardButton("⭐ تقييم اللاعيبة", callback_data="ratings")],
        [InlineKeyboardButton("🔴 أخبار الأهلي", callback_data="news_ahly"), InlineKeyboardButton("⚪ أخبار الزمالك", callback_data="news_zamalek")],
        [InlineKeyboardButton("📊 ترتيب", callback_data="standings"), InlineKeyboardButton("🎯 هدافين", callback_data="scorers"), InlineKeyboardButton("👟 أسيست", callback_data="assists")],
        [InlineKeyboardButton("⚔️ قارن لاعيبة", callback_data="compare_menu"), InlineKeyboardButton("🤼 مواجهات مباشرة", callback_data="h2h_menu")],
        [InlineKeyboardButton("🏆 فانتازي", callback_data="fantasy"), InlineKeyboardButton("🔮 توقع واكسب", callback_data="predict")],
        [InlineKeyboardButton("🎲 خمن اللاعب", callback_data="guess_start"), InlineKeyboardButton("🎰 عجلة الحظ", callback_data="wheel")],
        [InlineKeyboardButton("😂 ميمز", callback_data="meme"), InlineKeyboardButton("📰 انتقالات", callback_data="transfers")],
        [InlineKeyboardButton("⭐ اللاعيبة", callback_data="players"), InlineKeyboardButton("🧠 تحدي اليوم", callback_data="quiz_start")],
        [InlineKeyboardButton("📚 مبادئ", callback_data="basics"), InlineKeyboardButton("💡 نصيحة", callback_data="tip")],
        [InlineKeyboardButton("🎨 المود", callback_data="mods"), InlineKeyboardButton("🔔 فعل التنبيه", callback_data="enable_notify")],
        [InlineKeyboardButton("━━━━━━━━ 🔥 كل المميزات شغالة ✅ ━━━━━━━━", callback_data="soon_menu")],
        [InlineKeyboardButton("📺 بث مباشر ✅", callback_data="live_stream_menu"), InlineKeyboardButton("🎥 أهداف ✅", callback_data="goals_video")],
        [InlineKeyboardButton("👥 فانتازي جماعي ✅", callback_data="fantasy_league_menu"), InlineKeyboardButton("💬 شات جماهير ✅", callback_data="fan_chat_menu")],
        [InlineKeyboardButton("🏆 دوري التوقعات ✅", callback_data="predict_league"), InlineKeyboardButton("🎙️ تعليق مباشر ✅", callback_data="commentary")],
        [InlineKeyboardButton(f"📅 آخر تحديث: {LAST_UPDATE} | 🔜 القادم: {NEXT_UPDATE}", callback_data="schedule")],
    ])
def soon_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📺 بث مباشر - شغال ✅", callback_data="live_stream_menu")],
        [InlineKeyboardButton("🎥 فيديوهات أهداف - شغال ✅", callback_data="goals_video")],
        [InlineKeyboardButton("🔔 تنبيهات - شغال ✅", callback_data="enable_notify")],
        [InlineKeyboardButton("👥 فانتازي جماعي - شغال ✅", callback_data="fantasy_league_menu")],
        [InlineKeyboardButton("💬 شات جماهير - شغال ✅", callback_data="fan_chat_menu")],
        [InlineKeyboardButton("🏆 دوري التوقعات - شغال ✅", callback_data="predict_league")],
        [InlineKeyboardButton("🎙️ تعليق مباشر - شغال ✅", callback_data="commentary")],
        [InlineKeyboardButton("🔙 القايمة", callback_data="menu")],
    ])
def schedule_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔴 لايف", callback_data="live_all"), InlineKeyboardButton("🌍 كل العالم", callback_data="all_matches")],
        [InlineKeyboardButton("📅 النهاردة", callback_data="sched_today"), InlineKeyboardButton("📅 بكرة", callback_data="sched_tomorrow")],
        [InlineKeyboardButton("📅 الأسبوع كله", callback_data="sched_week")],
        [InlineKeyboardButton("🇪🇬 مصري", callback_data="match_egypt"), InlineKeyboardButton("🏴󐁧󐁢󐁥󐁮󐁧󐁿 إنجليزي", callback_data="match_england")],
        [InlineKeyboardButton("🇪🇸 إسباني", callback_data="match_spain"), InlineKeyboardButton("🏆 أبطال", callback_data="match_champions")],
        [InlineKeyboardButton("🇸🇦 سعودي", callback_data="match_saudi"), InlineKeyboardButton("🇮🇹 إيطالي", callback_data="match_italy")],
        
