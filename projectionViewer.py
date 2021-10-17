from wireframe import *
import pygame
import numpy as np
import math
from camera import *
import time

class ProjectionViewer:

	''' Displays 3D Objects on a Pygame Screen '''

	def __init__(self, width, height, center_point, drone):
		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode((width, height))
		pygame.display.set_caption('Wireframe Display')
		self.background = (10,10,50)

		self.drone = drone

		#Setup camera
		self.camera = Camera([-1200,-1000,0],0,0)
		self.center_point = center_point


		self.wireframes = {}
		self.displayNodes = False
		self.displayEdges = True
		self.nodeColour = (255,255,255)
		self.edgeColour = (200,200,200)
		self.nodeRadius = 4

		pygame.init()

	def run(self):

		key_to_function = {
		pygame.K_LEFT: (lambda x: x.rotate_about_camera('Y', 0.05)),
 		pygame.K_RIGHT:(lambda x: x.rotate_about_camera('Y', -0.05)),


 		pygame.K_w: (lambda x: x.move_cam_forward(20)),
 		pygame.K_s: (lambda x: x.move_cam_backward(20)),
 		pygame.K_a: (lambda x: x.move_cam_left(20)),
 		pygame.K_d: (lambda x: x.move_cam_right(20)),
 		pygame.K_UP: (lambda x: x.move_cam_up(10)),
 		pygame.K_DOWN: (lambda x: x.move_cam_down(10)),

		pygame.K_EQUALS: (lambda x: x.scale_centre([1.25,1.25,1.25])),
		pygame.K_MINUS: (lambda x: x.scale_centre([0.8,0.8,0.8])),

		pygame.K_q: (lambda x: x.rotateAll('X', 0.1)),
		pygame.K_z: (lambda x: x.rotateAll('Z', 0.1)),
		pygame.K_x: (lambda x: x.rotateAll('Z', -0.1)),
		
		

		pygame.K_u: (lambda x: x.drone_up()),
		pygame.K_j: (lambda x: x.drone_down()),
		pygame.K_h: (lambda x: x.drone_left()),
		pygame.K_k: (lambda x: x.drone_right()),
		pygame.K_y: (lambda x: x.drone_forward()),
		pygame.K_i: (lambda x: x.drone_backward()),
		pygame.K_o: (lambda x: x.drone_yaw('l')),
		pygame.K_p: (lambda x: x.drone_yaw('r')),

		pygame.K_m: (lambda x: x.mode())

		}


		running = True
		flag = False

		while running:

			keys = pygame.key.get_pressed()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

				
				
			if keys[pygame.K_LEFT]:
				key_to_function[pygame.K_LEFT](self)
			if keys[pygame.K_RIGHT]:
				key_to_function[pygame.K_RIGHT](self)
			if keys[pygame.K_DOWN]:
				key_to_function[pygame.K_DOWN](self)
			if keys[pygame.K_UP]:
				key_to_function[pygame.K_UP](self)
			if keys[pygame.K_EQUALS]:
				key_to_function[pygame.K_EQUALS](self)
			if keys[pygame.K_MINUS]:
				key_to_function[pygame.K_MINUS](self)
			if keys[pygame.K_LEFT]:
				key_to_function[pygame.K_LEFT](self)
			if keys[pygame.K_q]:
				key_to_function[pygame.K_q](self)
			if keys[pygame.K_w]:
				key_to_function[pygame.K_w](self)
			if keys[pygame.K_a]:
				key_to_function[pygame.K_a](self)
			if keys[pygame.K_s]:
				key_to_function[pygame.K_s](self)
			if keys[pygame.K_z]:
				key_to_function[pygame.K_z](self)
			if keys[pygame.K_x]:
				key_to_function[pygame.K_x](self)
			if keys[pygame.K_t]:
				key_to_function[pygame.K_t](self)
			if keys[pygame.K_d]:
				key_to_function[pygame.K_d](self)

			if keys[pygame.K_u]:
				key_to_function[pygame.K_u](self)
			if keys[pygame.K_h]:
				key_to_function[pygame.K_h](self)
			if keys[pygame.K_j]:
				key_to_function[pygame.K_j](self)
			if keys[pygame.K_k]:
				key_to_function[pygame.K_k](self)
			if keys[pygame.K_y]:
				key_to_function[pygame.K_y](self)
			if keys[pygame.K_i]:
				key_to_function[pygame.K_i](self)

			if keys[pygame.K_o]:
				key_to_function[pygame.K_o](self)
			if keys[pygame.K_p]:
				key_to_function[pygame.K_p](self)
			if keys[pygame.K_m]:
				key_to_function[pygame.K_m](self)


			self.display()
			self.drone_physics()
			pygame.display.flip()


			if self.drone.mode == "POS" and keys[pygame.K_h] == 0 and keys[pygame.K_k] == 0:
				self.drone.position_mode(self.camera)

	def addWireframe(self, name, wireframe):
		self.wireframes[name] = wireframe
		#translate to center
		wf = Wireframe()
		matrix = wf.translationMatrix(-self.width/2,-self.height/2,0)

		for wireframe in self.wireframes.values():
			wireframe.transform(matrix)

		

		wf = Wireframe()
		matrix = wf.translationMatrix(self.width,self.height,0)

		for wireframe in self.wireframes.values():
			wireframe.transform(matrix)


		

	def display(self):

		self.screen.fill(self.background)

		for wireframe in self.wireframes.values():
			wireframe.transform_for_perspective((self.width/2, self.height/2), self.camera.fov, self.camera.zoom)	

			if self.displayNodes == True:
				for node in wireframe.perspective_nodes:
					if node[2] > 0 and node[2] < 10000 and node[0] > 0 and node[0] < 1199:
						pygame.draw.circle(self.screen, self.nodeColour, (int(node[0]), int(node[1])), self.nodeRadius, 0)
			else:
				pass
			if self.displayEdges:
				for n1, n2 in wireframe.edges:
					if wireframe.perspective_nodes[n1][2] > 0 and wireframe.perspective_nodes[n2][2] > 0 and wireframe.perspective_nodes[n1][2] < 10000 and wireframe.perspective_nodes[n1][0] > 0 and wireframe.perspective_nodes[n1][0] < 1199 :
						pygame.draw.aaline(self.screen, self.edgeColour, wireframe.perspective_nodes[n1][:2], wireframe.perspective_nodes[n2][:2], 1)



	def translateAll(self, vector):
		''' Translate all wireframes along a given axis by d units '''
		wf = Wireframe()
		matrix = wf.translationMatrix(*vector)
		for wireframe in self.wireframes.values():
			wireframe.transform(matrix)

	def scaleAll(self, vector):
		wf = Wireframe()
		matrix = wf.scaleMatrix(*vector)

		for wireframe in self.wireframes.values():
			wireframe.transform(matrix)

	def rotateAll(self, axis, theta):

		wf = Wireframe()
		if axis == 'X':
			matrix = wf.rotateXMatrix(theta)
		elif axis == 'Y':
			matrix = wf.rotateYMatrix(theta)
		elif axis == 'Z':
			matrix = wf.rotateZMatrix(theta)

		for wireframe in self.wireframes.values():
			wireframe.transform(matrix)
			#wireframe.transform_for_perspective()


	def rotate_about_Center(self, Axis, theta):

		#First translate Centre of screen to 0,0

		wf = Wireframe()
		matrix = wf.translationMatrix(-self.width/2,-self.height/2,0)

		for wireframe in self.wireframes.values():
			wireframe.transform(matrix)

		#Do Rotation
		wf = Wireframe()
		if Axis == 'X':
			matrix = wf.rotateXMatrix(theta)
		elif Axis == 'Y':
			matrix = wf.rotateYMatrix(theta)
		elif Axis == 'Z':
			matrix = wf.rotateZMatrix(theta)

		for wireframe in self.wireframes.values():
			wireframe.transform(matrix)
		

		#Translate back to centre of screen

		wf = Wireframe()
		matrix = wf.translationMatrix(self.width/2,self.height/2,0)

		for wireframe in self.wireframes.values():
			wireframe.transform(matrix)

	def rotate_about_camera(self, Axis, theta):

		wf = Wireframe()

		matrix = wf.translationMatrix(-self.width/2, -self.height/2,0)

		for wireframe in self.wireframes.values():
			wireframe.transform(matrix)

		#Do Rotation
		wf = Wireframe()
		if Axis == 'X':
			matrix = wf.rotateXMatrix(theta)
		elif Axis == 'Y':
			matrix = wf.rotateYMatrix(theta)
		elif Axis == 'Z':
			matrix = wf.rotateZMatrix(theta)

		for wireframe in self.wireframes.values():
			wireframe.transform(matrix)
		

		#Translate back to original position

		wf = Wireframe()
		matrix = wf.translationMatrix(self.width/2,self.height/2,0)

		for wireframe in self.wireframes.values():
			wireframe.transform(matrix)


		

		if self.camera.hor_angle >= 2*math.pi:
			self.camera.hor_angle -= 2*math.pi
		elif self.camera.hor_angle < -2*math.pi:
			self.camera.hor_angle += 2*math.pi

		self.camera.define_render_space()
		self.camera.hor_angle += theta
		self.camera.set_position(self.center_point)
		print(self.camera.pos)

		#Update the position of the drone here!

		# a = (self.camera.pos[0] - self.drone.pos[0])**2
		# b = (self.camera.pos[2] - self.drone.pos[2])**2
		# r = math.sqrt(a+b)

		# self.drone.pos[0] = r*math.cos(self.camera.hor_angle)
		# self.drone.pos[2] = r*math.sin(self.camera.hor_angle)
		
		


	def scale_centre(self, vector):

		#Transform center of screen to origin

		wf = Wireframe()
		matrix = wf.translationMatrix(-self.width/2,-self.height/2,0)

		for wireframe in self.wireframes.values():
			wireframe.transform(matrix)

		#Scale the origin by vector

		wf = Wireframe()
		matrix = wf.scaleMatrix(*vector)

		for wireframe in self.wireframes.values():
			wireframe.transform(matrix)

		wf = Wireframe()
		matrix = wf.translationMatrix(self.width/2,self.height/2,0)

		for wireframe in self.wireframes.values():
			wireframe.transform(matrix)

	def move_cam_forward(self, amount):
		#Moving the camera forward will be a positive translation in the z axis for every other object.
		
		self.camera.define_render_space()
		self.translateAll([0,0,-amount])
		self.camera.set_position(self.center_point)
		print("Camera position: ")
		print(self.camera.pos)

	def move_cam_backward(self, amount):
		
		self.camera.define_render_space()
		self.translateAll([0,0,amount])
		self.camera.set_position(self.center_point)
		print("Camera position: ")
		print(self.camera.pos)

	def move_cam_left(self, amount):
		
		self.camera.define_render_space()
		self.translateAll([-amount,0,0])
		self.camera.set_position(self.center_point)
		print("Camera position: ")
		print(self.camera.pos)

	def move_cam_right(self, amount):
		
		self.camera.define_render_space()
		self.translateAll([amount,0,0])
		self.camera.set_position(self.center_point)
		print("Camera position: ")
		print(self.camera.pos)

	def move_cam_up(self, amount):
		
		self.camera.define_render_space()
		self.translateAll([0,-amount,0])
		self.camera.set_position(self.center_point)

	def move_cam_down(self, amount):
		
		self.camera.define_render_space()
		self.translateAll([0,amount,0])
		self.camera.set_position(self.center_point)

	def Toggle_Nodes(self):
		if self.displayNodes == True:
			self.displayNodes = False
		else:
			self.displayNodes = True

	def drone_up(self):
		self.drone.increase_altitude(20, self.camera)

	def drone_down(self):
		self.drone.decrease_altitude(10)

	def drone_left(self):
		# drone_Centre = pos1+pos1 / 2
		
		# self.drone.tilt((1/30)*math.pi, self.camera)
		prev = self.camera.hor_angle
		self.rotate_about_camera('Y', -self.camera.hor_angle)
		self.drone.tilt_drone_in_relation((1/30)*math.pi, self.camera)
		self.rotate_about_camera('Y', prev)

	def drone_right(self):
		# self.drone.tilt(-1*(1/30)*math.pi, self.camera)
		prev = self.camera.hor_angle
		self.rotate_about_camera('Y', -self.camera.hor_angle)
		self.drone.tilt_drone_in_relation(-(1/30)*math.pi, self.camera)
		self.rotate_about_camera('Y', prev)

	def drone_forward(self):
		prev = self.camera.hor_angle
		self.rotate_about_camera('Y', -self.camera.hor_angle)
		self.drone.pitch_drone_in_relation(-(1/30)*math.pi, self.camera)
		self.rotate_about_camera('Y', prev)

	def drone_backward(self):
		prev = self.camera.hor_angle
		self.rotate_about_camera('Y', -self.camera.hor_angle)
		self.drone.pitch_drone_in_relation((1/30)*math.pi, self.camera)
		self.rotate_about_camera('Y', prev)

	def drone_yaw(self, direction):
		prev = self.camera.hor_angle
		self.rotate_about_camera('Y', -self.camera.hor_angle)
		self.drone.yaw_(direction, (1/30)*math.pi, self.camera)
		self.rotate_about_camera('Y', prev)

	def drone_physics(self):
		#Drone Gravity
		#always decrease altiude with a acceleration
		if self.drone.pos[1] <= 0:
			pass
		else:
			self.drone.vertical_velocity -= 1
			self.drone.velocity[0] = self.drone.velocity[0] * 0.999 # <--- Drag coefficient x 
			self.drone.velocity[2] = self.drone.velocity[2] * 0.999 # <--- Drag coefficient z
			self.drone.decrease_altitude(-self.drone.vertical_velocity, self.camera, self.drone.velocity[0], self.drone.velocity[2])

		#Blit to screen drone roll angle, pitch angle and yaw angle
		font = pygame.font.Font('freesansbold.ttf', 20)
		text = font.render(f'Roll: {(self.drone.roll/(2*math.pi))*360:.2f}', True, (255,255,255),(self.background))
		textRect = text.get_rect()
		textRect.center = (1100, 50)
		self.screen.blit(text, textRect)

		font = pygame.font.Font('freesansbold.ttf', 20)
		text = font.render(f'Pitch: {(self.drone.pitch/(2*math.pi))*360:.2f}', True, (255,255,255),(self.background))
		textRect = text.get_rect()
		textRect.center = (1100, 75)
		self.screen.blit(text, textRect)

		font = pygame.font.Font('freesansbold.ttf', 20)
		text = font.render(f'Yaw: {(self.drone.yaw/(2*math.pi))*360:.2f}', True, (255,255,255),(self.background))
		textRect = text.get_rect()
		textRect.center = (1100, 100)
		self.screen.blit(text, textRect)

		font = pygame.font.Font('freesansbold.ttf', 20)
		text = font.render(f'Flight Mode: {self.drone.mode}', True, (255,255,255),(self.background))
		textRect = text.get_rect()
		textRect.center = (1100, 125)
		self.screen.blit(text, textRect)


		font = pygame.font.Font('freesansbold.ttf', 20)
		text = font.render(f'Camera Angle: {self.camera.hor_angle/(2*math.pi)*360:.2f}', True, (255,255,255),(self.background))
		textRect = text.get_rect()
		textRect.center = (1100, 150)
		self.screen.blit(text, textRect)


		font = pygame.font.Font('freesansbold.ttf', 20)
		text = font.render(f'POS(X,Y,Z): {self.drone.pos[0]:.2f}, {self.drone.pos[1]:.2f}, {self.drone.pos[2]:.2f}', True, (255,255,255),(self.background))
		textRect = text.get_rect()
		textRect.center = (1000, 175)
		self.screen.blit(text, textRect)

		font = pygame.font.Font('freesansbold.ttf', 20)
		text = font.render(f'VELOCITY(X,Y,Z): {self.drone.velocity[0]:.2f}, {self.drone.velocity[1]:.2f}, {self.drone.velocity[2]:.2f}', True, (255,255,255),(self.background))
		textRect = text.get_rect()
		textRect.center = (1000, 200)
		self.screen.blit(text, textRect)

	def mode(self):

		if self.drone.mode == 'ACRO':
			self.drone.mode = 'POS'
			print('changed mode to POS')
			
		elif self.drone.mode == 'POS':
			self.drone.mode = 'ACRO'
			print('changed mode to ACRO')

		
					








