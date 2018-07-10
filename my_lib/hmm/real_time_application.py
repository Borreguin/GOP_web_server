""" coding: utf-8
Created by rsanchez on 21/06/2018
Este proyecto ha sido desarrollado en la Gerencia de Operaciones de CENACE
Mateo633
"""

import numpy as np
import pandas as pd
# from hmmlearn.hmm import GaussianHMM
# from sklearn.externals import joblib
from collections import Counter
from my_lib.hmm import hmm_util as hmm_u
from my_lib.PI_connection import pi_connect as pi
from my_lib.holidays import holidays as hl
from my_lib.GOP_connection import GOPserver as op
import datetime
import os
script_path = os.path.dirname(os.path.abspath(__file__))

# from plotly import tools  # to do subplots
import plotly.offline as py
import cufflinks as cf
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

init_notebook_mode(connected=False)
cf.set_config_file(offline=True, world_readable=True, theme='ggplot')
# import pylab as pl
# from IPython.display import display

py.init_notebook_mode(connected=False)  # run at the start of every ipython notebook to use plotly.offline

max_alpha = 2
min_step = 0.1
alpha_values = np.arange(-1.5, max_alpha, min_step)
n_allowed_consecutive_violations = 3
n_profiles_to_see = 6
gop_svr = op.GOPserver()


def day_cluster_matrix(hmm_model, df_y):
    """
    Se crea una matrix de acuerdo a las familias encontradas
    las familias corresponden a:
        - ['Monday', 'Tuesday', ... 'Sunday']           -> perfiles típicos (categóricos y vacilantes siempre que supere
                                                            un porcentaje mayor a 15%)

        - ['sp_Monday', 'sp_Tuesday', ... 'sp_Sunday']  -> perfiles especiales (son un porcentaje menor al 15%)

        - ['atypicos']  -> son perfiles que contienen un número de días menor al 5% del total de muestra
                            o no superan al menos 3 días

        - ['holidays']  -> días correspondientes a días feriados
    :param hmm_model: Modelo HMM mejor entrenado
    :param df_y: la secuencia de estados ocultos de los observaciones df_x
    :return: matriz con el respectivo agrupamiento de familias
    """
    n_comp = hmm_model.n_components
    dict_cl_week = dict()
    sp = min(0.005 * len(df_y.index), 3)

    for n in range(n_comp):
        mask = df_y["hidden_states"].isin([n])
        df_aux = df_y[mask]
        n_members = len(df_aux.index)
        df_aux.index = pd.to_datetime(df_aux.index)
        df_aux.index = [x.weekday_name for x in df_aux.index]

        if n_members > sp:
            c_dict = Counter(list(df_aux.index))
            for c in c_dict:
                if c_dict[c] > n_members * 0.15:
                    dict_cl_week = append_in_list(dict_cl_week, c, n)
                else:
                    dict_cl_week = append_in_list(dict_cl_week, "sp_" + c, n)
        else:
            for n_d in df_aux.index:
                dict_cl_week = append_in_list(dict_cl_week, "at_" + n_d, n)

    dict_cl_week["holidays"] = hl.get_holidays_dates()
    return dict_cl_week


def append_in_list(dict_obj, key, value):
    """
    Creates a list inside of a dictionary, adds values if this list exists already
    :param dict_obj: dictionary where one adds a value using a key
    :param key:
    :param value:
    :return:
    """
    if key in dict_obj.keys():
        dict_obj[key].append(value)
    else:
        dict_obj[key] = [value]
    dict_obj[key] = list(set(dict_obj[key]))
    return dict_obj


