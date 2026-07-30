from telegram import ReplyKeyboardMarkup


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
        one_time_keyboard=False
    )


def admin_menu():
    keyboard = [
        ["📚 إدارة الملخصات"],
        ["📝 إدارة التكاليف"],
        ["📢 إدارة الإعلانات"],
        ["📄 إدارة الملفات"],
        ["⏰ إدارة الدوام"],
        ["🔙 العودة للقائمة الرئيسية"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )


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
        one_time_keyboard=False
    )


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
        one_time_keyboard=False
    )


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
        one_time_keyboard=False
    )


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
        one_time_keyboard=False
    )


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
        one_time_keyboard=False
    )


def view_summaries_menu(lectures):
    keyboard = []

    for lecture in lectures:
        keyboard.append([lecture])

    keyboard.append(["🔙 العودة للمواد"])

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )
