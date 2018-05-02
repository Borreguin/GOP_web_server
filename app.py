import datetime
import random

import binascii
import numpy as np
from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify
import json
import pandas as pd
import library_encrypt as en

# default code
app = Flask(__name__)

# Links for the main page:
links = [
    {"url": '/', "text": "Inicio"},
    {"url": '/test', 'text': "Nuevo Link"}
]


@app.route('/')
def hello_world():
    """ This is the MAIN PAGE of this Server Application"""
    # TODO: Create a default page
    return 'Hello World!'


""" A testing part ------------------------------------------------------------------------"""


@app.route("/test")
def test_page():
    """ Tests the use of templates and layouts"""
    school = {"school_name": 'prueba 1', "total_students": 32}
    return render_template('test/show_test.html', school=school)


@app.route("/test/<string:name>/")
def test(name):
    """ This is a testing path that include an argument called 'name' """
    return render_template('test/test.html', name=name)


@app.route("/layout/<string:name>/")
def layout(name):
    """ Testing a layout with name
        Ex: /layout/hero-twice
    """
    html = 'keen_io_dashboard/layouts/' + name + '/layout.html'
    title = 'General Title'
    titles = {'sbt1': "my subtitle 1", 'sbt2': "my subtitle 2"}
    notes = {'nt1': "my note 1", 'nt2': "my note 2"}
    return render_template(html, links=links, title=title, titles=titles, notes=notes)


@app.route("/map")
def create_map():
    map_data = json.load(open('./static/app_data/maps/ecuador_xy.json'))
    df_config = pd.read_excel('./static/app_data/maps/empr_electricas_por_provincia.xlsx')
    to_send = df_config.set_index('id').to_dict('index')
    title = "Creando un mapa"
    titles = {'sbt1': 'ECUADOR', 'sbt2': 'EMPTY'}
    notes = {'nt1': 'Este es un ejemplo de uso del mapa del Ecuador',
             'nt2': 'Sin nota'}
    return render_template('test/Ecuador_ Map_w_Template.html', map_data=map_data, map_config=to_send,
                           links=links, title=title, titles=titles, notes=notes)


""" End testing part ------------------------------------------------------------------------"""
""" PRODUCTION PART: Include new pages below this ___________________________________________"""


@app.route("/dashboard")
def test_dashboard():
    title = "Información Operativa en Tiempo Real"
    titles = {'sbt1': 'PRODUCCIÓN ENERGÉTICA (MWh)', 'sbt2': 'CURVA DE GENERACIÓN (MW)'}
    notes = {'nt1': 'Información preliminar, actualizada horariamente <br> Fuente: SCADA - CENACE',
             'nt2': 'Información preliminar, actualizada horariamente <br> Fuente: SCADA - CENACE'}

    data_panel = [
        {'id': 0, 'tag': 'tag1', 'label': 'Producción total', 'icon': 'static/my_icons/electrical/foco.png',
         'color': 'red'},
        {'id': 1, 'tag': 'tag2', 'label': 'EXPORTACIÓN', 'icon': 'static/my_icons/electrical/torre.png',
         'color': 'blue'},
        {'id': 2, 'tag': 'tag3', 'label': 'Hidráulica', 'icon': 'static/my_icons/electrical/hidroelectrica.png',
         'color': 'green'},
        {'id': 3, 'tag': 'tag4', 'label': 'Otra Generación', 'icon': 'static/my_icons/electrical/termoelectrica.png',
         'color': 'magenta'},
        {'id': 4, 'tag': 'tag5', 'label': 'No convencional', 'icon': 'static/my_icons/electrical/renovable.png',
         'color': 'black'}
    ]

    data_panel = en.encrypt_tag_obj(data_panel)
    # data_panel = en.decrypt_tag_obj(data_panel)
    return render_template('pages/ds_demanda.html',
                           links=links, title=title, titles=titles, notes=notes, data_panel=data_panel)

# ______________________________________________________________________________________________________
# __________________________________ WEB SERVICES FUNCTIONS ____________________________________________


@app.route("/tag/<string:tag_id>")
def get_snapshot(tag_id):
    try:
        tagname = en.decrypt(tag_id)
    except binascii.Error:
        tagname = 'Not encrypted'

    # connect with PI-Server
    result = {
        'id': tag_id,
        'tag': tagname,
        'timestamp': datetime.datetime.now(),
        'value': round(100*random.random(),2)
    }
    return jsonify(result)


if __name__ == '__main__':
    # app.run(host='10.30.2.45', port=5000)
    app.run()