def df_mean_df_std_from_model(model, list_clusters):
    """
    Obtiene los vectores medios y la desviación estandar del modelo HMM usando como filtro
    la lista de clusters deseada
    :param model: GaHMM model
    :param list_clusters: lista de enteros que contiene los clusters deseados
    :return: Dos DataFrames, Dataframe de los vectores medios, DataFrame de los vectores de desviación estandar
    """
    mean_list = list()
    std_list = list()
    for n in list_clusters:
        mean_list.append(model.means_[n])
        std_list.append(np.sqrt(np.diag(model.covars_[n])))

    df_mean = pd.DataFrame(mean_list, index=list_clusters)
    df_std = pd.DataFrame(std_list, index=list_clusters)
    return df_mean, df_std


def df_mean_df_std_from_holidays(df_x, list_holidays):
    """
    Usando una lista de días feriados, se crea perfiles únicos a partir de los feriados.
    :param df_x:  las muestras/observaciones (data) de la serie temporal
    :param list_holidays: lista de feriados
    :return:
    """
    mask = df_x.index.isin(list_holidays)
    df_mean = df_x[mask]
    std_list = list(df_mean.std() * 0.3)
    std_list = [std_list for i in range(len(df_mean.index))]
    df_std = pd.DataFrame(std_list, index=df_mean.index)
    return df_mean, df_std


def get_expected_profiles_from(df_mean, df_with, n_expected_clusters):
    """
    Obtener los perfiles que más se acerquen a df_with (perfil a comparar)
    :param df_mean: Dataframe de los vectores medios del modelo
    :param df_with: Perfil a ser comparado
    :param n_expected_clusters:  número de perfiles esperado
    :return: DataFrame con los perfiles más cercanos (menor error) al perfil comparado (df_with)
    """
    similar_index = df_mean.T.index.intersection(df_with.index)
    df_mean_pt = df_mean.T.loc[similar_index]
    df_with = df_with.loc[similar_index]

    n_real_time = len(df_with.index)
    df_error = df_mean_pt.sub(df_with.T, axis=0)
    # df_error = df_error.div(df_with.T, axis=0)
    # result = (df_error.sum() / n_real_time)*100

    df_error = df_error * df_error
    result = df_error.sum().pow(1 / 2)

    # return df_error * 100
    rs = result.nsmallest(n_expected_clusters)
    return rs


def define_profile_area_from(selected_clusters_list, df_mean, df_std):
    """
    Define el area esperada de acuerdo a los clusters (perfiles) seleccionados
    :param selected_clusters_list: lista de perfiles seleccionados
    :param df_mean: DataFrame con los vectores medios del modelo HMM
    :param df_std:  DataFrame con los vectores std del modelo HMM
    :return:  DataFrame con la definición del perfil experado (max y min son la mezcla de uno o varios perfiles)
              DataFrame con la definición de la desviación estándar, que permite determinar el area esperada
    """
    import matplotlib.pyplot as plt
    mask = df_mean.index.isin(selected_clusters_list)
    df_area = df_mean[mask]
    df_profile = pd.DataFrame()
    df_profile['min'] = df_area.min()
    df_profile['max'] = df_area.max()
    df_profile["expected"] = df_area.mean()
    return df_profile, df_std[mask]


