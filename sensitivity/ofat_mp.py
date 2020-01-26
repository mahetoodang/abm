"""
OFAT Analysis: replace names in problem dictionary with the variable name you are testing.
See below for available parameter names.
"""

import time
import multiprocessing
import numpy as np
import matplotlib.pyplot as plt
from mesa.batchrunner import BatchRunnerMP, BatchRunner
# from SALib.analyze import sobol
# import pandas as pd
import sys
sys.path.append('../')

from functionality.model import Friends


def perform_analysis():
    problem = {
        'num_vars': 1,
        'names': ['tolerance'],  # available parameters: 'tolerance','social_extroversion','mobility','decay'
        'bounds': [[0.01, 0.99]]
    }

    # Set the repetitions, the amount of steps, and the amount of distinct values per variable
    replicates = 10
    max_steps = 10
    distinct_samples = 10

    # Set the outputs
    model_reporters = {"Friends score": lambda m: m.avg_friends_score(),
                       "Friends distance": lambda m: m.avg_friends_social_distance(),
                       "Friends spatial distance": lambda m: m.avg_friends_spatial_distance()}

    data = {}
    begin = time.time()

    for i, var in enumerate(problem['names']):
        # Get the bounds for this variable and get <distinct_samples> samples within this space (uniform)
        samples = np.linspace(*problem['bounds'][i], num=distinct_samples)

        batch = BatchRunnerMP(Friends,
                            max_steps=max_steps,
                            iterations=replicates,
                            variable_parameters={var: samples},
                            model_reporters=model_reporters,
                            display_progress=True,
                            nr_processes=multiprocessing.cpu_count() - 1)

        batch.run_all()
        end = time.time()
        print(
            "Performed", replicates * distinct_samples,
            "model runs in", np.round(end - begin),
            "seconds."
        )

        data[var] = batch.get_model_vars_dataframe()
    return [problem, data]


# plotting function
def plot_param_var_conf(ax, df, var, param):
    x = df.groupby(var).mean().reset_index()[var]
    y = df.groupby(var).mean()[param]

    replicates = df.groupby(var)[param].count()
    err = (1.96 * df.groupby(var)[param].std()) / np.sqrt(replicates)

    ax.plot(x, y, c='k')
    ax.fill_between(x, y - err, y + err)

    ax.set_xlabel(var)
    ax.set_ylabel(param)


# plotting ofat analysis
def plot_ofat_results(problem, data):
    f, axs = plt.subplots(3, figsize=(7, 10))
    parameter = problem['names'][0]
    plot_param_var_conf(axs[0], data[parameter], parameter, 'Friends score')
    plot_param_var_conf(axs[1], data[parameter], parameter, 'Friends distance')
    plot_param_var_conf(axs[2], data[parameter], parameter, 'Friends spatial distance')
    plt.savefig('plots/' + str(parameter) + 'ofat.png')


def write_results_to_file(problem, data):
    parameter = problem['names'][0]
    data[parameter].to_csv('data/' + str(parameter) + 'ofat.csv')


if __name__ == '__main__':
    [problem, data] = perform_analysis()
    write_results_to_file(problem, data)
    plot_ofat_results(problem, data)
