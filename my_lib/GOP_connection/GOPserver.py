""" coding: utf-8
Created by rsanchez on 17/05/2018
Este proyecto ha sido desarrollado en la Gerencia de Operaciones de CENACE
Mateo633
"""

import pymssql
import pandas as pd
from my_lib.encrypt.library_encrypt import *
import pickle
import os
script_path = os.path.dirname(os.path.abspath(__file__))


class GOPserver:

    def __init__(self, ):
        self.conn = get_conn()

    def import_export_by_time(self, str_ini_date, str_fin_date, type_e="I"):
        """
        returns Importation/Exportation MW and MVAR
        :param str_ini_date: initial date (yyyy-mm-dd)
        :param str_fin_date: final date (yyyy-mm-dd)
        :param type_e: I/E  (Importation/ Exportation)
        :return: DataFrame Importation/Exportation MW and MVAR with validated values
        """
        sql = "SELECT * FROM[dbo].[fn_ImportExport]('" \
              + type_e + "', '" + str_ini_date +\
              "', '" + str_fin_date + "', 0)"
        df_result = pd.read_sql(sql, self.conn)
        df_result.index = pd.to_datetime(df_result["Fecha"] + " " + df_result["Hora"])

        df_r = pd.DataFrame()
        df_r["MV_Validado"] = df_result.groupby(df_result.index)["MV_Validado"].sum()
        df_r["MVAR_Validado"] = df_result.groupby(df_result.index)["MVAR_Validado"].sum()

        return df_r

    def matrix_generation(self, init_date, final_date=None):
        """
        Matrix of generation that is in line:
        :param date: time where we want to see the historic [yyyy-mm-dd hh:mm:ss]
        :return: DataFrame
        """
        if final_date is None:
            final_date = pd.to_datetime(init_date) + pd.to_timedelta("15m")
            final_date = final_date._short_repr

        sql = "SELECT [IdUnidad],[Central],[Unidad],[Tecnología]" + \
              ",[TAG],[Potencia],[Fecha]" + \
              "FROM [BOSNI].[dbo].[vHIST_UNIDAD_POT_EFECTIVA]" + \
              "WHERE Fecha BETWEEN '" + init_date + "' AND '" + final_date + "'"
        df = pd.read_sql(sql, self.conn)
        return df


def get_conn():

    try:
        path = script_path + '\\' + "st.pkl"
        with open(path, 'rb') as pickle_file:
            ps = pickle.load(pickle_file)
    except Exception as e:
        print(e)
        path = "./my_lib/GOP_connection/st.pkl"
        with open(path, 'rb') as pickle_file:
            ps = pickle.load(pickle_file)
    return pymssql.connect(server="QCITBVWBDCL3", user="readuser", password=decrypt(ps), port=1433)
    # return pymssql.connect(server="DOP-WKSTAADO", user="readuser", password=decrypt(ps), port=1433)


def connection_test():
    gop = GOPserver()
    sql_statement = "SELECT * FROM CFG_Pais"
    df_prueba = pd.read_sql(sql_statement, gop.conn)
    df = gop.import_export_by_time("2017-05-02", "2017-07-05", "I")
    # df = gop.matrix_generation("2018-05-17 12:00:00", "2018-05-17 12:15:00")
    # df = gop.matrix_generation("2018-05-17 12:00:00")
    print(df.head(5))
    print("\n Test exitoso")


if __name__ == '__main__':
    perform_test = False
    if perform_test:
        connection_test()