# -*- coding: utf-8 -*-
"""
Created by rsanchez on 03/05/2018
Este proyecto ha sido desarrollado en la Gerencia de Operaciones de CENACE
Mateo633
"""
__author__ = "@RobertoSanchezA"

import datetime
import warnings
from flask import request
import requests
import ast
# import plotly.utils as plt_u
import traceback
from xlrd import open_workbook
from xlutils.copy import copy

from my_lib.PI_connection import pi_connect as osi
from my_lib.calculations import calculos as cal
from my_lib.calculations import consultas as con
from my_lib.hmm import real_time_application as hmm_ap
from my_lib.hmm import Cargar_despacho_programado as c_desp
from my_lib.encrypt import library_encrypt as en
from my_lib.visualizations import visual_util as vi
from my_lib.temporal_files_manager import temporal_manager as tmp
from my_lib.mongo_db_manager import mongo_handler as mgh

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)

import binascii
from flask import Flask, render_template, jsonify, Response, redirect, send_from_directory
import flask_excel as excel
from flask_cors import CORS
import json
import pandas as pd

from logging.handlers import RotatingFileHandler
import logging
from time import strftime
import os

script_path = os.path.dirname(os.path.abspath(__file__))
# default code
app = Flask(__name__)
CORS(app)
excel.init_excel(app)  # excel functions
# ______________________________________________________________________________________________________________#
# ________________________________        GENERAL        VARIABLES       _______________________________________

# Links for the main page:
links = [
    {"url": '/', "text": "Inicio"}
    # {"url": '/test', 'text': "Nuevo Link"}
]

hmm_modelPath = './hmm_application/model/'  # Model path
file_dataPath = './hmm_application/data/'  # File data path


# ______________________________________________________________________________________________________________#

@app.route('/')
def main_page():
    """ This is the MAIN PAGE of this Server Application"""
    # TODO: Create a default page
    # return 'Página principal en construcción'
    return redirect("/map")


""" A testing part ------------------------------------------------------------------------"""


@app.route("/test")
def test_page():
    """ Tests the use of templates and layouts"""
    school = {"school_name": 'prueba 1', "total_students": 32}
    print(en.encrypt("/cal/energy_production"))
    resp = tmp.empty_temp_files(1)
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


@app.route("/map_test")
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

    graphs = [dict(data=[dict(x=[1, 2, 3], y=[10, 20, 30], type='scatter'), ],
                   layout=dict(title='first graph')),
              dict(data=[dict(x=[1, 3, 5], y=[10, 50, 30], type='bar'), ],
                   layout=dict(title='second graph')),
              dict(data=[dict(x=[str(x) for x in ts.index],  # Can use the pandas data structures directly
                              y=[str(x) for x in ts])])]

    # Add "ids" to each of the graphs to pass up to the client
    # for templating
    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]

    # Convert the figures to JSON
    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
    # objects to their JSON equivalents
    graphJSON = json.dumps(graphs)

    return render_template('test/index.html',
                           ids=ids, graphJSON=graphJSON)


""" End testing part ------------------------------------------------------------------------"""
""" PRODUCTION PART: Include new pages below this ___________________________________________"""


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.jpg', mimetype='image/vnd.microsoft.icon')


@app.route("/map/<string:detail>")
@app.route("/map")
def map_ecuador(detail=None):
    # map_data = json.load(open('./static/app_data/maps/ecuador_xy.json'))
    # df_config = pd.read_excel('./static/app_data/maps/empr_electricas_por_provincia.xlsx')
    if detail is None:
        detail = "global"
    title = "Información nacional de distribución"
    titles = {'sbt1': 'ECUADOR', 'sbt2': 'EMPTY'}
    notes = {'nt1': 'Este es un ejemplo de uso del mapa del Ecuador',
             'nt2': 'Sin nota'}
    links_send = dict()
    return render_template('pages/mp_ecuador_sala_control.html', detail=detail,
                           links=links_send, title=title, titles=titles, notes=notes)


