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
import numpy as np

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
empresas_file_config = r"\static\app_data\maps\empr_electricas_por_provincia.xlsx"

yyyy_MM_dd_HH_mm_ss = "yyyy-MM-dd HH:mm:ss"
yyyy_MM_dd = "yyyy-MM-dd"


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
    ini_date, end_date = pi_svr.start_and_time_of(time_range)
    sql = "SELECT V.IdUnidad, U.Codigo U_Codigo, V.Central,V.Unidad, V.Tecnología ,V.TAG," + \
          " V.Potencia,V.Fecha" + \
          " FROM [BOSNI].[dbo].[vHIST_UNIDAD_POT_EFECTIVA] AS V" + \
          " INNER JOIN CFG_Unidad U ON U.IdUnidad = V.IdUnidad" + \
          " WHERE [Fecha] between '{0}'  and '{1}'"

    sql = sql.format(ini_date, end_date)

    df_gen = pd.read_sql(sql, gop_svr.conn)

    # añadiendo generación no convencional (Fotovoltaica):
    # TODO: Caso Fotovoltaicas, Dado que no están todas implementadas en SIVO:
    # Se recoge el total de generación fotovoltaica en esta central
    caso_fotovoltaica = True
    if caso_fotovoltaica:
        mask = df_gen["Tecnología"] == "Fotovoltaica"
        try:
            df_gen[mask].drop(inplace=True)
        except ValueError:
            pass
        tag_total_fotovoltaica = obtener_tag_name_por_descripcion("Generación Fotovoltaica")
        df_values = tag_total_fotovoltaica.interpolated(time_range, span_30)
        tag_name = tag_total_fotovoltaica.tag_name
        for idx in df_values.index:
            df_aux = pd.DataFrame(
                ["Fotovoltaica", "Total", "Fotovoltaica", tag_name, df_values.at[idx, tag_name], idx, "FOTO-TOTAL"],
                index=["Central", "Unidad", "Tecnología", "TAG", "Potencia", "Fecha", "U_Codigo"])
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
    df_r.at["Calidad de servicio", "value"] = total - df_r["value"].loc["Gas natural"] - df_r["value"].loc[
        "No convencional"]
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

    # tagname de demanda nacional
    path_config_file = script_path.replace('my_lib\\calculations', 'hmm_application\\config.xlsx')
    df_config = pd.read_excel(path_config_file)
    df_config.set_index("entity", inplace=True)
    tag_name = df_config.at["demanda-nacional", 'tag']
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

    return df_demanda


def demanda_nacional_desde_sivo(ini_date=None, fin_date=None):
    """
    Esta función calcula la demanda nacional usando la matriz de generación de SIVO
    :param ini_date:  string en formato: yyyy-mm-dd hh:mm:ss
    :param fin_date:  string en formato: yyyy-mm-dd hh:mm:ss
    :return:
    """

    if ini_date is None and fin_date is None:
        time_range = pi_svr.time_range_for_today_all_day
    elif isinstance(ini_date, str) and ini_date.isnumeric():
        ini_date = float(ini_date)/1000
        ini_date = dt.datetime.fromtimestamp(ini_date)
        fin_date = ini_date + dt.timedelta(days=1)
        time_range = pi_svr.time_range(ini_date, fin_date)
    elif isinstance(ini_date, str) and fin_date is None:
        fin_date = convert_str_to_time(ini_date)
        fin_date = fin_date + dt.timedelta(days=1)
        time_range = pi_svr.time_range(ini_date, fin_date)
    else:
        time_range = pi_svr.time_range(ini_date, fin_date)

    str_ini, str_end = pi_svr.start_and_time_of(time_range)

    sql_str = "SELECT Empresa, UNegocio, Central, GrupoGeneracion, Unidad, concat(Fecha, ' ', Hora) Fecha" + \
              " ,MV_Validado Potencia,  TAG_MV FROM DV_Generacion" + \
              " WHERE Fecha BETWEEN '{0}' AND '{1}'".format(str_ini, str_end)

    df_gen = pd.read_sql(sql_str, gop_svr.conn)
    if df_gen.empty:
        df_gen = generation_matrix(time_range)

    df_gen = df_gen[df_gen["Potencia"] > 0]
    df_details = df_gen[["Potencia", "Fecha", "Central"]].groupby(["Central", "Fecha"]).sum()
    df_gen = df_gen[["Potencia", "Fecha", "Central"]].groupby(["Fecha"]).sum()
    df_gen.index = pd.to_datetime(df_gen.index)

    df_gen.sort_index(inplace=True)
    df_gen = df_gen.loc[str_ini:str_end]

    df_importacion = importacion_desde_sivo(time_range)
    if df_importacion.empty:
        df_importacion = intercambio_programado_importacion(time_range)
        df_importacion = df_importacion["Importación"]
    else:
        df_importacion = df_importacion.groupby(["Timestamp"])["MW"].sum()

    df_exportacion = exportacion_desde_sivo(time_range)
    if df_exportacion.empty:
        df_exportacion = intercambio_programado_exportacion(time_range)
        df_exportacion = df_exportacion["Exportación"]
    else:
        df_exportacion = df_exportacion.groupby(["Timestamp"])["MW"].sum()

    date_range = pd.date_range(str_ini, str_end, freq="30T")
    df_result = pd.DataFrame(index=[str(x) for x in date_range], columns=["Demanda nacional"])
    df_result["Demanda nacional"] = df_gen["Potencia"] + df_importacion - df_exportacion

    return df_result


