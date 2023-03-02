import pandas as pd
import os

DataPath = "C:\inetpub\wwwroot\Gop_WebServer_production\hmm_application\data"
fileName = "Bornes_P_Total.pkl"
df_t = pd.read_pickle(os.path.join(DataPath, fileName))
df_t = df_t[~df_t.index.duplicated(keep="first")]
df_t.columns = [x[1] for x in df_t.columns]
id = [x*2 for x in range(int(len(df_t.columns)/2))]
df_f = df_t.iloc[:, id]
df_r = pd.DataFrame(index=df_f.index, columns=range(len(id)*2))
for ix in range(len(df_f.index)-1):
    sd = list(df_f.iloc[ix]) + list(df_f.iloc[ix+1])
    df_r.loc[df_f.index[ix]] = sd

df_r.dropna(inplace=True)
df_r.to_pickle(os.path.join(DataPath, "2_" + fileName))