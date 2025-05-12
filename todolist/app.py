from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json

# Flask-App initialisieren
app = Flask(__name__)
app.secret_key = "dein_geheimer_schluessel"  # Für Session-Management

# Dateipfade für Benutzer- und Aufgabenlisten
USERS_DIR = 'unterricht'
USERS_FILE = os.path.join(USERS_DIR, 'users.json')
TODOS_FILE = os.path.join(USERS_DIR, 'todos.json')

# Sicherstellen, dass der Ordner für die Daten existiert
os.makedirs(USERS_DIR, exist_ok=True)

# =========================
# Benutzerverwaltung
# =========================

# Benutzer aus Datei laden
def load_users():
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Benutzer in Datei speichern
def save_users(users):
    os.makedirs(USERS_DIR, exist_ok=True)
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

# =========================
# Aufgabenverwaltung
# =========================

# Aufgaben aus Datei laden
def load_todos():
    try:
        with open(TODOS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Aufgaben in Datei speichern
def save_todos(todos):
    os.makedirs(USERS_DIR, exist_ok=True)
    with open(TODOS_FILE, 'w', encoding='utf-8') as f:
        json.dump(todos, f, ensure_ascii=False, indent=4)

# Neue eindeutige ID für Aufgaben generieren
def get_next_id(todos):
    if not todos:
        return 1
    ids = [todo.get('id', 0) for todo in todos]
    return max(ids) + 1

# =========================
# Routen für die Web-App
# =========================

# Registrierung eines neuen Benutzers
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']
        # Prüfen, ob Benutzername schon existiert
        if any(u['username'] == username for u in users):
            flash('Benutzername existiert bereits!', 'error')
            return redirect(url_for('register'))
        # Benutzer mit gehashtem Passwort speichern
        users.append({
            'username': username,
            'password_hash': generate_password_hash(password)
        })
        save_users(users)
        flash('Registrierung erfolgreich!', 'success')
        return redirect(url_for('login'))
    # Registrierungsseite anzeigen
    return render_template('register.html')

# Login eines Benutzers
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']
        # Benutzer suchen
        user = next((u for u in users if u['username'] == username), None)
        # Passwort prüfen
        if user and check_password_hash(user['password_hash'], password):
            session['username'] = username  # Benutzername in Session speichern
            flash('Login erfolgreich!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Falscher Benutzername oder Passwort!', 'error')
            return redirect(url_for('login'))
    # Loginseite anzeigen
    return render_template('login.html')

# Passwort vergessen-Funktion
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        users = load_users()
        user = next((u for u in users if u['username'] == username), None)
        if user:
            flash('Bitte wende dich an den Administrator, um dein Passwort zurückzusetzen.', 'info')
        else:
            flash('Benutzername nicht gefunden.', 'error')
        return redirect(url_for('forgot_password'))
    # Passwort-vergessen-Seite anzeigen
    return render_template('forgot_password.html')

# Logout eines Benutzers
@app.route('/logout')
def logout():
    session.pop('username', None)  # Benutzer aus Session entfernen
    flash('Du wurdest ausgeloggt.', 'info')
    return redirect(url_for('login'))

# Startseite (Aufgabenübersicht) – nur für eingeloggte Benutzer
@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    todos = load_todos()
    # Nur Aufgaben des eingeloggten Benutzers anzeigen
    user_todos = [t for t in todos if t.get('username') == session['username']]
    return render_template('index.html', todos=user_todos, username=session['username'])

# Aufgabe hinzufügen (POST)
@app.route('/add', methods=['POST'])
def add():
    if 'username' not in session:
        return redirect(url_for('login'))
    todos = load_todos()
    # Neue Aufgabe aus Formulardaten erstellen
    new_todo = {
        "id": get_next_id(todos),
        "username": session['username'],
        "task": request.form.get('task', ''),
        "status": request.form.get('status', ''),
        "due_date": request.form.get('due_date', ''),
        "priority": request.form.get('priority', ''),
        "note": request.form.get('note', ''),
        "responsible": request.form.get('responsible', ''),
        "category": request.form.get('category', '')
    }
    todos.append(new_todo)
    save_todos(todos)
    flash('Aufgabe hinzugefügt.', 'success')
    return redirect(url_for('index'))

# Aufgabe löschen (POST)
@app.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    todos = load_todos()
    # Nur Aufgaben löschen, die dem eingeloggten Benutzer gehören und die ID haben
    todos = [todo for todo in todos if not (todo.get('id') == task_id and todo.get('username') == session['username'])]
    save_todos(todos)
    flash('Aufgabe gelöscht.', 'info')
    return redirect(url_for('index'))

# Aufgabe bearbeiten (GET/POST)
@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    todos = load_todos()
    # Gesuchte Aufgabe finden
    todo = next((t for t in todos if t.get('id') == task_id and t.get('username') == session['username']), None)
    if not todo:
        flash('Aufgabe nicht gefunden oder keine Berechtigung.', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        # Felder aktualisieren
        todo['task'] = request.form.get('task', '')
        todo['status'] = request.form.get('status', '')
        todo['due_date'] = request.form.get('due_date', '')
        todo['priority'] = request.form.get('priority', '')
        todo['note'] = request.form.get('note', '')
        todo['responsible'] = request.form.get('responsible', '')
        todo['category'] = request.form.get('category', '')
        save_todos(todos)
        flash('Aufgabe aktualisiert.', 'success')
        return redirect(url_for('index'))

    # Bearbeiten-Seite anzeigen
    return render_template('edit.html', todo=todo)

# Flask-App starten
if __name__ == '__main__':
    app.run(debug=True)
