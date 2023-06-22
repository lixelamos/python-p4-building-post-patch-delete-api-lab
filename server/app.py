#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'


@app.route('/bakeries', methods=['GET', 'POST'])
def bakeries():
    if request.method == 'GET':
        bakeries = Bakery.query.all()
        bakeries_serialized = [bakery.to_dict() for bakery in bakeries]

        response = make_response(
            jsonify(bakeries_serialized),
            200
        )
        return response
    elif request.method == 'POST':
        name = request.form.get('name')
        # ... other bakery attributes

        bakery = Bakery(name=name)
        # ... set other bakery attributes

        db.session.add(bakery)
        db.session.commit()

        response = make_response(
            jsonify(bakery.to_dict()),
            201
        )
        return response


@app.route('/bakeries/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()

    if not bakery:
        response = make_response(
            jsonify({'message': 'Bakery not found'}),
             404
        )
        return response

    if request.method == 'GET':
        response = make_response(
            jsonify(bakery.to_dict()),
            200
        )
        return response

    elif request.method == 'PATCH':
        name = request.form.get('name')
        # ... other attributes to update

        bakery.name = name
        # ... update other bakery attributes

        db.session.commit()

        response = make_response(
            jsonify(bakery.to_dict()),
            200
        )
        return response

    elif request.method == 'DELETE':
        db.session.delete(bakery)
        db.session.commit()

        response = make_response(
            jsonify({'message': 'Bakery deleted successfully'}),
            200
        )
        return response
@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    name = request.form.get('name')
    # ... other baked good attributes

    baked_good = BakedGood(name=name)
    # ... set other baked good attributes

    db.session.add(baked_good)
    db.session.commit()

    response = make_response(
        jsonify(baked_good.to_dict()),
        201
    )
    return response

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get(id)

    if not baked_good:
        response = make_response(
            jsonify({'message': 'Baked good not found'}),
            404
        )
        return response

    db.session.delete(baked_good)
    db.session.commit()

    response = make_response(
        jsonify({'message': 'Baked good deleted successfully'}),
        200
    )
    return response


@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]

    response = make_response(
        jsonify(baked_goods_by_price_serialized),
        200
    )
    return response


@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()

    if not most_expensive:
        response = make_response(
            jsonify({'message': 'No baked goods found'}),
            404
        )
        return response

    response = make_response(
        jsonify(most_expensive.to_dict()),
        200
    )
    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
