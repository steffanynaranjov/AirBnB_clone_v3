#!/usr/bin/python3
""" States Views """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=['POST'])
def create_state():
    """
    Create new State
    """
    r_json = request.get_json()

    if not r_json:
        abort(400, "Not a JSON")
    elif not r_json.get('name'):
        abort(400, 'Missing name')

    nobj = State(**r_json)
    nobj.save()

    nobj = nobj.to_dict()
    return jsonify(nobj), 201


@app_views.route('/states', methods=['GET'])
def all_states():
    """
    Get all States
    """
    states = storage.all('State')
    states_list = []

    for state in states.values():
        states_list.append(state.to_dict())

    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """
    Get State by Id
    """
    state = storage.get('State', state_id)

    if state:
        return jsonify(state.to_dict())

    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def del_state(state_id):
    """
    Delete State by Id
    """
    state = storage.get('State', state_id)

    if state:
        storage.delete(state)
        storage.save()

        return jsonify({})

    abort(404)


@app_views.route('/states/<state_id>', methods=['PUT'])
def put_state(state_id):
    """
    Update State by Id
    """
    r_json = request.get_json()

    if not r_json:
        abort(400, "Not a JSON")

    state = storage.get('State', state_id)

    if state:
        r_json.pop('created_at', 0)
        r_json.pop('updated_at', 0)
        r_json.pop('id', 0)

        for attr in r_json:
            if hasattr(state, attr):
                state.__setattr__(attr, r_json[attr])

        state.save()

        return jsonify(state.to_dict())

    abort(404)
