from telegram import Update
from telegram.ext import ContextTypes


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحباً! أنا بوت تحليل البيانات\n\n"
        "ابعتلي ملف CSV أو Excel وهحلله ليك وأبعتلك داشبورد تفاعلي كامل\n\n"
        "جرب دلوقتي — ابعت الملف!"
    )
