import sqlite3

conn = sqlite3.connect("database/resume_ai.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE jobs ADD COLUMN responsibilities TEXT")
    print("✅ Added 'responsibilities' column to 'jobs' table.")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("ℹ️ Column 'responsibilities' already exists.")
    else:
        print("❌ Error updating schema:", e)

conn.commit()
conn.close()
