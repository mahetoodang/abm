import numpy as np
from random import choice
from functools import reduce


def find_path(start_pos, end_pos, length, bounds=False):
    x = end_pos[0] - start_pos[0]
    y = end_pos[1] - start_pos[1]
    manhattan = np.abs(x) + np.abs(y)
    if (length < manhattan) or (length - manhattan) % 2 != 0:
        return False
    steps = []
    steps.extend([[int(np.sign(x) * 1), 0] for i in range(np.abs(x))])
    steps.extend([[0, int(np.sign(y)) * 1] for i in range(np.abs(y))])
    missing_steps = length - manhattan
    while missing_steps > 0:
        [all_same, init_step] = moves_of_same_type(steps)
        if not all_same:
            if np.random.random() < 0.5:
                steps.append([1, 0])
                steps.append([-1, 0])
            else:
                steps.append([0, 1])
                steps.append([0, -1])
        else:
            if init_step[0] == 0:
                steps.append([1, 0])
                steps.append([-1, 0])
            else:
                steps.append([0, 1])
                steps.append([0, -1])
        missing_steps -= 2
    return non_overlapping_path(steps, [], bounds)


def non_overlapping_path(steps, path, bounds):
    remaining = list(map(list, steps))
    if not len(remaining):
        return path
    move_options = possible_options(remaining)
    while len(move_options):
        move = choice(move_options)
        move_options.remove(move)
        new_path = list(map(list, path))
        new_path.append(move)
        not_overlapping = not does_overlap(new_path)
        if bounds:
            in_bounds = not out_of_bounds(new_path, bounds)
        else:
            in_bounds = True
        if not_overlapping and in_bounds:
            try_remaining = list(map(list, remaining))
            try_remaining.remove(move)
            found_path = non_overlapping_path(try_remaining, new_path, bounds)
            if found_path:
                return found_path
    return False


def moves_of_same_type(steps):
    init_step = steps[0]
    all_same = True
    for step in steps:
        if step[0] != init_step[0] or step[1] != init_step[1]:
            all_same = False
            break
    return [all_same, init_step]


def possible_options(remaining):
    cardinals = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    possible = []
    for c in cardinals:
        for dir in remaining:
            if c[0] == dir[0] and c[1] == dir[1]:
                possible.append(c)
                break
    return possible


def does_overlap(steps):
    pos = [0, 0]
    path = [[0, 0]]
    for step in steps:
        pos = [
            pos[0] + step[0],
            pos[1] + step[1]
        ]
        for [x, y] in path:
            if x == pos[0] and y == pos[1]:
                return True
        path.append(pos)
    return False


def out_of_bounds(path, bounds):
    pos = reduce(lambda a, b: [a[0] + b[0], a[1] + b[1]], path)
    x_out = pos[0] < bounds[0][0] or pos[0] > bounds[1][0]
    y_out = pos[1] < bounds[0][1] or pos[1] > bounds[1][1]
    return x_out or y_out


if __name__ == '__main__':
    bounds = [[0, 0], [30, 30]]
    steps = find_path([0, 0], [40, 40], 70, bounds)
    pos = [0, 0]
    #for step in steps:
    #    pos = [
    #        pos[0] + step[0],
    #        pos[1] + step[1]
    #    ]
    #    print(pos)
