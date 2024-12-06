from flask import Flask
from app.database import init_db

def create_app():
    app = Flask(__name__)
    
    # Configuration de la base de données (Azure)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://<user>:<password>@<host>/<database>'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialiser la base de données
    init_db(app)
    
    # Enregistrer les routes
    from app.routes import init_routes
    init_routes(app)

    return app
