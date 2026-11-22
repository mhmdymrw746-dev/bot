# bot.py - بوت عدي WAR - PART 1
# الاونر: عدي 8188263997
import os, json, random, time, threading
from datetime import datetime
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

app_web = Flask(__name__)
@app_web.route('/')
def home(): return "Bot WAR by Ady Alive"
def run_web(): app_web.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
threading.Thread(target=run_web, daemon=True).start()

TOKEN = os.environ.get("TOKEN") or "PUT_YOUR_TOKEN_HERE"
OWNER_ID = 8188263997
VODAFONE_NUMBER = "01118093542"
DB_FILE = "db.json"

def load_db():
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f: return json.load(f)
    except: return {"users": {}, "codes": {}, "pending": {}, "rooms": [], "logs": []}
def save_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f: json.dump(db, f, ensure_ascii=False, indent=2)
def get_user(db, uid, name=""):
    uid = str(uid)
    if uid not in db["users"]:
        db["users"][uid] = {"name": name or "مستخدم", "points": 20, "vip": False, "banned": False, "invited": 0, "state": None, "last_daily": "", "wins": 0, "games": 0, "last_wheel": 0, "last_box": 0, "join": datetime.now().strftime("%Y-%m-%d"), "total_earned": 20, "codes_used": [], "level": 1, "xp": 0}
    return db["users"][uid]
def is_owner(uid): return int(uid) == OWNER_ID

