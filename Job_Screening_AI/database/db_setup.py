import sqlite3

conn = sqlite3.connect("database/resume_ai.db")
cursor = conn.cursor()

# Create jobs table
cursor.execute("""
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    jd_text TEXT,
    skills TEXT,
    experience TEXT,
    qualifications TEXT,
    responsibilities TEXT
)
""")

# Create candidates table
cursor.execute("""
CREATE TABLE IF NOT EXISTS candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    resume_text TEXT,
    skills TEXT,
    experience TEXT,
    education TEXT,
    certifications TEXT
)
""")

# Create matches table
cursor.execute("""
CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER,
    candidate_id INTEGER,
    match_score REAL,
    FOREIGN KEY(job_id) REFERENCES jobs(id),
    FOREIGN KEY(candidate_id) REFERENCES candidates(id)
)
""")

conn.commit()
conn.close()

print("✅ Database and tables created successfully!")
