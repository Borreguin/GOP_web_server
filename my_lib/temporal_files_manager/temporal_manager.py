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


def retrieve_file(file_name, dt_deltatime):
    file_path = temporal_path() + file_name
    file_path = file_path.replace(":", "_")
    if os.path.exists(file_path) and isinstance(dt_deltatime, dt.timedelta):

        modified_time = dt.datetime.fromtimestamp(os.path.getmtime(file_path))
        available_time = modified_time + dt_deltatime

        if dt.datetime.now() < available_time:
            # Getting back the objects:
            with open(file_path, 'rb') as f:
                resp = pickle.load(f)
            return resp

        else:
            return  None

    else:
        return None


def save_variables(file_name, list_objects):

    file_path = temporal_path() + file_name
    file_path = file_path.replace(":", "_")
    try:
        # Saving the objects:
        with open(file_path, 'wb') as f:
            pickle.dump(list_objects, f)
        return True
    except Exception as e:
        print(e)
        return False


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


