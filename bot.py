import logging
import os
import sqlite3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")

VIDEO_FILE_ID = "BAACAgUAAxkBAAOzaYwpGyevVBtmm5eDkC65_Ek_luQAAn4mAAKqQWFULEPwzMO6CCI6BA"

CHANNEL_LINKS = [
    "https://t.me/+_YmoMrDZ0oliMTll",
    "https://t.me/+-s8gGlM-BcY1NDll",
    "https://t.me/+az-lgmrUAnU1MzQ1",
    "https://t.me/+Ltw6NlDYtaQ5OWE1"
]

ADMIN_ID = 8566595573  # 🔴 Apni ID

logging.basicConfig(level=logging.INFO)

# ---------------- DATABASE ----------------
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)")
conn.commit()

# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()

    keyboard = [[InlineKeyboardButton("📢 Join Channel", url=link)] for link in CHANNEL_LINKS]
    keyboard.append([InlineKeyboardButton("✅ Check Status", callback_data="check")])

    await update.message.reply_text(
        "Kya tumhe meri exclusive video chahiye? 😘\n⚠️ Sabhi channels join karo.\n\nPhir 'Check Status' dabao.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ---------------- FIRST CHECK ----------------
async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [[InlineKeyboardButton("📢 Join Channel", url=link)] for link in CHANNEL_LINKS]
    keyboard.append([InlineKeyboardButton("✅ ha Bhej Di", callback_data="confirm")])

    await query.message.reply_text(
        "❌ Request confirm nahi hui.\n\n👉 Fir se request bhejo.\n\nBhej di.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ---------------- SECOND CLICK SEND VIDEO ----------------
async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.message.reply_video(
        video=VIDEO_FILE_ID,
        caption="🔥 Ye lo tumhara video 😎\nAur esi hi mast mast leak video buy krne ke liye dm kro @sexy_ladki_001"
    )

# ---------------- BROADCAST ----------------
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()

    sent = 0

    if update.message.reply_to_message:
        msg = update.message.reply_to_message

        for user in users:
            try:
                if msg.photo:
                    await context.bot.send_photo(
                        chat_id=user[0],
                        photo=msg.photo[-1].file_id,
                        caption=msg.caption
                    )
                elif msg.video:
                    await context.bot.send_video(
                        chat_id=user[0],
                        video=msg.video.file_id,
                        caption=msg.caption
                    )
                sent += 1
            except:
                pass
    else:
        message = " ".join(context.args)

        if not message:
            await update.message.reply_text("Reply to photo/video OR use:\n/broadcast your message")
            return

        for user in users:
            try:
                await context.bot.send_message(chat_id=user[0], text=message)
                sent += 1
            except:
                pass

    await update.message.reply_text(f"✅ Broadcast sent to {sent} users")

# ---------------- MAIN (WEBHOOK VERSION) ----------------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CallbackQueryHandler(check, pattern="check"))
    app.add_handler(CallbackQueryHandler(confirm, pattern="confirm"))

    PORT = int(os.environ.get("PORT", 8000))
    RAILWAY_URL = os.environ.get("https://worker-production-44acf.up.railway.app/")

    print("Bot running on webhook...")

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"https://{RAILWAY_URL}/",
    )

if __name__ == "__main__":
    main()