# ===== كل الحساسيات - كل التليفونات =====
SENS = {
 "samsung": {"title": "📱 سامسونج Samsung", "items": {
  "Galaxy A05": "🎯 Galaxy A05\n\nعام: 198\nنقطة حمراء: 194\n2x: 190\n4x: 185\nقناص: 128\nزر اطلاق: 54\nDPI: 690\nجيروسكوب: 188",
  "Galaxy A05s": "🎯 Galaxy A05s\n\nعام: 196\nنقطة حمراء: 192\n2x: 188\n4x: 184\nقناص: 126\nزر اطلاق: 55\nDPI: 680\nجيروسكوب: 186",
  "Galaxy A06": "🎯 Galaxy A06\n\nعام: 199\nنقطة حمراء: 195\n2x: 191\n4x: 186\nقناص: 129\nزر اطلاق: 54\nDPI: 695\nجيروسكوب: 189",
  "Galaxy A12": "🎯 Galaxy A12\n\nعام: 190\nنقطة حمراء: 185\n2x: 180\n4x: 175\nقناص: 120\nزر اطلاق: 55\nDPI: 650\nجيروسكوب: 180",
  "Galaxy A13": "🎯 Galaxy A13\n\nعام: 192\nنقطة حمراء: 188\n2x: 183\n4x: 178\nقناص: 122\nزر اطلاق: 56\nDPI: 660\nجيروسكوب: 182",
  "Galaxy A14": "🎯 Galaxy A14\n\nعام: 194\nنقطة حمراء: 190\n2x: 185\n4x: 180\nقناص: 124\nزر اطلاق: 54\nDPI: 670\nجيروسكوب: 184",
  "Galaxy A15": "🎯 Galaxy A15\n\nعام: 195\nنقطة حمراء: 191\n2x: 186\n4x: 181\nقناص: 125\nزر اطلاق: 53\nDPI: 680\nجيروسكوب: 185",
  "Galaxy A16": "🎯 Galaxy A16\n\nعام: 196\nنقطة حمراء: 192\n2x: 187\n4x: 182\nقناص: 126\nزر اطلاق: 53\nDPI: 685\nجيروسكوب: 186",
  "Galaxy A17": "🎯 Galaxy A17\n\nعام: 197\nنقطة حمراء: 193\n2x: 188\n4x: 183\nقناص: 127\nزر اطلاق: 52\nDPI: 690\nجيروسكوب: 187",
  "Galaxy A22": "🎯 Galaxy A22\n\nعام: 192\nنقطة حمراء: 188\n2x: 184\n4x: 180\nقناص: 120\nزر اطلاق: 56\nDPI: 660\nجيروسكوب: 182",
  "Galaxy A23": "🎯 Galaxy A23\n\nعام: 193\nنقطة حمراء: 189\n2x: 185\n4x: 181\nقناص: 121\nزر اطلاق: 55\nDPI: 665\nجيروسكوب: 183",
  "Galaxy A24": "🎯 Galaxy A24\n\nعام: 194\nنقطة حمراء: 190\n2x: 186\n4x: 182\nقناص: 122\nزر اطلاق: 55\nDPI: 670\nجيروسكوب: 184",
  "Galaxy A25": "🎯 Galaxy A25\n\nعام: 195\nنقطة حمراء: 191\n2x: 187\n4x: 183\nقناص: 123\nزر اطلاق: 54\nDPI: 675\nجيروسكوب: 185",
  "Galaxy A26": "🎯 Galaxy A26\n\nعام: 196\nنقطة حمراء: 192\n2x: 188\n4x: 184\nقناص: 124\nزر اطلاق: 53\nDPI: 680\nجيروسكوب: 186",
  "Galaxy A32": "🎯 Galaxy A32\n\nعام: 198\nنقطة حمراء: 194\n2x: 190\n4x: 185\nقناص: 128\nزر اطلاق: 54\nDPI: 690\nجيروسكوب: 188",
  "Galaxy A33": "🎯 Galaxy A33\n\nعام: 197\nنقطة حمراء: 193\n2x: 189\n4x: 184\nقناص: 127\nزر اطلاق: 53\nDPI: 685\nجيروسكوب: 187",
  "Galaxy A34": "🎯 Galaxy A34\n\nعام: 200\nنقطة حمراء: 195\n2x: 190\n4x: 185\nقناص: 130\nزر اطلاق: 50\nDPI: 700\nجيروسكوب: 190",
  "Galaxy A35": "🎯 Galaxy A35\n\nعام: 201\nنقطة حمراء: 196\n2x: 191\n4x: 186\nقناص: 131\nزر اطلاق: 50\nDPI: 705\nجيروسكوب: 191",
  "Galaxy A52": "🎯 Galaxy A52\n\nعام: 196\nنقطة حمراء: 192\n2x: 188\n4x: 184\nقناص: 126\nزر اطلاق: 52\nDPI: 680\nجيروسكوب: 186",
  "Galaxy A52s": "🎯 Galaxy A52s\n\nعام: 197\nنقطة حمراء: 193\n2x: 189\n4x: 185\nقناص: 127\nزر اطلاق: 52\nDPI: 685\nجيروسكوب: 187",
  "Galaxy A53": "🎯 Galaxy A53\n\nعام: 198\nنقطة حمراء: 194\n2x: 190\n4x: 186\nقناص: 128\nزر اطلاق: 51\nDPI: 690\nجيروسكوب: 188",
  "Galaxy A54": "🎯 Galaxy A54\n\nعام: 200\nنقطة حمراء: 196\n2x: 192\n4x: 188\nقناص: 130\nزر اطلاق: 50\nDPI: 700\nجيروسكوب: 190",
  "Galaxy A55": "🎯 Galaxy A55\n\nعام: 202\nنقطة حمراء: 198\n2x: 194\n4x: 190\nقناص: 132\nزر اطلاق: 49\nDPI: 710\nجيروسكوب: 192",
  "Galaxy A71": "🎯 Galaxy A71\n\nعام: 188\nنقطة حمراء: 184\n2x: 180\n4x: 176\nقناص: 118\nزر اطلاق: 55\nDPI: 640\nجيروسكوب: 178",
  "Galaxy A72": "🎯 Galaxy A72\n\nعام: 189\nنقطة حمراء: 185\n2x: 181\n4x: 177\nقناص: 119\nزر اطلاق: 54\nDPI: 645\nجيروسكوب: 179",
  "Galaxy A73": "🎯 Galaxy A73\n\nعام: 190\nنقطة حمراء: 186\n2x: 182\n4x: 178\nقناص: 120\nزر اطلاق: 53\nDPI: 650\nجيروسكوب: 180",
  "Galaxy S20": "🎯 Galaxy S20\n\nعام: 188\nنقطة حمراء: 184\n2x: 180\n4x: 176\nقناص: 112\nزر اطلاق: 52\nDPI: 640\nجيروسكوب: 178",
  "Galaxy S20 FE": "🎯 Galaxy S20 FE\n\nعام: 189\nنقطة حمراء: 185\n2x: 181\n4x: 177\nقناص: 113\nزر اطلاق: 52\nDPI: 645\nجيروسكوب: 179",
  "Galaxy S21": "🎯 Galaxy S21\n\nعام: 185\nنقطة حمراء: 180\n2x: 175\n4x: 170\nقناص: 110\nزر اطلاق: 52\nDPI: 600\nجيروسكوب: 170",
  "Galaxy S21 FE": "🎯 Galaxy S21 FE\n\nعام: 186\nنقطة حمراء: 181\n2x: 176\n4x: 171\nقناص: 111\nزر اطلاق: 51\nDPI: 610\nجيروسكوب: 171",
  "Galaxy S22": "🎯 Galaxy S22\n\nعام: 184\nنقطة حمراء: 179\n2x: 174\n4x: 169\nقناص: 109\nزر اطلاق: 51\nDPI: 595\nجيروسكوب: 169",
  "Galaxy S22 Ultra": "🎯 Galaxy S22 Ultra\n\nعام: 182\nنقطة حمراء: 177\n2x: 172\n4x: 167\nقناص: 107\nزر اطلاق: 49\nDPI: 585\nجيروسكوب: 167",
  "Galaxy S23": "🎯 Galaxy S23\n\nعام: 184\nنقطة حمراء: 179\n2x: 174\n4x: 169\nقناص: 109\nزر اطلاق: 50\nDPI: 595\nجيروسكوب: 169",
  "Galaxy S23 Ultra": "🎯 Galaxy S23 Ultra 👑\n\nعام: 180\nنقطة حمراء: 175\n2x: 170\n4x: 165\nقناص: 105\nزر اطلاق: 48\nDPI: 580\nجيروسكوب: 165",
  "Galaxy S24": "🎯 Galaxy S24\n\nعام: 183\nنقطة حمراء: 178\n2x: 173\n4x: 168\nقناص: 108\nزر اطلاق: 50\nDPI: 590\nجيروسكوب: 168",
  "Galaxy S24 Ultra": "🎯 Galaxy S24 Ultra 👑\n\nعام: 179\nنقطة حمراء: 174\n2x: 169\n4x: 164\nقناص: 104\nزر اطلاق: 47\nDPI: 575\nجيروسكوب: 164",
  "Galaxy S25": "🎯 Galaxy S25\n\nعام: 182\nنقطة حمراء: 177\n2x: 172\n4x: 167\nقناص: 107\nزر اطلاق: 49\nDPI: 585\nجيروسكوب: 167",
  "Galaxy S25 Ultra": "🎯 Galaxy S25 Ultra 👑🔥\n\nعام: 178\nنقطة حمراء: 173\n2x: 168\n4x: 163\nقناص: 103\nزر اطلاق: 46\nDPI: 570\nجيروسكوب: 163",
  "Galaxy M12": "🎯 Galaxy M12\n\nعام: 194\nنقطة حمراء: 190\n2x: 186\n4x: 182\nقناص: 124\nزر اطلاق: 58\nDPI: 670\nجيروسكوب: 184",
  "Galaxy M13": "🎯 Galaxy M13\n\nعام: 195\nنقطة حمراء: 191\n2x: 187\n4x: 183\nقناص: 125\nزر اطلاق: 57\nDPI: 675\nجيروسكوب: 185",
  "Galaxy M14": "🎯 Galaxy M14\n\nعام: 196\nنقطة حمراء: 192\n2x: 188\n4x: 184\nقناص: 126\nزر اطلاق: 56\nDPI: 680\nجيروسكوب: 186",
  "Galaxy M33": "🎯 Galaxy M33\n\nعام: 192\nنقطة حمراء: 188\n2x: 184\n4x: 180\nقناص: 122\nزر اطلاق: 57\nDPI: 660\nجيروسكوب: 182",
  "Galaxy M34": "🎯 Galaxy M34\n\nعام: 193\nنقطة حمراء: 189\n2x: 185\n4x: 181\nقناص: 123\nزر اطلاق: 56\nDPI: 665\nجيروسكوب: 183",
  "Galaxy M54": "🎯 Galaxy M54\n\nعام: 194\nنقطة حمراء: 190\n2x: 186\n4x: 182\nقناص: 124\nزر اطلاق: 55\nDPI: 670\nجيروسكوب: 184",
  "Galaxy M55": "🎯 Galaxy M55\n\nعام: 195\nنقطة حمراء: 191\n2x: 187\n4x: 183\nقناص: 125\nزر اطلاق: 54\nDPI: 675\nجيروسكوب: 185",
  "Galaxy F15": "🎯 Galaxy F15\n\nعام: 194\nنقطة حمراء: 190\n2x: 186\n4x: 182\nقناص: 124\nزر اطلاق: 56\nDPI: 670\nجيروسكوب: 186",
  "Galaxy F34": "🎯 Galaxy F34\n\nعام: 195\nنقطة حمراء: 191\n2x: 187\n4x: 183\nقناص: 125\nزر اطلاق: 55\nDPI: 675\nجيروسكوب: 187",
  "Galaxy F54": "🎯 Galaxy F54\n\nعام: 196\nنقطة حمراء: 192\n2x: 188\n4x: 184\nقناص: 126\nزر اطلاق: 54\nDPI: 680\nجيروسكوب: 188",
  "Galaxy F55": "🎯 Galaxy F55\n\nعام: 197\nنقطة حمراء: 193\n2x: 189\n4x: 185\nقناص: 127\nزر اطلاق: 53\nDPI: 685\nجيروسكوب: 189",
  "Galaxy Z Flip 5": "🎯 Z Flip 5\n\nعام: 175\nنقطة حمراء: 170\n2x: 165\n4x: 160\nقناص: 110\nزر اطلاق: 48\nDPI: 580\nجيروسكوب: 165",
  "Galaxy Z Flip 6": "🎯 Z Flip 6\n\nعام: 176\nنقطة حمراء: 171\n2x: 166\n4x: 161\nقناص: 111\nزر اطلاق: 47\nDPI: 585\nجيروسكوب: 166",
  "Galaxy Z Fold 5": "🎯 Z Fold 5\n\nعام: 174\nنقطة حمراء: 169\n2x: 164\n4x: 159\nقناص: 109\nزر اطلاق: 47\nDPI: 575\nجيروسكوب: 164",
  "Galaxy Z Fold 6": "🎯 Z Fold 6\n\nعام: 173\nنقطة حمراء: 168\n2x: 163\n4x: 158\nقناص: 108\nزر اطلاق: 46\nDPI: 570\nجيروسكوب: 163",
  "Galaxy Note 20": "🎯 Note 20\n\nعام: 182\nنقطة حمراء: 178\n2x: 174\n4x: 170\nقناص: 108\nزر اطلاق: 50\nDPI: 600\nجيروسكوب: 172",
  "Galaxy Note 20 Ultra": "🎯 Note 20 Ultra\n\nعام: 181\nنقطة حمراء: 176\n2x: 171\n4x: 166\nقناص: 106\nزر اطلاق: 49\nDPI: 590\nجيروسكوب: 170",
 }},
 "xiaomi": {"title": "📱 شاومي Xiaomi", "items": {
  "Redmi 10": "🎯 Redmi 10\n\nعام: 195\nنقطة حمراء: 190\n2x: 185\n4x: 180\nقناص: 125\nزر اطلاق: 58\nDPI: 680\nجيروسكوب: 188",
  "Redmi 12": "🎯 Redmi 12\n\nعام: 196\nنقطة حمراء: 191\n2x: 186\n4x: 181\nقناص: 126\nزر اطلاق: 57\nDPI: 685\nجيروسكوب: 189",
  "Redmi 13": "🎯 Redmi 13\n\nعام: 197\nنقطة حمراء: 192\n2x: 187\n4x: 182\nقناص: 127\nزر اطلاق: 56\nDPI: 690\nجيروسكوب: 190",
  "Redmi 13C": "🎯 Redmi 13C\n\nعام: 200\nنقطة حمراء: 196\n2x: 192\n4x: 188\nقناص: 132\nزر اطلاق: 60\nDPI: 700\nجيروسكوب: 194",
  "Redmi 14C": "🎯 Redmi 14C\n\nعام: 201\nنقطة حمراء: 197\n2x: 193\n4x: 189\nقناص: 133\nزر اطلاق: 59\nDPI: 705\nجيروسكوب: 195",
  "Redmi A3": "🎯 Redmi A3\n\nعام: 202\nنقطة حمراء: 198\n2x: 194\n4x: 190\nقناص: 134\nزر اطلاق: 61\nDPI: 710\nجيروسكوب: 196",
  "Redmi Note 11": "🎯 Redmi Note 11\n\nعام: 190\nنقطة حمراء: 188\n2x: 182\n4x: 178\nقناص: 120\nزر اطلاق: 55\nDPI: 660\nجيروسكوب: 180",
  "Redmi Note 12": "🎯 Redmi Note 12\n\nعام: 191\nنقطة حمراء: 189\n2x: 183\n4x: 179\nقناص: 121\nزر اطلاق: 54\nDPI: 665\nجيروسكوب: 181",
  "Redmi Note 13": "🎯 Redmi Note 13\n\nعام: 192\nنقطة حمراء: 190\n2x: 184\n4x: 180\nقناص: 122\nزر اطلاق: 54\nDPI: 670\nجيروسكوب: 182",
  "Redmi Note 14": "🎯 Redmi Note 14\n\nعام: 193\nنقطة حمراء: 191\n2x: 185\n4x: 181\nقناص: 123\nزر اطلاق: 53\nDPI: 675\nجيروسكوب: 183",
  "Redmi Note 11 Pro": "🎯 Redmi Note 11 Pro\n\nعام: 198\nنقطة حمراء: 195\n2x: 190\n4x: 185\nقناص: 130\nزر اطلاق: 50\nDPI: 700\nجيروسكوب: 192",
  "Redmi Note 12 Pro": "🎯 Redmi Note 12 Pro\n\nعام: 199\nنقطة حمراء: 196\n2x: 191\n4x: 186\nقناص: 131\nزر اطلاق: 50\nDPI: 705\nجيروسكوب: 193",
  "Redmi Note 13 Pro": "🎯 Redmi Note 13 Pro\n\nعام: 200\nنقطة حمراء: 197\n2x: 192\n4x: 187\nقناص: 132\nزر اطلاق: 49\nDPI: 710\nجيروسكوب: 194",
  "Redmi Note 13 Pro+": "🎯 Redmi Note 13 Pro+\n\nعام: 201\nنقطة حمراء: 198\n2x: 193\n4x: 188\nقناص: 133\nزر اطلاق: 48\nDPI: 715\nجيروسكوب: 195",
  "Mi 11": "🎯 Mi 11\n\nعام: 185\nنقطة حمراء: 180\n2x: 175\n4x: 170\nقناص: 112\nزر اطلاق: 50\nDPI: 620\nجيروسكوب: 175",
  "Mi 12": "🎯 Mi 12\n\nعام: 186\nنقطة حمراء: 181\n2x: 176\n4x: 171\nقناص: 113\nزر اطلاق: 50\nDPI: 625\nجيروسكوب: 176",
  "Mi 13": "🎯 Mi 13\n\nعام: 187\nنقطة حمراء: 182\n2x: 177\n4x: 172\nقناص: 114\nزر اطلاق: 49\nDPI: 630\nجيروسكوب: 177",
  "Mi 14": "🎯 Mi 14\n\nعام: 188\nنقطة حمراء: 183\n2x: 178\n4x: 173\nقناص: 115\nزر اطلاق: 49\nDPI: 635\nجيروسكوب: 178",
 }},
 "poco": {"title": "📱 بوكو Poco 🔥", "items": {
  "Poco X3": "🎯 Poco X3\n\nعام: 200\nنقطة حمراء: 200\n2x: 195\n4x: 190\nقناص: 135\nزر اطلاق: 48\nDPI: 720\nجيروسكوب: 195",
  "Poco X3 Pro": "🎯 Poco X3 Pro\n\nعام: 201\nنقطة حمراء: 201\n2x: 196\n4x: 191\nقناص: 136\nزر اطلاق: 47\nDPI: 725\nجيروسكوب: 196",
  "Poco X5": "🎯 Poco X5\n\nعام: 199\nنقطة حمراء: 199\n2x: 194\n4x: 189\nقناص: 134\nزر اطلاق: 48\nDPI: 715\nجيروسكوب: 194",
  "Poco X5 Pro": "🎯 Poco X5 Pro\n\nعام: 200\nنقطة حمراء: 200\n2x: 195\n4x: 190\nقناص: 135\nزر اطلاق: 47\nDPI: 720\nجيروسكوب: 195",
  "Poco X6": "🎯 Poco X6\n\nعام: 201\nنقطة حمراء: 201\n2x: 196\n4x: 191\nقناص: 136\nزر اطلاق: 46\nDPI: 725\nجيروسكوب: 196",
  "Poco X6 Pro": "🎯 Poco X6 Pro 🔥\n\nعام: 203\nنقطة حمراء: 203\n2x: 198\n4x: 193\nقناص: 138\nزر اطلاق: 45\nDPI: 735\nجيروسكوب: 198",
  "Poco X7": "🎯 Poco X7\n\nعام: 202\nنقطة حمراء: 202\n2x: 197\n4x: 192\nقناص: 137\nزر اطلاق: 46\nDPI: 730\nجيروسكوب: 197",
  "Poco F3": "🎯 Poco F3\n\nعام: 196\nنقطة حمراء: 192\n2x: 188\n4x: 184\nقناص: 128\nزر اطلاق: 52\nDPI: 690\nجيروسكوب: 186",
  "Poco F4": "🎯 Poco F4\n\nعام: 197\nنقطة حمراء: 193\n2x: 189\n4x: 185\nقناص: 129\nزر اطلاق: 51\nDPI: 695\nجيروسكوب: 187",
  "Poco F5": "🎯 Poco F5\n\nعام: 198\nنقطة حمراء: 194\n2x: 190\n4x: 186\nقناص: 130\nزر اطلاق: 50\nDPI: 700\nجيروسكوب: 188",
  "Poco F6": "🎯 Poco F6 🔥\n\nعام: 199\nنقطة حمراء: 195\n2x: 191\n4x: 187\nقناص: 131\nزر اطلاق: 49\nDPI: 705\nجيروسكوب: 189",
  "Poco M5": "🎯 Poco M5\n\nعام: 196\nنقطة حمراء: 192\n2x: 188\n4x: 184\nقناص: 128\nزر اطلاق: 52\nDPI: 690\nجيروسكوب: 186",
  "Poco M6": "🎯 Poco M6\n\nعام: 197\nنقطة حمراء: 193\n2x: 189\n4x: 185\nقناص: 129\nزر اطلاق: 51\nDPI: 695\nجيروسكوب: 187",
  "Poco C65": "🎯 Poco C65\n\nعام: 198\nنقطة حمراء: 194\n2x: 190\n4x: 186\nقناص: 130\nزر اطلاق: 53\nDPI: 695\nجيروسكوب: 188",
 }},
 "oppo": {"title": "📱 اوبو Oppo", "items": {
  "Oppo A18": "🎯 Oppo A18\n\nعام: 190\nنقطة حمراء: 186\n2x: 182\n4x: 178\nقناص: 118\nزر اطلاق: 59\nDPI: 640\nجيروسكوب: 182",
  "Oppo A38": "🎯 Oppo A38\n\nعام: 191\nنقطة حمراء: 187\n2x: 183\n4x: 179\nقناص: 119\nزر اطلاق: 58\nDPI: 645\nجيروسكوب: 183",
  "Oppo A53": "🎯 Oppo A53\n\nعام: 185\nنقطة حمراء: 180\n2x: 175\n4x: 170\nقناص: 115\nزر اطلاق: 60\nDPI: 620\nجيروسكوب: 175",
  "Oppo A54": "🎯 Oppo A54\n\nعام: 186\nنقطة حمراء: 181\n2x: 176\n4x: 171\nقناص: 116\nزر اطلاق: 59\nDPI: 625\nجيروسكوب: 176",
  "Oppo A57": "🎯 Oppo A57\n\nعام: 187\nنقطة حمراء: 183\n2x: 179\n4x: 175\nقناص: 117\nزر اطلاق: 58\nDPI: 630\nجيروسكوب: 177",
  "Oppo A58": "🎯 Oppo A58\n\nعام: 188\nنقطة حمراء: 184\n2x: 180\n4x: 176\nقناص: 118\nزر اطلاق: 57\nDPI: 635\nجيروسكوب: 178",
  "Oppo A60": "🎯 Oppo A60\n\nعام: 189\nنقطة حمراء: 185\n2x: 181\n4x: 177\nقناص: 119\nزر اطلاق: 56\nDPI: 640\nجيروسكوب: 179",
  "Oppo A78": "🎯 Oppo A78\n\nعام: 190\nنقطة حمراء: 186\n2x: 182\n4x: 178\nقناص: 120\nزر اطلاق: 55\nDPI: 645\nجيروسكوب: 180",
  "Oppo A79": "🎯 Oppo A79\n\nعام: 191\nنقطة حمراء: 187\n2x: 183\n4x: 179\nقناص: 121\nزر اطلاق: 54\nDPI: 650\nجيروسكوب: 181",
  "Oppo Reno 7": "🎯 Oppo Reno 7\n\nعام: 195\nنقطة حمراء: 192\n2x: 188\n4x: 182\nقناص: 126\nزر اطلاق: 52\nDPI: 680\nجيروسكوب: 188",
  "Oppo Reno 8": "🎯 Oppo Reno 8\n\nعام: 196\nنقطة حمراء: 193\n2x: 189\n4x: 183\nقناص: 127\nزر اطلاق: 51\nDPI: 685\nجيروسكوب: 189",
  "Oppo Reno 11": "🎯 Oppo Reno 11\n\nعام: 197\nنقطة حمراء: 194\n2x: 190\n4x: 184\nقناص: 128\nزر اطلاق: 50\nDPI: 690\nجيروسكوب: 190",
  "Oppo Reno 12": "🎯 Oppo Reno 12\n\nعام: 198\nنقطة حمراء: 195\n2x: 191\n4x: 185\nقناص: 129\nزر اطلاق: 49\nDPI: 695\nجيروسكوب: 191",
 }},
 "realme": {"title": "📱 ريلمي Realme", "items": {
  "Realme C51": "🎯 Realme C51\n\nعام: 192\nنقطة حمراء: 188\n2x: 184\n4x: 178\nقناص: 122\nزر اطلاق: 56\nDPI: 640\nجيروسكوب: 184",
  "Realme C53": "🎯 Realme C53\n\nعام: 193\nنقطة حمراء: 189\n2x: 185\n4x: 179\nقناص: 123\nزر اطلاق: 55\nDPI: 645\nجيروسكوب: 185",
  "Realme C55": "🎯 Realme C55\n\nعام: 194\nنقطة حمراء: 190\n2x: 186\n4x: 180\nقناص: 124\nزر اطلاق: 54\nDPI: 650\nجيروسكوب: 186",
  "Realme C61": "🎯 Realme C61\n\nعام: 194\nنقطة حمراء: 190\n2x: 186\n4x: 182\nقناص: 124\nزر اطلاق: 55\nDPI: 650\nجيروسكوب: 186",
  "Realme C63": "🎯 Realme C63\n\nعام: 195\nنقطة حمراء: 191\n2x: 187\n4x: 183\nقناص: 125\nزر اطلاق: 54\nDPI: 655\nجيروسكوب: 187",
  "Realme C67": "🎯 Realme C67\n\nعام: 196\nنقطة حمراء: 192\n2x: 188\n4x: 184\nقناص: 126\nزر اطلاق: 53\nDPI: 660\nجيروسكوب: 188",
  "Realme Note 50": "🎯 Realme Note 50\n\nعام: 195\nنقطة حمراء: 191\n2x: 187\n4x: 183\nقناص: 125\nزر اطلاق: 55\nDPI: 655\nجيروسكوب: 187",
  "Realme 11": "🎯 Realme 11\n\nعام: 198\nنقطة حمراء: 195\n2x: 190\n4x: 185\nقناص: 130\nزر اطلاق: 50\nDPI: 700\nجيروسكوب: 192",
  "Realme 11 Pro": "🎯 Realme 11 Pro\n\nعام: 199\nنقطة حمراء: 196\n2x: 191\n4x: 186\nقناص: 131\nزر اطلاق: 49\nDPI: 705\nجيروسكوب: 193",
  "Realme 12": "🎯 Realme 12\n\nعام: 199\nنقطة حمراء: 196\n2x: 191\n4x: 186\nقناص: 131\nزر اطلاق: 49\nDPI: 705\nجيروسكوب: 193",
  "Realme 12 Pro": "🎯 Realme 12 Pro\n\nعام: 200\nنقطة حمراء: 197\n2x: 192\n4x: 187\nقناص: 132\nزر اطلاق: 48\nDPI: 710\nجيروسكوب: 194",
  "Realme 13 Pro": "🎯 Realme 13 Pro\n\nعام: 201\nنقطة حمراء: 198\n2x: 193\n4x: 188\nقناص: 133\nزر اطلاق: 48\nDPI: 715\nجيروسكوب: 195",
 }},
 "infinix": {"title": "📱 انفنكس Infinix", "items": {
  "Hot 30": "🎯 Hot 30\n\nعام: 200\nنقطة حمراء: 195\n2x: 190\n4x: 185\nقناص: 132\nزر اطلاق: 60\nDPI: 700\nجيروسكوب: 192",
  "Hot 40": "🎯 Hot 40\n\nعام: 201\nنقطة حمراء: 196\n2x: 191\n4x: 186\nقناص: 133\nزر اطلاق: 59\nDPI: 705\nجيروسكوب: 193",
  "Hot 40 Pro": "🎯 Hot 40 Pro\n\nعام: 202\nنقطة حمراء: 198\n2x: 194\n4x: 190\nقناص: 135\nزر اطلاق: 58\nDPI: 710\nجيروسكوب: 195",
  "Hot 50": "🎯 Hot 50\n\nعام: 202\nنقطة حمراء: 198\n2x: 194\n4x: 190\nقناص: 135\nزر اطلاق: 58\nDPI: 712\nجيروسكوب: 195",
  "Hot 50 Pro": "🎯 Hot 50 Pro\n\nعام: 203\nنقطة حمراء: 199\n2x: 195\n4x: 191\nقناص: 136\nزر اطلاق: 57\nDPI: 715\nجيروسكوب: 196",
  "Note 30": "🎯 Note 30\n\nعام: 195\nنقطة حمراء: 192\n2x: 188\n4x: 180\nقناص: 126\nزر اطلاق: 55\nDPI: 680\nجيروسكوب: 186",
  "Note 40": "🎯 Note 40\n\nعام: 196\nنقطة حمراء: 193\n2x: 189\n4x: 181\nقناص: 127\nزر اطلاق: 54\nDPI: 685\nجيروسكوب: 187",
  "Note 40 Pro": "🎯 Note 40 Pro\n\nعام: 197\nنقطة حمراء: 194\n2x: 190\n4x: 182\nقناص: 128\nزر اطلاق: 53\nDPI: 690\nجيروسكوب: 188",
  "Note 50": "🎯 Note 50\n\nعام: 198\nنقطة حمراء: 195\n2x: 191\n4x: 183\nقناص: 129\nزر اطلاق: 53\nDPI: 695\nجيروسكوب: 189",
  "GT 20 Pro": "🎯 GT 20 Pro 🔥 جيمينج\n\nعام: 205\nنقطة حمراء: 200\n2x: 196\n4x: 192\nقناص: 140\nزر اطلاق: 52\nDPI: 730\nجيروسكوب: 200",
  "Zero 30": "🎯 Zero 30\n\nعام: 199\nنقطة حمراء: 196\n2x: 192\n4x: 188\nقناص: 131\nزر اطلاق: 51\nDPI: 705\nجيروسكوب: 191",
  "Smart 8": "🎯 Smart 8\n\nعام: 203\nنقطة حمراء: 199\n2x: 195\n4x: 191\nقناص: 136\nزر اطلاق: 60\nDPI: 715\nجيروسكوب: 196",
 }},
 "tecno": {"title": "📱 تكنو Tecno", "items": {
  "Spark 10": "🎯 Spark 10\n\nعام: 198\nنقطة حمراء: 194\n2x: 190\n4x: 185\nقناص: 128\nزر اطلاق: 60\nDPI: 690\nجيروسكوب: 190",
  "Spark 20": "🎯 Spark 20\n\nعام: 199\nنقطة حمراء: 195\n2x: 191\n4x: 186\nقناص: 129\nزر اطلاق: 59\nDPI: 695\nجيروسكوب: 191",
  "Spark Go": "🎯 Spark Go\n\nعام: 200\nنقطة حمراء: 196\n2x: 192\n4x: 188\nقناص: 131\nزر اطلاق: 60\nDPI: 700\nجيروسكوب: 192",
  "Camon 20": "🎯 Camon 20\n\nعام: 198\nنقطة حمراء: 194\n2x: 190\n4x: 185\nقناص: 128\nزر اطلاق: 58\nDPI: 690\nجيروسكوب: 190",
  "Camon 30": "🎯 Camon 30\n\nعام: 199\nنقطة حمراء: 195\n2x: 191\n4x: 186\nقناص: 129\nزر اطلاق: 57\nDPI: 695\nجيروسكوب: 191",
  "Pova 5": "🎯 Pova 5\n\nعام: 200\nنقطة حمراء: 196\n2x: 192\n4x: 188\nقناص: 131\nزر اطلاق: 56\nDPI: 700\nجيروسكوب: 192",
  "Pova 6": "🎯 Pova 6 🔥\n\nعام: 201\nنقطة حمراء: 197\n2x: 193\n4x: 189\nقناص: 132\nزر اطلاق: 55\nDPI: 705\nجيروسكوب: 193",
  "Pop 8": "🎯 Pop 8\n\nعام: 202\nنقطة حمراء: 198\n2x: 194\n4x: 190\nقناص: 134\nزر اطلاق: 61\nDPI: 710\nجيروسكوب: 194",
 }},
 "vivo": {"title": "📱 فيفو Vivo", "items": {
  "Vivo Y03": "🎯 Vivo Y03\n\nعام: 194\nنقطة حمراء: 190\n2x: 186\n4x: 182\nقناص: 124\nزر اطلاق: 58\nDPI: 670\nجيروسكوب: 186",
  "Vivo Y17s": "🎯 Vivo Y17s\n\nعام: 193\nنقطة حمراء: 189\n2x: 185\n4x: 181\nقناص: 123\nزر اطلاق: 58\nDPI: 665\nجيروسكوب: 185",
  "Vivo Y27": "🎯 Vivo Y27\n\nعام: 190\nنقطة حمراء: 186\n2x: 182\n4x: 178\nقناص: 120\nزر اطلاق: 55\nDPI: 650\nجيروسكوب: 182",
  "Vivo Y28": "🎯 Vivo Y28\n\nعام: 191\nنقطة حمراء: 187\n2x: 183\n4x: 179\nقناص: 121\nزر اطلاق: 55\nDPI: 655\nجيروسكوب: 183",
  "Vivo V29": "🎯 Vivo V29\n\nعام: 192\nنقطة حمراء: 188\n2x: 184\n4x: 180\nقناص: 122\nزر اطلاق: 54\nDPI: 660\nجيروسكوب: 184",
  "Vivo V30": "🎯 Vivo V30\n\nعام: 193\nنقطة حمراء: 189\n2x: 185\n4x: 181\nقناص: 123\nزر اطلاق: 53\nDPI: 665\nجيروسكوب: 185",
  "Vivo V40": "🎯 Vivo V40\n\nعام: 194\nنقطة حمراء: 190\n2x: 186\n4x: 182\nقناص: 124\nزر اطلاق: 52\nDPI: 670\nجيروسكوب: 186",
 }},
 "huawei": {"title": "📱 هواوي Huawei", "items": {
  "Huawei Nova 11": "🎯 Nova 11\n\nعام: 188\nنقطة حمراء: 184\n2x: 180\n4x: 175\nقناص: 118\nزر اطلاق: 58\nDPI: 630\nجيروسكوب: 180",
  "Huawei Nova 12": "🎯 Nova 12\n\nعام: 189\nنقطة حمراء: 185\n2x: 181\n4x: 176\nقناص: 119\nزر اطلاق: 57\nDPI: 635\nجيروسكوب: 181",
  "Huawei Y9": "🎯 Huawei Y9\n\nعام: 187\nنقطة حمراء: 183\n2x: 179\n4x: 174\nقناص: 117\nزر اطلاق: 59\nDPI: 625\nجيروسكوب: 179",
  "Huawei Y90": "🎯 Huawei Y90\n\nعام: 188\nنقطة حمراء: 184\n2x: 180\n4x: 175\nقناص: 118\nزر اطلاق: 58\nDPI: 630\nجيروسكوب: 180",
 }},
 "honor": {"title": "📱 هونر Honor", "items": {
  "Honor X6": "🎯 Honor X6\n\nعام: 192\nنقطة حمراء: 188\n2x: 184\n4x: 180\nقناص: 122\nزر اطلاق: 54\nDPI: 660\nجيروسكوب: 184",
  "Honor X8": "🎯 Honor X8\n\nعام: 193\nنقطة حمراء: 189\n2x: 185\n4x: 181\nقناص: 123\nزر اطلاق: 53\nDPI: 665\nجيروسكوب: 185",
  "Honor X9": "🎯 Honor X9\n\nعام: 194\nنقطة حمراء: 190\n2x: 186\n4x: 182\nقناص: 124\nزر اطلاق: 52\nDPI: 670\nجيروسكوب: 186",
  "Honor 90": "🎯 Honor 90\n\nعام: 195\nنقطة حمراء: 191\n2x: 187\n4x: 183\nقناص: 125\nزر اطلاق: 51\nDPI: 675\nجيروسكوب: 187",
  "Honor 200": "🎯 Honor 200\n\nعام: 196\nنقطة حمراء: 192\n2x: 188\n4x: 184\nقناص: 126\nزر اطلاق: 50\nDPI: 680\nجيروسكوب: 188",
 }},
 "iphone": {"title": "📱 ايفون iPhone", "items": {
  "iPhone 11": "🎯 iPhone 11\n\nعام: 175\nنقطة حمراء: 170\n2x: 165\n4x: 160\nقناص: 100\nزر اطلاق: 48\nجيروسكوب: 165",
  "iPhone 12": "🎯 iPhone 12\n\nعام: 176\nنقطة حمراء: 171\n2x: 166\n4x: 161\nقناص: 101\nزر اطلاق: 48\nجيروسكوب: 166",
  "iPhone 13": "🎯 iPhone 13\n\nعام: 177\nنقطة حمراء: 172\n2x: 167\n4x: 162\nقناص: 102\nزر اطلاق: 48\nجيروسكوب: 167",
  "iPhone 14": "🎯 iPhone 14\n\nعام: 180\nنقطة حمراء: 175\n2x: 170\n4x: 165\nقناص: 105\nزر اطلاق: 50\nجيروسكوب: 170",
  "iPhone 15": "🎯 iPhone 15\n\nعام: 181\nنقطة حمراء: 176\n2x: 171\n4x: 166\nقناص: 106\nزر اطلاق: 50\nجيروسكوب: 171",
  "iPhone 16": "🎯 iPhone 16\n\nعام: 182\nنقطة حمراء: 177\n2x: 172\n4x: 167\nقناص: 107\nزر اطلاق: 49\nDPI: 580\nجيروسكوب: 172",
  "iPhone 13 Pro Max": "🎯 13 Pro Max 👑\n\nعام: 178\nنقطة حمراء: 172\n2x: 168\n4x: 162\nقناص: 102\nزر اطلاق: 46\nجيروسكوب: 168",
  "iPhone 14 Pro Max": "🎯 14 Pro Max 👑\n\nعام: 178\nنقطة حمراء: 172\n2x: 168\n4x: 162\nقناص: 102\nزر اطلاق: 46\nجيروسكوب: 168",
  "iPhone 15 Pro Max": "🎯 15 Pro Max 👑🔥\n\nعام: 177\nنقطة حمراء: 171\n2x: 167\n4x: 161\nقناص: 101\nزر اطلاق: 45\nجيروسكوب: 167",
  "iPhone 16 Pro Max": "🎯 16 Pro Max 👑🔥\n\nعام: 176\nنقطة حمراء: 170\n2x: 166\n4x: 160\nقناص: 100\nزر اطلاق: 45\nجيروسكوب: 166",
  "iPad": "🎯 iPad\n\nعام: 160\nنقطة حمراء: 155\n2x: 150\n4x: 145\nقناص: 95\nزر اطلاق: 45\nجيروسكوب: 150\n💡 العب 4 صوابع",
  "iPad Pro": "🎯 iPad Pro\n\nعام: 158\nنقطة حمراء: 153\n2x: 148\n4x: 143\nقناص: 93\nزر اطلاق: 44\nجيروسكوب: 148",
 }},
 "other": {"title": "📱 باقي الماركات", "items": {
  "OnePlus 11": "🎯 OnePlus 11\n\nعام: 182\nنقطة حمراء: 178\n2x: 174\n4x: 168\nقناص: 110\nزر اطلاق: 48\nDPI: 600\nجيروسكوب: 170",
  "OnePlus 12": "🎯 OnePlus 12\n\nعام: 183\nنقطة حمراء: 179\n2x: 175\n4x: 169\nقناص: 111\nزر اطلاق: 47\nDPI: 605\nجيروسكوب: 171",
  "Google Pixel 7": "🎯 Pixel 7\n\nعام: 180\nنقطة حمراء: 176\n2x: 172\n4x: 168\nقناص: 108\nزر اطلاق: 50\nDPI: 620\nجيروسكوب: 172",
  "Google Pixel 8": "🎯 Pixel 8\n\nعام: 181\nنقطة حمراء: 177\n2x: 173\n4x: 169\nقناص: 109\nزر اطلاق: 49\nDPI: 625\nجيروسكوب: 173",
  "Google Pixel 9": "🎯 Pixel 9\n\nعام: 182\nنقطة حمراء: 178\n2x: 174\n4x: 170\nقناص: 110\nزر اطلاق: 48\nDPI: 630\nجيروسكوب: 174",
  "Nokia G22": "🎯 Nokia G22\n\nعام: 190\nنقطة حمراء: 186\n2x: 182\n4x: 178\nقناص: 120\nزر اطلاق: 58\nDPI: 650\nجيروسكوب: 182",
  "Itel S23": "🎯 Itel S23\n\nعام: 193\nنقطة حمراء: 189\n2x: 185\n4x: 181\nقناص: 124\nزر اطلاق: 61\nDPI: 650\nجيروسكوب: 186",
  "Itel P55": "🎯 Itel P55\n\nعام: 194\nنقطة حمراء: 190\n2x: 186\n4x: 182\nقناص: 125\nزر اطلاق: 60\nDPI: 655\nجيروسكوب: 187",
  "Itel A70": "🎯 Itel A70\n\nعام: 195\nنقطة حمراء: 191\n2x: 187\n4x: 183\nقناص: 126\nزر اطلاق: 60\nDPI: 660\nجيروسكوب: 188",
  "Samsung Tab A": "🎯 Samsung Tab\n\nعام: 165\nنقطة حمراء: 160\n2x: 155\n4x: 150\nقناص: 98\nزر اطلاق: 48\nDPI: 550\nجيروسكوب: 155",
  "Xiaomi Pad": "🎯 Xiaomi Pad\n\nعام: 166\nنقطة حمراء: 161\n2x: 156\n4x: 151\nقناص: 99\nزر اطلاق: 47\nDPI: 555\nجيروسكوب: 156",
  "Lenovo Tab": "🎯 Lenovo Tab\n\nعام: 167\nنقطة حمراء: 162\n2x: 157\n4x: 152\nقناص: 100\nزر اطلاق: 48\nDPI: 560\nجيروسكوب: 157",
  "تليفوني ضعيف / قديم": "🎯 تليفون ضعيف - حساسية تقيلة\n\nعام: 210\nنقطة حمراء: 205\n2x: 200\n4x: 195\nقناص: 145\nزر اطلاق: 65\nDPI: 750\nجيروسكوب: 205\n💡 اقفل الجرافيك على Smooth و Low",
  "تليفوني قوي / فلاجشيب": "🎯 تليفون قوي - حساسية هادية\n\nعام: 175\nنقطة حمراء: 170\n2x: 165\n4x: 160\nقناص: 105\nزر اطلاق: 48\nDPI: 580\nجيروسكوب: 165",
 }},
}
# ===== PART 2 - الباقات والمتجر والالعاب =====

