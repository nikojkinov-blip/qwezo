from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import sqlite3
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI(title="QAZLO Admin")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "bot.db")
ADMIN_ID = 6593438966

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_stats():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) as c FROM users"); users = c.fetchone()['c']
    c.execute("SELECT COUNT(*) as c FROM users WHERE paid=1"); paid = c.fetchone()['c']
    c.execute("SELECT COUNT(*) as c FROM payments WHERE status='confirmed'"); pays = c.fetchone()['c']
    c.execute("SELECT SUM(amount) as c FROM payments WHERE status='confirmed'"); rev = c.fetchone()['c'] or 0
    c.execute("SELECT COUNT(*) as c FROM payments WHERE status='pending'"); pending = c.fetchone()['c']
    conn.close()
    return {'users': users, 'paid': paid, 'pays': pays, 'revenue': rev, 'pending': pending}

def get_payments():
    conn = get_db()
    pays = [dict(r) for r in conn.cursor().execute("SELECT * FROM payments ORDER BY created_at DESC LIMIT 100").fetchall()]
    conn.close()
    return pays

def get_users():
    conn = get_db()
    users = [dict(r) for r in conn.cursor().execute("SELECT * FROM users ORDER BY joined_date DESC LIMIT 100").fetchall()]
    conn.close()
    return users

STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
:root{--bg:#0a0010;--card:#120020;--border:#2a1040;--primary:#b04dff;--accent:#ff2d95;--green:#00ff88;--text:#e0d0ff;--text2:#8060a0}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Orbitron',sans-serif;background:var(--bg);color:var(--text);min-height:100vh;display:flex}
body::before{content:'';position:fixed;top:0;left:0;width:100%;height:100%;background:url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg"><defs><pattern id="g" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0L0 0 0 40" fill="none" stroke="rgba(176,77,255,0.05)" stroke-width="1"/></pattern></defs><rect width="100%" height="100%" fill="url(%23g)"/></svg>');pointer-events:none;z-index:0}
.sidebar{width:280px;min-height:100vh;background:var(--card);border-right:1px solid var(--border);padding:30px 0;position:fixed;z-index:10}
.sidebar h2{text-align:center;font-size:20px;font-weight:900;letter-spacing:2px;background:linear-gradient(135deg,var(--primary),var(--accent));-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:30px}
.sidebar .nav-link{display:block;padding:14px 25px;color:var(--text2);text-decoration:none;font-size:13px;letter-spacing:1px;transition:.3s;margin:4px 0;border-left:3px solid transparent}
.sidebar .nav-link:hover,.sidebar .nav-link.active{color:var(--primary);border-left-color:var(--primary);background:rgba(176,77,255,0.05);text-shadow:0 0 10px var(--primary)}
.main{margin-left:280px;padding:30px;flex:1;position:relative;z-index:1}
h1{font-size:28px;font-weight:900;letter-spacing:2px;margin-bottom:20px;background:linear-gradient(135deg,var(--primary),var(--accent));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.stats-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:15px;margin-bottom:30px}
.stat-card{background:var(--card);border:1px solid var(--border);padding:25px;border-radius:15px;text-align:center;transition:.3s}
.stat-card:hover{border-color:var(--primary);box-shadow:0 0 30px rgba(176,77,255,0.2);transform:translateY(-3px)}
.stat-card .value{font-size:36px;font-weight:900;color:var(--primary)}
.stat-card .label{font-size:11px;color:var(--text2);margin-top:8px;letter-spacing:1px}
.card{background:var(--card);border:1px solid var(--border);border-radius:15px;padding:25px;margin-bottom:20px}
.card h3{font-size:16px;letter-spacing:1px;margin-bottom:15px;color:var(--primary2,#7b2fff)}
table{width:100%;border-collapse:collapse}
th{text-align:left;padding:12px;font-size:11px;color:var(--text2);letter-spacing:1px;border-bottom:1px solid var(--border)}
td{padding:12px;font-size:13px;border-bottom:1px solid rgba(42,16,64,0.5)}
tr:hover{background:rgba(176,77,255,0.03)}
.btn{display:inline-block;padding:10px 20px;border-radius:8px;font-size:12px;font-weight:700;letter-spacing:1px;cursor:pointer;transition:.3s;text-decoration:none;border:none;font-family:'Orbitron',sans-serif}
.btn-primary{background:var(--primary);color:#fff}.btn-primary:hover{box-shadow:0 0 20px rgba(176,77,255,0.5)}
.btn-success{background:var(--green);color:#000}.btn-success:hover{box-shadow:0 0 20px rgba(0,255,136,0.5)}
.btn-danger{background:#ff3355;color:#fff}
.btn-sm{padding:6px 14px;font-size:10px}
.badge{display:inline-block;padding:5px 12px;border-radius:20px;font-size:10px;letter-spacing:1px}
.badge-success{background:rgba(0,255,136,0.2);color:var(--green)}
.badge-warning{background:rgba(255,204,0,0.2);color:#ffcc00}
.form-control{width:100%;padding:12px;background:rgba(255,255,255,0.03);border:1px solid var(--border);border-radius:8px;color:var(--text);font-family:'Orbitron',sans-serif;font-size:13px;margin-bottom:10px}
textarea.form-control{resize:vertical;min-height:80px}
@media(max-width:768px){.sidebar{width:100%;min-height:auto;position:relative}.main{margin-left:0}.stats-grid{grid-template-columns:repeat(2,1fr)}}
</style>
"""

@app.get("/", response_class=HTMLResponse)
async def login():
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>QAZLO Admin</title>{STYLE}<style>body{{display:flex;align-items:center;justify-content:center;flex-direction:column}}.login-box{{background:var(--card);padding:40px;border-radius:20px;border:1px solid var(--border);text-align:center}}</style></head>
    <body><div class="login-box"><h1>⚡ QAZLO</h1><p style="color:var(--text2);margin-bottom:20px">CYBERPUNK ADMIN</p>
    <form method="POST" action="/login"><input type="number" name="user_id" placeholder="Telegram ID" style="width:100%;padding:15px;margin:15px 0;font-size:16px;background:rgba(255,255,255,0.03);border:1px solid var(--border);border-radius:8px;color:var(--text);text-align:center" required autofocus><br><button class="btn btn-primary" style="width:100%;padding:15px">🔓 ВХОД</button></form></div></body></html>"""

@app.post("/login")
async def login_post(user_id: int = Form(...)):
    if user_id != ADMIN_ID: return HTMLResponse("<h2>Доступ запрещён</h2>")
    response = RedirectResponse(url="/dashboard", status_code=302)
    response.set_cookie("admin", str(user_id))
    return response

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    if not request.cookies.get("admin"): return RedirectResponse(url="/")
    s = get_stats()
    pays = get_payments()[:10]
    users = get_users()[:10]
    
    pay_rows = ""
    for p in pays:
        st = "✅" if p['status']=='confirmed' else "⏳"
        pay_rows += f"<tr><td>#{p['id']}</td><td><code>{p['user_id']}</code></td><td>{p['amount']}₽</td><td><span class='badge badge-{'success' if p['status']=='confirmed' else 'warning'}'>{st}</span></td><td>{'<a href=\"/confirm/'+str(p['id'])+'\" class=\"btn btn-success btn-sm\">✓</a>' if p['status']=='pending' else ''}</td></tr>"
    
    user_rows = ""
    for u in users:
        u_st = "💎" if u.get('paid') else "⏳"
        user_rows += f"<tr><td><code>{u['user_id']}</code></td><td>@{u.get('username','?')}</td><td>{u_st}</td></tr>"
    
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><title>QAZLO Dashboard</title>{STYLE}</head><body>
    <div class="sidebar"><h2>⚡ QAZLO</h2>
        <a class="nav-link active" href="/dashboard">📊 ДАШБОРД</a>
        <a class="nav-link" href="/payments">💰 ПЛАТЕЖИ</a>
        <a class="nav-link" href="/users">👥 ПОЛЬЗОВАТЕЛИ</a>
        <a class="nav-link" href="/broadcast">📢 РАССЫЛКА</a>
        <div style="position:absolute;bottom:20px;padding:20px"><a href="/logout" style="color:#ff3355">🚪 ВЫХОД</a></div>
    </div>
    <div class="main"><h1>📊 ДАШБОРД</h1>
        <div class="stats-grid">
            <div class="stat-card"><div class="value">{s['users']}</div><div class="label">ПОЛЬЗОВАТЕЛЕЙ</div></div>
            <div class="stat-card"><div class="value">{s['paid']}</div><div class="label">ОПЛАТИВШИХ</div></div>
            <div class="stat-card"><div class="value">{s['revenue']}₽</div><div class="label">ДОХОД</div></div>
            <div class="stat-card"><div class="value">{s['pending']}</div><div class="label">ОЖИДАЮТ</div></div>
        </div>
        <div class="card"><h3>💰 ПОСЛЕДНИЕ ПЛАТЕЖИ</h3><table><tr><th>ID</th><th>USER</th><th>СУММА</th><th>СТАТУС</th><th></th></tr>{pay_rows}</table></div>
        <div class="card"><h3>👥 ПОСЛЕДНИЕ ЮЗЕРЫ</h3><table><tr><th>ID</th><th>USERNAME</th><th>СТАТУС</th></tr>{user_rows}</table></div>
    </div></body></html>"""

@app.get("/payments", response_class=HTMLResponse)
async def payments_page(request: Request):
    if not request.cookies.get("admin"): return RedirectResponse(url="/")
    pays = get_payments()
    rows = ""
    for p in pays:
        st = "✅" if p['status']=='confirmed' else "⏳"
        rows += f"<tr><td>#{p['id']}</td><td><code>{p['user_id']}</code></td><td>{p['amount']}₽</td><td><span class='badge badge-{'success' if p['status']=='confirmed' else 'warning'}'>{st}</span></td><td>{p.get('created_at','')[:16]}</td><td>{'<a href=\"/confirm/'+str(p['id'])+'\" class=\"btn btn-success btn-sm\">✓ ПОДТВЕРДИТЬ</a>' if p['status']=='pending' else ''}</td></tr>"
    return f"""<!DOCTYPE html><html><head><title>Платежи</title>{STYLE}</head><body>
    <div class="sidebar"><h2>⚡ QAZLO</h2><a class="nav-link" href="/dashboard">📊 ДАШБОРД</a><a class="nav-link active" href="/payments">💰 ПЛАТЕЖИ</a><a class="nav-link" href="/users">👥 ПОЛЬЗОВАТЕЛИ</a><div style="position:absolute;bottom:20px;padding:20px"><a href="/logout" style="color:#ff3355">🚪 ВЫХОД</a></div></div>
    <div class="main"><h1>💰 ПЛАТЕЖИ</h1><div class="card"><table><tr><th>ID</th><th>USER</th><th>СУММА</th><th>СТАТУС</th><th>ДАТА</th><th></th></tr>{rows}</table></div></div></body></html>"""

@app.get("/confirm/{payment_id}")
async def confirm(payment_id: int, request: Request):
    if not request.cookies.get("admin"): return RedirectResponse(url="/")
    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE payments SET status='confirmed', confirmed_at=? WHERE id=?", (datetime.now().isoformat(), payment_id))
    c.execute("SELECT user_id FROM payments WHERE id=?", (payment_id,))
    row = c.fetchone()
    if row: c.execute("UPDATE users SET paid=1 WHERE user_id=?", (row['user_id'],))
    conn.commit(); conn.close()
    return RedirectResponse(url="/payments", status_code=302)

@app.get("/users", response_class=HTMLResponse)
async def users_page(request: Request):
    if not request.cookies.get("admin"): return RedirectResponse(url="/")
    users = get_users()
    rows = ""
    for u in users:
        st = "💎" if u.get('paid') else "⏳"
        ban = "🚫" if u.get('banned') else ""
        rows += f"<tr><td><code>{u['user_id']}</code></td><td>@{u.get('username','?')}</td><td>{st}{ban}</td><td>{u.get('joined_date','')[:10]}</td><td><a href='/ban/{u['user_id']}' class='btn btn-danger btn-sm'>🚫</a> <a href='/unban/{u['user_id']}' class='btn btn-success btn-sm'>✅</a></td></tr>"
    return f"""<!DOCTYPE html><html><head><title>Пользователи</title>{STYLE}</head><body>
    <div class="sidebar"><h2>⚡ QAZLO</h2><a class="nav-link" href="/dashboard">📊 ДАШБОРД</a><a class="nav-link active" href="/users">👥 ПОЛЬЗОВАТЕЛИ</a><div style="position:absolute;bottom:20px;padding:20px"><a href="/logout" style="color:#ff3355">🚪 ВЫХОД</a></div></div>
    <div class="main"><h1>👥 ПОЛЬЗОВАТЕЛИ</h1><div class="card"><table><tr><th>ID</th><th>USERNAME</th><th>СТАТУС</th><th>ДАТА</th><th></th></tr>{rows}</table></div></div></body></html>"""

@app.get("/ban/{user_id}")
async def ban(user_id: int, request: Request):
    if not request.cookies.get("admin"): return
    get_db().cursor().execute("UPDATE users SET banned=1 WHERE user_id=?", (user_id,)); get_db().conn.commit()
    return RedirectResponse(url="/users", status_code=302)

@app.get("/unban/{user_id}")
async def unban(user_id: int, request: Request):
    if not request.cookies.get("admin"): return
    get_db().cursor().execute("UPDATE users SET banned=0 WHERE user_id=?", (user_id,)); get_db().conn.commit()
    return RedirectResponse(url="/users", status_code=302)

@app.get("/broadcast", response_class=HTMLResponse)
async def broadcast_page(request: Request):
    if not request.cookies.get("admin"): return RedirectResponse(url="/")
    s = get_stats()
    return f"""<!DOCTYPE html><html><head><title>Рассылка</title>{STYLE}</head><body>
    <div class="sidebar"><h2>⚡ QAZLO</h2><a class="nav-link" href="/dashboard">📊 ДАШБОРД</a><a class="nav-link active" href="/broadcast">📢 РАССЫЛКА</a><div style="position:absolute;bottom:20px;padding:20px"><a href="/logout" style="color:#ff3355">🚪 ВЫХОД</a></div></div>
    <div class="main"><h1>📢 РАССЫЛКА</h1><div class="card"><p style="color:var(--text2)">Всего: {s['users']} пользователей</p><form method="POST" action="/send_broadcast"><textarea name="message" class="form-control" rows="5" required></textarea><br><button type="submit" class="btn btn-primary">📢 ОТПРАВИТЬ</button></form></div></div></body></html>"""

@app.post("/send_broadcast")
async def send_broadcast(message: str = Form(...), request: Request = None):
    if not request.cookies.get("admin"): return
    users = get_db().cursor().execute("SELECT user_id FROM users WHERE banned=0").fetchall()
    return HTMLResponse(f"""<html><head>{STYLE}</head><body style="display:flex;align-items:center;justify-content:center"><div class="card" style="text-align:center"><h2>✅ РАССЫЛКА ЗАПУЩЕНА!</h2><p>Пользователей: {len(users)}</p><a href="/broadcast" class="btn btn-primary">НОВАЯ</a></div></body></html>""")

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("admin")
    return response
