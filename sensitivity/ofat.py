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
    'names': ['tolerance'],
    'bounds': [[0.01, 0.99]]
}
begin = time.time()
# Set the repetitions, the amount of steps, and the amount of distinct values per variable
replicates = 10
max_steps = 100
distinct_samples = 10

# Set the outputs
model_reporters = {"Friends score": lambda m: m.avg_friends_score(), 
                   "Friends distance": lambda m: m.avg_friends_social_distance(),
                   "Friends spatial distance": lambda m: m.avg_friends_spatial_distance()}
            
data = {}

for i, var in enumerate(problem['names']):
    # Get the bounds for this variable and get <distinct_samples> samples within this space (uniform)
    samples = np.linspace(*problem['bounds'][i], num=distinct_samples)
    
    # Keep in mind that wolf_gain_from_food should be integers. You will have to change
    # your code to acommidate for this or sample in such a way that you only get integers.
    #if var == 'wolf_gain_from_food':
    #    samples = np.linspace(*problem['bounds'][i], num=distinct_samples, dtype=int)
    
    batch = BatchRunnerMP(Friends, 
                        max_steps=max_steps,
                        iterations=replicates,
                        variable_parameters={var: samples},
                        model_reporters=model_reporters,
                        display_progress=True,
                        nr_processes=multiprocessing.cpu_count() - 1)
    
    batch.run_all()
    end = time.time()
    print("Model run-time:", end - begin)

    data[var] = batch.get_model_vars_dataframe()

    print(data)
    
# # plotting

def plot_param_var_conf(ax, df, var, param):
    x = df.groupby(var).mean().reset_index()[var]
    y = df.groupby(var).mean()[param]

    replicates = df.groupby(var)[param].count()
    err = (1.96 * df.groupby(var)[param].std()) / np.sqrt(replicates)

    ax.plot(x, y, c='k')
    ax.fill_between(x, y - err, y + err)

    ax.set_xlabel(var)
    ax.set_ylabel(param)

# def plot_all_vars(df, param):
#     F, axs = plt.subplots(3, figsize=(7, 10))
    
#     for i, var in enumerate(problem['names']):
#         plot_param_var_conf(axs[i], data[var], var, param, i)

# for param in ('Friends score'):
#     plot_all_vars(data, param)
#     plt.show()

f, axs = plt.subplots(3, figsize=(7, 10))

plot_param_var_conf(axs[0], data['tolerance'], 'tolerance', 'Friends score')
plt.show()




