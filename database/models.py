import sqlite3
from datetime import datetime
import os
import sys

# Путь к базе — в папке data рядом с ботом
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "bot.db")

# ПРИНУДИТЕЛЬНО создаём папку и базу
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
print(f"📁 База будет тут: {DB_PATH}")

class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
            cls._instance.conn.row_factory = sqlite3.Row
            cls._instance.cursor = cls._instance.conn.cursor()
        return cls._instance
    
    def execute(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor
        except Exception as e:
            print(f"❌ DB Error: {e}")
            self.conn.rollback()
    
    def fetchone(self, query, params=()):
        self.cursor.execute(query, params)
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def fetchall(self, query, params=()):
        self.cursor.execute(query, params)
        return [dict(row) for row in self.cursor.fetchall()]
    
    def insert(self, table, data):
        cols = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        self.execute(f"INSERT INTO {table} ({cols}) VALUES ({placeholders})", tuple(data.values()))
        return self.cursor.lastrowid
    
    def update(self, table, data, where, params):
        set_clause = ', '.join([f"{k}=?" for k in data])
        self.execute(f"UPDATE {table} SET {set_clause} WHERE {where}", tuple(data.values()) + params)

db = Database()

# ПРИНУДИТЕЛЬНО создаём таблицы
print("🔧 Создаю таблицы...")
db.execute('''CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY, username TEXT, first_name TEXT,
    joined_date TEXT, paid INTEGER DEFAULT 0, banned INTEGER DEFAULT 0
)''')
db.execute('''CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER,
    amount INTEGER, status TEXT DEFAULT 'pending',
    created_at TEXT, confirmed_at TEXT
)''')
print("✅ Таблицы готовы!")

def get_user(user_id): 
    return db.fetchone("SELECT * FROM users WHERE user_id=?", (user_id,))

def create_user(user_id, username, first_name):
    db.insert('users', {
        'user_id': user_id, 
        'username': username or '', 
        'first_name': first_name or '', 
        'joined_date': datetime.now().isoformat()
    })
    print(f"✅ Новый юзер: {user_id}")

def get_pending_payments(): 
    return db.fetchall("SELECT * FROM payments WHERE status='pending' ORDER BY created_at DESC")

def confirm_payment(payment_id):
    db.update('payments', {'status': 'confirmed', 'confirmed_at': datetime.now().isoformat()}, 'id=?', (payment_id,))
    pay = db.fetchone("SELECT * FROM payments WHERE id=?", (payment_id,))
    if pay: 
        db.update('users', {'paid': 1}, 'user_id=?', (pay['user_id'],))
        print(f"✅ Платёж #{payment_id} подтверждён!")

def get_total_stats():
    users = db.fetchone("SELECT COUNT(*) as c FROM users")
    paid = db.fetchone("SELECT COUNT(*) as c FROM users WHERE paid=1")
    pays = db.fetchone("SELECT COUNT(*) as c FROM payments WHERE status='confirmed'")
    revenue = db.fetchone("SELECT SUM(amount) as c FROM payments WHERE status='confirmed'")
    return {
        'users': users['c'] if users else 0, 
        'paid': paid['c'] if paid else 0, 
        'pays': pays['c'] if pays else 0, 
        'revenue': revenue['c'] or 0 if revenue else 0
    }
