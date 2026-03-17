from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'smarttask-secret-key-2026'

DATABASE = 'database.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )''')
    db.execute('''CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        priority TEXT NOT NULL DEFAULT 'Medium',
        status TEXT NOT NULL DEFAULT 'Pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    db.commit()

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to continue.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

# ─── AUTH ROUTES ────────────────────────────────────────────────

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        if not username or not password:
            flash('Username and password are required.')
            return render_template('register.html')
        hashed = generate_password_hash(password)
        try:
            db = get_db()
            db.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed))
            db.commit()
            flash('Account created! Please log in.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already taken. Try another.')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        flash('Invalid username or password.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.')
    return redirect(url_for('login'))

# ─── DASHBOARD & TASK ROUTES ────────────────────────────────────

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    db = get_db()
    user_id = session['user_id']

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'create':
            title = request.form.get('title', '').strip()
            priority = request.form.get('priority', 'Medium')
            status = request.form.get('status', 'Pending')
            if title:
                db.execute(
                    'INSERT INTO tasks (user_id, title, priority, status) VALUES (?, ?, ?, ?)',
                    (user_id, title, priority, status)
                )
                db.commit()
                flash('Task created successfully.')
            else:
                flash('Task title cannot be empty.')

        elif action == 'update':
            task_id = request.form.get('task_id')
            new_status = request.form.get('status')
            db.execute(
                'UPDATE tasks SET status = ? WHERE id = ? AND user_id = ?',
                (new_status, task_id, user_id)
            )
            db.commit()

        elif action == 'delete':
            task_id = request.form.get('task_id')
            db.execute('DELETE FROM tasks WHERE id = ? AND user_id = ?', (task_id, user_id))
            db.commit()
            flash('Task deleted.')

        return redirect(url_for('dashboard'))

    # Search & filters
    q = request.args.get('q', '').strip()
    priority_filter = request.args.get('priority', '')
    status_filter = request.args.get('status', '')

    base_sql = 'SELECT * FROM tasks WHERE user_id = ?'
    params = [user_id]

    if q:
        base_sql += ' AND title LIKE ?'
        params.append(f'%{q}%')
    if priority_filter:
        base_sql += ' AND priority = ?'
        params.append(priority_filter)
    if status_filter:
        base_sql += ' AND status = ?'
        params.append(status_filter)

    base_sql += ' ORDER BY created_at DESC'
    tasks = db.execute(base_sql, params).fetchall()

    # Stats
    total     = db.execute('SELECT COUNT(*) FROM tasks WHERE user_id = ?', (user_id,)).fetchone()[0]
    completed = db.execute('SELECT COUNT(*) FROM tasks WHERE user_id = ? AND status = "Completed"', (user_id,)).fetchone()[0]
    pending   = total - completed

    stats = {'total': total, 'completed': completed, 'pending': pending}

    chart_data = {
        'labels': ['Pending', 'Completed'],
        'data': [pending, completed],
        'colors': ['#f59e0b', '#10b981']
    }

    priorities = db.execute(
        'SELECT priority, COUNT(*) as cnt FROM tasks WHERE user_id = ? GROUP BY priority', (user_id,)
    ).fetchall()
    statuses = db.execute(
        'SELECT status, COUNT(*) as cnt FROM tasks WHERE user_id = ? GROUP BY status', (user_id,)
    ).fetchall()

    return render_template('dashboard.html',
        tasks=tasks, stats=stats, chart_data=chart_data,
        q=q, priority_filter=priority_filter, status_filter=status_filter,
        priorities=priorities, statuses=statuses
    )

# ─── MAIN ────────────────────────────────────────────────────────

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)
