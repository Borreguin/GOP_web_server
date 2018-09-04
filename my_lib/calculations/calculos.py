""" coding: utf-8
Created by rsanchez on 07/05/2018
Este proyecto ha sido desarrollado en la Gerencia de Operaciones de CENACE
Mateo633
"""
import datetime
import os
from my_lib.GOP_connection import GOPserver as op
from my_lib.PI_connection import pi_connect as osi
from my_lib.temporal_files_manager import temporal_manager as tmp
import datetime as dt
import pandas as pd

gop_svr = op.GOPserver()
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
gas_natural_list = ['Turbo Gas']                           # El tipo de combustible permite realizar el filtro correcto
no_convencional_list = ['Biomasa', 'Eólica', 'Fotovoltaica', 'Bio Gas']
hidraulica_list = ['Embalse', 'Pasada']

system_path_file = "F:\DATO\Estad\System SIVO\SYSTEM yyyy.xlsx"


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
        mask = df_gen["Tecnología"]=="Fotovoltaica"
        if len(df_gen[mask]) > 0:
            df_gen[mask].drop(inplace=True)
        tag_total_fotovoltaica = obtener_tag_name_por_descripcion("Generación Fotovoltaica")
        df_values = tag_total_fotovoltaica.interpolated(time_range, span_30)
        tag_name = tag_total_fotovoltaica.tag_name
        for idx in set(df_values.index):
            df_aux = pd.DataFrame(["Fotovoltaica", "Total", "Fotovoltaica", tag_name, df_values.at[idx, tag_name], idx],
                          index=["Central", "Unidad", "Tecnología", "TAG", "Potencia", "Fecha"])
            df_gen = df_gen.append(df_aux.T, ignore_index=True)

    df_gen["Fecha"] = [f._repr_base for f in df_gen["Fecha"]]
    df_gen["unique"] = df_gen["Central"] + "_" + df_gen["Unidad"] + "_" + df_gen["Fecha"]
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
    df_r.at["Calidad de servicio", "value"] = total - \
                                              df_r["value"].loc["Gas natural"] - \
                                              df_r["value"].loc["No convencional"]
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
    df_trend = df_matrix[mask].groupby("Fecha").sum()
    df_trend.columns = [technology[0]]

    # others
    for tech in technology[1:]:
        mask = (df_matrix["Tecnología"] == tech)
        df_trend[tech] = df_matrix[mask].groupby("Fecha").sum()

    return df_trend


def trend_hydro_and_others_today():
    df_by_tech = generation_trend_today_by_tech()
    df_by_tech.index = pd.to_datetime(df_by_tech.index)
    dt = datetime.datetime.today()
    dt_today = dt.strftime("%Y-%m-%d")
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
    :param delta:     span en formato string: 10m
    :return:
    """

    if ini_date is None and fin_date is None:
        time_range = pi_svr.time_range_for_today_all_day
    else:
        time_range = pi_svr.time_range(ini_date, fin_date)

    df_gen = generation_matrix(time_range)
    df_gen = df_gen[df_gen["Potencia"]> 0]
    df_gen = df_gen[["Potencia", "Fecha"]].groupby("Fecha").sum()
    df_importacion = intercambio_programado_importacion(time_range)
    df_exportacion = intercambio_programado_exportacion(time_range)
    df_result = pd.DataFrame(index=df_gen.index, columns=["Demanda nacional"])

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

    config_path_file = script_path.replace('\my_lib\calculations',
                                           '\static\\app_data\maps\empr_electricas_por_provincia.xlsx')
    df_config = pd.read_excel(config_path_file, sheet_name='demanda_empresas')

    year = dt.datetime.now().year
    sql_str = 'SELECT t.Nom_UNegocio, t.Fecha, PotMax MW FROM SIVO.dbo.TMP_System_Dem t ' + \
              'where YEAR(t.Fecha) = {0}'
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
        df_result.at[empresa, "current_value"] = int(pt.interpolated_value(time))
        df_result.at[empresa, "max_value"] = int(df_max[empresa].max())

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
        print("[{0}] [obtener_tag_name_por_descripcion] no encontró la siguiente tag: {1}".format(script_path, descripcion))
        return None
    tag_name = df_tag["TAGPI_CODIGO"].iloc[0]
    try:
        pt = osi.PI_point(pi_svr, tag_name)
        return pt
    except Exception as e:
        print(e)


def informacion_sankey_generacion_demanda(timestamp=None):
    import math as mt
    if timestamp is None:
        timestamp = time_last_30_m()

    details = ['Hidroeléctrica', 'Termoeléctrica', 'No convencional']
    df_result = pd.DataFrame(columns=["source", "target", "value", "timestamp"])
    idx = 0
    for detail in details:

        df_gen = detalle_generacion_potencia(detail, timestamp)
        df_gen = df_gen.groupby("Central").sum()
        # tag_list = list(df_gen["TAG"])
        # df_aux = pi_svr.snapshot_of_tag_list(tag_list, timestamp).T
        if df_gen["Potencia"].sum() > 0:
            df_result.at[idx, "source"] = detail
            df_result.at[idx, "value"] = mt.ceil(df_gen["Potencia"].sum())
            idx += 1

    # considerar importacion:
    time_range = pi_svr.time_range(str(timestamp), str(timestamp))
    imp_value = intercambio_programado_importacion(time_range)
    imp_value = imp_value["Importación"].iloc[-1]

    if imp_value >= 0.5:
        produccion_mw = mt.ceil(df_result["value"].sum() + imp_value)
    else:
        produccion_mw = mt.ceil(df_result["value"].sum())

    df_result["target"] = "Producción"

    # considerar exportación:
    exp_value = intercambio_programado_exportacion(time_range)
    exp_value = exp_value["Exportación"].iloc[-1]

    if exp_value >=0.5:
        demanda_nacional_mw = mt.ceil(produccion_mw - exp_value)
    else:
        demanda_nacional_mw = produccion_mw

    df_result.at[idx, "source"] = "Producción"
    df_result.at[idx, "target"] = "Demanda Nacional"
    df_result.at[idx, "value"] = demanda_nacional_mw

    idx += 1
    if imp_value >= 0.5:
        df_result.at[idx, "source"] = "Importación"
        df_result.at[idx, "target"] = "Producción"
        df_result.at[idx, "value"] = mt.ceil(imp_value)

    idx += 1
    if exp_value >= 0.5:
        df_result.at[idx, "source"] = "Producción"
        df_result.at[idx, "target"] = "Exportación"
        df_result.at[idx, "value"] = mt.ceil(exp_value)

    df_result["timestamp"] = str(timestamp)

    return df_result.T




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

"""
    result = 0
    if len(df.index) > 3:
        result = df.iloc[1:-1].sum() * dx + (df.iloc[0] + df.iloc[-1]) * (dx/2)
    else:
        result = df.sum() * dx
"""


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
