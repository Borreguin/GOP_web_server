""" coding: utf-8
Created by rsanchez on 07/05/2018
Este proyecto ha sido desarrollado en la Gerencia de Operaciones de CENACE
Mateo633
"""
import datetime
import os
from my_lib.GOP_connection import GOPserver as Gop
from my_lib.PI_connection import pi_connect as osi
from my_lib.temporal_files_manager import temporal_manager as tmp
import datetime as dt
import pandas as pd

gop_svr = Gop.GOPserver()
pi_svr = osi.PIserver()
script_path = os.path.dirname(os.path.abspath(__file__))
# ______________________________________________________________________________________________________________#
# ________________________________        GENERAL        VARIABLES       _______________________________________

delta_15 = 15  # minutes
factor_15 = delta_15 / 60  # factor for calculating Energy using P each 15 minutes
span_15 = pi_svr.span(str(delta_15) + "m")  # span time of 15 minutes

delta_30 = 30  # minutes
factor_30 = delta_30 / 60  # factor for calculating Energy using P each 15 minutes
span_30 = pi_svr.span(str(delta_30) + "m")  # span time of 15 minutes

technology = ['Embalse', 'Pasada', 'Turbo Vapor', 'Turbo Gas', 'MCI', 'Biomasa',
              'Eólica', 'Fotovoltaica', 'Bio Gas']

termoelectrica_list = ['Turbo Vapor', 'MCI', 'Turbo Gas']  # Machala Gas es de tipo 'Turbo Gas'
gas_natural_list = ['Turbo Gas']  # El tipo de combustible permite realizar el filtro correcto
no_convencional_list = ['Biomasa', 'Eólica', 'Fotovoltaica', 'Bio Gas']
hidraulica_list = ['Embalse', 'Pasada']

system_path_file = "F:\DATO\Estad\System SIVO\SYSTEM yyyy.xlsx"
empresas_file_config = "\static\\app_data\maps\empr_electricas_por_provincia.xlsx"


# ______________________________________________________________________________________________________________#


def energy_production():
    """
    Detalle de la energía producida desde 00:00 hasta el momento en el día
    - Hidráulica            (Mwh)   (%)
    - Otra generación       (Mwh)   (%)
    :return:
    """
    e_hydro = generation_now('Hidráulica')['value']
    e_total = generation_now('Total')['value']
    e_otra = e_total - e_hydro
    # e_otra = generation_now('otra generacion')['value']

    result = [{"id": 0, "label": "Hidráulica", "value": str(e_hydro) + " MWh", "percentage": e_hydro / e_total},
              {"id": 1, "label": "Otra Generación", "value": str(e_otra) + " MWh", "percentage": 1 - e_hydro / e_total}]
    return result


def df_tags_exportation():
    """
    :return: Todas las tags relacionadas a la exportación de energía
    """
    sql = "SELECT C.Codigo, C.Nombre, C2.TAG, C2.Descripcion, E.Elemento FROM CFG_Equivalencias E" + \
          " INNER JOIN CFG_Linea L ON E.Equivalencia=L.Codigo" + \
          " INNER JOIN CFG_Circuito C ON L.IdLinea=C.IdLinea " + \
          " INNER JOIN CFG_ElementoTAG M ON C.IdCircuito=M.IdElemento" + \
          " INNER JOIN CFG_TAG C2 on M.IdTAG = C2.IdTAG" + \
          " WHERE C2.TAG LIKE '%P.LINEA%'" \
          + "AND C2.IdTipoTAG IN (1,3,9,10)"  # according to the flows
    return pd.read_sql(sql, gop_svr.conn)


def df_tags_importation():
    """
        :return: Todas las tags relacionadas a la importación de energía
        """
    sql = "SELECT C.Codigo, C.Nombre, C2.TAG, C2.Descripcion, E.Elemento FROM CFG_Equivalencias E" + \
          " INNER JOIN CFG_Linea L ON E.Equivalencia=L.Codigo" + \
          " INNER JOIN CFG_Circuito C ON L.IdLinea=C.IdLinea " + \
          " INNER JOIN CFG_ElementoTAG M ON C.IdCircuito=M.IdElemento" + \
          " INNER JOIN CFG_TAG C2 on M.IdTAG = C2.IdTAG" + \
          " WHERE C2.TAG LIKE '%P.LINEA%'" \
          + "AND C2.IdTipoTAG IN (5,6,11,12)"  # according to the flows
    return pd.read_sql(sql, gop_svr.conn)


def exportation_energy_now():
    """
        Exportation energy (MWh) from 0:00 until the current moment in an span of (span minutes)
        :return: energy MWh
    """
    time_range = pi_svr.time_range_for_today
    return exportation_energy(time_range)


def exportation_energy(time_range):
    """
        Exportation energy (MWh) in the time range in an span of (span minutes)
        (span_15 = 15 minutes)
    :return: energy MWh
    """
    df_c = df_tags_exportation()
    tags_AV = list(set([x for x in df_c["TAG"] if ".AV" in x]))
    df_values = pi_svr.interpolated_of_tag_list(tags_AV, time_range, span_15)
    df_mw = df_values[df_values > 0].sum(axis=1)
    energy = int(integrating_by_average(df_mw, factor_15))
    return {'value': energy, 'tag': 'exportation_energy_now',
            'time_range': str(time_range), 'timestamp': timestamp_now()}


def importation_energy_now():
    """
    Importation energy (MWh) from 0:00 until the current moment in an span of (span 15 minutes)
    :return: energy MWh
    """
    time_range = pi_svr.time_range_for_today
    df_c = df_tags_importation()
    tags_AV = list(set([x for x in df_c["TAG"] if ".AV" in x]))
    df_values = pi_svr.interpolated_of_tag_list(tags_AV, time_range, span_15)
    df_mw = df_values[df_values > 0].sum(axis=1)
    energy = int(integrating_by_average(df_mw, factor_15))
    return {'value': energy, 'tag': 'importation_energy_now',
            'time_range': str(time_range), 'timestamp': timestamp_now()}


