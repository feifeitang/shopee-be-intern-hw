from flask_sqlalchemy import SQLAlchemy
import models.cluster
import models.item
import models.keyword
import models.shop

Cluster = models.cluster.Cluster
Item = models.item.Item
Keyword = models.keyword.Keyword
Shop = models.shop.Shop


def create_db(app):
    return SQLAlchemy(app)