def obtain_expected_area(model_path, data_path, tag_name, str_time_ini, str_time_end):
    """
    Obtener el area esperada de acuerdo a los perdiles más próximos y su correspondiente desviación estándar
    :param model_path:      Path del modelo HMM
    :param data_path:       Path de los datos (muestras/observaciones)
    :param tag_name:        Nombre de la tag en tiempo real a ser evaluada
    :param str_time_ini:    Fecha de inicio
    :param str_time_end:    Fecha de fin
    :return:    Dataframe que define el area esperada
    """
    """ Getting the HMM model, df_x (samples), df_y (labels) """
    model, df_x, df_y = hmm_u.get_model_dfx_dfy(model_path, data_path, filter_values=True, verbose=False)

    """ Grouping profiles according to the family of profile
        Ex: {"Monday": [23,12,...], "sp_Monday":[12,14,...], 
             "Wednesday": [2,10,...], "sp_Wednesday":[13,44,...],  
             "atypical":[13,25, ...] }
    """
    dict_cl_week = day_cluster_matrix(model, df_y)

    """ Getting information from the PIserver """
    pi_svr = pi.PIserver()
    pt = pi.PI_point(pi_svr, tag_name)
    time_range = pi_svr.time_range(str_time_ini, str_time_end)
    span = pi_svr.span("15m")       # Sampled in each 30 min
    df_int = pt.interpolated(time_range, span)
    d_week = df_int.index[0].weekday_name

    """ Find profile according to the family of profiles: """
    profile_families = [d_week, "sp_" + d_week, "at_" + d_week, "holidays"]

    min_error = np.inf
    family_error_dict = dict()
    result = dict()
    for family in profile_families:
        list_clusters = dict_cl_week[family]

        if family != "holidays":
            """ Get the mean and std of the model according to the list of clusters"""
            df_model_mean, df_model_std = df_mean_df_std_from_model(model, list_clusters)

        else:
            """ Get the mean and std of from holidays"""
            df_model_mean, df_model_std = df_mean_df_std_from_holidays(df_x, list_clusters)

        """ Setting the today timestamps for plotting """
        n_columns = pd.date_range(df_int.index[0], df_int.index[0] + pd.Timedelta('23 H 30 m'), freq='30T')
        df_model_mean.columns = n_columns
        df_model_std.columns = n_columns

        """ Find the n best profiles """
        family_error = np.inf
        for n_profiles in range(1, n_profiles_to_see + 1):

            rs = get_expected_profiles_from(df_model_mean, df_with=df_int[tag_name],
                                            n_expected_clusters=n_profiles)

            """ Define the n best expected profiles and the shape of the expected profile """
            expected_profiles = list(rs.index.values)
            df_profile, df_profile_std = define_profile_area_from(expected_profiles, df_model_mean, df_model_std)
            df_std = df_profile_std.mean()

            """ Find the expected area and adjust the band to do not make n violations """
            df_expected_area, alpha_min_max = adjust_expect_band(df_int[tag_name], df_profile, df_std)
            error = estimate_error(df_int[tag_name], df_expected_area["expected"])

            alpha_min_max[0], alpha_min_max[1] = abs(alpha_min_max[0]), abs(alpha_min_max[1])

            # if error < min_error and alpha_min_max[0] < max_alpha and alpha_min_max[1] < max_alpha:
            if error < min_error:
                min_error = error
                result["df_expected_area"] = df_expected_area
                result["family"] = family
                result["n_profiles"] = n_profiles
                result["expected_profiles"] = expected_profiles
                result["alpha_values"] = alpha_min_max
                result["min_error"] = min_error
                alpha_final = alpha_min_max[2]
                result["df_std"] = df_std * alpha_final

            if error < family_error and alpha_min_max[0] < max_alpha and alpha_min_max[1] < max_alpha:
                family_error = error
                family_error_dict[family] = error
                result["family_error"] = family_error_dict

    return result


