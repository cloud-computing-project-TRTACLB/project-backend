from flask import Blueprint, jsonify
from models.basket import Basket

basket_bp = Blueprint('baskets', __name__)

@basket_bp.route('/', methods=['GET'])
def get_baskets():
    baskets = Basket.query.all()
    return jsonify([{"id": b.id, "user_id": b.user_id} for b in baskets])
