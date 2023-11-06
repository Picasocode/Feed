import sqlite3 as sql
con = sql.connect("database.db")
cur = con.cursor()
cur.execute("SELECT username, password FROM users")
users = cur.fetchall()
con.close()
print(users)