#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, hero_power 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

@app.route('/')
def home():
    return 'Page for Super-Heroes'

# @app.route('/heroes')

class Heroes(Resource):
    def get(self):
        # heroes=[hero.to_dict() for hero in Hero.query.all()]
        heroes=[]
        for hero in Hero.query.all():
            hero_data = {
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name
            }
        heroes.append(hero_data)
        response = make_response(jsonify(heroes), 200) 
        return response
    
api.add_resource(Heroes, '/heros')

class HeroById(Resource):
    def get(self, id):
        hero = Hero.query.filter_by(id=id).first()
        if hero:
            hero_dict={
                'id': hero.id,
                'name': hero.name,
                'super_name': hero.super_name,
                "powers": [
                    {
                        "id": power.id,
                        "name": power.name,
                        "description": power.description
                    }
                    for power in hero.powers
                ]
            }
            response = make_response(jsonify(hero_dict), 200)
            return response
    
        else:
            response_dict = {
                'error': ['Hero not found']
            }
            response = make_response(jsonify(response_dict), 404)
            return response
api.add_resource(HeroById, '/heros/<int:id>')

class Powers(Resource):
    def get(self):
        powers = []
        for power in Power.query.all():
            power_data ={
                'id' : power.id,
                'name' : power.name,
                'description' : power.description
            }
        powers.append(power_data)
        response = make_response(jsonify(powers), 200) 
        return response

api.add_resource(Powers, '/powers')

class PowerById(Resource):
    def get(self, id):
        power=Power.query.filter_by(id=id).first()
        if power:
            power_dict={
                'id' : power.id,
                'name' : power.name,
                'description' :power.description
            }
        
            response = make_response(jsonify(power_dict), 200)
            return response
        else:
            response_dict = {
                'error': ['Power not found']
            }
            response = make_response(jsonify(response_dict), 404)
            return response
    
    def patch (self, id):
        record= Power.query.filter_by(id=id).first()
        if record :
            for attr in request.form:
                setattr(record,attr,request.form.get(attr))
            db.session.add(record)
            db.session.commit()

            record_data={
                "id": record.id,
                "name" : record.name,
                "description" : record.description,
                "powers":[
                    {
                        "strength":power.strength,
                        "hero_id": power.hero_id
                    }
                    for power in record.powers
                ]
            }
            response = make_response(jsonify(record_data), 200)
            return response
        elif not record:
            response_dict ={
                'error':['Power not found']
            }
            response= make_response(jsonify(response_dict), 404)
            return response
        else:
            response_dict ={
                "errors":["validation errors"]
            }
            response=make_response(jsonify(response_dict), 401)
            return response
        
api.add_resource(PowerById, '/powers/<int:id>')

class HeroPowers(Resource):
    def post(self, id):
        hero = Hero.query.filter_by(id=id).first()
        power_id = request.form.get('power_id')

        if hero is None:
            response_dict = {
                'error': ['Hero not found']
            }
            response = make_response(jsonify(response_dict), 404)
            return response

        if len(hero.powers) >= MAXIMUM_HERO_POWERS:
            response_dict = {
                'error': ['Maximum number of powers reached for the hero']
            }
            response = make_response(jsonify(response_dict), 400)
            return response

        power = Power.query.get(power_id)
        if power is None:
            response_dict = {
                'error': ['Power not found']
            }
            response = make_response(jsonify(response_dict), 404)
            return response

        hero_strength = HeroPower(
            strength=request.form['strength'],
            power_id=power_id,
            hero_id=id
        )
        db.session.add(hero_strength)
        db.session.commit()

        response = make_response(jsonify(hero_strength.to_dict()), 200)
        return response

api.add_resource(HeroPowers, '/heropowers/<int:id>')



if __name__ == '__main__':
    app.run(port=5555)


    # elif request.method == 'POST':
    #     new_review = Review(
    #         score=request.form.get("score"),
    #         comment=request.form.get("comment"),
    #         game_id=request.form.get("game_id"),
    #         user_id=request.form.get("user_id"),
    #     )

    #     db.session.add(new_review)
    #     db.session.commit()

    #     review_dict = new_review.to_dict()

    #     response = make_response(
    #         jsonify(review_dict),
    #         201
    #     )

    #     return response