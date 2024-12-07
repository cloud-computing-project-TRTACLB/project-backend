from flask import Flask
from models.users import db
from routes.users import users_blueprint

app = Flask(__name__)
app.config.from_pyfile('config.py')

# Initialiser la base de données
db.init_app(app)

with app.app_context():
    db.create_all()


# Enregistrer les blueprints
app.register_blueprint(users_blueprint, url_prefix='/users')

if __name__ == '__main__':
    app.run(debug=True)
