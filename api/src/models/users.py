from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
print('db est un objet de type', type(db),'et contient', db)
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    