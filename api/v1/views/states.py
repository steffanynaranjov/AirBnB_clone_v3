#!/usr/bin/python3
""" States Views """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route("/states", methods=["GET"])
def all_states():
    """Retrieves all states with a list of objects"""
    list = []
    s = storage.all('State').values()
    for v in s:
        list.append(v.to_dict())
    return jsonify(list)


@app_views.route("/states/<id>", methods=["GET"])
def id_state(id):
    """id state retrieve json object"""
    s = storage.all('State').values()
    for v in s:
        if v.id == id:
            return jsonify(v.to_dict())
    abort(404)


@app_views.route("/states/<id>", methods=["DELETE"])
def del_state(id):
    """delete state with id"""
    state = storage.get('State', id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def state_new():
    """Creates a new state"""
    state_data = request.get_json()
    if state_data is None:
        abort(400, "Not a JSON")
    if not state_data.get('name'):
        abort(400, "Missing name")
    new_state = State(**state_data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<id>', methods=['PUT'])
def state_upt(id):
    """Update a State object"""
    x = request.get_json()
    if x is None:
        abort(400, "Not a JSON")
    ignore = ['id', 'created_at', 'updated_at']
    state = storage.get("State", id)
    if state is None:
        abort(404)
    for k, v in x.items():
        if k not in ignore:
            setattr(state, k, v)
    state.save()
    return jsonify(state.to_dict()), 200
