import matplotlib.pyplot as plt # for plotting
from IPython.display import clear_output #for plotting to be cute
from random import randint # for sorting and creating data pts
from math import atan2 # for computing polar angle
import numpy as np

#if we do not have input file for demonstration, we'll create it
#using random points [0, 500]x[0, 500] space
#0.8 and 0.2 multipliers are used to have intersecting, but not overlaying convex hulls

def create_input_file(num, fname='input.txt', vmin=0, vmax=500):
    f = open(fname,"w+")
    f.write(str(num)+'\n')
    for i in range(num):
        c = randint(0,1)
        if c == 1:
            a = randint(vmin,int(vmax*0.8))
            b = randint(vmin,int(vmax*0.8))
        else:
            a = randint(int(vmax*0.2),vmax)
            b = randint(int(vmax*0.2),vmax)
        f.write(str(a)+' '+str(b)+' '+str(c)+'\n')
    f.close()

#reading file line by line storing
def read_file(fname):
    f = open(fname, "r")
    pts0 = []
    pts1 = []
    n_pts = f.readline().split()[0]
    for x in f:
        a = x.split()
        if len(a)>0:
            if a[2]=='0':
                pts0.append([a[0], a[1]])
            elif a[2]=='1':
                pts1.append([a[0], a[1]])

    pts0 = np.array(pts0).astype(int)
    pts1 = np.array(pts1).astype(int)
    f.close()
    return pts0, pts1

def plot_progress(coords, convex_hull):
    xs,ys=zip(*coords) # unzip into x and y coord lists
    plt.scatter(xs,ys, color = 'orange') # plot the data points
    clear_output(True)
    hull = np.array(convex_hull)
    x = np.append(hull[:, 0], hull[0, 0])
    y = np.append(hull[:, 1], hull[0, 1])
    plt.plot(x, y,color = 'blue')
    plt.show()

def plot_both(pts0, pts1, ch0, ch1):
    xs0,ys0 = zip(*pts0)
    plt.scatter(xs0, ys0, color = 'orange')
    xs1,ys1 = zip(*pts1)
    plt.scatter(xs1, ys1,color = 'blue')
    hull = np.array(ch0)
    x0 = np.append(hull[:, 0], hull[0, 0])
    y0 = np.append(hull[:, 1], hull[0, 1])
    plt.plot(x0, y0,color = 'orange')
    hull = np.array(ch1)
    x1 = np.append(hull[:, 0], hull[0, 0])
    y1 = np.append(hull[:, 1], hull[0, 1])
    plt.plot(x1, y1,color = 'blue')
    plt.show()

# Returns the polar angle (radians) from p0 to p1.
# If p1 is None, defaults to replacing it with the
# global variable 'anchor', normally set in the
# 'graham_scan' function.
def polar_angle(p0,p1=None):
    if p1==None:
        p1=anchor
    y_span=p0[1]-p1[1]
    x_span=p0[0]-p1[0]
    return atan2(y_span,x_span)


# Returns the euclidean distance from p0 to p1,
# square root is not applied for sake of speed.
# If p1 is None, defaults to replacing it with the
# global variable 'anchor', normally set in the
# 'graham_scan' function.
def distance(p0,p1=None):
    if p1==None:
        p1=anchor
    y_span=p0[1]-p1[1]
    x_span=p0[0]-p1[0]
    return y_span**2 + x_span**2



# Returns the determinant of the 3x3 matrix...
# [p1(x) p1(y) 1]
# [p2(x) p2(y) 1]
# [p3(x) p3(y) 1]
# If >0 then counter-clockwise
# If <0 then clockwise
# If =0 then collinear
def det(p1,p2,p3):
    return   (p2[0]-p1[0])*(p3[1]-p1[1]) \
                -(p2[1]-p1[1])*(p3[0]-p1[0])

# Sorts in order of increasing polar angle from 'anchor' point.
# 'anchor' variable is assumed to be global, set from within 'graham_scan'.
# For any values with equal polar angles, a second sort is applied to
# ensure increasing distance from the 'anchor' point.
def quicksort(a):
    if len(a)<=1: return a
    smaller,equal,larger=[],[],[]
    piv_ang=polar_angle(a[randint(0,len(a)-1)]) # select random pivot
    for pt in a:
        pt_ang=polar_angle(pt) # calculate current point angle
        if   pt_ang<piv_ang:
            smaller.append(pt)
        elif pt_ang==piv_ang:
            equal.append(pt)
        else:
            larger.append(pt)
    return   quicksort(smaller) \
            +sorted(equal,key=distance) \
            +quicksort(larger)


