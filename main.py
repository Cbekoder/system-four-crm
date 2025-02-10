import sqlite3

conn = sqlite3.connect("db.sqlite3")

cursor = conn.cursor()

cursor.execute("DELETE FROM garden_gardenexpense")

conn.commit()

conn.close()


# from sqlite3 import connect
# with connect("db.sqlite3") as conn:
#     cursor=conn.cursor()
#     cursor.execute(
#         """
#         SELECT * FROM users_user
#         """
#     )
#     print(cursor.fetchall())