PACKAGES = {
 "p1": {"label": "💎 100 نقطة - 20ج", "points": 100, "price": 20, "vip": False},
 "p2": {"label": "💎 300 نقطة - 50ج", "points": 300, "price": 50, "vip": False},
 "p3": {"label": "💎 700 نقطة - 100ج", "points": 700, "price": 100, "vip": False},
 "p4": {"label": "💎 1500 نقطة - 180ج", "points": 1500, "price": 180, "vip": False},
 "p5": {"label": "💎 3000 نقطة - 300ج", "points": 3000, "price": 300, "vip": False},
 "p6": {"label": "👑 VIP اسبوع - 50ج", "points": 0, "price": 50, "vip": True},
 "p7": {"label": "👑 VIP شهر - 100ج", "points": 0, "price": 100, "vip": True},
 "p8": {"label": "👑 VIP + 500 نقطة - 150ج", "points": 500, "price": 150, "vip": True},
 "p9": {"label": "👑 VIP دائم + 1000 نقطة - 250ج", "points": 1000, "price": 250, "vip": True},
 "p10": {"label": "👑 VIP دائم + 3000 نقطة - 500ج", "points": 3000, "price": 500, "vip": True},
}

SHOP = {
 "s1": {"label": "🎯 حساسية مخصوصة ليك - 50 نقطة", "cost": 50},
 "s2": {"label": "🎡 لفة عجلة زيادة - 20 نقطة", "cost": 20},
 "s3": {"label": "🎁 صندوق زيادة - 30 نقطة", "cost": 30},
 "s4": {"label": "👑 ترقية VIP اسبوع - 200 نقطة", "cost": 200},
 "s5": {"label": "🎲 محاولة لعبة زيادة - 10 نقطة", "cost": 10},
 "s6": {"label": "🔥 حساسية احترافية من عدي - 100 نقطة", "cost": 100},
 "s7": {"label": "🏆 دخول بطولة - 150 نقطة", "cost": 150},
 "s8": {"label": "💬 سؤال لعدي خاص - 30 نقطة", "cost": 30},
}

