from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.analyzer import analyze_file
from services.report_builder import build_report


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "mode_auto":
        await query.edit_message_text("ممتاز! جاري التحليل التلقائي...")
        await run_analysis(update, context, focus=None)

    elif data == "mode_custom":
        await query.edit_message_text(
            "اكتبلي إيه اللي عايز أركز عليه في التحليل\n\n"
            "مثلاً: المبيعات الشهرية، أو مقارنة المناطق، أو أعلى المنتجات"
        )
        context.user_data["waiting_for_focus"] = True

    elif data.startswith("col_"):
        col = data.replace("col_", "")
        await query.edit_message_text(f"هحلل البيانات مع التركيز على: {col}")
        await run_analysis(update, context, focus=col)


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("waiting_for_focus"):
        focus = update.message.text
        context.user_data["waiting_for_focus"] = False
        await update.message.reply_text(f"تمام! هركز على: {focus}\nجاري التحليل...")
        await run_analysis(update, context, focus=focus)
    else:
        await update.message.reply_text("ابعتلي ملف CSV أو Excel عشان أبدأ التحليل")


async def run_analysis(update: Update, context: ContextTypes.DEFAULT_TYPE, focus: str):
    file_path = context.user_data.get("file_path")
    file_name = context.user_data.get("file_name", "report")

    if not file_path:
        msg = update.callback_query.message if update.callback_query else update.message
        await msg.reply_text("مفيش ملف محفوظ. ابعت الملف تاني لو سمحت.")
        return

    msg = update.callback_query.message if update.callback_query else update.message

    progress_msg = await msg.reply_text(
        "جاري التحليل...\n"
        "1️⃣ قراءة البيانات\n"
        "2️⃣ إرسال لـ AI\n"
        "3️⃣ بناء الداشبورد"
    )

    try:
        ai_result = await analyze_file(file_path, focus=focus)

        await progress_msg.edit_text(
            "جاري التحليل...\n"
            "✅ قراءة البيانات\n"
            "✅ إرسال لـ AI\n"
            "3️⃣ بناء الداشبورد"
        )

        report_url = await build_report(file_path, file_name, ai_result)

        await progress_msg.edit_text(
            "جاري التحليل...\n"
            "✅ قراءة البيانات\n"
            "✅ إرسال لـ AI\n"
            "✅ بناء الداشبورد"
        )

        await msg.reply_text(
            f"التحليل جاهز!\n\n"
            f"الداشبورد: {report_url}\n\n"
            f"الملاحظة الرئيسية:\n{ai_result.get('insights', '')}"
        )

    except Exception as e:
        await progress_msg.edit_text(f"في مشكلة أثناء التحليل: {e}")
