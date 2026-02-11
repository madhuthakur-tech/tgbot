import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "YOUR_BOT_TOKEN"

VIDEO_FILE_ID = "BAACAgUAAxkBAAMGaYsBMV20nnbb4rsaPbLn1MRIHCsAApcrAALyjiBVj1XTQUYPxK86BA"

CHANNEL_LINKS = [
    "https://t.me/+_YmoMrDZ0oliMTll",
    "https://t.me/+-s8gGlM-BcY1NDll",
    "https://t.me/+az-lgmrUAnU1MzQ1",
    "https://t.me/+Ltw6NlDYtaQ5OWE1"
]

logging.basicConfig(level=logging.INFO)


# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("📢 Join Channel", url=link)] for link in CHANNEL_LINKS]

    keyboard.append([InlineKeyboardButton("✅ Check Status", callback_data="check")])

    await update.message.reply_text(
        "⚠️ Sabhi channels join karo.\n\nPhir 'Check Status' dabao.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# FIRST CHECK (NO VIDEO)
async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [[InlineKeyboardButton("📢 Join Channel", url=link)] for link in CHANNEL_LINKS]

    keyboard.append([InlineKeyboardButton("✅ Ab Bhej Di", callback_data="confirm")])

    await query.message.reply_text(
        "❌ Request confirm nahi hui.\n\n👉 Fir se request bhejo.\n\nBhej diya ho to niche button dabao.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# SECOND CONFIRM (SEND VIDEO)
async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.message.reply_video(
        video=VIDEO_FILE_ID,
        caption="🔥 Ye lo tumhara video 😎"
    )


# MAIN
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check, pattern="check"))
    app.add_handler(CallbackQueryHandler(confirm, pattern="confirm"))

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
