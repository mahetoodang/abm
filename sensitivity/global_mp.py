import numpy as np
import pandas as pd
import multiprocessing as mp
from SALib.sample import saltelli

import sys
sys.path.append('../')

from functionality.model import Friends


def run_model(vals):
    md = Friends(
        population_size=10,
        tolerance=vals[0],
        social_extroversion=vals[1],
        mobility=vals[2],
        decay=vals[3]
    )
    max_steps = 20
    md.run_model(step_count=max_steps)
    friends_score = md.avg_friends_score()
    social_dist = md.avg_friends_social_distance()
    spatial_dist = md.avg_friends_spatial_distance()
    return np.append(vals, [friends_score, social_dist, spatial_dist])


def run_analysis():
    problem = {
        'num_vars': 4,
        'names': ['tolerance', 'social_extroversion', 'mobility', 'decay'],
        'bounds': [[0.0, 1.0], [0.0, 1.0], [0.0, 1.0], [0.0, 1.0]]
    }
    replicates = 2
    distinct_samples = 2

    # We get all our samples here
    param_values = saltelli.sample(problem, distinct_samples)

    param_values = np.array(list(param_values) * replicates)
    p = mp.Pool(processes=mp.cpu_count() - 1)
    data = p.map(run_model, param_values)
    p.close()

    df = pd.DataFrame(
        data,
        columns=[
            'tolerance', 'social_extroversion', 'mobility', 'decay',
            'friends_score', 'social_distance', 'spatial_distance'
        ]
    )
    return df


if __name__ == '__main__':
    results = run_analysis()
    results.to_csv('data/global.csv')
