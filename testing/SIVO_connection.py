
import pymssql
import pandas as pd

def connection_test():
    conn = pymssql.connect(server="DOP-WKSTAADO", user="sivo", password="sivoer", port=1433)
    sql_statement = "SELECT * FROM CFG_Pais"
    df_prueba = pd.read_sql(sql_statement, conn)
    print(df_prueba.head(5))

if __name__ == '__main__':
    connection_test()