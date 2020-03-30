from flaskr import create_app

# Sprawdza istnienie poprwanośc pliku konfiguracyjnego. Jeśli test nie zostanie zaliczony, test zwróci domyślne
# ustawienia. Jeśli zostanie zaliczony, napisze domyslną konfigurację.
def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


# test funkcji "hello" wenątrz factory - sprawdzamy, czy fabryka jest dobrze skonfigurowana i działa. Sprawdzamy
# poprawność wyśietlonego (zwróconego) tekstu.
def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'