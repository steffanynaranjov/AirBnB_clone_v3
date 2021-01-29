#!/usr/bin/python3
"""places_review Module"""
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from flask import abort, jsonify, request


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def reviews(place_id):
    """Retrieves the list of all reviews in a place objects"""
    place = storage.get(Place, place_id)
    reviews_list = []
    if place is None:
        abort(404)
    for place in place.reviews:
        reviews_list.append(place.to_dict())
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def review_by_id(review_id):
    """Retrieves a review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a review in a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    request_dict = request.get_json()
    if request_dict is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in request_dict:
        abort(400, 'Missing user_id')
    user_id = request_dict['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if 'text' not in request_dict:
        abort(400, 'Missing text')
    review = Review(**request_dict)
    review.place_id = place_id
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates a review object"""
    request_dict = request.get_json()
    if request_dict is None:
        abort(400, 'Not a JSON')
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    for key, value in request_dict.items():
        if key != 'id' and key != 'user_id' and key != 'place_id' \
                and key != 'created_at' and key != 'updated_at':
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict())
