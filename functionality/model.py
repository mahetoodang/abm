import numpy as np
import pandas as pd
import networkx as nx

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation

from .agent import Human, Cell
from .schelling import SchellingModel


class Friends(Model):
    '''
    Model of making friends in a spatial setting
    '''
    def __init__(
            self,
            height=20, width=20,
            population_size=100,
            tolerance=0.3,
            social_extroversion=0.6,
            decay=0.99,
            mobility = 0.5,
            hubs = True
    ):

        super().__init__()

        self.height = height
        self.width = width
        self.population_size = population_size
        self.mobility = mobility
        self.hubs = hubs
        self.social_extroversion = social_extroversion
        self.decay = decay

        # Add a schedule and a grid
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(self.width, self.height, torus=False)

        self.data_collector = DataCollector({
            "Friends score": lambda m: self.avg_friends_score(),
            "Friends distance": lambda m: self.avg_friends_social_distance(),
            "Friends spatial distance": lambda m: self.avg_friends_spatial_distance()
        })

        # Create the population
        self.M = nx.Graph()
        self.init_population(tolerance)
        self.init_cells()

        self.friends = self.init_matrix() # not used
        self.friends_score = self.init_matrix()
        self.interactions = self.init_matrix()
        self.last_interaction = self.init_matrix()
        [self.social_distance, self.spatial_distance] = self.init_distances()

        # This is required for the data_collector to work
        self.running = True
        self.data_collector.collect(self)

    def init_population(self, tolerance):
        schelling = SchellingModel(
            self.height, self.width,
            tolerance,
            self.population_size
        )
        for i in range(200):
            schelling.step()
            if not schelling.running:
                break
        for ag in schelling.schedule.agents:
            speed = 1 + (np.random.random() < self.mobility) * 1
            [x, y] = ag.pos
            character = ag.character
            self.new_agent((x, y), speed, character)

    def init_cells(self):
        # Initialize cell values
        if self.hubs:
            for _, x, y in self.grid.coord_iter():
                agent_id = self.next_id()
                cell = Cell(agent_id, self, (x, y), 0.5)
                self.grid.place_agent(cell, (x, y))
        else:
            for _, x, y in self.grid.coord_iter():
                agent_id = self.next_id()
                cell = Cell(agent_id, self, (x, y), 0)
                self.grid.place_agent(cell, (x, y))


    def init_matrix(self):
        agents = self.schedule.agents
        ids = [ag.unique_id for ag in agents if type(ag) is Human]
        n = len(ids)
        mat = pd.DataFrame(np.zeros((n, n)), index=ids, columns=ids)
        return mat

    def init_distances(self):
        agents = self.schedule.agents
        social_distance = self.init_matrix()
        spatial_distance = self.init_matrix()
        for ag1 in agents:
            for ag2 in agents:
                i = ag1.unique_id
                j = ag2.unique_id
                if i != j:
                    soc_dist = np.abs(ag1.character - ag2.character)
                    spat_dist = ag1.get_distance(ag2.pos)
                    social_distance[i][j] = soc_dist
                    spatial_distance[i][j] = spat_dist
        return [social_distance, spatial_distance]

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

        # friends_score decay functionality
        val = self.friends_score.values
        mask_val = self.last_interaction.copy().values
        val[mask_val != 0] *= self.decay
        # old one for safety
        # for column in ids:
        #     values = self.friends_score[column].values
        #     mask_values = self.last_interaction[column].values
        #     mask = mask_values > 0
        #     values[mask] *= self.decay
        #     self.friends_score[column] = values
        self.last_interaction += 1

        # Save the statistics
        self.data_collector.collect(self)

    def avg_friends_score(self):
        mat = self.friends_score.copy().values
        mat[mat == 0] = np.nan
        try:
            means = np.nanmean(mat, axis=0)
            means[np.isnan(means)] = 0
            mean = np.mean(means)
        except:
            mean = 0
        return mean

    def avg_friends_social_distance(self):
        check = self.friends_score.copy().values
        mat = self.social_distance.copy().values
        mat[check == 0] = np.nan
        try:
            means = np.nanmean(mat, axis=0)
            means[np.isnan(means)] = 0
            mean = np.mean(means)
        except:
            mean = 0
        return mean

    def avg_friends_spatial_distance(self):
        check = self.friends_score.copy().values
        mat = self.spatial_distance.copy().values
        mat[check == 0] = np.nan
        try:
            means = np.nanmean(mat, axis=0)
            means[np.isnan(means)] = 0
            mean = np.mean(means)
        except:
            mean = 0
        return mean

    def run_model(self, step_count=500):
        for i in range(step_count):
            self.step()

        #file_name = 'data/' + 'sim_stats_' + str(self.population_size) + 'agents.csv'

        #if iterating:
        #    return create_sim_stats(self.schedule, self.M, True)
        #else:
        #    create_sim_stats(self.schedule, self.M, False, file_name)
