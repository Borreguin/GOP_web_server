from flask import Flask, flash, redirect, render_template, request, session, abort
import json

# default code
app = Flask(__name__)


@app.route('/')
def hello_world():
    """ This is the MAIN PAGE of this Server Application"""
    return 'Hello World!'


@app.route("/test/<string:name>/")
def test(name):
    """ This is a testing path """
    return render_template('test.html', name=name)


""" Include new pages below this """


@app.route("/map")
def create_map():
    map_data = json.load(open('./App_data/maps/ecuador_xy.json'))
    return render_template('Ecuador_Map.html', map_data=map_data)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=80)
