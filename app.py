""" coding: utf-8
Created by rsanchez on 03/05/2018
Este proyecto ha sido desarrollado en la Gerencia de Operaciones de CENACE
Mateo633
"""
import datetime
import warnings

import plotly.utils as plt_u

from my_lib.PI_connection import pi_connect as osi
from my_lib.calculations import calculos as cal
from my_lib.calculations import consultas as con
from my_lib.hmm import real_time_application as hmm_ap
from my_lib.encrypt import library_encrypt as en

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)

import binascii
from flask import Flask, render_template, jsonify
import json
import pandas as pd

import os
script_path = os.path.dirname(os.path.abspath(__file__))
# default code
app = Flask(__name__)

# ______________________________________________________________________________________________________________#
# ________________________________        GENERAL        VARIABLES       _______________________________________

# Links for the main page:
links = [
    {"url": '/', "text": "Inicio"},
    {"url": '/test', 'text': "Nuevo Link"}
]

hmm_modelPath = './hmm_application/model/'          # Model path
file_dataPath = './hmm_application/data/'           # File data path

# ______________________________________________________________________________________________________________#

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


@app.route('/plot_test')
def index():
    import numpy as np
    rng = pd.date_range('1/1/2011', periods=7500, freq='H')
    ts = pd.Series(np.random.randn(len(rng)), index=rng)

    graphs = [ dict( data=[ dict( x=[1, 2, 3], y=[10, 20, 30], type='scatter'),],
            layout=dict(title='first graph')),
            dict(data=[ dict( x=[1, 3, 5], y=[10, 50, 30], type='bar'),],
            layout=dict(title='second graph')),
        dict(data=[dict( x=ts.index,  # Can use the pandas data structures directly
                y=ts)])]

    # Add "ids" to each of the graphs to pass up to the client
    # for templating
    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]

    # Convert the figures to JSON
    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
    # objects to their JSON equivalents
    graphJSON = json.dumps(graphs, cls=plt_u.PlotlyJSONEncoder)

    return render_template('test/index.html',
                           ids=ids, graphJSON=graphJSON)


""" End testing part ------------------------------------------------------------------------"""
""" PRODUCTION PART: Include new pages below this ___________________________________________"""


@app.route("/dashboard")
def prepare_dashboard():
    title = "Información Operativa en Tiempo Real"
    titles = {'sbt1': 'PRODUCCIÓN ENERGÉTICA (MWh)', 'sbt2': 'CURVA DE GENERACIÓN (MW)'}
    notes = {'nt1': 'Información preliminar, actualizada cada 30 minutos, Fuente: SCADA - CENACE',
             'nt2': 'Información preliminar, actualizada cada 30 minutos, Fuente: SCADA - CENACE'}

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


@app.route("/pronostico/<string:entity>/<string:date>/<string:hour>")
@app.route("/pronostico/<string:entity>/<string:date>/")
@app.route("/pronostico/<string:entity>/<string:date>")
@app.route("/pronostico/<string:entity>/")
@app.route("/pronostico/<string:entity>")
@app.route("/pronostico")
def forecasting(entity="menu", date=None, hour=None):

    msg = ""
    model_name, tag_name, description, data_name, datetime_ini, datetime_fin = None, None, None, None, None, None

    if date is None:
        date = datetime.datetime.now().strftime("%Y-%m-%d")
    if hour is None:
        hour = datetime.datetime.now().strftime("%H:%M:%S")

    try:
        df_config = pd.read_excel("./hmm_application/config.xlsx")
        df_config.set_index("entity", inplace=True)
        description = df_config.at[entity,'description']
    except Exception as e:
        print(e)
        msg += "\n No existe la entidad: " + entity

    if msg != "":
        return msg

    # graphJSON = graph_pronostico_demanda(description, date, hour)

    title = "Pronóstico de la demanda en tiempo real"
    titles = {'sbt1': description, 'sbt2': ''}
    notes = {'nt1': 'Información preliminar, actualizada cada 15 minutos, Fuente: SCADA - CENACE',
             'nt2': 'Información preliminar, actualizada cada 15 minutos,  Fuente: SCADA - CENACE'}

    links_demand = [
        {"url": '/pronostico/demanda-nacional/{0}/{1}'.format(date, hour), "text": "Nacional"},
        {"url": '/pronostico/electrica-quito/{0}/{1}'.format(date, hour), 'text': "Quito"}
    ]
    return render_template('pages/pronostico.html',
                           links=links_demand, title=title, titles=titles, notes=notes, date=date, hour=hour)


@app.route("/grafica_pronostico/<string:description>/<string:date>/<string:hour>/<string:style>")
def graph_pronostico_demanda(description, date=None, hour=None, style="default"):

    if date is None:
        date = datetime.datetime.now().strftime("%Y-%m-%d")
    if hour is None:
        hour = datetime.datetime.now().strftime("%H:%M:%S")

    try:
        datetime_ini = datetime.datetime.strptime(date, '%Y-%m-%d')
        datetime_fin = datetime.datetime.strptime(date + " " + hour, '%Y-%m-%d %H:%M:%S')
    except Exception as e:
        msg = "Ingrese fecha en el siguiente formato (/yyy-mm-dd/H:M:S)  Ejemplo: /2018-01-01/16:32:12"
        print(e, msg)
        return {'graph':{}, layout:{}}

    df_config = pd.read_excel("./hmm_application/config.xlsx")
    df_config.set_index("description", inplace=True)
    model_name = df_config.at[description, 'model_name']
    tag_name = df_config.at[description, 'tag']
    despacho = df_config.at[description, 'despacho']
    data_name = model_name.replace("hmm_", "")

    hmm_modelPath_file = hmm_modelPath + model_name
    file_dataPath_file = file_dataPath + data_name

    graph = hmm_ap.graphic_pronostico_demanda(hmm_modelPath_file, file_dataPath_file, tag_name, despacho,
                                              datetime_ini, datetime_fin, style)

    # Convert the figures to JSON ( PlotlyJSONEncoder appropriately converts pandas, datetime, etc)
    # objects to their JSON equivalents
    json_graph = json.dumps(graph, cls=plt_u.PlotlyJSONEncoder)
    return json_graph


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
    app.run(host='10.30.2.45', port=80)
    # app.run(host='127.0.0.1', port=80)
    #app.run()