def importacion_desde_sivo(time_range_or_ini_time=None, end_time=None):
    if time_range_or_ini_time is None and end_time is None:
        time_range_or_ini_time = pi_svr.time_range_for_today_all_day
    elif isinstance(time_range_or_ini_time, str):
        end_time = convert_str_to_time(time_range_or_ini_time)
        end_time += dt.timedelta(days=1)
        time_range_or_ini_time = pi_svr.time_range(time_range_or_ini_time, str(end_time))
    elif time_range_or_ini_time is not None and end_time is not None:
        time_range_or_ini_time = pi_svr.time_range(time_range_or_ini_time, end_time)

    str_ini, str_end = pi_svr.start_and_time_of(time_range_or_ini_time)

    df_import = df_tags_importation()
    ls_circuitos = str(set(df_import["Codigo"])).replace('{', '').replace('}', '')
    sql_str = "SELECT Empresa, UNegocio, Elemento, MV_Validado MW, TAG, CONCAT(Fecha, ' ', Hora) Timestamp " \
              "FROM DV_Flujo WHERE Elemento IN ({0}) " \
              "AND Fecha BETWEEN '{1}' AND '{2}' " \
              "AND TipoValidacion = 'FLUJO2' " \
              " ORDER BY Timestamp".format(ls_circuitos, str_ini, str_end)

    df_import = pd.read_sql(sql_str, gop_svr.conn)
    if not df_import.empty:
        df_import.set_index('Timestamp', inplace=True)
        df_import.index = pd.to_datetime(df_import.index)
        mask = (df_import.index >= pd.to_datetime(str_ini)) & (df_import.index <= pd.to_datetime(str_end))
        df_import = df_import[mask]
        df_import["MW"][df_import["MW"] < 0] = 0
    return df_import


def exportacion_desde_sivo(time_range_or_ini_time=None, end_time=None):
    if time_range_or_ini_time is None and end_time is None:
        time_range_or_ini_time = pi_svr.time_range_for_today_all_day
    elif isinstance(time_range_or_ini_time, str):
        end_time = convert_str_to_time(time_range_or_ini_time)
        end_time += dt.timedelta(days=1)
        time_range_or_ini_time = pi_svr.time_range(time_range_or_ini_time, str(end_time))
    elif time_range_or_ini_time is not None and end_time is not None:
        time_range_or_ini_time = pi_svr.time_range(time_range_or_ini_time, end_time)

    str_ini, str_end = pi_svr.start_and_time_of(time_range_or_ini_time)

    df_export = df_tags_exportation()
    ls_circuitos = str(set(df_export["Codigo"])).replace('{', '').replace('}', '')
    sql_str = "SELECT Empresa, UNegocio, Elemento, MV_Validado MW, TAG, CONCAT(Fecha, ' ', Hora) Timestamp " \
              "FROM DV_Flujo WHERE Elemento IN ({0}) " \
              "AND Fecha BETWEEN '{1}' AND '{2}' " \
              "AND TipoValidacion = 'FLUJO1' " \
              " ORDER BY Timestamp".format(ls_circuitos, str_ini, str_end)

    df_export = pd.read_sql(sql_str, gop_svr.conn)
    if not df_export.empty:
        df_export.set_index('Timestamp', inplace=True)
        df_export.index = pd.to_datetime(df_export.index)
        mask = (df_export.index >= pd.to_datetime(str_ini)) & (df_export.index <= pd.to_datetime(str_end))
        df_export = df_export[mask]
        df_export["MW"][df_export["MW"] < 0] = 0
    return df_export


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
    sql_str = "SELECT t.Nom_UNegocio, t.Fecha, PotMax MW FROM SIVO.dbo.TMP_System_Dem t " + \
              "where YEAR(t.Fecha) = {0}"

    df_max = pd.read_sql(sql_str.format(year), gop_svr.conn)
    if df_max.empty:
        year = year - 1
        df_max = pd.read_sql(sql_str.format(year), gop_svr.conn)

    df_max.dropna(inplace=True)
    df_max.drop_duplicates(subset=['Nom_UNegocio'], keep='first', inplace=True)
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
        year = dt.datetime.now().year

    sql_str = 'SELECT TOP 1 * FROM [SIVO].[dbo].[TMP_System_Perdidas_Potencia] PP' + \
              ' WHERE YEAR(PP.Fecha)=yyyy ORDER BY PP.DeePerdidas DESC'
    sql_f = sql_str.replace("yyyy", str(year))
    df = pd.read_sql(sql_f, gop_svr.conn)
    if df.empty:
        sql_f = sql_str.replace("yyyy", str(year-1))
        df = pd.read_sql(sql_f, gop_svr.conn)
    # print(df)
    return df.T


