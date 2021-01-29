#!/usr/bin/python3
"""
reviews view
"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models.review import Review
from models import storage
import json


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def reviews(place_id):
    """
    Return all reviews of a place
    """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]

    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def list_reviews(review_id):
    """
    Retrieves a review object
    """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    review = review.to_dict()

    return jsonify(review)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """
    deletes a review object
    """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """
    post a review object
    """
    place = storage.get("Place", place_id)
    if place is None:
            abort(404)

    if not request.json:
        abort(400, "Not a JSON")

    data = request.json
    if 'user_id' not in data.keys():
        abort(400, "Missing user_id")

    user = storage.get("User", data['user_id'])
    if user is None:
                abort(404)

    if 'text' not in data.keys():
        abort(400, "Missing text")

    data['place_id'] = place_id
    instance = Review(**data)
    storage.new(instance)
    storage.save()

    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """
    update a review object
    """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)

    if not request.json:
        abort(400, "Not a JSON")

    data = request.json
    for key, value in data.items():
        if key == 'user_id' or key == 'place_id':
            continue
        setattr(review, key, value)

    storage.save()

    return make_response(jsonify(review.to_dict()), 200)
