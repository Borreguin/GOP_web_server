""" coding: utf-8
Created by rsanchez on 07/05/2018
Este proyecto ha sido desarrollado en la Gerencia de Operaciones de CENACE
Mateo633
"""
import datetime
import os
from my_lib.GOP_connection import GOPserver as op
from my_lib.PI_connection import pi_connect as osi
import pandas as pd
gop_svr = op.GOPserver()
pi_svr = osi.PIserver()
script_path = os.path.dirname(os.path.abspath(__file__))
# ______________________________________________________________________________________________________________#
# ________________________________        GENERAL        VARIABLES       _______________________________________

delta_15 = 15                                   # minutes
factor_15 = delta_15 / 60                       # factor for calculating Energy using P each 15 minutes
span_15 = pi_svr.span(str(delta_15) + "m")      # span time of 15 minutes

delta_30 = 30                                   # minutes
factor_30 = delta_30 / 60                       # factor for calculating Energy using P each 15 minutes
span_30 = pi_svr.span(str(delta_15) + "m")      # span time of 15 minutes

technology = ['Embalse', 'Pasada', 'Turbo Vapor', 'Turbo Gas', 'MCI', 'Biomasa',
              'Eólica', 'Fotovoltaica', 'Bio Gas']
# ______________________________________________________________________________________________________________#


def energy_production():
    e_hydro = generation_now('hidraulica')['value']
    e_total = generation_now('total')['value']
    e_otra = e_total - e_hydro
    # e_otra = generation_now('otra generacion')['value']

    result = [{"id": 0, "label": "Hidráulica", "value": str(e_hydro) + " MWh",  "percentage": e_hydro/e_total},
              {"id": 1, "label": "Otra Generación", "value": str(e_otra) + " MWh", "percentage": 1-e_hydro/e_total}]
    return result


def df_tags_exportation():
    sql = "SELECT C.Codigo, C.Nombre, C2.TAG, C2.Descripcion, E.Elemento FROM CFG_Equivalencias E" + \
          " INNER JOIN CFG_Linea L ON E.Equivalencia=L.Codigo" + \
          " INNER JOIN CFG_Circuito C ON L.IdLinea=C.IdLinea " + \
          " INNER JOIN CFG_ElementoTAG M ON C.IdCircuito=M.IdElemento" + \
          " INNER JOIN CFG_TAG C2 on M.IdTAG = C2.IdTAG" + \
          " WHERE C2.TAG LIKE '%P.LINEA%'" \
          + "AND C2.IdTipoTAG IN (1,3,9,10)"    # according to the flows
    return pd.read_sql(sql, gop_svr.conn)


def df_tags_importation():
    sql = "SELECT C.Codigo, C.Nombre, C2.TAG, C2.Descripcion, E.Elemento FROM CFG_Equivalencias E" + \
          " INNER JOIN CFG_Linea L ON E.Equivalencia=L.Codigo" + \
          " INNER JOIN CFG_Circuito C ON L.IdLinea=C.IdLinea " + \
          " INNER JOIN CFG_ElementoTAG M ON C.IdCircuito=M.IdElemento" + \
          " INNER JOIN CFG_TAG C2 on M.IdTAG = C2.IdTAG" + \
          " WHERE C2.TAG LIKE '%P.LINEA%'" \
          + "AND C2.IdTipoTAG IN (5,6,11,12)"     # according to the flows
    return pd.read_sql(sql, gop_svr.conn)


def exportation_energy_now():
    """
        Exportation energy (MWh) from 0:00 until the current moment in an span of (span minutes)
        :return: energy MWh
    """
    time_range = pi_svr.time_range_for_today()
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
    mw_h = df_values[df_values > 0].sum()
    energy = round(integrating_by_average(mw_h, factor_15), 0)
    return {'value': energy, 'tag': 'exportation_energy_now',
            'time_range': str(time_range), 'timestamp': timestamp_now()}


def importation_energy_now():
    """
    Importation energy (MWh) from 0:00 until the current moment in an span of (span minutes)
    :return: energy MWh
    """
    time_range = pi_svr.time_range_for_today()
    df_c = df_tags_importation()
    tags_AV = list(set([x for x in df_c["TAG"] if ".AV" in x]))
    df_values = pi_svr.interpolated_of_tag_list(tags_AV, time_range, span_15)
    mw_h = df_values[df_values > 0].sum()
    energy = round(integrating_by_average(mw_h, factor_15), 0)
    return {'value': energy, 'tag': 'importation_energy_now',
            'time_range': str(time_range), 'timestamp': timestamp_now()}


def generation_matrix(time_range):
    """
    Generation matrix that is stored over BOSNI Database
    :param time_range:  AFTimeRange (PIserver.time_range())
    :return: DataFrame
    """
    initial_date = time_range.StartTime.ToString("yyyy-MM-dd HH:mm:s")
    final_date = time_range.EndTime.ToString("yyyy-MM-dd HH:mm:s")
    sql = "SELECT [Central],[Unidad],[Tecnología]" + \
          ",[TAG],[Potencia],[Fecha]" +\
          " FROM [BOSNI].[dbo].[vHIST_UNIDAD_POT_EFECTIVA]" + \
          " WHERE [Fecha] between " +\
          "'" + initial_date + "' and '" + final_date + "'"

    df_gen = pd.read_sql(sql, gop_svr.conn)
    df_gen["Fecha"] = [f._repr_base for f in df_gen["Fecha"]]
    df_gen["unique"] = df_gen["Central"] + "_" + df_gen["Unidad"] + "_" + df_gen["Fecha"]
    df_gen.drop_duplicates(["unique"], keep='last', inplace=True)
    return df_gen