def tendencia_demanda_nacional_por_regiones(time_range=None, span=None):
    # calculo disponible en 2 minutos
    valid_range = [time_last_30_m(), tiempo_de_corte(30)]
    tmp_name = "tendencia_demanda_nacional_por_regiones" + str(time_range) + str(span) + ".pkl"
    tmp_file = tmp.retrieve_file(tmp_name)
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
    tmp.save_variables(tmp_name, df_result, valid_range=valid_range)
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
    # print(df_gen)
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
        df_gen = df_gen.groupby("Central")["Potencia"].sum()
        # print(df_gen)

        if df_gen.sum() > 0:
            df_result.at[idx, "source"] = detail
            df_result.at[idx, "value"] = round(df_gen.sum(), 1)
            idx += 1

    gen_total = detalle_generacion_potencia("Total", timestamp)
    gen_total = gen_total[gen_total["Potencia"] > 0]["Potencia"].sum()
    try:
        no_convencional_mw = gen_total - df_result["value"].sum()
        if no_convencional_mw > 0:
            df_result.at[idx, "source"] = "No convencional"
            df_result.at[idx, "value"] = round(no_convencional_mw, 1)
            idx += 1
    except Exception as e:
        print(e)

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
        df_gen = df_gen.groupby("Central")["Potencia"].sum()

        if df_gen.sum() > 0:
            df_result.at[idx, "source"] = detail
            df_result.at[idx, "value"] = round(df_gen.sum(), 1)
            idx += 1

    gen_total = detalle_generacion_potencia("Total", timestamp)
    gen_total = gen_total[gen_total["Potencia"] > 0]["Potencia"].sum()
    no_convencional_mw = gen_total - df_result["value"].sum()
    if no_convencional_mw > 0:
        df_result.at[idx, "source"] = "No convencional"
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
        df_gen = df_gen.groupby("Central")["Potencia"].sum()

        if df_gen.sum() > 0:
            df_result.at[idx, "source"] = detail
            df_result.at[idx, "value"] = round(df_gen.sum(), 1)
            idx += 1

    gen_total = detalle_generacion_potencia("Total", timestamp)
    gen_total = gen_total[gen_total["Potencia"] > 0]["Potencia"].sum()
    no_convencional_mw = gen_total - df_result["value"].sum()
    if no_convencional_mw > 0:
        df_result.at[idx, "source"] = "No convencional"
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


def informacion_sankey_generacion_demanda_por_provincia(provincia, timestamp=None):
    if timestamp is None:
        timestamp = time_last_30_m()

    time_range = pi_svr.time_range(str(timestamp), str(timestamp))
    details = ['Gen. Inmersa', 'Gen. Local', 'Desde S.N.I', 'Hacia S.N.I', 'Demanda ' + provincia]
    df_result = pd.DataFrame(columns=["source", "target", "value", "timestamp"])

    df_gen = generacion_por_provincia(provincia, time_range)
    df_detalle = detalle_puntos_entrega(provincia, timestamp)
    lst_posiciones = list(df_detalle["Codigo"])
    df_gen_inmersa = generacion_inmersa_en_puntos_carga(lst_posiciones, time_range)
    set_list = set(df_gen.columns).intersection(df_gen_inmersa.columns)
    if len(set_list) == 0 and len(df_gen_inmersa.columns) > 0:
        df_generacion_local = df_gen
        df_gen_inmersa = pd.DataFrame()
    else:
        df_generacion_local = df_gen.drop(set_list, axis=1)
        df_gen_inmersa = df_gen_inmersa[list(set_list)]

    gen_inmersa, gen_local = 0, 0
    if not df_gen_inmersa.empty:
        gen_inmersa = df_gen_inmersa.sum(axis=1).iloc[0]
    if not df_generacion_local.empty:
        gen_local = df_generacion_local.sum(axis=1).iloc[0]
    demanda_provincia = demanda_por_provincia(provincia, timestamp)["current_value"].sum()
    idx = 0

    # El S.N.I esta aportando potencia para cubrir la demanda
    if demanda_provincia > (gen_inmersa + gen_local):
        sni = demanda_provincia - (gen_inmersa + gen_local)
        values = [gen_inmersa, gen_local, sni]
        for d, v in zip(details, values):
            idx += 1
            if v > 0:
                df_result.at[idx, "source"] = d
                df_result.at[idx, "value"] = round(v, 1)
                df_result.at[idx, "target"] = "Demanda " + provincia

    # El S.N.I recibe potencia de los generadores locales e inmersa
    else:
        sni = (gen_inmersa + gen_local) - demanda_provincia
        values = [gen_inmersa, gen_local]
        for d, v in zip(details, values):
            idx += 1
            if v > 0:
                df_result.at[idx, "source"] = d
                df_result.at[idx, "value"] = round(v, 1)
                df_result.at[idx, "target"] = "Gen. " + provincia

        values = [sni, demanda_provincia]
        for d, v in zip(details[3:], values):
            idx += 1
            if v > 0:
                df_result.at[idx, "source"] = "Gen. " + provincia
                df_result.at[idx, "value"] = round(v, 1)
                df_result.at[idx, "target"] = d

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
    valid_range = [time_last_30_m(), tiempo_de_corte(30)]
    tmp_name = "tendencia_demanda_nacional_por_nivel_empresarial" + str(time_range) + str(span) + ".pkl"
    tmp_file = tmp.retrieve_file(tmp_name)
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
    tmp.save_variables(tmp_name, df_result, valid_range=valid_range)
    return df_result


