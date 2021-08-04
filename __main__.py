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

cube_nodes = grid_generation(10000,10000,False)
cube_nodes[0] = [0,0,0]

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

pv.addWireframe('floormesh', cube)
pv.addWireframe('drone1', drone_wf)

wf = wireframe.Wireframe()
translate_drone = wf.translationMatrix(600,500,0)

drone_wf.transform(translate_drone)

pv.run()



