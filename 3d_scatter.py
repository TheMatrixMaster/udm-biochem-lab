from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt 

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

xs = [3, 7, 4, 9, 13, 21, 2, 5]
ys = [9, 27, 17, 19, 13, 4, 2, 11]
zs = [22, 0, 6, 8, 21, 15, 14, 8]

ax.scatter(xs, ys, zs, c = 'r')

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()