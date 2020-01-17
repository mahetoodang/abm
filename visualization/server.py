from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import ChartModule

import sys
sys.path.append('../')

from functionality.model import Friends

model_params = {"population_size": UserSettableParameter('slider', 'population_size', 1, 1, 10)}

def draw_agent(agent):
    if agent is None:
        return
    portrayal = {
        "Filled": "true",
        "Layer": 0,
        "Shape": "circle",
        "r": 0.5
    }
    if agent.has_friends():
        portrayal["Color"] = "Red"
    else:
        portrayal["Color"] = "Blue"
    return portrayal

friend_chart = ChartModule([{"Label":"Friends", "Color": "Black"}], data_collector_name='data_collector')

interaction_chart = ChartModule([{"Label":"Interactions", "Color": "Blue"}], data_collector_name='data_collector')

canvas_element = CanvasGrid(draw_agent, 20, 20, 500, 500)

element_list = [canvas_element, friend_chart, interaction_chart]

server = ModularServer(Friends, element_list, "Making friends", model_params)

server.launch()
