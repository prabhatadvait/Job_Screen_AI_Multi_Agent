import sqlite3

conn = sqlite3.connect("database/resume_ai.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE candidates ADD COLUMN email TEXT")
    print("✅ Added 'email' column to 'candidates' table.")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("ℹ️ Column 'email' already exists in 'candidates' table.")
    else:
        print("❌ Error updating schema:", e)

conn.commit()
conn.close()
