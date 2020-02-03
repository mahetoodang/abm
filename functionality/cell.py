from mesa import Agent

class Cell(Agent):
    '''
    Cell class for all cells on the grid that keeps track of the cells'
    coordinates and the current cell value (used for social hubs).
    '''
    def __init__(self, unique_id, model, pos, value):
        super().__init__(unique_id, model)
        self.pos = pos
        self.value = value

    def update(self, score1, score2):
        '''
        Update cell value to equal average of the passed in character scores.
        '''
        self.value = (score1 + score2)/2

    def step(self):
        '''
        Skip step.
        '''
        pass
