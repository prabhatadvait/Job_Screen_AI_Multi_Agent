
# 🧠 Job Screening AI

A Multi-Agent AI system to enhance recruitment by automating job description analysis, resume matching, shortlisting, and interview invitation generation.

## 🚀 Problem Statement

**Enhancing Job Screening with AI and Data Intelligence**

The recruitment process often involves manually reviewing numerous job descriptions (JDs) and CVs, which is time-consuming and prone to human error. This project aims to develop a multi-agent system that automates:
- 📄 JD summarization
- 📋 Resume extraction
- 📊 Candidate-to-job matching
- ✅ Shortlisting based on match score
- 📧 Interview invitation email generation

---

## 🧰 Project Structure

```
Job_Screening_AI/
├── agents/
│   ├── jd_summarizer.py
│   ├── resume_matcher.py
│   └── shortlist_agent.py
├── dashboard/
│   └── app.py
├── database/
│   ├── db_setup.py
│   └── resume_ai.db
├── logs/
├── resume.pdf
└── scripts/
    ├── update_db_schema.py
    └── update_schema_email.py
```

---

## 🧑‍💻 How It Works

### 1. JD Summarizer
Extracts and summarizes key information from job descriptions like responsibilities, required skills, and qualifications.

### 2. Resume Matcher
Parses resumes, extracts candidate details (skills, education, experience) and computes a match score against the JD.

### 3. Shortlist Agent
Compares the score to a threshold (e.g., 75%) and generates an interview decision + personalized email message.

### 4. Dashboard
A simple Flask-based dashboard to view shortlisted candidates and scores.

### 5. Batch Scheduling (🕒 Cron)
Use `cron` to automate the shortlisting pipeline periodically.

---

## 🛠️ Installation

```bash
git clone htttps://github.com/prabhatadvait/Job_Screen_AI_Multi_Agent.git
cd Job_Screening_AI
pip install -r requirements.txt
```

Or use Anaconda Python environment.

---

## 🖥️ Run Instructions

### Run Shortlisting Agent

```bash
python3 agents/shortlist_agent.py
```

### Launch Dashboard

```bash
cd dashboard
python3 app.py
```

Dashboard will be live at [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## ⏱️ Batch Scheduling with Cron

To schedule auto-shortlisting every 5 minutes:

```bash
crontab -e
```

Then add this line (update Python path as needed):

```
*/5 * * * * /home/prabhat/anaconda3/bin/python3 /home/prabhat/Project/Accenture/Job_Screening_AI/agents/shortlist_agent.py >> /home/prabhat/Project/Accenture/Job_Screening_AI/logs/cron.log 2>&1
```

---

## ✅ Next Steps

- [ ] SMTP Integration (send real interview emails)
- [x] Batch scheduling with Cron
- [x] Simple Flask dashboard
- [ ] Vector store integration (FAISS/Chroma for semantic search)
- [ ] Multi-resume + multi-JD support

---

## 📂 Database

Using SQLite for persistent memory.

- **Tables**: `jobs`, `candidates`, `matches`
- Schema updatable via `scripts/update_db_schema.py`

---

## 👨‍💻 Author

**Prabhat Kumar**  
[Portfolio](https://prabhatadvait.github.io/Portfolio_Website/) | [LinkedIn](https://www.linkedin.com/in/prabhat-kumar-1260a5259) | [GitHub](https://github.com/prabhatadvait)

---

## 📃 License

This project is for educational and hackathon purposes.

---
