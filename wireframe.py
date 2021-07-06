import math
import numpy as np

# class Node:

# 	def __init__(self, coordinates):

# 		self.x = coordinates[0]
# 		self.y = coordinates[1]
# 		self.z = coordinates[2]


# class Edge:

# 	def __init__(self, start, stop):
# 		self.start = start
# 		self.stop = stop

class Wireframe:

	def __init__(self):
		self.nodes = np.zeros((0,4))
		self.perspective_nodes = None
		self.edges = []

	def addNodes(self, node_array):

		ones_column = np.ones((len(node_array), 1))
		ones_added = np.hstack((node_array, ones_column))
		self.nodes = np.vstack((self.nodes, ones_added))
		

	def addEdges(self, edgeList):
		self.edges += edgeList

	def outputNodes(self):
		print("\n --- Nodes ---")

		for i, (x, y, z, _) in enumerate(self.nodes):
			print(" %d: (%.2f, %.2f, %.2f)" % (i, node.x, node.y, node.z))

	def outputEdges(self):

		print("\n --- Edges ---")

		for i, (node1, node2) in enumerate(self.edges):
			print(" %d: %d -> %d" % (i, node1, node2))

	def translate(self, axis, d):
		if axis in ['x', 'y', 'z']:
			for node in self.nodes:
				setattr(node, axis, getattr(node, axis) + d)

	def scale(self, centre_x, centre_y, scale):

		for node in self.nodes:
			node.x = centre_x + scale * (node.x - centre_x)
			node.y = centre_y + scale * (node.y - centre_y)
			node.z *= scale

	def findCentre(self):

		num_nodes = len(self.nodes)
		meanX = sum([node.x for node in self.nodes]) / num_nodes
		meanY = sum([node.y for node in self.nodes]) / num_nodes
		meanZ = sum([node.z for node in self.nodes]) / num_nodes

		return (meanX, meanY, meanZ)

	def rotateZ(self, centre, radians):
		cx, cy, cz = centre

		for node in self.nodes:
			x = node.x - cx
			y = node.y - cy
			d = math.hypot(y,x)
			theta = math.atan2(y,x) + radians
			node.x = cx + d * math.cos(theta)
			node.y = cy + d * math.sin(theta)

	def rotateX(self, centre, radians):
		cx, cy, cz = centre
		for node in self.nodes:
			y = node.y - cy
			z = node.z - cz
			d = math.hypot(y,z)
			theta = math.atan2(y, z) + radians
			node.z = cz + d * math.cos(theta)
			node.y = cy + d * math.sin(theta)

	def rotateY(self, centre, radians):
		cx, cy, cz = centre
		for node in self.nodes:
			x = node.x - cx
			z = node.z - cz
			d = math.hypot(x, z)
			theta = math.atan2(x, z) + radians

			node.z = cz + d * math.cos(theta)
			node.x = cx + d * math.sin(theta)

	def transform(self, matrix):
		self.nodes = np.dot(self.nodes, matrix)

	def transform_for_perspective(self, center, fov, zoom):
		self.perspective_nodes = self.nodes.copy()
		for i in range(len(self.nodes)):
			node = self.nodes[i]
			p_node = self.perspective_nodes[i]
			# print(node[0], node[1], node[2])
			if node[2] != 0:
				p_node[0] = center[0] + (node[0]-center[0])*fov/(zoom-(node[2]))
				p_node[1] = center[1] + (node[1]-center[1])*fov/(zoom-(node[2]))
				p_node[2] = node[2] * 1
        

	def translationMatrix(self, dx=0, dy=0, dz=0):

		return np.array([[1,0,0,0],
						 [0,1,0,0],
						 [0,0,1,0],
						 [dx,dy,dz,1]])

	def scaleMatrix(self, sx=0, sy=0, sz=0):

		return np.array([[sx, 0, 0, 0], 
						 [0, sy, 0, 0],
						 [0, 0, sz, 0],
						 [0, 0, 0, 1]])

	def rotateXMatrix(self, radians):

		c = np.cos(radians)
		s = np.sin(radians)

		return np.array([[1,0,0,0],
						 [0,c,-s,0],
						 [0,s,c,0],
						 [0,0,0,1]])

	def rotateYMatrix(self, radians):

		c = np.cos(radians)
		s = np.sin(radians)

		return np.array([[c,0,s,0],
						 [0,1,0,0],
						 [-s,0,c,0],
						 [0,0,0,1]])

	def rotateZMatrix(self, radians):

		c = np.cos(radians)
		s = np.sin(radians)

		return np.array([[c,-s, 0, 0],
						 [s,c,0,0],
						 [0,0,1,0],
						 [0,0,0,1]])

	def movCamera(self, tilt, pan):

		return np.array([[1,0,0,200],
						 [0,1,0,0],
						 [pan,tilt,1,0],
						 [0,0,0,0]])


	def custom_matrix(matrix):

		return np.array(matrix)









	







