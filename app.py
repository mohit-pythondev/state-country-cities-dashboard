from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

# Toggle between MongoDB and JSON
USE_MONGODB = 0  # Set to True to use MongoDB, False to use JSON files

if USE_MONGODB:
    from flask_pymongo import PyMongo
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/countries-states-cities-database'  # Replace with your MongoDB URI
    mongo = PyMongo(app)

# Helper function to load JSON data
def load_json(filename):
    with open(os.path.join(os.getcwd(), filename), 'r', encoding='utf-8') as file:
        return json.load(file)

@app.route('/')
def index():
    if USE_MONGODB:
        regions = mongo.db.regions.find()
        regions_list = list(regions)
    else:
        regions_list = load_json('regions.json')
    return render_template('index.html', regions=regions_list)

@app.route('/subregions/<region_id>', methods=['GET'])
def get_subregions(region_id):
    if USE_MONGODB:
        subregions = mongo.db.subregions.find({'region_id': region_id})
        subregions_list = list(subregions)
    else:
        subregions = load_json('subregions.json')
        subregions_list = [subregion for subregion in subregions if subregion.get('region_id') == region_id]
    return render_template('subregions.html', subregions=subregions_list)

@app.route('/countries/<subregion_id>', methods=['GET'])
def get_countries(subregion_id):
    if USE_MONGODB:
        countries = mongo.db.countries.find({'subregion_id': subregion_id})
        countries_list = list(countries)
    else:
        countries = load_json('countries.json')
        countries_list = [country for country in countries if country.get('subregion_id') == subregion_id]
    return render_template('countries.html', countries=countries_list)

@app.route('/states/<country_id>', methods=['GET'])
def get_states(country_id):
    if USE_MONGODB:
        states = mongo.db.states.find({'country_id': country_id})
        states_list = list(states)
    else:
        states = load_json('states.json')
        states_list = [state for state in states if state.get('country_id') == country_id]
    return render_template('states.html', states=states_list)

@app.route('/cities/<state_id>', methods=['GET'])
def get_cities(state_id):
    if USE_MONGODB:
        cities = mongo.db.cities.find({'state_id': state_id})
        cities_list = list(cities)
    else:
        cities = load_json('cities.json')
        cities_list = [city for city in cities if city.get('state_id') == state_id]
    return render_template('cities.html', cities=cities_list)

if __name__ == '__main__':
    app.run(debug=True)
