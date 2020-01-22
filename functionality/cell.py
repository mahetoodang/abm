from mesa import Agent

class Cell(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos
        self.value = 0.5

    def update(self, score1, score2):
        self.value = (score1 + score2)/2

    def step(self):
        pass