# هدايا ونصايح عشوائية
TIPS = [
 "💡 نصيحة عدي: العب جيروسكوب، هيفرق معاك 180 درجة",
 "💡 نصيحة عدي: متعليش الحساسية اوي، الثبات اهم من السرعة",
 "💡 نصيحة عدي: اتدرب 10 دقايق في التدريب قبل كل روم",
 "💡 نصيحة عدي: زر الاطلاق خليه 50-55، ده احسن حاجة",
 "💡 نصيحة عدي: لو تليفونك بيسخن، قلل الجرافيك على Smooth",
 "💡 نصيحة عدي: العب 4 صوابع لو تليفونك شاشته كبيرة",
 "💡 نصيحة عدي: الـ DPI العالي = ايم اسرع بس اقل ثبات",
 "💡 نصيحة عدي: جرب حساسية عدي المخصوصة من المتجر",
]

DAILY_REWARDS = [25, 30, 40, 50, 100]

def main_kb(uid):
    db = load_db(); u = get_user(db, uid)
    kb = [
        [InlineKeyboardButton("🎯 حساسيات التليفونات - 180 موديل", callback_data="sens")],
        [InlineKeyboardButton(f"👤 حسابي | 💎 {u['points']} نقطة | {'👑 VIP' if u['vip'] else 'عادي'} | Lv {u.get('level',1)}", callback_data="profile")],
        [InlineKeyboardButton("🎡 عجلة الحظ", callback_data="wheel"), InlineKeyboardButton("🎁 صندوق", callback_data="box")],
        [InlineKeyboardButton("🎲 لعبة حظ", callback_data="game"), InlineKeyboardButton("🎁 هدية يومية", callback_data="daily")],
        [InlineKeyboardButton("🎰 سلوت", callback_data="slot"), InlineKeyboardButton("🪙 طرة ولا كتابة", callback_data="coin")],
        [InlineKeyboardButton("✂️ حجرة ورقة مقص", callback_data="rps"), InlineKeyboardButton("💡 نصيحة عدي", callback_data="tip")],
        [InlineKeyboardButton("🏆 المتصدرين", callback_data="top"), InlineKeyboardButton("🛒 المتجر", callback_data="shop")],
        [InlineKeyboardButton("💳 شحن - فودافون كاش", callback_data="charge")],
        [InlineKeyboardButton("🎁 دعوة صحابك +10", callback_data="invite"), InlineKeyboardButton("🔑 استبدال كود", callback_data="redeem_info")],
        [InlineKeyboardButton("🏟️ رومات وبطولات", callback_data="rooms"), InlineKeyboardButton("💬 كلم عدي", callback_data="support")],
    ]
    if is_owner(uid):
        kb.append([InlineKeyboardButton("👑 لوحة الاونر عدي - كل الصلاحيات", callback_data="admin")])
    return InlineKeyboardMarkup(kb)

