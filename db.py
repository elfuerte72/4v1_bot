import sqlite3
from datetime import datetime

conn = sqlite3.connect("dialogs.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS dialogs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    message TEXT,
    role TEXT,
    timestamp TEXT
)
""")
conn.commit()

def save_dialogue(user_id, message, role):
    timestamp = datetime.now().isoformat()
    cursor.execute("INSERT INTO dialogs (user_id, message, role, timestamp) VALUES (?, ?, ?, ?)",
                   (user_id, message, role, timestamp))
    conn.commit()