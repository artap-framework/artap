
import scipy.io
import pylab as pl
import matplotlib.tri as mtri

points = scipy.io.loadmat('transient_solver-heat_points.mat')['points']
elements = scipy.io.loadmat('transient_solver-heat_elements.mat')['elements']
u = scipy.io.loadmat('transient_solver-heat_solutions.mat')['slns']

step = 30

x = []
y = []
z = []
for i in range(0, len(points)):
    x.append(points[i][0])
    y.append(points[i][1])
    z.append(u[i][step])

triangles = []
for i in range(0, len(elements)):
    if elements[i][0] > 0 and elements[i][1] > 0 and elements[i][2] > 0:
        triangles.append([elements[i][0], elements[i][1], elements[i][2]])
    if elements[i][1] > 0 and elements[i][2] > 0 and elements[i][3] > 0:
        triangles.append([elements[i][1] , elements[i][2], elements[i][3] ])


triang = mtri.Triangulation(x, y, triangles)

tcf = pl.tricontourf(triang, z)
pl.triplot(triang, 'k-', linewidth=0.2)
pl.colorbar(tcf)

pl.tight_layout()
pl.show()