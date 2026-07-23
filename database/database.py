import sqlite3

DB_NAME = "unix2.db"


def get_connection():
    return sqlite3.connect(DB_NAME)
