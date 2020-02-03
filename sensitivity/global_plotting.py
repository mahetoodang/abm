from itertools import combinations
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from SALib.analyze import sobol


def analyse_results(df):
    global problem
    si_friends_score = sobol.analyze(problem, df['friends_score'].values, print_to_console=True)
    si_social_dist = sobol.analyze(problem, df['social_distance'].values, print_to_console=True)
    si_spatial_dist = sobol.analyze(problem, df['spatial_distance'].values, print_to_console=True)
    return [si_friends_score, si_social_dist, si_spatial_dist]


def plot_index(s, params, i, title=''):
    if i == '2':
        p = len(params)
        params = list(combinations(params, 2))
        indices = s['S' + i].reshape((p ** 2))
        indices = indices[~np.isnan(indices)]
        errors = s['S' + i + '_conf'].reshape((p ** 2))
        errors = errors[~np.isnan(errors)]
    else:
        indices = s['S' + i]
        errors = s['S' + i + '_conf']
        plt.figure()

    l = len(indices)

    plt.title(title)
    plt.ylim([-0.2, len(indices) - 1 + 0.2])
    plt.yticks(range(l), params)
    plt.errorbar(indices, range(l), xerr=errors, linestyle='None', marker='o')
    plt.axvline(0, c='k')
    plt.tight_layout()


def plot_results(df):
    global problem
    si_res = analyse_results(df)
    names = ['friends score', 'social distance', 'spatial distance']
    for idx, si in enumerate(si_res):
        # First order
        plot_index(si, problem['names'], '1', 'First order sensitivity for ' + names[idx])
        plt.show()

        # Second order
        plot_index(si, problem['names'], '2', 'Second order sensitivity for ' + names[idx])
        plt.show()

        # Total order
        plot_index(si, problem['names'], 'T', 'Total order sensitivity for ' + names[idx])
        plt.show()


if __name__ == '__main__':
    problem = {
        'num_vars': 4,
        'names': ['tolerance', 'social_extroversion', 'mobility', 'decay'],
        'bounds': [[0.0, 1.0], [0.0, 1.0], [0.0, 1.0], [0.0, 1.0]]
    }
    file_name = 'data/global_2000.csv'
    df = pd.read_csv(file_name)
    plot_results(df)
