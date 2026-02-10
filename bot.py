import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ChatJoinRequestHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")

VIDEO_FILE_ID = "BAACAgUAAxkBAAMGaYsBMV20nnbb4rsaPbLn1MRIHCsAApcrAALyjiBVj1XTQUYPxK86BA"

CHANNELS = {
    -1003708594569: "https://t.me/+_YmoMrDZ0oliMTll",
    -1003797237946: "https://t.me/+-s8gGlM-BcY1NDll",
    -1003585811000: "https://t.me/+az-lgmrUAnU1MzQ1",
    -1003737422554: "https://t.me/+Ltw6NlDYtaQ5OWE1",
}

user_requests = {}
video_sent = set()

# ========== START ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔥 Mujhe Exclusive Video Chahiye", callback_data="want_video")]
    ]
    await update.message.reply_text(
        "😈 *Kya tumhe meri exclusive video chahiye?*",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# ========== WANT VIDEO ==========
async def want_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    buttons = []
    for link in CHANNELS.values():
        buttons.append([InlineKeyboardButton("📢 Join Channel", url=link)])

    buttons.append([InlineKeyboardButton("✅ Check Status", callback_data="check_status")])

    await query.message.reply_text(
        "🔥 *Steps follow karo:*\n\n"
        "1️⃣ Sabhi channels me join request bhejo\n"
        "2️⃣ Phir yaha aakar *Check Status* dabao",
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="Markdown"
    )

# ========== JOIN REQUEST TRACK ==========
async def join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    req = update.chat_join_request
    user_id = req.from_user.id
    channel_id = req.chat.id

    if channel_id in CHANNELS:
        user_requests.setdefault(user_id, set()).add(channel_id)

# ========== CHECK STATUS ==========
async def check_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    joined = user_requests.get(user_id, set())

    if joined == set(CHANNELS.keys()):
        if user_id not in video_sent:
            await query.message.reply_video(
                video=VIDEO_FILE_ID,
                caption="✅ *Sabhi channels me request bhej di gayi hai*\n🔥 Ye rahi tumhari exclusive video",
                parse_mode="Markdown"
            )
            video_sent.add(user_id)
        else:
            await query.message.reply_text("🎥 Video already bhej di gayi hai.")
    else:
        await query.message.reply_text(
            "⚠️ Abhi sabhi channels me request nahi bheji.\n\n👉 Pehle sab channels join karo."
        )

# ========== MAIN ==========
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(want_video, pattern="want_video"))
    app.add_handler(CallbackQueryHandler(check_status, pattern="check_status"))
    app.add_handler(ChatJoinRequestHandler(join_request))

    print("Bot running...")
    app.run_polling(close_loop=False)

if __name__ == "__main__":
    main()


