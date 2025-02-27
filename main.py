import sqlite3

with sqlite3.connect("db.sqlite3") as connection:
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Jadvallar:", tables)
