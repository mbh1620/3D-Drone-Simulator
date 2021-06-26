#test


import wireframe
import numpy as np

cube = wireframe.Wireframe()

cube_nodes = [(x, y, z) for x in (50, 250) for y in (50, 250) for z in (50, 250)]

print(cube_nodes)

cube.addNodes(np.array(cube_nodes))

print(cube.nodes)






