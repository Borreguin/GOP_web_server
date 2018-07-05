""" coding: utf-8
Created by rsanchez on 18/06/2018
Este proyecto ha sido desarrollado en la Gerencia de Operaciones de CENACE
Mateo633
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
from my_lib.hmm import hmm_util as hmm_u
import datetime as dt
import pandas as pd
import os
script_path = os.path.dirname(os.path.abspath(__file__))

month_list = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
              "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

years = ['2014', '2015', '2016', '2017', '2018', '2019', '2020']
web_page = 'http://www.feriadosecuador.net/feriado/'
file_name = "fechas_feriados_ecuador.json"


def main():
    holiday_dataset = list()
    # obtener los días feriados desde la web_page
    for y in years:
        url_to_open = web_page + y
        holiday_dataset += get_holiday_from_page(url_to_open)
    # guardar archivo json
    path_file = script_path + '\\' + file_name
    hmm_u.save_json_file(holiday_dataset, path_file)
    df = pd.DataFrame(holiday_dataset)
    df.to_excel(path_file.replace(".json", ".xlsx"))
    print("Los días feriados han sido guardados...")

def get_holiday_from_page(quote_page):
    # specify # specify the url
    # quote_page = 'http://www.feriadosecuador.net/feriado/2015'

    # query the website and return the html to the variable ‘page’
    page = urlopen(quote_page)
    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(page, 'html.parser')
    # Get content from div class fer_caja1
    boxes = soup.findAll("div", {"class": "fer_caja1"})
    result = list()

    for box in boxes:
        box_dict = dict()
        for c in box.contents:
            if c == "\n":
                continue
            cls = c.attrs['class'][0]
            value = c.text.replace("«","")
            value = value.replace("»", "")
            value = value.replace("\t", "")
            if cls != 'fer_dias_cont':
                value = value.replace("\n", "")
            else:
                value = value.replace("\n", "#")
            box_dict[cls] = value.strip()

        box_dict['type'] = box_dict.pop('fer_tip')
        box_dict['name'] = box_dict.pop('fer_tit')
        box_dict['description'] = box_dict.pop('fer_lit')
        box_dict['month'] = box_dict.pop('fer_mes')
        box_dict['year'] = box_dict.pop('fer_anio')
        fer_dias_cont = box_dict['fer_dias_cont']
        box_dict.pop('fer_dias_cont')

        for d in fer_dias_cont.split("#"):
            if not d.isdigit():
                continue

            month = month_list.index(box_dict['month'])
            year = box_dict['year']
            date_f = dt.datetime(int(year), int(month), int(d))
            box_dict['date'] = date_f.strftime("%Y-%m-%d")
            box_dict['day'] = d
            box_dict['day_name'] = date_f.strftime("%A")
            result.append(box_dict.copy())

    return result


def get_holiday_dates_as_df(verbose=True):
    if verbose:
        print("Read holidays from: " + script_path)
    path_file = script_path + '\\' + file_name.replace(".json",".xlsx")
    df = pd.read_excel(path_file)
    return df


def get_holidays_dates():
    df_holiday = get_holiday_dates_as_df(False)
    return pd.to_datetime(df_holiday["date"])


if __name__ == "__main__":
    main()
    holiday_dates = get_holiday_dates_as_df()