def tendencia_demanda_por_provincia(provincia, time_range=None, span=None):
    if "-" in provincia:
        provincia = provincia.replace("-", " ")

    if "Santo Domingo de los Tsáchilas" == provincia:
        provincia = "Sto. Domingo de los Tsachilas"

    # calculo válido en cada 30 minutos
    valid_range = [time_last_30_m(), tiempo_de_corte(30)]
    tmp_name = "tendencia_demanda_por_provincia_" + str(provincia) + str(time_range) + str(span) + ".pkl"
    tmp_file = tmp.retrieve_file(tmp_name)
    if tmp_file is not None:
        return tmp_file

    if time_range is None:
        time_range = pi_svr.time_range_for_today_all_day
    if span is None:
        span = span_30

    str_ini, str_end = pi_svr.start_and_time_of(time_range)

    df_cargas = detalle_puntos_entrega(provincia, str_ini)
    str_item = "Subestacion"
    item_set = set(df_cargas[str_item])
    if len(item_set) == 1:
        str_item = "Posicion"
        item_set = set(df_cargas[str_item])

    df_result = pd.DataFrame(columns=item_set)
    for item in item_set:
        mask = (df_cargas[str_item] == item)
        posiciones = list(df_cargas["Codigo"][mask])
        tag_list = list(df_cargas["TAG"][mask])

        # Buscar demanda en SIVO, si no existe traerlos de PI-Server:
        df_values = demanda_por_posicion_desde_sivo(posiciones, time_range)
        if df_values.empty:
            df_values = pi_svr.interpolated_of_tag_list(tag_list, time_range, span, numeric=True)
            df_values.columns = posiciones

        # Obtener generación inmersa desde SIVO
        df_gen_inmersa = generacion_inmersa_en_puntos_carga(posiciones, time_range)

        if not df_gen_inmersa.empty:
            df_values = df_values.join(df_gen_inmersa, how='outer')

        # En el caso que sea menor que cero entonces la demanda es cero
        df_values = df_values.sum(axis=1, skipna=False)
        df_values[df_values < 0] = 0
        df_result[item] = df_values
        df_result[item] = df_result[item].round(decimals=1)

    df_aux = df_result.dropna()
    df_result = df_result.T.sort_values(by=[df_aux.index[-1]], ascending=False)
    df_result = df_result.T
    tmp.save_variables(tmp_name, df_result, valid_range)
    return df_result


def demanda_por_posicion_desde_sivo(lst_posiciones, time_range=None):
    if time_range is None:
        time_range = pi_svr.time_range_for_today_all_day
    ini_date, end_date = pi_svr.start_and_time_of(time_range)

    str_posiciones = ''
    if lst_posiciones is not None:
        if isinstance(lst_posiciones, str):
            str_posiciones = [lst_posiciones]

        if isinstance(lst_posiciones, list):
            str_posiciones = str(lst_posiciones).replace('[', '').replace(']', '')
        str_posiciones = 'Posicion IN ({0})'.format(str_posiciones)

    sql_str = "SELECT Posicion, MV_Validado, concat(Fecha, ' ', Hora) Timestamp " \
              " FROM DV_Entrega " \
              " WHERE {0} " \
              " AND Fecha BETWEEN '{1}' AND '{2}'".format(str_posiciones, ini_date, end_date)

    df_demanda = pd.read_sql(sql_str, gop_svr.conn)
    if not df_demanda.empty:
        df_demanda = df_demanda.pivot(index="Timestamp", columns="Posicion", values="MV_Validado")
        df_demanda.index = pd.to_datetime(df_demanda.index)
        mask = (pd.to_datetime(ini_date) <= df_demanda.index) & \
               (df_demanda.index <= pd.to_datetime(end_date))
        df_demanda = df_demanda[mask]

    return df_demanda


def demanda_por_provincia(provincia, timestamp=None):
    if "-" in provincia:
        provincia = provincia.replace("-", " ")

    if "Santo Domingo de los Tsáchilas" == provincia:
        provincia = "Sto. Domingo de los Tsachilas"

    if timestamp is None:
        timestamp = time_last_30_m()

    time_range = pi_svr.time_range(str(timestamp), str(timestamp))

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

    df_result = pd.DataFrame(index=df_demanda.columns,
                             columns=["current_value", "max_value", "dif", "percentage", "timestamp"])
    for item in df_demanda.columns:
        df_result.at[item, "current_value"] = df_demanda[item].loc[timestamp]
        df_result.at[item, "max_value"] = df_max.at[item, "max_value"]
        check = df_result.at[item, "max_value"] - df_result.at[item, "current_value"]
        if check > 0:
            df_result.at[item, "dif"] = round(check, 1)
        else:
            df_result.at[item, "dif"] = 0

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
        t_ini, t_fin = pi_svr.start_and_time_of(time_range)

    tmp_name = "max_mw_posicion" + str(posicion_list) + str(t_fin)[:10] + ".pkl"
    tmp_file = tmp.retrieve_file(tmp_name)
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
        tmp.save_variables(tmp_name, max_value, dt_delta=dt_delta)
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


def detalle_generacion_inmersa(ls_position_code=None, timestamp=None):
    if ls_position_code is None:
        ls_position_code = ""
    elif len(ls_position_code) == 0:
        return pd.DataFrame()
    else:
        if isinstance(ls_position_code, str):
            ls_position_code = [ls_position_code]
        ls_position_code = str(ls_position_code).replace("[", "").replace("]", "")
        ls_position_code = " AND P.Codigo IN ({0})".format(ls_position_code)

    if timestamp is None:
        timestamp = timestamp_now()

    sql_str = "SELECT P.Codigo Posicion, U.Codigo CodUnidad, U.Nombre Unidad, PU.FechaInicio, PU.FechaFin" \
              " FROM CFG_Posicion P " \
              " INNER JOIN CFG_PosicionUnidad PU ON P.IdPosicion=PU.IdPosicion " \
              " INNER JOIN CFG_Unidad U ON PU.IdUnidad=U.IdUnidad " \
              " WHERE '{1}' between PU.FechaInicio " \
              " AND isnull(PU.FechaFin, '{1}')" \
              " {0} ".format(ls_position_code, timestamp)

    df_gen_inmersa = pd.read_sql(sql_str, gop_svr.conn)
    return df_gen_inmersa


