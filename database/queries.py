from database.database import get_connection


# =========================================================
# الملخصات
# =========================================================

def add_summary(subject, lecture, file_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO summaries (subject, lecture, file_id)
        VALUES (?, ?, ?)
        ON CONFLICT(subject, lecture)
        DO UPDATE SET file_id = excluded.file_id
        """,
        (subject, lecture, file_id),
    )

    conn.commit()
    conn.close()


def get_summaries(subject):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT lecture, file_id
        FROM summaries
        WHERE subject = ?
        ORDER BY id ASC
        """,
        (subject,),
    )

    data = cursor.fetchall()

    conn.close()

    return [(row["lecture"], row["file_id"]) for row in data]


def delete_summary(summary_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM summaries
        WHERE id = ?
        """,
        (summary_id,),
    )

    conn.commit()
    conn.close()


def delete_summary_by_subject(subject, lecture):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM summaries
        WHERE subject = ? AND lecture = ?
        """,
        (subject, lecture),
    )

    conn.commit()
    conn.close()


# =========================================================
# الامتحانات السابقة
# =========================================================

def add_exam(subject, exam_name, file_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO exams (subject, exam_name, file_id)
        VALUES (?, ?, ?)
        ON CONFLICT(subject, exam_name)
        DO UPDATE SET file_id = excluded.file_id
        """,
        (subject, exam_name, file_id),
    )

    conn.commit()
    conn.close()


def get_exams(subject):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT exam_name, file_id
        FROM exams
        WHERE subject = ?
        ORDER BY id ASC
        """,
        (subject,),
    )

    data = cursor.fetchall()

    conn.close()

    return [(row["exam_name"], row["file_id"]) for row in data]


def delete_exam_by_subject(subject, exam_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM exams
        WHERE subject = ? AND exam_name = ?
        """,
        (subject, exam_name),
    )

    conn.commit()
    conn.close()


# =========================================================
# الإعلانات
# =========================================================

def add_announcement(title, content, created_by=""):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO announcements (title, content, created_by)
        VALUES (?, ?, ?)
        """,
        (title, content, created_by),
    )

    announcement_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return announcement_id


def get_announcements():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, title, content, created_by, created_at
        FROM announcements
        ORDER BY id DESC
        """
    )

    data = cursor.fetchall()

    conn.close()

    return [
        (
            row["id"],
            row["title"],
            row["content"],
            row["created_by"],
            row["created_at"],
        )
        for row in data
    ]


def delete_announcement(announcement_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM announcements
        WHERE id = ?
        """,
        (announcement_id,),
    )

    conn.commit()
    conn.close()


# =========================================================
# الدوام
# =========================================================

def add_attendance(day, status, subject="", time="", location="", details=""):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO attendance (day, status, subject, time, location, details)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (day, status, subject, time, location, details),
    )

    attendance_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return attendance_id


def get_attendance():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, day, status, subject, time, location, details, created_at
        FROM attendance
        ORDER BY id DESC
        """
    )

    data = cursor.fetchall()

    conn.close()

    return [
        (
            row["id"],
            row["day"],
            row["status"],
            row["subject"],
            row["time"],
            row["location"],
            row["details"],
            row["created_at"],
        )
        for row in data
    ]


def delete_attendance(attendance_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM attendance
        WHERE id = ?
        """,
        (attendance_id,),
    )

    conn.commit()
    conn.close()


# =========================================================
# القاعات
# =========================================================

def add_room(name, building="", floor="", details=""):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO rooms (name, building, floor, details)
        VALUES (?, ?, ?, ?)
        """,
        (name, building, floor, details),
    )

    room_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return room_id


def get_rooms():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, name, building, floor, details
        FROM rooms
        ORDER BY id ASC
        """
    )

    data = cursor.fetchall()

    conn.close()

    return [
        (
            row["id"],
            row["name"],
            row["building"],
            row["floor"],
            row["details"],
        )
        for row in data
    ]


def delete_room(room_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM rooms
        WHERE id = ?
        """,
        (room_id,),
    )

    conn.commit()
    conn.close()


# =========================================================
# الطلاب
# =========================================================

def add_student(name, student_id=None, phone="", department="", level=""):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO students
        (name, student_id, phone, department, level)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(student_id)
        DO UPDATE SET
            name = excluded.name,
            phone = excluded.phone,
            department = excluded.department,
            level = excluded.level
        """,
        (name, student_id, phone, department, level),
    )

    student_db_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return student_db_id


