from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from matplotlib import cm, colors
import sys
sys.path.append('../')

from functionality.schelling import SchellingModel

'''
Schelling server test
'''

model_params = {
    "height": 20,
    "width": 20,
    "population": UserSettableParameter('slider', 'Population size', 1, 1, 500),
    "tolerance": UserSettableParameter('slider', 'Tolerance level', value=0.2, min_value=0, max_value=1, step=0.05),
}

c_map = cm.get_cmap('Greys', 255)


def draw_agent(agent):
    if agent is None:
        return
    portrayal = {}
    color = colors.rgb2hex(c_map(agent.character))
    portrayal["Color"] = color
    portrayal["Filled"] = "true"
    portrayal["Layer"] = 1
    portrayal["Shape"] = "circle"
    portrayal["r"] = 0.6
    return portrayal


canvas_element = CanvasGrid(draw_agent, 20, 20, 500, 500)

element_list = [canvas_element]

server = ModularServer(SchellingModel, element_list, "Schelling", model_params)

server.launch()
