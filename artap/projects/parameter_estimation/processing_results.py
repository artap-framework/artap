import pylab as pl
import glob
import numpy as np
import os


class Result:

    def __init__(self):
        self.parameters = []
        self.curves = []
        self.values_at_points = []


results = []
names = ['inlet%s.txt', 'outlet%s.txt', 'inlet_tube%s.txt', 'outlet_tube%s.txt', 'inlet_sleeve%s.txt',
         'outlet_sleeve%s.txt']
colors = ['red', 'green', 'blue', 'cyan', 'grey', 'purple']
k = 0
pl.rcParams['figure.figsize'] = 6, 4
Y = []

os.chdir('./2018-10-23 11:08:56.228071')
for file in glob.glob('params*.txt'):
    result = Result()
    time_stamp = file[7:-4]
    with open(file) as param_file:
        lines = param_file.readlines()
        for line in lines:
            result.parameters.append(float(line))

    with open("max%s.txt" % time_stamp) as max_file:
        lines = max_file.readlines()

    t = []
    n = len(lines[5].split())
    point_curves = []
    for i in range(n-1):
        point_curves.append([])

    for line in lines[5:]:
        line_list = line.split()
        t.append(float(line_list[0]))
        for i in range(0, n-1):
            point_curves[i].append(float(line_list[i+1]))

    result.values_at_points = point_curves
    result.t = t
    for name in names:
        curve = []
        file = name % time_stamp
        result_file = open(file)
        content = result_file.readlines()
        x = []
        y = []
        for line in content[8:]:
            numbers = line.split()
            x.append(float(numbers[0]))
            y.append(float(numbers[1]))

        max_x = max(x)
        for i in range(len(x)):
            x[i] = x[i] / max_x * 360

        curve.append(x.copy())
        curve.append(y.copy())

        result.curves.append(curve.copy())
    results.append(result)

for i in [0,1]:
    Y = []
    for result in results:
            x = result.curves[i][0]
            Y.append(result.curves[i][1])

    x = np.array(x)
    Y = np.array(Y)

    Y_mean = np.mean(Y, axis=0)
    Y_std = np.std(Y, axis=0)

    pl.plot(x, Y_mean, color=colors[i])
    pl.plot(x, Y_mean + Y_std, 'k--')
    pl.plot(x, Y_mean - Y_std, 'k--')
    pl.fill_between(x.flatten(), Y_mean.flatten() - Y_std.flatten(), Y_mean.flatten() + Y_std.flatten(),
                    color=colors[i], alpha=0.2)

pl.xlabel('$\\alpha $ [deg]', fontsize=18)
pl.ylabel('$T$ [$^\circ$C]', fontsize=18)
pl.xticks(fontsize=14)
pl.yticks(fontsize=14)
pl.tight_layout()
pl.grid()
pl.savefig('sensitivity.pdf')
pl.show()


ref_param = [900.0, 160, 37740000.0, 2700, 900, 160, 37740000.0, 2700, 900, 160, 37740000.0, 2700, 900,
             160, 37740000.0, 2700, 900, 160, 37740000.0, 2700]

# dependence of value at point on particular parameter
n_param = 1
for j in range(31):
    parameter = []
    for result in results:
        changes = 0
        i = 0
        for item in ref_param:
            if result.parameters[i] != item:
                changes += 1
            i += 1

        if changes == 1 and ref_param[n_param] != result.parameters[n_param]:
            parameter.append([result.parameters[n_param], result.values_at_points[j][-1]])
    parameter.sort(key=lambda x: x[0])
    x = []
    y = []
    for item in parameter:
        x.append(item[0])
        y.append(item[1])
    pl.plot(x, y)
pl.xlabel('$\\lambda_\\mathrm{block}$ [W $\\cdot$ m$^{-1} \\cdot$ K$^{-1}]$ ', fontsize=18)
pl.ylabel('$T$ [$^\circ$C]', fontsize=18)
pl.xticks(fontsize=14)
pl.yticks(fontsize=14)
pl.tight_layout()
pl.grid()
pl.savefig('dependence_on_parameter.pdf')


# ploting of time dependencies
j = 0
for i in [3, 4]:
    Y = []
    for result in results:
        for time_curve in result.values_at_points[i:i+1]:
            Y.append(time_curve)

    Y_mean = np.mean(Y, axis=0)
    Y_max = np.max(Y, axis=0)
    Y_min = np.min(Y, axis=0)

    pl.plot(result.t, Y_mean, color=colors[j])
    pl.plot(result.t, Y_max, '--', color=colors[j])
    pl.plot(result.t, Y_min, '--', color=colors[j])


    pl.fill_between(result.t, Y_min, Y_max,
                        color=colors[j], alpha=0.2)
    j += 1

pl.xlabel('$t $ [s]', fontsize=18)
pl.ylabel('$T$ [$^\circ$C]', fontsize=18)
pl.xticks(fontsize=14)
pl.yticks(fontsize=14)
pl.grid()
pl.tight_layout()
pl.savefig('sensitivity_transient.pdf')