def generation_matrix(time_range):
    """
    Generation matrix that is stored over BOSNI Database
    Esta es la matriz porosa actualizada cada 30 minutos,
    :param time_range:  AFTimeRange (PIserver.time_range())
    :return: DataFrame con los generadores y su producción que se encuentran en linea
    al corte de cada 30 minutos
    """
    initial_date = time_range.StartTime.ToString("yyyy-MM-dd HH:mm:s")
    final_date = time_range.EndTime.ToString("yyyy-MM-dd HH:mm:s")
    sql = "SELECT [Central],[Unidad],[Tecnología]" + \
          ",[TAG],[Potencia],[Fecha]" + \
          " FROM [BOSNI].[dbo].[vHIST_UNIDAD_POT_EFECTIVA]" + \
          " WHERE [Fecha] between '{0}' and '{1}'"
    sql = sql.format(initial_date, final_date)

    df_gen = pd.read_sql(sql, gop_svr.conn)

    # añadiendo generación no convencional (Fotovoltaica):
    # TODO: Caso Fotovoltaicas, Dado que no están todas implementadas en SIVO:
    # Se recoge el total de generación fotovoltaica en esta central
    caso_fotovoltaica = True
    if caso_fotovoltaica:
        mask = df_gen["Tecnología"] == "Fotovoltaica"
        if len(df_gen[mask]) > 0:
            df_gen[mask].drop(inplace=True)
        tag_total_fotovoltaica = obtener_tag_name_por_descripcion("Generación Fotovoltaica")
        df_values = tag_total_fotovoltaica.interpolated(time_range, span_30)
        tag_name = tag_total_fotovoltaica.tag_name
        for idx in df_values.index:
            df_aux = pd.DataFrame(["Fotovoltaica", "Total", "Fotovoltaica", tag_name, df_values.at[idx, tag_name], idx],
                                  index=["Central", "Unidad", "Tecnología", "TAG", "Potencia", "Fecha"])
            df_gen = df_gen.append(df_aux.T, ignore_index=True)

    df_gen["Fecha"] = [f._repr_base for f in df_gen["Fecha"]]
    df_gen["unique"] = df_gen["Central"] + "_" + df_gen["Unidad"] + "_" + df_gen["Fecha"]
    df_gen.sort_values(by=["Central", "Unidad", "Fecha", "TAG"], inplace=True)
    df_gen.drop_duplicates(["unique"], keep='last', inplace=True)
    return df_gen


def generation_energy_by_tech_now():
    """
    Energy values for each kind of technology from 00:00 until the current moment
    :return: dictionary with energy of each kind of technology
    """
    time_range = pi_svr.time_range_for_today
    return generation_energy_by_tech(time_range)


def generation_energy_by_tech(time_range):
    """
    Energy values for each kind of technology according to time_range
    :param time_range: AFTimeRange.
      Example: pi_svr.time_range("yyyy-mm-dd HH:MM.SS", "yyyy-mm-dd HH:MM.SS")
    :return: dictionary with energy of each kind of technology
    """
    # time_range = pi_svr.time_range("2018-05-22", "2018-05-22 07:00:00")
    df_gen = generation_matrix(time_range)
    df_gen = df_gen[df_gen["Potencia"] > 0]
    # df_gen.sort_values(by=['Central', 'Unidad'], inplace=True)

    # calculating energy by technology:
    result = {"time_range": str(time_range)}
    for tech in technology:
        mask = (df_gen["Tecnología"] == tech)
        # df_w = df_gen.loc[mask]
        # df_r = df_w.groupby('Central').sum()
        df_c = df_gen.loc[mask].groupby('Fecha')
        df_c = df_c["Potencia"].sum()
        # integrating using average:
        result[tech] = integrating_by_average(df_c, dx=factor_30)
    return result


# Ex:   /cal/generation_now/otra generacion
#       /cal/generation_now/hidraulica
def generation_now(detail="Total"):
    """
    Energy of generation in MWh (dictionary with energy values)
    :param detail: options: 'Total', 'Hidráulica', 'Otra generación',
     'No convencional', 'Termoeléctrica', 'Termoeléctrica + interconexión'
    :return: dictionary with energy values
    """
    subtotal = generation_energy_by_tech_now()
    total = 0

    if detail == 'Total':
        for sb in subtotal:
            if sb != "time_range":
                total += subtotal[sb]
        total += importation_energy_now()["value"]

    elif detail == 'Hidráulica':
        for sb in hidraulica_list:
            total += subtotal[sb]

    elif detail == 'Otra generación':
        for sb in subtotal:
            if sb != "time_range":
                total += subtotal[sb]
        total += importation_energy_now()["value"]

        hydro = 0
        for sb in hidraulica_list:
            hydro += subtotal[sb]
        total -= hydro

    elif detail == 'Termoeléctrica':
        for sb in termoelectrica_list:
            total += subtotal[sb]

    elif detail == 'Termoeléctrica + interconexión':
        for sb in termoelectrica_list:
            total += subtotal[sb]
        total += importation_energy_now()["value"]

    elif detail == 'No convencional':
        for sb in no_convencional_list:
            total += subtotal[sb]

    else:
        for sb in [detail]:
            total += subtotal[sb]

    total = round(total, 0)
    return {'value': total, 'tag': 'generation_now',
            'time_range': subtotal['time_range'], 'detail': detail,
            'timestamp': timestamp_now()}


# Ex. http://127.0.0.1:5000/cal/generation_detail_now/Embalse,Pasada&9
# http://127.0.0.1:5000/cal/generation_detail_now/Turbo Vapor,Turbo Gas
def generation_detail_now(list_tech, level=7):
    """
    Detalle de generación de acuerdo al tipo de tecnología (list_tech) desde las 00:00 hasta el momento
    :param list_tech: opciones disponibles: Embalse, Pasada, Turbo Vapor, Turbo Gas, MCI, Biomasa,
              Eólica, Fotovoltaica, Bio Gas, Termoelectrica, No convencional
    :param level: indica el nivel de detalle a observar
    :return: diccionario con el detalle de generación de cada generador
    """
    level = int(level)
    if isinstance(list_tech, str):
        list_tech = list_tech.split(",")
    time_range = pi_svr.time_range_for_today
    return generation_detail(time_range, list_tech, level)


def generation_detail(time_range, list_tech, level=7):
    """
        Detalle de generación de acuerdo al tipo de tecnología (list_tech) en el periodo de consulta (time_range)
        :param time_range: El periodo de consulta
        :param list_tech: opciones disponibles: Embalse, Pasada, Turbo Vapor, Turbo Gas, MCI, Biomasa,
                  Eólica, Fotovoltaica, Bio Gas
        :param level: indica el nivel de detalle a observar
        :return: diccionario con el detalle de generación de cada generador
        """
    if "Termoelectrica" in list_tech:
        list_tech += termoelectrica_list

    if "Gas Natural" in list_tech:
        # TODO: aumentar filtro por tipo de combustible
        list_tech += gas_natural_list

    if "No convencional" in list_tech:
        list_tech += no_convencional_list

    df_gen = generation_matrix(time_range)
    mask = (df_gen["Tecnología"].isin(list_tech))
    df_gen = df_gen[mask]
    df_gen = df_gen[df_gen["Potencia"] > 0]
    centrals = list(set(df_gen["Central"]))
    df_result = pd.DataFrame(index=centrals, columns=["Energía"])
    for c in centrals:
        df_x = df_gen[df_gen["Central"] == c]["Potencia"]
        df_result.at[c, "Energía"] = integrating_by_average(df_x, factor_30)

    df_result.sort_values(by=["Energía"], ascending=False, inplace=True)
    df_head = df_result.head(level)
    total = df_result["Energía"].sum()

    if total == 0:
        print("[{0}] [calculos.py] \t [generation_detail] "
              "\t La matrix de generación se encuentra vacía".format(script_path))
        return None

    result = list()
    acc = 0
    for idx, name in enumerate(df_head.index):
        value = df_head["Energía"].iloc[idx]
        name = name.replace("Central ", "")
        percentage = round(value / total, 4)
        if len(name) > 15:
            name = name[:15] + "."

        r = {"id": idx,
             "label": name,
             "value": str(int(value)) + " MWh",
             "percentage": percentage
             }
        result.append(r)
        acc += percentage

    if level > 0:
        r = {"id": level,
             "label": "Otros",
             "value": str(int((1 - acc) * total)) + " MWh",
             "percentage": round(1 - acc, 4)
             }
        result.append(r)

    return result


