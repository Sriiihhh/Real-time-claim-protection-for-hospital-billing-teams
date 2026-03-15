from flask import Flask, render_template, redirect, jsonify
import sqlite3
from monitor import check_policy_updates

app = Flask(__name__)


# -----------------------------
# DATABASE CONNECTION
# -----------------------------
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# -----------------------------
# HOME PAGE
# -----------------------------
@app.route("/")
def index():
    return render_template("index.html")


# -----------------------------
# RUN POLICY MONITOR
# -----------------------------
@app.route("/monitor")
def monitor():

    updates = check_policy_updates()

    conn = get_db()
    cur = conn.cursor()

    # GET LAST POLICY ID
    last = conn.execute(
        "SELECT id FROM policies ORDER BY id DESC LIMIT 1"
    ).fetchone()

    if last:
        num = int(last["id"].split("-")[1]) + 1
    else:
        num = 2601

    # INSERT NEW POLICIES
    for policy in updates:

        policy_id = f"PY-{num}"

        cur.execute("""
        INSERT INTO policies (id, policy_name, company, status)
        VALUES (?, ?, ?, ?)
        """, (
            policy_id,
            policy["policy_name"],
            policy["company"],
            policy["status"]
        ))

        num += 1

    conn.commit()
    conn.close()

    return redirect("/dashboard")


# -----------------------------
# DASHBOARD PAGE
# -----------------------------
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# -----------------------------
# API : ALL POLICIES (REAL TIME)
# -----------------------------
@app.route("/api/policies")
def get_policies():

    conn = get_db()

    rows = conn.execute("""
    SELECT id, policy_name, company, status
    FROM policies
    ORDER BY id DESC
    """).fetchall()

    conn.close()

    data = [dict(row) for row in rows]

    return jsonify(data)


# -----------------------------
# API : ANALYTICS FOR CHARTS
# -----------------------------
@app.route("/api/analytics")
def analytics():

    conn = get_db()

    rows = conn.execute("""
    SELECT company, COUNT(*) as total
    FROM policies
    WHERE status = 'Changed'
    GROUP BY company
    """).fetchall()

    conn.close()

    data = []

    for r in rows:
        data.append({
            "company": r["company"],
            "count": r["total"]
        })

    return jsonify(data)


# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)