@app.route("/dashboard")
def prepare_dashboard():
    title = "Información Operativa en Tiempo Real"
    titles = {'sbt1': 'PRODUCCIÓN ENERGÉTICA (MWh)', 'sbt2': 'CURVA DE GENERACIÓN (MW)'}
    notes = {'nt1': 'Información preliminar, actualizada cada 30 minutos, Fuente: SCADA - CENACE',
             'nt2': 'Información preliminar, actualizada cada 30 minutos, Fuente: SCADA - CENACE'}

    # Configurations for icon panel:
    data_panel = pd.read_excel("static/app_data/produccion_energetica/produccion_energetica.xlsx")
    data_panel = data_panel.to_dict('register')
    # data_panel = en.encrypt_tag_obj(data_panel)
    # data_panel = en.decrypt_tag_obj(data_panel)

    # data for donut
    data_donut = cal.energy_production()

    # data for hydro_bar:
    data_bar_hydro = cal.generation_detail_now(['Embalse', 'Pasada'])

    # data for otra generacion bar:
    data_bar_otra = cal.other_generation_detail_now()

    return render_template('pages/ds_demanda.html',
                           links=links, title=title, titles=titles, notes=notes, data_panel=data_panel,
                           data_donut=data_donut, data_bar_hydro=data_bar_hydro, data_bar_otra=data_bar_otra)


@app.route("/graph_trend_hydro_and_others_today")
def graph_trend_hydro_and_others_today():
    # data for trend hydro and others:
    df_trend = cal.trend_hydro_and_others_today()
    to_send = vi.get_traces_for_gen_hydro_and_others(df_trend)
    json_data = json.dumps(to_send, allow_nan=True)
    json_data = json_data.replace('NaN', 'null')
    return json_data


@app.route("/cargar_re_despacho/<string:fecha>")
def cargar_re_despacho(fecha):
    date = datetime.datetime.strptime(fecha, '%Y-%m-%d')
    try:
        title, msgs = c_desp.run_process_for(date)
    except Exception as e:
        msgs = str(e)
        title = "Error al cargar el re/despacho " + str(fecha)
    msgs = msgs.replace("\n", "<br/>")
    return jsonify(dict(title=title, msgs=msgs))


