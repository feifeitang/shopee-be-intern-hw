from app import create_app
from flask_sqlalchemy import SQLAlchemy

app = create_app()
db = SQLAlchemy(app)


class Shop(db.Model):
    __tablename__ = 'shop'
    shop_id = db.Column(db.String(20), primary_key=True)
    is_official_shop = db.Column(db.Boolean, nullable=False)
    shop_location = db.Column(db.String(10), nullable=True)

    def __init__(self, shop_id, is_official_shop, shop_location):
        self.shop_id = shop_id
        self.is_official_shop = is_official_shop
        self.shop_location = shop_location
