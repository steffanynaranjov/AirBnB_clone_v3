#!/usr/bin/python3
"""
View Amenities
"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, Response, make_response, request
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def amenities():
    """
    Return all amenities
    """
    all_amenities = storage.all('Amenity').values()
    amenities = []
    for obj in all_amenities:
        amenities.append(obj.to_dict())

    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def list_amenities(amenity_id):
    """
    Retrieves a amenity object
    """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    amenity = amenity.to_dict()

    return jsonify(amenity)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """
    deletes a amenity object
    """
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)

    storage.delete(amenity)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """
    post a amenity object
    """
    if not request.json:
        abort(400, "Not a JSON")
    data = request.json
    if 'name' not in data.keys():
        abort(400, "Missing name")
    instance = Amenity(**data)
    storage.new(instance)
    storage.save()

    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """
    update a amenity object
    """
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)

    if not request.json:
        abort(400, "Not a JSON")

    data = request.json
    for key, value in data.items():
        setattr(amenity, key, value)

    storage.save()

    return make_response(jsonify(amenity.to_dict()), 200)
