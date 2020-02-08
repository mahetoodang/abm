import pandas as pd
import numpy as np
import time
from os import path, makedirs

from functionality.model import Friends
from visualization.graph_visualization import \
    visualize_network, \
    distance_histograms, \
    friends_speed_histogram
from visualization.model_report import create_model_report
from functionality.helpers import create_sim_stats


def main(iter, seg, mob, hub):

    # Print model parameters to console
    parameters = [seg, mob, hub]
    param_str = []
    for param in parameters:
        if param == True:
            param_str.append("WITH ")
        else:
            param_str.append("WITHOUT ")
    print('RUNNING Friends model for ' + str(iter) + ' ITERATION(S)\n' + param_str[0] +
        "tolerance,\n" + param_str[1] + "varying mobility and\n" +
        param_str[2] + "social hubs.\n")

    # Tolerance level to 0
    if seg == False:
        s = 0
        friends = Friends(tolerance=s, mobility=mob, hubs=hub)
    else:
        friends = Friends(mobility=mob, hubs=hub)

    all_dfs = []
    scores = np.zeros(friends.height + friends.width)
    # Loop if iterations more than one
    if iter > 1:
        begin = time.time()
        for i in range(iter):
            friends.run_model()
            iteration_df = create_sim_stats(friends.schedule, friends.M, True)
            all_dfs.append(iteration_df)
            visualize_network(friends.M, friends.friends_score, i, iter)
            scores = distance_histograms(friends.M, friends, i, iter, scores)
        end = time.time()
        print("Model run-time:", end - begin)
        all_dfs = pd.concat(all_dfs)
        by_row_index = all_dfs.groupby(all_dfs.index)
        df_means = by_row_index.mean()
        df_means.to_csv('data/avg_stats/sim_stats_avg_' + str(iter) + '_runs.csv')

    else:
        # Running model once (without iterations)
        i = 0
        begin = time.time()
        friends.run_model()
        end = time.time()
        print("Model run-time:", end - begin)
        df = friends.data_collector.get_model_vars_dataframe()
        visualize_network(friends.M, friends.friends_score, i, iter)
        distance_histograms(friends.M, friends, i, iter, scores)
        friends_speed_histogram(friends.M)
        print(df)
        timestr = time.strftime("%Y%m%d-%H%M%S")
        stats_df = create_sim_stats(friends.schedule, friends.M, False, 'data/stats/' + timestr + '.csv')
        create_model_report(html_report=True)  # set html_report to True to produce pandas_profiling report


if __name__ == '__main__':
    '''Run model: iterations, segregation, varying mobility, social hubs'''
    # READ ME FIRST
    # MOBILITY set either to 0.5 for True or 0/False for False. In the latter case it gives speed 1 to everybody,
    # in the former it gives speed 1 and 2 to roughly half the population. Changing this value between 0 and 1,
    #  changes the distribution of agents receiving a speed of 2.
    # if you would like to change the values of the other input parameters to something other than nominal values
    # you can change them in init in model.py (e.g tolerance and social extroversion). For tolerance you must also
    # turn seg to True.

    img_dir = path.exists('data/img')
    stats_dir = path.exists('data/stats')
    avg_dir = path.exists('data/avg_stats')
    html_dir = path.exists('data/html')

    if (img_dir & stats_dir & avg_dir & html_dir):
        pass
    else:
        makedirs('data/img')
        makedirs('data/stats')
        makedirs('data/avg_stats')
        makedirs('data/html')

    main(iter=1, seg=False, mob=0.5, hub=False) # SIMULATION CONFIGURATION
