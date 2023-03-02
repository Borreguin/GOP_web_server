""""
    Created by Roberto Sánchez A, based on the Master Thesis:
    "A proposed method for unsupervised anomaly detection for a multivariate building dataset "
    University of Bern/Neutchatel/Fribourg - 2017
    Any copy of this code should be notified at rg.sanchez.a@gmail.com
    to avoid intellectual property's problems.

    Not details about this code are included, if you need more information. Please contact the email above.
    "My work is well done to honor God at any time" R Sanchez A.
    Mateo 6:33
"""
import os.path

"""
    Este proyecto ha sido desarrollado en la Gerencia de Operaciones de CENACE
    Mateo633
"""

import datetime
import pickle
import time
import warnings

# import ipyparallel as ipp
import numpy as np
import pandas as pd
import json
from hmmlearn.hmm import GaussianHMM
import joblib

# Función para imprimir con Markdown style:
# from IPython.display import Markdown, display


def h(x):
    return -3 * pow(x, 3) + 2 * pow(x, 2) + 5 * x


def get_ipp_client(profile='default'):
    rc = None
    try:
        # rc = ipp.Client(profile=profile)
        # rc = Client(profile=profile)
        print("Engines running for this client: {0}".format(rc.ids))
    except Exception as e:
        print(e)
        print("Make sure you are running engines by the command: \n $ipcluster start --profile=default -n 4")
    return rc


def pivot_DF_using_dates_and_hours(df):
    df = df[~df.index.duplicated(keep='first')]
    """ Allow to pivot the dataframe using dates and hours"""
    df["hour"] = [x.time() for x in df.index]
    df['date'] = [x._date_repr for x in df.index]
    # transform series in a table for hour and dates
    try:
        df = df.pivot(index='date', columns='hour')
        # df.fillna(method='pad', inplace=True)
        df.dropna(inplace=True)
    except Exception as e:
        print(e)
        print('No possible convertion, in format: index-> date, columns-> hours')
        df = pd.DataFrame()

    return df


def select_best_HMM(training_set, validating_set, nComp_list, seed=777):
    """ client is an instance of ipp.Client:
        df_dataSet is an instance of pd.DataFrame
    """
    best_score, best_log_prob = 0, -np.inf  # best_score in [0 to 1] and best_log_prob > -np.inf
    best_model, log_register_list = None, list()
    np.random.seed(seed)  # different random seed
    for n_component in nComp_list:
        try:
            model = GaussianHMM(n_components=n_component, covariance_type="diag", n_iter=200).fit(training_set)
            assert isinstance(model, GaussianHMM)
            score, log_prob = score_model(validating_set, model)
            log_register_list.append({"n_component": n_component, "score": round(score, 5),
                                      "log_prob": round(log_prob, 1), "val_size": len(validating_set),
                                      "train_size": len(training_set)})

            if score > best_score and log_prob > best_log_prob:
                best_score = score
                best_model = model
                best_log_prob = log_prob
        except:
            return None, None
    # return best_model, score_list, best_log_prob
    return best_model, log_register_list


def score_model(validating_set, model):
    r, n = 0, len(validating_set)

    try:
        score_samples = model.predict_proba(validating_set)
        log_prob = model.score(validating_set)
        for sample_score in score_samples:
            max_prob = max(sample_score)
            r += max_prob

        score = (r / n)
    except:
        return 0, -np.inf

    return score, log_prob


def select_best_model_from_list(best_model_list, validating_set, verbose=True):
    # warnings.warn("deprecated", DeprecationWarning)
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    warnings.filterwarnings("ignore", category=RuntimeWarning)

    best_score, best_log_prob = 0, -np.inf
    best_model, log_register = None, list()
    last_register = list()
    err = 0
    for item_model in best_model_list:
        model = item_model['model']
        if item_model['log_register'] is not None:
            log_register += item_model['log_register']
        if model is not None:
            assert isinstance(model, GaussianHMM)
            score, log_prob = score_model(validating_set, model)
            last_register.append({"n_component": model.n_components, "score": round(score, 5),
                                  "log_prob": round(log_prob, 1), "val_size": len(validating_set)})

            if score > best_score and log_prob > best_log_prob:
                best_score = score
                best_model = model
                best_log_prob = log_prob
        else:
            err += 1
    if verbose:
        # print('Trained models: {0}'.format(last_register))
        try:
            print('\tBest model: \t\t\t\tnComp={0}, score={1:3.4f}, log_prob={2:5.2f}'.format(
                best_model.n_components, best_score, best_log_prob))
        except Exception as e:
            print(e)
            err += 1
        if err > 0:
            print("\tThere is {0} errors related to trained models".format(err))

    return best_model, log_register + last_register