def generacion_inmersa_en_puntos_carga(list_posiciones=None, time_range=None):
    if time_range is None:
        timestamp = timestamp_now()
        time_range = pi_svr.time_range_for_today_all_day
    else:
        timestamp = time_range.EndTime.ToString("yyyy-MM-dd")

    df_gen_inmersa = detalle_generacion_inmersa(list_posiciones, timestamp)
    if df_gen_inmersa.empty:
        return pd.DataFrame()

    code_gen_list = list(df_gen_inmersa["CodUnidad"])
    if len(code_gen_list) > 0:

        # Buscar generación en SIVO, si no existe, traerla de la matriz de generacion
        df_value_gen = generacion_desde_sivo(code_gen_list, time_range)
        if df_value_gen.empty:
            df_value_gen = generation_matrix(time_range)
            mask = df_value_gen["U_Codigo"].isin(code_gen_list)
            df_value_gen = df_value_gen[mask]

            # if not df_value_gen.empty:
            df_value_gen = df_value_gen.pivot(index='Fecha', columns='U_Codigo',
                                              values='Potencia')

            # TODO: considerar valor de cero cuando no exista el index.
            df_value_gen.fillna(value=0, inplace=True)
            df_value_gen.index = pd.to_datetime(df_value_gen.index)
            return df_value_gen

        return df_value_gen

    return pd.DataFrame()


def generacion_desde_sivo(lst_cod_unidades=None, time_range=None):
    if time_range is None:
        time_range = pi_svr.time_range_for_today_all_day

    str_ini, str_end = pi_svr.start_and_time_of(time_range)

    str_cod_unidades = ''
    if lst_cod_unidades is not None:
        if isinstance(lst_cod_unidades, str):
            str_cod_unidades = [lst_cod_unidades]
        if isinstance(lst_cod_unidades, list):
            str_cod_unidades = str(lst_cod_unidades).replace('[', '').replace(']', '')
            str_cod_unidades = 'Unidad IN ({0}) AND'.format(str_cod_unidades)

    sql_str = "SELECT concat(Fecha, ' ', Hora) Timestamp, " \
              " Empresa, Central, GrupoGeneracion, Unidad, MV_Validado " \
              " FROM DV_Generacion " \
              " WHERE {0} " \
              " Fecha between '{1}' AND '{2}'".format(str_cod_unidades, str_ini, str_end)

    df_gen = pd.read_sql(sql_str, gop_svr.conn)
    if df_gen.empty:
        df_gen = generation_matrix(time_range)
        ls_fechas = list(set(df_gen["Fecha"]))
        ls_fechas.sort()
        ind_timestamp = pd.to_datetime(ls_fechas)
        if lst_cod_unidades is not None:
            mask = df_gen['U_Codigo'].isin(lst_cod_unidades)
            df_gen = df_gen[mask]
        df_gen = df_gen.pivot(index='Fecha', columns='U_Codigo', values='Potencia')
        df_gen.fillna(0, inplace=True)
        df_gen.index = pd.to_datetime(df_gen.index)
        df_gen = df_gen.reindex(ind_timestamp, fill_value=0)
    else:
        df_gen = df_gen.pivot(index='Timestamp', columns="Unidad", values="MV_Validado")
        df_gen.index = pd.to_datetime(df_gen.index)
        mask = (pd.to_datetime(str_ini) <= df_gen.index) & \
               (df_gen.index <= pd.to_datetime(str_end))
        df_gen = df_gen[mask]
    return df_gen


def generacion_por_provincia(provincia, time_range=None):
    if "-" in provincia:
        provincia = provincia.replace("-", " ")

    if "Santo Domingo de los Tsáchilas" == provincia:
        provincia = "Sto. Domingo de los Tsachilas"

    provincia = provincia.upper()

    if time_range is None:
        time_range = pi_svr.time_range_for_today_all_day

    str_ini, str_end = pi_svr.start_and_time_of(time_range)

    sql_str = "SELECT Pr.Nombre, C2.Nombre Central, Un.Codigo, Un.Nombre, Un.FechaAlta, Un.FechaBaja" \
              " FROM CFG_Unidad Un " \
              " INNER JOIN CFG_Central C2 ON Un.IdCentral = C2.IdCentral " \
              " INNER JOIN CFG_Provincia Pr ON C2.IdProvincia = Pr.IdProvincia " \
              " WHERE UPPER(Pr.Nombre) = '{0}' " \
              " AND '{1}' BETWEEN Un.FechaAlta " \
              " AND isnull(Un.FechaBaja, '{1}')".format(provincia, str_ini)

    df_cod_unidades = pd.read_sql(sql_str, con=gop_svr.conn)
    if not df_cod_unidades.empty:
        lst_unidades = list(df_cod_unidades["Codigo"])
        df_gen = generacion_desde_sivo(lst_unidades, time_range)
        return df_gen
    else:
        return pd.DataFrame()


