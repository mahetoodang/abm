import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

def visualize_network(M, graph):
    # to plot the nodes and edges of friendships
    scores = graph.to_numpy()
    for j in range(len(scores)):
        for t in range(len(scores[0])):
            if scores[j][t] != 0:
                M.add_edge(j, t, weight=scores[j][t])

    # agents
    slow = {idx: data['pos'] for (idx, data) in M.nodes(data=True) if data['speed'] == 1}
    moderate = {idx: data['pos'] for (idx, data) in M.nodes(data=True) if data['speed'] == 2}
    fast = {idx: data['pos'] for (idx, data) in M.nodes(data=True) if data['speed'] == 3}

    nx.draw_networkx_nodes(
        M,
        nx.get_node_attributes(M, 'pos'),
        nodelist=slow, node_size=50,
        node_color='gray'
    )
    nx.draw_networkx_nodes(
        M,
        nx.get_node_attributes(M, 'pos'),
        nodelist=moderate, node_size=50,
        node_color='yellow'
    )
    nx.draw_networkx_nodes(
        M,
        nx.get_node_attributes(M, 'pos'),
        nodelist=fast, node_size=50,
        node_color='red'
    )

    # connections between agents
    close = [(u, v) for (u, v, d) in M.edges(data=True) if d['weight'] < 5]
    mid = [(u, v) for (u, v, d) in M.edges(data=True) if 5 <= d['weight'] < 10]
    far = [(u, v) for (u, v, d) in M.edges(data=True) if d['weight'] >= 10]

    nx.draw_networkx_edges(
        M,
        nx.get_node_attributes(M, 'pos'),
        edgelist=close, width=0.7, edge_color='navy'
    )
    nx.draw_networkx_edges(
        M,
        nx.get_node_attributes(M, 'pos'),
        edgelist=mid, width=0.7, edge_color='royalblue'
    )
    nx.draw_networkx_edges(
        M,
        nx.get_node_attributes(M, 'pos'),
        edgelist=far, width=0.7, edge_color='skyblue'
    )

    plt.axes().set_aspect('equal')
    plt.savefig('data/img/network_graph.png')
    plt.close()


def distance_vs_number_histogram(M):
    # creating stacked histogram
    edges = list(M.edges())
    # need to get farthest distance (right now 25ish) automatically
    max_dist = 30
    close = np.zeros(max_dist)
    mid = np.zeros(max_dist)
    far = np.zeros(max_dist)
    character = nx.get_node_attributes(M, 'character')
    pos = nx.get_node_attributes(M, 'pos')
    
    for i in range(len(edges)):
        p1 = edges[i][0]
        p2 = edges[i][1]
        dist = abs(pos[p1][0] - pos[p2][0]) + abs(pos[p1][1] - pos[p2][1])
        # max_dist = np.max([max_dist, dist])
        index = int(dist)
        if abs(character[edges[i][0]] - character[edges[i][1]]) < 0.3:
            close[index] += 1
        elif abs(character[edges[i][0]] - character[edges[i][1]]) < 0.6:
            mid[index] += 1
        else:
            far[index] += 1
            
    bins = np.arange(max_dist)

    plt.hist(bins, max_dist, weights=close, stacked=True, label='similar')
    plt.hist(bins, max_dist, weights=mid, stacked=True, label='not so similar' )
    plt.hist(bins, max_dist, weights=far, stacked=True, label="not similar at all")
    plt.legend(title="Similarity of Friends")
    plt.xlabel("Distance of friends", fontsize=16)  
    plt.ylabel("Number of friends", fontsize=16)
    plt.savefig('data/img/distance_hist.png')
    plt.close()


def friends_speed_histogram(M):
    # creating stacked histogram
    edges = list(M.edges())
    # need to get farthest distance (right now 25ish) automatically
    max_dist = 30
    slow = np.zeros(max_dist)
    moderate = np.zeros(max_dist)
    fast = np.zeros(max_dist)
    speeds = nx.get_node_attributes(M, 'speed')
    pos = nx.get_node_attributes(M, 'pos')

    for i in range(len(edges)):
        p1 = edges[i][0]
        p2 = edges[i][1]
        dist = abs(pos[p1][0] - pos[p2][0]) + abs(pos[p1][1] - pos[p2][1])
        index = int(dist)
        if speeds[p1] == 1:
            slow[index] += 1
        elif speeds[p1] == 2:
            moderate[index] += 1
        else:
            fast[index] += 1

        if speeds[p2] == 1:
            slow[index] += 1
        elif speeds[p2] == 2:
            moderate[index] += 1
        else:
            fast[index] += 1

    bins = np.arange(max_dist)

    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(9, 4))
    [ax1, ax2, ax3] = ax
    ax1.hist(slow, bins, color="violet", density=True)
    ax2.hist(moderate, bins, color="blue", density=True)
    ax3.hist(fast, bins, color="red", density=True)
    ax1.title.set_text('Slow')
    ax2.title.set_text('Moderate')
    ax3.title.set_text('Fast')
    plt.setp(ax, ylim=(0, 1), xlabel="Distance to friend", ylabel="Proportion of friends")
    plt.tight_layout()
    plt.savefig('data/img/friend_speed.png')
    plt.close()
