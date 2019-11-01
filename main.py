import matplotlib.pyplot as plt
import numpy as np
from math import sqrt
import random
import os


# Reads the file  of colours
# Returns the number of colours in the file and a list with the colours (RGB) values

def read_file(fname):
    with open(fname, 'r') as afile:
        lines = afile.readlines()
    n = int(lines[3])  # number of colours  in the file
    col = []
    lines = lines[4:]  # colors as rgb values
    for l in lines:
        rgb = l.split()
        for i in range(len(rgb)):
            rgb[i] = float(rgb[i])

        col.append(rgb)
    return n, col


# Display the colours in the order of the permutation in a pyplot window
# Input, list of colours, and ordering  of colours.
# They need to be of the same length

def plot_colours(col, perm):
    assert len(col) == len(perm)

    ratio = 20  # ratio of line height/width, e.g. colour lines will have height 10 and width 1
    img = np.zeros((ratio, len(col), 3))
    for i in range(0, len(col)):
        img[:, i, :] = colours[perm[i]]

    fig, axes = plt.subplots(1, figsize=(8, 4))  # figsize=(width,height) handles window dimensions
    axes.imshow(img, interpolation='nearest')
    axes.axis('off')
    plt.show()


#####_______main_____######

# Get the directory where the file is located
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)  # Change the working directory so we can read the file

ncolours, colours = read_file('colours.txt')  # Total number of colours and list of colours

test_size = 100  # Size of the subset of colours for testing
test_colours = colours[0:test_size]  # list of colours for testing

# plot_colours(test_colours, permutation)


def random_sol():
    # produces random permutation of length test_size, from the numbers 0 to test_size -1
    return random.sample(range(test_size), test_size)


def calc_dist(col1, col2):
    r1,g1,b1 = colours[col1]
    r2,g2,b2 = colours[col2]
    dist = sqrt((r2 - r1) ** 2 + (g2 - g1) ** 2 + (b2 - b1) ** 2)
    return dist


def evaluate(sol):
    dist = 0
    for i in range(len(sol) - 1):
        dist += calc_dist(sol[i], sol[i+1])

    return dist


def hill_climbing(number):
    s = random_sol()
    plot_colours(test_colours, s)
    for i in range(number):
        dist = evaluate(s)
        print('Distance: ', dist)
        r = random.randint(0, test_size - 1)
        print(r)
        r1 = random.randint(0, test_size - 1)
        print(r1)
        print(s)
        s[r:r1:-1]
        print(s)
        s1 = s.copy()
        if evaluate(s1) < dist:
            s = s1

    return s


s = hill_climbing(2000)
plot_colours(test_colours, s)
print('Hill Climb: ',evaluate(s))