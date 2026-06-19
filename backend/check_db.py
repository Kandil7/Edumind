import sqlite3
conn = sqlite3.connect("edumind.db")
c = conn.cursor()
for t in ["students","lessons","concepts","skills","content_chunks"]:
    c.execute(f"SELECT COUNT(*) FROM {t}")
    print(f"{t}: {c.fetchone()[0]}")
conn.close()
