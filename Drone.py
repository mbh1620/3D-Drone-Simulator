import wireframe
import numpy as np
import math
'''

Drone Object

'''
class Drone():

	def __init__(self, pos, alt, heading):
		self.pos = pos
		self.alt = alt
		self.roll = 0
		self.pitch = 0
		self.yaw = 0
		self.mode = 'Acro'
		self.heading = heading
		self.wireframe = wireframe.Wireframe()
		
		self.vertical_velocity = 0
		self.horizontal_velocity = 0

		a = np.array([[250,0,0],[250,0,500], [0,0,250], [500,0,250]])

		self.wireframe.addNodes(a)
		self.wireframe.addEdges([(0,1), (2,3)])

	def Wireframe(self):
		return self.wireframe

	def increase_altitude(self, amount, camera):
		
		self.pos[0] += amount*math.sin(self.roll)
		self.pos[1] += (amount*math.cos(self.roll))+(amount*math.cos(self.pitch))-30
		self.pos[2] += amount*math.sin(self.pitch)
		# print('y increment')
		# print(amount*math.cos(self.roll))

		wf = wireframe.Wireframe()

		matrix = wf.translationMatrix(-250+camera.pos[0]-self.pos[0], camera.pos[1]-self.pos[1], -250+camera.pos[2])

		self.wireframe.transform(matrix)

		wf = wireframe.Wireframe()

		matrix = wf.rotateYMatrix(-camera.hor_angle)

		self.wireframe.transform(matrix)

		wf = wireframe.Wireframe()

		matrix = wf.translationMatrix(-amount*math.sin(self.roll),(amount*math.cos(self.roll))+(amount*math.cos(self.pitch))-30,amount*math.sin(self.pitch))
		
		self.wireframe.transform(matrix)

		wf = wireframe.Wireframe()

		matrix = wf.rotateYMatrix(camera.hor_angle)

		self.wireframe.transform(matrix)

		wf = wireframe.Wireframe()
		matrix = wf.translationMatrix(250-camera.pos[0]+self.pos[0],-camera.pos[1]+self.pos[1],250-camera.pos[2])

		self.wireframe.transform(matrix)

		self.vertical_velocity = amount * math.cos(self.roll)

	def decrease_altitude(self, amount):
		wf = wireframe.Wireframe()
		self.pos[1] -= amount
		self.vertical_velocity = -amount
		matrix = wf.translationMatrix(0,-amount,0)
		self.wireframe.transform(matrix)

	def tilt_back(self, amount, camera):


		wf = wireframe.Wireframe()

		matrix = wf.translationMatrix(-250+camera.pos[0]-self.pos[0], camera.pos[1]-self.pos[1], -250+camera.pos[2]-self.pos[2])

		self.wireframe.transform(matrix)

		#Do Rotation
		wf = wireframe.Wireframe()
		
		matrix = wf.rotateXMatrix((1/30)*math.pi)
		self.wireframe.transform(matrix)

		wf = wireframe.Wireframe()
		matrix = wf.translationMatrix(250-camera.pos[0]+self.pos[0],-camera.pos[1]+self.pos[1],250-camera.pos[2]+self.pos[2])

		self.wireframe.transform(matrix)

		self.pitch -= (1/30)*math.pi



	def tilt_forward(self, amount, camera):
	
		

		wf = wireframe.Wireframe()

		matrix = wf.translationMatrix(-250+camera.pos[0], camera.pos[1]-self.pos[1], -250+camera.pos[2]-self.pos[2])

		self.wireframe.transform(matrix)

		#Do Rotation
		wf = wireframe.Wireframe()
		
		matrix = wf.rotateXMatrix(-(1/30)*math.pi)
		self.wireframe.transform(matrix)

		wf = wireframe.Wireframe()
		matrix = wf.translationMatrix(250-camera.pos[0],-camera.pos[1]+self.pos[1],250-camera.pos[2]+self.pos[2])

		self.wireframe.transform(matrix)

		self.pitch += (1/30)*math.pi

	def tilt_left(self, amount, camera):
		

		wf = wireframe.Wireframe()

		matrix = wf.translationMatrix(-250+camera.pos[0]+self.pos[0], camera.pos[1]-self.pos[1], -250+camera.pos[2])

		self.wireframe.transform(matrix)



		wf = wireframe.Wireframe()

		matrix = wf.rotateYMatrix(-camera.hor_angle)

		self.wireframe.transform(matrix)



		wf = wireframe.Wireframe()

		matrix = wf.translationMatrix((250*math.sin(camera.hor_angle))-(self.pos[0]*math.sin(camera.hor_angle)),0,0)

		self.wireframe.transform(matrix)


		#Do Rotation
		wf = wireframe.Wireframe()
		
		matrix = wf.rotateZMatrix((1/30)*math.pi)
		self.wireframe.transform(matrix)


		
		wf = wireframe.Wireframe()

		matrix = wf.translationMatrix((-250*math.sin(camera.hor_angle))+(self.pos[0]*math.sin(camera.hor_angle)),0,0)

		self.wireframe.transform(matrix)




		wf = wireframe.Wireframe()

		matrix = wf.rotateYMatrix(camera.hor_angle)

		self.wireframe.transform(matrix)




		wf = wireframe.Wireframe()
		matrix = wf.translationMatrix(250-camera.pos[0]-self.pos[0],-camera.pos[1]+self.pos[1],250-camera.pos[2])

		self.wireframe.transform(matrix)

		self.roll -= (1/30)*math.pi

	def tilt_right(self, amount, camera):
		

		wf = wireframe.Wireframe()

		matrix = wf.translationMatrix(-250+camera.pos[0]+self.pos[0], camera.pos[1]-self.pos[1], -250+camera.pos[2])

		self.wireframe.transform(matrix)



		wf = wireframe.Wireframe()

		matrix = wf.rotateYMatrix(-camera.hor_angle)

		self.wireframe.transform(matrix)



		wf = wireframe.Wireframe()

		matrix = wf.translationMatrix((250*math.sin(camera.hor_angle))-(self.pos[0]*math.sin(camera.hor_angle)),0,0)

		self.wireframe.transform(matrix)


		#Do Rotation
		wf = wireframe.Wireframe()
		
		matrix = wf.rotateZMatrix(-(1/30)*math.pi)
		self.wireframe.transform(matrix)


		
		wf = wireframe.Wireframe()

		matrix = wf.translationMatrix((-250*math.sin(camera.hor_angle))+(self.pos[0]*math.sin(camera.hor_angle)),0,0)

		self.wireframe.transform(matrix)




		wf = wireframe.Wireframe()

		matrix = wf.rotateYMatrix(camera.hor_angle)

		self.wireframe.transform(matrix)




		wf = wireframe.Wireframe()
		matrix = wf.translationMatrix(250-camera.pos[0]-self.pos[0],-camera.pos[1]+self.pos[1],250-camera.pos[2])

		self.wireframe.transform(matrix)

		self.roll += (1/30)*math.pi


	def yaw_left(self, amount, camera):
		pass

	def yaw_right(self, amount, camera):
		pass

	def stabilise_PID_controller(self, camera):

		#Controller used for auto level mode

		p_parameter = 0 
		i_parameter = 0
		d_parameter = 0

	def GPS_PID_controller(self, camera):

		#Controller used to stabilise waypoint positioning

		p_parameter = 0
		i_parameter = 0
		d_parameter = 0



