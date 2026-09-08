from telegram import ReplyKeyboardMarkup

import os
SYSTEM_NAME = os.getenv("SYSTEM_NAME", "Unix2")


# =========================================================
# لوحة الإدارة الرئيسية
# =========================================================

def admin_menu():
    """القائمة الرئيسية للوحة الإدارة"""

    keyboard = [
        ["📚 إدارة الملخصات"],
        ["📄 إدارة الامتحانات السابقة"],
        ["📝 إدارة التكاليف"],
        ["📢 إدارة الإعلانات"],
        ["⏰ إدارة الدوام"],
        ["📍 إدارة أماكن القاعات"],
        ["👥 إدارة الطلاب"],
        ["💾 النسخ الاحتياطي"],
        ["⚙️ إعدادات النظام"],
        ["🔙 العودة للقائمة الرئيسية"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder=f"🔐 لوحة إدارة {SYSTEM_NAME}",
    )


# =========================================================
# إدارة الملخصات
# =========================================================

def summaries_admin_menu():
    """قائمة إدارة الملخصات"""

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
# إدارة الامتحانات
# =========================================================

def exams_admin_menu():
    """قائمة إدارة الامتحانات السابقة"""

    keyboard = [
        ["➕ إضافة امتحان"],
        ["📂 عرض الامتحانات"],
        ["❌ حذف امتحان"],
        ["🔙 العودة للوحة الإدارة"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="📄 اختر العملية...",
    )


# =========================================================
# إدارة الإعلانات
# =========================================================

def announcements_admin_menu():
    """قائمة إدارة الإعلانات"""

    keyboard = [
        ["➕ إضافة إعلان"],
        ["📂 عرض الإعلانات"],
        ["❌ حذف إعلان"],
        ["🔙 العودة للوحة الإدارة"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="📢 اختر العملية...",
    )


# =========================================================
# إدارة الدوام
# =========================================================

def attendance_admin_menu():
    """قائمة إدارة الدوام"""

    keyboard = [
        ["✅ إضافة دوام"],
        ["❌ حذف دوام"],
        ["📂 عرض الدوام"],
        ["🔙 العودة للوحة الإدارة"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="⏰ اختر العملية...",
    )


# =========================================================
# إدارة الطلاب
# =========================================================

def students_admin_menu():
    """قائمة إدارة الطلاب"""

    keyboard = [
        ["👥 قائمة الطلاب"],
        ["🔍 البحث عن طالب"],
        ["📊 إحصائيات الطلاب"],
        ["🔙 العودة للوحة الإدارة"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="👥 اختر العملية...",
    )


# =========================================================
# النسخ الاحتياطي وإعدادات النظام
# =========================================================

def system_admin_menu():
    """قائمة النسخ الاحتياطي وإعدادات النظام"""

    keyboard = [
        ["💾 إنشاء نسخة احتياطية"],
        ["📥 استعادة نسخة احتياطية"],
        ["⚙️ إعدادات النظام"],
        ["🔙 العودة للوحة الإدارة"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="⚙️ اختر العملية...",
    )
