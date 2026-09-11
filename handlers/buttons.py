from multiprocessing import context
from pydoc import text
from turtle import update

from telegram import Update
from telegram.ext import ContextTypes

from keyboards.main_menu import (
    main_menu,
    summaries_admin_menu,
    subjects_summary_menu,
    lectures_summary_menu,
    view_summaries_menu,
    subjects_exam_menu,
    exams_menu,
    ai_chat_button,
)
from keyboards.admin_menu import admin_menu, exams_admin_menu

from database.queries import (
    get_summaries,
    delete_summary_by_subject,
    get_exams,
    add_exam,
    delete_exam_by_subject,
    get_assignments,
)


# =========================================================
# تنظيف حالات المستخدم
# =========================================================

def clear_user_states(context):
    context.user_data.pop("viewing_exam", None)
    context.user_data.pop("exam_subject", None)

    context.user_data.pop("adding_summary", None)
    context.user_data.pop("viewing_summary", None)
    context.user_data.pop("deleting_summary", None)

    context.user_data.pop("adding_exam", None)
    context.user_data.pop("deleting_exam", None)

    context.user_data.pop("subject", None)
    context.user_data.pop("lecture", None)
    context.user_data.pop("exam_name", None)


# =========================================================
# معالج الأزرار الرئيسي
# =========================================================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):


