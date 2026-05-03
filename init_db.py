import sqlite3
import os

DB_PATH = "data/bot.db"
os.makedirs("data", exist_ok=True)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY, username TEXT, first_name TEXT,
    joined_date TEXT, paid INTEGER DEFAULT 0, banned INTEGER DEFAULT 0
)''')

c.execute('''CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER,
    amount INTEGER, status TEXT DEFAULT 'pending',
    created_at TEXT, confirmed_at TEXT
)''')

conn.commit()
conn.close()
print("✅ База создана!")