def reserva_de_generacion(timestamp=None, n_times=0):
    if timestamp is None:
        timestamp = time_last_30_m()
    elif isinstance(timestamp, str):
        timestamp = convert_str_to_time(timestamp)

    timestamp = time_last_30_m(timestamp)

    # calculo válido para cualquier momento ([None, None])
    collection_name = "reserva_de_generacion"
    cal_id = str(timestamp)
    success, data_dict = tmp.retrieve_dict_in_cal_db(collection_name, cal_id)
    if success and data_dict is not None:
        return data_dict

    time_range = pi_svr.time_range(str(timestamp), str(timestamp))
    df_indisponibilidad = detalle_de_indisponibilidad(timestamp)
    df_efectiva = potencia_efectiva_sni(str(timestamp))
    p_efectiva = round(df_efectiva["PotenciaEfectiva"].sum(axis=0), 1)

    if dt.datetime.now() <= timestamp:
        resp = dict(p_efectiva=p_efectiva, p_indisponible_linea=None,
                    p_disponible_linea=None, p_generacion=None,
                    p_indisponible_total=None, p_disponible_total=None,
                    p_reserva=None, p_efectiva_linea=None, timestamp=str(timestamp))
        return resp

    p_indisponible_total = round(df_indisponibilidad.loc["POT_INDISPONIBLE"].sum(axis=0), 1)
    p_disponible_total = p_efectiva - p_indisponible_total

    df_gen_linea = generacion_desde_sivo(None, time_range).T
    mask = df_gen_linea.iloc[:, 0] > 0
    df_gen_linea = df_gen_linea[mask]
    set_linea = set(df_gen_linea.index).intersection(df_indisponibilidad.columns)
    df_indisponibilidad_linea = df_indisponibilidad[list(set_linea)]
    p_efectiva_en_linea = round(df_indisponibilidad_linea.loc["POT_EFECTIVA"].sum(axis=0, skipna=True), 1)
    p_indisponible_linea = round(df_indisponibilidad_linea.loc["POT_INDISPONIBLE"].sum(axis=0, skipna=True), 1)
    # print(df_indisponibilidad_linea.loc["POT_INDISPONIBLE"])
    p_disponible_linea = round(p_efectiva_en_linea - p_indisponible_linea, 1)
    p_generacion = round(df_gen_linea.iloc[:, 0].sum(skipna=False), 1)
    p_reserva = round(p_disponible_linea - p_generacion, 1)
    resp = dict(p_efectiva=p_efectiva, p_indisponible_linea=p_indisponible_linea,
                p_disponible_linea=p_disponible_linea, p_generacion=p_generacion,
                p_reserva=p_reserva, p_efectiva_linea=p_efectiva_en_linea,
                p_indisponible_total=p_indisponible_total, p_disponible_total=p_disponible_total,
                timestamp=str(timestamp))

    if (p_efectiva_en_linea >= p_efectiva or p_efectiva_en_linea < p_efectiva*0.2 or
        p_reserva >= p_disponible_total or p_reserva <= 0 or p_disponible_linea > p_efectiva or
        p_indisponible_linea > p_disponible_total) and n_times < 5:
        reserva_de_generacion(timestamp, n_times + 1)
    tmp.save_dict_in_cal_db(collection_name, cal_id, resp)
    return resp


def tendencia_reserva_de_generacion(ini_date=None, end_date=None, freq=None):
    if ini_date is None:
        ini_date = dt.date.today()
    if end_date is None:
        end_date = dt.date.today() + dt.timedelta(days=1)
    if freq is None:
        freq = "30T"

    resp = list()
    date_range = pd.date_range(start=ini_date, end=end_date, freq=freq)
    aux = reserva_de_generacion(date_range[0])
    resp.append(aux)
    for d_i in date_range[1:]:
        if d_i <= dt.datetime.now():
            aux = reserva_de_generacion(d_i)
        else:
            aux = aux.copy()
            aux2 = {"timestamp": str(d_i), "p_efectiva": aux["p_efectiva"]}
            for ix in aux.keys():
                aux[ix] = None
            aux.update(aux2)
        resp.append(aux)
    return resp


def detalle_de_indisponibilidad(ini_date=None, end_date=None):
    if ini_date is None:
        ini_date = time_last_30_m()
    if end_date is None:
        end_date = ini_date
    if isinstance(ini_date, str):
        ini_date = convert_str_to_time(ini_date)
    if isinstance(end_date, str):
        end_date = convert_str_to_time(end_date)

    sql_str = " EXEC Sp_EstadoUnidadesVigentes '{0}','{1}' ".format(ini_date, end_date)
    df_indisponibilidad = pd.read_sql(sql_str, con=gop_svr.bosni_conn)
    df_indisponibilidad["FECHA_HORA"] = [str(x) for x in df_indisponibilidad["FECHA_HORA"]]
    df_indisponibilidad["EVENTO_FECHA"] = [str(x) for x in df_indisponibilidad["EVENTO_FECHA"]]
    df_indisponibilidad.set_index("UNIDAD", inplace=True)
    df_indisponibilidad["POT_DISPONIBLE"] = df_indisponibilidad["POT_EFECTIVA"] - df_indisponibilidad[
        "POT_INDISPONIBLE"]

    return df_indisponibilidad.T


def detalle_de_disponibilidad(ini_date=None, end_date=None):
    if ini_date is None:
        ini_date = time_last_30_m()
    if end_date is None:
        end_date = ini_date
    if isinstance(ini_date, str):
        ini_date = convert_str_to_time(ini_date)
    if isinstance(end_date, str):
        end_date = convert_str_to_time(end_date)

    df_indisponibilidad = detalle_de_indisponibilidad(ini_date, end_date)
    time_range = pi_svr.time_range(time_last_30_m(ini_date), time_last_30_m(end_date))
    df_linea = generation_matrix(time_range)
    df_linea.index = df_linea["U_Codigo"]
    mask = df_linea["Potencia"] > 0
    df_linea = df_linea[mask].T

    set_int = set(df_linea.columns).intersection(df_indisponibilidad.columns)
    df_indisponibilidad = df_indisponibilidad.append(df_linea.loc["Potencia"])
    df_indisponibilidad = df_indisponibilidad[list(set_int)]
    df_indisponibilidad.fillna(" ", inplace=True)

    return df_indisponibilidad


