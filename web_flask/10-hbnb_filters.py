#!/usr/bin/python3
""" process 10-hbnb_filters.py with 10-hbnb_filters.html """
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """ load cities and states and amenities for 10-hbnb_filters.html """
    amenities = storage.all('Amenity').values()
    sorted_amenities = sorted(amenities, key=lambda a: a.name)

    states = storage.all('State').values()
    sorted_states = sorted(states, key=lambda s: s.name)

    cities = storage.all('City').values()
    sorted_cities = sorted(cities, key=lambda c: c.name)

    return render_template('10-hbnb_filters.html',
                           amenities=sorted_amenities,
                           states=sorted_states,
                           cities=sorted_cities)


@app.teardown_appcontext
def close_db_session(exception=None):
    """close session after each request."""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
