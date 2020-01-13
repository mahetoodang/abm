from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

import sys
sys.path.append('../')

from functionality.model import Friends


def draw_agent(agent):
    if agent is None:
        return
    portrayal = {
        "Filled": "true",
        "Layer": 0,
        "Color": "#" + ("%06x" % int(agent.character * 0x0000FF))
    }
    if agent.has_friends():
        portrayal["Shape"] = "rect"
        portrayal["w"] = 0.5
        portrayal["h"] = 0.5
    else:
        portrayal["Shape"] = "circle"
        portrayal["r"] = 0.5
    return portrayal


canvas_element = CanvasGrid(draw_agent, 20, 20, 500, 500)
server = ModularServer(Friends, [canvas_element], "Making friends")
server.launch()
