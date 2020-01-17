from functionality.model import Friends
from visualization.graph_visualization import visualize_network


def main():
    friends = Friends()
    friends_score = friends.run_model()
    df = friends.data_collector.get_model_vars_dataframe()
    visualize_network(friends.M, friends.friends_score)
    print("Number of pairs of friends: ", df['Friends'].iloc[-1])
    print("Number of interactions: ", df['Interactions'].iloc[-1])


if __name__ == '__main__':
    main()
