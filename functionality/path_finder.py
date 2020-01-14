import numpy as np


def find_path(start_pos, end_pos, length):
    x = end_pos[0] - start_pos[0]
    y = end_pos[1] - start_pos[1]
    manhattan = np.abs(x) + np.abs(y)
    if (length < manhattan) or (length - manhattan) % 2 != 0:
        return False
    steps = []
    for i in range(np.abs(x)):
        steps.append([np.sign(x) * 1, 0])
    for i in range(np.abs(y)):
        steps.append([0, np.sign(y) * 1])
    missing_steps = length - manhattan
    while missing_steps > 0:
        if np.random.random() < 0.5:
            steps.append([1, 0])
            steps.append([-1, 0])
        else:
            steps.append([0, 1])
            steps.append([0, -1])
        missing_steps -= 2
    return find_non_overlapping_order(steps)


def find_non_overlapping_order(steps):
    np.random.shuffle(steps)
    i = 0
    while does_overlap(steps):
        np.random.shuffle(steps)
        i += 1
    return steps


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


if __name__ == '__main__':
    steps = find_path([0, 0], [-10, 10], 26)
    pos = [0, 0]
    for step in steps:
        pos = [
            pos[0] + step[0],
            pos[1] + step[1]
        ]
        print(pos)
