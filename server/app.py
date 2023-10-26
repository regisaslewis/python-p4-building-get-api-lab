#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakery_list = []
    bakeries = Bakery.query.all()
    for n in bakeries:
        bakery_list.append(n.to_dict())
    return make_response(bakery_list, 200)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id = id).first()
    if bakery:
        body = bakery.to_dict()
        status = 200
    else:
        body = {"message": f"Bakery #{id} not found."}
        status = 404
    return make_response(body, status)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_list = []
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    for n in baked_goods_by_price:
        baked_goods_list.append(n.to_dict())
    return make_response(baked_goods_list, 200)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by("price").all()[-1]
    return make_response(most_expensive.to_dict(), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
