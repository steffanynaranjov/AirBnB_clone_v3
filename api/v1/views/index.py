#!/usr/bin/python3
"""
Create routes for status api,
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.engine.db_storage import classes


@app_views.route('/status')
def api_status():
    """
    Return status ok
    """
    return jsonify({
        "status": "OK"
    })


@app_views.route('/stats')
def api_stats():
    """
    Return count of each table / model
    """
    count = {}

    for model in classes:
        name = classes[model].__tablename__
        count[name] = storage.count(model)

    return jsonify(count)
