from telegram.ext import Application, CommandHandler, MessageHandler, filters

from config import BOT_TOKEN
from handlers.start import start
from handlers.buttons import button_handler
from handlers.files import handle_document
from database.models import create_tables


def main():

    # إنشاء جداول قاعدة البيانات
    create_tables()

    app = Application.builder().token(BOT_TOKEN).build()

    # أمر البداية
    app.add_handler(CommandHandler("start", start))

    # التعامل مع ضغطات الأزرار
    app.add_handler(MessageHandler(filters.TEXT, button_handler))

    # استقبال الملفات
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    print("🚀 UniX2 Bot Started Successfully")

    app.run_polling()


if __name__ == "__main__":
    main()