def adjust_expect_band(df_int, df_profile, df_std):
    """
    Adjust the expected band such that there is not 3 consecutive violations
    :param df_int:      Real time trend
    :param df_profile:  The closer profile to the Real time trend
    :param df_std:      The defined standard deviation
    :return: Dataframe with the definition of the expected area, alpha values
    """
    df_aux = df_int.dropna()
    similar_index = df_aux.index.intersection(df_profile.index)

    # Define the expected area:
    df_area = pd.DataFrame(index=df_profile.index)
    alpha_max_lim, alpha_min_lim = 0, 0

    # Adjusting the expected band by changing the alpha values:
    for alpha in alpha_values:
        # df_area["min"] = df_profile['min'] - alpha * df_std.values
        df_area["min"] = df_profile['expected'] - alpha * df_std.values
        check_list = list(df_int.loc[similar_index] < df_area["min"].loc[similar_index])
        alpha_min_lim = alpha
        if not there_is_n_consecutive_violations(check_list, n_allowed_consecutive_violations):
            break

    for alpha in alpha_values:
        # df_area["max"] = df_profile['max'] + alpha * df_std.values
        df_area["max"] = df_profile['expected'] + alpha * df_std.values
        check_list = list(df_int.loc[similar_index] > df_area["max"].loc[similar_index])
        alpha_max_lim = alpha
        if not there_is_n_consecutive_violations(check_list, n_allowed_consecutive_violations):
            break

    alpha_min_lim += min_step
    alpha_max_lim += min_step

    df_area["max"] = df_profile['expected'] + alpha_max_lim * df_std.values
    df_area["min"] = df_profile['expected'] - alpha_min_lim * df_std.values

    df_area["expected"] = (df_area["max"] + df_area["min"]) * 0.505

    # TODO: Evaluate if this change makes sense:
    alpha_avg = (abs(alpha_max_lim) + abs(alpha_min_lim))*0.4
    df_area["max"] = df_area["expected"] + alpha_avg * df_std.values
    df_area["min"] = df_area["expected"] - alpha_avg * df_std.values

    df_area = pd.concat([df_area, df_int], ignore_index=False, axis=1)
    df_area = df_area[['min', 'max', 'expected']].interpolate()
    df_area["real time"] = df_int
    return df_area, [alpha_min_lim, alpha_max_lim, alpha_avg]


# mean absolute percentage error (MAPE)
def estimate_error(df_real, df_predicted):
    # same size for two dataFrames
    similar_index = df_real.index.intersection(df_predicted.index)
    df_real = df_real.loc[similar_index]
    df_predicted = df_predicted.loc[similar_index]

    n_real_time = len(df_real.index)

    df_error = df_real.sub(df_predicted.T, axis=0).abs()
    df_error = df_error / df_real
    df_error = df_error.sum() / n_real_time

    return df_error * 100


def there_is_n_consecutive_violations(check_list, n_violations):
    violations = ["True"] * n_violations
    str_violations = ", ".join(violations)
    # print(str(check_list).find(str(str_violations)))
    # print(check_list[-1])

    if len(check_list) == 0:
        return True
    if str(check_list).find(str(str_violations)) >= 0 or check_list[-1]:
        return True
    else:
        return False


def despacho_nacional_programado(str_date):
    """
    Obtiene el despacho programado del día str_date, información provemiente de SIVO
    :param str_date: fecha en formato (yyyy-mm-dd)
    :return: list of Dataframes con la tendencia del despacho operativo
    """

    dt_date = datetime.datetime.strptime(str_date, '%Y-%m-%d')
    df_index = pd.date_range(dt_date, dt_date + pd.Timedelta('23 H 30 m'), freq='60T')
    df_despacho = pd.DataFrame(index=df_index)
    for n_desp in range(9):
        sql = "SELECT t.Fecha, t.Hora, t.Unidad, t.MV, t.EsRedespacho, t.NumRedespacho" + \
              " FROM SIVO.dbo.DPL_DespachoProgramado t" + \
              " where Fecha = '{0}'" + \
              " and NumRedespacho = {1}"
        sql = sql.format(str_date, n_desp)
        df = pd.read_sql(sql, gop_svr.conn)
        if n_desp <= 0:
            name_desp = "Despacho programado"
        else:
            name_desp = "Redespacho " + str(n_desp)

        if not df.empty:
            try:
                df = df[df["MV"] > 0]
                df = df.groupby("Hora").sum()
                df.index = df_index
                df_despacho[name_desp] = df["MV"]
            except Exception as e:
                print(script_path, e)
                print("Problema al obtener el despacho programado, despacho incompleto")
        else:
            break

    return df_despacho


