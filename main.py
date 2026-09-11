import logging
import asyncio

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
AI_BOT_TOKEN = os.getenv("AI_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
from handlers.start import start
from handlers.buttons import button_handler
from handlers.files import handle_document
from database.models import create_tables

# إعداد السجل
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def error_handler(update, context):
    """معالجة الأخطاء العامة"""
    logger.error(msg="حدث خطأ أثناء معالجة تحديث:", exc_info=context.error)

    if update and update.effective_chat:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="⚠️ حدث خطأ غير متوقع، الرجاء المحاولة لاحقًا أو إبلاغ الإدارة.",
        )


def build_main_app():
    """بناء تطبيق البوت الرئيسي UniX2"""
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button_handler))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_error_handler(error_handler)

    return app


def build_ai_app():
    """بناء تطبيق بوت UniX2 AI"""
    import google.generativeai as genai

    genai.configure(api_key=GEMINI_API_KEY)

    from handlers.ai_bot import start as ai_start
    from handlers.ai_bot import handle_message as ai_handle
    from handlers.ai_bot import handle_photo as ai_photo

    app = Application.builder().token(AI_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", ai_start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_handle))
    app.add_handler(MessageHandler(filters.PHOTO, ai_photo))

    return app


async def run_bots():
    """تشغيل البوتين معًا"""
    create_tables()

    main_app = build_main_app()
    ai_app = build_ai_app()

    logger.info("✅ Database tables are ready")
    logger.info("🚀 UniX2 Bot Started Successfully")
    logger.info("🚀 UniX2 AI Bot Started Successfully")

    await main_app.initialize()
    await ai_app.initialize()

    await main_app.start()
    await ai_app.start()

    await asyncio.gather(
        main_app.updater.start_polling(drop_pending_updates=True),
        ai_app.updater.start_polling(drop_pending_updates=True),
    )

    await asyncio.Event().wait()


def main():
    asyncio.run(run_bots())


if __name__ == "__main__":
    main()
