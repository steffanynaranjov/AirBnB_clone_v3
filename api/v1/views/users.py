#!/usr/bin/python3
"""
View users
"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    """
    Return all users
    """
    users = storage.all('User')
    users = [user.to_dict() for user in users.values()]

    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def list_users(user_id):
    """
    Retrieves a user object
    """
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    user = user.to_dict()

    return jsonify(user)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """
    deletes a user object
    """
    user = storage.get('User', user_id)
    if user is None:
        abort(404)

    storage.delete(user)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def post_user():
    """
    post a user object
    """
    if not request.json:
        abort(400, "Not a JSON")

    data = request.json
    if 'email' not in data.keys():
        abort(400, "Missing email")
    if 'password' not in data.keys():
        abort(400, "Missing password")

    instance = User(**data)
    storage.new(instance)
    storage.save()

    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
    update a user object
    """
    user = storage.get('User', user_id)
    if user is None:
        abort(404)

    if not request.json:
        abort(400, "Not a JSON")

    data = request.json
    for key, value in data.items():
        if key == 'email':
            continue
        setattr(user, key, value)

    storage.save()

    return make_response(jsonify(user.to_dict()), 200)
