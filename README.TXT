🤖 AI Prompt Evaluator

An AI-powered web application that evaluates prompts and AI responses based on Relevance, Clarity, Accuracy, and Consistency, with user authentication, history tracking, analytics dashboard, and PDF report generation.

🚀 Features
🔐 User Registration & Login (Flask-Login)
🤖 AI Prompt Evaluation System
📊 Analytics Dashboard (average scores)
📜 Evaluation History with search
🧠 Session-based chat tracking (multiple evaluations per session)
📄 Download full PDF report
🎨 Modern UI with sidebar navigation
🗂️ SQLite database storage
🏗️ Tech Stack
Frontend: HTML, CSS, JavaScript (Jinja2 templates)
Backend: Flask (Python)
Database: SQLite + SQLAlchemy
Authentication: Flask-Login
PDF Generation: ReportLab
📁 Project Structure
AI Prompt Evaluator/
│
├── app.py
├── models.py
├── evaluator.py
├── app.db
│
├── templates/
│   ├── landing.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── history.html
│   ├── analytics.html
│
├── static/
│   ├── css/
│   ├── js/
│
└── README.md
⚙️ Installation & Setup
1. Clone the repository
git clone https://github.com/your-username/ai-prompt-evaluator.git
cd ai-prompt-evaluator
2. Create virtual environment
python -m venv venv

Activate it:

Windows

venv\Scripts\activate

Mac/Linux

source venv/bin/activate
3. Install dependencies
pip install flask flask-login flask-sqlalchemy werkzeug reportlab
4. Run the application
python app.py
5. Open in browser
http://127.0.0.1:5000/
🔑 How It Works
Register/Login as a user
Go to Dashboard
Enter:
Prompt
AI Response
Click Evaluate
System generates scores:
Relevance
Clarity
Accuracy
Consistency
Overall Score
Data is saved to database
📊 Analytics Module
Shows average performance scores
Helps track AI response quality over time
📜 History Module
Stores all previous evaluations
Search functionality for quick filtering
📄 PDF Report
Generates complete evaluation report
Includes:
User details
All evaluations
Summary analytics
🧠 Future Improvements
Add AI API (OpenAI / Gemini) integration
Improve dashboard charts (Chart.js)
Add multi-user admin panel
Export CSV feature
Better session-based chat UI (like ChatGPT)
🐞 Common Issue Fix

If you get errors like:

no such column: evaluation.session_id

👉 Run:

db.drop_all()
db.create_all()

or delete app.db and restart server.

👨‍💻 Author

Built by Sravsssss
B.Sc Mathematics, Statistics & Data Science Student