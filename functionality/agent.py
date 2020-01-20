from mesa import Agent
import random
import numpy as np

from .path_finder import find_path


class Human(Agent):
    def __init__(self, unique_id, model, pos, speed):
        super().__init__(unique_id, model)
        self.pos = pos
        self.home = pos
        self.max_travel_time = np.random.randint(5, 10)
        self.speed = speed
        self.max_travel = np.random.randint(9, 14)
        self.character = random.random()
        self.interaction = False
        self.path = []

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

    def get_distance(self, point):
        # returns manhattan distance to point
        return np.abs(self.pos[0] - point[0]) + np.abs(self.pos[1] - point[1])

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
                if random.uniform(0, 0.6) < suitability:
                    self.model.friends[i][j] = 1
                    rand_suit = random.random() * suitability
                    self.model.friends_score[i][j] += 1 + rand_suit
                    self.model.friends_score[j][i] += 1 + rand_suit

                self.model.interactions[i][j] += 1
                break

    def create_trip(self):
        bounds = self.get_relative_bounds()
        min_travel_time = 1
        path = False
        while not path:
            trip_time = np.random.randint(min_travel_time, self.max_travel_time)
            trip_length = self.speed * trip_time
            possible_trips = self.find_manhattan_neighbors(trip_length)
            chosen_trip = random.choice(possible_trips)
            destination = [
                chosen_trip[0] - self.pos[0],
                chosen_trip[1] - self.pos[1]
            ]
            path = find_path([0, 0], destination, trip_length + 2, bounds)
        self.path = path

    def go_home(self):
        bounds = self.get_relative_bounds()
        destination = self.relative_home_location()
        trip_length = np.abs(destination[0]) + np.abs(destination[1])
        path = find_path([0, 0], destination, trip_length + 2, bounds)
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
        i = 0
        while i < self.speed:
            if len(self.path):
                move = self.path.pop(0)
                new_pos = (
                    self.pos[0] + move[0],
                    self.pos[1] + move[1]
                )
                self.model.grid.move_agent(self, new_pos)
                i += 1
            else:
                break

    def get_relative_bounds(self):
        # returns [ [min_x, min_y], [max_x, max_y] ]
        # showing the moving limits of the agents
        [min_x, min_y] = [0, 0]
        [max_x, max_y] = [self.model.grid.width-1, self.model.grid.height-1]
        pos = self.pos
        bounds = [
            [min_x - pos[0], min_y - pos[1]],
            [max_x - pos[0], max_y - pos[1]]
        ]
        return bounds

    def find_manhattan_neighbors(self, radius):
        # constructs all possible destinations given manhattan radius
        neighborhood = []
        for i in range(radius+1):
            if i != 0:
                neighborhood.append([i, radius - i])
                neighborhood.append([-i, radius - i])
                if (radius - i) != 0:
                    neighborhood.append([i, -(radius - i)])
                    neighborhood.append([-i, -(radius - i)])
            else:
                neighborhood.append([i, radius - i])
                neighborhood.append([i, -(radius - i)])
        # translates relative coordinates to world coordinates and
        # filters out the ones that are out of bounds
        pos = self.pos
        [max_x, max_y] = [self.model.grid.width-1, self.model.grid.height-1]
        neighbors = []
        for n in neighborhood:
            p = [n[0] + pos[0], n[1] + pos[1]]
            x_in = 0 <= p[0] <= max_x
            y_in = 0 <= p[1] <= max_y
            if x_in and y_in:
                neighbors.append(p)
        return neighbors

    def random_move(self):
        grid = self.model.grid
        neighborhood = grid.get_neighborhood(self.pos, True, radius=1)
        grid.move_agent(self, random.choice(neighborhood))
