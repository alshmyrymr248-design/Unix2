import os
import logging
import google.generativeai as genai

from telegram import Update
from telegram.ext import ContextTypes

# إعداد Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-3.6-flash")

logger = logging.getLogger(__name__)


# ============================
# أمر البداية
# ============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """رسالة الترحيب بمحادثة UniX2 AI"""

    user_name = update.effective_user.full_name or "عزيزي الطالب"

    welcome_text = f"""
╔════════════════════════════╗
       🧠 UniX2 AI
   🤖 المساعد الذكي المتطور
╚════════════════════════════╝

✨ أهلاً بك {user_name} ✨

أنا مساعدك الجامعي الذكي،
تم تطويري لخدمة طلاب قسم تقنية المعلومات.

━━━━━━━━━━━━━━━━━━━━
⚡ ماذا أستطيع أن أفعل؟
━━━━━━━━━━━━━━━━━━━━

📚 شرح المواد الدراسية
💻 حل مسائل البرمجة
📝 كتابة الأبحاث والتقارير
🧠 تبسيط المفاهيم المعقدة
🌍 الإجابة عن أي سؤال
🖼️ قراءة الصور وفهمها

━━━━━━━━━━━━━━━━━━━━
✅ مميزاتي:
━━━━━━━━━━━━━━━━━━━━

🔹 إجابات دقيقة وسريعة
🔹 أدعم العربية والإنجليزية
🔹 أحتفظ بسجل المحادثة
🔹 أستقبل الصور والأسئلة

━━━━━━━━━━━━━━━━━━━━
👨‍💻 مهندس النظام:
⭐ عمر الشميري

🚀 UniX2 AI - ذكاء بلا حدود
"""

    await update.message.reply_text(welcome_text)


# ============================
# معالجة الرسائل النصية
# ============================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة رسائل الطالب النصية"""

    user_text = update.message.text

    if not user_text:
        return

    await update.message.chat.send_chat_action("typing")

    try:
        history = context.user_data.get("ai_history", [])

        chat = model.start_chat(history=history)

        response = chat.send_message(user_text)

        reply_text = response.text

        history.append({"role": "user", "parts": [user_text]})
        history.append({"role": "model", "parts": [reply_text]})

        context.user_data["ai_history"] = history[-10:]

        await update.message.reply_text(reply_text)

    except Exception as e:
        logger.error(f"AI Error: {e}")
        await update.message.reply_text(
            "⚠️ حدث خطأ أثناء معالجة سؤالك.\n"
            "حاول مرة أخرى بعد قليل."
        )


# ============================
# معالجة الصور
# ============================

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة الصور المرسلة للذكاء الاصطناعي"""

    await update.message.chat.send_chat_action("typing")

    try:
        # جلب أكبر حجم للصورة
        photo = update.message.photo[-1]
        file = await photo.get_file()

        # تنزيل الصورة في الذاكرة
        photo_bytes = await file.download_as_bytearray()

        # إرسال الصورة إلى Gemini
        image_data = {
            "mime_type": "image/jpeg",
            "data": bytes(photo_bytes),
        }

        caption = update.message.caption or "اشرح لي هذه الصورة بالتفصيل"

        response = model.generate_content([caption, image_data])

        reply_text = response.text

        await update.message.reply_text(reply_text)

    except Exception as e:
        logger.error(f"Photo AI Error: {e}")
        await update.message.reply_text(
            "⚠️ حدث خطأ أثناء معالجة الصورة.\n"
            "حاول مرة أخرى بعد قليل."
        )