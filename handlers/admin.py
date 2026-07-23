from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_IDS


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in ADMIN_IDS:
        await update.message.reply_text(
            "❌ ليس لديك صلاحية دخول لوحة الإدارة."
        )
        return

    await update.message.reply_text(
        """
━━━━━━━━━━━━━━━━━━━━
🔐 لوحة إدارة UniX2
━━━━━━━━━━━━━━━━━━━━

👨‍💻 أهلاً بك يا مهندس النظام

اختر الخدمة التي تريد إدارتها:

📚 إدارة الملخصات
📝 إدارة التكاليف
📢 إدارة الإعلانات
📄 إدارة الملفات
⏰ إدارة الدوام

━━━━━━━━━━━━━━━━━━━━
🚀 UniX2
💡 نظامك الجامعي الذكي
"""
    )
