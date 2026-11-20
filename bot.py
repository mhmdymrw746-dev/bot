import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎬 تحميل HD 🔥", callback_data="hd")],
        [InlineKeyboardButton("✨ بدون علامة مائية", callback_data="no_wm")],
        [InlineKeyboardButton("⚡ تحميل سريع", callback_data="fast")],
        [InlineKeyboardButton("👑 تواصل مع عدي", url="https://t.me/TRAN_5")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👑 أهلا بيك يا وحش في بوت عدي 🔥\n\n"
        "📥 ابعت لينك تيك توك وأنا أحملهولك\n"
        "🎬 جودة عالية HD\n"
        "✨ بدون علامة مائية\n"
        "⚡ تحميل سريع\n\n"
        "👇 ابعت اللينك دلوقتي",
        reply_markup=main_menu()
    )

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if "tiktok" not in url:
        await update.message.reply_text("❌ ابعت لينك تيك توك بس يا وحش")
        return

    context.user_data["last_url"] = url
    await update.message.reply_text(
        "🔥 تمام، لقيت اللينك\nاختار عايز تحمله ازاي 👇",
        reply_markup=main_menu()
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    url = context.user_data.get("last_url")

    if not url:
        await q.message.reply_text("❌ ابعت اللينك الأول يا وحش")
        return

    await q.message.reply_text("⏳ بحملك الفيديو بجودة عالية... استنى ثواني 🔥")

    try:
        r = requests.get(f"https://www.tikwm.com/api/?url={url}&hd=1", timeout=40).json()
        data = r.get("data", {})

        # أعلى جودة ممكنة HD أولا
        video_url = data.get("hdplay") or data.get("play") or data.get("wmplay")
        title = data.get("title", "فيديو تيك توك")
        author = data.get("author", {}).get("nickname", "TikTok")
        duration = data.get("duration", 0)

        if not video_url:
            await q.message.reply_text(
                "❌ اللينك ده محمي أو الفيديو خاص\n"
                "جرب فيديو عام تاني يكون صاحبه سامح بالتحميل"
            )
            return

        await q.message.reply_video(
            video=video_url,
            caption=f"🔥 {title}\n\n👤 بواسطة: {author}\n⏱ المدة: {duration} ثانية\n🎬 جودة: HD عالية\n\n👑 بوت عدي | @TRAN_5",
            reply_markup=main_menu()
        )

    except Exception as e:
        await q.message.reply_text("❌ حصل خطأ، جرب لينك تاني يا وحش")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    app.run_polling()