def other_generation_detail_now():
    """
    Detalle de la generación "Otra generación" ("Gas natural", "No convencional", "Calidad de servicio")
    :return: diccionario con el detalle de generación
    """
    df_r = pd.DataFrame(
        index=["Gas natural", "No convencional", "Calidad de servicio"],
        columns=["value", "id", "label", "percentage"])
    df_r["label"] = df_r.index
    df_r["id"] = range(len(df_r.index))
    total = generation_now('Otra generación')['value']
    df_r.at["Gas natural", "value"] = generation_now('Turbo Gas')['value']
    df_r.at["No convencional", "value"] = generation_now('No convencional')['value']
    df_r.at["Calidad de servicio", "value"] = total - df_r["value"].loc["Gas natural"] - df_r["value"].loc["No convencional"]
    df_r["percentage"] = df_r["value"] / total
    df_r["numeric"] = df_r["value"]
    df_r["value"] = [str(x) + " MWh" for x in df_r["value"]]
    return df_r.to_dict("record")


def generation_trend_today_by_tech():
    """
    La tendencia de generación por cada tipo de tecnología:
    :return: DataFrame
    """
    time_range = pi_svr.time_range_for_today
    df_matrix = generation_matrix(time_range)
    # init
    mask = (df_matrix["Tecnología"] == technology[0])
    df_trend = df_matrix[mask].groupby("Fecha")["Potencia"].sum()
    df_result = pd.DataFrame(index=df_trend.index, columns=technology)
    df_result[technology[0]] = df_trend

    # others
    for tech in technology[1:]:
        mask = (df_matrix["Tecnología"] == tech)
        df_result[tech] = df_matrix[mask].groupby("Fecha")["Potencia"].sum()

    return df_result


def trend_hydro_and_others_today():
    df_by_tech = generation_trend_today_by_tech()
    df_by_tech.index = pd.to_datetime(df_by_tech.index)
    dt_n = datetime.datetime.today()
    dt_today = dt_n.strftime("%Y-%m-%d")
    dt_today = datetime.datetime.strptime(dt_today, "%Y-%m-%d").date()
    index_range = pd.date_range(dt_today, dt_today + datetime.timedelta(hours=24), freq="30T")

    df_trend = pd.DataFrame(columns=["Hydro", "Others"], index=index_range)

    # Trend of importation
    df_c = df_tags_importation()
    tags_AV = list(set([x for x in df_c["TAG"] if ".AV" in x]))
    df_values = pi_svr.interpolated_of_tag_list(tags_AV, pi_svr.time_range_for_today, span_30)
    df_importation = df_values[df_values > 0].fillna(0).sum(axis=1)
    df_importation.index = pd.to_datetime(df_importation.index)

    # Trend of exportation
    df_c = df_tags_exportation()
    tags_AV = list(set([x for x in df_c["TAG"] if ".AV" in x]))
    df_values = pi_svr.interpolated_of_tag_list(tags_AV, pi_svr.time_range_for_today, span_30)
    df_exportation = df_values[df_values > 0].fillna(0).sum(axis=1)
    df_exportation.index = pd.to_datetime(df_exportation.index)

    # Trend by Hydro and Others technologies
    hydro = ['Embalse', 'Pasada']
    others = list(set(technology) - set(hydro))

    df_trend["Hydro"] = df_by_tech[hydro].sum(axis=1) - df_exportation.values
    df_trend["Others"] = df_by_tech[others].sum(axis=1) + df_importation.values
    df_trend["Exportation"] = df_exportation
    df_trend["Total"] = df_trend["Others"] + df_by_tech[hydro].sum(axis=1)
    df_trend["National_demand"] = df_trend["Total"].loc[df_exportation.index] - df_exportation.values

    return df_trend


def demanda_nacional_desde_tag(ini_date=None, fin_date=None, delta=None):
    """

    :param ini_date:
    :param fin_date:
    :param delta: string format: Ex: 10m
    :return:
    """
    # calculo disponible en 2 minutos
    dt_delta = dt.timedelta(minutes=2)
    tmp_name = "calculos_demanda_nacional" + str(ini_date) + str(fin_date) + str(delta) + ".pkl"
    tmp_file = tmp.retrieve_file(tmp_name, dt_delta)
    if tmp_file is not None:
        return tmp_file

    # tagname de demanda nacional
    path_config_file = script_path.replace('my_lib\\calculations', 'hmm_application\\config.xlsx')
    df_config = pd.read_excel(path_config_file)
    df_config.set_index("description", inplace=True)
    tag_name = df_config.at["Demanda Nacional del Ecuador", 'tag']
    # tag_name = obtener_tag_name_por_descripcion("Demanda Nacional")

    # valores por defecto
    time_range = pi_svr.time_range_for_today_all_day
    span = pi_svr.span("30m")

    if ini_date is not None and fin_date is not None:
        time_range = pi_svr.time_range(ini_date, fin_date)

    if delta is not None:
        span = pi_svr.span(delta)

    pt = osi.PI_point(pi_svr, tag_name)
    df_demanda = pt.interpolated(time_range, span)
    df_demanda.rename(index=str, columns={tag_name: "Demanda nacional"}, inplace=True)

    tmp.save_variables(tmp_name, df_demanda)
    return df_demanda


