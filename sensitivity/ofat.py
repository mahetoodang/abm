"""
OFAT Analysis: replace names in problem dictionary with the variable name you are testing.
See below for available parameter names.
"""

import sys
sys.path.append('../')
import time

from functionality.model import Friends
from mesa.batchrunner import BatchRunnerMP, BatchRunner
from functionality.agent import Human
from SALib.analyze import sobol
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
import multiprocessing

problem = {
    'num_vars': 1,
    'names': ['mobility'], # available parameters: 'tolerance','social_extroversion','mobility','decay'
    'bounds': [[0.01, 0.99]]
}
begin = time.time()

# Set the repetitions, the amount of steps, and the amount of distinct values per variable
replicates = 100
max_steps = 1000
distinct_samples = 15

# Set the outputs
model_reporters = {"Friends score": lambda m: m.avg_friends_score(),
                   "Friends distance": lambda m: m.avg_friends_social_distance(),
                   "Friends spatial distance": lambda m: m.avg_friends_spatial_distance()}

data = {}

for i, var in enumerate(problem['names']):
    # get the bounds for this variable and get <distinct_samples> samples within this space (uniform)
    samples = np.linspace(*problem['bounds'][i], num=distinct_samples)

    batch = BatchRunner(Friends,
                        max_steps=max_steps,
                        iterations=replicates,
                        variable_parameters={var: samples},
                        model_reporters=model_reporters,
                        display_progress=True)

    batch.run_all()
    end = time.time()
    print("Model run-time:", end - begin)

    data[var] = batch.get_model_vars_dataframe()

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

f, axs = plt.subplots(3, figsize=(7, 10))
parameter = problem['names'][0]
plot_param_var_conf(axs[0], data[parameter], parameter, 'Friends score')
plot_param_var_conf(axs[1], data[parameter], parameter, 'Friends distance')
plot_param_var_conf(axs[2], data[parameter], parameter, 'Friends spatial distance')
plt.savefig('plots/' + str(parameter) + 'ofat.png')
plt.show()
