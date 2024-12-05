import pytest
from main import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_all_candles(client):
    response = client.get('/candles')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_get_single_candle(client):
    response = client.get('/candles/1')
    assert response.status_code == 200
    assert response.get_json()['name'] == 'Lavender Candle'

def test_add_candle(client):
    new_candle = {'name': 'Citrus Candle', 'price': 11.99}
    response = client.post('/candles', json=new_candle)
    assert response.status_code == 201
    assert response.get_json()['name'] == 'Citrus Candle'

def test_update_candle(client):
    updated_data = {'price': 15.99}
    response = client.put('/candles/1', json=updated_data)
    assert response.status_code == 200
    assert response.get_json()['price'] == 15.99

def test_delete_candle(client):
    response = client.delete('/candles/1')
    assert response.status_code == 204
    # Verify it no longer exists
    response = client.get('/candles/1')
    assert response.status_code == 404
