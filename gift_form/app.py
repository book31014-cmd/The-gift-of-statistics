from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_NAME = "data.db"

# ---------- 初始化資料庫 ----------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS gifts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        zhuyin TEXT,
        hint TEXT,
        created_at TEXT
    )
    """)
    conn.commit()
    conn.close()

# ---------- 首頁 ----------
@app.route("/")
def index():
    return render_template("index.html")

# ---------- 送出表單 ----------
@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    if not data:
        return jsonify({"ok": False, "error": "No data"}), 400

    name = data.get("name")
    zhuyin = data.get("zhuyin")
    hint = data.get("hint")

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT INTO gifts (name, zhuyin, hint, created_at) VALUES (?,?,?,?)",
        (name, zhuyin, hint, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()

    return jsonify({"ok": True})

# ---------- 管理頁 ----------
@app.route("/admin")
def admin():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    rows = c.execute("SELECT * FROM gifts ORDER BY id DESC").fetchall()
    conn.close()

    html = """
    <h1>🎁 交換禮物填寫名單</h1>
    <table border="1" cellpadding="8" cellspacing="0">
      <tr>
        <th>姓名</th>
        <th>注音</th>
        <th>提示</th>
        <th>填寫時間</th>
      </tr>
    """

    for r in rows:
        html += f"""
        <tr>
          <td>{r['name']}</td>
          <td>{r['zhuyin']}</td>
          <td>{r['hint']}</td>
          <td>{r['created_at']}</td>
        </tr>
        """

    html += "</table>"
    return html

# ---------- 啟動 ----------
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)