def generation_energy_by_tech_now():
    """
    Energy values for each kind of technology from 00:00 until the current moment
    :return: dictionary with energy of each kind of technology
    """
    time_range = pi_svr.time_range_for_today()
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
def generation_now(detail="total"):
    """
    Energy of generation in MWh (dictionary with energy values)
    :param detail: options: 'total', 'hidraulica', 'otra generacion',
     'no convencional', 'termoelectrica', 'termoelectrica + interconnexion'
    :return: dictionary with energy values
    """
    subtotal = generation_energy_by_tech_now()
    total = 0

    if detail == 'total':
        for sb in subtotal:
            if sb != "time_range":
                total += subtotal[sb]
        total += importation_energy_now()["value"]

    elif detail == 'hidraulica':
        for sb in ['Embalse', 'Pasada']:
            total += subtotal[sb]

    elif detail == 'otra generacion':
        for sb in subtotal:
            if sb != "time_range":
                total += subtotal[sb]
        total += importation_energy_now()["value"]

        hydro = 0
        for sb in ['Embalse', 'Pasada']:
            hydro += subtotal[sb]
        total -= hydro

    elif detail == 'termoelectrica':
        for sb in ['Turbo Vapor', 'Turbo Gas', 'MCI']:
            total += subtotal[sb]

    elif detail == 'termoelectrica + interconnexion':
        for sb in ['Turbo Vapor', 'Turbo Gas', 'MCI']:
            total += subtotal[sb]
        total += importation_energy_now()["value"]

    elif detail == 'no convencional':
        for sb in ['Biomasa', 'Eólica', 'Fotovoltaica', 'Bio Gas']:
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
    level = int(level)
    if isinstance(list_tech,str):
        list_tech = list_tech.split(",")
    time_range = pi_svr.time_range_for_today()
    return generation_detail(time_range, list_tech, level)


def generation_detail(time_range, list_tech, level=7):
    df_gen = generation_matrix(time_range)
    mask = (df_gen["Tecnología"].isin(list_tech))
    df_gen = df_gen[mask]
    df_gen = df_gen[df_gen["Potencia"] > 0]
    centrals = list(set(df_gen["Central"]))
    df_result = pd.DataFrame(index=centrals, columns=["Potencia"])
    for c in centrals:
        df_x = df_gen[df_gen["Central"] == c]["Potencia"]
        df_result.at[c, "Potencia"] = integrating_by_average(df_x, factor_30)

    df_result.sort_values(by=["Potencia"], ascending=False, inplace=True)
    df_head = df_result.head(level)
    total = generation_now('hidraulica')['value']

    if total == 0:
        print("[{0}] \t [generation_detail] "
              "\t La matrix de generación se encuentra vacía".format(script_path))
        return None

    result = list()
    acc = 0
    for idx, name in enumerate(df_head.index):
        value = df_head["Potencia"].iloc[idx]
        name = name.replace("Central ", "")
        percentage = round(value/total, 4)
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
             "value": str(int((1-acc)*total)) + " MWh",
             "percentage": round(1-acc, 4)
        }
        result.append(r)

    return result


def other_generation_detail_now():

    df_r = pd.DataFrame(
        index=["Gas natural", "No convencional", "Calidad de servicio"],
        columns=["value", "id", "label", "percentage"])
    df_r["label"] = df_r.index
    df_r["id"] = range(len(df_r.index))
    total = generation_now('otra generacion')['value']
    df_r.at["Gas natural", "value"] = generation_now('Turbo Gas')['value']
    df_r.at["No convencional", "value"] = generation_now('no convencional')['value']
    df_r.at["Calidad de servicio", "value"] = total - \
                                               df_r["value"].loc["Gas natural"] - \
                                               df_r["value"].loc["No convencional"]
    df_r["percentage"] = df_r["value"]/ total
    df_r["value"] = [str(x) + " MWh" for x in df_r["value"]]
    return df_r.to_dict("record")


def integrating_by_average(df, dx):
    # integrating using average:
    mean_y = (df[:-1] + df.shift(-1)[:-1]) / 2
    # delta_x = x.shift(-1)[:-1] - x[:-1]
    # scaled_int = mean_y.multiply(delta_x)
    scaled_int = mean_y*dx
    scaled_int.fillna(0, inplace=True)
    return scaled_int.sum()


def timestamp_now():
    dt = datetime.datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")

"""
    result = 0
    if len(df.index) > 3:
        result = df.iloc[1:-1].sum() * dx + (df.iloc[0] + df.iloc[-1]) * (dx/2)
    else:
        result = df.sum() * dx
"""

# def total_generation_now():
# x = cal_exportation_now()
# y = cal_importation_now()
# r = generation_energy_by_tech_now()

# generation_detail_now(['Embalse', 'Pasada'])
other_generation_detail_now()