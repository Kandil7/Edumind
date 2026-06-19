import sqlite3
conn = sqlite3.connect("edumind.db")
c = conn.cursor()
c.execute("UPDATE students SET id='00000000-0000-0000-0000-000000000001' WHERE email='demo@edumind.com'")
conn.commit()
c.execute("SELECT id, email FROM students")
for row in c.fetchall():
    print(f"id={row[0]} email={row[1]}")
conn.close()
