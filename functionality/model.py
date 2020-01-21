import random
import numpy as np
import pandas as pd
import networkx as nx

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation

from .agent import Human
from .agent import Cell


class Friends(Model):
    '''
    Model of making friends in a spatial setting
    '''

    def __init__(
            self,
            height=20, width=20,
            population_size=30
    ):

        super().__init__()

        self.height = height
        self.width = width
        self.population_size = population_size

        # Add a schedule
        self.schedule = RandomActivation(self)

        self.grid = MultiGrid(self.width, self.height, torus=False)
        self.data_collector = DataCollector({
            "Friends": lambda m: np.count_nonzero(self.friends.values),
            "Interactions": lambda m: np.sum(self.interactions.values)
        })

        # Create the population
        self.M = nx.Graph()
        self.init_population()
        self.init_cells()

        self.friends = self.init_matrix()
        self.interactions = self.init_matrix()
        self.friends_score = self.init_matrix()

        # This is required for the datacollector to work
        self.running = True
        self.data_collector.collect(self)

    def init_population(self):
        speed_dist = [0.6, 0.3, 0.1]
        for i in range(self.population_size):
            choice = np.random.random()
            if choice < speed_dist[0]:
                speed = 1
            elif choice < speed_dist[0] + speed_dist[1]:
                speed = 2
            else:
                speed = 3
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            self.new_agent((x, y), speed)

    def init_cells(self):
        # Innitialize cell values
        #TODO: use new_agent()
        for _, x, y in self.grid.coord_iter():
            agent_id = self.next_id()
            cell = Cell(agent_id, self, (x, y))
            self.grid.place_agent(cell, (x, y))
            self.schedule.add(cell)


    def init_matrix(self):
        agents = self.schedule.agents
        ids = [ag.unique_id for ag in agents]
        n = len(ids)
        mat = pd.DataFrame(np.zeros((n, n)), index=ids, columns=ids)
        return mat

    def new_agent(self, pos, speed):
        agent_id = self.next_id()
        agent = Human(agent_id, self, pos, speed)
        self.grid.place_agent(agent, pos)
        self.schedule.add(agent)

        #ID and initial pos also used for node graph
        M = nx.Graph()
        M.add_node((agent_id-1), pos=pos, speed=speed)
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
        #print(self.friends_score)

        sim_stats = pd.DataFrame()

        for agent in self.schedule.agents:
            if type(agent) is Human:
                nx.set_node_attributes(self.M, {(agent.unique_id-1):{'character':agent.character}})
                score, social, spatial, count = agent.get_avg()
                stats = dict(
                    agent_id = agent.unique_id,
                    friend_count = count,
                    avg_friend_score = score,
                    avg_social_dist = social,
                    avg_spatial_dist = spatial)

                sim_stats = sim_stats.append(stats, ignore_index=True)

        file_string = 'data/' + 'sim_stats_' + str(self.population_size) + 'agents.csv'

        sim_stats.to_csv(file_string)

        #return self.friends_score
