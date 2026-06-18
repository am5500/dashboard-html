import logging
import os
import threading
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
)
from handlers.file_handler import handle_file
from handlers.callback_handler import handle_callback
from handlers.start_handler import handle_start

# استيراد السيرفر
from server import app

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

BOT_TOKEN = os.getenv("BOT_TOKEN", "8861695419:AAFMWZ2_jpsjwkbJccl-WdEQt0dWgCHf5Lo")

def run_server():
    """تشغيل سيرفر Flask في Thread منفصل"""
    port = int(os.getenv("PORT", 5000))
    print(f"🌐 السيرفر شغال على http://localhost:{port}")
    app.run(host="0.0.0.0", port=port)

def main():
    # شغل السيرفر في Thread منفصل (عشان ميوقفش البوت)
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # شغل البوت
    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()

    app_bot.add_handler(CommandHandler("start", handle_start))
    app_bot.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    app_bot.add_handler(CallbackQueryHandler(handle_callback))

    print("🤖 البوت شغال...")
    app_bot.run_polling()

if __name__ == "__main__":
    main()
