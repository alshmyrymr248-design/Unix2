from datetime import datetime


# =========================================================
# تنسيق التاريخ والوقت
# =========================================================

def current_datetime():
    """إرجاع التاريخ والوقت الحالي"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def current_date():
    """إرجاع التاريخ الحالي فقط"""
    return datetime.now().strftime("%Y-%m-%d")


def current_time():
    """إرجاع الوقت الحالي فقط"""
    return datetime.now().strftime("%H:%M:%S")


# =========================================================
# تنظيف النصوص
# =========================================================

def clean_text(text):
    """تنظيف النص من المسافات الزائدة"""
    if not text:
        return ""

    return " ".join(str(text).strip().split())


def title_case(text):
    """تحويل النص إلى صيغة عنوان"""
    if not text:
        return ""

    return clean_text(text).title()


# =========================================================
# التحقق من امتداد الملفات
# =========================================================

def is_allowed_file(filename):
    """التحقق من نوع الملف المسموح به"""
    if not filename:
        return False

    allowed_extensions = (
        ".pdf",
        ".doc",
        ".docx",
    )

    return filename.lower().endswith(allowed_extensions)


def get_file_extension(filename):
    """استخراج امتداد الملف"""
    if not filename:
        return ""

    return filename.lower().rsplit(".", 1)[-1] if "." in filename else ""


# =========================================================
# التحقق من الأرقام
# =========================================================

def is_number(value):
    """التحقق مما إذا كانت القيمة رقمًا"""
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False


def to_int(value, default=0):
    """تحويل القيمة إلى رقم صحيح بأمان"""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


# =========================================================
# تنسيق حجم الملفات
# =========================================================

def format_file_size(size_bytes):
    """تحويل حجم الملف من بايت إلى صيغة مقروءة"""
    if not size_bytes:
        return "0 KB"

    size_bytes = float(size_bytes)

    if size_bytes < 1024:
        return f"{size_bytes:.0f} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"


# =========================================================
# الوقت النسبي
# =========================================================

def time_ago(datetime_string):
    """تحويل الوقت إلى صيغة نسبية مثل: منذ 5 دقائق"""
    try:
        past = datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        diff = now - past

        seconds = diff.total_seconds()

        if seconds < 60:
            return "منذ لحظات"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            return f"منذ {minutes} دقيقة"
        elif seconds < 86400:
            hours = int(seconds // 3600)
            return f"منذ {hours} ساعة"
        else:
            days = int(seconds // 86400)
            return f"منذ {days} يوم"

    except (ValueError, TypeError):
        return datetime_string


# =========================================================
# تقسيم الرسائل الطويلة
# =========================================================

def split_message(text, max_length=4000):
    """تقسيم النص الطويل إلى أجزاء مناسبة لتيليجرام"""
    if not text:
        return []

    if len(text) <= max_length:
        return [text]

    parts = []
    current = ""

    for line in text.split("\n"):
        if len(current) + len(line) + 1 > max_length:
            if current:
                parts.append(current)
            current = line
        else:
            if current:
                current += "\n"
            current += line

    if current:
        parts.append(current)

    return parts
