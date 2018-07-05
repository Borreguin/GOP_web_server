import numpy as np
from matplotlib import cm, pyplot as plt, style as st, gridspec as gd
from matplotlib.dates import YearLocator, MonthLocator
import pylab as pl
from IPython.display import display

st.use('seaborn-colorblind')
# use of plotly:
import plotly.offline as py
import plotly.graph_objs as go  #important library for the plotly
py.init_notebook_mode(connected=False) # run at the start of every ipython notebook to use plotly.offline
from plotly import tools #to do subplots


# use of cufflinks:
import cufflinks as cf
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=False)
cf.set_config_file(offline=True, world_readable=True, theme='ggplot')

def set_iCol_and_iRow(iCol, iRow, nrows, ncols):
    iCol += 1
    if iRow >= nrows:
        iRow = 0
    if iCol >= ncols:
        iCol = 0
        iRow += 1
    return iCol, iRow


def plot_profiles_24h(df_x, df_y, states_to_plot, yLim, units, n_col=4, figsize=(16, 24)):
    nrows = int(np.ceil(len(states_to_plot) / n_col))
    n_samples = len(df_x.loc[df_x.index[0]])
    if n_samples == 24:
        labels = range(24)
    elif n_samples > 24:
        fc = n_samples / 24
        labels = [x / fc for x in range(int(fc * n_samples))]
    else:
        labels = range(n_samples)

    id_n = -1
    figures = list()
    for i in range(nrows):
        fig, axes = plt.subplots(nrows=1, ncols=n_col, figsize=figsize)
        medianprops = dict(linewidth=4, color='red')
        for j in range(n_col):
            id_n += 1

            if id_n < len(states_to_plot):
                n = states_to_plot[id_n]
                mask = df_y[df_y['hidden_states'] == n].index
                if (len(mask)) > 0:
                    df_to_plot = df_x.loc[mask]
                    df_to_plot.plot.box(ax=axes[j], notch=False, medianprops=medianprops, showfliers=True)
                    axes[j].set_ylim(yLim)
                    axes[j].set_xlabel('Hours')
                    # axes[-1][j].set_xlabel('Hours')
                    axes[j].set_ylabel('[ ' + units + ' ]')
                    axes[j].set_title('ID_= ' + str(n) + ' #Days=' + str(len(mask)))
                    axes[j].set_xticklabels(labels=labels, rotation=-90)

                for label in axes[j].get_xticklabels()[::2]:
                    label.set_visible(False)
        figures.append(fig)
        plt.tight_layout()
        plt.show()

    return figures
