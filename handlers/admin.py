import logging

from telegram import Update
from telegram.ext import ContextTypes

import os

ADMIN_IDS = [6850454574]
SYSTEM_NAME = os.getenv("SYSTEM_NAME", "UniX2")
from keyboards.admin_menu import admin_menu

logger = logging.getLogger(__name__)


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    فتح لوحة إدارة UniX2 والتحقق من صلاحية المستخدم.
    """

    user_id = update.effective_user.id
    full_name = update.effective_user.full_name or "مدير النظام"

    # =====================================================
    # التحقق من صلاحية المستخدم
    # =====================================================

    if user_id not in ADMIN_IDS:
        await update.message.reply_text(
            "❌ ليس لديك صلاحية دخول لوحة الإدارة."
        )
        return

    # تسجيل دخول المدير في السجل
    logger.info(f"🔐 Admin {full_name} ({user_id}) opened admin panel")

    # =====================================================
    # تنظيف الحالات القديمة
    # =====================================================

    context.user_data.pop("admin_state", None)
    context.user_data.pop("subject", None)
    context.user_data.pop("lecture", None)
    context.user_data.pop("exam_subject", None)

    # =====================================================
    # رسالة لوحة الإدارة
    # =====================================================

    admin_message = f"""
━━━━━━━━━━━━━━━━━━━━
🔐 لوحة إدارة <b>{SYSTEM_NAME}</b>
━━━━━━━━━━━━━━━━━━━━

👨‍💻 أهلاً بك <b>{full_name}</b>

من هنا تستطيع إدارة النظام الجامعي بالكامل:

📚 الملخصات
📄 الامتحانات السابقة
📝 التكاليف
📢 الإعلانات
⏰ الدوام
📍 أماكن القاعات
👥 الطلاب
💾 النسخ الاحتياطي
⚙️ إعدادات النظام

━━━━━━━━━━━━━━━━━━━━
🚀 <b>{SYSTEM_NAME}</b>
💡 نظامك الجامعي الذكي
"""

    await update.message.reply_text(
        admin_message,
        reply_markup=admin_menu(),
        parse_mode="HTML",
    )
