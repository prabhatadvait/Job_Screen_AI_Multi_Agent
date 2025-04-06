# resume_matcher.py

from PyPDF2 import PdfReader
import sqlite3
import json
import subprocess
import os

def extract_resume_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def get_latest_jd_from_db():
    conn = sqlite3.connect("database/resume_ai.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    
    print("🧾 Latest job row fetched from DB:", row)
    
    if row:
        return {
            "title": row[1],
            "jd_text": row[2],
            "skills": row[3],
            "experience": row[4],
            "qualifications": row[5],
            "responsibilities": row[6] if len(row) > 6 else "",  # 🛡️ Safe fallback
        }
    else:
        return {}

def ensure_job_exists():
    conn = sqlite3.connect("database/resume_ai.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM jobs")
    count = cursor.fetchone()[0]

    if count == 0:
        print("⚠️ No jobs found. Inserting dummy job...")
        cursor.execute("""
            INSERT INTO jobs (title, jd_text, skills, experience, qualifications, responsibilities)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            "Software Engineer II",
            "Looking for a skilled engineer in Python, SQL, cloud technologies like AWS.",
            "Python, SQL, AWS",
            "2+ years",
            "Bachelor's in CS",
            "Responsible for developing scalable software systems."
        ))
        conn.commit()
        print("✅ Dummy job inserted.")
    conn.close()

def ensure_candidate_exists(resume_text):
    conn = sqlite3.connect("database/resume_ai.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM candidates")
    count = cursor.fetchone()[0]

    if count == 0:
        print("⚠️ No candidates found. Inserting dummy candidate...")
        cursor.execute("""
            INSERT INTO candidates (name, resume_text, skills, experience, education, certifications)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            "Prabhat Kumar",
            resume_text,
            "Python, SQL, Data Analysis",
            "2 years in data analysis",
            "B.Tech in CSE",
            "Azure Data Fundamentals"
        ))
        conn.commit()
        print("✅ Dummy candidate inserted.")
    conn.close()

def get_latest_ids():
    conn = sqlite3.connect("database/resume_ai.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM jobs ORDER BY id DESC LIMIT 1")
    job_row = cursor.fetchone()
    if not job_row:
        conn.close()
        raise Exception("⚠️ No job records found in the database.")
    job_id = job_row[0]

    cursor.execute("SELECT id FROM candidates ORDER BY id DESC LIMIT 1")
    candidate_row = cursor.fetchone()
    if not candidate_row:
        conn.close()
        raise Exception("⚠️ No candidate records found in the database.")
    candidate_id = candidate_row[0]

    conn.close()
    return job_id, candidate_id

def save_match_to_db(job_id, candidate_id, match_score):
    conn = sqlite3.connect("database/resume_ai.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO matches (job_id, candidate_id, match_score)
        VALUES (?, ?, ?)
    """, (job_id, candidate_id, match_score))
    conn.commit()
    conn.close()
    print("💾 Match result saved to database!")

def call_ollama_for_match(jd_dict, resume_text):
    prompt = f"""
Compare the following job description and resume. Give a match score out of 100, 
and explain why the score was given.

Job Description:
{json.dumps(jd_dict, indent=2)}

Resume:
{resume_text}

Return the result in JSON format like:
{{
  "match_score": 85,
  "summary": "The candidate meets most of the required skills and experience...",
  "missing_skills": ["Docker", "Kubernetes"]
}}
"""
    result = subprocess.run(
        ["ollama", "run", "mistral"],
        input=prompt.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    output = result.stdout.decode("utf-8").strip()
    try:
        json_start = output.index("{")
        parsed = json.loads(output[json_start:])
        return parsed
    except Exception as e:
        print("❌ Failed to parse Ollama output:", e)
        print("🔍 Raw Output START:\n", output, "\n🔍 Raw Output END")
        return None

if __name__ == "__main__":
    resume_path = "resume.pdf"  # Make sure it's in the same folder or use full path
    resume_text = extract_resume_text(resume_path)
    print("📄 Resume extracted.")

    jd = get_latest_jd_from_db()
    if not jd:
        ensure_job_exists()
        jd = get_latest_jd_from_db()

    print("🤖 Matching resume with JD using Mistral...")
    result = call_ollama_for_match(jd, resume_text)

    if result:
        print("\n✅ Match Result:")
        print(json.dumps(result, indent=2))

        ensure_candidate_exists(resume_text)
        ensure_job_exists()
        job_id, candidate_id = get_latest_ids()
        save_match_to_db(job_id, candidate_id, result["match_score"])
    else:
        print("❌ Matching failed.")
