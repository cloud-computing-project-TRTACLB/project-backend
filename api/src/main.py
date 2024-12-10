import sys
import os

# Ajouter le répertoire parent (api) au chemin de recherche
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from flask import Flask
from utils import init_db
from app.routes.user_routes import user_bp  # Assure-toi que c'est le bon chemin vers ton fichier de routes

# Créer l'application Flask
app = Flask(__name__)

# Configuration de la base de données
##On doit changer le server ???
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc:///?odbc_connect=Driver={ODBC Driver 18 for SQL Server};Server=tcp:userdb-6e697eca91c8.database.windows.net,1433;Database=userdb;Uid=adminuser;Pwd={P@ssword123};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialiser la base de données
init_db(app)
print(user_bp)

# Enregistrer les Blueprints
app.register_blueprint(user_bp, url_prefix='/users')

if __name__ == "__main__":
    app.run(debug=True)

