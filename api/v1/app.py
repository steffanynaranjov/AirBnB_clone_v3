#!/usr/bin/python3
"""
Create app flask
"""
from flask import Flask, make_response, jsonify
from api.v1.views import app_views
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(self):
    """
    Close storage
    """
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """
    Handle 404 code
    """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', 5000)
    app.run(host, port, threaded=True)
