from telegram import Update
from telegram.ext import ContextTypes

from keyboards.main_menu import main_menu
from keyboards.admin_menu import admin_menu

import os

ADMIN_IDS = [6850454574]
ASSIGNMENT_ADMIN_IDS = []
REP_IDS = []
SYSTEM_NAME = os.getenv("SYSTEM_NAME", "UniX2")
SYSTEM_VERSION = os.getenv("SYSTEM_VERSION", "2.0")
MAINTENANCE_MODE = os.getenv("MAINTENANCE_MODE", "false").lower() == "true"
from database.queries import add_user


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر /start - بداية تفاعل المستخدم مع البوت"""

    user_id = update.effective_user.id
    username = update.effective_user.username or ""
    full_name = update.effective_user.full_name or "طالب"

    # تنظيف الحالات السابقة
    context.user_data.clear()

    # ============================
    # فحص وضع الصيانة
    # ============================
    if MAINTENANCE_MODE and user_id not in ADMIN_IDS:
        await update.message.reply_text(
            "🛠️ <b>النظام في وضع الصيانة حالياً</b>\n"
            "الرجاء المحاولة لاحقًا.\n\n"
            "شكرًا لتفهمك 🌹",
            parse_mode="HTML",
        )
        return

    # ============================
    # تسجيل المستخدم تلقائيًا
    # ============================
    try:
        # تحديد الدور بناءً على معرف المستخدم
        if user_id in ADMIN_IDS:
            role = "super_admin"
        elif user_id in ASSIGNMENT_ADMIN_IDS:
            role = "assignments_admin"
        elif user_id in REP_IDS:
            role = "representative"
        else:
            role = "student"

        # تسجيل أو تحديث بيانات المستخدم
        add_user(
            telegram_id=user_id,
            name=full_name,
            role=role,
        )

    except Exception as e:
        print(f"❌ Error registering user {user_id}: {e}")

    # ============================
    # اختيار القائمة المناسبة
    # ============================
    if user_id in ADMIN_IDS:
        keyboard = admin_menu()
        role_text = "👨‍💻 <b>مهندس النظام</b>"
    elif user_id in ASSIGNMENT_ADMIN_IDS:
        # سيتم لاحقًا إنشاء قائمة خاصة بمسؤول التكاليف
        keyboard = admin_menu()
        role_text = "💰 <b>مسؤول التكاليف</b>"
    elif user_id in REP_IDS:
        # سيتم لاحقًا إنشاء قائمة خاصة بالمندوب
        keyboard = admin_menu()
        role_text = "👤 <b>مندوب الدفعة</b>"
    else:
        keyboard = main_menu()
        role_text = "👨‍🎓 <b>طالب</b>"

    # ============================
    # إرسال رسالة الترحيب
    # ============================
    welcome_message = f"""
╔════════════════════════════╗
          🎓 <b>{SYSTEM_NAME}</b>
   Smart University Assistant
           Version {SYSTEM_VERSION}
╚════════════════════════════╝

السلام عليكم ورحمة الله وبركاته 🌹

✨ أهلاً وسهلاً بك في
🎓 <b>{SYSTEM_NAME}</b>

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

💎 نوع الحساب: {role_text}

💡 اختر الخدمة التي تريدها
من القائمة الموجودة بالأسفل 👇

🚀 نتمنى لك تجربة جامعية ممتعة
مع {SYSTEM_NAME}.
"""    

    await update.message.reply_text(
        welcome_message,
        reply_markup=keyboard,
        parse_mode="HTML",
    )
