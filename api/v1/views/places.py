#!/usr/bin/python3
"""
Places view
"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models.place import Place
from models import storage


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def places(city_id):
    """
    Return all places of a City
    """
    cities = storage.get('City', city_id)
    if cities is None:
        abort(404)
    places = [place.to_dict() for place in cities.places]

    return jsonify(places)


@app_views.route('/places/<place_id>', strict_slashes=False)
def list_places(place_id):
    """
    Retrieves a place object
    """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    place = place.to_dict()

    return jsonify(place)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
    deletes a place object
    """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """
    post a place object
    """
    if not request.json:
        abort(400, "Not a JSON")

    city = storage.get("City", city_id)
    if city is None:
            abort(404)

    data = request.json
    if 'user_id' not in data.keys():
        abort(400, "Missing user_id")

    user = storage.get("User", data['user_id'])
    if user is None:
                abort(404)

    if 'name' not in data.keys():
        abort(400, "Missing name")

    data['city_id'] = city_id
    instance = Place(**data)
    storage.new(instance)
    storage.save()

    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
    update a place object
    """
    if not request.json:
        abort(400, "Not a JSON")

    place = storage.get('Place', place_id)
    if place is None:
        abort(404)

    data = request.json
    for key, value in data.items():
        if key == 'user_id' or key == 'city_id':
            continue
        setattr(place, key, value)

    storage.save()

    return make_response(jsonify(place.to_dict()), 200)
