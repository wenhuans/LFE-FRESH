################################################################################
## This script create a preliminary G-code file for 3D heart ventricle fiber  ##
## embedding                                                                  ## 

import math
import numpy as np
from matplotlib import pyplot as plt
import os.path
from itertools import product, combinations
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection



def main():
    def plot_cube(cube_definition):
        cube_definition_array = [
            np.array(list(item))
            for item in cube_definition
        ]

        points = []
        points += cube_definition_array
        vectors = [
            cube_definition_array[1] - cube_definition_array[0],
            cube_definition_array[2] - cube_definition_array[0],
            cube_definition_array[3] - cube_definition_array[0]
        ]

        points += [cube_definition_array[0] + vectors[0] + vectors[1]]
        points += [cube_definition_array[0] + vectors[0] + vectors[2]]
        points += [cube_definition_array[0] + vectors[1] + vectors[2]]
        points += [cube_definition_array[0] + vectors[0] + vectors[1] + vectors[2]]

        points = np.array(points)

        edges = [
            [points[0], points[3], points[5], points[1]],
            [points[1], points[5], points[7], points[4]],
            [points[4], points[2], points[6], points[7]],
            [points[2], points[6], points[3], points[0]],
            [points[0], points[2], points[4], points[1]],
            [points[3], points[6], points[7], points[5]]
        ]

        faces = Poly3DCollection(edges, linewidths=.25, edgecolors='k')
        faces.set_facecolor((0,1,1,0.1))

        ax.add_collection3d(faces)

        # Plot the points themselves to force the scaling of the axes
        ax.scatter(points[:,0], points[:,1], points[:,2], s=0)

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

    file = "conical_helix.gcode"
    num_rev = 3
    radi = np.linspace(1, 3, 120 * num_rev)
    height = 3
    angles = np.linspace(0, num_rev * 2 * math.pi - 0.05, 120 * num_rev)
    X = np.zeros_like(angles)
    Y = np.zeros_like(angles)
    Z=  np.zeros_like(angles)
    org_x = np.ones_like(angles) * 0
    org_y = np.ones_like(angles) * 3 #1
    X = org_x - np.multiply(radi, np.sin(angles))
    Y = org_y - np.multiply(radi, np.cos(angles))
    Z = height / 120 / num_rev * np.arange(120 * num_rev)
    X[np.abs(X)<1e-5] = 0
    Y[np.abs(Y)<1e-5] = 0
    Z[np.abs(Z)<1e-5] = 0


    output = 'T0; set temperature to 0\nG92 X0 Y0 Z0; set current position as home, go when start\n; Filament gcode\nG21 ; set units to millimeters\nG90 ; use absolute coordinates\nG1 F50\n'

    output += ';startFlag\n'

    for i in range(120*num_rev):
    	adder = 'G1 X   ' + str(X[i]) + ' Y  ' + str(Y[i]) + ' Z  ' + str(Z[i]) + '\n'
    	output += adder
    output += '\n;endFlag'


    open(file, "w").write(output)

    fig, ax = plt.subplots()
    # fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot3D(X,Y,Z, 'black',alpha = 1)

    set_axes_equal(ax)

    cube_definition = [
        (-3,0,0), (3,0,0), (-3,6,0), (-3,0,4)
    ]
    ax.set_zlim(0,4)
    plot_cube(cube_definition)
    plt.tick_params(labelsize=25)
    plt.savefig('conical_helix.png')
    plt.show()

if __name__ == "__main__":
    main()