def get_students():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, name, student_id, phone, department, level
        FROM students
        ORDER BY id ASC
        """
    )

    data = cursor.fetchall()

    conn.close()

    return [
        (
            row["id"],
            row["name"],
            row["student_id"],
            row["phone"],
            row["department"],
            row["level"],
        )
        for row in data
    ]


def search_students(search_text):
    conn = get_connection()
    cursor = conn.cursor()

    search_pattern = f"%{search_text}%"

    cursor.execute(
        """
        SELECT id, name, student_id, phone, department, level
        FROM students
        WHERE name LIKE ?
           OR student_id LIKE ?
           OR phone LIKE ?
        ORDER BY name ASC
        """,
        (search_pattern, search_pattern, search_pattern),
    )

    data = cursor.fetchall()

    conn.close()

    return [
        (
            row["id"],
            row["name"],
            row["student_id"],
            row["phone"],
            row["department"],
            row["level"],
        )
        for row in data
    ]


def delete_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM students
        WHERE id = ?
        """,
        (student_id,),
    )

    conn.commit()
    conn.close()


# =========================================================
# التكاليف
# =========================================================

def add_assignment(subject, title, description="", deadline="", file_id=None, created_by=""):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO assignments
        (subject, title, description, deadline, file_id, created_by)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (subject, title, description, deadline, file_id, created_by),
    )

    assignment_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return assignment_id


def get_assignments(subject=None):
    conn = get_connection()
    cursor = conn.cursor()

    if subject:
        cursor.execute(
            """
            SELECT id, subject, title, description, deadline, file_id, created_by
            FROM assignments
            WHERE subject = ?
            ORDER BY id DESC
            """,
            (subject,),
        )
    else:
        cursor.execute(
            """
            SELECT id, subject, title, description, deadline, file_id, created_by
            FROM assignments
            ORDER BY id DESC
            """
        )

    data = cursor.fetchall()

    conn.close()

    return [
        (
            row["id"],
            row["subject"],
            row["title"],
            row["description"],
            row["deadline"],
            row["file_id"],
            row["created_by"],
        )
        for row in data
    ]


def delete_assignment(assignment_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM assignments
        WHERE id = ?
        """,
        (assignment_id,),
    )

    conn.commit()
    conn.close()


# =========================================================
# المستخدمون والأدوار
# =========================================================

def add_user(telegram_id, name="", role="student"):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO users (telegram_id, name, role)
        VALUES (?, ?, ?)
        ON CONFLICT(telegram_id)
        DO UPDATE SET
            name = excluded.name,
            role = excluded.role,
            updated_at = CURRENT_TIMESTAMP
        """,
        (str(telegram_id), name, role),
    )

    user_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return user_id


def get_user_by_telegram_id(telegram_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, telegram_id, name, role, is_active
        FROM users
        WHERE telegram_id = ?
        """,
        (str(telegram_id),),
    )

    user = cursor.fetchone()

    conn.close()

    if user:
        return {
            "id": user["id"],
            "telegram_id": user["telegram_id"],
            "name": user["name"],
            "role": user["role"],
            "is_active": user["is_active"],
        }

    return None


def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, telegram_id, name, role, is_active, created_at
        FROM users
        ORDER BY id ASC
        """
    )

    data = cursor.fetchall()

    conn.close()

    return [
        (
            row["id"],
            row["telegram_id"],
            row["name"],
            row["role"],
            row["is_active"],
            row["created_at"],
        )
        for row in data
    ]


def count_users():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total FROM users")
    result = cursor.fetchone()

    conn.close()

    return result["total"] if result else 0


def deactivate_user(telegram_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users
        SET is_active = 0, updated_at = CURRENT_TIMESTAMP
        WHERE telegram_id = ?
        """,
        (str(telegram_id),),
    )

    conn.commit()
    conn.close()


def activate_user(telegram_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users
        SET is_active = 1, updated_at = CURRENT_TIMESTAMP
        WHERE telegram_id = ?
        """,
        (str(telegram_id),),
    )

    conn.commit()
    conn.close()


# =========================================================
# النسخ الاحتياطي
# =========================================================

def get_table_counts():
    conn = get_connection()
    cursor = conn.cursor()

    tables = [
        "summaries",
        "exams",
        "announcements",
        "attendance",
        "rooms",
        "students",
        "assignments",
        "users",
    ]

    stats = {}

    for table in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) as total FROM {table}")
            result = cursor.fetchone()
            stats[table] = result["total"] if result else 0
        except:
            stats[table] = 0

    conn.close()

    return stats
