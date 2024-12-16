from flask import Flask, jsonify, request
from functools import wraps
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
import datetime
import pyodbc
# Load the .env file
load_dotenv()

# Charger les informations de connexion à la base de données depuis les variables d'environnement
private_endpoint_ip = os.getenv('PRIVATE_ENDPOINT_IP')
SQL_CONNECTION_STRING = os.getenv('SQL_CONNECTION_STRING')
app = Flask(__name__)

# Retrieve the secret key from the environment
SECRET_KEY = os.getenv("SECRET_KEY")
print("Secret key:", SECRET_KEY)  # Debugging
print("SQL connection string:", SQL_CONNECTION_STRING)  # Debugging
# In-memory user database
users = {}

# Sample data
items = [
    {'id': 1, 'name': 'Lavender Candle', 'price': 13.99},
    {'id': 2, 'name': 'Vanilla Candle', 'price': 11.99},
    {'id': 3, 'name': 'Rose Candle', 'price': 19.99}
]

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        print(f"Received token: {token}")
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user = data['username']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(*args, **kwargs)
    return decorated

# Exemple de connexion à la base de données SQL Azure
def get_db_connection():
    connection = pyodbc.connect(SQL_CONNECTION_STRING)
    return connection
# Route for user registration (signup)
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = str(data.get('password'))

    if not username or not password:
        return jsonify({'message': 'Username and password are required!'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    # Check if the user already exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    existing_user = cursor.fetchone()
    if existing_user:
        cursor.close()
        connection.close()
        return jsonify({'message': 'User already exists!'}), 409

    # Hash the password for storage
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    try:
        # Insert the new user into the database
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        connection.commit()
    except Exception as e:
        cursor.close()
        connection.close()
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500

    cursor.close()
    connection.close()
    return jsonify({'message': 'User registered successfully!'}), 201




# Route for user login (authentication)
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = str(data.get('password'))

    if not username or not password:
        return jsonify({'message': 'Username and password are required!'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    # Check if the user exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()

    if not user or not check_password_hash(user[1], password):
        return jsonify({'message': 'Invalid username or password!'}), 401

    expiration = datetime.datetime.now() + datetime.timedelta(hours=1)
    # Generate a token
    token = jwt.encode({
        'username': username,
        'exp': expiration
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({'token': token})

# Route for getting items
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

# Protected route example
@app.route('/profile', methods=['GET'])
@token_required
def profile():
    return jsonify({'message': f'Welcome, {request.user}!'})




# Utilisation de cette connexion dans une route
@app.route('/data', methods=['GET'])
def get_data():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM my_table")  # Exemple de requête
    rows = cursor.fetchall()
    return jsonify({'data': rows})

@app.route('/data', methods=['POST'])
def post_data():
                data = request.get_json()
                if not data:
                    return jsonify({'message': 'No data provided!'}), 400

                connection = get_db_connection()
                cursor = connection.cursor()

                # Assuming the data contains 'name' and 'value' fields
                name = data.get('name')
                value = data.get('value')

                if not name or not value:
                    return jsonify({'message': 'Name and value are required!'}), 400

                try:
                    cursor.execute("INSERT INTO my_table (name, value) VALUES (?, ?)", (name, value))
                    connection.commit()
                except Exception as e:
                    return jsonify({'message': f'An error occurred: {str(e)}'}), 500
                finally:
                    cursor.close()
                    connection.close()

                return jsonify({'message': 'Data inserted successfully!'}), 201
   
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 80)))