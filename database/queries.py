from database.database import get_connection


def add_summary(subject, title, file_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO summaries (subject, title, file_id)
        VALUES (?, ?, ?)
        """,
        (subject, title, file_id)
    )

    conn.commit()
    conn.close()


def get_summaries(subject):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT title, file_id
        FROM summaries
        WHERE subject = ?
        """,
        (subject,)
    )

    data = cursor.fetchall()

    conn.close()

    return data


def delete_summary(summary_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM summaries
        WHERE id = ?
        """,
        (summary_id,)
    )

    conn.commit()
    conn.close()
