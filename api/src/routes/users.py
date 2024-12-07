from flask import Blueprint, request, jsonify
from models.users import db, User

# Créer un blueprint pour les routes des utilisateurs
users_blueprint = Blueprint('users', __name__)

@users_blueprint.route('/add', methods=['POST'])
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

@users_blueprint.route('/all', methods=['GET'])
def get_all_users():
    """
    Récupérer tous les utilisateurs dans la base de données.
    """
    users = User.query.all()
    users_list = [{"id": user.id, "username": user.username, "email": user.email} for user in users]
    return jsonify(users_list), 200