def graham_scan(points,show_progress=False):
    global anchor # to be set, (x,y) with smallest y value

    # Find the (x,y) point with the lowest y value,
    # along with its index in the 'points' list. If
    # there are multiple points with the same y value,
    # choose the one with smallest x.
    min_idx=None
    for i,(x,y) in enumerate(points):
        if min_idx==None or y<points[min_idx][1]:
            min_idx=i
        if y==points[min_idx][1] and x<points[min_idx][0]:
            min_idx=i

    # set the global variable 'anchor', used by the
    # 'polar_angle' and 'distance' functions
    anchor=points[min_idx]

    # sort the points by polar angle then delete
    # the anchor from the sorted list
    sorted_pts=quicksort(points)
    del sorted_pts[sorted_pts.index(anchor)]

    # anchor and point with smallest polar angle will always be on hull
    hull=[anchor,sorted_pts[0]]
    for s in sorted_pts[1:]:
        while det(hull[-2],hull[-1],s)<=0:
            del hull[-1] # backtrack
            if len(hull)<2: break
        hull.append(s)
        if show_progress: plot_progress(points,hull)
    return hull


def AreaSign(a, b, c):
    area = (b[0] - a[0]) * (c[1] - a[1]) - \
           (c[0] - a[0]) * (b[1] - a[1])

    if area > 0.5:
        return 1
    elif area < -0.5:
        return -1
    else:
        return 0


"""-------------------------------------------------------------------
SegSegInt: Finds the point of intersection p between two closed
segments ab and cd.  Returns p and a char with the following meaning:
   'e': The segments collinearly overlap, sharing a point.
   'v': An endpoint (vertex) of one segment is on the other segment,
        but 'e' doesn't hold.
   '1': The segments intersect properly (i.e., they share a point and
        neither 'v' nor 'e' holds).
   '0': The segments do not intersect (i.e., they share no points).
Note that two collinear segments that share just one point, an endpoint
of each, returns 'e' rather than 'v' as one might expect.
---------------------------------------------------------------------*/"""


def SegSegInt(p0, p1, q0, q1, p, q):
    code = '?'  # Return char characterizing intersection
    x1 = p0[0]
    x2 = p1[0]
    x3 = q0[0]
    x4 = q1[0]
    y1 = p0[1]
    y2 = p1[1]
    y3 = q0[1]
    y4 = q1[1]

    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    # denom = p0[0] * ( q1[1] - q0[1] ) +\
    #       p1[0] * ( q0[1] - q1[1] ) +\
    #      q1[0] * ( p1[1] - q0[1] ) +\
    #     q0[0] * ( p0[1] - p1[1] )

    if (denom == 0.0):  # segments are parallel: handle separately.
        return ParallelInt(p0, p1, q0, q1, p, q)

    # num =   p0[0] * ( q1[1] - q0[1] ) +\
    #       q0[0] * ( p0[1] - q1[1] ) +\
    #      q1[0] * ( q0[1] - p0[1] )

    num = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)

    if ((num == 0.0) or (num == denom)):
        code = 'v'

    s = num / denom  # wiki - t

    # num = -(p0[0] * ( q0[1] - p1[1] ) +\
    #       p1[0] * ( p0[1] - q0[1] ) +\
    #      q0[0] * ( p1[1] - p0[1] ))

    num = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3))

    if ((num == 0.0) or (num == denom)):
        code = 'v'

    t = num / denom  # wiki - u

    if ((0.0 < s) and (s < 1.0) and (0.0 < t) and (t < 1.0)):
        code = '1'

    elif ((0.0 > s) or (s > 1.0) or (0.0 > t) or (t > 1.0)):
        code = '0'

    x = x1 + s * (x2 - x1)
    y = y1 + s * (y2 - y1)
    p = [x, y]

    q = None

    return code, p, q


