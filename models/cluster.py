from app import create_app
from flask_sqlalchemy import SQLAlchemy

app = create_app()
db = SQLAlchemy(app)


class Cluster(db.Model):
    __tablename__ = 'cluster'
    cluster_id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    gross_income = db.Column(db.Integer, nullable=False)
    keyword_id = db.Column(db.Integer, nullable=False)

    def __init__(self, number, gross_income, keyword_id):
        self.number = number
        self.gross_income = gross_income
        self.keyword_id = keyword_id
