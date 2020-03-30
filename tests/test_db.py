import sqlite3

import pytest
from flaskr.db import get_db


# Weryfikacja czy przy wywoływaniu danych z bazy aplikacji, zwracan jet zawsze ta sama wartość. Po wryfikacji utworzony
# 'context' pod testowanie zostaje zamknięty.
def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)

# The init-db command should call the init_db function and output a message.
# tests/test_db.py

def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('flaskr.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called
