import random
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation

from .agent import Human


class Friends(Model):
    '''
    Model of making friends in a spatial setting
    '''

    def __init__(
            self,
            height=20, width=20,
            population_size=40
    ):

        super().__init__()

        self.height = height
        self.width = width
        self.population_size = population_size

        # Add a schedule
        self.schedule = RandomActivation(self)

        self.grid = MultiGrid(self.width, self.height, torus=True)
        self.data_collector = DataCollector({
            "Friends": lambda m: np.count_nonzero(self.friends.values),
            "Interactions": lambda m: np.sum(self.interactions.values)
        })

        # Create the population
        self.init_population(self.population_size)
        self.friends = self.init_matrix()
        self.interactions = self.init_matrix()
        self.friends_score = self.init_matrix()

        # This is required for the datacollector to work
        self.running = True
        self.data_collector.collect(self)

    def init_population(self, n):
        for i in range(n):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            self.new_agent((x, y))

    def init_matrix(self):
        agents = self.schedule.agents
        ids = [ag.unique_id for ag in agents]
        n = len(ids)
        mat = pd.DataFrame(np.zeros((n, n)), index=ids, columns=ids)
        return mat

    def store(self, Graph, bool):
        if bool:
            if list(Graph)[0]==0:
                global M
                M = Graph
            else:
                M = nx.compose(M,Graph)
        else:
            #to plot the nodes and edges of friendships
            scores = Graph.to_numpy()
            for j in range(len(scores)):
                for t in range(len(scores[0])):
                    if scores[j][t]!=0:
                        M.add_edge(j,t, weight = scores[j][t])

            close=[(u,v) for (u,v,d) in M.edges(data=True) if d['weight'] <0.3]
            mid=[(u,v) for (u,v,d) in M.edges(data=True) if d['weight'] >0.3 and d['weight']<0.6]
            far=[(u,v) for (u,v,d) in M.edges(data=True) if d['weight'] >=0.6]

            nx.draw_networkx_nodes(M, nx.get_node_attributes(M, 'pos'), node_size=80, node_color='dimgrey')
            nx.draw_networkx_edges(M, nx.get_node_attributes(M, 'pos'), edgelist=close, width=3.5, edge_color='navy')
            nx.draw_networkx_edges(M, nx.get_node_attributes(M, 'pos'), edgelist=mid, width=2, edge_color='royalblue')
            nx.draw_networkx_edges(M, nx.get_node_attributes(M, 'pos'), edgelist=far, width=0.8, edge_color='skyblue')

            plt.show()

    def new_agent(self, pos):
        ID = self.next_id()
        agent = Human(ID, self, pos)
        self.grid.place_agent(agent, pos)
        self.schedule.add(agent)

        #ID and initial pos also used for node graph
        M = nx.Graph()
        M.add_node((ID-1), pos=pos)
        self.store(M, True)

    def step(self):
        self.schedule.step()

        # Save the statistics
        self.data_collector.collect(self)

    def run_model(self, step_count=500):
        for i in range(step_count):
            self.step()

            # once every 5 steps
            if i % 5 == 0:
                 self.friends_score = self.friends_score * 0.99
        print(self.friends_score)
        self.store(self.friends_score, False)
