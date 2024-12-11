import pytest
import jwt
from main import app, SECRET_KEY, items

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Génère un token valide pour les tests
def generate_token(username='test_user'):
    token = jwt.encode({'username': username}, SECRET_KEY, algorithm='HS256')
    return token

# Test de l'inscription
def test_signup(client):
    response = client.post('/signup', json={'username': 'test_user', 'password': 'password123'})
    assert response.status_code == 201
    assert response.get_json()['message'] == 'User registered successfully!'

    # Test de réinscription avec le même utilisateur
    response = client.post('/signup', json={'username': 'test_user', 'password': 'password123'})
    assert response.status_code == 409
    assert response.get_json()['message'] == 'User already exists!'

# Test de la connexion
def test_login(client):
    client.post('/signup', json={'username': 'test_user', 'password': 'password123'})
    response = client.post('/login', json={'username': 'test_user', 'password': 'password123'})
    assert response.status_code == 200
    assert 'token' in response.get_json()

    # Test avec des identifiants invalides
    response = client.post('/login', json={'username': 'test_user', 'password': 'wrongpassword'})
    assert response.status_code == 401
    assert response.get_json()['message'] == 'Invalid credentials!'

# Test d'accès à une route protégée
def test_protected_route(client):
    token = generate_token()
    response = client.get('/profile', headers={'x-access-token': token})
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Welcome, test_user!'

    # Test sans token
    response = client.get('/profile')
    assert response.status_code == 403
    assert response.get_json()['message'] == 'Token is missing!'

# Test de récupération des articles
def test_get_items(client):
    token = generate_token()
    response = client.get('/items', headers={'x-access-token': token})
    assert response.status_code == 200
    assert response.get_json() == items