def back_kb(): return InlineKeyboardMarkup([[InlineKeyboardButton("🏠 القايمة الرئيسية", callback_data="home")]])

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
    await update.message.reply_text(f"👑 اهلا يا {user.first_name} في بوت عدي WAR 🔥\n\n💎 نقطك: {u['points']} | {'👑 VIP' if u['vip'] else 'عضو عادي'} | ليفل {u.get('level',1)}\n\n🎯 180+ موديل تليفون بحساسيته\n🎡 عجلة حظ + صندوق + سلوت + العاب\n💳 شحن فودافون كاش بصورة تحويل\n🔑 اكواد بتدي نقط بجد\n🏆 بطولات ورومات\n💡 نصايح عدي الاحترافية\n\nاختار من تحت 👇", reply_markup=main_kb(user.id))

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
        await q.edit_message_text("📱 اختار نوع تليفونك - عندنا كل الماركات:", reply_markup=InlineKeyboardMarkup(kb)); return
    if data.startswith("brand_"):
        b = data.replace("brand_", ""); kb = [[InlineKeyboardButton(n, callback_data=f"phone_{b}_{i}")] for i,n in enumerate(SENS[b]["items"])]
        kb.append([InlineKeyboardButton("⬅️ رجوع", callback_data="sens")])
        await q.edit_message_text(f"{SENS[b]['title']}\n\nاختار موديلك بالظبط - {len(SENS[b]['items'])} موديل:", reply_markup=InlineKeyboardMarkup(kb)); return
    if data.startswith("phone_"):
        _, b, idx = data.split("_"); name = list(SENS[b]["items"].keys())[int(idx)]; txt = SENS[b]["items"][name]
        await q.edit_message_text(txt + f"\n\n📱 موديلك: {name}\n👑 من عدي WAR", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📤 شير لصحابك", callback_data="invite")],[InlineKeyboardButton("🎯 حساسية تانية", callback_data="sens")],[InlineKeyboardButton("🏠 رجوع", callback_data="home")]])); return
    if data == "profile":
        await q.edit_message_text(f"👤 حسابك يا {u['name']}\n\n🆔 ID: {uid}\n💎 النقط: {u['points']}\n👑 VIP: {'✅ نعم' if u['vip'] else '❌ لا'}\n⭐ ليفل: {u.get('level',1)} | XP: {u.get('xp',0)}\n🎁 دعيت: {u['invited']} واحد\n🎮 لعبت: {u['games']} مرة | كسبت: {u['wins']} مرة\n📅 دخلت: {u.get('join','')}\n💰 اجمالي اللي كسبته: {u.get('total_earned',0)} نقطة", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💳 شحن", callback_data="charge")],[InlineKeyboardButton("🏠 رجوع", callback_data="home")]])); return
    if data == "wheel":
        now = time.time()
        if now - u.get("last_wheel", 0) < 60 and not is_owner(uid):
            await q.edit_message_text(f"⏳ استنى {int(60-(now-u['last_wheel']))} ثانية ولف تاني!", reply_markup=back_kb()); return
        win = random.choice([5,5,10,10,15,20,25,0,0,50,100]); u["points"] += win; u["last_wheel"] = now; u["xp"] = u.get("xp",0)+5; save_db(db)
        msg = f"🎡 عجلة الحظ...\n\n🎉 كسبت {win} نقطة!\n💎 رصيدك: {u['points']}" if win>0 else f"😅 المرة دي مجاش حاجة\n💎 رصيدك: {u['points']}"
        await q.edit_message_text(msg, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎡 لف تاني", callback_data="wheel")],[InlineKeyboardButton("🏠 رجوع", callback_data="home")]])); return
    if data == "box":
        now = time.time()
        if now - u.get("last_box", 0) < 60 and not is_owner(uid):
            await q.edit_message_text("⏳ استنى دقيقة وافتح صندوق تاني!", reply_markup=back_kb()); return
        win = random.choice([10,20,30,50,100,200]); u["points"] += win; u["last_box"] = now; save_db(db)
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
    if data == "slot":
        symbols = ["🍒","🍋","🔔","💎","⭐","7️⃣"]
        a,b,c = random.choice(symbols), random.choice(symbols), random.choice(symbols)
        if a==b==c:
            win = 100 if a=="💎" else 50; u["points"] += win; save_db(db)
            await q.edit_message_text(f"🎰 {a} | {b} | {c}\n\n🎉 جاكبوت! كسبت {win} نقطة!\nرصيدك: {u['points']}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎰 العب تاني", callback_data="slot")],[InlineKeyboardButton("🏠 رجوع", callback_data="home")]]))
        elif a==b or b==c or a==c:
            u["points"] += 10; save_db(db)
            await q.edit_message_text(f"🎰 {a} | {b} | {c}\n\n😊 اتنين شبه بعض! كسبت 10 نقط\nرصيدك: {u['points']}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎰 العب تاني", callback_data="slot")],[InlineKeyboardButton("🏠 رجوع", callback_data="home")]]))
        else:
            u["points"] = max(0, u["points"]-5); save_db(db)
            await q.edit_message_text(f"🎰 {a} | {b} | {c}\n\n😅 مفيش حاجة، خسرت 5\nرصيدك: {u['points']}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎰 حاول تاني", callback_data="slot")],[InlineKeyboardButton("🏠 رجوع", callback_data="home")]]))
        return
    if data == "coin":
        kb = [[InlineKeyboardButton("👑 ملك - طرة", callback_data="coin_head"), InlineKeyboardButton("🪙 كتابة", callback_data="coin_tail")],[InlineKeyboardButton("🏠 رجوع", callback_data="home")]]
        await q.edit_message_text("🪙 طرة ولا كتابة؟\n\nلو صح تكسب 20 نقطة، لو غلط تخسر 5 بس.", reply_markup=InlineKeyboardMarkup(kb)); return
    if data.startswith("coin_"):
        pick = data.replace("coin_",""); real = random.choice(["head","tail"]); u["games"] += 1
        if pick == real:
            u["points"] += 20; u["wins"] += 1; save_db(db)
            await q.edit_message_text(f"🎉 صح! طلعت {'طرة' if real=='head' else 'كتابة'}\nكسبت +20\nرصيدك: {u['points']}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🪙 العب تاني", callback_data="coin")],[InlineKeyboardButton("🏠 رجوع", callback_data="home")]]))
        else:
            u["points"] = max(0, u["points"]-5); save_db(db)
            await q.edit_message_text(f"😅 غلط! طلعت {'طرة' if real=='head' else 'كتابة'}\nخسرت 5\nرصيدك: {u['points']}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🪙 حاول تاني", callback_data="coin")],[InlineKeyboardButton("🏠 رجوع", callback_data="home")]]))
        return
    if data == "rps":
        kb = [[InlineKeyboardButton("✂️ مقص", callback_data="rps_scissors"), InlineKeyboardButton("🪨 حجرة", callback_data="rps_rock"), InlineKeyboardButton("📄 ورقة", callback_data="rps_paper")],[InlineKeyboardButton("🏠 رجوع", callback_data="home")]]
        await q.edit_message_text("✂️ حجرة ورقة مقص ضد البوت!\n\nلو كسبت تاخد 20 نقطة", reply_markup=InlineKeyboardMarkup(kb)); return
    if data.startswith("rps_"):
        pick = data.replace("rps_",""); bot_pick = random.choice(["rock","paper","scissors"]); names = {"rock":"🪨 حجرة","paper":"📄 ورقة","scissors":"✂️ مقص"}
        win_map = {"rock":"scissors","paper":"rock","scissors":"paper"}
        if pick == bot_pick:
            await q.edit_message_text(f"🤝 تعادل! انت {names[pick]} والبوت {names[bot_pick]}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✂️ العب تاني", callback_data="rps")],[InlineKeyboardButton("🏠 رجوع", callback_data="home")]]))
        elif win_map[pick]==bot_pick:
            u["points"] += 20; u["wins"] += 1; u["games"] += 1; save_db(db)
            await q.edit_message_text(f"🎉 كسبت! انت {names[pick]} والبوت {names[bot_pick]}\n+20 نقطة | رصيدك: {u['points']}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✂️ العب تاني", callback_data="rps")],[InlineKeyboardButton("🏠 رجوع", callback_data="home")]]))
        else:
            u["points"] = max(0, u["points"]-5); u["games"] += 1; save_db(db)
            await q.edit_message_text(f"😅 خسرت! انت {names[pick]} والبوت {names[bot_pick]}\n-5 نقط | رصيدك: {u['points']}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✂️ حاول تاني", callback_data="rps")],[InlineKeyboardButton("🏠 رجوع", callback_data="home")]]))
        return
    if data == "tip":
        tip = random.choice(TIPS)
        await q.edit_message_text(f"{tip}\n\n👑 من عدي WAR", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💡 نصيحة تانية", callback_data="tip")],[InlineKeyboardButton("🏠 رجوع", callback_data="home")]])); return
    if data == "daily":
        today = datetime.now().strftime("%Y-%m-%d")
        if u.get("last_daily") == today:
            await q.edit_message_text("🎁 خدت هديتك النهاردة خلاص! تعالى بكرة.", reply_markup=back_kb()); return
        reward = random.choice(DAILY_REWARDS); u["last_daily"] = today; u["points"] += reward; save_db(db)
        await q.edit_message_text(f"🎁 هدية يومية!\n\nخدت +{reward} نقطة\nرصيدك: {u['points']}", reply_markup=back_kb()); return
    if data == "top":
        users = sorted(db["users"].values(), key=lambda x: x["points"], reverse=True)[:15]
        txt = "🏆 المتصدرين - اعلى نقط:\n\n"
        for i, x in enumerate(users, 1): txt += f"{i}. {x['name']} - {x['points']} نقطة {'👑' if x['vip'] else ''} Lv {x.get('level',1)}\n"
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
        if k == "s4": u["vip"] = True
        if k == "s2": u["last_wheel"] = 0
        if k == "s3": u["last_box"] = 0
        save_db(db)
        await q.edit_message_text(f"✅ اشتريت: {item['label']}\nرصيدك دلوقتي: {u['points']}", reply_markup=back_kb())
        if k in ["s1","s6","s8"]:
            try: await context.bot.send_message(OWNER_ID, f"🛒 حد اشترى من المتجر!\nمن: {u['name']} - ID: {uid}\nاشترى: {item['label']}")
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
    if data.startswith("approve_") and is_owner(uid):
        _, target, pk = data.split("_"); target = int(target); p = PACKAGES[pk]
        tu = get_user(db, target); tu["points"] += p["points"]
        if p.get("vip"): tu["vip"] = True
        tu["state"] = None; db["pending"].pop(str(target), None); save_db(db)
        await q.edit_message_text(f"✅ تم القبول - {p['label']} وصلت لـ {target}")
        try: await context.bot.send_message(target, f"✅ عدي قبل التحويل بتاعك! 🎉\n\nوصلك: {p['label']}\n💎 رصيدك: {tu['points']} نقطة\n👑 VIP: {'✅' if tu['vip'] else '❌'}")
        except: pass
        return
    if data.startswith("reject_") and is_owner(uid):
        _, target, pk = data.split("_"); target = int(target)
        tu = get_user(db, target); tu["state"] = None; db["pending"].pop(str(target), None); save_db(db)
        await q.edit_message_text(f"❌ تم الرفض لـ {target}")
        try: await context.bot.send_message(target, "❌ عدي رفض التحويل بتاعك.\nلو حولت بجد كلم عدي وابعتله الصورة تاني.")
        except: pass
        return
    if data == "admin" and is_owner(uid):
        total = len(db["users"]); pend = len(db["pending"]); vip_count = sum(1 for x in db["users"].values() if x["vip"])
        await q.edit_message_text(f"👑 لوحة عدي - الجزء 3 فيه باقي الاوامر\n\n👥 المستخدمين: {total}\n👑 VIP: {vip_count}\n⏳ طلبات شحن معلقة: {pend}\n🔑 اكواد: {len(db['codes'])}\n\nاستنى الجزء 3 عشان باقي الاوامر", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 رجوع", callback_data="home")]])); return
        # ===== PART 3 - رسايل + اوامر الاونر + التشغيل =====

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = load_db(); uid = update.effective_user.id; u = get_user(db, uid, update.effective_user.first_name)
    if u["banned"]: return
    # صورة تحويل فودافون كاش
    if update.message.photo and u.get("state","").startswith("wait_receipt_"):
        pk = u["state"].replace("wait_receipt_", ""); p = PACKAGES[pk]
        photo_id = update.message.photo[-1].file_id
        db["pending"][str(uid)] = {"pkg": pk, "photo": photo_id}; save_db(db)
        await update.message.reply_text("✅ وصلت الصورة! مستني عدي يراجعها.\nهيجيلك رسالة اول ما يقبل او يرفض.")
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("✅ قبول", callback_data=f"approve_{uid}_{pk}"), InlineKeyboardButton("❌ رفض", callback_data=f"reject_{uid}_{pk}")]])
        try: await context.bot.send_photo(OWNER_ID, photo_id, caption=f"💳 طلب شحن جديد!\n\nمن: {u['name']} - ID: {uid}\nالباقة: {p['label']}\nالسعر: {p['price']}ج\nحول على: {VODAFONE_NUMBER}", reply_markup=kb)
        except: pass
        return
    # استبدال كود
    if update.message.text and u.get("state") == "wait_code":
        code = update.message.text.strip().upper()
        if code in db["codes"] and not db["codes"][code].get("used"):
            c = db["codes"][code]
            if c.get("vip"): u["vip"] = True
            u["points"] += c["points"]; c["used"] = True; c["used_by"] = uid; u["state"] = None; u["codes_used"].append(code); save_db(db)
            await update.message.reply_text(f"✅ الكود صح! 🎉\nخدت +{c['points']} نقطة\n👑 VIP: {'✅' if u['vip'] else '❌'}\nرصيدك: {u['points']}", reply_markup=main_kb(uid))
            try: await context.bot.send_message(OWNER_ID, f"🔑 حد استخدم كود!\nمن: {u['name']} - ID: {uid}\nالكود: {code} - {c['points']} نقطة")
            except: pass
        else:
            await update.message.reply_text("❌ الكود غلط او مستخدم قبل كده")
        return
    # رسالة دعم لعدي
    if update.message.text and u.get("state") == "wait_support":
        u["state"] = None; save_db(db)
        await update.message.reply_text("✅ رسالتك وصلت لعدي، هيرد عليك قريب.")
        try: await context.bot.send_message(OWNER_ID, f"💬 رسالة جديدة من {u['name']} - ID: {uid}\n\n{update.message.text}\n\nللرد: /reply {uid} رسالتك")
        except: pass
        return
    if update.message.text and not update.message.text.startswith("/"):
        await update.message.reply_text("استخدم الزراير من /start 👇", reply_markup=main_kb(uid))

