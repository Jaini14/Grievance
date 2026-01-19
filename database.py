import sqlite3
from datetime import datetime

DB_NAME = "grievance_db.db"

# ---------- Create Database ----------
def create_table():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS grievances (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        category TEXT,
        priority TEXT,
        sentiment TEXT,
        status TEXT,
        anonymous TEXT,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()

# ---------- Insert Grievance ----------
def insert_grievance(text, category, priority, sentiment, anonymous):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO grievances 
    (text, category, priority, sentiment, status, anonymous, date)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        text,
        category,
        priority,
        sentiment,
        "Pending",
        anonymous,
        datetime.now().strftime("%Y-%m-%d")
    ))

    conn.commit()
    conn.close()

# ---------- Fetch All Grievances ----------
def fetch_grievances():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT * FROM grievances")
    rows = cur.fetchall()

    conn.close()
    return rows
