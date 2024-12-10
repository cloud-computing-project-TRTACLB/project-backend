import pytest
import jwt
from main import app, SECRET_KEY

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def generate_token():
    """Helper function to generate a valid JWT token."""
    return jwt.encode({'user': 'test_user'}, SECRET_KEY, algorithm='HS256')

def test_get_items(client):
    token = generate_token()
    response = client.get('/items', headers={'x-access-token': token})
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) > 0
    assert 'name' in data[0]

def test_get_items_no_token(client):
    response = client.get('/items')
    assert response.status_code == 403
    data = response.get_json()
    assert data['message'] == 'Token is missing!'

def test_get_items_invalid_token(client):
    response = client.get('/items', headers={'x-access-token': 'invalidtoken'})
    assert response.status_code == 403
    data = response.get_json()
    assert data['message'] == 'Token is invalid!'

def test_get_item(client):
    token = generate_token()
    response = client.get('/items/1', headers={'x-access-token': token})
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Lavender Candle'

def test_get_item_not_found(client):
    token = generate_token()
    response = client.get('/items/99', headers={'x-access-token': token})
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'item not found'

def test_add_item(client):
    token = generate_token()
    new_item = {'name': 'Cinnamon Candle', 'price': 15.99}
    response = client.post('/items', json=new_item, headers={'x-access-token': token})
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == new_item['name']
    assert data['price'] == new_item['price']

def test_update_item(client):
    token = generate_token()
    updated_data = {'name': 'Updated Lavender Candle', 'price': 13.99}
    response = client.put('/items/1', json=updated_data, headers={'x-access-token': token})
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == updated_data['name']
    assert data['price'] == updated_data['price']

def test_update_item_not_found(client):
    token = generate_token()
    updated_data = {'name': 'Non-existent Item'}
    response = client.put('/items/99', json=updated_data, headers={'x-access-token': token})
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'item not found'

def test_delete_item(client):
    token = generate_token()
    response = client.delete('/items/1', headers={'x-access-token': token})
    assert response.status_code == 204
    # Verify the item is deleted
    response = client.get('/items/1', headers={'x-access-token': token})
    assert response.status_code == 404

def test_delete_item_not_found(client):
    token = generate_token()
    response = client.delete('/items/99', headers={'x-access-token': token})
    assert response.status_code == 204
