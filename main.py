from app import create_app
from datetime import datetime
from flask import jsonify
from flask import request
from flask_marshmallow import Marshmallow
import models
from services.CalcMarketSize import CalcMarketSize

# init app
app = create_app()

# init db
db = models.create_db(app)

# init ma
ma = Marshmallow(app)


class ClusterSchema(ma.Schema):
    class Meta:
        fields = ('cluster_id', 'number', 'gross_income')


class ItemSchema(ma.Schema):
    class Meta:
        fields = ('item_id', 'name', 'price',
                  'description', 'tag', 'historical_sold')


class KeywordSchema(ma.Schema):
    class Meta:
        fields = ('keyword_id', 'name', 'create_time')


cluster_schema = ClusterSchema()
clusters_schema = ClusterSchema(many=True)

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

keyword_schema = KeywordSchema()
keywords_schema = KeywordSchema(many=True)


@app.route('/cluster', methods=['GET'])
def get_clusters():
    all_clusters = models.Cluster.query.all()
    result = clusters_schema.dump(all_clusters)
    print(result)
    return jsonify(result)


@app.route('/item', methods=['POST'])
def add_item():
    item_id = request.json['item_id']
    name = request.json['name']
    price = request.json['price']
    description = request.json['description']
    tag = request.json['tag']
    historical_sold = request.json['historical_sold']
    keyword_id = request.json['keyword_id']
    shop_id = request.json['shop_id']

    new_item = (item_id, name, price, description,
                tag, historical_sold, keyword_id, shop_id)

    db.session.add(new_item)
    db.session.commit()

    return item_schema.jsonify(new_item)


@app.route('/item', methods=['GET'])
def get_items():
    all_items = models.Item.query.all()
    result = items_schema.dump(all_items)
    print(result)
    return jsonify(result)


@app.route('/item/<id>', methods=['GET'])
def get_item(id):
    item = models.Item.query.get(id)
    return item_schema.jsonify(item)


@app.route('/item/<id>', methods=['PUT'])
def update_item(id):
    item = models.Item.query.get(id)

    name = request.json['name']
    price = request.json['price']
    description = request.json['description']
    tag = request.json['tag']
    historical_sold = request.json['historical_sold']

    item.name = name
    item.price = price
    item.description = description
    item.tag = tag
    item.historical_sold = historical_sold

    db.session.commit()

    return item_schema.jsonify(item)


@app.route('/item/<id>', methods=['DELETE'])
def delete_item(id):
    item = models.Item.query.get(id)
    db.session.delete(item)
    db.session.commit()

    return item_schema.jsonify(item)


@app.route('/keyword', methods=['POST'])
def add_keyword():
    name = request.json['name']
    create_time = datetime.now

    new_keyword = (name, create_time)

    db.session.add(new_keyword)
    db.session.commit()

    return keyword_schema.jsonify(new_keyword)


@app.route('/keyword/<name>', methods=['GET'])
def get_keyword(name):
    try:
        keyword = models.Keyword.query.get(name)
        return keyword_schema.jsonify(keyword)
    except Exception as e:
        print('get_keyword error:', str(e))


@app.route('/crawler/<keyword>', methods=['GET'])
def crawler(keyword):
    keyword = keyword.encode('cp1252').decode('utf8')
    print('keyword', keyword)
    from tasks import crawler
    r = crawler.delay(keyword)

    return jsonify({'status': 'OK'})


@app.route('/calcMarketSize', methods=['GET'])
def calc_market_size():
    CalcMarketSize.calc_market_size()

    return jsonify({'status': 'OK'})


# @app.route('/')
# def index():
#     # Create data
#     db.create_all()

#     return jsonify({'status': 'OK'})


# run server
if __name__ == "__main__":
    app.run(debug=True)
