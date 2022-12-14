import argparse
import warnings
from optuna.exceptions import ExperimentalWarning

from ForeTiS.utils import helper_functions
from . import optim_pipeline

if __name__ == '__main__':
    """
    Run file to start the whole procedure:
            Parameter Input 
            Check and prepare data files
            Bayesian optimization for each chosen model
            Evaluation
    """
    warnings.simplefilter(action='ignore', category=FutureWarning)
    warnings.simplefilter(action='ignore', category=ExperimentalWarning)
    # User Input #
    parser = argparse.ArgumentParser()
    # Input Params #
    parser.add_argument("-dd", "--data_dir", type=str, default='docs/source/tutorials/tutorial_data',
                        help="Provide the full path of your data directory.")
    parser.add_argument("-sd", "--save_dir", type=str, default='docs/source/tutorials/tutorial_data',
                        help="Provide the full path of the directory in which you want to save your results. "
                             "Default is same as data_dir.")
    parser.add_argument("-data", "--data", type=str, default='offenloch',
                        help="specify the dataset that you want to use.")
    parser.add_argument("-tc", "--target_column", type=str, default='Viola cornuta_amount',
                        help="specify the target column for the prediction.")
    parser.add_argument("-fs", "--featuresets", type=list, default=['optimize'],
                        help="specify on which featuresets the models should be optimized: Valid arguments are: " +
                             str(helper_functions.get_list_of_featuresets()) +
                             "If optimize, the featuresets will be optimized by optuna.")

    # Data Engineering Params
    parser.add_argument("-wf", "--windowsize_current_statistics", type=int, default=3,
                        help="specify the windowsize for the feature engineering of the current statistics. "
                             "Standard is 3")
    parser.add_argument("-ws", "--windowsize_lagged_statistics", type=int, default=3,
                        help="specify the windowsize for the feature engineering of the lagged statistics. "
                             "Standard is 3")
    parser.add_argument("-sl", "--seasonal_lags", type=list, default=[1],
                        help="specify the seasonal lags to add in the feature engineering for the lagged statistics. "
                             "Standard is [1, 2]")
    parser.add_argument("-ce", "--cyclic_encoding", type=bool, default=True,
                        help="specify whether to do cyclic encoding or not. "
                             "Standard is True")
    parser.add_argument("-im", "--imputation_method", type=str, default='mean',
                        help="Only relevant if imputation is set in dataset_specific_config.ini: "
                             "define the imputation method to use: 'mean' | 'knn' | 'iterative'. "
                             "Standard is 'mean'")
    parser.add_argument("-cn", "--correlation_number", type=int, default=5,
                        help="Only relevant if the amount of a focus product gets predicted: "
                             "define the number of with the focus product correlating products "
                             "which will be add as sales features. "
                             "Standard is 5")
    parser.add_argument("-cm", "--correlation_method", type=str, default='kendall',
                        help="Only relevant if the amount of a focus product gets predicted: 'kendall' | 'pearson' | "
                             "'spearman'"
                             "define the used method to calculate the correlations. "
                             "Standard is 'kendall'")

    # Preprocess Params #
    parser.add_argument("-split", "--datasplit", type=str, default='timeseries-cv',
                        help="specify the data split method to use: 'timeseries-cv' | 'train-val-test' | 'cv'. "
                             "Standard is timeseries-cv")
    parser.add_argument("-testperc", "--test_set_size_percentage", type=int, default=2021,
                        help="specify the size of the test set in percentage. "
                             "Also 2021 can be passed, then the year 2021 will be used as test set. "
                             "Standard is 2021")
    parser.add_argument("-valperc", "--val_set_size_percentage", type=int, default=20,
                        help="Only relevant for data split method 'train-val-test': "
                             "define the size of the validation set in percentage. "
                             "Standard is 20")
    parser.add_argument("-splits", "--n_splits", type=int, default=3,
                        help="Only relevant for datasplit methods 'timeseries-cv' and 'cv': define the number of "
                             "splits to use for 'timeseries-cv' or 'cv'. "
                             "Standard is 3")

    # Model and Optimization Params #
    parser.add_argument("-mod", "--models", nargs='+', type=list, default=['ard', 'arima', 'arimax', 'averagehistorical', 'averagemoving', 'averageseasonal', 'averageseasonallag', 'bayesridge', 'elasticnet', 'es', 'gpr', 'gprtf', 'lasso', 'lstm', 'lstmbayes', 'mlp', 'mlpbayes', 'ridge', 'xgboost'],  # 'ard', 'arima', 'arimax', 'averagehistorical', 'averagemoving', 'averageseasonal', 'averageseasonallag', 'bayesridge', 'elasticnet', 'es', 'gpr', 'gprtf', 'lasso', 'lstm', 'lstmbayes', 'mlp', 'mlpbayes', 'ridge', 'xgboost'
                        help="specify the models to optimize: 'all' or naming according to source file name. "
                             "Multiple models can be selected by just naming multiple model names, "
                             "e.g. --models mlp xgboost. "
                             "The following are available: " + str(helper_functions.get_list_of_implemented_models()))
    parser.add_argument("-tr", "--n_trials", type=int, default=200,
                        help="specify the number of trials for the Bayesian optimization (optuna).")
    parser.add_argument("-sf", "--save_final_model", type=bool, default=True,
                        help="specify whether to save the final model to hard drive or not "
                             "(caution: some models may use a lot of disk space, "
                             "unfitted models that can be retrained are already saved by default).")
    parser.add_argument("-prc", "--periodical_refit_cycles", type=list, default=['complete', 0, 1, 2, 4, 8],
                        help="specify with which periods periodical refitting will be done. "
                             "0 means no periodical refitting, "
                             "complete means no periodical refitting and the whole train dataset will be used for "
                             "retraining instead of the refit_window specified below. "
                             "Standard is ['complete', 0, 1, 2, 4, 8]")
    parser.add_argument("-rd", "--refit_drops", type=int, default=0,
                        help="specify how many rows of the train dataset get dropped before refitting. "
                             "Standard is 0")
    parser.add_argument("-rw", "--refit_window", type=int, default=5,
                        help="specify how many seasons get used for refitting. "
                             "Standard ist 5")
    parser.add_argument("-iri", "--intermediate_results_interval", type=int, default=None,
                        help="specify the number of trials after which intermediate results will be calculated. "
                             "Standard is None")

    # Only relevant for Neural Networks #
    parser.add_argument("-bs", "--batch_size", type=int, default=None,
                        help="Only relevant for neural networks: define the batch size. If nothing is specified,"
                             "it will be considered as a hyperparameter for optimization.")
    parser.add_argument("-ep", "--n_epochs", type=int, default=100000,
                        help="Only relevant for neural networks: define the number of epochs. If nothing is specified,"
                             "it will be considered as a hyperparameter for optimization.")

    # Only relevant for bayesian Neural Networks #
    parser.add_argument("-nmc", "--num_monte_carlo", type=int, default=None,
                        help="Only relevant for bayesian neural networks: define the number of Monte Carlo samples. "
                             "If nothing is specified, it will be considered as a hyperparameter for optimization.")

    args = vars(parser.parse_args())

    optim_pipeline.run(**args)
