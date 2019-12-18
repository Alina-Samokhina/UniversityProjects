# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt


def read_file(fname):
    try:
        f = open(fname, "r")
    except FileNotFoundError:
        print ('No such file. We have 56 fish and 51 bird. \n\
               We will open our favourite bird. You can try again!')
        fname = get_fname('b', 32)
        f = open(fname, "r")
    pts = []
    n_pts = f.readline().split()[0]
    for x in f:
        a = x.split()
        if len(a)>0:
            pts.append([a[0], a[1]])

    pts = np.array(pts).astype(int)
    f.close()
    return pts


def plot_figure(pts):
    plt.figure(figsize = (8,6))
    plt.scatter(pts[:, 0], pts[:, 1])
    plt.axis('off')
    plt.show


def get_fname(imtype='b', num = 1):
    if imtype == 'bird' or imtype == 'b':
        imtype = "п"
    if imtype == 'fish' or imtype == 'f':
        imtype = "р"
    fname = "./Data/"+imtype+"_"+str(num)+".txt"
    return fname


def dist(a, b):
    dist = sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)
    return dist


def get_edges_with_length(edges, pts):
    lengths = []
    for e in edges:
        a = pts[e[0]]
        b = pts[e[1]]
        d = dist(a, b)
        lengths.append([e, d])#, a[0], a[1], b[0], b[1]])
        #lengths.append([e, d])
    return lengths


def get_tri_edges(tri):
    triang_edges = []  # start point, end point,  length
    for i in tri:
        a = min(i[0], i[1], i[2])
        c = max(i[0], i[1], i[2])
        if a != i[0] and c != i[0]:
            b = i[0]
        elif a != i[1] and c != i[1]:
            b = i[1]
        else:
            b = i[2]
        for i in [(a, b), (b, c), (a, c)]:
            info = tuple(i)
            triang_edges.append(info)

    return triang_edges


def get_tri_dist(tri, pts):
    tri_dist = []
    d = []
    for i in tri.simplices:
        a = pts[i[0]]
        b = pts[i[1]]
        c = pts[i[2]]
        tri_dist.append([i, dist(a, b), dist(a, c), dist(b, c)])
        d.append(dist(a, b))
        d.append(dist(a, c))
        d.append(dist(c, b))
    return tri_dist, np.mean(d), np.std(d)


def select_tri_short_edges(triang_dist, mean_length, std_length, coef = 1.75):
    tri_sel = []
    for td in triang_dist:
        if td[1]<=mean_length+coef*std_length and\
           td[2]<=mean_length+coef*std_length and\
           td[3]<=mean_length+coef*std_length:

            tri_sel.append(td[0])
    return tri_sel


def get_outer_edges(edges, pts):
    occurences = [[x,list(edges).count(x)] for x in set(edges)] #how many triangles each edge appeared in
    m = [] #edges of contour
    points_m = [] #points of this edges for convinience
    for i in occurences:
        if i[1] == 1:
            m.append(i[0])
            p1 = pts[i[0][0]]
            p2 = pts[i[0][1]]
            points_m.append([p1[0], p1[1], p2[0], p2[1] ])

    return m, np.array(points_m)


def square_ft(triangle, pts):
    p1 = pts[triangle[0]]
    p2 = pts[triangle[1]]
    p3 = pts[triangle[2]]
    a = dist(p1, p2)
    b = dist(p2, p3)
    c = dist(p3, p1)
    pp = 0.5 * (a + b + c)
    s = sqrt(pp * (pp - a) * (pp - b) * (pp - c))
    return s
