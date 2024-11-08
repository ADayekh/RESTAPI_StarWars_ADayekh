"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def users_obtain():

    query_results = User.query.all()
    results = list(map(lambda item: item.serialize(), query_results))

    if results == []:
        return jsonify("Not users"), 404
    
    response_body = {
        "msg": "This is the list of users:",
        "users": results
    }
    return jsonify(response_body), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def singleuser_obtain(user_id):

    user = User.query.get(user_id)

    if user == None:
        return jsonify ("User doesn't exist"), 404
    
    response_body = {
        "msg": "The user is:",
        "user": user.serialize()
    }
    return jsonify(response_body), 200

@app.route('/planet', methods=['GET'])
def planets_obtain():

    query_results = Planet.query.all()
    results = list(map(lambda item: item.serialize(), query_results))

    if results == []:
        return jsonify("Not planets"), 404
    
    response_body = {
        "msg": "This is the list of planets:",
        "planets": results
    }
    return jsonify(response_body), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def singleplanet_obtain(planet_id):

    planet = Planet.query.get(planet_id)

    if planet == None:
        return jsonify ("Planet doesn't exist"), 404
    
    response_body = {
        "msg": "The planet is:",
        "planet": planet.serialize()
    }
    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def character_obtain():

    query_results = Character.query.all()
    results = list(map(lambda item: item.serialize(), query_results))

    if results == []:
        return jsonify("Not characters"), 404
    
    response_body = {
        "msg": "This is the list of characters:",
        "characters": results
    }
    return jsonify(response_body), 200

@app.route('/people/<int:character_id>', methods=['GET'])
def singlecharacter_obtain(character_id):

    character = Character.query.get(character_id)

    if character == None:
        return jsonify ("Character doesn't exist"), 404
    
    response_body = {
        "msg": "The character is:",
        "character": character.serialize()
    }
    return jsonify(response_body), 200

@app.route('/user/favorite', methods=['GET'])
def users_favorite_obtain():

    query_results = Favorite.query.all()
    results = list(map(lambda item: item.serialize(), query_results))

    if results == []:
        return jsonify("Not favorites"), 404
    
    response_body = {
        "msg": "This is the list of favorites:",
        "favorites": results
    }
    return jsonify(response_body), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):

    planet = Planet.query.get(planet_id)

    if planet == None:
        return jsonify ("Planet doesn't exist"), 404

    favorite = Favorite()
    favorite.user_id = 1
    favorite.planet_id = planet_id
    db.session.add(favorite)
    db.session.commit()
    response_body = favorite.serialize()

    return jsonify(response_body), 200
    
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    
    planet = Favorite.query.filter(Favorite.user_id == 1, Favorite.planet_id == planet_id).first()

    if planet == None:
        return ("Planet not found"), 404
    
    db.session.delete(planet)
    db.session.commit()

    return ("Planet deleted without problems"), 200

@app.route('/favorite/people/<int:character_id>', methods=['POST'])
def add_favorite_character(character_id):

    character = Character.query.get(character_id)

    if character == None:
        return jsonify ("Character doesn't exist"), 404
    
    favorite = Favorite()
    favorite.user_id = 1
    favorite.character_id = character_id
    db.session.add(favorite)
    db.session.commit()
    response_body = favorite.serialize()

    return jsonify(response_body), 200

@app.route('/favorite/people/<int:character_id>', methods=['DELETE'])
def delete_favorite_pcharacter(character_id):

    character = Favorite.query.filter(Favorite.user_id == 1, Favorite.character_id == character_id).first()

    if character == None:
        return ("Character not found"), 404
    
    db.session.delete(character)
    db.session.commit()

    return ("Character deleted without problems"), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