# ===== اوامر الاونر عدي - كل الصلاحيات =====
async def owner_only(update):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("🚫 ده للاونر عدي بس! 👑"); return False
    return True

async def makecode(update, context):
    if not await owner_only(update): return
    if len(context.args) < 2:
        await update.message.reply_text("اكتب: /makecode WAR100 50\nاو: /makecode VIP50 0 VIP"); return
    db = load_db(); is_vip = len(context.args) >= 3 and context.args[2].upper() == "VIP"
    db["codes"][context.args[0].upper()] = {"points": int(context.args[1]), "used": False, "vip": is_vip, "used_by": None}; save_db(db)
    await update.message.reply_text(f"✅ عملت كود {context.args[0].upper()} بـ {context.args[1]} نقطة {'+ VIP 👑' if is_vip else ''}")

async def makecodes(update, context):
    # تعمل 10 اكواد مرة واحدة: /makecodes WAR 50 10
    if not await owner_only(update): return
    if len(context.args) < 3:
        await update.message.reply_text("اكتب: /makecodes WAR 50 10\nهيعمل 10 اكواد WAR1 لحد WAR10"); return
    db = load_db(); base = context.args[0].upper(); pts = int(context.args[1]); count = int(context.args[2])
    for i in range(1, count+1):
        db["codes"][f"{base}{i}"] = {"points": pts, "used": False, "vip": False, "used_by": None}
    save_db(db)
    await update.message.reply_text(f"✅ عملت {count} كود من {base}1 لحد {base}{count} - كل واحد {pts} نقطة")

