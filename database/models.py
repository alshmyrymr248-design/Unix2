from database.database import get_connection


# =========================================================
# إنشاء جداول قاعدة البيانات
# =========================================================

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # =====================================================
    # جدول المستخدمين (الأدوار والصلاحيات)
    # =====================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id TEXT UNIQUE NOT NULL,
            name TEXT,
            role TEXT DEFAULT 'student',
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # =====================================================
    # جدول الأدوار
    # =====================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # =====================================================
    # جدول الملخصات
    # =====================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            lecture TEXT NOT NULL,
            file_id TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(subject, lecture)
        )
        """
    )

    # =====================================================
    # جدول الامتحانات السابقة
    # =====================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            exam_name TEXT NOT NULL,
            file_id TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(subject, exam_name)
        )
        """
    )

    # =====================================================
    # جدول الإعلانات
    # =====================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS announcements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_by TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # =====================================================
    # جدول الدوام
    # =====================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day TEXT NOT NULL,
            subject TEXT,
            time TEXT,
            location TEXT,
            status TEXT NOT NULL,
            details TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # =====================================================
    # جدول القاعات
    # =====================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            building TEXT,
            floor TEXT,
            details TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # =====================================================
    # جدول الطلاب
    # =====================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            student_id TEXT UNIQUE,
            phone TEXT,
            department TEXT,
            level TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # =====================================================
    # جدول التكاليف
    # =====================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            deadline TEXT,
            file_id TEXT,
            created_by TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn.commit()
    conn.close()


# =========================================================
# تهيئة الأدوار الافتراضية
# =========================================================

def seed_roles():
    """
    إضافة الأدوار الافتراضية عند أول تشغيل.
    """
    conn = get_connection()
    cursor = conn.cursor()

    roles = [
        ("super_admin", "المسؤول الأعلى - يملك كافة الصلاحيات"),
        ("representative", "مندوب الدفعة - إعلانات وتنبيهات"),
        ("assignments_admin", "مسؤول التكاليف والواجبات"),
        ("student", "طالب - صلاحيات قراءة فقط"),
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO roles (name, description) VALUES (?, ?)",
        roles
    )

    conn.commit()
    conn.close()