def ordered_hmm_model(model, method='average', metric='euclidean'):
    """
    From a trained model, creates a new model that reorder the means of the model according
    to the hierarchical clustering HC
    :param model:  a trained Hidden Markov Model
    :param method: Available methods: 'average', 'single', 'complete', 'median', 'ward', 'weighted'
    :param metric: Available metrics: 'euclidean', 'minkowski', 'cityblock', 'sqeuclidean'
    :return: A ordered hmm model
    """
    from scipy.cluster.hierarchy import linkage
    import copy
    # from hmmlearn.hmm import GaussianHMM
    ordered_model = copy.deepcopy(model)

    # try:
    # assert isinstance(model,GaussianHMM)

    """ Z_f contains the distance matrix of the means of the model """
    Z_f = linkage(model.means_, method=method, metric=metric)

    """ Create a new order for the means of the model according to the hierarchical clustering """

    n_comp, new_order = model.n_components, list()
    for idx, idy, d, c in Z_f:
        if idx < n_comp:
            new_order.append(int(idx))
        if idy < n_comp:
            new_order.append(int(idy))

    """ Ordering the means and covars according to 'new_order': """
    # The use of model._covars_ is exceptional, usually it should be "model.covars_"

    old_means, old_covars = model.means_, model._covars_
    new_means, new_covars = np.zeros_like(old_means), np.zeros_like(old_covars)
    for idx, re_idx in zip(list(range(n_comp)), new_order):
        new_means[idx] = old_means[re_idx]
        new_covars[idx] = old_covars[re_idx]

    """ Ordering transition matrix B and  start probability \pi """
    old_transmat, new_transmat = model.transmat_, np.zeros_like(model.transmat_)
    n = old_transmat.shape[0]
    for x in list(range(n)):
        for y in list(range(n)):
            new_transmat[y, x] = old_transmat[new_order[y], new_order[x]]

    start_p = np.array([1 / n_comp for i in range(n_comp)])

    """ Setting the new ordered model """
    ordered_model.startprob_ = start_p
    ordered_model.transmat_ = new_transmat
    ordered_model.means_ = new_means
    ordered_model.covars_ = new_covars

    return ordered_model
    # except:
    #    return model


def save_model_and_log(model, log_register, model_path, log_path, file_name):
    file1 = os.path.join(model_path, file_name)
    file2 = os.path.join(log_path, file_name.replace(".pkl", ".json"))

    try:
        joblib.dump(model, filename=file1, compress=3, protocol=2)
        save_json_file(log_register, file2)

    except FileNotFoundError:
        file1 = "./" + file_name
        file2 = "./" + file_name.replace(".pkl", ".json")
        joblib.dump(model, filename=file1, compress=3, protocol=2)
        save_json_file(log_register, file2)

    print('\tBest model saved in: \t\t\t', file1)
    print('\tLog register in: \t\t\t', file2)


def open_pickle_file(file_path):
    b = None
    try:
        with open(file_path, 'rb') as handle:
            b = pickle.load(handle)
    except Exception as e:
        print(e)
    return b


def save_pickle_file(file_path, to_save):
    try:
        with open(file_path, 'wb') as handle:
            pickle.dump(to_save, handle, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as e:
        print(e)


def save_json_file(to_save, file_path):
    try:
        with open(file_path, 'w') as outfile:
            json.dump(to_save, outfile)
    except Exception as e:
        print(e)


def open_json_file(file_path):
    j = None
    try:
        with open(file_path, 'r') as outfile:
            j = json.load(outfile)
    except Exception as e:
        print(e)
    return j


def printmd(string):
    # display(Markdown(string))
    print(string)


def d_time(time_reference):
    return time.time() - time_reference


def time_now():
    return datetime.datetime.now().strftime('%H:%M:%S')


def get_model_dfx_dfy(model_path, data_path, filter_values=True, verbose=True):
    """
    Read a HMM model and the correspondent data to be processed
    :param verbose: print details about this function
    :param filter_values: Exclude undesirable samples
    :param model_path: path of the model
    :param data_path:  path of the data to be processed
    :return: model, df_x (data), df_y (labels)
    """

    """ Reading the HMM model """
    model = joblib.load(model_path)
    n_comp = model.n_components
    n_features = model.n_features

    """ Reading data from """
    df_x = read_dfx_from(data_path, filter_values)
    x = df_x.values

    """ Inferring the hidden states from the observed samples """
    hidden_states = model.predict(x)
    df_y = pd.DataFrame(hidden_states, columns=['hidden_states'])
    df_y.index = df_x.index

    if verbose:
        print("-> Reading the HMM model from: \n\t\t{0}".format(model_path))
        print("\t\tn_comp = {0}, n_features = {1}".format(n_comp, n_features))
        print('-> Reading data from: \n\t\t' + data_path)
        print("\t\t From " + df_x.index[0].strftime("%Y-%m-%d") + " to " + df_x.index[-1].strftime("%Y-%m-%d"))
        print("\t\t Number of samples to observe: ", len(x))
        print("-> Inferring the hidden states from the observed samples: "
              "\n\t\t A sequence of {0} hidden status were inferred".format(len(hidden_states)))

    return model, df_x, df_y


def read_dfx_from(data_path, filter_values=True):
    """Read raw data"""
    df = pd.read_pickle(data_path)
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors= 'coerce')
        df[col] = df[col].interpolate(method='nearest', limit=3, limit_direction='both')

    """Excluding undesirable data"""
    if filter_values:
        try:
            exclude_dates_list = open_json_file(data_path.replace(".pkl", "_exclude.json"))
            mask = ~df.index.isin(exclude_dates_list)
            df = df[mask]
        except Exception as e:
            print(e)
            print("[{0: <21s}] No hay datos a filtrar".format(time_now()))

    """Datetime index"""
    try:
        df.index = pd.to_datetime(df.index)
    except Exception as e:
        print(e)

    if len(df.columns) < 24:
        df = pivot_DF_using_dates_and_hours(df)

    return df


def get_lol_upl(df_x):
    lol = df_x.quantile(0.02)
    lol = np.amin(lol)
    upl = df_x.quantile(0.98)
    upl = np.amax(upl)
    return lol, upl

# def holiday_cluster_matrix():
#    df_holiday = hl.get_holiday_dates_as_df()
#    holiday_dates = df_holiday["date"].values
#    mask = df_x.index.isin(holiday_dates)
#    df_x_holiday = df_x[mask]
#    df_x_holiday.T.iplot()


# Shared memory is most costly instead break down the DataFrame
# mgr = Manager()
# ns = mgr.Namespace()
# ns.df = pd.DataFrame(list(range(1, 500000)))
# ns.dt = dataSet
# to_save = [{"a":5},{"b":6}]
# save_json_file("test.json", to_save)