def graphic_pronostico_demanda(hmm_modelPath, file_dataPath, tag_name, despacho, datetime_ini, datetime_fin, style):
    """
    Realiza el gráfico de pronóstico de la demanda usando el modelo HMM, el data set de muestras y
    la señal en tiempo real
    :param style: Define el estilo de la gráfica
    :param hmm_modelPath: path del modelo HMM a usar
    :param file_dataPath: path del dataset a usar
    :param tag_name:      nombre de la tag a ser consultada en el Pi-Server
    :param datetime_ini:  Fecha inicial (datetime)
    :param datetime_fin:  Fecha final (datetime)
    :return:  La gráfica en formato {data=data, layout=layout}
    """

    layout_graph = get_layout(style)     # Layout definida para el gráfico
    """ Obtener el area esperada de acuerdo al modelo HMM, sus observaciones y la tendencia en tiempo real """
    result = obtain_expected_area(hmm_modelPath, file_dataPath, tag_name,
                                  datetime_ini.strftime("%Y-%m-%d"), datetime_fin.strftime("%Y-%m-%d %H:%M:%S"))

    df_int = result["df_expected_area"]["real time"]
    df_int.dropna(inplace=True)
    family = flag_day(result["family"])
    t_stamp = df_int.index[-1]
    d_real = int(df_int.loc[t_stamp])
    d_esperada = '---'

    # TODO: Una capa encima que ayude a mejorar el pronóstico de la demanda en horas tempranas
    if datetime_fin.hour < 7:
        result["df_expected_area"]["min"] = np.NAN
        result["df_expected_area"]["max"] = np.NAN
        result["df_expected_area"]["expected"] = np.NAN

    else:
        d_esperada = int(result["df_expected_area"]["expected"].loc[t_stamp])

    trace_std = trace_df_std(result["df_std"])

    if "df_expected_area" not in result.keys():
        return dict(data={}, layout=layout_graph)

    list_traces_expected_area = traces_expected_area_and_real_time(result["df_expected_area"])

    if despacho == "despacho-nacional-programado":
        df_despacho = despacho_nacional_programado(datetime_ini.strftime("%Y-%m-%d"))
    elif despacho == "None":
        df_despacho = pd.DataFrame()
    else:
        # TODO: Realizar la consulta de despacho programado dependiendo de cada entidad (Quito, Guayaquil, etc)
        df_despacho = pd.DataFrame()




    """ Añadir la curva de despacho programado (si existe): """
    if not df_despacho.empty:
        trace_dispatch, last_color = trace_df_despacho(df_despacho)
        df_error = df_despacho.iloc[:, -1].sub(df_int, axis=0)
        df_error.dropna(inplace=True)
        trace_deviation = trace_df_error(df_error, last_color)
        data = [trace_deviation] + trace_std + list_traces_expected_area + trace_dispatch
        t_prog = df_error.index[-1]
        d_programada = int(df_despacho.loc[t_prog].values[0])
        h_programada = t_prog.hour
        desvio_d = d_programada - int(df_int.loc[t_prog])
    else:
        data = trace_std + list_traces_expected_area
        d_programada = "---"
        h_programada = "---"
        desvio_d = "---"

    # graphs = go.Figure(data=data, layout=layout_graph)

    panel_info = dict(d_real=d_real, d_esperada=d_esperada, d_programada=d_programada,
                      h_programada=h_programada, family=family, desvio_d=desvio_d)

    # panel_info = result
    return dict(data=data, layout=layout_graph, panel_info=panel_info)


def flag_day(family):
    day_type = str()
    if "sp_" in family:
        day_type = " especial"
        family = family.replace("sp_", "")

    if "at_" in family:
        day_type = " atípico"
        family = family.replace("at_", "")

    tags = dict(Monday="Lunes", Tuesday="Martes", Wednesday="Miércoles", Thursday="Jueves",
                Friday="Viernes", Saturday="Sábado", Sunday="Domingo", holidays="Feriado",
                atypical="Atípico")
    if family in tags.keys():
        return tags[family] + day_type
    else:
        return "No determinado"

"""
    GRAPHICAL PART OF THIS MODULE
"""