def ParallelInt(a, b, c, d, p, q):
    if (AreaSign(a, b, c) != 0):  # non-colinear
        return '0', p, q

    if (Between(a, b, c) and Between(a, b, d)):
        return 'e', c, d

    if (Between(c, d, a) and Between(c, d, b)):
        return 'e', a, b

    if (Between(a, b, c) and Between(c, d, b)):
        return 'e', c, b

    if (Between(a, b, c) and Between(c, d, a)):
        return 'e', c, a

    if (Between(a, b, d) and Between(c, d, b)):
        return 'e', d, b

    if (Between(a, b, d) and Between(c, d, a)):
        return 'e', d, a

    return '0', p, q

def Between( a, b, c):
    if ( a[0] != b[0] ):
        return (((a[0] <= c[0]) and (c[0] <= b[0])) or ((a[0] >= c[0]) and (c[0] >= b[0])))
    else:
        return ((a[1] <= c[1]) and (c[1] <= b[1])) or ((a[1] >= c[1]) and (c[1] >= b[1]))

def InOut(inflag, aHB, bHA):
    if  ( aHB > 0):
        return 'Pin'
    elif ( bHA > 0):
        return 'Qin'
    else:
        return inflag


def get_intersection_of_hulls(P, Q):
    n = len(P)
    nq = len(Q)
    # a, b - indices, we strt from the bottom
    a = 1
    b = 1
    # counting steps in both hulls
    ca = 0
    cb = 0
    ip = [None, None]
    iq = [None, None]
    zero_point = [0, 0]

    inflag = 'Unknown'
    firstpoint = True

    intersection = []

    while (ca < n or cb < nq) and (ca < n * n) and (cb < nq * nq):

        ap = (a + n - 1) % n
        bp = (b + nq - 1) % nq
        va = P[a] - P[ap]
        vb = Q[b] - Q[bp]

        # sign of AxB:
        sign = AreaSign(zero_point, va, vb)

        # to count advances, Halfplane condition a\in H(B) and b\in H(A):
        aHB = AreaSign(Q[bp], Q[b], P[a])
        bHA = AreaSign(P[ap], P[a], Q[b])

        code, ip, iq = SegSegInt(P[ap], P[a], Q[bp], Q[b], ip, iq)  # MB vice versa!!!
        # print(code, ip, iq)

        if (code == '1' or code == 'v'):
            if inflag == 'Unknown' and firstpoint:
                ca = 0
                cb = 0
                firstpoint = False

                # intersection.append(p0)
            inflag = InOut(inflag, aHB, bHA)
            intersection.append(ip)

        # Advance rules
        # Sprcial cases
        # A B overlap oppositely oriented
        if (code == 'e' and numpy.dot(va, vb) < 0):
            uru = 0
            # intersection.append(ip)
            # intersection.append(iq)
        # parallel and sepaarated - nothing
        # collinear:
        elif (sign == 0 and aHB == 0 and bHA == 0):
            if inflag == 'Pin':
                # if inflag == 'Qin':
                #    intersection.append([Q[b][0], Q[b][1]])
                b = (b + 1) % nq
                cb += 1
            else:
                # if inflag == 'Pin':
                #    intersection.append([P[a][0], P[a][1]])
                a = (a + 1) % n
                ca += 1
        # Genericc ases
        elif (sign >= 0):
            if (bHA > 0):
                if inflag == 'Pin':
                    intersection.append([P[a][0], P[a][1]])
                a = (a + 1) % n
                ca += 1
            else:
                if inflag == 'Qin':
                    intersection.append([Q[b][0], Q[b][1]])
                b = (b + 1) % nq
                cb += 1
        else:
            if (aHB > 0):
                if inflag == 'Qin':
                    intersection.append([Q[b][0], Q[b][1]])
                b = (b + 1) % nq
                cb += 1
            else:
                if inflag == 'Pin':
                    intersection.append([P[a][0], P[a][1]])
                a = (a + 1) % n
                ca += 1
    if firstpoint and isInside(P[0], Q):
        intersection = P
    elif firstpoint and isInside(Q[0], P):
        intersection = Q
    return intersection


def isInside(p, hull):
    if hull[0][0] != hull[len(hull) - 1][0] and hull[0][1] != hull[len(hull) - 1][1]:
        hull.append(hull[0])
    closed_hull = np.array(hull)

    flag = True
    for i in range(len(closed_hull) - 1):
        a = closed_hull[i, :]
        b = closed_hull[i + 1, :]
        res = AreaSign(a, b, p)
        if res == -1:  # don't lie left. borders included
            flag = False
    return flag


