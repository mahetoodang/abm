import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import seaborn as sns


def visualize_network(M, graph, friends):
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
    plt.savefig('Node_Graph.png')

    #creating stacked histograms
    # Num Friends VS Distance (per similarity)
    A = list(M.edges())
    fig1 = plt.figure(figsize=(8,5))
    ax1 = fig1.add_subplot(111, axisbelow=True)
    maxdist = friends.height + friends.width
    close = np.zeros(maxdist)
    mid = np.zeros(maxdist)
    far = np.zeros(maxdist)
    close2 = np.zeros(maxdist)
    mid2 = np.zeros(maxdist)
    far2 = np.zeros(maxdist)
    character = nx.get_node_attributes(M,'character')
    pos = nx.get_node_attributes(M,'pos')
    
    for i in range(len(M.edges())):
        p1 = A[i][0] 
        p2 = A[i][1]
        weight_friend = M[p1][p2]['weight']
        dist = abs(pos[p1][0]- pos[p2][0]) + abs(pos[p1][1]- pos[p2][1])
        index = int(dist)
        if abs(character[A[i][0]]-character[A[i][1]]) < 0.33:
            close[index] += 1
            close2[index] += weight_friend
        elif abs(character[A[i][0]]-character[A[i][1]]) < 0.66:
            mid[index] += 1
            mid2[index] += weight_friend
        else :
            far[index] += 1
            far2[index] += weight_friend
            
    bins = np.arange(maxdist)
    ax1.hist(bins,maxdist, weights=close, stacked=True, label='similar')
    ax1.hist(bins,maxdist, weights=mid, stacked=True,label ='not so similar' )
    ax1.hist(bins,maxdist, weights=far, stacked=True, label = "not similar at all")
    ax1.legend(title="Similarity of Friends")
    ax1.set_xlabel("Spatial of Distance of friends", fontsize=16)  
    ax1.set_ylabel("Number of friends", fontsize=16)
    plt.axes().set_aspect('equal')
    fig1.savefig('Number Friends VS Distance.png')

    #Avg Friend Score VS Distance (per similarity)
    fig2 = plt.figure(figsize=(8,5))
    ax2 = fig2.add_subplot(111, axisbelow=True)
    
    for i in range(len(far)):
        if close2[i] != 0:
            close2[i] = close2[i]/close[i]
        if mid2[i] != 0:
            mid2[i] = mid2[i]/mid[i]
        if far2[i] != 0:
            far2[i] = far2[i]/far[i]
            
    bins = np.arange(maxdist)
    ax2.hist(bins,maxdist, weights=close2, stacked=True, label='similar')
    ax2.hist(bins,maxdist, weights=mid2, stacked=True,label ='not so similar' )
    ax2.hist(bins,maxdist, weights=far2, stacked=True, label = "not similar at all")
    ax2.legend(title="Similarity of Friends")
    ax2.set_xlabel("Spatial of Distance of friends", fontsize=16)  
    ax2.set_ylabel("Avg. Friend Score", fontsize=16)
    plt.axes().set_aspect('equal')
    fig2.savefig('Friend Score VS Distance.png')

