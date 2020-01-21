import numpy as np
import pandas as pd
import networkx as nx


def choose_speed(speed_dist):
    choice = np.random.random()
    if choice < speed_dist[0]:
        speed = 1
    elif choice < speed_dist[0] + speed_dist[1]:
        speed = 2
    else:
        speed = 3
    return speed


def create_segregation_centers(seg_number, width, height):
    if seg_number == 2:
        placements = [
            [int(0.8 * width), int(0.8 * height)],
            [int(0.2 * width), int(0.2 * height)]
        ]
    elif seg_number == 3:
        placements = [
            [int(0.8 * width), int(0.5 * height)],
            [int(0.2 * width), int(0.8 * height)],
            [int(0.2 * width), int(0.2 * height)]
        ]
    else:
        placements = []
    return placements


def create_sim_stats(schedule, M, file_name):
    sim_stats = pd.DataFrame()

    for agent in schedule.agents:
        nx.set_node_attributes(M, {(agent.unique_id - 1): {'character': agent.character}})
        score, social, spatial, count = agent.get_avg()
        stats = dict(
            agent_id=agent.unique_id,
            friend_count=count,
            avg_friend_score=score,
            avg_social_dist=social,
            avg_spatial_dist=spatial)

        sim_stats = sim_stats.append(stats, ignore_index=True)

    sim_stats.to_csv(file_name)
