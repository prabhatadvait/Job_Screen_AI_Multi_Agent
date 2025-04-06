import subprocess
import json
import sqlite3

def query_ollama(jd_text):
    prompt = f"""
Summarize the following Job Description and extract the following details:
1. Job Title
2. Required Skills (comma-separated)
3. Experience
4. Qualifications
5. Responsibilities (summarized)

Only respond in the following JSON format:

{{
  "title": "...",
  "skills": "...",
  "experience": "...",
  "qualifications": "...",
  "responsibilities": "..."
}}

Job Description:
\"\"\"{jd_text}\"\"\"
"""
    result = subprocess.run(
        ["ollama", "run", "mistral"], 
        input=prompt.encode(),
        capture_output=True
    )
    return result.stdout.decode()

def insert_into_db(data, jd_text):
    conn = sqlite3.connect("database/resume_ai.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO jobs (title, jd_text, skills, experience, qualifications, responsibilities)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (data["title"], jd_text, data["skills"], data["experience"], data["qualifications"], data["responsibilities"]))
    conn.commit()
    conn.close()

def run_jd_summarizer():
    jd_text = input("Paste the full Job Description:\n")

    print("\n⏳ Extracting with Ollama...\n")
    raw_output = query_ollama(jd_text)

    try:
        structured_data = json.loads(raw_output)
        print("✅ Extracted Info:\n")
        for key, value in structured_data.items():
            print(f"{key.title()}: {value}")

        insert_into_db(structured_data, jd_text)
        print("\n💾 JD saved in database!")
    except Exception as e:
        print("❌ Failed to parse JSON or insert into DB:", e)
        print("🔍 Raw Output START:\n", repr(raw_output), "\n🔍 Raw Output END")

if __name__ == "__main__":
    run_jd_summarizer()
