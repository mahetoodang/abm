from mesa import Agent
import random
import numpy as np

class Human(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos
        self.character = random.random()

    def step(self):
        self.random_move()
        neighbors = self.model.grid.get_neighbors(self.pos, True, include_center=True, radius=0)
        for neighbor in neighbors:
            if self.unique_id != neighbor.unique_id:
                # only the upper part of matrix is used, thus the ordering of indexes
                i = np.max([self.unique_id, neighbor.unique_id])
                j = np.min([self.unique_id, neighbor.unique_id])
                suitability = 1 - np.abs(self.character - neighbor.character)
                if random.random() < suitability:
                    self.model.friends[i][j] = 1
                self.model.interactions[i][j] += 1
            break

    def has_friends(self):
        friend_count = self.nr_friends()
        return friend_count > 0

    def nr_friends(self):
        friends_df = self.model.friends
        uid = self.unique_id
        friend_count = np.sum(friends_df[uid].values) + np.sum(friends_df.loc[uid].values)
        return friend_count

    def random_move(self):
        grid = self.model.grid
        neighborhood = grid.get_neighborhood(self.pos, True, radius=1)
        grid.move_agent(self, random.choice(neighborhood))