def flujo_de_lineas(nivel_voltaje, ini_date=None, end_date=None):
    if ini_date is None:
        ini_date = dt.datetime.now() - dt.timedelta(minutes=15)
    if end_date is None:
        end_date = dt.datetime.now()

    sql_str = "select * from sivo.dbo.vDetalleCircuitos " \
              " WHERE '{0}' between FechaAlta AND isnull(FechaBaja, '{0}')" \
              " AND Voltaje = '{1} kV' " \
              " ORDER BY CodigoLinea".format(ini_date.date(), nivel_voltaje)

    df_detail = pd.read_sql(sql_str, con=gop_svr.conn)
    del df_detail["FechaBaja"]
    df_detail.dropna(axis=0, inplace=True)
    df_detail["CodigoLinea"] = [x.strip() for x in df_detail["CodigoLinea"]]

    df_detail["ID_circuito"] = [df_detail["CodigoLinea"].loc[x] + "_" + df_detail["Circuito"].loc[x]
                                for x in df_detail.index]
    df_detail["CodigoMed"] = [df_detail["CodigoLinea"].loc[x] + "_" + df_detail["Circuito"].loc[x] + "_"
                              + str(df_detail["TipoTag"].loc[x][-1])
                              for x in df_detail.index]

    time_range = pi_svr.time_range(ini_date, end_date)

    # trabajando con los puntos .AV:
    mask_av = (df_detail["IdTipoTAG"] == 15) | (df_detail["IdTipoTAG"] == 17)
    df_values = process_values(df_detail[mask_av], time_range)

    # trabajando con los puntos .AQ:
    mask_aq = (df_detail["IdTipoTAG"] == 16) | (df_detail["IdTipoTAG"] == 18)
    df_quality = process_calidad(df_detail[mask_aq])

    # uniendo valor y calidad de la tag:
    df_values = df_values.join(df_quality["quality"], how='inner')

    df_values["CodigoMed"] = df_values.index
    # Filtrando tags no encontradas:
    mask = ~(df_values["quality"] == "NOT FOUND")
    df_values = df_values[mask]

    codes = set(df_values["ID_circuito"])
    r = [validar_flujo(df_values[df_values["ID_circuito"] == code]) for code in codes]
    r = pd.DataFrame(r)
    r.index = r["CodigoMed"]
    r = pd.merge(r, df_detail[mask_av], on=["CodigoMed", "ID_circuito"])
    r = r.sort_values(by=["Lim_MaxOperacion", "ID_circuito", "Circuito"], ascending=True)
    return r


def datos_cargabilidad_lineas(nivel_voltaje, ini_date=None, end_date=None):
    if ini_date is None:
        ini_date = dt.datetime.now() - dt.timedelta(minutes=15)
    if end_date is None:
        end_date = dt.datetime.now()

    df = flujo_de_lineas(nivel_voltaje, ini_date, end_date)
    df = df.replace({np.nan: None})
    resp = [preparar_dict(df.loc[ix]) for ix in df.index]
    resp = [x for y in resp for x in y]

    return dict(data=resp, settings=dict(max=df["Lim_Termico"].max(), min=df["Lim_Termico"].min()))


def preparar_dict(serie):
    serie = serie.copy()
    select = ['count', 'mean', 'std', 'min', 'per_25', 'per_50', 'per_75', 'max',
              'timestamp', 'current_value', 'quality',
              'dif', 'Linea', 'Voltaje', 'Lim_MaxOperacion', 'Lim_OperacionContinuo',
              'Lim_Termico', 'TAG']
    serie['timestamp'] = str(serie['timestamp'])
    s_destino = serie['NombreSubDestino']
    s_origen = serie['NombreSubOrigen']
    circuito = serie['ID_circuito']
    if s_destino > s_origen:
        code_1 = s_origen + "#" + s_destino + "--" + circuito
        code_2 = s_destino + "#" + s_origen + "--" + circuito
    else:
        code_1 = s_destino + "#" + s_origen + "--" + circuito
        code_2 = s_origen + "#" + s_destino + "--" + circuito
    value = serie[select].to_dict()

    resp = [dict(name=code_1, value=value, imports=[code_2]), dict(name=code_2, value=value, imports=[])]
    return resp


def process_values(df_work, time_range):
    df_result = pd.DataFrame()

    columns = ['count', 'mean', 'std', 'min', 'per_25', 'per_50', 'per_75', 'max', "timestamp", "current_value",
               "ID_circuito"]

    for ix in df_work.index:
        pi_point = osi.PI_point(pi_svr, df_work["TAG"].loc[ix])
        if pi_point.pt is not None:
            df_values = pi_point.recorded_values(time_range)
            snapshot = pi_point.snapshot()
            describe = df_values.describe().T
            describe.index = [df_work["CodigoMed"].loc[ix]]
            describe["timestamp"] = snapshot.Timestamp
            try:
                describe["current_value"] = float(snapshot.Value)
            except Exception as e:
                print("[{0}]: ".format(pi_point.pt) + str(e))
                describe["current_value"] = None
        else:
            describe = pd.DataFrame(columns=columns, index=[df_work["CodigoMed"].loc[ix]])
            describe["timestamp"] = dt.datetime.now()
            describe["current_value"] = np.NAN

        describe["ID_circuito"] = df_work["ID_circuito"].loc[ix]
        describe.columns = columns
        df_result = df_result.append(describe)

    return df_result


def process_calidad(df_work):
    df_result = pd.DataFrame()

    columns = ["quality"]
    for ix in df_work.index:
        pi_point = osi.PI_point(pi_svr, df_work["TAG"].loc[ix])
        if pi_point.pt is not None:
            snapshot = pi_point.snapshot()
            describe = pd.DataFrame(index=[df_work["CodigoMed"].loc[ix]], columns=columns)
            describe["quality"] = str(snapshot.Value)
        else:
            describe = pd.DataFrame(index=[df_work["CodigoMed"].loc[ix]], columns=columns)
            describe["quality"] = "NOT FOUND"

        df_result = df_result.append(describe)

    return df_result


