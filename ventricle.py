import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math

def main():
	def y2x(y):
	    return np.sqrt(y/0.8)

	def set_axes_equal(ax):
	    '''Make axes of 3D plot have equal scale so that spheres appear as spheres,
	    cubes as cubes, etc..  This is one possible solution to Matplotlib's
	    ax.set_aspect('equal') and ax.axis('equal') not working for 3D.

	    Input
	      ax: a matplotlib axis, e.g., as output from plt.gca().
	    '''

	    x_limits = ax.get_xlim3d()
	    y_limits = ax.get_ylim3d()
	    z_limits = ax.get_zlim3d()

	    x_range = abs(x_limits[1] - x_limits[0])
	    x_middle = np.mean(x_limits)
	    y_range = abs(y_limits[1] - y_limits[0])
	    y_middle = np.mean(y_limits)
	    z_range = abs(z_limits[1] - z_limits[0])
	    z_middle = np.mean(z_limits)

	    # The plot bounding box is a sphere in the sense of the infinity
	    # norm, hence I call half the max range the plot radius.
	    plot_radius = 0.5*max([x_range, y_range, z_range])

	    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
	    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
	    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])

	#theta inclination angle
	#phi azimuthal angle
	n_theta = 50 # number of values for theta
	n_phi = 200  # number of values for phi
	r = 4        # radius of sphere
	theta, phi = np.mgrid[0.0:.5*np.pi:n_theta*1j, 0.0:2.0*np.pi:n_phi*1j]
	#bottom surface .5 * x.^2;
	x_b = r*np.sin(theta)*np.cos(phi)
	y_b = r*np.sin(theta)*np.sin(phi)
	z_b = .5*(x_b**2 + y_b**2)
	#upper surface 1 * x.^2 + 2
	r = np.sqrt(6)
	x_t = r*np.sin(theta)*np.cos(phi)
	y_t = r*np.sin(theta)*np.sin(phi)
	z_t = (x_t**2 + y_t**2)+2
	#Set colours and render
	fig = plt.figure(figsize=(10, 8))
	ax = fig.add_subplot(111, projection='3d')
	colors = np.empty(x_b.shape, dtype=object)
	for i in range(len(x_b)):
		colors[i] = 'lightskyblue'
		colors[i] = 'darkturquoise'
	ax.plot_surface(
	    x_b,y_b,z_b, alpha = .5, facecolors = colors, linewidth = 0) 

	# embedding for plotting
	num_rev = 2.4
	height = 6
	angles = np.linspace(.5 * math.pi, .5 * math.pi+ num_rev * 2 * math.pi, int(120 * num_rev))
	Z = height / 120 / num_rev * np.arange(120 * num_rev) + 0.5
	radi = y2x(Z)
	X = np.multiply(radi, np.sin(angles))
	Y = np.multiply(radi, np.cos(angles))
	Z = Z + 1.5
	output = 'T0; set temperature to 0\nG92 X0 Y0 Z0; set current position as home, go when start\n; Filament gcode\nG21 ; set units to millimeters\nG90 ; use absolute coordinates\nG1 F50\n'
	output += ';startFlag\n'
	for i in range(len(angles)):
		adder = 'G1 X   ' + str(X[i]) + ' Y  ' + str(Y[i]) + ' Z  ' + str(Z[i]) + '\n'
		output += adder
	output += '\n;endFlag'
	open("ventricle.gcode", "w").write(output)




	ax.plot3D(X,Y,Z, 'black',alpha = 1, linewidth = 2)
	ax.plot_surface(
	    x_t,y_t,z_t, alpha = .55, facecolors = colors, linewidth = 0) 

	# top seal
	theta, phi = np.mgrid[0.21*np.pi:.5*np.pi:n_theta*1j, 0.0:2.0*np.pi:n_phi*1j]
	r=4
	x_s = r*np.sin(theta)*np.cos(phi)
	y_s = r*np.sin(theta)*np.sin(phi)
	z_s = np.ones_like(x_s)*8
	ax.plot_surface(
	    x_s,y_s,z_s, alpha = .5, facecolors = colors, linewidth = 0) 
	ax.set_xlim([-4.2,4.2])
	ax.set_ylim([-4.2,4.2])
	ax.set_zlim([0,8.8])
	plt.tick_params(labelsize=25)
	set_axes_equal(ax)
	plt.savefig('ventricle.png')
	plt.show()

if __name__ == "__main__":
	main()