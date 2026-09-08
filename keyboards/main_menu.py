from telegram import ReplyKeyboardMarkup


# =========================================================
# القائمة الرئيسية للطلاب
# =========================================================

def main_menu():
    keyboard = [
        ["📚 المواد الدراسية", "📁 الملخصات"],
        ["📝 التكاليف", "📄 الامتحانات السابقة"],
        ["⏰ الدوام", "📍 أماكن القاعات"],
        ["📢 الإعلانات", "🧠 UniX2 AI"],
        ["👤 المندوب", "💰 مسؤول التكاليف"],
        ["👨‍💻 مهندس النظام", "ℹ️ عن النظام"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="💡 اختر الخدمة المطلوبة...",
    )


# =========================================================
# قائمة المواد
# =========================================================

def subjects_summary_menu():
    keyboard = [
        ["🗄️ أساسيات قواعد البيانات"],
        ["💻 معمارية وتنظيم الحاسوب"],
        ["☕ البرمجة الكائنية التوجه (Java)"],
        ["🌐 شبكات الحاسوب"],
        ["🎨 تصميم الويب 1"],
        ["🗣️ مهارات الاتصال"],
        ["🇾🇪 ثقافة وطنية"],
        ["🔙 العودة"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="📚 اختر المادة...",
    )


# =========================================================
# قائمة محاضرات الملخصات
# =========================================================

def lectures_summary_menu():
    keyboard = [
        ["1️⃣ المحاضرة الأولى"],
        ["2️⃣ المحاضرة الثانية"],
        ["3️⃣ المحاضرة الثالثة"],
        ["4️⃣ المحاضرة الرابعة"],
        ["5️⃣ المحاضرة الخامسة"],
        ["6️⃣ المحاضرة السادسة"],
        ["7️⃣ المحاضرة السابعة"],
        ["🔙 العودة للمواد"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="📖 اختر المحاضرة...",
    )


# =========================================================
# قائمة إدارة الملخصات
# =========================================================

def summaries_admin_menu():
    keyboard = [
        ["➕ إضافة ملخص"],
        ["📂 عرض الملخصات"],
        ["❌ حذف ملخص"],
        ["🔙 العودة للوحة الإدارة"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="📚 اختر العملية...",
    )


# =========================================================
# عرض ملخصات المادة
# =========================================================

def view_summaries_menu(lectures):
    keyboard = []

    for lecture in lectures:
        keyboard.append([lecture])

    keyboard.append(["🔙 العودة للمواد"])

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="📂 اختر الملخص...",
    )


# =========================================================
# قائمة مواد الامتحانات
# =========================================================

def subjects_exam_menu():
    keyboard = [
        ["🗄️ أساسيات قواعد البيانات"],
        ["💻 معمارية وتنظيم الحاسوب"],
        ["☕ البرمجة الكائنية التوجه (Java)"],
        ["🌐 شبكات الحاسوب"],
        ["🎨 تصميم الويب 1"],
        ["🗣️ مهارات الاتصال"],
        ["🇾🇪 ثقافة وطنية"],
        ["🔙 العودة"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="📚 اختر المادة...",
    )


# =========================================================
# قائمة امتحانات المادة
# =========================================================

def exams_menu(exams):
    keyboard = []

    for exam in exams:
        keyboard.append([exam])

    keyboard.append(["🔙 العودة للمواد"])

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="📄 اختر الامتحان...",
    )




# =========================================================
# زر فتح محادثة UniX2 AI
# =========================================================

from telegram import InlineKeyboardMarkup, InlineKeyboardButton


def ai_chat_button():
    """زر فتح محادثة UniX2 AI"""

    keyboard = [
        [
            InlineKeyboardButton(
                "🧠 فتح محادثة UniX2 AI",
                url="https://t.me/UniX2_AI_Bot",
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)

