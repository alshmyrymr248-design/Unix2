import shutil
from datetime import datetime
from pathlib import Path


# =========================================================
# مسارات المشروع
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DB_FILE = BASE_DIR / "unix2.db"
BACKUP_DIR = BASE_DIR / "backups"


# =========================================================
# إنشاء نسخة احتياطية
# =========================================================

def create_backup():
    """إنشاء نسخة احتياطية من قاعدة البيانات"""

    try:
        BACKUP_DIR.mkdir(exist_ok=True)

        if not DB_FILE.exists():
            print("❌ قاعدة البيانات غير موجودة")
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        backup_file = BACKUP_DIR / f"unix2_backup_{timestamp}.db"

        shutil.copy2(DB_FILE, backup_file)

        print(f"✅ تم إنشاء النسخة الاحتياطية: {backup_file.name}")

        return backup_file

    except Exception as e:
        print(f"❌ خطأ في إنشاء النسخة الاحتياطية: {e}")
        return None


# =========================================================
# الحصول على النسخ الاحتياطية
# =========================================================

def get_backups():
    """جلب قائمة النسخ الاحتياطية المتاحة"""

    try:
        BACKUP_DIR.mkdir(exist_ok=True)

        backups = list(BACKUP_DIR.glob("unix2_backup_*.db"))

        backups.sort(
            key=lambda file: file.stat().st_mtime,
            reverse=True,
        )

        return backups

    except Exception as e:
        print(f"❌ خطأ في جلب النسخ الاحتياطية: {e}")
        return []


# =========================================================
# استعادة نسخة احتياطية
# =========================================================

def restore_backup(backup_file):
    """استعادة قاعدة البيانات من نسخة احتياطية"""

    try:
        backup_path = Path(backup_file)

        if not backup_path.exists():
            print("❌ النسخة الاحتياطية غير موجودة")
            return False

        # إنشاء نسخة أمان من قاعدة البيانات الحالية
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        safety_backup = BACKUP_DIR / f"before_restore_{timestamp}.db"

        if DB_FILE.exists():
            BACKUP_DIR.mkdir(exist_ok=True)
            shutil.copy2(DB_FILE, safety_backup)
            print(f"✅ تم إنشاء نسخة أمان: {safety_backup.name}")

        # استعادة النسخة المطلوبة
        shutil.copy2(backup_path, DB_FILE)

        print(f"✅ تمت استعادة النسخة: {backup_path.name}")

        return True

    except Exception as e:
        print(f"❌ خطأ في استعادة النسخة: {e}")
        return False


# =========================================================
# معلومات النسخة الاحتياطية
# =========================================================

def backup_info(backup_file):
    """جلب معلومات عن نسخة احتياطية معينة"""

    try:
        backup_path = Path(backup_file)

        if not backup_path.exists():
            return None

        stat = backup_path.stat()

        return {
            "name": backup_path.name,
            "size": stat.st_size,
            "created": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
        }

    except Exception as e:
        print(f"❌ خطأ في جلب معلومات النسخة: {e}")
        return None


# =========================================================
# عدد النسخ الاحتياطية
# =========================================================

def count_backups():
    """إرجاع عدد النسخ الاحتياطية المتاحة"""

    try:
        backups = get_backups()
        return len(backups)
    except:
        return 0


# =========================================================
# حذف النسخ الاحتياطية القديمة
# =========================================================

def delete_old_backups(max_backups=10):
    """حذف النسخ الاحتياطية القديمة مع الإبقاء على الأحدث"""

    try:
        backups = get_backups()

        if len(backups) <= max_backups:
            return 0

        deleted_count = 0

        for backup in backups[max_backups:]:
            backup.unlink()
            deleted_count += 1

        return deleted_count

    except Exception as e:
        print(f"❌ خطأ في حذف النسخ القديمة: {e}")
        return 0
