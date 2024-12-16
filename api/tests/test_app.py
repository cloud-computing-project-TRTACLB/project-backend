import pytest
import jwt
from main import app,get_db_connection



@pytest.fixture
def client():
    # Configure Flask pour testing
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_db_connection():
    """
    Test la connexion à la base de données.
    Vérifie si une connexion peut être établie avec la chaîne donnée.
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1")  # Test minimal pour vérifier la connexion
        result = cursor.fetchone()
        assert result is not None, "Aucune donnée récupérée - la connexion semble échouer."
        assert result[0] == 1, "La requête de test ne retourne pas la valeur attendue."
        cursor.close()
        connection.close()
    except Exception as e:
        pytest.fail(f"Échec de connexion à la base de données : {e}")

def test_signup(client):
    # Test de l'inscription d'un nouvel utilisateur
    response = client.post('/signup', json={
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == 'User registered successfully!'

    # Test de la tentative d'inscription d'un utilisateur déjà existant
    response = client.post('/signup', json={
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 409
    assert response.get_json()['message'] == 'User already exists!'

def test_login(client):
    # Test de connexion avec un utilisateur existant
    # Créer un utilisateur avant de tester la connexion
    client.post('/signup', json={
        "username": "testuser2",
        "password": "testpassword"
    })
    
    response = client.post('/login', json={
        "username": "testuser2",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert 'token' in response.get_json()

    # Test de connexion avec un mot de passe incorrect
    response = client.post('/login', json={
        "username": "testuser2",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert response.get_json()['message'] == 'Invalid username or password!'

def test_get_items(client):
    # Test de récupération des articles
    response = client.get('/items')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert 'name' in data[0] and 'price' in data[0]
