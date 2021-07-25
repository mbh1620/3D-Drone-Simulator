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
		self.mode = 'ACRO'
		self.heading = heading
		self.wireframe = wireframe.Wireframe()
		
		self.vertical_velocity = 0
		self.horizontal_velocity = 0

		a = np.array([[-250,0,0],[250,0,0], [0,0,250], [0,0,-250], [1000, 0, 0], [0, 1000, 0], [0, 0, 1000], [0,0,0]])

		self.wireframe.addNodes(a)
		self.wireframe.addEdges([(0,1), (2,3)])
		self.wireframe.addEdges([(4,7), (5,7), (6,7)])

		self.current_roll_error = 0
		self.proportional = 0
		self.integral = 0
		self.differential = 0

		self.current_tilt_error = 0

		self.t_proportional = 0
		self.t_integral = 0
		self.t_differential = 0

		self.stabilise_PID_controller()


	def Wireframe(self):
		return self.wireframe

	def increase_altitude(self, amount, camera):
		
		self.pos[0] += amount*math.sin(self.roll)
		self.pos[1] += amount*(math.cos(self.roll)*math.cos(self.pitch))
		self.pos[2] += amount*math.sin(self.pitch)
		# print('y increment')
		# print(amount*math.cos(self.roll))


		wf = wireframe.Wireframe()

		matrix = wf.translationMatrix(self.pos[0]-camera.pos[0], self.pos[1]-camera.pos[1], self.pos[2]-camera.pos[2])

		self.wireframe.transform(matrix)

		self.yaw_('r', camera.hor_angle, camera)

		wf = wireframe.Wireframe()

		matrix = wf.translationMatrix(-amount*math.sin(self.roll),amount*(math.cos(self.roll)*math.cos(self.pitch)),amount*math.sin(self.pitch))
		
		self.wireframe.transform(matrix)

		self.yaw_('l', camera.hor_angle, camera)

		wf = wireframe.Wireframe()
		matrix = wf.translationMatrix(-self.pos[0]+camera.pos[0],-self.pos[1]+camera.pos[1],-self.pos[2]+camera.pos[2])

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

		matrix = wf.translationMatrix(camera.pos[0]+self.pos[0], -self.pos[1]+camera.pos[1], camera.pos[2]-self.pos[2])

		self.wireframe.transform(matrix)

		#Do Rotation
		wf = wireframe.Wireframe()
		
		matrix = wf.rotateXMatrix(amount)
		self.wireframe.transform(matrix)

		wf = wireframe.Wireframe()
		matrix = wf.translationMatrix(-camera.pos[0]-self.pos[0],self.pos[1]-camera.pos[1],-camera.pos[2]+self.pos[2])

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

	def tilt_drone_test(self, amount, camera):

		self.yaw_('r', camera.hor_angle, camera)
		self.tilt(amount, camera)
		self.yaw_('l', camera.hor_angle, camera)
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

		self.tilt(amount*math.sin(self.yaw-camera.hor_angle), camera)
		self.pitch_(-amount*math.cos(self.yaw-camera.hor_angle), camera)

		self.pitch += amount





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
		
		matrix = wf.rotateYMatrix(var*amount)
		self.wireframe.transform(matrix)

		wf = wireframe.Wireframe()
		matrix = wf.translationMatrix(-camera.pos[0]-self.pos[0],-camera.pos[1]+self.pos[1],-camera.pos[2]+self.pos[2])

		self.wireframe.transform(matrix)

		self.yaw -= var*amount
		

	def stabilise_PID_controller(self):

		#Controller used for auto level mode

		self.p1_parameter = 0.3
		self.i1_parameter = 0.01
		self.d1_parameter = 0.1

	def GPS_PID_controller(self, camera):

		#Controller used to stabilise waypoint positioning

		self.p2_parameter = 0
		self.i2_parameter = 0
		self.d2_parameter = 0

	def position_mode(self, camera):

		height = self.pos[1]

		#-----------------------------------
		#		Roll PID Controller
		#-----------------------------------

		self.prev_roll_error = self.current_roll_error

		self.current_roll_error = self.roll

		self.proportional = self.current_roll_error
		self.integral += self.current_roll_error
		self.differential = self.current_roll_error - self.prev_roll_error
		

		ROLL_PID_OUTPUT = (self.proportional*self.p1_parameter) + (self.integral*self.i1_parameter)+(self.differential*self.d1_parameter)

		#print(ROLL_PID_OUTPUT)

		self.tilt_drone_in_relation(ROLL_PID_OUTPUT, camera)

		
		#-----------------------------------
		#		Tilt PID Controller
		#-----------------------------------

		self.prev_tilt_error = self.current_tilt_error

		self.current_tilt_error = self.pitch

		self.t_proportional = self.current_tilt_error
		self.t_integral += self.current_tilt_error
		self.t_differential = self.current_tilt_error - self.prev_tilt_error


		TILT_PID_OUTPUT = (self.t_proportional*self.p1_parameter) + (self.t_integral*self.i1_parameter) + (self.t_differential*self.d1_parameter)

		#print(TILT_PID_OUTPUT)

		self.pitch_drone_in_relation(TILT_PID_OUTPUT, camera)





		pitch_error = 0 - self.pitch

		height_error = height - self.pos[1]








