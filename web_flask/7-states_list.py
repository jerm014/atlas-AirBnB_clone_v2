#!/usr/bin/python3
""" task 6 """
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def root():
    return "Hello HBNB!"


@app.route('/hnbn', strict_slashes=False)
def hbnb():
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c(text):
    return "C {}".format(text.replace('_', ''))


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python(text="is cool"):
    return "Python {}".format(text.replace('_', ' '))


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    return "{} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n: int):
    if n % 2 == 0:
        value = 'even'
    else:
        value = 'odd'
    return render_template('6-number_odd_or_even.html', n=n, value=value)


@app.route('/states_list', strict_slashes=False)
def states_list():
    from models import storage
    states = dict(sorted(storage.all('State').items(), key=get_name))
    return render_template('7-states_list.html', states=states)


def get_name(item):
    key, value = item
    return value.name


@app.teardown_appcontext
def teardown(exc):
    from models import storage
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
