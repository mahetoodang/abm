from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import ChartModule
from matplotlib import cm, colors
import sys
sys.path.append('../')

from functionality.model import Friends
from functionality.agent import Human
from functionality.cell import Cell


model_params = {
    "population_size": UserSettableParameter('slider', 'Population size', 1, 1, 500),
    "segregation": UserSettableParameter('slider', 'Segregation level', value=0, min_value=0, max_value=1, step=0.05),
    "social_proximity": UserSettableParameter(
        'slider', 'Social proximity level',
        value=0, min_value=0, max_value=1, step=0.05
    )
}

agent_cmap = cm.get_cmap('Greys', 255)
cell_cmap = cm.get_cmap('YlGn', 255)


def draw_agent(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Human:
        color = colors.rgb2hex(agent_cmap(agent.character))
        portrayal["Color"] = color
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 1
        portrayal["Shape"] = "circle"
        if agent.speed == 3:
            portrayal["r"] = 0.6
        elif agent.speed == 2:
            portrayal["r"] = 0.45
        else:
            portrayal["r"] = 0.3

    elif type(agent) is Cell:
        color = colors.rgb2hex(cell_cmap(agent.value))
        portrayal["Color"] = color
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
