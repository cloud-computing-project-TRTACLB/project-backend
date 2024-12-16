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
sql_connection_string = os.getenv('SQL_CONNECTION_STRING')

sql_connection ="mssql+pyodbc:///?odbc_connect=Driver={ODBC Driver 18 for SQL Server};Server=tcp:"+sql_connection_string+",1433;Database=userdb;Uid=adminuser;Pwd={P@ssword123};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
app = Flask(__name__)

# Retrieve the secret key from the environment
SECRET_KEY = os.getenv("SECRET_KEY")
print("Secret key:", SECRET_KEY)  # Debugging
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

# Route for user registration (signup)
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    print("Received data:", data)  # Debugging
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required!'}), 400

    if username in users:
        return jsonify({'message': 'User already exists!'}), 400

    hashed_password = generate_password_hash(password, method='sha256')
    users[username] = {'password': hashed_password}

    # Insert the new user into the database
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        connection.commit()
    except Exception as e:
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify({'message': 'User registered successfully!'}), 201



# Route for user login (authentication)
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print("Received data:", data)  # Debugging
    username = data.get('username')
    password = str(data.get('password'))

    if not username or not password:
        return jsonify({'message': 'Username and password are required!'}), 400

    user = users.get(username)
    if not user or not check_password_hash(user['password'], password):
        return jsonify({'message': 'Invalid credentials!'}), 401
    expiration = datetime.datetime.now() + datetime.timedelta(hours=1)
    # Generate a JWT token
    token = jwt.encode({
        'username': username,
        'exp': expiration
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({'token': token})

# Protected route example
@app.route('/profile', methods=['GET'])
@token_required
def profile():
    return jsonify({'message': f'Welcome, {request.user}!'})

# Route for getting items
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

# Exemple de connexion à la base de données SQL Azure
def get_db_connection():
    connection = pyodbc.connect(sql_connection)
    return connection

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