def demanda_nacional_desde_sivo(ini_date=None, fin_date=None):
    """
    Esta función calcula la demanda nacional usando la matriz porosa de SIVO
    :param ini_date:  string en formato: yyyy-mm-dd hh:mm:ss
    :param fin_date:  string en formato: yyyy-mm-dd hh:mm:ss
    :return:
    """

    if ini_date is None and fin_date is None:
        time_range = pi_svr.time_range_for_today_all_day
    else:
        time_range = pi_svr.time_range(ini_date, fin_date)

    df_gen = generation_matrix(time_range)
    df_gen = df_gen[df_gen["Potencia"] > 0]
    df_gen = df_gen[["Potencia", "Fecha"]].groupby("Fecha").sum()
    df_importacion = intercambio_programado_importacion(time_range)
    df_exportacion = intercambio_programado_exportacion(time_range)
    date_range = pd.date_range(time_range.get_StartTime().ToString("yyyy-MM-dd HH:mm:s"),
                               time_range.get_EndTime().ToString("yyyy-MM-dd HH:mm:s"), freq="30T")
    df_result = pd.DataFrame(index=[str(x) for x in date_range], columns=["Demanda nacional"])
    df_result["Demanda nacional"] = df_gen["Potencia"] + df_importacion["Importación"] - df_exportacion["Exportación"]
    return df_result


def demanda_empresas(time=None, level=-1):
    level = int(level)

    # calculo disponible en 3 minutos
    # dt_delta = dt.timedelta(minutes=3)
    # tmp_file = tmp.retrieve_file("calculos_demanda_empresas_now.pkl", dt_delta)
    # if tmp_file is not None:
    #    return tmp_file

    if time is None:
        time = dt.datetime.now()

    config_path_file = script_path.replace('\my_lib\calculations', empresas_file_config)
    df_config = pd.read_excel(config_path_file, sheet_name='demanda_empresas')

    year = dt.datetime.now().year
    sql_str = 'SELECT t.Nom_UNegocio, t.Fecha, PotMax MW FROM SIVO.dbo.TMP_System_Dem t ' + \
              "where YEAR(t.Fecha) = {0}"

    df_max = pd.read_sql(sql_str.format(year), gop_svr.conn)

    if df_max.empty:
        year = year - 1
        df_max = pd.read_sql(sql_str.format(year), gop_svr.conn)

    df_max.dropna(inplace=True)
    df_max = df_max.pivot(index='Fecha', columns='Nom_UNegocio')
    df_max.columns = [col[1] for col in df_max.columns]

    df_result = pd.DataFrame(index=df_config["EMPRESA"], columns=["current_value", "timestamp", "max_value", "dif"])
    for empresa, tag in zip(df_config["EMPRESA"], df_config["TAG"]):
        pt = osi.PI_point(pi_svr, tag)
        # df_result.at[empresa, "timestamp"] = pt.snapshot().Timestamp.ToString("yyyy-MM-dd HH:mm:s")
        df_result.at[empresa, "timestamp"] = str(time)
        # df_result.at[empresa, "current_value"] = int(pt.snapshot().Value)
        df_result.at[empresa, "current_value"] = round(pt.interpolated_value(time), 1)
        df_result.at[empresa, "max_value"] = round(df_max[empresa].max(), 1)

    df_result["dif"] = df_result["max_value"] - df_result["current_value"]
    df_result.sort_values(by=["current_value"], ascending=False, inplace=True)

    if level > 1:
        df_tail = df_result.iloc[level:]
        df_result = df_result.iloc[:level]
        df_result.at["Otros", "current_value"] = df_tail["current_value"].sum()
        df_result.at["Otros", "timestamp"] = df_tail["timestamp"].iloc[0]
        df_result.at["Otros", "dif"] = df_tail["dif"].sum()
        df_result.at["Otros", "max_value"] = df_result.at["Otros", "current_value"] + df_result.at["Otros", "dif"]

    df_result["percentage"] = df_result["current_value"] / df_result["current_value"].sum() * 100
    df_result["percentage"] = [str(round(x, 1)) + "%" for x in df_result["percentage"].values]
    mask = df_result["dif"] < 0
    df_result["dif"][mask] = 0
    # tmp.save_variables("calculos_demanda_empresas_now.pkl", df_result)
    return df_result


def maxima_demanda_nacional(year=None):
    if year is None:
        year = str(dt.datetime.now().year)

    sql_str = 'SELECT TOP 1 * FROM [SIVO].[dbo].[TMP_System_Perdidas_Potencia] PP' + \
              ' WHERE YEAR(PP.Fecha)=yyyy ORDER BY PP.DeePerdidas DESC'
    sql_str = sql_str.replace("yyyy", year)
    df = pd.read_sql(sql_str, gop_svr.conn)
    return df.T


def tendencia_demanda_nacional_por_regiones(time_range=None, span=None):
    # calculo disponible en 2 minutos
    dt_delta = dt.timedelta(minutes=2)
    tmp_name = "tendencia_demanda_nacional_por_regiones" + str(time_range) + str(span) + ".pkl"
    tmp_file = tmp.retrieve_file(tmp_name, dt_delta)
    if tmp_file is not None:
        return tmp_file

    if time_range is None:
        time_range = pi_svr.time_range_for_today_all_day
    if span is None:
        span = span_30

    config_path_file = script_path.replace('\my_lib\calculations', empresas_file_config)
    df_config = pd.read_excel(config_path_file, sheet_name='demanda_empresas')
    df_config.fillna(0, inplace=True)
    regiones = ['Costa', 'Sierra', 'Oriente']
    df_result = pd.DataFrame(columns=regiones)
    for region in regiones:
        mask = (df_config["% " + region] > 0)
        tag_list = list(df_config["TAG"][mask])
        df_values = pi_svr.interpolated_of_tag_list(tag_list, time_range, span, numeric=True)
        factor = df_config["% " + region][mask]
        df_values = factor.values * df_values
        df_result[region] = df_values.sum(axis=1, skipna=False)
        df_result[region] = df_result[region].round(decimals=1)
    tmp.save_variables(tmp_name, df_result)
    return df_result


def demanda_regiones(time=None):
    # calculo disponible en 3 minutos
    # dt_delta = dt.timedelta(minutes=3)
    # tmp_file = tmp.retrieve_file("calculos_demanda_empresas_now.pkl", dt_delta)
    # if tmp_file is not None:
    #    return tmp_file

    if time is None:
        time = dt.datetime.now()

    config_path_file = script_path.replace('\my_lib\calculations', empresas_file_config)
    df_config = pd.read_excel(config_path_file, sheet_name='demanda_empresas')
    df_config.index = df_config["EMPRESA"]
    df_config.fillna(0, inplace=True)
    df_config.sort_index(inplace=True)

    df_empresas = demanda_empresas(time)
    df_empresas.sort_index(inplace=True)
    regions = ["Costa", "Sierra", "Oriente"]
    df_result = pd.DataFrame(index=regions, columns=df_empresas.columns)

    for region in regions:
        mask = (df_config["% " + region] > 0)
        df_aux = df_empresas[mask].copy()
        factors = df_config["% " + region][mask].values
        df_aux["current_value"] = df_aux["current_value"] * factors
        df_result["current_value"].loc[region] = round(df_aux["current_value"].sum(), 1)
        df_result["max_value"].loc[region] = round(df_aux["max_value"].sum(), 1)

    df_result["dif"] = df_result["max_value"] - df_result["current_value"]
    df_result["percentage"] = df_result["current_value"] / df_result["current_value"].sum() * 100
    df_result["percentage"] = [str(round(x, 1)) + "%" for x in df_result["percentage"].values]
    df_result[df_result["dif"] < 0]["dif"] = 0
    df_result["timestamp"] = str(time)
    return df_result


