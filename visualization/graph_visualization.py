import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import seaborn as sns

def visualize_network(M, graph, num, iterations):
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
    
     #draw only once! Last iteration
    if (num+1)== iterations:
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
    

    if (num+1)== iterations:
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
        plt.savefig('data/img/Node_Graph.png')
        plt.close()


def distance_histograms(M, friends, num, iterations, scores):
    # creating stacked histograms 
    edges = list(M.edges())
    maxdist = friends.height + friends.width

    close = np.zeros(maxdist)
    mid = np.zeros(maxdist)
    far = np.zeros(maxdist)
    close2 = np.zeros(maxdist)
    mid2 = np.zeros(maxdist)
    far2 = np.zeros(maxdist)

    character = nx.get_node_attributes(M, 'character')
    pos = nx.get_node_attributes(M, 'pos')
    for i in range(len(edges)):
        p1 = edges[i][0]
        p2 = edges[i][1]
        dist = abs(pos[p1][0] - pos[p2][0]) + abs(pos[p1][1] - pos[p2][1])
        index = int(dist)
        weight_friend = M[p1][p2]['weight']
        if abs(character[edges[i][0]] - character[edges[i][1]]) < 0.3:
            close[index] += 1
            close2[index] += weight_friend
        elif abs(character[edges[i][0]] - character[edges[i][1]]) < 0.6:
            mid[index] += 1
            mid2[index] += weight_friend
        else:
            far[index] += 1
            far2[index] += weight_friend
     
    for i in range(len(far2)):
        if close2[i] != 0:
            close2[i] = close2[i]/close[i]
        if mid2[i] != 0:
            mid2[i] = mid2[i]/mid[i]
        if far2[i] != 0:
            far2[i] = far2[i]/far[i]

    scores = np.vstack((scores,close))
    scores = np.vstack((scores,mid))
    scores = np.vstack((scores,far))
    scores = np.vstack((scores,close2))
    scores = np.vstack((scores,mid2))
    scores = np.vstack((scores,far2))


    if (num+1) == iterations:
        fig4 = plt.figure(figsize=(8,5))
        ax4 = fig4.add_subplot(111, axisbelow=True)

        scores = np.delete(scores, (0), axis=0)
        close = scores[::6]
        mid = scores[1::6]
        far = scores[2::6]

        avg_close = np.mean(close, axis = 0)
        sd_close = np.std(close, axis=0)
        avg_mid = np.mean(mid, axis = 0)
        sd_mid = np.std(mid, axis=0)
        avg_far = np.mean(far, axis = 0)
        sd_far = np.std(far, axis=0)
        close = avg_close
        mid = avg_mid
        far = avg_far

        bins = np.arange(maxdist)
        nc, bin_c, _ = ax4.hist(bins,maxdist, weights=close, stacked=True, label='similar', color='blue')
        midway = 0.5*(bin_c[1:] + bin_c[:-1])
        plt.errorbar(midway, nc, yerr=sd_close, fmt='none')

        nm, bin_m, _ = ax4.hist(bins,maxdist, weights=mid, stacked=True,label ='not so similar', color='green' )
        midway = 0.5*(bin_m[1:] + bin_m[:-1])
        plt.errorbar(midway, nm, yerr=sd_mid, fmt='none')

        nf, bin_f, _ = ax4.hist(bins,maxdist, weights=far, stacked=True, label = "not similar at all", color='purple')
        midway = 0.5*(bin_f[1:] + bin_f[:-1])
        plt.errorbar(midway, nf, yerr=sd_far, fmt='none')

        ax4.legend(title="Similarity of Friends")
        ax4.set_xlabel("Spatial of Distance of friends", fontsize=16)  
        ax4.set_ylabel("Number of friends", fontsize=16)
        fig4.savefig('data/img/Number Friends VS Distance.png')
        plt.close()

        fig5 = plt.figure(figsize=(8,5))
        ax5 = fig5.add_subplot(111, axisbelow=True) 

        close = scores[3::6]
        mid = scores[4::6]
        far = scores[5::6]
        avg_close = np.mean(close, axis = 0)
        sd_close = np.std(close, axis=0)
        avg_mid = np.mean(mid, axis = 0)
        sd_mid = np.std(mid, axis=0)
        avg_far = np.mean(far, axis = 0)
        sd_far = np.std(far, axis=0)
        close = avg_close
        mid = avg_mid
        far = avg_far

        nc, bin_c, _ = ax5.hist(bins,maxdist, weights=close, stacked=True, label='similar', color='blue')
        midway = 0.5*(bin_c[1:] + bin_c[:-1])
        plt.errorbar(midway, nc, yerr=sd_close, fmt='none')

        nm, bin_m, _ = ax5.hist(bins,maxdist, weights=mid, stacked=True,label ='not so similar', color='green')
        midway = 0.5*(bin_m[1:] + bin_m[:-1])
        plt.errorbar(midway, nm, yerr=sd_mid, fmt='none')

        nf, bin_f, _ = ax5.hist(bins,maxdist, weights=far, stacked=True, label = "not similar at all", color='purple')
        midway = 0.5*(bin_f[1:] + bin_f[:-1])
        plt.errorbar(midway, nf, yerr=sd_far, fmt='none')

        ax5.legend(title="Similarity of Friends")
        ax5.set_xlabel("Spatial distance of friends", fontsize=16)  
        ax5.set_ylabel("Avg. Friend Score", fontsize=16)
        fig5.savefig('data/img/AVG. Friend Score VS Distance.png')
        plt.close()
        print()

    return scores    


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
