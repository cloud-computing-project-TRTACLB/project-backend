from database import db

class Basket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    items = db.relationship('Item', secondary='basket_items', backref='baskets')

    def __repr__(self):
        return f'<Basket {self.id}>'
