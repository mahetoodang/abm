import pandas as pd
import numpy as np
import time

from functionality.model import Friends
from visualization.graph_visualization import \
    visualize_network, \
    distance_histograms, \
    friends_speed_histogram
from visualization.model_report import create_model_report


def main(iterations, loop):
    
    all_dfs = []
    friends = Friends()
    scores = np.zeros(friends.height + friends.width)
    
    if loop:
        for i in range(iterations):
            iteration_df = friends.run_model(iterating=True)
            all_dfs.append(iteration_df)
            visualize_network(friends.M, friends.friends_score, i , iterations)
            scores = distance_histograms(friends.M, friends, i, iterations, scores)
        all_dfs = pd.concat(all_dfs)
        by_row_index = all_dfs.groupby(all_dfs.index)
        df_means = by_row_index.mean()
        df_means.to_csv('data/sim_stats_avg_' + str(iterations) + '_runs.csv')

     
    else:
        i = 0
        friends.run_model()
        df = friends.data_collector.get_model_vars_dataframe()
        visualize_network(friends.M, friends.friends_score, i, iterations)
        distance_histograms(friends.M, friends, i, iterations, scores)
        friends_speed_histogram(friends.M)
        print("Number of pairs of friends: ", df['Friends'].iloc[-1])
        print("Number of interactions: ", df['Interactions'].iloc[-1])
        create_model_report(html_report=False)  # set html_report to True to produce pandas_profiling report


if __name__ == '__main__':
    begin = time.time()
    print(begin)
    main(iterations=2, loop=True)  # set loop to true to run model multiple times
    end = time.time()
    print("this run took:", end-begin)