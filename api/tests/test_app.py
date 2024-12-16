import pytest
import jwt
from main import app, SECRET_KEY, items
import os
import pyodbc

sql_connection_string = os.getenv('SQL_CONNECTION_STRING')
sql_connection ="mssql+pyodbc:///?odbc_connect=Driver={ODBC Driver 18 for SQL Server};Server=tcp:"+sql_connection_string+",1433;Database=userdb;Uid=adminuser;Pwd={P@ssword123};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
        
def test_db_connection():
    """
    Test la connexion à la base de données.
    Vérifie si une connexion peut être établie avec la chaîne donnée.
    """
    sql_connection_string = os.getenv("SQL_CONNECTION_STRING")
    assert sql_connection_string is not None, "La variable d'environnement SQL_CONNECTION_STRING est manquante."

    try:
        connection = pyodbc.connect(sql_connection)
        cursor = connection.cursor()
        cursor.execute("SELECT 1")  # Test minimal pour vérifier la connexion
        result = cursor.fetchone()
        assert result is not None, "Aucune donnée récupérée - la connexion semble échouer."
        assert result[0] == 1, "La requête de test ne retourne pas la valeur attendue."
        cursor.close()
        connection.close()
    except Exception as e:
        pytest.fail(f"Échec de connexion à la base de données : {e}")

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