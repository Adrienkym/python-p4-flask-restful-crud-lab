#!/usr/bin/env python3

from flask import jsonify, request, make_response
from flask_restful import Api, Resource

from config import app, db
from models import Plant

api = Api(app)

class Plants(Resource):
    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)

    def post(self):
        data = request.get_json()
        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'],
            is_in_stock=data.get('is_in_stock', True)
        )
        db.session.add(new_plant)
        db.session.commit()
        return make_response(new_plant.to_dict(), 201)

api.add_resource(Plants, '/plants')


class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.filter_by(id=id).first()
        if not plant:
            return {"error": "Plant not found"}, 404
        return make_response(plant.to_dict(), 200)

    def patch(self, id):
        plant = Plant.query.filter_by(id=id).first()
        if not plant:
            return {"error": "Plant not found"}, 404
        data = request.get_json()
        for key, value in data.items():
            setattr(plant, key, value)
        db.session.commit()
        return make_response(plant.to_dict(), 200)

    def delete(self, id):
        plant = Plant.query.filter_by(id=id).first()
        if not plant:
            return {"error": "Plant not found"}, 404
        db.session.delete(plant)
        db.session.commit()
        return "", 204

api.add_resource(PlantByID, '/plants/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
