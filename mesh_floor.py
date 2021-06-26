#Grid generator

def grid_generation(i_length, j_length, z_function):

	points = []

	for j in range(1,j_length,1000):

		for i in range(1,i_length,1000):
			
			'''
			
				X ------- X
				|		  |
		 		|		  |
				|		  |
				|		  |
				X ------- X

			'''

			points.append([i,0,j])

	return points