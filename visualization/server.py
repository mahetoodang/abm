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

'''
Mesa-based user interface for the FriendSim Agent Based model.
Ability to configure model parameters and visualise key statistics.
'''

# Setting model parameters
model_params = {
    "population_size": UserSettableParameter('slider', 'Population size', 1, 1, 500),
    "tolerance": UserSettableParameter('slider', 'Tolerance level', value=0.2, min_value=0, max_value=1, step=0.05),
    "social_extroversion": UserSettableParameter(
        'slider', 'Extroversion of society',
        value=0.4, min_value=0, max_value=1, step=0.05
    ),
    "decay": UserSettableParameter(
        'slider', 'Friendship decay speed',
        value=0.99, min_value=0.01, max_value=0.99, step=0.01
    ),
    "mobility": UserSettableParameter(
        'slider', 'Ratio of faster agents',
        value=0.5, min_value=0, max_value=1, step=0.05
    )
}

# Setting color maps
agent_cmap = cm.get_cmap('Greys', 255)
cell_cmap = cm.get_cmap('YlGn', 255)

# Defining agent portrayal
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
        if agent.speed == 2:
            portrayal["r"] = 0.6
        else:
            portrayal["r"] = 0.4

    elif type(agent) is Cell:
        color = colors.rgb2hex(cell_cmap(agent.value))
        portrayal["Color"] = color
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal

# Generating animated charts
friend_chart = ChartModule(
    [{"Label": "Friends score", "Color": "Black"}],
    data_collector_name='data_collector'
)

social_chart = ChartModule(
    [{"Label": "Friends distance", "Color": "Blue"}],
    data_collector_name='data_collector'
)

spatial_chart = ChartModule(
    [{"Label": "Friends spatial distance", "Color": "Red"}],
    data_collector_name='data_collector'
)

# Drawing the grid, initialising elements and launching server
canvas_element = CanvasGrid(draw_agent, 20, 20, 500, 500)

element_list = [canvas_element, friend_chart, social_chart, spatial_chart]

server = ModularServer(Friends, element_list, "Making friends", model_params)

server.launch()
