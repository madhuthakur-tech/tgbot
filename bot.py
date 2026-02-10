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
    keyboard = [
        [InlineKeyboardButton("🔥 Mujhe Exclusive Video Chahiye", callback_data="want")]
    ]
    await update.message.reply_text(
        "😈 *Exclusive video chahiye?*",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# ============ WANT VIDEO ============
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

    try:
        member_ok = []
        for cid in CHANNELS:
            member = await context.bot.get_chat_member(cid, q.from_user.id)
            if member.status in ("member", "administrator", "creator"):
                member_ok.append(cid)

        if len(member_ok) == len(CHANNELS):
            keyboard = [
                [InlineKeyboardButton("✅ HAAN, AB BHEJ DI", callback_data="confirm")]
            ]
            await q.message.reply_text(
                "✅ *Lagta hai sabhi requests bhej di hai*\n\n"
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

    except:
        await q.message.reply_text(
            "⚠️ Error aa raha hai\n\n"
            "👉 Fir se request bhejo aur dobara check karo"
        )

# ============ CONFIRM ============
async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer("Sending video...")

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
    app.add_handler(CallbackQueryHandler(want, lambda q: q.data == "want"))
    app.add_handler(CallbackQueryHandler(check, lambda q: q.data == "check"))
    app.add_handler(CallbackQueryHandler(confirm, lambda q: q.data == "confirm"))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
