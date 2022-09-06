from app import create_app
from flask_sqlalchemy import SQLAlchemy

app = create_app()
db = SQLAlchemy(app)


class Item(db.Model):
    __tablename__ = 'item'
    item_id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(3000), nullable=True)
    tag = db.Column(db.String(60), nullable=True)
    historical_sold = db.Column(db.Integer, nullable=False)
    keyword_id = db.Column(db.Integer, nullable=False)
    shop_id = db.Column(db.String(20), nullable=False)

    def __init__(self, item_id, name, price, description, tag, historical_sold, keyword_id, shop_id):
        self.item_id = item_id
        self.name = name
        self.price = price
        self.description = description
        self.tag = tag
        self.historical_sold = historical_sold
        self.keyword_id = keyword_id
        self.shop_id = shop_id
