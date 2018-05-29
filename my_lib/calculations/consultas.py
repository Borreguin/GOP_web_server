""" coding: utf-8
Created by rsanchez on 17/05/2018
Este proyecto ha sido desarrollado en la Gerencia de Operaciones de CENACE
Mateo633
"""
import datetime

from GOP_connection.GOPserver import GOPserver
from flask import jsonify

sivo = GOPserver()

# Example: /con/import_export_by_time/2017-05-16&2017-05-17&E
def import_export_by_time(date_ini, date_end, type_e="I"):
    df = sivo.import_export_by_time(date_ini, date_end, type_e)
    df.index = [x._repr_base for x in df.index]
    return df.to_dict("index")


def import_energy_today():
    now_d = datetime.datetime.now()
    df = sivo.import_export_by_time("2017-05-16", "2017-05-18", "I")
    df.index = [x._repr_base for x in df.index]
    return df.to_dict("index")