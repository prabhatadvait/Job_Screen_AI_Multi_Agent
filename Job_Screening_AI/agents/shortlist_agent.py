import sqlite3

DB_PATH = "database/resume_ai.db"
SHORTLIST_THRESHOLD = 70  # Set threshold for shortlisting

def get_latest_match():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT matches.id, match_score, jobs.title, candidates.name, candidates.email
        FROM matches
        JOIN jobs ON matches.job_id = jobs.id
        JOIN candidates ON matches.candidate_id = candidates.id
        ORDER BY matches.id DESC LIMIT 1
    """)
    result = cursor.fetchone()
    conn.close()
    return result  # (match_id, score, job_title, candidate_name, email)

def shortlist_decision(score):
    return "Shortlisted ✅" if score >= SHORTLIST_THRESHOLD else "Rejected ❌"

def generate_email(candidate_name, job_title):
    return f"""
📧 Generated Interview Invitation Email:

Subject: Interview Invitation for {job_title}

Dear {candidate_name},

We are pleased to inform you that based on your profile and our job description for the role of *{job_title}*, you have been shortlisted for the next round of interviews.

Please reply to this email with your availability for a virtual interview this week.

Best regards,  
HR Team
"""

if __name__ == "__main__":
    print("🤖 Evaluating latest candidate for shortlisting...")

    match_data = get_latest_match()

    if match_data:
        match_id, score, job_title, candidate_name, email = match_data
        decision = shortlist_decision(score)

        print(f"\n📌 Job Title      : {job_title}")
        print(f"👤 Candidate Name : {candidate_name}")
        print(f"📊 Match Score    : {score}%")
        print(f"📥 Final Decision : {decision}")

        if decision.startswith("Shortlisted"):
            email_content = generate_email(candidate_name, job_title)
            print(email_content)
    else:
        print("⚠️ No match records found in the database.")
