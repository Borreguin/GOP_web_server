""" coding: utf-8
Created by rsanchez on 17/05/2018
Este proyecto ha sido desarrollado en la Gerencia de Operaciones de CENACE
Mateo633
"""
import datetime

from flask import jsonify
from my_lib.GOP_connection import GOPserver as op
from my_lib.PI_connection import pi_connect as osi
import pandas as pd

gop_svr = op.GOPserver()

# Example: /con/import_export_by_time/2017-05-16&2017-05-17&E
def import_export_by_time(date_ini, date_end, type_e="I"):
    df = gop_svr.import_export_by_time(date_ini, date_end, type_e)
    df.index = [x._repr_base for x in df.index]
    return df.to_dict("index")


def import_energy_today():
    dt = datetime.datetime.now()
    str_td = dt.strftime("%Y-%m-%d")
    dt = dt + datetime.timedelta(days=1)
    str_td2 = dt.strftime("%Y-%m-%d")
    df = gop_svr.import_export_by_time(str_td, str_td2, "I")
    df.index = [x._repr_base for x in df.index]
    return df.to_dict("index")


def get_df_despacho_programado(str_date):
    df_despacho = pd.DataFrame()
    for n_desp in range(9):
        sql = "SELECT t.Fecha, t.Hora, t.Unidad, t.MV, t.EsRedespacho, t.NumRedespacho" + \
              " FROM SIVO.dbo.DPL_DespachoProgramado t" + \
              " where Fecha = '{0}'" + \
              " and NumRedespacho = {1}"
        sql = sql.format(str_date, n_desp)
        df = pd.read_sql(sql, gop_svr.conn)
        if not df.empty:
            df_despacho = df
        else:
            break
    df_despacho = df_despacho[df_despacho["MV"] > 0]
    return df_despacho


def despacho_programado_total_por_hora(str_date):
    df = get_df_despacho_programado(str_date)
    df = df.groupby("Hora")
    df = df.sum()
    print(df)


def test():
    print("start testing module")
    # import_energy_today()
    # import_export_by_time('2017-05-16', '2017-05-17', 'E')
    # import_export_by_time('2017-05-16', '2017-05-16', 'E')
    # get_df_despacho_programado("2018-01-11")
    despacho_programado_total_por_hora("2018-01-11")


if __name__ == "__main__":
    perform_test = True
    if perform_test:
        test()