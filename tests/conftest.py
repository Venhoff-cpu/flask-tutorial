import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    # Tworzymy tymczasową bazę danych która ma symulować bazę aplikacji flaskr. Po zakończeniu działania zostanie
    # usunięta. Ścieżka do DATABASE jest nadpisywana przez tą komendę
    db_fd, db_path = tempfile.mkstemp()

    # Mówimy Flask'owi, że jesteśmy w trybie testowania.
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)

# Dodatek pytest tworzy klienta testowego, który będzie wykonywał testy. Klient wytworzy dla siebie narzędzia,
# które beda przypasowane do funkcji w "fabryce" aplikacji.
@pytest.fixture
def client(app):
    return app.test_client()

# Dodatek pytest symulujący pracę klienta, odpowiadać będzie za wywoływanie akcji typu "click" -> klikanie pzycisków i
#  odnośników na stronie.
@pytest.fixture
def runner(app):
    return app.test_cli_runner()


# Utworzenie klienta testowego w celu logowania się i weryfikacji systemu autentyfikacji (auth).
class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


# dzięki narzędziu auth, jesteśmy wstanie uzywac w testach funkcji auth.login(), by zalogowac się jako użytkownik
# testowy
@pytest.fixture
def auth(client):
    return AuthActions(client)