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

        # add a schedule and a grid
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(self.width, self.height, torus=False)

        # add datacollector
        self.data_collector = DataCollector({
            "Friends score": lambda m: self.avg_friends_score(),
            "Friends distance": lambda m: self.avg_friends_social_distance(),
            "Friends spatial distance": lambda m: self.avg_friends_spatial_distance()
        })

        # create the population
        self.M = nx.Graph()
        self.init_population(tolerance)
        self.init_cells()

        # matrices to keep track of friends, friends scores, interaction count
        # time since last interaction, social distance and spatial distance
        self.friends = self.init_matrix() # not used
        self.friends_score = self.init_matrix()
        self.interactions = self.init_matrix()
        self.last_interaction = self.init_matrix()
        [self.social_distance, self.spatial_distance] = self.init_distances()

        # this is required for the data_collector to work
        self.running = True
        self.data_collector.collect(self)

    def init_population(self, tolerance):
        '''
        Runs Schelling model based on grid size, tolerance level and population
        size. Innitializes population (Human agents) and home locations.
        '''
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
        '''
        Innitializes cell population for grid.
        '''

        # initialize cells and values for model with social hubs.
        if self.hubs:
            for _, x, y in self.grid.coord_iter():
                agent_id = self.next_id()
                cell = Cell(agent_id, self, (x, y), 0.5)
                self.grid.place_agent(cell, (x, y))
        # initialize cells for model without social hubs.
        else:
            for _, x, y in self.grid.coord_iter():
                agent_id = self.next_id()
                cell = Cell(agent_id, self, (x, y), 0)
                self.grid.place_agent(cell, (x, y))

    def init_matrix(self):
        '''
        Creates and returns zeros DataFrame with the Human agent id's used as labels.
        '''

        agents = self.schedule.agents
        ids = [ag.unique_id for ag in agents if type(ag) is Human]
        n = len(ids)
        mat = pd.DataFrame(np.zeros((n, n)), index=ids, columns=ids)
        return mat

    def init_distances(self):
        '''
        Creates and returns two matrices to keep track of social and spatial
        distances between pairs of Human agents.
        '''

        agents = self.schedule.agents
        processed = []
        social_distance = self.init_matrix()
        spatial_distance = self.init_matrix()
        for ag1 in agents:
            i = ag1.unique_id
            for ag2 in agents:
                j = ag2.unique_id
                if i != j and j not in processed:
                    soc_dist = np.abs(ag1.character - ag2.character)
                    spat_dist = ag1.get_distance(ag2.pos)
                    social_distance.values[i-1,j-1] = social_distance.values[j-1,i-1] = soc_dist
                    spatial_distance.values[i-1][j-1] = spatial_distance.values[j-1][i-1] = spat_dist
            processed.append(i)
        return [social_distance, spatial_distance]

    def new_agent(self, pos, speed, character):
        '''
        Create new Human agent
        '''

        agent_id = self.next_id()
        agent = Human(agent_id, self, pos, character, speed)
        self.grid.place_agent(agent, pos)
        self.schedule.add(agent)

        # ID and initial pos also used for node graph
        M = nx.Graph()
        M.add_node((agent_id-1), pos=pos, speed=speed, character=character)
        self.M = nx.compose(self.M, M)

    def step(self):
        '''
        Execute next time step.
        '''
        self.schedule.step()

        # friends_score decay functionality
        val = self.friends_score.values
        mask_val = self.last_interaction.copy().values
        val[mask_val != 0] *= self.decay
        self.last_interaction += 1

        # Save the statistics
        self.data_collector.collect(self)

    def avg_friends_score(self):
        '''
        Return average friends score of population.
        '''

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
        '''
        Returns average social distance between two friends.
        '''

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
        '''
        Returns average spatial distance between two friends.
        '''

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
        '''
        Runs model.
        '''
        
        for i in range(step_count):
            self.step()
