import random
import numpy as np
import pandas as pd
import networkx as nx

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
            population_size=10
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
        self.M = nx.Graph()
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

    def new_agent(self, pos):
        agent_id = self.next_id()
        agent = Human(agent_id, self, pos)
        self.grid.place_agent(agent, pos)
        self.schedule.add(agent)

        #ID and initial pos also used for node graph
        M = nx.Graph()
        M.add_node((agent_id-1), pos=pos)
        self.M = nx.compose(self.M, M)

    def step(self):
        self.schedule.step()

        # Save the statistics
        self.data_collector.collect(self)

    def run_model(self, step_count=500):
        for i in range(step_count):
            self.step()

            # once every 5 steps
            if i % 10 == 0:
                 self.friends_score = self.friends_score * 0.99
        print(self.friends_score)

        for agent in self.schedule.agents:
            score, social, spatial, count = agent.get_avg()
            print(agent.unique_id)
            print(count)
            print(score)
            print(social)
            print(spatial)
            print()
        #self.store(self.friends_score, False)
        