# Example:
# /cal/filtrar_generacion_por/No convencional&2018-08-20 08:45:00, 2018-08-20 09:05:00
def filtrar_generacion_por(detail="Total", time_range=None):
    """
    Entrega la matriz de generación (matriz porosa) filtrada de acuerdo al parámetro @param:detail en el periodo
    delimitado por @param:time_range:
    :param time_range: define el periodo de consulta, puede ser 1. AFTime Object o 2. String:
            Ex1: pi_svr.time_range("yyyy-mm-dd hh:mm:ss", "yyyy-mm-dd hh:mm:ss")
            Ex2: 2018-08-20 08:45:00, 2018-08-20 09:05:00
    :param detail: detalle de tecnologías: valores válidos: Embalse, Pasada, Turbo Vapor, Turbo Gas, MCI, Biomasa,
              Eólica, Fotovoltaica, Bio Gas, Termoelectrica, No convencional, Total
    :return:
    """
    if isinstance(detail, str):
        detail = detail.split(',')
    filter_list = list()

    if time_range is None:
        time_range = pi_svr.time_range_for_today
    elif isinstance(time_range, str):
        try:
            time_range = time_range.split(",")
            time_range = pi_svr.time_range(time_range[0], time_range[1])
        except Exception as e:
            print(e)
            return dict(error=e)

    df_gen = generation_matrix(time_range)

    if 'Total' in detail:
        filter_list = technology
    if 'Termoeléctrica' in detail:
        # TODO: Verificar tipo de combustible para termoelectrica
        filter_list += termoelectrica_list
    if 'Gas Natural' in detail:
        # TODO: Filtrar por tipo de combustible
        filter_list += gas_natural_list
    if 'No convencional' in detail:
        filter_list += no_convencional_list
    if 'Hidroeléctrica' in detail:
        filter_list += hidraulica_list

    if len(filter_list) == 0:
        filter_list += detail

    mask = df_gen["Tecnología"].isin(filter_list)
    df_gen = df_gen[mask].drop_duplicates(["unique"])
    df_gen.drop(columns=['unique'], inplace=True)
    df_gen.set_index(["Fecha"], inplace=True)
    df_gen["Fecha"] = df_gen.index
    return df_gen


def detalle_generacion_potencia(detail='Total', timestamp=None):
    """

    :param timestamp:
    :param detail: detalle de tecnologías: valores válidos: Embalse, Pasada, Turbo Vapor, Turbo Gas, MCI, Biomasa,
              Eólica, Fotovoltaica, Bio Gas, Termoelectrica, No convencional, Total
    :return: DataFrame con el detalle de generación al corte 30 m
    """
    if timestamp is None:
        timestamp = dt.datetime.now()
        m = timestamp.minute
        if 0 < m < 30:
            timestamp = timestamp.replace(minute=0)
        elif m > 30:
            timestamp = timestamp.replace(minute=30)
        timestamp = timestamp.replace(second=0, microsecond=0)

    time_range = pi_svr.time_range(str(timestamp), str(timestamp))
    # time_range = pi_svr.time_range("2018-8-21 11:00:00", "2018-8-21 11:15:00")
    df_gen = filtrar_generacion_por(detail, time_range)
    df_gen = df_gen[df_gen["Potencia"] > 0]
    return df_gen


def potencia_importacion(time=None):
    if time is None:
        time = dt.datetime.now()
    df_c = df_tags_importation()
    tags_AV = list(set([x for x in df_c["TAG"] if ".AV" in x]))
    df_values = pi_svr.snapshot_of_tag_list(tags_AV, time)
    total = df_values.sum(axis=1).values[0]
    if total < 0:
        total = 0

    return dict(timestamp=str(time), importacion=total)


def potencia_exportacion(time=None):
    if time is None:
        time = dt.datetime.now()
    df_c = df_tags_exportation()
    tags_AV = list(set([x for x in df_c["TAG"] if ".AV" in x]))
    df_values = pi_svr.snapshot_of_tag_list(tags_AV, time)
    total = df_values.sum(axis=1).values[0]
    if total < 0:
        total = 0

    return dict(timestamp=str(time), exportacion=total)


def intercambio_programado_exportacion(time_range=None, span=None):
    if time_range is None:
        time_range = pi_svr.time_range_for_today
    if span is None:
        span = span_30

    tag_pt = obtener_tag_name_por_descripcion("Intercambio programado")
    tag_name = tag_pt.tag_name
    df_values = tag_pt.interpolated(time_range, span)
    df_values[df_values[tag_name] < 0] = 0
    df_values.rename(index=str, columns={tag_name: "Exportación"}, inplace=True)
    return df_values


def intercambio_programado_importacion(time_range=None, span=None):
    if time_range is None:
        time_range = pi_svr.time_range_for_today
    if span is None:
        span = span_30

    tag_pt = obtener_tag_name_por_descripcion("Intercambio programado")
    tag_name = tag_pt.tag_name
    df_values = tag_pt.interpolated(time_range, span)
    df_values[df_values[tag_name] > 0] = 0
    df_values = -df_values
    df_values.rename(index=str, columns={tag_name: "Importación"}, inplace=True)
    return df_values


def obtener_tag_name_por_descripcion(descripcion):
    sql_str = "select * from CFG_Tag_PiSicom WHERE UPPER(TAGPI_DESCRIPCION) = '{0}'".format(descripcion.upper())
    df_tag = pd.read_sql(sql_str, gop_svr.conn)
    if df_tag.empty:
        print("[{0}] [obtener_tag_name_por_descripcion] no encontró la siguiente tag: {1}".format(script_path,
                                                                                                  descripcion))
        return None
    tag_name = df_tag["TAGPI_CODIGO"].iloc[0]
    try:
        pt = osi.PI_point(pi_svr, tag_name)
        return pt
    except Exception as e:
        print(e)


