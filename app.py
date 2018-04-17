from flask import Flask, flash, redirect, render_template, request, session, abort
import json
import pandas as pd

# default code
app = Flask(__name__)


@app.route('/')
def hello_world():
    """ This is the MAIN PAGE of this Server Application"""
    return 'Hello World!'


@app.route("/test/<string:name>/")
def test(name):
    """ This is a testing path """
    return render_template('test.html', name=name)


""" Include new pages below this """


@app.route("/map")
def create_map():
    map_data = json.load(open('./static/app_data/maps/ecuador_xy.json'))
    paths = map_data["paths"]
    maxX, minX, maxY, minY = 0, 1000, 0, 1000
    for p in paths:
        m = paths[p]["xy"]
        df_aux = pd.DataFrame(m)
        df_aux.dropna(inplace=True)
        try:
            xmax_df, ymax_df = df_aux.max()
            xmin_df, ymin_df = df_aux.min()

            if xmax_df > maxX:
                maxX = xmax_df
            if ymax_df > maxY:
                maxY = ymax_df

            if xmin_df < minX:
                minX = xmin_df
            if ymin_df < minY:
                minY = ymin_df

            paths[p]['minX'] = xmin_df
            paths[p]['minY'] = ymin_df
            paths[p]['maxX'] = xmax_df
            paths[p]['maxY'] = ymax_df

        except:
            print(p)

    print(minX,maxX,minY,maxY)
    map_data["paths"] = paths
    #with open("final.json", 'w') as to_save:
    #    json.dump(map_data, to_save)
    df_config = pd.read_excel('./static/app_data/maps/empr_electricas_por_provincia.xlsx')
    to_send = df_config.set_index('id').to_dict('index')
    return render_template('Ecuador_Map.html', map_data=map_data, map_config=to_send)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=80)
