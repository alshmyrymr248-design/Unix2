from telegram import Update
from telegram.ext import ContextTypes

from database.queries import add_summary


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):

    document = update.message.document

    subject = context.user_data.get("subject")
    lecture = context.user_data.get("lecture")

    if not subject or not lecture:
        await update.message.reply_text(
            "⚠️ لم يتم تحديد المادة أو المحاضرة."
        )
        return


    file_id = document.file_id


    add_summary(
        subject,
        lecture,
        file_id
    )


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
{document.file_name}

━━━━━━━━━━━━━━━━━━━━
🚀 UniX2
💡 نظامك الجامعي الذكي
"""
    )


    context.user_data.pop("subject", None)
    context.user_data.pop("lecture", None)
    context.user_data.pop("adding_summary", None)
    