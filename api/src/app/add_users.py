from database import db
from models.user import User
from flask import Flask

# Initialiser l'application Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc:///?odbc_connect=Driver={ODBC Driver 18 for SQL Server};Server=tcp:userdb-6e697eca91c8.database.windows.net,1433;Database=userdb;Uid=adminuser;Pwd={P@ssword123};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Ajouter des utilisateurs
with app.app_context():
    user1 = User(username="JohnDoe", email="john@example.com", password="hashed_password_1")
    user2 = User(username="JaneDoe", email="jane@example.com", password="hashed_password_2")

    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    print("Users added successfully.")
