import google.generativeai as genai
from telegram import Update
from telegram.ext import ContextTypes

import os
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# إعداد Gemini
genai.configure(api_key=GEMINI_API_KEY)

# الموديل الجديد المدعوم
model = genai.GenerativeModel("gemini-3.6-flash")


async def ai_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """الرد على رسائل الطالب داخل محادثة الذكاء الاصطناعي"""

    user_id = update.effective_user.id
    user_text = update.message.text

    # لو الطالب كتب خروج أو رجوع
    if user_text in ["خروج", "رجوع", "الخروج", "الرجوع"]:
        context.user_data.pop("ai_mode", None)
        context.user_data.pop("ai_history", None)
        from keyboards.main_menu import main_menu
        await update.message.reply_text(
            "✅ تم الخروج من محادثة الذكاء الاصطناعي.\n"
            "🏠 أهلاً بك في القائمة الرئيسية.",
            reply_markup=main_menu(),
        )
        return

    # إرسال حالة الكتابة
    await update.message.chat.send_chat_action("typing")

    try:
        # جلب آخر 10 رسائل من سجل المحادثة
        history = context.user_data.get("ai_history", [])

        # بناء المحادثة
        chat = model.start_chat(history=history)

        # إرسال السؤال
        response = chat.send_message(user_text)

        # الحصول على الرد
        reply_text = response.text

        # تحديث السجل
        history.append({"role": "user", "parts": [user_text]})
        history.append({"role": "model", "parts": [reply_text]})

        # الاحتفاظ بآخر 10 رسائل فقط
        context.user_data["ai_history"] = history[-10:]

        # إرسال الرد
        await update.message.reply_text(reply_text)

    except Exception as e:
        print(f"❌ AI Error for user {user_id}: {e}")
        await update.message.reply_text(
            "⚠️ حدث خطأ أثناء معالجة سؤالك.\n"
            "حاول مرة أخرى بعد قليل."
        )
