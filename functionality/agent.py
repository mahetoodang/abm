from mesa import Agent
import random
import numpy as np
from .path_finder import find_path

class Human(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos
        self.home = pos
        self.max_travel = np.random.randint(9, 14)
        self.character = {
            'attribute_one': random.uniform(0, 1),
            'attribute_two': random.uniform(0, 1)
        }
        self.interaction = False
        self.path = []

    def step(self):
        if self.is_home():
            self.create_trip()
        if self.interaction and len(self.path):
            self.move()
        else:
            self.go_home()

        if not self.interaction:
            self.interact_with_neighbors()

        if not self.interaction and len(self.path):
            self.move()

    def interact_with_neighbors(self):
        neighbors = self.model.grid.get_neighbors(self.pos, True, include_center=True, radius=0)
        for neighbor in neighbors:
            if self.unique_id != neighbor.unique_id:
                # only the upper part of matrix is used, thus the ordering of indexes
                i = np.max([self.unique_id, neighbor.unique_id])
                j = np.min([self.unique_id, neighbor.unique_id])
                character_vector = [i for i in self.character.values()]
                neighbour_character_vector = np.array([i for i in neighbor.character.values()])
                character_dist = np.linalg.norm(character_vector - neighbour_character_vector)
                suitability = 1 - np.abs(character_dist)
                ##print(suitability)
                if random.uniform(0, 0.6) < suitability:
                    self.model.friends[i][j] = 1
                    self.model.friends_score[i][j] += 1 + random.random() * suitability
                    self.interaction = True
                self.model.interactions[i][j] += 1
                break

    def create_trip(self):
        min_travel = 5
        trip_length = np.random.randint(min_travel, self.max_travel)
        x_len = np.random.randint(0, trip_length)
        y_len = trip_length - x_len
        x_dir = 1 if random.random() < 0.5 else -1
        y_dir = 1 if random.random() < 0.5 else -1
        destination = [x_dir * x_len, y_dir * y_len]
        self.path = find_path([0, 0], destination, trip_length + 2)

    def go_home(self):
        destination = self.relative_home_location()
        trip_length = np.abs(destination[0]) + np.abs(destination[1])
        self.path = find_path([0, 0], destination, trip_length + 2)

    def has_friends(self):
        friend_count = self.nr_friends()
        return friend_count > 0

    def nr_friends(self):
        friends_df = self.model.friends
        uid = self.unique_id
        friend_count = np.sum(friends_df[uid].values) + np.sum(friends_df.loc[uid].values)
        return friend_count

    def is_home(self):
        return self.pos[0] == self.home[0] and self.pos[1] == self.home[1]

    def relative_home_location(self):
        x = self.home[0] - self.pos[0]
        y = self.home[1] - self.pos[1]
        return [x, y]

    def move(self):
        move = self.path.pop()
        new_pos = (
            self.pos[0] + move[0],
            self.pos[1] + move[1]
        )
        self.model.grid.move_agent(self, new_pos)

    def random_move(self):
        grid = self.model.grid
        neighborhood = grid.get_neighborhood(self.pos, True, radius=1)
        grid.move_agent(self, random.choice(neighborhood))
