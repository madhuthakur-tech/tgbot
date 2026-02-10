import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ============ CONFIG ============
TOKEN = os.getenv("BOT_TOKEN")

VIDEO_FILE_ID = "BAACAgUAAxkBAAMGaYsBMV20nnbb4rsaPbLn1MRIHCsAApcrAALyjiBVj1XTQUYPxK86BA"

CHANNELS = {
    -1003708594569: "https://t.me/+_YmoMrDZ0oliMTll",
    -1003797237946: "https://t.me/+-s8gGlM-BcY1NDll",
    -1003585811000: "https://t.me/+az-lgmrUAnU1MzQ1",
    -1003737422554: "https://t.me/+Ltw6NlDYtaQ5OWE1",
}

# ============ START ============
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton("🔥 Mujhe Exclusive Video Chahiye", callback_data="want")
    ]]
    await update.message.reply_text(
        "😈 *Exclusive video chahiye?*",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# ============ WANT ============
async def want(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    buttons = [
        [InlineKeyboardButton("📢 Join Channel", url=link)]
        for link in CHANNELS.values()
    ]
    buttons.append([InlineKeyboardButton("✅ Check Status", callback_data="check")])

    await q.message.reply_text(
        "👇 *Sabhi channels me join request bhejo*\n\n"
        "Phir **Check Status** dabao",
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="Markdown"
    )

# ============ CHECK STATUS ============
async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    joined = 0
    for cid in CHANNELS:
        try:
            m = await context.bot.get_chat_member(cid, q.from_user.id)
            if m.status in ("member", "administrator", "creator"):
                joined += 1
        except:
            pass

    if joined == len(CHANNELS):
        keyboard = [[
            InlineKeyboardButton("✅ HAAN, AB BHEJ DI", callback_data="confirm")
        ]]
        await q.message.reply_text(
            "✅ *Sabhi channels confirmed*\n\n"
            "Confirm karo 👇",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
    else:
        buttons = [
            [InlineKeyboardButton("📢 Join Channel", url=link)]
            for link in CHANNELS.values()
        ]
        buttons.append([InlineKeyboardButton("🔄 Dobara Check Status", callback_data="check")])

        await q.message.reply_text(
            "❌ *Abhi sabhi channels join nahi hue*\n\n"
            "👉 Fir se request bhejo",
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode="Markdown"
        )

# ============ CONFIRM ============
async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer("Video bhej raha hoon...")

    await context.bot.send_video(
        chat_id=q.message.chat_id,
        video=VIDEO_FILE_ID,
        caption="🔥 *Ye rahi tumhari exclusive video*",
        parse_mode="Markdown"
    )

# ============ MAIN ============
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(want, pattern="^want$"))
    app.add_handler(CallbackQueryHandler(check, pattern="^check$"))
    app.add_handler(CallbackQueryHandler(confirm, pattern="^confirm$"))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
