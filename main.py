from functionality.model import Friends
from visualization.graph_visualization import \
    visualize_network, \
    distance_vs_number_histogram, \
    friends_speed_histogram
from visualization.model_report import create_model_report


def main():
    friends = Friends()
    friends.run_model()
    df = friends.data_collector.get_model_vars_dataframe()
    visualize_network(friends.M, friends.friends_score)
    distance_vs_number_histogram(friends.M)
    friends_speed_histogram(friends.M)
    print("Number of pairs of friends: ", df['Friends'].iloc[-1])
    print("Number of interactions: ", df['Interactions'].iloc[-1])
    create_model_report(html_report=False)  # set to True if you want html report else False


if __name__ == '__main__':
    main()
