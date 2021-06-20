"""My first Serverless Flask API!"""

# Import libraries
import json
import random
from flask import Flask, jsonify, make_response, request

from helpers import generator, find_id

# Create Flask application
app = Flask(__name__)


data_file = "dice.json"
with open(data_file) as f:
    DICE_BAG = json.load(f)['data']


@app.route('/dice/<int:id>')
def get_die(id:int):
    result = find_id(generator(DICE_BAG), id)
    if not result:
        return jsonify({'error': 'Could not find die with provided "id"'}), 404

    return jsonify(
        {
            'id': result.get('id'), 
            'name': result.get('name'), 
            'sides': result.get('sides')
        }
    )


@app.route('/roll/<int:id>/<int:numRolls>')
@app.route('/roll/<int:id>')
def roll_dice(id:int, numRolls:int=1):
    result = find_id(generator(DICE_BAG), id)
    if not result:
        return jsonify(
            {'error': 'Could not find die with provided "id"'}
        ), 404
    elif numRolls > 10:
        return jsonify({'error': 'You can\'t roll more than 10 times'}), 400
    elif numRolls < 1:
        return jsonify({'error': 'You need to roll a die at least once'}), 400

    id = result.get('id')
    name = result.get('name')
    sides = result.get('sides')
    rolls = [random.randint(1, sides) for _ in range(numRolls)]
    message = f'You rolled a {name} {numRolls} time(s) and got {rolls}!'
    return jsonify(
        [
            {
                'id': result.get('id'), 
                'name': result.get('name'), 
                'sides': result.get('sides')
            },
            {
                'message': message,
                'numRolls': numRolls,
                'rolls': rolls,
                'total': sum(rolls)
            }
        ]
    )


@app.route('/dice', methods=['POST'])
def create_die():
    id = request.json.get('id')
    name = request.json.get('name')
    sides = request.json.get('sides')
    if not id or not name or not sides:
        return jsonify(
            {'error': 'Please provide a "id", "name", and "sides"'}
        ), 400

    DICE_BAG.append({'id': id, 'name': name, 'sides': sides})

    return jsonify({'id': id, 'name': name, 'sides': sides})


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)
