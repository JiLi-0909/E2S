#!/bin/env dls-python
import os
import sys
import numpy as np
import matplotlib.pyplot as plt

def execfile(filepath, globals):
    if globals is None:
        globals = {}
    globals.update({
        "__file__": filepath,
        "__name__": "__main__",
    })
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), globals)

def print_usage():
    print ('Usage:', sys.argv[0], '[directory] [flip axis]')
    print ('')
    print ('If no directory is given the current working directory')
    print ('will be assumed. Any second argument will always negate')
    print ('both axis in the graph.')


def plot(directory, flip_axis=False):
    # Call with a value (0..1) to get colour four tuple
    color_map = plt.get_cmap('rainbow')

    # Plot files in the current directory
    front_files = [x for x in os.listdir(directory) if 'fronts.' in x]
    print('front_files is:')
    print(front_files)
    if not front_files:
        print_usage()

    generations = []
    for front_file in front_files:
        env = {}
        execfile(front_file, env)
        generations.append(env['fronts'])

    for index, fronts in enumerate(generations):
        front = fronts[0]  # Only use the best front
        color = color_map(1.0 * index / (len(generations)))

        points = np.array(front)[:, 1]
        if flip_axis:  # Might want to negate points as NSGA is a minimizer
            points = [(-x, -y) for (x, y) in points]
        points = sorted(points)

        lines = points[:]
        for p1, p2 in zip(points, points[1:]):
            #lines.append((min(p1[0], p2[0]), min(p1[1], p2[1])))# FBT : original line
            #lines.append((min(p1[0], p2[0]), min(p1[1], p2[1])))# FBT : original line
            lines.append((max(p1[0], p2[0]), max(p1[1], p2[1])))
        lines = sorted(lines, key=lambda x:(x[0], -x[1]))

        plt.plot(*zip(*points), linestyle='' , marker='.', color=color)
        plt.plot(*zip(*lines), linestyle='--', color=color)
        if index==38 :#len(generations)-1:
            plt.plot(*zip(*points), linestyle='' , marker='D', color=color) 
            plt.plot(*zip(*lines), color='black' )
    #plt.xlabel('sigma_x')
    #plt.ylabel('sigma_y')
    plt.xlabel('fwhmx(cm)')
    plt.ylabel('fwhmy(cm)')
    plt.show()


if __name__ == '__main__':
    # Defaults
    flip_axis = False
    directory = os.getcwd()

    # Check args
    if sys.argv[1:]:
        directory=sys.argv[1]
    if sys.argv[2:]:
        negate = True

    plot(directory, flip_axis)
