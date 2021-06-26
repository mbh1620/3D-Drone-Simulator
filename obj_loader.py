#OBJ file loader class
import wireframe
import numpy as np

class OBJ_loader:

	def __init__(self, filename):
		self.filename = filename

	def create_wireframe(self):

		f = open(self.filename, "r")

		

		array = []

		for i in f:
			#for each line in the file, check whether its a vertex
			if i[0] == 'v':
				#line is a vertex, so create a node
				i = i.split()

				array.append((float(i[1]), float(i[2]), float(i[3])))

		print(array)

		Object = wireframe.Wireframe()

		Object.addNodes(np.array(array))

		f.close()

		return Object
