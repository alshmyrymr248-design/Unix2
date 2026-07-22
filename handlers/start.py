from telegram import Update
from telegram.ext import ContextTypes

from keyboards.main_menu import main_menu


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    welcome_message = """
╔════════════════════════════╗
          🎓 UniX2
   Smart University Assistant
           Version 2.0
╚════════════════════════════╝

السلام عليكم ورحمة الله وبركاته 🌹

✨ أهلاً وسهلاً بك في
🎓 UniX2

النظام الجامعي الذكي المصمم
لتسهيل حياتك الجامعية وجمع كل
الخدمات في مكان واحد.

━━━━━━━━━━━━━━━━━━━━━━

🏛️ كلية علوم وهندسة الحاسوب
💻 قسم تقنية المعلومات

━━━━━━━━━━━━━━━━━━━━━━

👨‍💻 مهندس النظام:
⭐ عمر الشميري

👤 مندوب الدفعة:
⭐ عبدالرزاق النجار

━━━━━━━━━━━━━━━━━━━━━━

💎 اختر الخدمة التي تريدها
من القائمة الموجودة بالأسفل 👇

🚀 نتمنى لك تجربة جامعية ممتعة
مع UniX2.
"""

    await update.message.reply_text(
        welcome_message,
        reply_markup=main_menu()
    )
