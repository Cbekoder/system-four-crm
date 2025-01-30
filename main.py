import sqlite3

conn = sqlite3.connect("db.sqlite3")

cursor = conn.cursor()

cursor.execute("DELETE FROM fridge_electricitybill")

conn.commit()

conn.close()