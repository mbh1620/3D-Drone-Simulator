from projectionViewer import ProjectionViewer 
import wireframe
import numpy as np
from obj_loader import OBJ_loader
import random
from mesh_floor import *
from building_generator import *
from Drone import *
import time

cube = wireframe.Wireframe()

# a = np.array([[0,0,0],[1000,0,0], [0,1000,0], [0,0,1000]])

# axes.addNodes(a)
# axes.addEdges([(0,1), (0,2), (0,3)])

cube_nodes = grid_generation(10000,10000,False)
cube_nodes[0] = [0,0,0]

# b = generate_points_for_building(5000, 7000)
# axes.addNodes(b)
# axes.addEdges([(0,1),(1,2),(2,3),(3,0),(0,4),(1,5),(2,6),(3,7),(4,5),(5,6),(6,7),(7,4)])

# c = generate_points_for_building(3000, 10000)
# axes.addNodes(c)
# axes.addEdges([(0+8,1+8),(1+8,2+8),(2+8,3+8),(3+8,0+8),(0+8,4+8),(1+8,5+8),(2+8,6+8),(3+8,7+8),(4+8,5+8),(5+8,6+8),(6+8,7+8),(7+8,4+8)])

# d = generate_points_for_building(1000, 4000)
# axes.addNodes(d)
# axes.addEdges([(0+16,1+16),(1+16,2+16),(2+16,3+16),(3+16,0+16),(0+16,4+16),(1+16,5+16),(2+16,6+16),(3+16,7+16),(4+16,5+16),(5+16,6+16),(6+16,7+16),(7+16,4+16)])


drone1 = Drone([0,0,0],0,0)

drone_wf = drone1.Wireframe()


print(len(cube_nodes))

a = np.array(cube_nodes)

cube.addNodes(a)
cube.addEdges([(n, n + 1) for n in range(0, 9, 1)])
cube.addEdges([(n, n + 1) for n in range(10, 19, 1)])
cube.addEdges([(n, n + 1) for n in range(20, 29, 1)])
cube.addEdges([(n, n + 1) for n in range(30, 39, 1)])
cube.addEdges([(n, n + 1) for n in range(40, 49, 1)])
cube.addEdges([(n, n + 1) for n in range(50, 59, 1)])
cube.addEdges([(n, n + 1) for n in range(60, 69, 1)])
cube.addEdges([(n, n + 1) for n in range(70, 79, 1)])
cube.addEdges([(n, n + 1) for n in range(80, 89, 1)])
cube.addEdges([(n, n + 1) for n in range(90, 99, 1)])

for i in range(0,10):
	cube.addEdges([(0+i,10+i),(10+i,20+i),(20+i,30+i),(30+i,40+i),(40+i,50+i),(50+i,60+i),(60+i,70+i),(70+i,80+i),(80+i,90+i)])
		

pv = ProjectionViewer(1200, 1000, cube, drone1)
# pv.addWireframe('object', Object)

pv.addWireframe('floormesh', cube)
pv.addWireframe('drone1', drone_wf)

wf = wireframe.Wireframe()
translate_drone = wf.translationMatrix(600,500,0)

drone_wf.transform(translate_drone)

pv.run()



