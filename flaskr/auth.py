import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

# ustawienie blueprinta dla 'fabryki' w __init__.py
bp = Blueprint('auth', __name__, url_prefix='/auth')


# funkcjonalność strony do rejestrowania. Weryfikacja poprawności wpisanych danych oraz czy użtkownik juz nie jest
# zarejestrowany w bazie db. Jeśli wszytko OK, dodaje żytkownia i hashuje hasło.
@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif db.execute(
                'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = f"User {username} is already registered."

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for("auth.login"))

        flash(error)
    return render_template("auth/register.html")


# Strona logowania, a dokładnie jej funkcjonalność. Weryfikacja użytkoiwnia i hasła. Poprawne dane logują dane sesji
# z informacjami użytkownika.
@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)
    return render_template('auth/login.html')


# Funkcja działająca przed wyświtelniem strony po zapytaniu. Sprawdza czy użytkownik jest zalogowany i wczytuje jego
# dane jeśli jest, w innym rzie g.user bedzie None - uzytkownik jest wylogowany.
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


# Wylogowanie. Usuwamy ID użytkownika z sesji i kolenych zapytań.
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))



# Weryfikacja czy użytkownik jest zalogowany. Weryfikacja następuje przy próbie wprowadzania zmian, oddawania postów etc
# Zwraca aktualny widok, jesli uzytkownik jest zalogowany. Zwraca stronę logowania w przeciwnym razie.
# Dekorator zostanie wykorzystany przy funkcji tworzenia postów.
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

