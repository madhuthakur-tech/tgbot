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

TOKEN = os.getenv("BOT_TOKEN")

VIDEO_FILE_ID = "BAACAgUAAxkBAAMGaYsBMV20nnbb4rsaPbLn1MRIHCsAApcrAALyjiBVj1XTQUYPxK86BA"

START_PHOTO = "https://i.imgur.com/xxxxxxx.jpg"  # apni photo link daalna

CHANNELS = {
    -1003708594569: "https://t.me/+link1",
    -1003797237946: "https://t.me/+link2",
    -1003585811000: "https://t.me/+link3",
    -1003737422554: "https://t.me/+link4",
}

# user_id -> set(channel_ids)
user_requests = {}
video_sent = set()

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton("🔥 Mujhe Exclusive Video Chahiye", callback_data="want_video")
    ]]
    await update.message.reply_photo(
        photo=START_PHOTO,
        caption="😈 Kya tumhe meri *exclusive video* chahiye?",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# ============== BUTTON CLICK ==============
async def want_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    buttons = []
    for link in CHANNELS.values():
        buttons.append([InlineKeyboardButton("📢 Join Channel", url=link)])

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

    if channel_id not in CHANNELS:
        return

    # approve request
    await context.bot.approve_chat_join_request(channel_id, user_id)

    # track user
    user_requests.setdefault(user_id, set()).add(channel_id)

    # check all channels done
    if user_requests[user_id] == set(CHANNELS.keys()):
        if user_id not in video_sent:
            await context.bot.send_video(
                chat_id=user_id,
                video=VIDEO_FILE_ID,
                caption="✅ *Sabhi channels join ho gaye*\n\n🔥 Ye rahi tumhari exclusive video",
                parse_mode="Markdown"
            )
            video_sent.add(user_id)
    else:
        await context.bot.send_message(
            chat_id=user_id,
            text="⚠️ Abhi sabhi channels join nahi hue.\n\n👉 Saare channels join karo tabhi video milegi."
        )

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

