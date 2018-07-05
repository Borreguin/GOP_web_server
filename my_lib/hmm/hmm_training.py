# This is an excellent example of scatter
# could lead in memory problems due the big size of the dataSet
import os
import ipyparallel as ipp
import time
import pandas as pd
from my_lib.hmm import hmm_util as hmm_u
import warnings

DataPath = "./data/"
ModelPath = "./model/"
LogPath = "./log/"
n_comp_min = 35
n_comp_max = 60
n_interaction = 5
n_col_p = 24    # allow pivot if the number of columns is less than 'n_col_p'

def d_time(time_reference):
    return time.time() - time_reference


def get_ipp_client(profile='default'):
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    rc = None
    try:
        rc = ipp.Client(profile=profile)
        print("Engines running for this client: {0}".format(rc.ids))
    except OSError or TimeoutError:
        print("Make sure you are running engines. Example of the command: \n $ipcluster start --profile=default -n 4")
    return rc


def main():
    tr = time.time()
    rc = get_ipp_client()
    dview = rc[:]
    print('[{0:4.2f}] Parallel client connected:\n'.format(d_time(tr)))

    data_set_file_names = os.listdir(DataPath)
    data_set_file_names = [x for x in data_set_file_names if ".pkl" in x]
    # print(dataSetFileNames)

    """ ________________________________________________________
        Setting engines:  
            Set CWD space to work
            Scatter and push variable to work with
    """
    v = rc.load_balanced_view()
    v.block = True
    v.map(os.chdir, [os.getcwd()] * len(v))
    """ os.getcwd(): Get the current CWD, ex: 'C:\\Repositorios\\parallel_programing' 
        os.chdir() : Set the current CWD """

    """  Scattering the list of nComponents in current engines """
    dview.scatter('var_list_nComp', list(range(n_comp_min, n_comp_max + 1)))
    """  make sure that all process contains a scattered list of nComp """
    make_sure = dview.pull('var_list_nComp').get()  # important
    print("[{0:4.2f}] Going to train with nComponents in each engine: \n{1} \n".format(d_time(tr), make_sure))

    """ __________________________________________________________
        START: Defining the parallel function for training process 
    """

    @v.parallel(block=True)
    def hmm_model_training(idp):
        """
            :return the best model that was found in the training process using:
            idp, identify the interaction that is running (if is needed)
            @var_var_dataSet:       is a numpy array of shape (m x n) m features, n samples
                                    1 samples contains m features
            @var_var_list_nComp:    list of components to test and evaluate
            @var_index:             list of index that defines the evaluating dataset
            Note: To pass values to this function use: push and scatter methods.
        """
        import my_lib.hmm.hmm_util as hmm_u
        import numpy as np

        # Shared variables:
        global var_dataSet  # dview.push({'var_dataSet': dataset})
        global var_list_nComp  # dview.scatter('var_list_nComp', list(range(n_comp_min,n_comp_max+1)))
        global var_index  # dview.scatter('var_index', list(len(df.index)))

        """ Taking a slide of the hole data set for validating purposes """
        validating_set = var_dataSet[var_index]
        """ Taking the rest of the dataSet for training purposes """
        ini, end = var_index[0], var_index[-1]
        training_set = np.concatenate((var_dataSet[0:ini], var_dataSet[end:-1]))

        """ Training a list of best models """
        best_model, log_register = hmm_u.select_best_HMM(training_set, validating_set, var_list_nComp, seed=idp)

        """ Send the best model and a register/log of the training process """
        return {'model': best_model, "log_register": log_register}
        # return len(var_dataSet)

    """ ________________________________________________________
        END: Defining the parallel function for training process 
    """

    for fileName in data_set_file_names:

        """ Reading and preparing dataset from DataPath"""
        df = pd.read_pickle(DataPath + fileName)
        # allow pivot if the number of columns is less than 'n_col_p'
        if len(df.columns) < n_col_p:
            # transform dataset in format: [[sample1], [sample2],... , [sampleN]]
            df = hmm_u.pivot_DF_using_dates_and_hours(df)
        # df = df.head(100) #only 100 samples
        dataSet = df.values

        if len(dataSet) == 0:
            print("Check information for {0}".format(fileName))
            continue

        print("[{0:4.2f}] Training a HMM model for: \t\t{1}".format(d_time(tr), fileName))
        tc = time.time()  # measuring training process
        """ Setting engines for the training process"""
        # push df.values in all engines to start training process:
        dview.push({'var_dataSet': dataSet})
        # scattering indexes for validating purposes:
        dview.scatter('var_index', list(range(len(df.index))))
        dview.gather('var_index').get()  # make sure "var_index" is in engines.
        dview.pull('var_dataSet').get()

        """ Run the training process: (n_interaction) times in parallel fashion: """
        best_model_list = hmm_model_training(range(n_interaction * len(v) + 1))
        # print(best_model_list)
        final_model, log_register = hmm_u.select_best_model_from_list(best_model_list, dataSet)

        """ Ordering the best model according to a Hierarchical Clustering """
        ordered_model = hmm_u.ordered_hmm_model(final_model, method='average', metric='euclidean')

        """ Saving the best model and his log_register for posterior analysis """
        print("[{0:4.2f}] Select from final list ({2}) in: \t{1:4.2f}".format(d_time(tr), d_time(tc),
                                                                              len(best_model_list)))
        hmm_u.save_model_and_log(ordered_model, log_register, ModelPath, LogPath, 'hmm_' + fileName)
        print("[{0:4.2f}] End training process in: \t\t{1:4.2f}\n ".format(d_time(tr), d_time(tc)))

    print('[{0:4.2f}] End of script '.format(d_time(tr)))


if __name__ == "__main__":
    main()

# main()
