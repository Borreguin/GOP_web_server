""" coding: utf-8
Created by rsanchez on 10/07/2018
Este proyecto ha sido desarrollado en la Gerencia de Operaciones de CENACE
Mateo633
"""

# from plotly import tools  # to do subplots
import plotly.offline as py
import cufflinks as cf
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

init_notebook_mode(connected=False)
cf.set_config_file(offline=True, world_readable=True, theme='ggplot')


def get_stacked_layout():
    return go.Layout(
        xaxis=dict(
            tickcolor="black",
            gridcolor='gray',
            linecolor='gray',
            nticks=24,
            tickangle=270
        ),
        yaxis=dict(
            tickcolor="black",
            gridcolor='gray',
            linecolor='gray'
        ),
        paper_bgcolor="white",
        plot_bgcolor="#f2f2f2",
        margin=go.Margin(
            t=50,
            r=60,
            b=100,
            pad=0
        ),
        legend=dict(
            orientation="h",
            xanchor="center",
            y=1.2,
            x=0.5
        ),
        barmode='stack'

    )


def get_traces_for_gen_hydro_and_others(df_trend):
    names = dict(Hydro="Hidraúlica", Others="Otra generación", Exportation="Exportación",
                 Total="Producción Total", National_demand="Demanda Nacional")

    colors = dict(Hydro="#5897dd", Others="#e7ac14", Exportation="#9803b1",
                  Total="black", National_demand="green")

    width = dict(Hydro=1, Others=1, Exportation=2, Total=3, National_demand=3)

    traces = list()

    for column in ["Hydro", "Others", "Exportation"]:

        trace_i = go.Bar(
            x=df_trend.index,
            y=df_trend[column],
            name=names[column],
            marker=dict(
                color=colors[column]
            )
        )

        traces.append(trace_i)

    for column in ["Total", "National_demand"]:
        trace_i = go.Scatter(
            x=df_trend.index,
            y=df_trend[column],
            mode='lines',
            name=names[column],
            line=dict(
                width=width[column],
                color=colors[column]
            )
        )
        traces.append(trace_i)

    return dict(data=traces, layout=get_stacked_layout())