def informacion_sankey_generacion_demanda(timestamp=None):
    if timestamp is None:
        timestamp = time_last_30_m()

    details = ['Hidroeléctrica', 'Termoeléctrica']
    df_result = pd.DataFrame(columns=["source", "target", "value", "timestamp"])
    idx = 0
    for detail in details:

        df_gen = detalle_generacion_potencia(detail, timestamp)
        df_gen = df_gen.groupby("Central").sum()

        if df_gen["Potencia"].sum() > 0:
            df_result.at[idx, "source"] = detail
            df_result.at[idx, "value"] = round(df_gen["Potencia"].sum(), 1)
            idx += 1

    gen_total = detalle_generacion_potencia("Total", timestamp)
    gen_total = gen_total[gen_total["Potencia"] > 0]["Potencia"].sum()
    no_convencional_mw = gen_total - df_result["value"].sum()
    if no_convencional_mw > 0:
        df_result.at[idx, "source"] = "No convecional"
        df_result.at[idx, "value"] = round(no_convencional_mw, 1)
        idx += 1

    # considerar importacion:
    time_range = pi_svr.time_range(str(timestamp), str(timestamp))
    imp_value = intercambio_programado_importacion(time_range)
    imp_value = imp_value["Importación"].iloc[-1]

    if imp_value >= 0.5:
        produccion_mw = round(df_result["value"].sum() + imp_value, 1)
    else:
        produccion_mw = round(df_result["value"].sum(), 1)

    df_result["target"] = "Producción"

    # considerar exportación:
    exp_value = intercambio_programado_exportacion(time_range)
    exp_value = exp_value["Exportación"].iloc[-1]

    if exp_value >= 0.5:
        demanda_nacional_mw = round(produccion_mw - exp_value, 1)
    else:
        demanda_nacional_mw = produccion_mw

    df_result.at[idx, "source"] = "Producción"
    df_result.at[idx, "target"] = "Demanda Nacional"
    df_result.at[idx, "value"] = demanda_nacional_mw

    idx += 1
    if imp_value >= 0.5:
        df_result.at[idx, "source"] = "Importación"
        df_result.at[idx, "target"] = "Producción"
        df_result.at[idx, "value"] = round(imp_value, 1)

    idx += 1
    if exp_value >= 0.5:
        df_result.at[idx, "source"] = "Producción"
        df_result.at[idx, "target"] = "Exportación"
        df_result.at[idx, "value"] = round(exp_value, 1)

    df_result["timestamp"] = str(timestamp)

    return df_result.T


def informacion_sankey_generacion_demanda_regional(timestamp=None):
    if timestamp is None:
        timestamp = time_last_30_m()

    details = ['Hidroeléctrica', 'Termoeléctrica']
    df_result = pd.DataFrame(columns=["source", "target", "value", "timestamp"])
    idx = 0
    for detail in details:

        df_gen = detalle_generacion_potencia(detail, timestamp)
        df_gen = df_gen.groupby("Central").sum()

        if df_gen["Potencia"].sum() > 0:
            df_result.at[idx, "source"] = detail
            df_result.at[idx, "value"] = round(df_gen["Potencia"].sum(), 1)
            idx += 1

    gen_total = detalle_generacion_potencia("Total", timestamp)
    gen_total = gen_total[gen_total["Potencia"] > 0]["Potencia"].sum()
    no_convencional_mw = gen_total - df_result["value"].sum()
    if no_convencional_mw > 0:
        df_result.at[idx, "source"] = "No convecional"
        df_result.at[idx, "value"] = round(no_convencional_mw, 1)
        idx += 1

    time_range = pi_svr.time_range(str(timestamp), str(timestamp))
    imp_value = intercambio_programado_importacion(time_range)
    imp_value = imp_value["Importación"].iloc[-1]

    if imp_value >= 0.5:
        produccion_mw = round(df_result["value"].sum() + imp_value, 1)
    else:
        produccion_mw = round(df_result["value"].sum(), 1)

    df_result["target"] = "Producción"

    # considerar regiones:
    df_dem_regiones = tendencia_demanda_nacional_por_regiones(time_range)
    dem_mw_regiones = 0
    for region in df_dem_regiones:
        df_result.at[idx, "source"] = "Producción"
        df_result.at[idx, "target"] = region
        df_result.at[idx, "value"] = round(df_dem_regiones[region].iloc[0], 1)
        dem_mw_regiones += df_result.at[idx, "value"]
        idx += 1

        # considerar exportación:
    exp_value = intercambio_programado_exportacion(time_range)
    exp_value = exp_value["Exportación"].iloc[-1]

    idx += 1
    if imp_value >= 0.5:
        df_result.at[idx, "source"] = "Importación"
        df_result.at[idx, "target"] = "Producción"
        df_result.at[idx, "value"] = round(imp_value, 1)

    idx += 1
    if exp_value >= 0.5:
        df_result.at[idx, "source"] = "Producción"
        df_result.at[idx, "target"] = "Exportación"
        df_result.at[idx, "value"] = round(exp_value, 1)

    idx += 1
    df_result.at[idx, "source"] = "Producción"
    df_result.at[idx, "target"] = "Pérdidas"
    df_result.at[idx, "value"] = produccion_mw - dem_mw_regiones

    df_result["timestamp"] = str(timestamp)

    return df_result.T


def informacion_sankey_generacion_demanda_nivel_empresarial(timestamp=None):
    if timestamp is None:
        timestamp = time_last_30_m()

    details = ['Hidroeléctrica', 'Termoeléctrica']
    df_result = pd.DataFrame(columns=["source", "target", "value", "timestamp"])

    idx = 0
    for detail in details:

        df_gen = detalle_generacion_potencia(detail, timestamp)
        df_gen = df_gen.groupby("Central").sum()

        if df_gen["Potencia"].sum() > 0:
            df_result.at[idx, "source"] = detail
            df_result.at[idx, "value"] = round(df_gen["Potencia"].sum(), 1)
            idx += 1

    gen_total = detalle_generacion_potencia("Total", timestamp)
    gen_total = gen_total[gen_total["Potencia"] > 0]["Potencia"].sum()
    no_convencional_mw = gen_total - df_result["value"].sum()
    if no_convencional_mw > 0:
        df_result.at[idx, "source"] = "No convecional"
        df_result.at[idx, "value"] = round(no_convencional_mw, 1)
        idx += 1

    time_range = pi_svr.time_range(str(timestamp), str(timestamp))
    imp_value = intercambio_programado_importacion(time_range)
    imp_value = imp_value["Importación"].iloc[-1]

    if imp_value >= 0.5:
        produccion_mw = round(df_result["value"].sum() + imp_value, 1)
    else:
        produccion_mw = round(df_result["value"].sum(), 1)

    df_result["target"] = "Producción"

    # considerar nivel empresarial:
    df_dem_empresas = tendencia_demanda_nacional_por_nivel_empresarial(time_range)
    dem_mw_empresas = 0
    for nivel in df_dem_empresas:
        df_result.at[idx, "source"] = "Producción"
        df_result.at[idx, "target"] = nivel
        df_result.at[idx, "value"] = round(df_dem_empresas[nivel].iloc[0], 1)
        dem_mw_empresas += df_result.at[idx, "value"]
        idx += 1

    # considerar exportación:
    exp_value = intercambio_programado_exportacion(time_range)
    exp_value = exp_value["Exportación"].iloc[-1]

    idx += 1
    if imp_value >= 0.5:
        df_result.at[idx, "source"] = "Importación"
        df_result.at[idx, "target"] = "Producción"
        df_result.at[idx, "value"] = round(imp_value, 1)

    idx += 1
    if exp_value >= 0.5:
        df_result.at[idx, "source"] = "Producción"
        df_result.at[idx, "target"] = "Exportación"
        df_result.at[idx, "value"] = round(exp_value, 1)

    idx += 1
    df_result.at[idx, "source"] = "Producción"
    df_result.at[idx, "target"] = "Pérdidas"
    df_result.at[idx, "value"] = produccion_mw - dem_mw_empresas

    df_result["timestamp"] = str(timestamp)

    return df_result.T


