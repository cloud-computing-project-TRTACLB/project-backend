from flask import Blueprint, request, jsonify
from ..models.user import User
from app.database import db
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta

# Initialisation du Blueprint
user_bp = Blueprint('users', __name__)

# Clé secrète pour JWT
SECRET_KEY = "ton_secret_key_super_securisé"

# Route pour récupérer tous les utilisateurs
@user_bp.route('/all', methods=['GET'])
def get_all_users():
    users = User.query.all()
    users_list = [{"id": user.id, "username": user.username, "email": user.email} for user in users]
    return jsonify(users_list), 200

"""
# Route pour créer un utilisateur
@user_bp.route('/', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=generate_password_hash(data['password'])  # Hashage du mot de passe
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201
"""

@user_bp.route('/add', methods=['POST'])
def add_user():
    """
    Ajouter un utilisateur dans la base de données.
    Attente d'un JSON : {"username": "example", "email": "example@example.com"}
    """
    data = request.json
    if not data or not data.get('username') or not data.get('email'):
        return jsonify({"error": "Invalid input"}), 400

    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User added!", "user_id": new_user.id}), 201


# Route pour s'inscrire
@user_bp.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.json
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing data"}), 400

    # Vérifie si l'utilisateur existe déjà
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({"error": "Email already registered"}), 400

    # Crée un nouvel utilisateur
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=generate_password_hash(data['password'])  # Hashage du mot de passe
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# Route pour se connecter
@user_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing data"}), 400

    # Recherche l'utilisateur dans la base de données
    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({"error": "Invalid email or password"}), 401

    # Génère un token JWT
    token = jwt.encode(
        {"sub": user.id, "exp": datetime.utcnow() + timedelta(minutes=30)},
        SECRET_KEY,
        algorithm="HS256"
    )

    return jsonify({"access_token": token, "token_type": "bearer"}), 200
