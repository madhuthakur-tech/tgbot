from telegram.ext import MessageHandler, filters

async def get_video_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video = update.message.video
    if video:
        await update.message.reply_text(f"VIDEO FILE ID:\n{video.file_id}")

app.add_handler(MessageHandler(filters.VIDEO, get_video_id))
