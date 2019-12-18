# -*- coding: utf-8 -*-
import utils
import matplotlib.pyplot as plt # for plotting
from scipy.spatial import Delaunay
import numpy as np
import sys

exit_flag = '1'
while exit_flag == '1':
    print("If you want to see a fish - enter f \nIf you want to see a bird - enter b")
    flag = sys.stdin.readline().split()[0]
    print("Enter number of the image \nbirds: 1 - 51, fish: 1-56")
    num = sys.stdin.readline().split()[0]

    filename = utils.get_fname(flag, num)
    short_fname = filename.split('/')[-1]
    pts = utils.read_file(filename)

    tri = Delaunay(pts)
    triang_dist, mean_length, std_length = utils.get_tri_dist(tri, pts)
    tri_sel = utils.select_tri_short_edges(triang_dist, mean_length, std_length, 1.75)
    edges = utils.get_tri_edges(tri_sel)
    m, points_m = utils.get_outer_edges(edges, pts)
    length_edges = utils.get_edges_with_length(m, pts)

    p = 0
    for i in length_edges:
        p += i[1]

    s = 0
    for i in tri_sel:
        s += utils.square_ft(i, pts)

    plt.figure(figsize=(8, 8))
    plt.title(short_fname)
    plt.gcf().text(0.6, 0.875, 'Perimeter: ' + str(round(p, 2)) + '\nSquare: ' + str(round(s, 2)))
    plt.plot([points_m[:, 0], points_m[:, 2]], [points_m[:, 1], points_m[:, 3]], color='orange', alpha=0.85)
    plt.scatter(pts[:, 0], pts[:, 1], alpha=0.5)
    plt.axis('off')
    plt.show()

    print("If you want to start from the beginning - enter 1. \nOtherwise - enter any other number")
    exit_flag = sys.stdin.readline().split()[0]
