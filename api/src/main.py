from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data
items = [
    {'id': 1, 'name': 'Lavender Candle', 'price': 12.99},
    {'id': 2, 'name': 'Vanilla Candle', 'price': 11.99},
    {'id': 3, 'name': 'Rose Candle', 'price': 19.99}
]

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((c for c in items if c['id'] == item_id), None)
    if item is None:
        return jsonify({'error': 'item not found'}), 404
    return jsonify(item)

@app.route('/items', methods=['POST'])
def add_item():
    new_item = request.get_json()
    new_item['id'] = len(items) + 1
    items.append(new_item)
    return jsonify(new_item), 201

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = next((c for c in items if c['id'] == item_id), None)
    if item is None:
        return jsonify({'error': 'item not found'}), 404
    updated_data = request.get_json()
    item.update(updated_data)
    return jsonify(item)

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global items
    items = [c for c in items if c['id'] != item_id]
    return '', 204

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)