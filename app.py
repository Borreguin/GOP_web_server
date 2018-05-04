""" coding: utf-8
Created by rsanchez on 03/05/2018
Este proyecto ha sido desarrollado en la Gerencia de Operaciones de CENACE
Mateo633
"""
import datetime
import random
from my_lib.PI_connection import pi_connect as PI
import binascii
from flask import Flask, render_template, jsonify
import json
import pandas as pd
from encrypt import library_encrypt as en

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

    data_panel = pd.read_excel("static/app_data/produccion_energetica/produccion_energetica.xlsx")
    data_panel = data_panel.to_dict('register')
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
        msg = 'Tag no encriptada'
        print('get_snapshot:' + msg)
        return jsonify({"error": msg})

    # connect with PI-Server
    pi_server = PI.PIServer('UIOSEDE-COMBAP')
    snapshot = pi_server.get_tag_snapshot(tagname)
    result = {
        'id': tag_id,
        'tag': tagname,
        'timestamp': snapshot.timestamp,
        'value': round(snapshot.value,2)
    }
    return jsonify(result)


if __name__ == '__main__':
    # app.run(host='10.30.2.45', port=5000)
    app.run()
