from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

import sys
sys.path.append('../')

from functionality.model import Friends


def draw_agent(agent):
    if agent is None:
        return
    portrayal = {
        "Shape": "circle",
        "r": 0.5,
        "Filled": "true",
        "Layer": 0
    }
    if agent.has_friends():
        portrayal["Color"] = "Red"
    else:
        portrayal["Color"] = "Blue"
    return portrayal


canvas_element = CanvasGrid(draw_agent, 20, 20, 500, 500)
server = ModularServer(Friends, [canvas_element], "Making friends")
server.launch()