# =====================================================
# وضع الذكاء الاصطناعي 
# =====================================================

    if context.user_data.get("ai_mode"):
        from handlers.ai import ai_reply
        await ai_reply(update, context)
        return

    if not update.message or not update.message.text:
        return

    text = update.message.text

    # =====================================================
    # القائمة الرئيسية
    # =====================================================

    if text == "📚 المواد الدراسية":

        clear_user_states(context)

        await update.message.reply_text(
            "━━━━━━━━━━━━━━━━━━\n"
            "📚 المواد الدراسية\n"
            "🎓 المستوى الثاني\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "📚 المواد الدراسية:\n\n"
            "🗄️ أساسيات قواعد البيانات\n"
            "💻 معمارية وتنظيم الحاسوب\n"
            "☕ البرمجة الكائنية التوجه (Java)\n"
            "🌐 شبكات الحاسوب\n"
            "🎨 تصميم الويب 1\n"
            "🗣️ مهارات الاتصال\n"
            "🇾🇪 ثقافة وطنية\n\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "🚀 UniX2\n"
            "💡 نظامك الجامعي الذكي"
        )

        return

    # =====================================================
    # الملخصات
    # =====================================================

    elif text == "📁 الملخصات":

        clear_user_states(context)

        context.user_data["viewing_summary"] = True

        await update.message.reply_text(
            "━━━━━━━━━━━━━━━━━━\n"
            "📁 الملخصات\n"
            "🎓 المستوى الثاني\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "اختر المادة التي تريد ملخصاتها 👇\n\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "🚀 UniX2"
        )

        await update.message.reply_text(
            "📚 اختر المادة:",
            reply_markup=subjects_summary_menu()
        )

        return

    # =====================================================
    # التكاليف
    # =====================================================

    elif text == "📝 التكاليف":

        clear_user_states(context)

        assignments = get_assignments()

        if assignments:
            message = (
                 "━━━━━━━━━━━━━━━━━━\n"
                 "📝 التكاليف والواجبات\n"
                 "🎓 المستوى الثاني\n"
                 "━━━━━━━━━━━━━━━━━━\n\n"
                 "📚 التكاليف الحالية:\n\n"

            )

            for assignment in assignments:
                subject = assignment[1]
                title = assignment[2]
                description = assignment[3]
                deadline = assignment[4]

                message += f"🗄️ المادة: {subject}\n"
                message += f"📝 التكليف: {title}\n"

                if description:
                    message += f"📋 التفاصيل: {description}\n"

                if deadline:
                    message += f"📅 التسليم: {deadline}\n"

                message += "\n"

                message += (
                    "━━━━━━━━━━━━━━━━━━\n"
                    "🚀 UniX2\n"
                    "💡 نظامك الجامعي الذكي"

            )

        else:
            message = (
                "━━━━━━━━━━━━━━━━━━\n"
                "📝 التكاليف والواجبات\n"
                "🎓 المستوى الثاني\n"
                "━━━━━━━━━━━━━━━━━━\n\n"
                "✨ لا توجد تكاليف حاليًا ✨\n\n"
                "📚 استمتع بوقتك وركّز على مذاكرتك.\n"
                "🔔 أي تكليف جديد سيظهر هنا مباشرة.\n\n"
                "━━━━━━━━━━━━━━━━━━\n"
                "🚀 UniX2"
                "💡 نظامك الجامعي الذكي"
            )

        await update.message.reply_text(message)
        return

                
    # =====================================================
    # الامتحانات السابقة - للطلاب
    # =====================================================

    elif text == "📄 الامتحانات السابقة":

        clear_user_states(context)

        context.user_data["viewing_exam"] = True

        await update.message.reply_text(
            """
━━━━━━━━━━━━━━━━━━━━
📄 الامتحانات السابقة
━━━━━━━━━━━━━━━━━━━━

📚 اختر المادة التي تريد عرض امتحاناتها:

━━━━━━━━━━━━━━━━━━━━
🚀 UniX2
💡 نظامك الجامعي الذكي
""",
            reply_markup=subjects_exam_menu()
        )

        return

    # =====================================================
    # الدوام
    # =====================================================

    elif text == "⏰ الدوام":

        clear_user_states(context)

        from database.queries import get_attendance

        attendance = get_attendance()

        if attendance:

           latest = attendance[0]
           details = latest[6] if len(latest) > 6 else ""

           await update.message.reply_text(
               f"━━━━━━━━━━━━━━━━━━━━\n"
               f"⏰ دوام اليوم\n"
               f"🎓 المستوى الثاني\n"
               f"━━━━━━━━━━━━━━━━━━━━\n\n"
               f"{details}\n\n"
               f"━━━━━━━━━━━━━━━━━━━━\n"
               f"🚀 UniX2"
            )

        else:

            await update.message.reply_text(
                "━━━━━━━━━━━━━━━━━━\n"
                "⏰ حالة الدوام اليوم\n"
                "🎓 المستوى الثاني\n"
                "━━━━━━━━━━━━━━━━━━\n\n"
                "❌ لا يوجد دوام اليوم\n\n"
                "📌 لا توجد محاضرات مسجلة حالياً.\n\n"
                "🔔 سيتم تحديث حالة الدوام\n"
                "عند إضافة أي محاضرة جديدة.\n\n"
                "━━━━━━━━━━━━━━━━━━\n"
                "🚀 UniX2\n"
                "💡 نظامك الجامعي الذكي"
            )

        return

    # =====================================================
    # أماكن القاعات
    # =====================================================

    elif text == "📍 أماكن القاعات":

        clear_user_states(context)

        await update.message.reply_text(
            "━━━━━━━━━━━━━━━━━━\n"
            "📍 أماكن القاعات\n"
            "🏛️ كلية علوم وهندسة الحاسوب\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "🏛️ المبنى القديم\n\n"
            "⬆️ الدور الثاني\n"
            "🎓 المدرج 6\n\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "🏢 مبنى الآداب\n\n"
            "📌 معافا الأهدل\n"
            "🎓 المدرجات الاثنين\n"
            "🎓 العلفي\n"
            "💻 معمل يمن موبايل\n"
            "💻 معمل الهندسة\n\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "🚀 UniX2\n"
            "📚 دليلك الجامعي الذكي"
        )

        return

    # =====================================================
    # الإعلانات
    # =====================================================

    elif text == "📢 الإعلانات":

        clear_user_states(context)

        await update.message.reply_text(
            "━━━━━━━━━━━━━━━━━━\n"
            "📢 الإعلانات الجامعية\n"
            "🎓 قسم تقنية المعلومات\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "🔔 آخر الأخبار والتحديثات:\n\n"
            "📌 لا توجد إعلانات جديدة حالياً.\n\n"
            "سيتم نشر:\n"
            "✅ مواعيد الاختبارات\n"
            "✅ تغييرات الدوام\n"
            "✅ التنبيهات المهمة\n"
            "✅ أخبار القسم\n\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "🚀 UniX2\n"
            "📚 ابقَ على اطلاع دائم"
        )

        return

    # =====================================================
    # UniX2 AI
    # =====================================================

    elif text == "🧠 UniX2 AI":

        clear_user_states(context)

        await update.message.reply_text(
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🧠 UniX2 AI\n"
            "🤖 المساعد الذكي المتطور\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "✨ اضغط على الزر بالأسفل\n"
            "لفتح محادثة خاصة مع المساعد الذكي ✨\n\n"
            "👨‍💻 مهندس النظام:\n"
            "⭐ عمر الشميري\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🚀 UniX2",

            reply_markup=ai_chat_button()
        )
    

        return

    # =====================================================
    # المندوب
    # =====================================================

    elif text == "👤 المندوب":

        clear_user_states(context)

        await update.message.reply_text(
            "━━━━━━━━━━━━━━━━━━\n"
            "👤 مندوب الدفعة\n"
            "🎓 المستوى الثاني\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "⭐ الاسم:\n"
            "عبدالرزاق النجار\n\n"
            "💬 حساب التواصل:\n"
            '<a href="https://t.me/axyom_rzq">@axyom_rzq</a>\n\n'
            "📌 اضغط على الحساب للتواصل مباشرة.\n\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "🚀 UniX2",
            parse_mode="HTML"
        )

        return

    # =====================================================
    # مسؤول التكاليف
    # =====================================================

    elif text == "💰 مسؤول التكاليف":

        clear_user_states(context)

        await update.message.reply_text(
            "━━━━━━━━━━━━━━━━━━\n"
            "💰 مسؤول التكاليف\n"
            "🎓 المستوى الثاني\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "⭐ الاسم:\n"
            "عبدالله البرعي\n\n"
            "📱 رقم التواصل:\n"
            "+967730185760\n\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "🚀 UniX2"
        )

        return

    # =====================================================
    # مهندس النظام
    # =====================================================

    elif text == "👨‍💻 مهندس النظام":

        clear_user_states(context)

        await update.message.reply_text(
            "━━━━━━━━━━━━━━━━━━━━\n"
            "👨‍💻 مهندس النظام\n"
            "🚀 UniX2 Developer\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "✨ مطور وصانع نظام UniX2 الذكي ✨\n\n"
            "⭐ الاسم:\n"
            "عمر الشميري\n\n"
            "💻 التخصص:\n"
            "تقنية معلومات | IT\n\n"
            "🧠 مجالات التطوير:\n"
            "🐍 Python\n"
            "🤖 الذكاء الاصطناعي\n"
            "⚙️ تطوير الأنظمة والبوتات\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "💬 للتواصل:\n"
            '<a href="https://t.me/alshmyrymr248">@alshmyrymr248</a>\n\n'
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🚀 UniX2",
            parse_mode="HTML"
        )

        return

    # =====================================================
    # عن النظام
    # =====================================================

    elif text == "ℹ️ عن النظام":

        clear_user_states(context)

        await update.message.reply_text(
            "━━━━━━━━━━━━━━━━━━━━\n"
            "ℹ️ عن نظام UniX2\n"
            "🎓 Smart University Assistant\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "🚀 UniX2 هو نظام جامعي ذكي\n"
            "تم تطويره لخدمة طلاب كلية علوم وهندسة الحاسوب\n"
            "وقسم تقنية المعلومات.\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "🎯 أهداف النظام:\n"
            "✅ تسهيل الوصول إلى الخدمات الجامعية\n"
            "✅ تنظيم المواد والملخصات\n"
            "✅ متابعة التكاليف والواجبات\n"
            "✅ معرفة الدوام والقاعات\n"
            "✅ توفير المساعدة الذكية\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "👨‍💻 مهندس النظام:\n"
            "⭐ عمر الشميري\n\n"
            "🚀 الإصدار:\n"
            "Version 2.0\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "💡 UniX2"
        )

        return

    # =====================================================
    # لوحة الإدارة
    # =====================================================

    elif text == "🔐 لوحة الإدارة":

        clear_user_states(context)

        from handlers.admin import admin_panel

        await admin_panel(update, context)

        return

    # =====================================================
    # إدارة الملخصات
    # =====================================================

    elif text == "📚 إدارة الملخصات":

        clear_user_states(context)

        await update.message.reply_text(
            """
━━━━━━━━━━━━━━━━━━━━
📚 إدارة الملخصات
━━━━━━━━━━━━━━━━━━━━

اختر العملية التي تريد تنفيذها:

━━━━━━━━━━━━━━━━━━━━
🚀 UniX2
💡 نظامك الجامعي الذكي
""",
            reply_markup=summaries_admin_menu()
        )

        return

    # =====================================================
    # إضافة ملخص
    # =====================================================

    elif text == "➕ إضافة ملخص":

        clear_user_states(context)

        context.user_data["adding_summary"] = True

        await update.message.reply_text(
            """
━━━━━━━━━━━━━━━━━━━━
➕ إضافة ملخص جديد
━━━━━━━━━━━━━━━━━━━━

📚 اختر المادة التي تريد إضافة ملخص لها:

━━━━━━━━━━━━━━━━━━━━
🚀 UniX2
💡 نظامك الجامعي الذكي
""",
            reply_markup=subjects_summary_menu()
        )

        return

    # =====================================================
    # إدارة الامتحانات السابقة
    # =====================================================

    elif text == "📄 إدارة الامتحانات السابقة":

        clear_user_states(context)

        await update.message.reply_text(
            """
━━━━━━━━━━━━━━━━━━━━
📄 إدارة الامتحانات السابقة
━━━━━━━━━━━━━━━━━━━━

اختر العملية التي تريد تنفيذها:

━━━━━━━━━━━━━━━━━━━━
🚀 UniX2
💡 نظامك الجامعي الذكي
""",
            reply_markup=exams_admin_menu()
        )

        return

    # =====================================================
    # عرض الملخصات
    # =====================================================

    elif text == "📂 عرض الملخصات":

        clear_user_states(context)

        context.user_data["viewing_summary"] = True

        await update.message.reply_text(
            """
━━━━━━━━━━━━━━━━━━━━
📂 عرض الملخصات
━━━━━━━━━━━━━━━━━━━━

📚 اختر المادة التي تريد عرض ملخصاتها:

━━━━━━━━━━━━━━━━━━━━
🚀 UniX2
💡 نظامك الجامعي الذكي
""",
            reply_markup=subjects_summary_menu()
        )

        return

    # =====================================================
    # حذف ملخص
    # =====================================================

    elif text == "❌ حذف ملخص":

        clear_user_states(context)

        context.user_data["deleting_summary"] = True

        await update.message.reply_text(
            """
━━━━━━━━━━━━━━━━━━━━
❌ حذف ملخص
━━━━━━━━━━━━━━━━━━━━

📚 اختر المادة التي تريد حذف ملخص منها:

━━━━━━━━━━━━━━━━━━━━
🚀 UniX2
💡 نظامك الجامعي الذكي
""",
            reply_markup=subjects_summary_menu()
        )

        return

    # =====================================================
    # اختيار مادة
    # =====================================================

    elif text in [
        "🗄️ أساسيات قواعد البيانات",
        "💻 معمارية وتنظيم الحاسوب",
        "☕ البرمجة الكائنية التوجه (Java)",
        "🌐 شبكات الحاسوب",
        "🎨 تصميم الويب 1",
        "🗣️ مهارات الاتصال",
        "🇾🇪 ثقافة وطنية",
    ]:

        # -------------------------------------------------
        # الامتحانات
        # -------------------------------------------------

        if context.user_data.get("viewing_exam"):

            context.user_data["exam_subject"] = text

            exams = get_exams(text)

            if not exams:

                await update.message.reply_text(
                    f"""
━━━━━━━━━━━━━━━━━━━━
📄 امتحانات المادة
━━━━━━━━━━━━━━━━━━━━

📚 المادة:
{text}

⚠️ لا توجد امتحانات مضافة لهذه المادة حالياً.

━━━━━━━━━━━━━━━━━━━━
🚀 UniX2
"""
                )

                return

            exam_list = []

            for exam_name, file_id in exams:
                exam_list.append(exam_name)

            await update.message.reply_text(
                f"""
━━━━━━━━━━━━━━━━━━━━
📄 امتحانات المادة
━━━━━━━━━━━━━━━━━━━━

📚 المادة:
{text}

اختر الامتحان الذي تريد فتحه 👇

━━━━━━━━━━━━━━━━━━━━
🚀 UniX2
💡 نظامك الجامعي الذكي
""",
                reply_markup=exams_menu(exam_list)
            )

            return

        # -------------------------------------------------
        # إضافة تكليف
        # -------------------------------------------------

        if context.user_data.get("adding_assignment"):

            context.user_data["assignment_subject"] = text

            await update.message.reply_text(
                f"📚 المادة: {text}\n\n"
                "📝 أرسل اسم التكليف وتاريخ التسليم بهذا الشكل:\n\n"
                "اسم التكليف | تاريخ التسليم\n\n"
                "مثال:\n"
                "حل الأسئلة 1-10 | الخميس"
            )

            return


        # -------------------------------------------------
        # إضافة ملخص
        # -------------------------------------------------

        if context.user_data.get("adding_summary"):

            context.user_data["subject"] = text

            await update.message.reply_text(
                f"""
━━━━━━━━━━━━━━━━━━━━
📖 اختيار المحاضرة
━━━━━━━━━━━━━━━━━━━━

📚 المادة:
{text}

اختر المحاضرة التي تريد إضافة ملخص لها 👇

━━━━━━━━━━━━━━━━━━━━
🚀 UniX2
💡 نظامك الجامعي الذكي
""",
                reply_markup=lectures_summary_menu()
            )

            return

        # -------------------------------------------------
        # حذف ملخص
        # -------------------------------------------------

        if context.user_data.get("deleting_summary"):

            context.user_data["subject"] = text

            summaries = get_summaries(text)

            lectures = []

            for lecture, file_id in summaries:
                lectures.append(lecture)

            if not lectures:

                await update.message.reply_text(
                    f"""
━━━━━━━━━━━━━━━━━━━━
❌ حذف ملخص
━━━━━━━━━━━━━━━━━━━━

📚 المادة:
{text}

⚠️ لا توجد ملخصات لهذه المادة.

━━━━━━━━━━━━━━━━━━━━
🚀 UniX2
""",
                    reply_markup=subjects_summary_menu()
                )

                return

            await update.message.reply_text(
                f"""
━━━━━━━━━━━━━━━━━━━━
❌ حذف ملخص
━━━━━━━━━━━━━━━━━━━━

📚 المادة:
{text}

اختر المحاضرة التي تريد حذفها 👇

━━━━━━━━━━━━━━━━━━━━
🚀 UniX2
💡 نظامك الجامعي الذكي
""",
                reply_markup=view_summaries_menu(lectures)
            )

            return

        # -------------------------------------------------
        # عرض ملخصات المادة
        # -------------------------------------------------

        if context.user_data.get("viewing_summary"):

            context.user_data["subject"] = text

            summaries = get_summaries(text)

            lectures = []

            for lecture, file_id in summaries:
                lectures.append(lecture)

            if summaries:

                message = (
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "📚 ملخصات المادة\n"
                    "━━━━━━━━━━━━━━━━━━━━\n\n"
                    f"📖 المادة: {text}\n\n"
                    "📂 الملخصات المتوفرة:\n\n"
                )

                for lecture, file_id in summaries:
                    message += f"• {lecture}\n"

                message += (
                    "\n━━━━━━━━━━━━━━━━━━━━\n"
                    "🚀 UniX2\n"
                    "💡 نظامك الجامعي الذكي"
                )

            else:

                message = (
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "📚 ملخصات المادة\n"
                    "━━━━━━━━━━━━━━━━━━━━\n\n"
                    f"📖 المادة: {text}\n\n"
                    "⚠️ لا توجد ملخصات مضافة لهذه المادة حالياً.\n\n"
                    "🔔 سيتم إضافة الملخصات قريباً.\n\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "🚀 UniX2"
                )

            await update.message.reply_text(
                message,
                reply_markup=view_summaries_menu(lectures)
            )

            return

    # =====================================================
    # أزرار المحاضرات
    # =====================================================

    elif text in [
        "1️⃣ المحاضرة الأولى",
        "2️⃣ المحاضرة الثانية",
        "3️⃣ المحاضرة الثالثة",
        "4️⃣ المحاضرة الرابعة",
        "5️⃣ المحاضرة الخامسة",
        "6️⃣ المحاضرة السادسة",
        "7️⃣ المحاضرة السابعة",
    ]:

        # -------------------------------------------------
        # عرض الملخص
        # -------------------------------------------------

        if context.user_data.get("viewing_summary"):

            subject = context.user_data.get("subject")

            summaries = get_summaries(subject)

            for lecture, file_id in summaries:

                if lecture == text:

                    await update.message.reply_document(
                        file_id,
                        caption=f"""
━━━━━━━━━━━━━━━━━━━━
📚 ملخص المادة
━━━━━━━━━━━━━━━━━━━━

📖 المادة:
{subject}

📎 المحاضرة:
{lecture}

━━━━━━━━━━━━━━━━━━━━
🚀 UniX2
💡 نظامك الجامعي الذكي
"""
                    )

                    return

            await update.message.reply_text(
                "⚠️ لم يتم العثور على ملف هذه المحاضرة."
            )

            return

        # -------------------------------------------------
        # حذف ملخص
        # -------------------------------------------------

        if context.user_data.get("deleting_summary"):

            subject = context.user_data.get("subject")

            delete_summary_by_subject(
                subject,
                text
            )

            await update.message.reply_text(
                f"""
━━━━━━━━━━━━━━━━━━━━
✅ تم حذف الملخص بنجاح
━━━━━━━━━━━━━━━━━━━━

📚 المادة:
{subject}

📖 المحاضرة:
{text}

━━━━━━━━━━━━━━━━━━━━
🚀 UniX2
💡 نظامك الجامعي الذكي
"""
            )

            context.user_data["deleting_summary"] = False
            context.user_data["subject"] = None

            return

        # -------------------------------------------------
        # إضافة ملخص
        # -------------------------------------------------

        if context.user_data.get("adding_summary"):

            context.user_data["lecture"] = text

            await update.message.reply_text(
                """
━━━━━━━━━━━━━━━━━━━━
📎 رفع الملخص
━━━━━━━━━━━━━━━━━━━━

أرسل ملف الملخص الآن:

✅ PDF
✅ DOC
✅ DOCX

━━━━━━━━━━━━━━━━━━━━
🚀 UniX2
💡 نظامك الجامعي الذكي
"""
            )

            return

    elif text == "🔙 العودة" and context.user_data.get("viewing_exam"):
        context.user_data.pop("viewing_exam", None)
        context.user_data.pop("exam_subject", None)
        await update.message.reply_text(
            "📄 اختر المادة التي تريد عرض امتحاناتها:",
            reply_markup=subjects_exam_menu()
        )
        return

    # =====================================================
    # فتح امتحان
    # =====================================================

    elif context.user_data.get("viewing_exam"):

        subject = context.user_data.get("exam_subject")

        exams = get_exams(subject)

        for exam_name, file_id in exams:

            if exam_name == text:

                await update.message.reply_document(
                    file_id,
                    caption=f"""
━━━━━━━━━━━━━━━━━━━━
📄 الامتحان السابق
━━━━━━━━━━━━━━━━━━━━

📚 المادة:
{subject}

📝 الامتحان:
{exam_name}

━━━━━━━━━━━━━━━━━━━━
🚀 UniX2
💡 نظامك الجامعي الذكي
"""
                )

                return

        await update.message.reply_text(
            "⚠️ لم يتم العثور على ملف الامتحان."
        )

        return

    # =====================================================
    # العودة من شاشة الامتحانات إلى المواد
    # =====================================================

    elif text == "🔙 العودة للمواد":

        if context.user_data.get("viewing_exam"):

            context.user_data["viewing_exam"] = True
            context.user_data.pop("exam_subject", None)

            await update.message.reply_text(
                """
━━━━━━━━━━━━━━━━━━━━
📄 الامتحانات السابقة
━━━━━━━━━━━━━━━━━━━━

📚 اختر المادة التي تريد عرض امتحاناتها:

━━━━━━━━━━━━━━━━━━━━
🚀 UniX2
💡 نظامك الجامعي الذكي
""",
                reply_markup=subjects_exam_menu()
            )

            return

        if (
            context.user_data.get("viewing_summary")
            or context.user_data.get("deleting_summary")
            or context.user_data.get("adding_summary")
        ):

            await update.message.reply_text(
                """
━━━━━━━━━━━━━━━━━━━━
📚 اختر المادة:

━━━━━━━━━━━━━━━━━━━━
🚀 UniX2
💡 نظامك الجامعي الذكي
""",
                reply_markup=subjects_summary_menu()
            )

            return

    # =====================================================
    # العودة من اختيار المادة
    # =====================================================

    elif text == "🔙 العودة":

        clear_user_states(context)

        await update.message.reply_text(
            "🏠 تم الرجوع إلى القائمة الرئيسية.",
            reply_markup=main_menu()
        )

        return

    # =====================================================
    # العودة للوحة الإدارة
    # =====================================================

    elif text == "🔙 العودة للوحة الإدارة":

        clear_user_states(context)

        await update.message.reply_text(
            "🔐 تم الرجوع إلى لوحة الإدارة.",
            reply_markup=admin_menu()
        )

        return

    # =====================================================
    # العودة للقائمة الرئيسية
    # =====================================================

    elif text == "🔙 العودة للقائمة الرئيسية":

        clear_user_states(context)

        await update.message.reply_text(
            "🏠 تم الرجوع إلى القائمة الرئيسية.",
            reply_markup=main_menu()
        )

        return


    # =====================================================
    # إدارة التكاليف
    # =====================================================

    elif text == "📝 إدارة التكاليف":
        clear_user_states(context)
        context.user_data["adding_assignment"] = True
        await update.message.reply_text(
            "📚 اختر المادة التي تريد إضافة تكليف لها:",
            reply_markup=subjects_summary_menu()
        )

        return

    # =====================================================
    # إدارة الإعلانات
    # =====================================================

    elif text == "📢 إدارة الإعلانات":
        clear_user_states(context)
        context.user_data["adding_announcement"] = True
        await update.message.reply_text(
            "📢 أرسل نص الإعلان الذي تريد نشره للطلاب:"
        )

        return
    # =====================================================
    # إدارة الدوام
    # =====================================================

    elif text == "⏰ إدارة الدوام":
        clear_user_states(context)
        context.user_data["adding_attendance"] = True
        await update.message.reply_text(
            "⏰ أرسل تفاصيل الدوام كاملة كرسالة واحدة.\n\n"
            "📌 يمكن أن تحتوي على محاضرة أو اثنتين أو ثلاث.\n\n"
            "المثال:\n\n"
            "الأربعاء 2026/9/9م\n"
            "━━━━━━━━━━━━━━━━\n\n"
            "🔹 المحاضرة الأولى:\n"
            "📖 المقرر: ...\n"
            "👨‍🏫 الدكتور: ...\n"
            "🕒 الوقت: ...\n"
            "🏛️ المكان: ...\n\n"
            "━━━━━━━━━━━━━━━━\n"
            "دمتم سالمين"
        )

        return



    # =====================================================
    # إدارة أماكن القاعات
    # =====================================================

    elif text == "📍 إدارة أماكن القاعات":
        clear_user_states(context)
        context.user_data["adding_room"] = True
        await update.message.reply_text(
            "📍 أرسل اسم القاعة والمبنى والدور بهذا الشكل:\n\n"
            "اسم القاعة | المبنى | الدور\n\n"
            "مثال:\n"
            "المدرج 6 | المبنى القديم | الثاني"
        )

        return

    # =====================================================
    # إدارة الطلاب
    # =====================================================

    elif text == "👥 إدارة الطلاب":
        clear_user_states(context)
        from database.queries import get_all_users, count_users

        total = count_users()
        users = get_all_users()

        message = "👥 إدارة الطلاب\n\n"
        message += f"📊 عدد الطلاب المسجلين: {total}\n\n"

        for user in users[:20]:
            message += f"• {user[2]} - {user[3]}\n"

        await update.message.reply_text(message)

        return
    
    # =====================================================
    # النسخ الاحتياطي
    # =====================================================

    elif text == "💾 النسخ الاحتياطي":
        clear_user_states(context)
        from utils.backup import create_backup
        backup_file = create_backup()

        if backup_file:
            await update.message.reply_text(f"✅ تم إنشاء نسخة احتياطية:\n{backup_file.name}")
        else:
           await update.message.reply_text("❌ فشل إنشاء النسخة الاحتياطية.")

        return

    # =====================================================
    # إعدادات النظام
    # =====================================================

    elif text == "⚙️ إعدادات النظام":
        clear_user_states(context)
        await update.message.reply_text(
            "⚙️ إعدادات النظام\n\n"
            "✅ اسم النظام: UniX2\n"
            "✅ الإصدار: 2.0\n"
            "✅ الحالة: يعمل"
        )
    
        return

    # =====================================================
    # استقبال اسم التكليف وتاريخ التسليم
    # =====================================================

    elif context.user_data.get("adding_assignment") and context.user_data.get("assignment_subject"):

       from database.queries import add_assignment

       parts = text.split("|")

       title = parts[0].strip() if len(parts) > 0 else text
       deadline = parts[1].strip() if len(parts) > 1 else ""

       subject = context.user_data.get("assignment_subject")

       add_assignment(subject, title, "", deadline, None, str(update.effective_user.id))

       await update.message.reply_text(
           f"✅ تم حفظ التكليف بنجاح\n\n"
           f"📚 المادة: {subject}\n"
           f"📝 التكليف: {title}\n"
           f"📅 التسليم: {deadline}"
        )

       context.user_data.pop("adding_assignment", None)
       context.user_data.pop("assignment_subject", None)

       return


    # =====================================================
    # استقبال رسالة الدوام كاملة
    # =====================================================

    elif context.user_data.get("adding_attendance"):

        from database.queries import add_attendance

        add_attendance(
            day="اليوم",
            status="مفعل",
            subject="",
            time="",
            location="",
            details=text,
        )

        await update.message.reply_text(
            "✅ تم حفظ الدوام بنجاح\n\n"
            "📢 سيظهر للطلاب في زر ⏰ الدوام"
        )

        context.user_data.pop("adding_attendance", None)

        return


    # =====================================================
    # زر غير معروف
    # =====================================================

    else:

        await update.message.reply_text(
            "⚡ اختر أحد الخيارات من القائمة."
        )

    