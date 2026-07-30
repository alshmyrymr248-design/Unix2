from database.database import get_connection


def add_summary(subject, lecture, file_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM summaries
        WHERE subject = ? AND lecture = ?
        """,
        (subject, lecture)
    )

    cursor.execute(
        """
        INSERT INTO summaries (subject, lecture, file_id)
        VALUES (?, ?, ?)
        """,
        (subject, lecture, file_id)
    )

    conn.commit()
    conn.close()



def get_summaries(subject):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT DISTINCT lecture, file_id
        FROM summaries
        WHERE subject = ?
        ORDER BY lecture
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
