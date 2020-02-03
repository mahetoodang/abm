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


def create_samples(problem):
    replicates = 10
    distinct_samples = 2

    # We get all our samples here
    param_values = saltelli.sample(problem, distinct_samples)
    param_values = np.array(list(param_values) * replicates)
    return param_values


def run_analysis(samples):
    data = []
    p = mp.Pool(processes=mp.cpu_count() - 1)
    for item in samples:
        p.apply_async(run_model, args=[item], callback=make_log_result(data, len(samples)))
    p.close()
    p.join()

    df = pd.DataFrame(
        data,
        columns=[
            'tolerance', 'social_extroversion', 'mobility', 'decay',
            'friends_score', 'social_distance', 'spatial_distance'
        ]
    )
    return df


def make_log_result(results, len_data):
    def log_result(retval):
        results.append(retval)
        if len(results) % (len_data // 20) == 0:
            print('{:.0%} done'.format(len(results)/len_data))
    return log_result


if __name__ == '__main__':
    problem = {
        'num_vars': 4,
        'names': ['tolerance', 'social_extroversion', 'mobility', 'decay'],
        'bounds': [[0.0, 1.0], [0.0, 1.0], [0.0, 1.0], [0.0, 1.0]]
    }
    samples = create_samples(problem)
    results = run_analysis(samples)
    results.to_csv('data/global.csv')
