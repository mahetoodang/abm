from functionality.model import Friends


def main():
    friends = Friends()
    friends.run_model(20)
    df = friends.data_collector.get_model_vars_dataframe()
    print("Number of pairs of friends: ", df['Friends'].iloc[-1])
    print("Number of interactions: ", df['Interactions'].iloc[-1])


if __name__ == '__main__':
    main()
