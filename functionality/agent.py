from mesa import Agent
import random
import numpy as np
import math
from .path_finder import find_path

class Human(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos
        self.home = pos
        self.max_travel = np.random.randint(9, 14)
        self.character = random.random()
        self.interaction = False
        self.path = []

    def get_pos(self):
        return self.pos

    def get_character(self):
        return self.character

    def get_friends(self):
        others = self.model.friends_score[self.unique_id]
        ids = others[others > 0].index
        friends = []
        for agent in self.model.schedule.agents:
            if agent.unique_id in ids:
                friends.append(agent)
        return friends

    def get_distance(self, friend_pos):
        # returns euclidean distance to friend position
        return math.sqrt((self.pos[0] - friend_pos[0])**2 + (self.pos[1] - friend_pos[1])**2)

    def get_avg(self):
        friends = self.get_friends()

        count = len(friends)
        score_sum = 0
        social_sum = 0
        spatial_sum = 0

        if count == 0:
            avg_score = score_sum
            avg_social = social_sum
            avg_spatial = spatial_sum
        else:
            # Sum
            for friend in friends:
                #score_sum += self.model.friends_score[self.unique_id][friend.unique_id]
                score_sum += self.model.friends_score.at[self.unique_id, friend.unique_id]
                social_sum += abs(self.character - friend.character)
                spatial_sum += self.get_distance(friend.pos)

            # Average
            avg_score = score_sum/count
            avg_social = social_sum/count
            avg_spatial = spatial_sum/count

        return avg_score, avg_social, avg_spatial, count

    def step(self):
        if self.is_home():
            self.create_trip()
        if self.interaction and len(self.path):
            self.move()
        else:
            if not len(self.path):
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

                # social distance & suitability
                character_dist = abs(self.character - neighbor.character)
                suitability = 1 - np.abs(character_dist)
                ##print(suitability)
                if random.uniform(0, 0.6) < suitability:
                    self.model.friends[i][j] = 1
                    self.model.friends_score[i][j] += 1 + random.random() * suitability

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
        path = find_path([0, 0], destination, trip_length + 2)
        self.path = path

    def go_home(self):
        destination = self.relative_home_location()
        trip_length = np.abs(destination[0]) + np.abs(destination[1])
        path = find_path([0, 0], destination, trip_length + 2)
        self.path = path

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