async def listcodes(update, context):
    if not await owner_only(update): return
    db = load_db()
    if not db["codes"]: await update.message.reply_text("مفيش اكواد"); return
    txt = "🔑 الاكواد:\n\n"
    for k,v in db["codes"].items(): txt += f"{k} - {v['points']} نقطة {'+VIP' if v.get('vip') else ''} - {'✅ مستخدم by '+str(v.get('used_by')) if v['used'] else '⏳ شغال'}\n"
    await update.message.reply_text(txt)

async def delcode(update, context):
    if not await owner_only(update): return
    db = load_db(); db["codes"].pop(context.args[0].upper(), None); save_db(db); await update.message.reply_text("✅ اتمسح")

async def clearcodes(update, context):
    if not await owner_only(update): return
    db = load_db(); db["codes"] = {}; save_db(db); await update.message.reply_text("✅ اتمسحت كل الاكواد")

async def ban(update, context):
    if not await owner_only(update): return
    db = load_db(); t = get_user(db, int(context.args[0])); t["banned"] = True; save_db(db); await update.message.reply_text("🚫 اتحظر")
    try: await context.bot.send_message(int(context.args[0]), "🚫 عدي حظرك من البوت.")
    except: pass

async def unban(update, context):
    if not await owner_only(update): return
    db = load_db(); t = get_user(db, int(context.args[0])); t["banned"] = False; save_db(db); await update.message.reply_text("✅ اتفك حظره")
    try: await context.bot.send_message(int(context.args[0]), "✅ عدي فك حظرك، تقدر ترجع تلعب 👑")
    except: pass

