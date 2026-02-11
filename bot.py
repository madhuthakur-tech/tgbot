import os
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")  # Railway/Render me env variable me token daalo

async def get_video_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video = update.message.video

    file_id = video.file_id
    file_unique_id = video.file_unique_id

    await update.message.reply_text(
        f"🎥 Video File ID:\n\n{file_id}\n\n"
        f"🔹 Unique ID:\n{file_unique_id}"
    )

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.VIDEO, get_video_id))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()

