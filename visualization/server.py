from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import ChartModule



import sys
sys.path.append('../')

from functionality.model import Friends
from functionality.agent import Human
from functionality.cell import Cell


model_params = {
    "population_size": UserSettableParameter('slider', 'population_size', 1, 1, 500)
}


def draw_agent(agent):
    if agent is None:
        return

    '''
    portrayal = {
        "Filled": "true",
        "Layer": 0,
        "Shape": "circle",
        "r": 0.5
    }
    '''

    portrayal = {}

    if type(agent) is Human:
        if agent.has_friends():
            portrayal["Color"] = "Red"
        else:
            portrayal["Color"] = "Blue"

        portrayal["Filled"] = "true"
        portrayal["Layer"] = 1
        portrayal["Shape"] = "circle"
        portrayal["r"] = 0.5

    elif type(agent) is Cell:
        if agent.value < 0.25:
            portrayal["Color"] = "#00F800"
        elif agent.value < 0.5:
            portrayal["Color"] = "#00AA00"
        elif agent.value < 0.75:
            portrayal["Color"] = "#008300"
        else:
            portrayal["Color"] = "#005C00"

        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


friend_chart = ChartModule(
    [{"Label": "Friends", "Color": "Black"}],
    data_collector_name='data_collector'
)

interaction_chart = ChartModule(
    [{"Label": "Interactions", "Color": "Blue"}],
    data_collector_name='data_collector'
)

canvas_element = CanvasGrid(draw_agent, 20, 20, 500, 500)

element_list = [canvas_element, friend_chart, interaction_chart]

server = ModularServer(Friends, element_list, "Making friends", model_params)

server.launch()