def validar_flujo(df_to):
    df_to = df_to.copy()
    try:
        df_to = df_to.sort_values(by="timestamp")
        df_to["dif"] = abs(df_to["current_value"].iloc[0] - df_to["current_value"].iloc[-1])
    except Exception as e:
        print(e)
        df_to["dif"] = 0

    # si las mediciones se enuentran en estado normal:
    if ("Normal" in df_to["quality"].iloc[0] or "AL" in df_to["quality"].iloc[0]) and \
            ("Normal" in df_to["quality"].iloc[-1] or "AL" in df_to["quality"].iloc[-1]):
        resp = df_to.max()
        resp.loc["current_value"] = df_to["current_value"].iloc[-1]
        return resp

    # si ambas mediciones se encuentran en error de telemetría:
    if "TE" in df_to["quality"].iloc[0] and "TE" in df_to["quality"].iloc[-1]:
        resp = df_to.max()
        resp.loc["current_value"] = df_to["current_value"].iloc[-1]
        resp.loc["quality"] = "TE"
        return resp

    # si ambas mediciones se encuentran en ingreso manual:
    if "TE" in df_to["quality"].iloc[0] and "TE" in df_to["quality"].iloc[-1]:
        resp = df_to.max()
        resp.loc["current_value"] = df_to["current_value"].iloc[-1]
        resp.loc["quality"] = "ME"
        return resp

    # Buscando una medición que este correcta: en primer caso
    if "Normal" in df_to["quality"].iloc[0] or "AL" in df_to["quality"].iloc[0]:
        resp = df_to.iloc[0]
        return resp

    # Buscando una medición que este correcta: en segundo caso
    if "Normal" in df_to["quality"].iloc[-1] or "AL" in df_to["quality"].iloc[-1]:
        resp = df_to.iloc[-1]
        return resp

    return df_to.max()


def potencia_efectiva_sni(timestamp=None):
    if timestamp is None:
        timestamp = timestamp_now()

    sql_str = "exec sivo.dbo.PotenciasEfectivasSNI '{0}'".format(timestamp)
    df_detail = pd.read_sql(sql_str, gop_svr.conn)
    df_detail["FechaAlta"] = [str(x) for x in df_detail["FechaAlta"]]
    df_detail["FechaBaja"] = [str(x) for x in df_detail["FechaBaja"]]
    df_detail["FechaInicioOpComercial"] = [str(x) for x in df_detail["FechaInicioOpComercial"]]
    return df_detail


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
    dt_now = datetime.datetime.now()
    return dt_now.strftime("%Y-%m-%d %H:%M:%S")


def time_last_30_m(fecha_evaluada=None):
    if fecha_evaluada is None:
        dt_eval = datetime.datetime.now()
    else:
        dt_eval = fecha_evaluada
    m = dt_eval.minute
    if m < 30:
        dt_eval = dt_eval.replace(minute=0)
    if m > 30:
        dt_eval = dt_eval.replace(minute=30)
    dt_eval = dt_eval.replace(second=0, microsecond=0)

    return dt_eval


def tiempo_de_corte(corte_minutos, fecha_evaluada=None):
    if fecha_evaluada is None:
        dt_now = datetime.datetime.now()

    else:
        dt_now = fecha_evaluada

    m, acc_m = dt_now.minute, 0
    dt_now = dt_now.replace(second=0, microsecond=0)
    if m < corte_minutos:
        dt_now = dt_now.replace(minute=corte_minutos)
    else:
        dt_now = dt_now.replace(minute=0)
        for i in range(60):
            dt_now += datetime.timedelta(minutes=corte_minutos)
            acc_m += corte_minutos
            if m < acc_m:
                break
    return dt_now


def convert_str_to_time(str_time, ls_format=None):
    if ls_format is None:
        ls_format = ["%Y-%m-%d", "%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S"]
    dt_resp = dt.datetime.now()
    for fmt in ls_format:
        try:
            dt_resp = dt.datetime.strptime(str_time, fmt)
            break
        except ValueError:
            pass
    return dt_resp


def consultar_for():
    for_path = r"\\qcitbfwnas01\SAO\Varios\plantilla_FOR.xlsx"
    # t = datetime.datetime.now()

    skip_rows = 0
    result = dict()
    try:
        xl = pd.ExcelFile(for_path)
        sheet_ls = xl.sheet_names
        for sheet in sheet_ls:
            df_for = xl.parse(sheet, skiprows=skip_rows)
            cols = [x for x in df_for.columns if "Unnamed" not in x]
            df_for = df_for[cols]
            df_for.fillna(method='ffill', inplace=True)
            df_for.sort_values(by=["Voltaje", "FOR"], inplace=True, ascending=False)
            df_for.reset_index(inplace=True)
            result[sheet] = df_for.to_dict(orient="index")
    except Exception as e:
        print(e)
        return dict(error="El archivo " + for_path + "no fue encontrado")
    return result


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
    # tag = obtener_tag_name_por_descripcion("Demanda Nacional")
    # tendencia_demanda_por_provincia("Pichincha", pi_svr.time_range("2018-10-09", "2018-10-10"))
    # generacion_por_provincia("Pichincha")
    # informacion_sankey_generacion_demanda_por_provincia("Azuay")
    # demanda_empresas()

    pass


if __name__ == "__main__":
    perform_test = True
    if perform_test:
        test()
