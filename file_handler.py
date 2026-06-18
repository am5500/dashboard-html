import os
import pandas as pd
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

ALLOWED_EXTENSIONS = [".csv", ".xlsx", ".xls"]
DOWNLOADS_DIR = "downloads"
os.makedirs(DOWNLOADS_DIR, exist_ok=True)


async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document
    file_name = doc.file_name or "file"
    ext = os.path.splitext(file_name)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        await update.message.reply_text(
            "الملف ده مش مدعوم\n"
            "ابعتلي ملف CSV أو Excel فقط (.csv / .xlsx / .xls)"
        )
        return

    await update.message.reply_text("جاري تحميل الملف...")

    file = await context.bot.get_file(doc.file_id)
    local_path = os.path.join(DOWNLOADS_DIR, f"{update.effective_user.id}_{file_name}")
    await file.download_to_drive(local_path)

    try:
        if ext == ".csv":
            df = pd.read_csv(local_path)
        else:
            df = pd.read_excel(local_path)
    except Exception as e:
        await update.message.reply_text(f"في مشكلة في قراءة الملف: {e}")
        return

    rows, cols = df.shape
    col_names = ", ".join(df.columns.tolist()[:8])
    if len(df.columns) > 8:
        col_names += f" ... وأكثر"

    context.user_data["file_path"] = local_path
    context.user_data["file_name"] = file_name
    context.user_data["rows"] = rows
    context.user_data["cols"] = cols

    keyboard = [
        [
            InlineKeyboardButton("تلقائي - حلل كل حاجة", callback_data="mode_auto"),
            InlineKeyboardButton("مخصص - أنا أحدد", callback_data="mode_custom"),
        ]
    ]

    await update.message.reply_text(
        f"تم استلام الملف\n\n"
        f"الاسم: {file_name}\n"
        f"الصفوف: {rows:,} | الأعمدة: {cols}\n"
        f"الأعمدة: {col_names}\n\n"
        "عايز التحليل يكون إزاي؟",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
