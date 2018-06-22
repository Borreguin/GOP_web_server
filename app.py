""" coding: utf-8
Created by rsanchez on 03/05/2018
Este proyecto ha sido desarrollado en la Gerencia de Operaciones de CENACE
Mateo633
"""
import datetime
import random
from my_lib.PI_connection import pi_connect as osi
from my_lib.calculations import calculos as cal
from my_lib.calculations import consultas as con
import binascii
from flask import Flask, render_template, jsonify, redirect
import json
import pandas as pd
from encrypt import library_encrypt as en
import os
script_path = os.path.dirname(os.path.abspath(__file__))
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
    print(en.encrypt("/cal/energy_production"))
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
    notes = {'nt1': 'Información preliminar, actualizada cada 30 minutos <br> Fuente: SCADA - CENACE',
             'nt2': 'Información preliminar, actualizada cada 30 minutos <br> Fuente: SCADA - CENACE'}

    # Configurations for icon panel:
    data_panel = pd.read_excel("static/app_data/produccion_energetica/produccion_energetica.xlsx")
    data_panel = data_panel.to_dict('register')
    data_panel = en.encrypt_tag_obj(data_panel)
    # data_panel = en.decrypt_tag_obj(data_panel)

    # data for donut
    data_donut = cal.energy_production()
    
    # data for hydro_bar:
    data_bar_hydro = cal.generation_detail_now(['Embalse', 'Pasada'])

    # data for otra generacion bar:

    data_bar_otra = cal.other_generation_detail_now()

    return render_template('pages/ds_demanda.html',
                           links=links, title=title, titles=titles, notes=notes, data_panel=data_panel
                           , data_donut=data_donut, data_bar_hydro=data_bar_hydro, data_bar_otra=data_bar_otra)


# ______________________________________________________________________________________________________
# __________________________________ WEB SERVICES FUNCTIONS ____________________________________________


@app.route("/tag/<string:tag_id>")
def get_snapshot(tag_id):
    try:
        tagname = en.decrypt(tag_id)
    except binascii.Error:
        msg = 'Tag no encriptada'
        print('[get_snapshot]:' + msg)
        return jsonify({"error": msg})

    if '/cal/' in tagname or '/con/' in tagname:
        n = tagname[6:].find('/')
        params = None
        if n == -1:
            method = tagname[5:]
        else:
            method = tagname[5:n + 6]
            params = tagname[n + 7:]

        # if the request is calculated:
        if '/cal/' in tagname:
            return get_cal(method, params, tag_id)

        # if the request is a query:
        if '/con/' in tagname:
            return get_cons(method, params, tag_id)

    # connect with PI-Server
    pi_svr = osi.PIserver()
    pt = osi.PI_point(pi_svr, tagname)
    result = {
        'id': tag_id,
        'tag': tagname,
        'timestamp': pt.current_value().Timestamp.ToString(),
        'value': round(pt.current_value().Value, 2)
    }
    return jsonify(result)


@app.route("/cal/<string:cal_id_function>")
@app.route("/cal/<string:cal_id_function>/<string:parameters>")
def get_cal(cal_id_function, parameters=None, id_encrypt=None):

    try:
        method_to_call = getattr(cal, cal_id_function)
        if parameters is None:
            result = method_to_call()
        else:
            params = parameters.split("&")
            result = method_to_call(*params)

        if isinstance(result, dict):
            result['id'] = id_encrypt

        return jsonify(result)

    except Exception as e:
        print(e)
        msg = "[get_cal] [{0}] There is a error in module calc".format(cal_id_function)
        print("[" + script_path + "] \t" + msg)
        return jsonify({"error": msg})


@app.route("/con/<string:cons_id_function>")
@app.route("/con/<string:cons_id_function>/<string:parameters>")
def get_cons(cons_id_function, parameters=None, id_encrypt=None):

    try:
        method_to_call = getattr(con, cons_id_function)
        if parameters is None:
            result = method_to_call()
        else:
            params = parameters.split("&")
            result = method_to_call(*params)

        if isinstance(result, dict):
            result['id'] = id_encrypt

        return jsonify(result)

    except Exception as e:
        print(e)
        msg = "[get_cons] [{0}] There is an error in module cons".format(cons_id_function)
        print("[" + script_path + "] \t" + msg)
        return jsonify({"error": msg})


if __name__ == '__main__':
    # app.run(host='10.30.2.45', port=5000)

    app.run()
