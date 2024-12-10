from flask import Flask
from app.routes.user_routes import user_bp
from flask_sqlalchemy import SQLAlchemy

class App:
    def __init__(self):
        self.app = Flask(__name__)

        # Configuration de la base de données
        self.app.config['SQLALCHEMY_DATABASE_URI'] =  'mssql+pyodbc:///?odbc_connect=Driver={ODBC Driver 18 for SQL Server};Server=tcp:userdb-6e697eca91c8.database.windows.net,1433;Database=userdb;Uid=adminuser;Pwd={P@ssword123};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        # Initialiser la base de données
        init_db(self.app)

        # Enregistrer les Blueprints
        self.app.register_blueprint(user_bp, url_prefix='/users')

    def get_app(self):
        return self.app



db = SQLAlchemy()
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Crée les tables si elles n'existent pas encore


