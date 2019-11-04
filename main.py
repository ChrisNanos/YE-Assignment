import matplotlib.pyplot as plt
import numpy as np
from math import sqrt
from scipy.spatial import distance
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
    r1, g1, b1 = colours[col1]
    r2, g2, b2 = colours[col2]
    dist = sqrt((r2 - r1) ** 2 + (g2 - g1) ** 2 + (b2 - b1) ** 2)
    return dist


def evaluate(sol):
    dist = 0
    for i in range(len(sol) - 1):
        dist += calc_dist(sol[i], sol[i + 1])

    return dist


s = random_sol()


def hill_climbing(s):
    best = s
    for i in range(2000):
        dist = evaluate(s)
        s1 = s.copy()
        r = random.randint(0, test_size - 1)
        r1 = random.randint(0, test_size - 1)
        if r < r1:
            s1[r:r1] = s1[r:r1][::-1]
        else:
            s1[r1:r] = s1[r1:r][::-1]

        dist1 = evaluate(s1)
        if dist1 < dist:
            s = s1.copy()

    return s


# s = hill_climbing(1000)
# plot_colours(test_colours, s)
# print('Hill Climb: ', evaluate(s))


def multi_hill_climbing(number):
    s = random_sol()
    best = s
    plot_colours(test_colours, best)

    for i in range(number):
        s = hill_climbing(s)
        dist = evaluate(s)
        print('Climb ', i + 1, ' distance: ', dist)
        b = evaluate(best)
        if dist < b:
            best = s
        s = random_sol()

    return best


# s = multi_hill_climbing(10)
# plot_colours(test_colours, s)
# print('Multi Hill Climb: ', evaluate(s))


def f_evaluate(sol):
    dist = 0
    for i in range(len(sol) - 1):
        dist += f_calc_dist(sol[i], sol[i + 1])

    return dist


def f_calc_dist(col1, col2):
    r1, g1, b1 = colours[col1]
    r2, g2, b2 = colours[col2]
    dist = sqrt((r2 - r1) ** 2 + (g2 - g1) ** 2 + (b2 - b1) ** 2)
    # if dist <= 0.2:
    #     temp.append(colours[col1])
    #     temp.append(colours[col2])

    return dist


def greedy():
    s = random_sol()
    final = []
    best = 0
    temp = []
    i = 0
    j = 0
    while i < len(s):
        s1 = s[-1]
        while j < len(s):
            s2 = s[j]
            dist = calc_dist(s1, s2)
            print(s[j])
            if dist < best:
                best = dist.copy()
                temp = test_colours[s2]
        final.append(s1)
        final.append(s2)

    return final


s = greedy()
print(len(s))
plot_colours(test_colours, s)
print('Greedy: ', evaluate(s))