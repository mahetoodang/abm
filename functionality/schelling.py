import numpy as np

from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import SingleGrid


class SchellingAgent(Agent):
    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.pos = pos
        self.character = np.random.random()
        self.did_move = True

    def step(self):
        self.did_move = False
        cur_distance = self.get_cell_fit(self.pos, self.character)
        if cur_distance > self.model.tolerance:
            for pos in self.model.grid.empties:
                cell_dist = self.get_cell_fit(pos, self.character)
                if cell_dist < cur_distance:
                    self.model.grid.move_agent(self, pos)
                    self.did_move = True
                    break
        else:
            self.model.happy += 1

    def get_cell_fit(self, pos, character):
        distance = 0
        neighbors = self.model.grid.neighbor_iter(pos)
        for neighbor in neighbors:
            distance += np.abs(neighbor.character - character)
        avg_distance = distance / 8
        return avg_distance


class SchellingModel(Model):

    def __init__(self, height=20, width=20, tolerance=0.3, population=200):
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

    def happy_ratio(self):
        agents = self.schedule.agents
        return self.happy / len(agents)

    def step(self):
        self.happy = 0  # Reset counter of happy agents
        self.schedule.step()
        if self.happy_ratio() > 0.99:
            self.running = False


if __name__ == '__main__':
    md = SchellingModel(20, 20, 0.3, 200)
    for i in range(200):
        md.step()
    print(i)
    print(md.happy)