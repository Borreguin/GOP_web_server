""" coding: utf-8
Created by rsanchez on 15/08/2018
Este proyecto ha sido desarrollado en la Gerencia de Operaciones de CENACE
Mateo633
"""
import os
import pickle
import datetime as dt
script_path = os.path.dirname(os.path.abspath(__file__))


def root_path():
    return script_path.replace('my_lib\\temporal_files_manager', "")


def temporal_path():
    return root_path() + 'static\\temp\\'


def retrieve_file(file_name, eval_time=None):
    file_path = temporal_path() + file_name
    file_path = valid_path(file_path)

    if eval_time is None and os.path.exists(file_path):
        # eval_time = dt.datetime.fromtimestamp(os.path.getmtime(file_path))
        eval_time = dt.datetime.now()

    if isinstance(eval_time, dt.timedelta):
        return SyntaxError

    if os.path.exists(file_path) and isinstance(eval_time, dt.datetime):

        with open(file_path, 'rb') as f:
            resp = pickle.load(f)

        list_objects = resp["list_objects"]
        valid_range = resp["valid_range"]

        if valid_range[0] < eval_time < valid_range[1]:
            empty_temp_files(100)
            return list_objects
        else:
            return None

    else:
        return None


def empty_temp_files(limit_number_of_files):
    file_list = os.listdir(temporal_path())
    if limit_number_of_files < len(file_list):
        for f in file_list:
            os.remove(os.path.join(temporal_path(), f))


def save_variables(file_name, list_objects, valid_range=None, dt_delta=None):

    file_path = temporal_path() + file_name
    file_path = valid_path(file_path)
    dt_n = dt.datetime.now()
    if valid_range is None and dt_delta is None:
        valid_range = [dt_n, dt_n + dt.timedelta(minutes=2)]
    elif isinstance(dt_delta, dt.timedelta):
        valid_range = [dt_n, dt_n + dt_delta]

    try:
        # Saving the objects:
        with open(file_path, 'wb') as f:
            to_dump = dict(list_objects=list_objects, valid_range=valid_range)
            pickle.dump(to_dump, f)
        return True
    except Exception as e:
        print(e)
        return False


def valid_path(file_path):
    file_path = file_path[:3] + file_path[3:].replace(":", "_")
    file_path = file_path[:3] + file_path[3:].replace("/", "_")
    return file_path


def test():
    # cálculo disponible por 1 minuto:
    dt_delta = dt.timedelta(minutes=1)
    rt_value = retrieve_file("temporal_manager_test.pkl", dt_delta)
    if rt_value is not None:
        return rt_value

    # recalculate after 1 minute:
    aux_1 = str(dt.datetime.now())
    aux_2 = "value2"
    aux_3 = "value3"

    save_variables("temporal_manager_test.pkl", [aux_1, aux_2, aux_3])

    return aux_1, aux_2, aux_3


if __name__ == "__main__":
    perform_test = True
    if perform_test:
        print(test())


