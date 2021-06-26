'''
building generator
'''
import numpy as np

def generate_points_for_building(x,y):
	

	b = np.array([[0+x,0,0],[1000+x,0,0], [1000+x,0,1000], [0+x,0,1000], [0+x,y,0],[1000+x,y,0], [1000+x,y,1000], [0+x,y,1000]])

	return b