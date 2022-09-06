from app import create_app
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = create_app()
db = SQLAlchemy(app)


class Keyword(db.Model):
    __tablename__ = 'keyword'
    keyword_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, name, create_time):
        self.name = name
        self.create_time = create_time
