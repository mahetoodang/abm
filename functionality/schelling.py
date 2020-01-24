import numpy as np

from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import SingleGrid


class SchellingAgent(Agent):
    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.pos = pos
        self.character = np.random.random()

    def step(self):
        distance = 0
        neighbors = self.model.grid.neighbor_iter(self.pos)
        for neighbor in neighbors:
            distance += np.abs(neighbor.character - self.character)
        avg_distance = distance / 8
        if avg_distance > self.model.tolerance:
            self.model.grid.move_to_empty(self)
        else:
            self.model.happy += 1


class SchellingModel(Model):

    def __init__(self, height, width, tolerance, population):
        self.height = height
        self.width = width
        self.tolerance = tolerance
        self.population = population
        self.happy = 0

        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(height, width, torus=False)
        self.running = True
        self.setup()

    def setup(self):
        occupied = []
        for i in range(self.population):
            x = np.random.randint(0, self.width)
            y = np.random.randint(0, self.height)
            while [x, y] in occupied:
                x = np.random.randint(0, self.width)
                y = np.random.randint(0, self.height)
            occupied.append([x, y])
            agent = SchellingAgent((x, y), self)
            self.grid.position_agent(agent, (x, y))
            self.schedule.add(agent)

    def step(self):
        self.happy = 0  # Reset counter of happy agents
        self.schedule.step()
        if self.happy == self.schedule.get_agent_count():
            self.running = False