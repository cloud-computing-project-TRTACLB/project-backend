from flask import Flask, jsonify, request
from functools import wraps
import jwt
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

app = Flask(__name__)

# Retrieve the secret key from the environment
SECRET_KEY = os.getenv('SECRET_KEY')

# Sample data
items = [
    {'id': 1, 'name': 'Lavender Candle', 'price': 12.99},
    {'id': 2, 'name': 'Vanilla Candle', 'price': 11.99},
    {'id': 3, 'name': 'Rose Candle', 'price': 19.99}
]

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(*args, **kwargs)
    return decorated

@app.route('/items', methods=['GET'])
@token_required
def get_items():
    return jsonify(items)

@app.route('/items/<int:item_id>', methods=['GET'])
@token_required
def get_item(item_id):
    item = next((c for c in items if c['id'] == item_id), None)
    if item is None:
        return jsonify({'error': 'item not found'}), 404
    return jsonify(item)

@app.route('/items', methods=['POST'])
@token_required
def add_item():
    new_item = request.get_json()
    new_item['id'] = len(items) + 1
    items.append(new_item)
    return jsonify(new_item), 201

@app.route('/items/<int:item_id>', methods=['PUT'])
@token_required
def update_item(item_id):
    item = next((c for c in items if c['id'] == item_id), None)
    if item is None:
        return jsonify({'error': 'item not found'}), 404
    updated_data = request.get_json()
    item.update(updated_data)
    return jsonify(item)

@app.route('/items/<int:item_id>', methods=['DELETE'])
@token_required
def delete_item(item_id):
    global items
    items = [c for c in items if c['id'] != item_id]
    return '', 204

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
