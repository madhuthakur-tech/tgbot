import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ====== ENV VARIABLES ======
BOT_TOKEN = os.getenv("BOT_TOKEN")
VIDEO_ID = os.getenv("VIDEO_ID")

logging.basicConfig(level=logging.INFO)


# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Join Channel ✅", callback_data="check")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Button ko 2 baar click karo 😉",
        reply_markup=reply_markup
    )


# Button handler (2nd click logic)
async def check_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    # agar first time click
    if context.user_data.get("clicked") is None:
        context.user_data["clicked"] = 1
        await query.message.reply_text("Ek baar aur click karo 👇")
    else:
        # second click pe video send
        await query.message.reply_video(video=VIDEO_ID)


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_click, pattern="check"))

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()


