from mesa import Agent
import random
import numpy as np

from .path_finder import find_path
from .cell import Cell


class Human(Agent):
    '''
    Human class
    '''
    def __init__(self, unique_id, model, pos, character, speed):
        super().__init__(unique_id, model)
        self.pos = pos
        self.home = pos
        self.max_travel_time = np.random.randint(5, 10)
        self.speed = speed
        self.character = character
        self.interaction = False
        self.path = []
        self.destinations = self.find_possible_destionations()

    def step(self):
        '''
        Execute step (move/interact/create new trip/go home).
        '''

        # create new trip if home
        if self.is_home():
            self.create_trip()

        # move if interacting and trip not completed
        if self.interaction and len(self.path):
            self.move()
        # return home if trip completed
        else:
            if not len(self.path):
                self.go_home()

        # interact with neighbors if not yet interacting
        if not self.interaction:
            self.interact_with_neighbors()

        # move if still not interacting and trip not completed
        if not self.interaction and len(self.path):
            self.move()

    def get_friends(self):
        '''
        Returns list of friends.
        '''
        others = self.model.friends_score[self.unique_id]
        ids = others[others > 0].index
        friends = []
        for agent in self.model.schedule.agents:
            if agent.unique_id in ids:
                friends.append(agent)
        return friends

    def get_distance(self, point):
        '''
        Returns manhattan distance from current position to point on grid.
        '''

        return np.abs(self.pos[0] - point[0]) + np.abs(self.pos[1] - point[1])

    def get_avg(self):
        '''
        Returns average friends score, spatial distance, social distance.
        '''

        friends = self.get_friends()

        count = len(friends)
        score_sum = 0
        social_sum = 0
        spatial_sum = 0

        if not count:
            avg_score = score_sum
            avg_social = social_sum
            avg_spatial = spatial_sum
        else:
            for friend in friends:
                score_sum += self.model.friends_score.at[self.unique_id, friend.unique_id]
                social_sum += abs(self.character - friend.character)
                spatial_sum += self.get_distance(friend.pos)
            # Average
            avg_score = score_sum/count
            avg_social = social_sum/count
            avg_spatial = spatial_sum/count

        return avg_score, avg_social, avg_spatial, count

    def interact_with_neighbors(self):
        '''
        Interact with other Human agents on same cell.
        '''

        # get agents on current position
        neighbors = self.model.grid.get_cell_list_contents([self.pos])
        for neighbor in neighbors:

            # if other human agent on current position
            if self.unique_id != neighbor.unique_id and type(neighbor) is Human:

                # only the upper part of matrix is used, thus the ordering of indexes
                i = np.max([self.unique_id, neighbor.unique_id])
                j = np.min([self.unique_id, neighbor.unique_id])

                # social distance & suitability
                character_dist = abs(self.character - neighbor.character)
                suitability = 1 - np.abs(character_dist)
                social_introversion = 1 - self.model.social_extroversion

                # interact
                if random.uniform(social_introversion, 1) < suitability:
                    # reset 'last interaction' count (decay)
                    self.model.last_interaction.values[i-1,j-1] = 0
                    self.model.last_interaction.values[j-1, i-1] = 0

                    # update friends score
                    rand_suit = random.random() * suitability
                    self.model.friends_score.values[i-1, j-1] += rand_suit
                    self.model.friends_score.values[j-1, i-1] += rand_suit

                    # update cell values if running with social hubs
                    if self.model.hubs:
                        cell = self.get_cell()
                        cell.update(self.character, neighbor.character)

                self.model.interactions[i][j] += 1
                break

    def get_cell(self):
        '''
        Returns cell for current position
        '''

        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        for agent in this_cell:
            if type(agent) is Cell:
                return agent

    def create_trip(self):
        '''
        Generates path/trip to random destination.
        '''
        bounds = self.get_relative_bounds()

        # get all possible destination cells
        path = False
        while not path:
            cells = []
            for pos in self.destinations:
                this_cell = self.model.grid.get_cell_list_contents([pos])
                for agent in this_cell:
                    if type(agent) is Cell:
                        cells.append(agent)

            # weighted random choice based on cell value if running with social hubs
            if self.model.hubs:
                value_sum = sum((1 - abs(self.character - cell.value)) for cell in cells)
                w = [(1 - abs(self.character - cell.value)) / value_sum for cell in cells]
                selected_cell = random.choices(population=cells, weights=w, k=1)
                chosen_trip = selected_cell[0].pos
            else:
                selected_cell = random.choice(cells)
                chosen_trip = selected_cell.pos

            # find path to chosen destination
            destination = [
                chosen_trip[0] - self.pos[0],
                chosen_trip[1] - self.pos[1]
            ]
            trip_length = np.abs(destination[0]) + np.abs(destination[1])
            path = find_path([0, 0], destination, trip_length + 2, bounds)

        self.path = path

    def go_home(self):
        '''
        Generate path/trip from current location to home.
        '''

        bounds = self.get_relative_bounds()
        destination = self.relative_home_location()
        trip_length = np.abs(destination[0]) + np.abs(destination[1])
        path = find_path([0, 0], destination, trip_length + 2, bounds)
        self.path = path

    def has_friends(self):
        '''
        Returns True if agent has friends.
        '''

        friend_count = self.nr_friends()
        return friend_count > 0

    def nr_friends(self):
        '''
        Returns number of friends.
        '''

        friends_df = self.model.friends
        uid = self.unique_id
        friend_count = np.sum(friends_df[uid].values) + np.sum(friends_df.loc[uid].values)
        return friend_count

    def is_home(self):
        '''
        Returns True if agent is home.
        '''
        return self.pos[0] == self.home[0] and self.pos[1] == self.home[1]

    def relative_home_location(self):
        '''
        Returns location relative to home location.
        '''
        x = self.home[0] - self.pos[0]
        y = self.home[1] - self.pos[1]
        return [x, y]

    def move(self):
        '''
        Perform next move/stap in path.
        '''
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
        '''
        Returns grid bounds relative to current position.
        '''
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

    def is_inside(self, p, max_x, max_y):
        '''
        Checks if coordinate p is within grid.
        '''

        x_in = 0 <= p[0] <= max_x
        y_in = 0 <= p[1] <= max_y
        return x_in and y_in

    def find_manhattan_neighbors(self, radius):
        '''
        Returns coordinates of neighboring cells.
        '''

        neighbors = []
        pos = self.pos
        [max_x, max_y] = [self.model.grid.width - 1, self.model.grid.height - 1]
        for i in range(radius+1):
            if i != 0:
                p = [i + pos[0], radius - i + pos[1]]
                if self.is_inside(p, max_x, max_y):
                    neighbors.append(p)
                p = [-i + pos[0], radius - i + pos[1]]
                if self.is_inside(p, max_x, max_y):
                    neighbors.append(p)
                if (radius - i) != 0:
                    p = [i + pos[0], -(radius - i) + pos[1]]
                    if self.is_inside(p, max_x, max_y):
                        neighbors.append(p)
                    p = [-i + pos[0], -(radius - i) + pos[1]]
                    if self.is_inside(p, max_x, max_y):
                        neighbors.append(p)
            else:
                p = [i + pos[0], radius - i + pos[1]]
                if self.is_inside(p, max_x, max_y):
                    neighbors.append(p)
                p = [i + pos[0], -(radius - i) + pos[1]]
                if self.is_inside(p, max_x, max_y):
                    neighbors.append(p)
        return neighbors

    def find_possible_destionations(self):
        '''
        Returns coordinates of all possible destinations within range (based on
        speed and maximum travel time).
        '''

        min_trip_length = self.speed
        max_trip_length = self.speed * self.max_travel_time
        destinations = []
        for i in range(min_trip_length, max_trip_length):
            destinations.extend(self.find_manhattan_neighbors(i))
        return destinations

    def random_move(self):
        '''
        Execute random move.
        '''
        grid = self.model.grid
        neighborhood = grid.get_neighborhood(self.pos, True, radius=1)
        grid.move_agent(self, random.choice(neighborhood))
