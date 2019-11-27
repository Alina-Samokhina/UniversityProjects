import utils
import matplotlib.pyplot as plt # for plotting
import numpy as np
import sys

print("If you want to use generated random points file - print 0 \n If you want to use your file - print 1")
flag = sys.stdin.readline()
if flag == '0\n':
    utils.create_input_file(30)
    fname = 'input.txt'
else:
    fname = None
    print("input file name:\n(If file is in the same folder - just nave like 'input.txt' is enough. Otherwise, specify the full path (must contain no spaces)")
    while fname is None:
        fname = sys.stdin.readline().split()[0]
        try:
            f = open(fname, "r")
        except OSError:
            print("No such file, try again")
            fname = None

pts0, pts1 = utils.read_file(fname)

#fname = "Lab-1-2019-Dannye.txt"



hull0 = utils.graham_scan(list(pts0),False)
hull1 = utils.graham_scan(list(pts1),False)
#plot_both(pts0, pts1, hull0, hull1)

intersection_hull = utils.get_intersection_of_hulls(hull0, hull1)

allpts = np.append(pts0, pts1, axis = 0)

inside_points = []
outside_pts = []
for p in allpts:
    if utils.isInside(p, intersection_hull):
        inside_points.append(p)
    else:
        outside_pts.append(p)

inside_points = np.array(inside_points)
outside_pts = np.array(outside_pts)

f = open("output.txt", "w+")
f.write("Convex hull 0:\n")
for i in hull0:
    f.write(str(i[0])+' '+str(i[1])+ '\n')
f.write("Convex hull 1:\n")
for i in hull1:
    f.write(str(i[0])+' '+str(i[1])+ '\n')
f.write("Points inside the intersectio:\n")
for i in inside_points:
    f.write(str(i[0])+' '+str(i[1])+ '\n')
f.close()

not_in_intersection0 = [p for p in pts0 if p not in inside_points]
not_in_intersection1 = [p for p in pts1 if p not in inside_points]
num_outs0 = len(not_in_intersection0)
num_outs1 = len(not_in_intersection1)
num_in = len(inside_points)

plt.figure(figsize = (8, 6))
plt.gcf().text(0.6, 0.9, "Total points inside intersection:"+str(num_in)+"\nPoints from 0 cloud, outside the intersection: " + str(num_outs0)+\
         "\nPoints from 1 cloud, outside the intersection: " + str(num_outs1)+"\nDetails about hulls and intersection points are in output.txt", fontsize=6)
plt.plot(np.append(np.array(hull0)[:, 0], np.array(hull0)[0, 0]), np.append(np.array(hull0)[:, 1], np.array(hull0)[0, 1]), color = 'blue')
plt.plot(np.append(np.array(hull1)[:, 0], np.array(hull1)[0, 0]), np.append(np.array(hull1)[:, 1], np.array(hull1)[0, 1]), color = 'orange')
plt.plot(np.append(np.array(intersection_hull)[:, 0], np.array(intersection_hull)[0, 0]),\
         np.append(np.array(intersection_hull)[:, 1], np.array(intersection_hull)[0, 1]), color  = 'green')
plt.scatter(inside_points[:,0], inside_points[:,1], color = 'green')
plt.scatter(outside_pts[:,0], outside_pts[:,1], color = 'yellow')

plt.show()