async def addpoints(update, context):
    if not await owner_only(update): return
    db = load_db(); t = get_user(db, int(context.args[0])); t["points"] += int(context.args[1]); t["total_earned"] += int(context.args[1]); save_db(db); await update.message.reply_text(f"✅ بقى معاه {t['points']} نقطة")
    try: await context.bot.send_message(int(context.args[0]), f"🎉 عدي زودلك +{context.args[1]} نقطة!\nرصيدك: {t['points']}")
    except: pass

async def removepoints(update, context):
    if not await owner_only(update): return
    db = load_db(); t = get_user(db, int(context.args[0])); t["points"] = max(0, t["points"] - int(context.args[1])); save_db(db); await update.message.reply_text(f"✅ بقى معاه {t['points']}")

async def setpoints(update, context):
    if not await owner_only(update): return
    db = load_db(); t = get_user(db, int(context.args[0])); t["points"] = int(context.args[1]); save_db(db); await update.message.reply_text(f"✅ بقى معاه {t['points']} بالظبط")

async def makevip(update, context):
    if not await owner_only(update): return
    db = load_db(); t = get_user(db, int(context.args[0])); t["vip"] = True; save_db(db); await update.message.reply_text("👑 بقى VIP")
    try: await context.bot.send_message(int(context.args[0]), "👑 عدي خلاك VIP! مبروك 🎉")
    except: pass

async def remvip(update, context):
    if not await owner_only(update): return
    db = load_db(); t = get_user(db, int(context.args[0])); t["vip"] = False; save_db(db); await update.message.reply_text("❌ اتشال VIP")

async def resetuser(update, context):
    if not await owner_only(update): return
    db = load_db(); t = get_user(db, int(context.args[0])); t["points"] = 20; t["vip"] = False; t["wins"] = 0; t["games"] = 0; t["invited"] = 0; save_db(db); await update.message.reply_text("✅ اتصفر حسابه")

async def deluser(update, context):
    if not await owner_only(update): return
    db = load_db(); db["users"].pop(str(context.args[0]), None); save_db(db); await update.message.reply_text("✅ اتحذف نهائيا")

async def addroom(update, context):
    if not await owner_only(update): return
    db = load_db(); db["rooms"].append(" ".join(context.args)); save_db(db); await update.message.reply_text("✅ اتضاف الروم")
    # اعلن للكل
    for uid in list(db["users"].keys()):
        try: await context.bot.send_message(int(uid), f"🏟️ روم جديد من عدي!\n\n{' '.join(context.args)}")
        except: pass

async def clearrooms(update, context):
    if not await owner_only(update): return
    db = load_db(); db["rooms"] = []; save_db(db); await update.message.reply_text("✅ اتمسحت الرومات")

async def broadcast(update, context):
    if not await owner_only(update): return
    db = load_db(); msg = " ".join(context.args); c = 0
    for uid in list(db["users"].keys()):
        try: await context.bot.send_message(int(uid), f"📢 من عدي:\n\n{msg}"); c += 1
        except: pass
    await update.message.reply_text(f"✅ اتبعتت لـ {c} واحد")

async def vipbroadcast(update, context):
    if not await owner_only(update): return
    db = load_db(); msg = " ".join(context.args); c = 0
    for uid, u in list(db["users"].items()):
        if u.get("vip"):
            try: await context.bot.send_message(int(uid), f"👑 رسالة VIP من عدي:\n\n{msg}"); c += 1
            except: pass
    await update.message.reply_text(f"✅ اتبعتت لـ {c} VIP")

async def reply_cmd(update, context):
    if not await owner_only(update): return
    try: await context.bot.send_message(int(context.args[0]), f"💬 رد من عدي:\n\n{' '.join(context.args[1:])}"); await update.message.reply_text("✅ اتبعت")
    except: await update.message.reply_text("❌ مش عارف ابعتله")

async def stats_cmd(update, context):
    if not await owner_only(update): return
    db = load_db(); total = len(db["users"]); vip_c = sum(1 for x in db["users"].values() if x["vip"]); banned_c = sum(1 for x in db["users"].values() if x["banned"]); total_points = sum(x["points"] for x in db["users"].values())
    today = datetime.now().strftime("%Y-%m-%d"); today_users = sum(1 for x in db["users"].values() if x.get("join") == today)
    await update.message.reply_text(f"📊 احصائيات عدي 👑\n\n👥 الكل: {total}\n🆕 النهاردة: {today_users}\n👑 VIP: {vip_c}\n🚫 محظور: {banned_c}\n💎 مجموع النقط: {total_points}\n🔑 اكواد: {len(db['codes'])}\n⏳ شحن معلق: {len(db['pending'])}\n🏟️ رومات: {len(db['rooms'])}\n📋 سجلات: {len(db['logs'])}")

async def users_cmd(update, context):
    if not await owner_only(update): return
    db = load_db(); items = list(db["users"].items())[-20:]
    txt = "👥 اخر 20 يوزر:\n\n"
    for uid, u in items: txt += f"{u['name']} - ID: {uid} - {u['points']} نقطة {'👑' if u['vip'] else ''} {'🚫' if u['banned'] else ''}\n"
    await update.message.reply_text(txt)

async def search_cmd(update, context):
    if not await owner_only(update): return
    db = load_db(); q = " ".join(context.args).lower(); found = []
    for uid, u in db["users"].items():
        if q in u["name"].lower() or q == uid: found.append((uid, u))
    if not found: await update.message.reply_text("❌ ملقيتش حد"); return
    txt = "🔍 النتايج:\n\n"
    for uid, u in found: txt += f"{u['name']} - ID: {uid} - {u['points']} نقطة - VIP: {'✅' if u['vip'] else '❌'} - محظور: {'✅' if u['banned'] else '❌'} - دعا: {u['invited']} - لعب: {u['games']}\n"
    await update.message.reply_text(txt)

async def info_cmd(update, context):
    if not await owner_only(update): return
    db = load_db(); uid = str(context.args[0]); u = db["users"].get(uid)
    if not u: await update.message.reply_text("❌ مش موجود"); return
    await update.message.reply_text(f"👤 معلومات كاملة:\n\nالاسم: {u['name']}\nID: {uid}\nنقط: {u['points']}\nVIP: {'✅' if u['vip'] else '❌'}\nمحظور: {'✅' if u['banned'] else '❌'}\nدعا: {u['invited']}\nلعب: {u['games']} | كسب: {u['wins']}\nدخل: {u.get('join','')}\nاجمالي كسبه: {u.get('total_earned',0)}\nاكواد استخدمها: {', '.join(u.get('codes_used',[])) or 'مفيش'}")

async def giveall(update, context):
    if not await owner_only(update): return
    db = load_db(); amount = int(context.args[0]); c = 0
    for uid, u in db["users"].items():
        u["points"] += amount; c += 1
    save_db(db); await update.message.reply_text(f"✅ اديت {amount} نقطة لـ {c} واحد")
    for uid in list(db["users"].keys()):
        try: await context.bot.send_message(int(uid), f"🎉 عدي ادى للكل +{amount} نقطة!\nرصيدك: {db['users'][str(uid)]['points']}")
        except: pass

async def admin_help(update, context):
    if not await owner_only(update): return
    await update.message.reply_text("👑 اوامر الاونر عدي - كلها:\n\n🔑 اكواد:\n/makecode WAR100 50\n/makecodes WAR 50 10\n/listcodes\n/delcode WAR100\n/clearcodes\n\n👤 يوزرز:\n/ban 123\n/unban 123\n/addpoints 123 100\n/removepoints 123 50\n/setpoints 123 500\n/makevip 123\n/remvip 123\n/resetuser 123\n/deluser 123\n/info 123\n/search اسم\n/users\n/stats\n/giveall 50\n\n🏟️ رومات:\n/addroom اسم | ID | باس\n/clearrooms\n\n📢 بث:\n/broadcast رسالة\n/vipbroadcast رسالة\n/reply 123 رسالة")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("makecode", makecode))
    app.add_handler(CommandHandler("makecodes", makecodes))
    app.add_handler(CommandHandler("listcodes", listcodes))
    app.add_handler(CommandHandler("delcode", delcode))
    app.add_handler(CommandHandler("clearcodes", clearcodes))
    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("unban", unban))
    app.add_handler(CommandHandler("addpoints", addpoints))
    app.add_handler(CommandHandler("removepoints", removepoints))
    app.add_handler(CommandHandler("setpoints", setpoints))
    app.add_handler(CommandHandler("makevip", makevip))
    app.add_handler(CommandHandler("remvip", remvip))
    app.add_handler(CommandHandler("resetuser", resetuser))
    app.add_handler(CommandHandler("deluser", deluser))
    app.add_handler(CommandHandler("addroom", addroom))
    app.add_handler(CommandHandler("clearrooms", clearrooms))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("vipbroadcast", vipbroadcast))
    app.add_handler(CommandHandler("reply", reply_cmd))
    app.add_handler(CommandHandler("stats", stats_cmd))
    app.add_handler(CommandHandler("users", users_cmd))
    app.add_handler(CommandHandler("search", search_cmd))
    app.add_handler(CommandHandler("info", info_cmd))
    app.add_handler(CommandHandler("giveall", giveall))
    app.add_handler(CommandHandler("admin", admin_help))
    app.add_handler(CallbackQueryHandler(callbacks))
    app.add_handler(MessageHandler(filters.PHOTO | (filters.TEXT & ~filters.COMMAND), handle_msg))
    print("Bot Running - WAR by Ady - Owner 8188263997 - ALL PHONES")
    app.run_polling()

if __name__ == "__main__": main()
