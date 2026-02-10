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

# STEP 1
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [[InlineKeyboardButton("🔥 Mujhe Exclusive Video Chahiye", callback_data="step2")]]
    await update.message.reply_text(
        "😈 *Exclusive video unlock karni hai?*",
        reply_markup=InlineKeyboardMarkup(kb),
        parse_mode="Markdown"
    )

# STEP 2 – JOIN CHANNELS
async def step2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    buttons = [[InlineKeyboardButton("📢 Join Channel", url=link)] for link in CHANNELS.values()]
    buttons.append([InlineKeyboardButton("✅ Check Status", callback_data="step3")])

    await q.message.reply_text(
        "📌 *STEP 2*\n\n"
        "👇 Sabhi channels me join request bhejo\n"
        "Uske baad *Check Status* dabao",
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="Markdown"
    )

# TRACK JOIN REQUESTS
async def join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.chat_join_request.from_user.id
    cid = update.chat_join_request.chat.id
    if cid in CHANNELS:
        user_requests.setdefault(uid, set()).add(cid)

# STEP 3 – ERROR + RETRY
async def step3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    kb = [[InlineKeyboardButton("🔁 Dobara Request Bhejo", callback_data="step4")]]

    await q.message.reply_text(
        "❌ *ERROR AAYA*\n\n"
        "⚠️ Lagta hai sab channels me request nahi gayi\n"
        "🔁 Firse sab channels me join request bhejo",
        reply_markup=InlineKeyboardMarkup(kb),
        parse_mode="Markdown"
    )

# STEP 4 – CONFIRM
async def step4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    kb = [[InlineKeyboardButton("✅ Haan, Ab Bhej Di", callback_data="step5")]]

    await q.message.reply_text(
        "📌 *CONFIRMATION*\n\n"
        "Agar tumne ab *sab channels* me request bhej di hai\n"
        "to niche confirm karo 👇",
        reply_markup=InlineKeyboardMarkup(kb),
        parse_mode="Markdown"
    )

# STEP 5 – FINAL CHECK
async def step5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    uid = q.from_user.id
    joined = user_requests.get(uid, set())

    if joined == set(CHANNELS.keys()):
        if uid not in video_sent:
            await q.message.reply_video(
                video=VIDEO_FILE_ID,
                caption="✅ *ACCESS GRANTED*\n🔥 Ye rahi tumhari exclusive video",
                parse_mode="Markdown"
            )
            video_sent.add(uid)
    else:
        await q.message.reply_text(
            "❌ *Abhi bhi pending hai*\n\n"
            "👉 Sabhi channels me request nahi gayi.\n"
            "🔁 Firse request bhejo aur phir check karo."
        )

# MAIN
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(step2, pattern="step2"))
    app.add_handler(CallbackQueryHandler(step3, pattern="step3"))
    app.add_handler(CallbackQueryHandler(step4, pattern="step4"))
    app.add_handler(CallbackQueryHandler(step5, pattern="step5"))
    app.add_handler(ChatJoinRequestHandler(join_request))

    print("Bot running...")
    app.run_polling(close_loop=False)

if __name__ == "__main__":
    main()
