""" coding: utf-8
Created by rsanchez on 07/05/2018
Este proyecto ha sido desarrollado en la Gerencia de Operaciones de CENACE
Mateo633
"""
import datetime

from my_lib.GOP_connection import GOPserver as op
from my_lib.PI_connection import pi_connect as osi
import pandas as pd
gop_svr = op.GOPserver()
pi_svr = osi.PIserver()

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
    e_hidro = generation_now('hidraulica')['value']
    e_total = generation_now('total')['value']
    e_otra = e_total - e_hidro

    result = [{"label": "Hidráulica", "value": str(e_hidro) + " MWh",  "percentage": e_hidro/e_total},
              {"label": "Otra Generación", "value": str(e_otra) + " MWh", "percentage": 1-e_hidro/e_total}]
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
    # time_range = pi_svr.time_range("2018-05-22", "2018-05-22 07:00:00")
    df_c = df_tags_exportation()
    tags_AV = list(set([x for x in df_c["TAG"] if ".AV" in x]))
    df_values = pi_svr.interpolated_of_tag_list(tags_AV, time_range, span_15)
    mw_h = df_values[df_values > 0].sum()
    energy = round(factor_15*mw_h.sum(), 0)
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
    energy = round(factor_15*mw_h.sum(), 0)
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
    sql = "SELECT [IdUnidad],[Central],[Unidad],[Tecnología]" + \
          ",[TAG],[Potencia],[Fecha]" +\
          " FROM [BOSNI].[dbo].[vHIST_UNIDAD_POT_EFECTIVA]" + \
          " WHERE [Fecha] between " +\
          "'" + initial_date + "' and '" + final_date + "'"
    return pd.read_sql(sql, gop_svr.conn)


def generation_energy_now_by_tech():
    """
    Energy values for each kind of technology
    :return: dictionary with energy of each kind of technology
    """
    time_range = pi_svr.time_range_for_today()
    # time_range = pi_svr.time_range("2018-05-22", "2018-05-22 07:00:00")
    df_gen = generation_matrix(time_range)
    df_gen = df_gen[df_gen["Potencia"] > 0]
    # df_gen.sort_values(by=['Central', 'Unidad'], inplace=True)
    df_gen["Fecha"] = [f._repr_base for f in df_gen["Fecha"]]
    df_gen["unique"] = df_gen["Central"] + "_" + df_gen["Unidad"] + "_" + df_gen["Fecha"]
    df_gen.drop_duplicates(["unique"], keep='last', inplace=True)

    # calculating energy by technology:
    result = {"time_range": str(time_range)}
    for tech in technology:
        mask = (df_gen["Tecnología"] == tech)
        # df_w = df_gen.loc[mask]
        # df_r = df_w.groupby('Central').sum()
        df_c = df_gen.loc[mask].groupby('Fecha')
        df_c = df_c["Potencia"].sum()
        # integrating using average:
        if len(df_c.index) > 3:
            result[tech] = df_c.iloc[1:-1].sum() * factor_30 + (df_c.iloc[0] + df_c.iloc[-1])*factor_15
        else:
            result[tech] = df_c.sum()*factor_30
    return result


# Ex:   /cal/generation_now/otra generacion
#       /cal/generation_now/hidraulica
def generation_now(detail="total"):
    """
    Energy of generation in MWh
    :param detail: options: 'total', 'hidraulica', 'otra generacion', 'no convencional'
    :return: dictionary with energy
    """
    subtotal = generation_energy_now_by_tech()
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
        for sb in ['Turbo Vapor', 'Turbo Gas', 'MCI']:
            total += subtotal[sb]
        total += importation_energy_now()["value"]

    elif detail == 'no convencional':
        for sb in ['Biomasa', 'Eólica', 'Fotovoltaica', 'Bio Gas']:
            total += subtotal[sb]

    total = round(total, 0)
    return {'value': total, 'tag': 'generation_now',
            'time_range': subtotal['time_range'], 'detail': detail,
            'timestamp': timestamp_now()}


def timestamp_now():
    dt = datetime.datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")

# def total_generation_now():
# x = cal_exportation_now()
# y = cal_importation_now()
# r = generation_energy_now_by_tech()


