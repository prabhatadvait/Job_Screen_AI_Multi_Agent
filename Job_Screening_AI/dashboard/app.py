from flask import Flask, render_template_string
import sqlite3

app = Flask(__name__)
DB_PATH = "database/resume_ai.db"
THRESHOLD = 75  # Shortlisting threshold


@app.route("/")
def index():
    # Connect to the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Fetch match results
    cursor.execute("""
        SELECT matches.id, jobs.title, candidates.name, match_score
        FROM matches
        JOIN jobs ON matches.job_id = jobs.id
        JOIN candidates ON matches.candidate_id = candidates.id
        ORDER BY matches.id DESC
    """)
    rows = cursor.fetchall()
    conn.close()

    # Prepare data for display
    data = [
        {
            "id": row[0],
            "job_title": row[1],
            "candidate_name": row[2],
            "score": row[3],
            "decision": "Shortlisted ✅" if row[3] >= THRESHOLD else "Rejected ❌",
            "status_class": "shortlisted" if row[3] >= THRESHOLD else "rejected"
        } for row in rows
    ]

    # Render the HTML using render_template_string
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Job Screening AI Dashboard</title>
        <style>
            body {
                font-family: 'Segoe UI', sans-serif;
                background-color: #f4f9fd;
                margin: 0;
                padding: 20px;
            }
            .header {
                background: #3a7bd5;
                color: white;
                padding: 20px;
                text-align: center;
                border-radius: 10px;
                margin-bottom: 30px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
            .header h1 {
                margin: 0;
                font-size: 36px;
            }
            .header p {
                margin-top: 8px;
                font-size: 18px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                box-shadow: 0 0 20px rgba(0,0,0,0.05);
                background: white;
                border-radius: 10px;
                overflow: hidden;
            }
            th, td {
                padding: 14px;
                border-bottom: 1px solid #ddd;
                text-align: center;
            }
            th {
                background-color: #edf4ff;
                font-weight: bold;
            }
            tr:hover {
                background-color: #f1faff;
            }
            .status {
                font-weight: bold;
            }
            .shortlisted {
                color: green;
            }
            .rejected {
                color: red;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🤖 Job Screening AI</h1>
            <p>Multi-Agent System for Smart Candidate Shortlisting</p>
        </div>
        <table>
            <tr>
                <th>ID</th>
                <th>Job Title</th>
                <th>Candidate</th>
                <th>Score (%)</th>
                <th>Status</th>
            </tr>
            {% for item in data %}
            <tr>
                <td>{{ item.id }}</td>
                <td>{{ item.job_title }}</td>
                <td>{{ item.candidate_name }}</td>
                <td>{{ item.score }}</td>
                <td class="status {{ item.status_class }}">{{ item.decision }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """, data=data)


@app.route("/agents")
def agents_view():
    agents_data = [
        {
            "name": "JobAnalysisAgent",
            "role": "Analyzes job description",
            "action": "Extracted keywords: ['Python', 'Machine Learning', 'SQL']",
            "icon": "🧠",
            "status": "success"
        },
        {
            "name": "ResumeParserAgent",
            "role": "Parses candidate resume",
            "action": "Extracted skills: ['Python', 'Deep Learning', 'NLP']",
            "icon": "📄",
            "status": "success"
        },
        {
            "name": "MatchScorerAgent",
            "role": "Scores resume against job",
            "action": "Calculated match score: 85%",
            "icon": "📊",
            "status": "success"
        },
        {
            "name": "DecisionAgent",
            "role": "Final decision maker",
            "action": "Candidate is shortlisted ✅",
            "icon": "🤖",
            "status": "success"
        }
    ]

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Agents Interaction</title>
        <style>
            body {
                font-family: 'Segoe UI', sans-serif;
                background-color: #f4f9fd;
                margin: 0;
                padding: 30px;
            }
            h1 {
                text-align: center;
                color: #2c3e50;
                margin-bottom: 40px;
            }
            .timeline {
                display: flex;
                gap: 20px;
                overflow-x: auto;
                padding-bottom: 20px;
            }
            .agent-card {
                min-width: 280px;
                background: white;
                border-radius: 12px;
                padding: 20px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.05);
                border-left: 6px solid #3498db;
                position: relative;
                transition: transform 0.3s ease;
            }
            .agent-card:hover {
                transform: translateY(-5px);
            }
            .icon {
                font-size: 32px;
                margin-bottom: 10px;
            }
            .name {
                font-weight: bold;
                font-size: 20px;
                color: #34495e;
            }
            .role {
                font-size: 14px;
                color: #7f8c8d;
                margin-bottom: 10px;
            }
            .action {
                font-size: 16px;
                margin-bottom: 10px;
                color: #2c3e50;
            }
            .status.success {
                color: green;
            }
            .status.failed {
                color: red;
            }
        </style>
    </head>
    <body>
        <h1>🤖 Agents' Interaction Flow</h1>
        <div class="timeline">
            {% for agent in agents %}
            <div class="agent-card">
                <div class="icon">{{ agent.icon }}</div>
                <div class="name">{{ agent.name }}</div>
                <div class="role">{{ agent.role }}</div>
                <div class="action">{{ agent.action }}</div>
                <div class="status {{ agent.status }}">{{ agent.status.capitalize() }}</div>
            </div>
            {% endfor %}
        </div>
    </body>
    </html>
    """, agents=agents_data)


if __name__ == "__main__":
    app.run(debug=True)
