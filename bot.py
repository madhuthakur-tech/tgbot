from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

async def get_video_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.video:
        await update.message.reply_text(
            f"VIDEO FILE ID:\n{update.message.video.file_id}"
        )

app.add_handler(MessageHandler(filters.VIDEO, get_video_id))

