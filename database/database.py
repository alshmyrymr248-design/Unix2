import sqlite3
from pathlib import Path

# =========================================================
# إعداد المسارات
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DB_NAME = BASE_DIR / "unix2.db"


# =========================================================
# إنشاء اتصال بقاعدة البيانات
# =========================================================

def get_connection():
    """
    إنشاء اتصال بقاعدة البيانات مع إعدادات أمان وأداء محسنة.
    """
    try:
        conn = sqlite3.connect(DB_NAME)

        # يسمح باستخدام أسماء الأعمدة بدل الأرقام
        conn.row_factory = sqlite3.Row

        # تفعيل دعم المفاتيح الخارجية
        conn.execute("PRAGMA foreign_keys = ON")

        # منع أخطاء التزامن عند الضغط المتزامن
        conn.execute("PRAGMA busy_timeout = 5000")

        return conn

    except sqlite3.Error as e:
        print(f"❌ Database connection error: {e}")
        raise


# =========================================================
# تهيئة قاعدة البيانات
# =========================================================

def init_db():
    """
    تهيئة قاعدة البيانات وإنشاء الاتصال الأولي.
    """
    conn = get_connection()
    try:
        # سيتم استدعاء create_tables من models.py لاحقًا
        from database.models import create_tables
        create_tables()
        print("✅ Database initialized successfully")
    finally:
        conn.close()
