import matplotlib.pyplot as plt
import networkx as nx


def visualize_network(M, graph):
    # to plot the nodes and edges of friendships
    scores = graph.to_numpy()
    for j in range(len(scores)):
        for t in range(len(scores[0])):
            if scores[j][t] != 0:
                M.add_edge(j, t, weight=scores[j][t])

    close = [(u, v) for (u, v, d) in M.edges(data=True) if d['weight'] < 0.3]
    mid = [(u, v) for (u, v, d) in M.edges(data=True) if d['weight'] > 0.3 and d['weight'] < 0.6]
    far = [(u, v) for (u, v, d) in M.edges(data=True) if d['weight'] >= 0.6]

    nx.draw_networkx_nodes(
        M,
        nx.get_node_attributes(M, 'pos'),
        node_size=80, node_color='dimgrey'
    )
    nx.draw_networkx_edges(
        M,
        nx.get_node_attributes(M, 'pos'),
        edgelist=close, width=3.5, edge_color='navy'
    )
    nx.draw_networkx_edges(
        M,
        nx.get_node_attributes(M, 'pos'),
        edgelist=mid, width=2, edge_color='royalblue'
    )
    nx.draw_networkx_edges(
        M,
        nx.get_node_attributes(M, 'pos'),
        edgelist=far, width=0.8, edge_color='skyblue'
    )

    plt.axes().set_aspect('equal')
    plt.show()
