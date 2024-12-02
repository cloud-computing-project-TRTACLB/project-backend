from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data
candles = [
    {'id': 1, 'name': 'Lavender Candle', 'price': 12.99},
    {'id': 2, 'name': 'Vanilla Candle', 'price': 10.99},
    {'id': 3, 'name': 'Rose Candle', 'price': 14.99}
]

@app.route('/candles', methods=['GET'])
def get_candles():
    return jsonify(candles)

@app.route('/candles/<int:candle_id>', methods=['GET'])
def get_candle(candle_id):
    candle = next((c for c in candles if c['id'] == candle_id), None)
    if candle is None:
        return jsonify({'error': 'Candle not found'}), 404
    return jsonify(candle)

@app.route('/candles', methods=['POST'])
def add_candle():
    new_candle = request.get_json()
    new_candle['id'] = len(candles) + 1
    candles.append(new_candle)
    return jsonify(new_candle), 201

@app.route('/candles/<int:candle_id>', methods=['PUT'])
def update_candle(candle_id):
    candle = next((c for c in candles if c['id'] == candle_id), None)
    if candle is None:
        return jsonify({'error': 'Candle not found'}), 404
    updated_data = request.get_json()
    candle.update(updated_data)
    return jsonify(candle)

@app.route('/candles/<int:candle_id>', methods=['DELETE'])
def delete_candle(candle_id):
    global candles
    candles = [c for c in candles if c['id'] != candle_id]
    return '', 204

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)