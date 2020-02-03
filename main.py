import os
import random
from math import sqrt
import statistics
import matplotlib.pyplot as plt
import numpy as np


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

test_size, colours = read_file('colours.txt')  # Total number of colours and list of colours

test_size = 100  # Size of the subset of colours for testing
test_colours = colours[0:test_size]  # list of colours for testing


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
trace = []


def hill_climbing(s):
    trace.append(evaluate(s))
    for i in range(1000):
        dist = evaluate(s)
        s1 = s.copy()  # Make a copy of the solution
        # Generate 2 random integers, within the test_size limits
        r = random.randint(0, test_size - 1)
        r1 = random.randint(0, test_size - 1)

        # Index Inverse Neighbourhood
        if r < r1:
            s1[r:r1] = s1[r:r1][::-1]

        else:
            s1[r1:r] = s1[r1:r][::-1]

        # Index Swap Neighbourhood
        # s1[r], s1[r1] = s1[r1], s1[r]

        dist1 = evaluate(s1)
        trace.append(dist1)
        if dist1 < dist:
            s = s1
            # trace.append(dist1)

    return s, trace


def multi_hill_climbing(s, number):
    best = s
    best_trace = []

    for i in range(number):
        s, trace = hill_climbing(best)
        dist = evaluate(s)
        print('Climb ', i + 1, ' distance: ', dist)
        b = evaluate(best)
        if dist < b:
            best = s
            trace.sort(reverse=True)
            best_trace = trace

    return best, best_trace


def list_dist():
    s = np.zeros((test_size, test_size))  # sets a 2d array s, of size [test_size][test_size]
    for i in range(test_size):
        for j in range(test_size):
            s[i, j] = calc_dist(i, j)  # enters every possible distance calculated into the array

    return s


# s is the solution provided, start is the index of the starting location
def greedy_construction(start):
    s = list_dist()
    best = [start]
    mask = np.ones(test_size, dtype=bool)  # Masking array of size test_size, with values of type boolean, set to True

    for i in range(test_size - 1):
        last = best[-1]
        # Find the minimum distance in s, for the last index, parsed by mask (only those that are true)
        next_index = np.argmin(s[last][mask])
        # print('Next index: ', next_index, ', Last: ', last, ', Mask: ', mask)

        # Arrange all values (test_size), subtracting the False ones from mask
        # and set the next index as a parameter
        next_location = np.arange(test_size)[mask][next_index]
        # print('Next Loc: ', next_location, ' Mask: ', mask)

        best.append(next_location)
        mask[next_location] = False

    return best


# ---------------------- Random ----------------------
plot_colours(test_colours, random_sol())

# ---------------------- Hill Climbing ----------------------
# best, b_trace = hill_climbing(random_sol())
# print('Distance: ', evaluate(best))
# plot_colours(test_colours, best)
# print(b_trace)
# plt.figure()
# plt.plot(b_trace, 'bo', markersize=1.5)  # 'bo' indicates to plot as dots (circles) blue color
# plt.title('Hill Climb Best Trace')
# plt.ylabel('Distance')
# plt.xlabel('Solutions')
# plt.show()

# ---------------------- Multi Hill Climbing ----------------------
# iter = 30  # set the maximum iterations for the hill-climber
# best, b_trace = multi_hill_climbing(random_sol(), iter)
# plot_colours(test_colours, best)
# # print(b_trace)
# dist = evaluate(best)
# print('Distance: ', dist)
# print('Mean: ', statistics.mean(b_trace))
# print('Median: ', statistics.median(b_trace))
# print('Std. dev: ', statistics.stdev(b_trace))
# plt.figure()
# plt.plot(b_trace, 'bo', markersize=1.5)  # 'bo' indicates to plot as dots (circles) blue color
# plt.title('Multi Hill Climb Trace')
# plt.ylabel('Distance')
# plt.xlabel('Solutions')
# plt.show()

# ---------------------- Greedy Construction ----------------------
# s = greedy_construction(0)
# plot_colours(test_colours, s)
# dist = evaluate(s)
# print('Greedy distance: ', dist)

# ---------------------- Exhaustive Greedy Construction ----------------------
s = greedy_construction(0)
d = evaluate(s)
for i in range(test_size - 1):
    s1 = greedy_construction(i)
    d1 = evaluate(s1)
    if d1 < d:
        s = s1
        d = d1
        print('Index: ', i, ' distance: ', d1)

plot_colours(test_colours, s)
dist = evaluate(s)
print('Exhaustive Greedy distance: ', dist)
# ---------------------- Greedy Construction & Hill Climb ----------------------
# s = greedy_construction(0)
# # s, trace = hill_climbing(s)
# plot_colours(test_colours, s)
# s, trace = multi_hill_climbing(s, 10)
# dist = evaluate(s)
# print('Greedy Hill Climb distance: ', dist)
