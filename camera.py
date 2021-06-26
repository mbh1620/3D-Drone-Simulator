import math
'''
Camera class

position
FOV
zoom 

'''


class Camera:

	def __init__(self, pos, hor_angle, ver_angle, fov=250, zoom=500):
		self.pos = pos
		self.fov = fov
		self.hor_angle = hor_angle
		self.ver_angle = ver_angle
		self.zoom = self.pos[2]
		self.back_straight_x = 0
		self.back_straight_z = 0

	def set_position(self, center_point):

		print(center_point)

		self.pos[0] = -center_point.nodes[0][0]
		self.pos[1] = -center_point.nodes[0][1]
		self.pos[2] = -center_point.nodes[0][2]

	def define_render_space(self):

		#So we want to only render objects that are within a bounding box infront of the camera
		back_limit = 1000 #The distance to the back limit from the camera
		back_limit_length = 100
		front_limit = 20 #The distance to the front limit from the camera
		# adding_x_val = back_limit*math.cos(self.hor_angle)
		# adding_z_val = back_limit*math.sin(self.hor_angle)

		self.back_straight_x = self.pos[0] + 100
		self.back_straight_z = self.pos[2] + 10000

		print("back_straight_x")
		print(self.back_straight_x)
		print("back_straight_z")
		print(self.back_straight_z)


