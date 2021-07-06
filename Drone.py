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

		a = np.array([[-250,0,0],[250,0,0], [0,0,250], [0,0,-250], [1000, 0, 0], [0, 1000, 0], [0, 0, 1000], [0,0,0]])

		self.wireframe.addNodes(a)
		self.wireframe.addEdges([(0,1), (2,3)])
		self.wireframe.addEdges([(4,7), (5,7), (6,7)])


	def Wireframe(self):
		return self.wireframe

	def increase_altitude(self, amount, camera):
		
		self.pos[0] += amount*math.sin(self.roll)
		self.pos[1] += amount*(math.cos(self.roll)*math.cos(self.pitch))
		self.pos[2] += amount*math.sin(self.pitch)
		# print('y increment')
		# print(amount*math.cos(self.roll))


		wf = wireframe.Wireframe()

		matrix = wf.translationMatrix(camera.pos[0]-self.pos[0], camera.pos[1]-self.pos[1], self.pos[2]-camera.pos[2])

		self.wireframe.transform(matrix)

		wf = wireframe.Wireframe()

		matrix = wf.rotateYMatrix(-camera.hor_angle)

		self.wireframe.transform(matrix)

		wf = wireframe.Wireframe()

		matrix = wf.translationMatrix(-amount*math.sin(self.roll),amount*(math.cos(self.roll)*math.cos(self.pitch)),amount*math.sin(self.pitch))
		
		self.wireframe.transform(matrix)

		wf = wireframe.Wireframe()

		matrix = wf.rotateYMatrix(camera.hor_angle)

		self.wireframe.transform(matrix)

		wf = wireframe.Wireframe()
		matrix = wf.translationMatrix(-camera.pos[0]+self.pos[0],-camera.pos[1]+self.pos[1],self.pos[2]+camera.pos[2])

		self.wireframe.transform(matrix)

		self.vertical_velocity = amount * math.cos(self.roll)

	def decrease_altitude(self, amount):
		wf = wireframe.Wireframe()
		self.pos[1] -= amount
		self.vertical_velocity = -amount
		matrix = wf.translationMatrix(0,-amount,0)
		self.wireframe.transform(matrix)

	def pitch_(self, amount, camera):
	
		

		wf = wireframe.Wireframe()

		matrix = wf.translationMatrix(camera.pos[0], camera.pos[1]-self.pos[1], camera.pos[2]-self.pos[2])

		self.wireframe.transform(matrix)

		#Do Rotation
		wf = wireframe.Wireframe()
		
		matrix = wf.rotateXMatrix(amount)
		self.wireframe.transform(matrix)

		wf = wireframe.Wireframe()
		matrix = wf.translationMatrix(-camera.pos[0],-camera.pos[1]+self.pos[1],-camera.pos[2]+self.pos[2])

		self.wireframe.transform(matrix)

		

	def tilt(self, amount, camera):

		theta = math.pi - camera.hor_angle

		wf = wireframe.Wireframe()

		matrix = wf.translationMatrix(camera.pos[0]+self.pos[0], -self.pos[1]+camera.pos[1], -self.pos[2]-camera.pos[2])

		self.wireframe.transform(matrix)

		#Do Rotation
		wf = wireframe.Wireframe()
		
		matrix = wf.rotateZMatrix(amount)

		# var*(1/30)*math.pi

		self.wireframe.transform(matrix)


		#Minus camera position

		wf = wireframe.Wireframe()

		matrix = wf.translationMatrix(-camera.pos[0]-self.pos[0],self.pos[1]-camera.pos[1],self.pos[2]+camera.pos[2])

		self.wireframe.transform(matrix)


		

	def tilt_drone_in_relation(self, amount, camera):
		#To tilt the drone depending on where the camera is we need to tilt and roll, this means that a combination of tilt and roll need to be added

		#tilt = amount*sin(camera.heading)
		#roll = amount*cos(camera.heading)

		self.tilt(amount*math.cos(self.yaw-camera.hor_angle), camera)
		self.pitch_(amount*math.sin(self.yaw-camera.hor_angle), camera)

		self.roll -=  amount

	def pitch_drone_in_relation(self, amount, camera):
		#To tilt the drone depending on where the camera is we need to tilt and roll, this means that a combination of tilt and roll need to be added

		#tilt = amount*sin(camera.heading)
		#roll = amount*cos(camera.heading)
		'''
		r = sqrt(x^2+y^2)

		x = camera_x_coord - drone_x_coord
		y = camera_z_coord - drone_z_coord

		'''

		a = (camera.pos[0] - self.pos[0])**2
		b = (camera.pos[2] - self.pos[2])**2

		r = math.sqrt(a + b)

		self.tilt(amount*math.sin(camera.hor_angle), camera)
		self.pitch_(-amount*math.cos(camera.hor_angle), camera)

		self.pitch -= amount





	def yaw_(self, direction, amount, camera):

		if direction == 'l':
			var = 1
		else:
			var = -1

		wf = wireframe.Wireframe()

		matrix = wf.translationMatrix(camera.pos[0]+self.pos[0], camera.pos[1]-self.pos[1], camera.pos[2]-self.pos[2])

		self.wireframe.transform(matrix)

		#Do Rotation
		wf = wireframe.Wireframe()
		
		matrix = wf.rotateYMatrix(var*(1/30)*math.pi)
		self.wireframe.transform(matrix)

		wf = wireframe.Wireframe()
		matrix = wf.translationMatrix(-camera.pos[0]-self.pos[0],-camera.pos[1]+self.pos[1],-camera.pos[2]+self.pos[2])

		self.wireframe.transform(matrix)

		self.yaw -= var*(1/30)*math.pi
		

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



