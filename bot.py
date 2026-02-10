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
    ChatJoinRequestHandler,
    ContextTypes,
)

# ================= CONFIG =================
TOKEN = os.getenv("BOT_TOKEN")

VIDEO_FILE_ID = "BAACAgUAAxkBAAMGaYsBMV20nnbb4rsaPbLn1MRIHCsAApcrAALyjiBVj1XTQUYPxK86BA"

# CHANNEL_ID : INVITE_LINK
CHANNELS = {
    -1003708594569: "https://t.me/+_YmoMrDZ0oliMTll",
    -1003797237946: "https://t.me/+-s8gGlM-BcY1NDll",
    -1003585811000: "https://t.me/+az-lgmrUAnU1MzQ1",
    -1003737422554: "https://t.me/+Ltw6NlDYtaQ5OWE1",
}

# user_id -> set(channel_ids)
user_requests = {}
video_sent = set()

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔥 Mujhe Exclusive Video Chahiye", callback_data="want_video")]
    ]

    await update.message.reply_text(
        "😈 *Kya tumhe meri exclusive video chahiye?*",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# ============== BUTTON CLICK ==============
async def want_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    buttons = [
        [InlineKeyboardButton("📢 Join Channel", url=link)]
        for link in CHANNELS.values()
    ]

    await query.message.reply_text(
        "🔥 *Meri video paane ke liye*\n\n"
        "👇 Niche diye gaye *sabhi channels* me join request bhejo.\n"
        "⚠️ Jab sabme request jayegi tabhi video milegi.",
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="Markdown"
    )

# ========== JOIN REQUEST HANDLER ==========
async def join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    req = update.chat_join_request
    user_id = req.from_user.id
    channel_id = req.chat.id

    # sirf apne channels check karo
    if channel_id not in CHANNELS:
        return

    # track request (approve BOT NAHI KAREGA)
    user_requests.setdefault(user_id, set()).add(channel_id)

    # agar sab channels me request aa gayi
    if user_requests[user_id] == set(CHANNELS.keys()):
        if user_id not in video_sent:
            try:
                await context.bot.send_video(
                    chat_id=user_id,
                    video=VIDEO_FILE_ID,
                    caption="✅ *Sabhi channels me request bhej di gayi hai*\n\n🔥 Ye rahi tumhari exclusive video",
                    parse_mode="Markdown"
                )
                video_sent.add(user_id)
            except:
                # user ne /start nahi kiya hoga
                pass

# ================= MAIN =================
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(want_video, pattern="want_video"))
    app.add_handler(ChatJoinRequestHandler(join_request))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()

