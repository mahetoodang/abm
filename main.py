import pandas as pd

from functionality.model import Friends
from visualization.graph_visualization import \
    visualize_network, \
    distance_histograms, \
    friends_speed_histogram
from visualization.model_report import create_model_report


def main(iter, seg, mob, hub):

    # Test/Info Print statement
    parameters = [seg, mob, hub]
    param_str = []
    for param in parameters:
        if param == True:
            param_str.append("WITH ")
        else:
            param_str.append("WITHOUT ")
    print('RUNNING Friends model for ' + str(iter) + ' ITERATION(S)\n' + param_str[0] +
        "segregation,\n" + param_str[1] + "varying mobility and\n" +
        param_str[2] + "social hubs.\n")

    # Segregation level to 0
    if seg == False:
        s = 0

    friends = Friends(segregation=s, mobility=mob, hubs=hub)

    all_dfs = []
    # Loop if iterations more than one
    if iter > 1:
        for i in range(iter):
            iteration_df = friends.run_model(iterating=True)
            all_dfs.append(iteration_df)
        all_dfs = pd.concat(all_dfs)
        by_row_index = all_dfs.groupby(all_dfs.index)
        df_means = by_row_index.mean()
        df_means.to_csv('data/sim_stats_avg_' + str(iterations) + '_runs.csv')

    else:
        friends.run_model()
        df = friends.data_collector.get_model_vars_dataframe()
        visualize_network(friends.M, friends.friends_score)
        distance_histograms(friends.M, friends)
        friends_speed_histogram(friends.M)
        print("Number of pairs of friends: ", df['Friends'].iloc[-1])
        print("Number of interactions: ", df['Interactions'].iloc[-1])
        create_model_report(html_report=False)  # set html_report to True to produce pandas_profiling report


if __name__ == '__main__':
    '''Run model'''
    
    main(iter=1, seg=False, mob=False, hub=False)
