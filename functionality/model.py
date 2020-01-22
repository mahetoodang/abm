import numpy as np
import pandas as pd
import networkx as nx

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation

from .agent import Human, Cell
from .helpers import \
    choose_speed, \
    create_sim_stats
from .schelling import SchellingModel


class Friends(Model):
    '''
    Model of making friends in a spatial setting
    '''
    def __init__(
            self,
            height=20, width=20,
            population_size=100,
            segregation=0.3,
            social_proximity=0.2
    ):

        super().__init__()

        self.height = height
        self.width = width
        self.population_size = population_size
        self.speed_dist = [0.6, 0.3, 0.1]

        # Add a schedule and a grid
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(self.width, self.height, torus=False)

        self.data_collector = DataCollector({
            "Friends": lambda m: np.count_nonzero(self.friends.values),
            "Interactions": lambda m: np.sum(self.interactions.values)
        })

        # Create the population
        self.M = nx.Graph()
        self.init_population(segregation, social_proximity)
        self.init_cells()

        self.friends = self.init_matrix()
        self.interactions = self.init_matrix()
        self.friends_score = self.init_matrix()

        # This is required for the data_collector to work
        self.running = True
        self.data_collector.collect(self)

    def init_population(self, segregation, social_proximity):
        schelling = SchellingModel(
            self.height, self.width,
            segregation,
            social_proximity,
            self.population_size
        )
        for i in range(200):
            schelling.step()
            if not schelling.running:
                break
        for ag in schelling.schedule.agents:
            speed = choose_speed(self.speed_dist)
            [x, y] = ag.pos
            character = ag.character
            self.new_agent((x, y), speed, character)

    def init_cells(self):
        # Initialize cell values
        for _, x, y in self.grid.coord_iter():
            agent_id = self.next_id()
            cell = Cell(agent_id, self, (x, y))
            self.grid.place_agent(cell, (x, y))

    def init_matrix(self):
        agents = self.schedule.agents
        ids = [ag.unique_id for ag in agents]
        n = len(ids)
        mat = pd.DataFrame(np.zeros((n, n)), index=ids, columns=ids)
        return mat

    def new_agent(self, pos, speed, character):
        agent_id = self.next_id()
        agent = Human(agent_id, self, pos, character, speed)
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

    def run_model(self, iterating=False, step_count=500):
        for i in range(step_count):
            self.step()

            # once every 5 steps
            if i % 10 == 0:
                 self.friends_score = self.friends_score * 0.99

        file_name = 'data/' + 'sim_stats_' + str(self.population_size) + 'agents.csv'

        if iterating:
            return create_sim_stats(self.schedule, self.M, True)
        else:
            create_sim_stats(self.schedule, self.M, False, file_name)
