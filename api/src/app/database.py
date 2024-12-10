from flask_sqlalchemy import SQLAlchemy

# Initialisation de l'instance SQLAlchemy
db = SQLAlchemy()

class Database:
    def __init__(self, app=None):
        """Initialise la base de données avec l'application Flask."""
        if app is not None:
            self.init_db(app)
    
    def init_db(self, app):
        """Configure la base de données avec l'application Flask et crée les tables si elles n'existent pas encore."""
        db.init_app(app)
        with app.app_context():
            db.create_all()  # Crée les tables si elles n'existent pas encore

# Exemple d'utilisation :
# app = Flask(__name__)
# database = Database(app)
