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

		self.desired_alt = 700
		
		self.vertical_velocity = 0
		self.horizontal_velocity = 0

		self.velocity = [0,0,0]

		a = np.array([[-250,0,-250],[250,0,250], [-250,0,250], [250,0,-250], [1000, 0, 0], [0, 1000, 0], [0, 0, 1000], [0,0,0]])

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

		self.current_alt_error = 0

		self.a_proportional = 0
		self.a_integral = 0
		self.a_differential = 0

		self.stabilise_PID_controller()

		self.waypoint_list = []

		self.active_waypoint = None

		#waypoint constants
		self.wp_max_pitch_angle = 60 
		self.wp_max_speed = 30
		self.wp_max_yaw_speed = None
		self.wp_max_alt_climb = None

	def Wireframe(self):
		return self.wireframe

	def increase_altitude(self, amount, camera):

		a = (amount*math.sin(self.roll)*math.cos(-self.yaw)) + (-amount*math.sin(self.pitch)*math.sin(self.yaw))
		b = amount*(math.cos(self.roll)*math.cos(self.pitch))
		c = (amount*math.sin(self.pitch)*math.cos(self.yaw)) + (amount*math.sin(self.roll)*math.sin(self.yaw))
		
		self.pos[0] += a
		self.pos[1] += b
		self.pos[2] += c

		wf = wireframe.Wireframe()

		matrix = wf.translationMatrix(self.pos[0]-camera.pos[0], self.pos[1]-camera.pos[1], self.pos[2]-camera.pos[2])

		self.wireframe.transform(matrix)

		self.yaw_('r', camera.hor_angle, camera)

		wf = wireframe.Wireframe()

		matrix = wf.translationMatrix(-a,b,c)
		
		self.wireframe.transform(matrix)

		self.yaw_('l', camera.hor_angle, camera)

		wf = wireframe.Wireframe()
		matrix = wf.translationMatrix(-self.pos[0]+camera.pos[0],-self.pos[1]+camera.pos[1],-self.pos[2]+camera.pos[2])

		self.wireframe.transform(matrix)

		self.vertical_velocity = amount * math.cos(self.roll)

		self.velocity[0] = (amount*math.sin(self.roll)*math.cos(-self.yaw)) + (-amount*math.sin(self.pitch)*math.sin(self.yaw))
 
		self.velocity[1] = amount*(math.cos(self.roll)*math.cos(self.pitch))

		self.velocity[2] = (amount*math.sin(self.pitch)*math.cos(self.yaw)) + (amount*math.sin(self.roll)*math.sin(self.yaw)) 

	def decrease_altitude(self, amount, x=0, y=0, z=0):
		wf = wireframe.Wireframe()
		self.pos[0] += x
		self.pos[1] -= amount
		self.pos[2] += z
		self.vertical_velocity = -amount
		self.velocity[0] = x
		self.velocity[2] = z
		matrix = wf.translationMatrix(-x,-amount,-z)
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

		self.p2_parameter = 0.04
		self.i2_parameter = 0.01
		self.d2_parameter = 0.1

	def GPS_PID_controller(self, camera):

		#Controller used to stabilise waypoint positioning

		self.p2_parameter = 0
		self.i2_parameter = 0
		self.d2_parameter = 0

	def position_mode(self, camera):

		self.alt = self.pos[1]

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

		#-----------------------------------
		#		Tilt PID Controller
		#-----------------------------------

		self.prev_alt_error = self.current_alt_error

		self.current_alt_error = self.desired_alt - self.alt

		self.a_proportional = self.current_alt_error
		self.a_integral += self.current_alt_error
		self.a_differential = self.current_alt_error - self.prev_alt_error

		ALT_PID_OUTPUT = (self.a_proportional*self.p2_parameter) + (self.a_integral*self.i2_parameter) + (self.a_differential*self.d2_parameter)

		if ALT_PID_OUTPUT > 0:
			self.increase_altitude(ALT_PID_OUTPUT, camera)

	def yaw_PID(self, camera):
		#Implementation for PID controller for yaw
		pass

	def Add_Waypoint(self, x, y, z):
		wp = [x,y,z]
		waypoint_list.push(wp)

	def Remove_Waypoint(self):
		pass

	def Activate_next_Waypoint(self):
		active_waypoint = waypoint_list[0]


	def WayPoint_Mode(self, camera):

		#Get position of active waypoint and calculate heading towards waypoint

		#Point towards active Waypoint on a PID(sort out later)

		x_diff = (self.active_waypoint[0]-self.pos[0])**2
		z_diff = (self.active_waypoint[2]-self.pos[2])**2

		heading = math.atan(z_diff/x_diff)+self.yaw

		while((self.yaw - heading) % 360 != 0):
			self.yaw_('l', self.wp_max_yaw_speed, camera)

		#Now fly in that direction

		#Pitch forward and increase altitude

		self.pitch_drone_in_relation(20, camera)







		








