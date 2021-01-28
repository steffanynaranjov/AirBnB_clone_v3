#!/usr/bin/python3
"""
Create routes for status api,
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route('/status')
def api_status():
    """
    Return status ok
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def api_stats():
    """
    endpoint
    """
   objects = {"amenities": storage.count("Amenity"),
               "cities": storage.count("City"),
               "places": storage.count("Place"),
               "reviews": storage.count("Review"),
               "states": storage.count("State"),
               "users": storage.count("User")}
    return jsonify(objects)
