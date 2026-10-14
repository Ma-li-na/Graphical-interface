#  Создание тестовой SQLite-базы для лабораторной работы №3.

import sqlite3

conn = sqlite3.connect("sample.db")
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id    INTEGER PRIMARY KEY,
        name  TEXT,
        grade INTEGER
    )
""")
cur.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        id    INTEGER PRIMARY KEY,
        title TEXT,
        hours INTEGER
    )
""")

cur.executemany(
    "INSERT INTO students (name, grade) VALUES (?, ?)",
    [("Алина", 5), ("Иван", 4), ("Мария", 5), ("Пётр", 3)]
)
cur.executemany(
    "INSERT INTO courses (title, hours) VALUES (?, ?)",
    [("PyQt", 36), ("SQL", 24), ("Python", 48)]
)

conn.commit()
conn.close()
print("sample.db успешно создана")