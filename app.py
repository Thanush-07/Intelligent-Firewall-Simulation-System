from flask import Flask, render_template, request, redirect, jsonify, send_file, session
from flask_cors import CORS
import os
import secrets
import subprocess
import threading
app = Flask(__name__)
CORS(app) # Enable CORS for all routes
app.secret_key = secrets.token_hex(16)

# ---------------- CONFIGURATION ---------------- #

# # Autorun the code of firewall_simulation.py to ensure logs directory and files exist
def run_firewall_simulation():
    subprocess.Popen(["python", "firewall_simulation.py"])
threading.Thread(target=run_firewall_simulation).start()

# Read the rules file 
def load_rules():
    try:
        if os.path.exists('rules.json'):
            with open('rules.json' ,'r') as file:
                return json.load(file)
    except Exception as e:
        print(f"Error loading rules: {e}")
    return {"blocked_ip": [], "blocked_protocols": [], "blocked_ports": []}

USERNAME = "root"
PASSWORD = "firewall#"

def load_logs(filename, limit=None):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            lines = [line.strip() for line in f.readlines()]
            total = len(lines)
            if limit:
                return lines[-limit:], total
            return lines, total
    return [], 0

# ---------------- LOGIN SYSTEM ---------------- #

@app.route("/", methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect("/index")
    
    if request.method == "POST":
        if request.form["username"] == USERNAME and request.form["password"] == PASSWORD:
            session["user"] = USERNAME
            return redirect("/index")
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

@app.route("/index")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template("index.html")

# ✅ Route for AJAX to fetch logs and rules in real-time
@app.route("/get_logs")
def get_logs():
    # Only return the last 50 logs to prevent browser lag, but get total counts
    allowed_logs, total_allowed = load_logs("logs/firewall_Allowed_log.txt", limit=50)
    blocked_logs, total_blocked = load_logs("logs/firewall_log.txt", limit=50)
    
    # Reload rules to show updates if they change
    current_rules = load_rules()
    
    response = jsonify({
        "allowed": allowed_logs,
        "total_allowed": total_allowed,
        "blocked": blocked_logs,
        "total_blocked": total_blocked,
        "rules": current_rules
    })
    
    # Prevents browser from caching the log data
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    
    return response

# download logs 
@app.route("/download/all")
def download_all_logs():
    combined_file = "logs/all_logs.txt"

    allowed_logs, _ = load_logs("logs/firewall_Allowed_log.txt")
    blocked_logs, _ = load_logs("logs/firewall_log.txt")

    # Combine logs into a single file
    with open(combined_file, "w") as f:
        f.write("===== ALLOWED LOGS =====\n")
        if allowed_logs:
            for line in allowed_logs:
                f.write(line + "\n")
        else:
            f.write("No allowed logs.\n")

        f.write("\n===== BLOCKED LOGS =====\n")
        if blocked_logs:
            for line in blocked_logs:
                f.write(line + "\n")
        else:
            f.write("No blocked logs.\n")

    return send_file(combined_file, as_attachment=True, download_name="firewall_logs.txt")

if __name__ == "__main__":
    app.run(debug=True)
