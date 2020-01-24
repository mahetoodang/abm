from mesa import Agent

class Cell(Agent):
    def __init__(self, unique_id, model, pos, value):
        super().__init__(unique_id, model)
        self.pos = pos
        self.value = value

    def update(self, score1, score2):
        self.value = (score1 + score2)/2

    def step(self):
        pass
