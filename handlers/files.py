import logging

from telegram import Update
from telegram.ext import ContextTypes

import os

ADMIN_IDS = [6850454574]
ASSIGNMENT_ADMIN_IDS = []
SYSTEM_NAME = os.getenv("SYSTEM_NAME", "UniX2")
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "20"))
from database.queries import add_summary, add_exam
from keyboards.main_menu import subjects_summary_menu
from keyboards.main_menu import subjects_exam_menu

logger = logging.getLogger(__name__)


# =========================================================
# استقبال الملفات
# =========================================================

async def handle_document(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """معالجة الملفات المستلمة من المسؤولين"""

    user_id = update.effective_user.id
    document = update.message.document

    if not document:
        return

    file_name = document.file_name or "ملف بدون اسم"
    file_id = document.file_id
    file_size = document.file_size or 0

    # =====================================================
    # التحقق من صلاحية رفع الملفات
    # =====================================================

    allowed_users = set(ADMIN_IDS) | set(ASSIGNMENT_ADMIN_IDS)

    if user_id not in allowed_users:
        await update.message.reply_text(
            "❌ ليس لديك صلاحية رفع الملفات."
        )
        return

    # =====================================================
    # التحقق من نوع الملف
    # =====================================================

    allowed_extensions = (
        ".pdf",
        ".doc",
        ".docx",
    )

    if not file_name.lower().endswith(allowed_extensions):
        await update.message.reply_text(
            """
⚠️ نوع الملف غير مدعوم.

✅ الملفات المسموحة:
📄 PDF
📝 DOC
📝 DOCX
"""
        )
        return

    # =====================================================
    # التحقق من حجم الملف
    # =====================================================

    max_size_bytes = MAX_FILE_SIZE_MB * 1024 * 1024

    if file_size > max_size_bytes:
        await update.message.reply_text(
            f"⚠️ حجم الملف كبير جدًا.\n"
            f"الحد الأقصى: {MAX_FILE_SIZE_MB} MB"
        )
        return

    # =====================================================
    # إضافة ملخص
    # =====================================================

    if context.user_data.get("adding_summary"):

        subject = context.user_data.get("subject")
        lecture = context.user_data.get("lecture")

        if not subject or not lecture:
            await update.message.reply_text(
                "⚠️ لم يتم تحديد المادة أو المحاضرة."
            )
            return

        add_summary(subject, lecture, file_id)

        logger.info(f"✅ Summary added: {subject} - {lecture} by {user_id}")

        await update.message.reply_text(
            f"""
━━━━━━━━━━━━━━━━━━━━
✅ تم حفظ الملخص بنجاح
━━━━━━━━━━━━━━━━━━━━

📚 المادة:
{subject}

📖 المحاضرة:
{lecture}

📎 اسم الملف:
{file_name}

━━━━━━━━━━━━━━━━━━━━
🚀 <b>{SYSTEM_NAME}</b>
💡 نظامك الجامعي الذكي
""",
            reply_markup=subjects_summary_menu(),
            parse_mode="HTML"
        )

        # تنظيف الحالة
        context.user_data.pop("subject", None)
        context.user_data.pop("lecture", None)
        context.user_data.pop("adding_summary", None)

        return

    # =====================================================
    # إضافة امتحان
    # =====================================================

    if context.user_data.get("adding_exam"):

        subject = context.user_data.get("exam_subject")
        exam_name = context.user_data.get("exam_name")

        if not subject or not exam_name:
            await update.message.reply_text(
                "⚠️ لم يتم تحديد المادة أو اسم الامتحان."
            )
            return

        add_exam(subject, exam_name, file_id)

        logger.info(f"✅ Exam added: {subject} - {exam_name} by {user_id}")

        await update.message.reply_text(
            f"""
━━━━━━━━━━━━━━━━━━━━
✅ تم حفظ الامتحان بنجاح
━━━━━━━━━━━━━━━━━━━━

📚 المادة:
{subject}

📝 الامتحان:
{exam_name}

📎 اسم الملف:
{file_name}

━━━━━━━━━━━━━━━━━━━━
🚀 <b>{SYSTEM_NAME}</b>
💡 نظامك الجامعي الذكي
""",
            reply_markup=subjects_exam_menu(),
            parse_mode="HTML"
        )

        # تنظيف الحالة
        context.user_data.pop("exam_subject", None)
        context.user_data.pop("exam_name", None)
        context.user_data.pop("adding_exam", None)

        return

    # =====================================================
    # ملف بدون عملية محددة
    # =====================================================

    await update.message.reply_text(
        "⚠️ لم يتم تحديد العملية المطلوبة لهذا الملف."
    )