def demanda_por_nivel_empresarial(timestamp=None):
    if timestamp is None:
        timestamp = time_last_30_m()

    config_path_file = script_path.replace('\my_lib\calculations', empresas_file_config)
    df_config = pd.read_excel(config_path_file, sheet_name='demanda_empresas')
    nivel_empresa = list(set(df_config["N_Empresarial"]))
    df_empresas = demanda_empresas(timestamp)
    df_result = pd.DataFrame(columns=df_empresas.columns, index=nivel_empresa)
    for nivel in nivel_empresa:
        emp_list = list(df_config[df_config["N_Empresarial"] == nivel]["EMPRESA"])
        df_aux = df_empresas.loc[emp_list]
        df_result.loc[nivel] = df_aux.sum()

    df_result["timestamp"] = str(timestamp)
    df_result["percentage"] = df_result["current_value"] / df_result["current_value"].sum()
    df_result["percentage"] = [str(round(x * 100, 2)) + " %" for x in df_result["percentage"]]

    df_result.sort_values(by=["current_value"], ascending=False, inplace=True)
    return df_result


def tendencia_demanda_nacional_por_nivel_empresarial(time_range=None, span=None):
    # calculo disponible en 2 minutos
    dt_delta = dt.timedelta(minutes=2)
    tmp_name = "tendencia_demanda_nacional_por_nivel_empresarial" + str(time_range) + str(span) + ".pkl"
    tmp_file = tmp.retrieve_file(tmp_name, dt_delta)
    if tmp_file is not None:
        return tmp_file

    if time_range is None:
        time_range = pi_svr.time_range_for_today_all_day
    if span is None:
        span = span_30

    config_path_file = script_path.replace('\my_lib\calculations', empresas_file_config)
    df_config = pd.read_excel(config_path_file, sheet_name='demanda_empresas')
    df_config.fillna(0, inplace=True)
    nivel_empresa = list(set(df_config["N_Empresarial"]))

    df_result = pd.DataFrame(columns=nivel_empresa)
    for nivel in nivel_empresa:
        mask = (df_config["N_Empresarial"] == nivel)
        tag_list = list(df_config["TAG"][mask])
        df_values = pi_svr.interpolated_of_tag_list(tag_list, time_range, span, numeric=True)
        df_result[nivel] = df_values.sum(axis=1, skipna=False)
        df_result[nivel] = df_result[nivel].round(decimals=1)
    tmp.save_variables(tmp_name, df_result)
    return df_result


def tendencia_demanda_por_provincia(provincia, time_range=None, span=None):
    if "-" in provincia:
        provincia = provincia.replace("-", " ")

    if "Santo Domingo de los Tsáchilas" == provincia:
        provincia = "Sto. Domingo de los Tsachilas"

    # calculo disponible en 2 minutos
    dt_delta = dt.timedelta(minutes=2)
    tmp_name = "tendencia_demanda_por_provincia" + str(provincia) + str(time_range) + str(span) + ".pkl"
    tmp_file = tmp.retrieve_file(tmp_name, dt_delta)
    if tmp_file is not None:
        return tmp_file

    if time_range is None:
        time_range = pi_svr.time_range_for_today_all_day
    if span is None:
        span = span_30

    df_cargas = detalle_puntos_entrega(provincia, time_range.StartTime.ToString("yyyy-MM-dd"))
    str_item = "Subestacion"
    item_set = set(df_cargas[str_item])
    if len(item_set) == 1:
        str_item = "Posicion"
        item_set = set(df_cargas[str_item])

    df_result = pd.DataFrame(columns=item_set)
    for item in item_set:
        mask = (df_cargas[str_item] == item)
        tag_list = list(df_cargas["TAG"][mask])
        df_values = pi_svr.interpolated_of_tag_list(tag_list, time_range, span, numeric=True)
        df_values[df_values < 0] = 0
        df_result[item] = df_values.sum(axis=1, skipna=False)
        df_result[item] = df_result[item].round(decimals=1)

    df_aux = df_result.dropna()
    df_result = df_result.T.sort_values(by=[df_aux.index[-1]], ascending=False)
    df_result = df_result.T
    tmp.save_variables(tmp_name, df_result)
    return df_result


def demanda_por_provincia(provincia, timestamp=None):
    if "-" in provincia:
        provincia = provincia.replace("-", " ")

    if "Santo Domingo de los Tsáchilas" == provincia:
        provincia = "Sto. Domingo de los Tsachilas"

    if timestamp is None:
        timestamp = time_last_30_m()
        time_range = pi_svr.time_range(str(timestamp), str(timestamp))
    else:
        time_range = None

    df_demanda = tendencia_demanda_por_provincia(provincia, time_range)
    df_cargas = detalle_puntos_entrega(provincia, timestamp)
    df_cargas = df_cargas[df_cargas['Provincia'] == provincia]
    df_max = pd.DataFrame(index=df_demanda.columns, columns=["max_value"])
    df_max["max_value"] = 0

    str_item = "Subestacion"
    item_set = set(df_cargas[str_item])
    if len(item_set) == 1:
        str_item = "Posicion"
        item_set = set(df_cargas[str_item])

    for item in item_set:
        mask = df_cargas[str_item] == item
        p_list = list(df_cargas[mask]["Codigo"])
        max_v = max_mw_posicion(p_list)
        df_max["max_value"].loc[item] += max_v

        # df_max["max_value"].loc[subestation] = df_max["max_value"].loc[subestation]/ len(p_list)

    df_result = pd.DataFrame(index=df_demanda.columns,
                             columns=["current_value", "max_value", "dif", "percentage", "timestamp"])
    for subestation in df_demanda.columns:
        df_result.at[subestation, "current_value"] = df_demanda[subestation].loc[timestamp]
        df_result.at[subestation, "max_value"] = df_max.at[subestation, "max_value"]
        check = df_result.at[subestation, "max_value"] - df_result.at[subestation, "current_value"]
        if check > 0:
            df_result.at[subestation, "dif"] = round(check, 1)
        else:
            df_result.at[subestation, "dif"] = 0

    df_result["timestamp"] = str(timestamp)
    df_result["percentage"] = df_result["current_value"] / df_result["current_value"].sum()
    df_result["percentage"] = [str(round(x * 100, 2)) + " %" for x in df_result["percentage"]]

    # df_result.sort_values(by=["current_value"], ascending=False, inplace=True)
    return df_result


