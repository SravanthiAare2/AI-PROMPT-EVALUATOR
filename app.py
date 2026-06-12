from flask import Flask, render_template, request, redirect, send_file
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Evaluation
from evaluator import evaluate

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template("landing.html")

# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter(
            (User.email == email) | (User.username == username)
        ).first()

        if existing_user:
            return redirect('/login')

        user = User(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )

        db.session.add(user)
        db.session.commit()

        return redirect('/login')

    return render_template("register.html")

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter(
            (User.email == email) | (User.username == email)
        ).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect('/dashboard')

        return redirect('/login')

    return render_template("login.html")

# ---------------- LOGOUT ----------------
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

# ---------------- DASHBOARD ----------------
@app.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    result = None

    if request.method == 'POST':
        prompt = request.form['prompt']
        response = request.form['response']

        result = evaluate(prompt, response)

        entry = Evaluation(
            user_id=current_user.id,
            prompt=prompt,
            response=response,
            relevance=result["relevance"],
            clarity=result["clarity"],
            accuracy=result["accuracy"],
            consistency=result["consistency"],
            overall=result["overall"]
        )

        db.session.add(entry)
        db.session.commit()

    return render_template("dashboard.html", result=result)

# ---------------- HISTORY ----------------
@app.route('/history')
@login_required
def history():
    data = Evaluation.query.filter_by(user_id=current_user.id).all()
    return render_template("history.html", data=data)

# ---------------- ANALYTICS ----------------
@app.route('/analytics')
@login_required
def analytics():
    data = Evaluation.query.filter_by(user_id=current_user.id).all()

    if len(data) == 0:
        return render_template("analytics.html", r=0, c=0, a=0, co=0)

    r = sum(d.relevance for d in data) / len(data)
    c = sum(d.clarity for d in data) / len(data)
    a = sum(d.accuracy for d in data) / len(data)
    co = sum(d.consistency for d in data) / len(data)

    return render_template("analytics.html", r=r, c=c, a=a, co=co)

# ---------------- FULL PDF EXPORT ----------------
@app.route('/pdf')
@login_required
def pdf():
    data = Evaluation.query.filter_by(user_id=current_user.id).all()

    file_name = f"AI_Report_{current_user.username}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    doc = SimpleDocTemplate(file_name)
    styles = getSampleStyleSheet()

    content = []

    # TITLE
    content.append(Paragraph("AI PROMPT EVALUATION REPORT", styles["Title"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph(f"User: {current_user.username}", styles["Normal"]))
    content.append(Paragraph(f"Date: {datetime.now()}", styles["Normal"]))
    content.append(Spacer(1, 12))

    if len(data) == 0:
        content.append(Paragraph("No evaluation data found.", styles["Normal"]))
        doc.build(content)
        return send_file(file_name, as_attachment=True)

    # ANALYTICS
    r = sum(d.relevance for d in data) / len(data)
    c = sum(d.clarity for d in data) / len(data)
    a = sum(d.accuracy for d in data) / len(data)
    co = sum(d.consistency for d in data) / len(data)

    content.append(Paragraph("SUMMARY ANALYTICS", styles["Heading2"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"Relevance: {round(r,2)}", styles["Normal"]))
    content.append(Paragraph(f"Clarity: {round(c,2)}", styles["Normal"]))
    content.append(Paragraph(f"Accuracy: {round(a,2)}", styles["Normal"]))
    content.append(Paragraph(f"Consistency: {round(co,2)}", styles["Normal"]))
    content.append(Spacer(1, 15))

    # HISTORY
    content.append(Paragraph("HISTORY REPORT", styles["Heading2"]))
    content.append(Spacer(1, 10))

    for d in data:
        content.append(Paragraph("────────────────────", styles["Normal"]))
        content.append(Paragraph(f"Prompt: {d.prompt}", styles["Normal"]))
        content.append(Paragraph(f"Response: {d.response}", styles["Normal"]))
        content.append(Paragraph(f"Relevance: {d.relevance}", styles["Normal"]))
        content.append(Paragraph(f"Clarity: {d.clarity}", styles["Normal"]))
        content.append(Paragraph(f"Accuracy: {d.accuracy}", styles["Normal"]))
        content.append(Paragraph(f"Consistency: {d.consistency}", styles["Normal"]))
        content.append(Paragraph(f"Overall: {d.overall}", styles["Normal"]))
        content.append(Spacer(1, 10))

    doc.build(content)

    return send_file(file_name, as_attachment=True)

# ---------------- RUN ----------------
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)