layout = go.Layout(
    autosize=False,
    width=700,
    height=900,
    margin=go.Margin(
        l=50,
        r=50,
        b=50,
        t=50,
        pad=0
    )
    # paper_bgcolor='#7f7f7f',
    # plot_bgcolor='#c7c7c7'
)


def traces_expected_area_and_real_time(df_expected_area):
    traces = list()
    colors = {'min': 'rgba(210, 210, 210, .4)', 'max': 'rgba(210, 210, 210, .4)', 'real time': 'red',
              'expected': 'rgba(0, 170, 0, 1)'}
    width = {'min': 1, 'max': 1, 'real time': 4, 'expected': 2}
    dash = {'min': None, 'max': None, 'real time': None, 'expected': None} #dashdot
    fill = {'min': None, 'max': 'tonexty', 'real time': None, 'expected': None}
    names = {'min': 'Min demanda esperada', 'max': 'Max demanda esperada', 'real time': 'Demanda real',
             'expected': 'Demanda esperada'}

    for column in df_expected_area.columns:
        trace = go.Scatter(
            x=df_expected_area.index,
            y=df_expected_area[column],
            name=names[column],
            mode='line',
            fill=fill[column],
            line=dict(
                width=width[column],
                color=colors[column],
                dash=dash[column]
            )
        )

        traces.append(trace)
    return traces


def trace_df_std(df_std):
    list_trace = list()
    dict_to_draw = dict(positive=1, negative=-1)
    show_legend = dict(positive=True, negative=False)
    for f in dict_to_draw.keys():
        trace = go.Scatter(
            x=df_std.index,
            y=df_std*dict_to_draw[f],
            name="Desviación estándar",
            mode='line',
            fill='tozeroy',
            xaxis='x',
            yaxis='y2',
            line=dict(
                width=1,
                color='rgba(210, 210, 210, .8)',
                shape='hv'
            ),
            showlegend=show_legend[f]

        )
        list_trace.append(trace)
    return list_trace


def trace_df_despacho(df_despacho):

    traces = list()
    colors = ['rgba(26, 198, 255, 1)', 'rgba(102, 255, 194, 1)', 'rgba(255, 255, 102, 1)', 'rgba(255, 255, 255, 1)']
    idx = -1
    for column in df_despacho.columns:
        idx += 1
        trace = go.Scatter(
            x=df_despacho.index,
            y=df_despacho[column],
            name=column,
            mode='line',
            line=dict(
                width=3,
                color=colors[idx],
                dash='dashdot'
            )
        )
        traces.append(trace)
    return traces, colors[idx]


def trace_df_error(df_error, last_color):
    trace = go.Scatter(
        x=df_error.index,
        y=df_error,
        name="Desviación de demanda",
        mode='line',
        xaxis='x',
        yaxis='y2',
        line=dict(
            width=2,
            color=last_color,
            dash=None
        )

    )
    return trace


def get_layout(style):

    tick_color = {"default": "white", "white_style": "black", "black_style": "white"}
    paper_bgcolor = {"default": 'rgba(32, 56, 100, .9)', "white_style": "white", "black_style": 'rgba(15, 15, 15, 1)'}
    plot_bgcolor = {"default": 'rgba(32, 56, 50, 0.5)', "white_style": 'white', "black_style": "black"}
    font_color = {"default": "white", "white_style": "black", "black_style": "white"}
    # 32, 56, 100,

    return go.Layout(
        xaxis=dict(
            domain=[0, 1],
            tickcolor=tick_color[style],
            gridcolor='gray'
        ),
        yaxis=dict(
            domain=[0, 0.70],
            tickcolor=tick_color[style],
            gridcolor='gray'
        ),
        yaxis2=dict(
            domain=[0.75, 1.2],
            tickcolor=tick_color[style],
            gridcolor='gray'
        ),
        paper_bgcolor=paper_bgcolor[style],
        plot_bgcolor=plot_bgcolor[style],
        font=dict(color=font_color[style]),
        margin=go.Margin(
            t=50,
            pad=0
        )
    )