from functionality.model import Friends
from visualization.graph_visualization import \
    visualize_network, \
    distance_vs_number_histogram, \
    friends_speed_histogram
from visualization.model_report import create_model_report
import pandas as pd


def main(iterations, loop):
    
    all_dfs=[]
    
    if loop == True:
        for i in range(iterations):
            friends = Friends()
            iteration_df = friends.run_model(iterating=True)
            all_dfs.append(iteration_df)
     
    else:
        friends = Friends()
        friends.run_model()
        df = friends.data_collector.get_model_vars_dataframe()
        visualize_network(friends.M, friends.friends_score)
        distance_vs_number_histogram(friends.M)
        friends_speed_histogram(friends.M)
        print("Number of pairs of friends: ", df['Friends'].iloc[-1])
        print("Number of interactions: ", df['Interactions'].iloc[-1])
        create_model_report(html_report=False)  # set html_report to True to produce pandas_profiling report
        
    all_dfs = pd.concat(all_dfs)
    by_row_index = all_dfs.groupby(all_dfs.index)
    df_means = by_row_index.mean()
    df_means.to_csv('data/sim_stats_avg_' + str(iterations) + '_runs.csv')



if __name__ == '__main__':
    main(iterations=2, loop=True) # set loop to true to run model multiple times
