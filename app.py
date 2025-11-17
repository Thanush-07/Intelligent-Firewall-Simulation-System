from flask import Flask, render_template, request, redirect, jsonify , send_file
import os
import subprocess
import threading
app = Flask(__name__)

# ---------------- CONFIGURATION ---------------- #

# # Autorun the code of firewall_simulation.py to ensure logs directory and files exist
def run_firewall_simulation():
    subprocess.Popen(["python", "firewall_simulation.py"])
threading.Thread(target=run_firewall_simulation).start()

USERNAME = "root"
PASSWORD = "firewall#"
logged_in_flag = False

def load_logs(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return [line.strip() for line in f.readlines()]
    return []

# ---------------- LOGIN SYSTEM ---------------- #

@app.route("/", methods=["GET", "POST"])
def login():
    global logged_in_flag
    if request.method == "POST":
        if request.form["username"] == USERNAME and request.form["password"] == PASSWORD:
            logged_in_flag = True
            return redirect("/index")
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/logout")
def logout():
    global logged_in_flag
    logged_in_flag = False
    return redirect("/")

@app.route("/index")
def dashboard():
    global logged_in_flag
    if not logged_in_flag:
        return redirect("/")
    return render_template("index.html")

# ✅ Route for AJAX to fetch logs in real-time
@app.route("/get_logs")
def get_logs():
    allowed_logs = load_logs("logs/firewall_Allowed_log.txt")
    blocked_logs = load_logs("logs/firewall_log.txt")
    return jsonify({
        "allowed": allowed_logs,
        "blocked": blocked_logs
    })

# download logs 
@app.route("/download/all")
def download_all_logs():
    combined_file = "logs/all_logs.txt"

    allowed_logs = load_logs("logs/firewall_Allowed_log.txt")
    blocked_logs = load_logs("logs/firewall_log.txt")

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
