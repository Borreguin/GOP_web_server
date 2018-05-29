
import pymssql
import pandas as pd
from my_lib.GOP_connection import GOPserver as gop
import matplotlib.pyplot as plt

def connection_test():
    conn = pymssql.connect(server="DOP-WKSTAADO", user="sivo", password="sivoer", port=1433)
    sql_statement = "SELECT * FROM CFG_Pais"
    df_prueba = pd.read_sql(sql_statement, conn)
    print(df_prueba.head(5))

def total_generation():
    gop_sv =  gop.GOPserver()
    print("starting...")
    sql = "SELECT t.Central, t.Unidad, t.MV_Validado, " +\
          "t.Fecha, t.Hora FROM SIVO.dbo.DV_Generacion t "+ \
          "where t.MV_Validado > 0 and t.Fecha between '2014-01-01' and '2018-05-28'"

    df = pd.read_sql(sql,gop_sv.conn)
    print("transforming...")
    df["timestamp"] = df["Fecha"] + " " + df["Hora"]
    del df["Fecha"]
    del df["Hora"]
    df["unique"] = df["Central"] + df["Unidad"] + df["timestamp"]
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    print(len(df.index))
    df.drop_duplicates(subset=["unique"], inplace=True)
    print(len(df.index))
    print("summing...")
    df = df.groupby('timestamp').sum()
    df.sort_index(inplace=True)
    # df.plot()
    # plt.show()
    df.to_pickle('Bornes_P_Total.pkl')
    print("finish")

if __name__ == '__main__':
    # connection_test()
    total_generation()