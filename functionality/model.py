import random
import numpy as np
import pandas as pd

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
            population_size=6
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
        agent = Human(self.next_id(), self, pos)
        self.grid.place_agent(agent, pos)
        self.schedule.add(agent)

    def step(self):
        self.schedule.step()
        # Save the statistics
        self.data_collector.collect(self)

    def run_model(self, step_count=200):
        for i in range(step_count):
            self.step()