@app.route("/pronostico/<string:entity>/<string:date>/<string:hour>")
@app.route("/pronostico/<string:entity>/<string:date>/")
@app.route("/pronostico/<string:entity>/<string:date>")
@app.route("/pronostico/<string:entity>/")
@app.route("/pronostico/<string:entity>")
@app.route("/pronostico")
def forecasting(entity="menu", date=None, hour=None):
    msg = ""
    model_name, tag_name, description, data_name, datetime_ini, datetime_fin = None, None, None, None, None, None
    links_demand = None

    if date is None:
        date = datetime.datetime.now().strftime("%Y-%m-%d")
    if hour is None:
        hour = datetime.datetime.now().strftime("%H:%M:%S")
    else:
        try:
            hour_dt = datetime.datetime.strptime(date + " " + hour, '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            hour_dt = datetime.datetime.strptime(date + " " + hour, '%Y-%m-%d %H:%M')
        hour = hour_dt.strftime("%H:%M:%S")

    try:
        df_config = pd.read_excel("./hmm_application/config.xlsx", sheet_name="web_page")
        df_config.set_index("entity", inplace=True)
        description = df_config.at[entity, 'description']
        links_demand = list()
        for url, text in zip(df_config.index, df_config["text"]):
            link = dict(url='/pronostico/' + url + '/{0}/{1}'.format(date, hour), text=text)
            links_demand.append(link)

    except Exception as e:
        print(e)
        msg += "\n No existe la entidad: " + entity + "en config"

    if msg != "":
        return msg

    # graphJSON = graph_pronostico_demanda(description, date, hour)

    title = "Pronóstico de la demanda en tiempo real"
    titles = {'sbt1': description, 'sbt2': 'Información complementaria'}
    notes = {'nt1': 'Información preliminar, actualizada cada 15 minutos, Fuente: SCADA - CENACE',
             'nt2': ''}

    return render_template('pages/pronostico.html',
                           links=links_demand, title=title, titles=titles, notes=notes, date=date, hour=hour)


@app.route("/pronostico/admin")
def pronostico_admin():
    return render_template('pages/pronostico_admin.html', title="Administración Pronóstico de la demanda")


@app.route("/delete_temp")
def delete_temp():
    resp = tmp.empty_temp_files(1)
    return jsonify(resp)


@app.route("/pronostico-videowall/<string:entity>/<string:date>/<string:hour>")
@app.route("/pronostico-videowall/<string:entity>/<string:date>/")
@app.route("/pronostico-videowall/<string:entity>/<string:date>")
@app.route("/pronostico-videowall/<string:entity>/")
@app.route("/pronostico-videowall/<string:entity>")
@app.route("/pronostico-videowall")
def forecasting_videowall(entity="menu", date=None, hour=None):
    msg = ""
    model_name, tag_name, description, data_name, datetime_ini, datetime_fin = None, None, None, None, None, None

    if date is None:
        date = datetime.datetime.now().strftime("%Y-%m-%d")
    if hour is None:
        hour = datetime.datetime.now().strftime("%H:%M:%S")
    else:
        try:
            hour_dt = datetime.datetime.strptime(date + " " + hour, '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            hour_dt = datetime.datetime.strptime(date + " " + hour, '%Y-%m-%d %H:%M')
        hour = hour_dt.strftime("%H:%M:%S")

    try:
        df_config = pd.read_excel("./hmm_application/config.xlsx", sheet_name="web_page")
        df_config.set_index("entity", inplace=True)
        description = df_config.at[entity, 'description']
    except Exception as e:
        print(e)
        msg += "\n No existe la entidad: " + entity

    if msg != "":
        return msg

    # graphJSON = graph_pronostico_demanda(description, date, hour)

    title = "Pronóstico de la demanda en tiempo real"
    titles = {'sbt1': description, 'sbt2': 'Información complementaria'}
    return render_template('pages/pronostico_sala_control.html',
                           title=title, titles=titles, date=date, hour=hour)


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
        return {'graph': {}, layout: {}}

    df_config = pd.read_excel("./hmm_application/config.xlsx", sheet_name="web_page")
    df_config.set_index("description", inplace=True)
    model_name = df_config.at[description, 'model_name']
    tag_name = df_config.at[description, 'tag']
    despacho = df_config.at[description, 'despacho']
    data_name = model_name.replace("hmm_", "")
    entity = df_config.at[description, 'entity']

    hmm_modelPath_file = hmm_modelPath + model_name
    file_dataPath_file = file_dataPath + data_name

    if entity == "demanda-nacional":
        if leer_modo_demanda(True) == "scada":
            df_tag = cal.demanda_nacional_desde_tag(datetime_ini, datetime_fin, "15m")
            df_tag.index = pd.to_datetime(df_tag.index)
        else:
            df_tag = pd.DataFrame(index=pd.date_range(datetime_ini, datetime_fin, freq="15T"))
            df_aux = cal.demanda_nacional_desde_sivo(datetime_ini, datetime_fin)
            df_aux.index = pd.to_datetime(df_aux.index)
            df_tag = pd.concat([df_tag, df_aux], axis=1).interpolate()

    else:
        """ Getting information from the PIserver """

        pi_svr = osi.PIserver()
        pt = osi.PI_point(pi_svr, tag_name)
        time_range = pi_svr.time_range(datetime_ini, datetime_fin)
        span = pi_svr.span("15m")  # Sampled in each 15 min
        df_tag = pt.interpolated(time_range, span)
        df_tag.index = pd.to_datetime(df_tag.index)

    to_send = hmm_ap.graphic_pronostico_demanda(hmm_modelPath_file, file_dataPath_file, df_tag, despacho,
                                                datetime_ini, datetime_fin, style)

    # Convert the figures to JSON ( PlotlyJSONEncoder appropriately converts pandas, datetime, etc)
    # objects to their JSON equivalents
    json_data = json.dumps(to_send)
    json_data = json_data.replace('NaN', 'null')
    return json_data


@app.route("/demanda_en_modo/<string:modo>")
def demanda_en_modo(modo):
    success, msg = mgh.save_settings("demanda_en_modo", modo)
    if success:
        return jsonify("Datos de la demanda en modo: " + modo)
    else:
        return jsonify("Error: " + msg)


@app.route("/leer_modo_demanda")
def leer_modo_demanda(value=False):
    success, config_dict = mgh.read_config()
    if success and not value:
        return jsonify(config_dict["demanda_en_modo"])
    elif success and value:
        return config_dict["demanda_en_modo"]
    else:
        return jsonify("error " + str(config_dict))


@app.route("/get_graph_layout/<string:style>")
def define_layout(style):
    layout_graph = hmm_ap.get_layout(style)
    json_data = json.dumps(layout_graph)
    return json_data


@app.route('/tabla', methods=['GET'])
def show_table():
    url = request.args.get('url')
    param = request.args.get('param')
    obj = request.args.get('obj')
    config = request.args.get('config')
    if param != "":
        url = url + "/" + param

    if url is None and obj is None:
        return jsonify(dict(error="Nada que mostrar"))

    tb_data = None
    title = str()

    if obj is not None:
        tb_data = json.loads(obj)

    if config is not None:
        try:
            config = ast.literal_eval(config)
        except Exception as e:
            return jsonify(dict(error='Error en la definición de la configuración ' + str(e)))
        if 'title' in config.keys():
            title = config['title']

    return render_template('pages/tabla.html', title=title, tb_data=tb_data, url=url, config=config)


@app.route("/tendencia_reserva")
def tendencia_reserva():
    title = "Tendencia de la reserva rodante"
    return render_template('pages/tendencia_reserva.html', title=title)


@app.route("/cargabilidad_lineas")
@app.route("/cargabilidad_lineas/")
@app.route("/cargabilidad_lineas/<string:voltaje>")
def cargabilidad_lineas(voltaje=None):
    if voltaje is None:
        voltaje = 500

    voltaje = str(voltaje)
    if voltaje in ["138", "230", "500"]:

        title = "Cargabilidad " + voltaje + "kV"
        return render_template('pages/hierarchical_edge.html', title=title, voltaje=voltaje)
    else:
        return "No existe datos para cargabilidad de " + voltaje + "kV"


@app.route("/cargabilidad_lineas_for")
@app.route("/cargabilidad_lineas_for/")
@app.route("/cargabilidad_lineas_for/<string:voltaje>")
def cargabilidad_lineas_for(voltaje=None):
    if voltaje is None:
        voltaje = 500

    voltaje = str(voltaje)
    if voltaje in ["138", "230", "500"]:

        title = "Cargabilidad " + voltaje + "kV"
        return render_template('pages/hierarchical_edge_w_FOR.html', title=title, voltaje=voltaje)
    else:
        return "No existe datos para cargabilidad de " + voltaje + "kV"


@app.route("/c_lineas")
@app.route("/c_lineas/")
def c_lineas():
    title = "Cargabilidad 230, 138 kV"
    return render_template('pages/c_lineas.html', title=title)


# ______________________________________________________________________________________________________
# __________________________________ WEB SERVICES FUNCTIONS ____________________________________________

@app.route("/informe_semanal")
@app.route("/informe_semanal/<string:init_date>/<string:end_date>")
def call_service(init_date=None, end_date=None):
    if end_date is None:
        end_date = datetime.datetime.now()
        end_date = end_date.strftime("%Y-%m-%d")
    if init_date is None:
        init_date = datetime.datetime.now() - datetime.timedelta(days=7)
        init_date = init_date.strftime("%Y-%m-%d")

    import requests
    to_send = [{'FechaInicio': init_date, 'FechaFin': end_date}]

    response = requests.get('http://dop-wkstaado/CENSOLServices/PresentacionSemanal/',
                            auth=('rsanchez', 'samweb'), params=to_send)
    data = response.json()

    return jsonify(data)


@app.route("/tag/<string:tag_id>")
def get_snapshot(tag_id):
    """
    try:
        tagname = en.decrypt(tag_id)
    except binascii.Error:
        msg = 'Tag no encriptada'
        print('[get_snapshot]:' + msg)
        return jsonify({"error": msg})
    """
    tagname = tag_id

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
def get_cal(cal_id_function, parameters=None):  # id_encrypt=None


    method_to_call = getattr(cal, cal_id_function)
    if parameters is None:
        result = method_to_call()
    else:
        params = parameters.split("&")
        result = method_to_call(*params)

    if isinstance(result, dict):
        if parameters is None:
            result['id'] = '/cal/' + cal_id_function
        else:
            result['id'] = '/cal/' + cal_id_function + "/" + str(parameters)

    if isinstance(result, pd.DataFrame):
        result.index = [str(x) for x in result.index]
        for orient in ["columns", "records", "index", "split", "values"]:
            try:
                result = result.to_json(orient=orient)
                break
            except Exception as e:
                print(e)
                pass

        resp = Response(response=result,
                        status=200,
                        mimetype="application/json")
        return resp
    return jsonify(result)


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


# -----------------------------------------------------------------------------------------------------------
#    DOWNLOAD SECTION:

@app.route("/download/pronostico/<string:description>/<string:date>/<string:hour>", methods=['GET'])
@app.route("/download/pronostico/<string:description>/<string:date>/", methods=['GET'])
@app.route("/download/pronostico/<string:description>/<string:date>", methods=['GET'])
@app.route("/download/pronostico/<string:description>/", methods=['GET'])
@app.route("/download/pronostico/<string:description>", methods=['GET'])
@app.route("/download/pronostico", methods=['GET'])
def download_pronostico_file(description, date=None, hour=None, Excel_file=True):  # style="default"
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
        return {'graph': {}, layout: {}}

    df_config = pd.read_excel("./hmm_application/config.xlsx")
    df_config.set_index("description", inplace=True)
    model_name = df_config.at[description, 'model_name']
    tag_name = df_config.at[description, 'tag']
    data_name = model_name.replace("hmm_", "")

    hmm_modelPath_file = hmm_modelPath + model_name
    file_dataPath_file = file_dataPath + data_name
    str_date_ini = datetime_ini.strftime("%Y-%m-%d")

    result = hmm_ap.obtain_expected_area(hmm_modelPath_file, file_dataPath_file, tag_name,
                                         str_date_ini, datetime_fin.strftime("%Y-%m-%d %H:%M:%S"))

    df_despacho = hmm_ap.despacho_nacional_programado(str_date_ini)
    df_result = result["df_expected_area"]
    df_result["3.1_Desvio Demanda "] = df_result["real time"] - df_despacho['Despacho programado']
    df_error = df_result["3.1_Desvio Demanda "] / df_result["real time"]
    df_error = df_error.dropna().abs()
    df_result["3.2_Desvio Demanda (%)"] = df_error * 100
    df_result["3.2_Desvio Demanda (%)"] = df_result["3.2_Desvio Demanda (%)"].round(2)
    df_result["4_"] = ""

    df_result = pd.concat([df_despacho, df_result], axis=1)
    mask = df_result.index.isin(df_despacho.index)
    df_result = df_result[mask]
    # print(df_result.columns)
    dict_result = df_result.to_dict('list')
    dict_result['0_Fecha'] = [str(x) for x in df_result.index]
    columns = ['Despacho programado', 'min', 'max', 'expected', 'real time']
    ind = ['1_Despacho programado', '7_Dmin estimada', '6_Dmax estimada', '5_Demanda esperada', '2_Demanda real']
    for ix, col in zip(ind, columns):
        dict_result[ix] = dict_result.pop(col)

    name_file = "pron_" + str_date_ini
    if Excel_file:
        return excel.make_response_from_dict(dict_result, file_type="xlsx", status=200, file_name=name_file)
    else:
        return df_result


@app.route("/download/reporte-pronostico/<string:year>/<string:month>/<string:description>/", methods=['GET'])
@app.route("/download/reporte-pronostico", methods=['GET'])
def download_reporte_pronostico(year=None, month=None, description=None, Excel_file=True):  # style="default"
    import calendar as cld
    dt_now = datetime.datetime.now()

    if year is None:
        year = dt_now.year
    if month is None:
        month = dt_now.month - 1
    if description is None:
        description = "Demanda Nacional del Ecuador"

    n_day, lst_day = cld.monthrange(int(year), int(month))

    datetime_ini = datetime.datetime.strptime(str(year) + "-" + str(month) + "-" + "1", "%Y-%m-%d")
    datetime_fin = datetime.datetime.strptime(str(year) + "-" + str(month) + "-" + str(lst_day), "%Y-%m-%d")
    date_range = pd.date_range(start=datetime_ini, end=datetime_fin, freq="D")

    valid_range = [datetime_ini, datetime_fin + datetime.timedelta(days=30)]
    tmp_name = "download_reporte_pronostico_" + str(date_range[0]) + str(date_range[-1]) + ".pkl"
    tmp_file = tmp.retrieve_file(tmp_name, datetime_ini)
    if tmp_file is None:

        df_result = pd.DataFrame()
        for d in date_range:
            df_i = download_pronostico_file(description, str(d._date_repr), "23:30:00", Excel_file=False)
            df_result = df_result.append(df_i)

        tmp.save_variables(tmp_name, df_result, valid_range)

    else:
        df_result = tmp_file

    dict_result = df_result.to_dict('list')
    dict_result['0_Fecha'] = [str(x) for x in df_result.index]
    columns = ['Despacho programado', 'min', 'max', 'expected', 'real time']
    ind = ['1_Despacho programado', '7_Dmin estimada', '6_Dmax estimada', '5_Demanda esperada', '2_Demanda real']
    for ix, col in zip(ind, columns):
        dict_result[ix] = dict_result.pop(col)

    name_file = "pron_" + datetime_ini.strftime("%Y-%m-%d") + "_" + datetime_fin.strftime("%Y-%m-%d")

    if Excel_file:
        return excel.make_response_from_dict(dict_result, file_type="xlsx", status=200, file_name=name_file)
    else:
        return df_result


@app.after_request
def after_request(response):
    """ Logging after every request. """
    # This avoids the duplication of registry in the log,
    # since that 500 is already logged via @app.errorhandler.
    if response.status_code != 500:
        ts = strftime('[%Y-%b-%d %H:%M]')
        logger.error('%s %s %s %s %s %s',
                      ts,
                      request.remote_addr,
                      request.method,
                      request.scheme,
                      request.full_path,
                      response.status)
    return response


@app.errorhandler(Exception)
def exceptions(e):
    traceback.print_exc()

    """ Logging after every Exception. """
    ts = strftime('[%Y-%b-%d %H:%M]')
    tb = traceback.format_exc()
    logger.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s',
                  ts,
                  request.remote_addr,
                  request.method,
                  request.scheme,
                  request.full_path,
                  tb)
    return "Internal Server Error", 500


if __name__ == '__main__':
    excel.init_excel(app)
    # maxBytes to small number, in order to demonstrate the generation of multiple log files (backupCount).
    handler = RotatingFileHandler(os.path.join(script_path, 'logs', 'GOP_WebServer.log'), maxBytes=10000, backupCount=3)
    # getLogger(__name__):   decorators loggers to file + werkzeug loggers to stdout
    # getLogger('werkzeug'): decorators loggers to file + nothing to stdout
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)
    logger.addHandler(handler)
    # app.run(host='10.30.2.45', port=80, debug=True)     # threaded=True
    app.run(host='10.30.200.100', port=80, debug=True)     # threaded=True
    # app.run(port=80, debug=True)     # threaded=True
    # app.run(host='127.0.0.1', port=5000)
    # app.run()

handler = RotatingFileHandler(os.path.join(script_path, 'logs', 'GOP_WebServer.log'), maxBytes=10000, backupCount=3)
# getLogger(__name__):   decorators loggers to file + werkzeug loggers to stdout
# getLogger('werkzeug'): decorators loggers to file + nothing to stdout
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
logger.addHandler(handler)