def max_mw_posicion(posicion_list, time_range=None):
    dt_delta = dt.timedelta(hours=12)

    if time_range is None:
        t_fin = timestamp_now()
        t_ini = dt.datetime.now() - dt.timedelta(days=365)
    else:
        t_ini = time_range.StartTime.ToString("yyyy-MM-dd hh:mm:ss")
        t_fin = time_range.EndTime.ToString("yyyy-MM-dd hh:mm:ss")

    tmp_name = "max_mw_posicion" + str(posicion_list) + str(t_fin)[:10] + ".pkl"
    tmp_file = tmp.retrieve_file(tmp_name, dt_delta)
    if tmp_file is not None:
        return tmp_file

    sql_str = "SELECT t.Posicion, t.MV_Validado MW, CONCAT(t.Fecha, ' ' , t.Hora) as Timestamp " + \
              " FROM SIVO.dbo.DV_Entrega t where t.Fecha" + \
              " between '{0}' and '{1}' " + \
              " and t.Posicion in ( {2} ) order by Timestamp"

    posicion_list = str(posicion_list)
    posicion_list = posicion_list[1:].replace("]", "")

    sql_str = sql_str.format(t_ini, t_fin, posicion_list)
    try:
        pd_resp = pd.read_sql(sql_str, gop_svr.conn)
        pd_resp = pd_resp.groupby("Timestamp")["MW"].sum()
        max_value = pd_resp.max()
        tmp.save_variables(tmp_name, max_value)
        return max_value
    except Exception as e:
        print(e)
        return 0


def detalle_puntos_entrega(provincia=None, timestamp=None):
    if timestamp is None:
        timestamp = time_last_30_m()

    sql_str = "SELECT PSC.IdPosicionConectada ID, UN.Nombre UNegocio,SUB.Nombre Subestacion, C.Nombre Posicion," + \
              " c.Codigo, TAG.TAG, TAG.Descripcion, PR.Nombre Provincia, PSC.FechaAlta, PSC.FechaBaja" + \
              " FROM SIVO.dbo.CFG_PosicionesConectadas PSC" + \
              " INNER JOIN CFG_ElementosConectados ECO on ECO.IdElementoConectado = PSC.IdElementoConectado" + \
              " INNER JOIN CFG_Carga CAR on ECO.IdCarga = CAR.IdCarga" + \
              " INNER JOIN CFG_UnidadNegocio UN on CAR.IdUNegocio = UN.IdUNegocio" + \
              " INNER JOIN CFG_SubEstacion SUB on PSC.IdSubestacion = SUB.IdSubestacion" + \
              " INNER JOIN CFG_Posicion C on PSC.IdPosicion = C.IdPosicion" + \
              " INNER JOIN CFG_ElementoTAG ETAG on c.IdPosicion = ETAG.IdElemento" + \
              " INNER JOIN CFG_TAG TAG on ETAG.IdTAG = TAG.IdTAG" + \
              " INNER JOIN CFG_Provincia PR on SUB.IdProvincia = PR.IdProvincia" + \
              " WHERE '{0}' between PSC.FechaAlta and isnull(PSC.FechaBaja, '{0}')" + \
              " AND TAG.TAG LIKE '%P.CARGA%.AV'" + \
              " {1}" + \
              " ORDER BY SUB.Nombre"

    if provincia is None:
        sql_str = sql_str.format(timestamp, "")
        df_cargas = pd.read_sql(sql_str, gop_svr.conn)

    else:
        sql_pr = "AND PR.Nombre = '{0}'".format(provincia)
        sql_str = sql_str.format(timestamp, sql_pr)
        df_cargas = pd.read_sql(sql_str, gop_svr.conn)

    config_path_file = script_path.replace('\my_lib\calculations', empresas_file_config)
    df_exceptions = pd.read_excel(config_path_file, sheet_name='excepciones_carga')
    exclude_idx = list(set(df_exceptions["ID"]).intersection(df_cargas["ID"]))
    df_cargas.index = df_cargas["ID"]
    df_cargas.drop(index=exclude_idx, inplace=True)
    df_exceptions = df_exceptions[df_exceptions["Provincia"] == provincia]
    df_cargas = df_cargas.append(df_exceptions)

    return df_cargas


"""
FUNCIONES AUXILIARES:
"""


def integrating_by_average(df, dx):
    # integrating using average:
    mean_y = (df[:-1] + df.shift(-1)[:-1]) / 2
    # delta_x = x.shift(-1)[:-1] - x[:-1]
    # scaled_int = mean_y.multiply(delta_x)
    scaled_int = mean_y * dx
    scaled_int.fillna(0, inplace=True)
    return scaled_int.sum()


def timestamp_now():
    dt = datetime.datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def time_last_30_m():
    dt = datetime.datetime.now()
    m = dt.minute
    if m < 30:
        dt = dt.replace(minute=0)
    if m > 30:
        dt = dt.replace(minute=30)
    dt = dt.replace(second=0, microsecond=0)

    return dt


def test():
    # other_generation_detail_now()
    # generation_energy_by_tech_now()
    # def total_generation_now():
    # x = cal_exportation_now()
    # y = cal_importation_now()
    # r = generation_energy_by_tech_now()
    # generation_detail_now(['Embalse', 'Pasada'])
    # generation_trend_today_by_tech()
    # trend_hydro_and_others_today()
    # demanda_empresas_now(7)
    # maxima_demanda_nacional("2017")
    # filtrar_generacion_por("Total")
    # detalle_generacion_potencia("Total")
    # informacion_sankey_generacion_demanda()
    # demanda_nacional("2018-08-21", "2018-08-22")
    tag = obtener_tag_name_por_descripcion("Demanda Nacional")


if __name__ == "__main__":
    perform_test = True
    if perform_test:
        test()
