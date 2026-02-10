import os
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ================= CONFIG =================
TOKEN = os.getenv("BOT_TOKEN")

VIDEO_FILE_ID = "BAACAgUAAxkBAAMGaYsBMV20nnbb4rsaPbLn1MRIHCsAApcrAALyjiBVj1XTQUYPxK86BA"

CHANNEL_LINKS = [
    "https://t.me/+_YmoMrDZ0oliMTll",
    "https://t.me/+-s8gGlM-BcY1NDll",
    "https://t.me/+az-lgmrUAnU1MzQ1",
    "https://t.me/+Ltw6NlDYtaQ5OWE1",
]

sent_video = set()

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔥 Mujhe Exclusive Video Chahiye", callback_data="want")]
    ]

    await update.message.reply_text(
        "😈 *Kya tumhe meri exclusive video chahiye?*",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# ============== STEP 2 ==================
async def want(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    buttons = [[InlineKeyboardButton("📢 Join Channel", url=link)] for link in CHANNEL_LINKS]
    buttons.append([InlineKeyboardButton("✅ Check Status", callback_data="check")])

    await q.message.reply_text(
        "🔥 *Meri video paane ke liye*\n\n"
        "👇 Sabhi channels me join request bhejo\n"
        "Uske baad *Check Status* dabao",
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="Markdown"
    )

# ============== STEP 4 (ERROR + REJOIN) ==================
async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    buttons = [[InlineKeyboardButton("📢 Join Channel", url=link)] for link in CHANNEL_LINKS]
    buttons.append([InlineKeyboardButton("✅ Haan, Ab Bhej Di", callback_data="confirm")])

    await q.message.reply_text(
        "❌ *ERROR AAYA*\n\n"
        "Sabhi channels me request confirm nahi hui.\n"
        "👇 Firse sab channels me join request bhejo\n"
        "Aur phir confirm karo 👇",
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="Markdown"
    )

# ============== STEP 5 (FINAL VIDEO) ==================
async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    uid = q.from_user.id
    if uid in sent_video:
        return

    await q.message.reply_video(
        video=VIDEO_FILE_ID,
        caption="✅ *Access Granted*\n\n🔥 Ye rahi tumhari exclusive video",
        parse_mode="Markdown"
    )

    sent_video.add(uid)

# ================= MAIN =================
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(want, pattern="want"))
    app.add_handler(CallbackQueryHandler(check, pattern="check"))
    app.add_handler(CallbackQueryHandler(confirm, pattern="confirm"))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
