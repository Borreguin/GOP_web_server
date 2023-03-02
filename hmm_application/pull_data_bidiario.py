import os
import pandas as pd
import sys
sys.path.append('../../')
from my_lib.hmm import hmm_util as hmm_u
from my_lib.GOP_connection import GOPserver as gop
import datetime
import numpy as np

# Progress bar
from tqdm import tqdm

script_path = os.path.dirname(os.path.abspath(__file__))
data_path = script_path + "\\data\\"
gop_sv = gop.GOPserver()
dt_1d = datetime.timedelta(days=1)
dt_23h = datetime.timedelta(hours=23)

def run_process():
    df_config = pd.read_excel(script_path + "\\config.xlsx")
    df_config.dropna(inplace=True)
    for ix in df_config.index:
        sql_str = df_config["historic"].loc[ix]
        sql_file = df_config["model_name"].loc[ix].replace("hmm_1", "2")
        run_pull(sql_str, sql_file)
    return True


def run_pull(sql_str, sql_file):

    n_parts = 100
    dt_now = datetime.datetime.now()
    d = pd.date_range("2014-01-01", dt_now)
    # d = pd.date_range("2018-11-01", dt_now)
    sp_time_range = np.array_split(d, n_parts)
    file_path = data_path + sql_file

    if not os.path.exists(file_path):
        df_t = pull_data(sql_str, sp_time_range)
    else:
        df_t = pd.read_pickle(file_path)
        d = pd.date_range(df_t.index[-1], dt_now)
        sp_new = np.array_split(d, n_parts + 1)
        df_n = pull_data(sql_str, sp_new)
        df_t = df_t.append(df_n)

    print("[{0: <30s}] Pulling data from {1} to {2} ".format(sql_file, df_t.index[0], df_t.index[-1]))
    df_t.dropna(inplace=True)
    df_t = df_t[~df_t.index.duplicated(keep="first")]
    df_t.to_pickle(file_path)
    return True


def pull_data(sql_str, sp_time_range):
    sp_time_range = [x for x in sp_time_range if not x.empty]
    df_t = pd.DataFrame(columns=range(0, 48))
    for sp in tqdm(sp_time_range, desc="Pulling process", ncols=100):
        for i_sp in sp:
            sql = sql_str.format(i_sp, i_sp + dt_1d)
            t_fin = i_sp + dt_1d + dt_23h
            t_range = pd.date_range(i_sp, t_fin, freq="60T")
            # print(sql, len(t_range))
            df = pd.read_sql(sql, gop_sv.conn)
            df["timestamp"] = df["Fecha"] + " " + df["Hora"]
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df.index = df["timestamp"]
            df = df[df.index.isin(t_range)]
            df = df.groupby(df.index).sum()
            try:
                df.sort_index(inplace=True)
                df_aux = pd.DataFrame(data=df.T.values, index=[i_sp], columns=range(0, 48))
                # print(df.info())
                # df = hmm_u.pivot_DF_using_dates_and_hours(df)
                df_t = df_t.append(df_aux)
            except Exception as e:
                print("\n" + str(i_sp) + "\n" + str(e))
                continue
    return df_t


if __name__ == "__main__":
    run_process()
