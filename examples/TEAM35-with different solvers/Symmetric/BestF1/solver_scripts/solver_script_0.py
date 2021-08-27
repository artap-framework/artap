import agros2d as a2d

# PROBLEM
problem = a2d.problem(clear=True)
problem.coordinate_type = "axisymmetric"
problem.mesh_type = "triangle"

magnetic = a2d.field("magnetic")
magnetic.analysis_type = "steadystate"
magnetic.number_of_refinements = 2
magnetic.polynomial_order = 2
magnetic.solver = "linear"

geometry = a2d.geometry

magnetic.adaptivity_type = "hp-adaptivity"
magnetic.adaptivity_parameters["tolerance"] = 0.2
magnetic.adaptivity_parameters["steps"] = 10

# MATERIAL DEFINITIONS
magnetic.add_material("J+", {'magnetic_remanence_angle': 0.0, 'magnetic_velocity_y': 0.0, 'magnetic_current_density_external_real': 2000000.0, 'magnetic_permeability': 1.0, 'magnetic_conductivity': 0.0, 'magnetic_remanence': 0.0, 'magnetic_velocity_angular': 0.0, 'magnetic_velocity_x': 0.0})
magnetic.add_material("air", {'magnetic_remanence_angle': 0.0, 'magnetic_velocity_y': 0.0, 'magnetic_current_density_external_real': 0.0, 'magnetic_permeability': 1.0, 'magnetic_conductivity': 0.0, 'magnetic_remanence': 0.0, 'magnetic_velocity_angular': 0.0, 'magnetic_velocity_x': 0.0})
magnetic.add_material("control", {'magnetic_remanence_angle': 0.0, 'magnetic_velocity_y': 0.0, 'magnetic_current_density_external_real': 0.0, 'magnetic_permeability': 1.0, 'magnetic_conductivity': 0.0, 'magnetic_remanence': 0.0, 'magnetic_velocity_angular': 0.0, 'magnetic_velocity_x': 0.0})

# BOUNDARY DEFINITIONS
magnetic.add_boundary("a0", "magnetic_potential", {'magnetic_potential_real': 0.0})
magnetic.add_boundary("n0", "magnetic_surface_current", {'magnetic_surface_current_real': 0.0})

# GEOMETRY
geometry.add_edge(0.14, 0.14, 0.14, 0.0, boundaries={'magnetic': 'a0'})
geometry.add_edge(0.0, 0.14, 0.14, 0.14, boundaries={'magnetic': 'a0'})
geometry.add_edge(0.0, 0.0, 0.0, 0.005, boundaries={'magnetic': 'a0'})
geometry.add_edge(0.0, 0.005, 0.0, 0.14, boundaries={'magnetic': 'a0'})
geometry.add_edge(0.007900000000000006, 0.0, 0.005, 0.0, boundaries={'magnetic': 'n0'})
geometry.add_edge(0.005, 0.0, 0.0, 0.0, boundaries={'magnetic': 'n0'})
geometry.add_edge(0.14, 0.0, 0.008900000000000005, 0.0, boundaries={'magnetic': 'n0'})
geometry.add_edge(0.008899999999999977, 0.0, 0.007900000000000006, 0.0, boundaries={'magnetic': 'n0'})
geometry.add_edge(0.0, 0.005, 0.005, 0.005)
geometry.add_edge(0.005, 0.005, 0.005, 0.0)
geometry.add_edge(0.0079, 0.0015, 0.0085, 0.0015)
geometry.add_edge(0.0085, 0.0015, 0.0089, 0.0015)
geometry.add_edge(0.0089, 0.0015, 0.0089, 0.0)
geometry.add_edge(0.0079, 0.0, 0.0079, 0.0015)
geometry.add_edge(0.0075, 0.003, 0.0085, 0.003)
geometry.add_edge(0.0085, 0.003, 0.0085, 0.0015)
geometry.add_edge(0.0079, 0.0015, 0.0075, 0.0015)
geometry.add_edge(0.0075, 0.0015, 0.0075, 0.003)
geometry.add_edge(0.0075, 0.0045000000000000005, 0.008, 0.0045000000000000005)
geometry.add_edge(0.008, 0.0045000000000000005, 0.0085, 0.0045000000000000005)
geometry.add_edge(0.0085, 0.0045000000000000005, 0.0085, 0.003)
geometry.add_edge(0.0075, 0.003, 0.0075, 0.0045000000000000005)
geometry.add_edge(0.007, 0.006, 0.007219999999999999, 0.006)
geometry.add_edge(0.007219999999999999, 0.006, 0.008, 0.006)
geometry.add_edge(0.008, 0.006, 0.008, 0.0045000000000000005)
geometry.add_edge(0.0075, 0.0045000000000000005, 0.007, 0.0045000000000000005)
geometry.add_edge(0.007, 0.0045000000000000005, 0.007, 0.006)
geometry.add_edge(0.007220000000000004, 0.0075, 0.008220000000000002, 0.0075)
geometry.add_edge(0.008220000000000002, 0.0075, 0.008220000000000002, 0.006)
geometry.add_edge(0.008220000000000002, 0.006, 0.007999999999999998, 0.006)
geometry.add_edge(0.00722, 0.006, 0.00722, 0.0075)
geometry.add_edge(0.0057599999999999995, 0.009000000000000001, 0.006160000000000004, 0.009000000000000001)
geometry.add_edge(0.006160000000000004, 0.009000000000000001, 0.0067599999999999995, 0.009000000000000001)
geometry.add_edge(0.0067599999999999995, 0.009000000000000001, 0.0067599999999999995, 0.0075)
geometry.add_edge(0.0067599999999999995, 0.0075, 0.0057599999999999995, 0.0075)
geometry.add_edge(0.0057599999999999995, 0.0075, 0.0057599999999999995, 0.009000000000000001)
geometry.add_edge(0.0051600000000000005, 0.0105, 0.006160000000000005, 0.0105)
geometry.add_edge(0.0061600000000000005, 0.0105, 0.0061600000000000005, 0.009000000000000001)
geometry.add_edge(0.005760000000000005, 0.009000000000000001, 0.0051600000000000005, 0.009000000000000001)
geometry.add_edge(0.0051600000000000005, 0.009000000000000001, 0.0051600000000000005, 0.0105)
geometry.add_edge(0.0012900000000000012, 0.012, 0.00229, 0.012)
geometry.add_edge(0.00229, 0.012, 0.00229, 0.0105)
geometry.add_edge(0.00229, 0.0105, 0.0012900000000000001, 0.0105)
geometry.add_edge(0.0012900000000000001, 0.0105, 0.0012900000000000001, 0.012)
geometry.add_edge(0.00609, 0.0135, 0.00709, 0.0135)
geometry.add_edge(0.00709, 0.0135, 0.00709, 0.012)
geometry.add_edge(0.00709, 0.012, 0.00609, 0.012)
geometry.add_edge(0.00609, 0.012, 0.00609, 0.0135)
geometry.add_edge(0.0035499999999999998, 0.015, 0.00455, 0.015)
geometry.add_edge(0.00455, 0.015, 0.00455, 0.0135)
geometry.add_edge(0.00455, 0.0135, 0.0035499999999999998, 0.0135)
geometry.add_edge(0.0035499999999999998, 0.0135, 0.0035499999999999998, 0.015)

# BLOCK LABELS
geometry.add_label(0.00865, 0.00075, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00825, 0.0022500000000000003, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00825, 0.00375, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00775, 0.00525, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00797, 0.00675, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00651, 0.00825, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00591, 0.00975, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00204, 0.01125, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00684, 0.012750000000000001, materials = {'magnetic' : 'J+'})
geometry.add_label(0.0043, 0.01425, materials = {'magnetic' : 'J+'})
geometry.add_label(0.03, 0.03, materials = {'magnetic' : 'air'})
geometry.add_label(0.003, 0.001, materials = {'magnetic' : 'control'})

# SOLVE
problem.solve()
a2d.view.zoom_best_fit()
f = open("solution_0.csv", "w")

# POSTPROCESSING AND EXPORTING
point = magnetic.local_values(1e-06, 1e-06)["Brz"]
f.write("{}, 1e-06, 1e-06, {}\n".format("Bz", point))

point = magnetic.local_values(1e-06, 1e-06)["Brr"]
f.write("{}, 1e-06, 1e-06, {}\n".format("Br", point))

point = magnetic.local_values(1e-06, 0.00125075)["Brz"]
f.write("{}, 1e-06, 0.00125075, {}\n".format("Bz", point))

point = magnetic.local_values(1e-06, 0.00125075)["Brr"]
f.write("{}, 1e-06, 0.00125075, {}\n".format("Br", point))

point = magnetic.local_values(1e-06, 0.0025004999999999997)["Brz"]
f.write("{}, 1e-06, 0.0025004999999999997, {}\n".format("Bz", point))

point = magnetic.local_values(1e-06, 0.0025004999999999997)["Brr"]
f.write("{}, 1e-06, 0.0025004999999999997, {}\n".format("Br", point))

point = magnetic.local_values(1e-06, 0.00375025)["Brz"]
f.write("{}, 1e-06, 0.00375025, {}\n".format("Bz", point))

point = magnetic.local_values(1e-06, 0.00375025)["Brr"]
f.write("{}, 1e-06, 0.00375025, {}\n".format("Br", point))

point = magnetic.local_values(1e-06, 0.005)["Brz"]
f.write("{}, 1e-06, 0.005, {}\n".format("Bz", point))

point = magnetic.local_values(1e-06, 0.005)["Brr"]
f.write("{}, 1e-06, 0.005, {}\n".format("Br", point))

point = magnetic.local_values(0.0005564444444444444, 1e-06)["Brz"]
f.write("{}, 0.0005564444444444444, 1e-06, {}\n".format("Bz", point))

point = magnetic.local_values(0.0005564444444444444, 1e-06)["Brr"]
f.write("{}, 0.0005564444444444444, 1e-06, {}\n".format("Br", point))

point = magnetic.local_values(0.0005564444444444444, 0.00125075)["Brz"]
f.write("{}, 0.0005564444444444444, 0.00125075, {}\n".format("Bz", point))

point = magnetic.local_values(0.0005564444444444444, 0.00125075)["Brr"]
f.write("{}, 0.0005564444444444444, 0.00125075, {}\n".format("Br", point))

point = magnetic.local_values(0.0005564444444444444, 0.0025004999999999997)["Brz"]
f.write("{}, 0.0005564444444444444, 0.0025004999999999997, {}\n".format("Bz", point))

point = magnetic.local_values(0.0005564444444444444, 0.0025004999999999997)["Brr"]
f.write("{}, 0.0005564444444444444, 0.0025004999999999997, {}\n".format("Br", point))

point = magnetic.local_values(0.0005564444444444444, 0.00375025)["Brz"]
f.write("{}, 0.0005564444444444444, 0.00375025, {}\n".format("Bz", point))

point = magnetic.local_values(0.0005564444444444444, 0.00375025)["Brr"]
f.write("{}, 0.0005564444444444444, 0.00375025, {}\n".format("Br", point))

point = magnetic.local_values(0.0005564444444444444, 0.005)["Brz"]
f.write("{}, 0.0005564444444444444, 0.005, {}\n".format("Bz", point))

point = magnetic.local_values(0.0005564444444444444, 0.005)["Brr"]
f.write("{}, 0.0005564444444444444, 0.005, {}\n".format("Br", point))

point = magnetic.local_values(0.0011118888888888888, 1e-06)["Brz"]
f.write("{}, 0.0011118888888888888, 1e-06, {}\n".format("Bz", point))

point = magnetic.local_values(0.0011118888888888888, 1e-06)["Brr"]
f.write("{}, 0.0011118888888888888, 1e-06, {}\n".format("Br", point))

point = magnetic.local_values(0.0011118888888888888, 0.00125075)["Brz"]
f.write("{}, 0.0011118888888888888, 0.00125075, {}\n".format("Bz", point))

point = magnetic.local_values(0.0011118888888888888, 0.00125075)["Brr"]
f.write("{}, 0.0011118888888888888, 0.00125075, {}\n".format("Br", point))

point = magnetic.local_values(0.0011118888888888888, 0.0025004999999999997)["Brz"]
f.write("{}, 0.0011118888888888888, 0.0025004999999999997, {}\n".format("Bz", point))

point = magnetic.local_values(0.0011118888888888888, 0.0025004999999999997)["Brr"]
f.write("{}, 0.0011118888888888888, 0.0025004999999999997, {}\n".format("Br", point))

point = magnetic.local_values(0.0011118888888888888, 0.00375025)["Brz"]
f.write("{}, 0.0011118888888888888, 0.00375025, {}\n".format("Bz", point))

point = magnetic.local_values(0.0011118888888888888, 0.00375025)["Brr"]
f.write("{}, 0.0011118888888888888, 0.00375025, {}\n".format("Br", point))

point = magnetic.local_values(0.0011118888888888888, 0.005)["Brz"]
f.write("{}, 0.0011118888888888888, 0.005, {}\n".format("Bz", point))

point = magnetic.local_values(0.0011118888888888888, 0.005)["Brr"]
f.write("{}, 0.0011118888888888888, 0.005, {}\n".format("Br", point))

point = magnetic.local_values(0.0016673333333333332, 1e-06)["Brz"]
f.write("{}, 0.0016673333333333332, 1e-06, {}\n".format("Bz", point))

point = magnetic.local_values(0.0016673333333333332, 1e-06)["Brr"]
f.write("{}, 0.0016673333333333332, 1e-06, {}\n".format("Br", point))

point = magnetic.local_values(0.0016673333333333332, 0.00125075)["Brz"]
f.write("{}, 0.0016673333333333332, 0.00125075, {}\n".format("Bz", point))

point = magnetic.local_values(0.0016673333333333332, 0.00125075)["Brr"]
f.write("{}, 0.0016673333333333332, 0.00125075, {}\n".format("Br", point))

point = magnetic.local_values(0.0016673333333333332, 0.0025004999999999997)["Brz"]
f.write("{}, 0.0016673333333333332, 0.0025004999999999997, {}\n".format("Bz", point))

point = magnetic.local_values(0.0016673333333333332, 0.0025004999999999997)["Brr"]
f.write("{}, 0.0016673333333333332, 0.0025004999999999997, {}\n".format("Br", point))

point = magnetic.local_values(0.0016673333333333332, 0.00375025)["Brz"]
f.write("{}, 0.0016673333333333332, 0.00375025, {}\n".format("Bz", point))

point = magnetic.local_values(0.0016673333333333332, 0.00375025)["Brr"]
f.write("{}, 0.0016673333333333332, 0.00375025, {}\n".format("Br", point))

point = magnetic.local_values(0.0016673333333333332, 0.005)["Brz"]
f.write("{}, 0.0016673333333333332, 0.005, {}\n".format("Bz", point))

point = magnetic.local_values(0.0016673333333333332, 0.005)["Brr"]
f.write("{}, 0.0016673333333333332, 0.005, {}\n".format("Br", point))

point = magnetic.local_values(0.0022227777777777775, 1e-06)["Brz"]
f.write("{}, 0.0022227777777777775, 1e-06, {}\n".format("Bz", point))

point = magnetic.local_values(0.0022227777777777775, 1e-06)["Brr"]
f.write("{}, 0.0022227777777777775, 1e-06, {}\n".format("Br", point))

point = magnetic.local_values(0.0022227777777777775, 0.00125075)["Brz"]
f.write("{}, 0.0022227777777777775, 0.00125075, {}\n".format("Bz", point))

point = magnetic.local_values(0.0022227777777777775, 0.00125075)["Brr"]
f.write("{}, 0.0022227777777777775, 0.00125075, {}\n".format("Br", point))

point = magnetic.local_values(0.0022227777777777775, 0.0025004999999999997)["Brz"]
f.write("{}, 0.0022227777777777775, 0.0025004999999999997, {}\n".format("Bz", point))

point = magnetic.local_values(0.0022227777777777775, 0.0025004999999999997)["Brr"]
f.write("{}, 0.0022227777777777775, 0.0025004999999999997, {}\n".format("Br", point))

point = magnetic.local_values(0.0022227777777777775, 0.00375025)["Brz"]
f.write("{}, 0.0022227777777777775, 0.00375025, {}\n".format("Bz", point))

point = magnetic.local_values(0.0022227777777777775, 0.00375025)["Brr"]
f.write("{}, 0.0022227777777777775, 0.00375025, {}\n".format("Br", point))

point = magnetic.local_values(0.0022227777777777775, 0.005)["Brz"]
f.write("{}, 0.0022227777777777775, 0.005, {}\n".format("Bz", point))

point = magnetic.local_values(0.0022227777777777775, 0.005)["Brr"]
f.write("{}, 0.0022227777777777775, 0.005, {}\n".format("Br", point))

point = magnetic.local_values(0.002778222222222222, 1e-06)["Brz"]
f.write("{}, 0.002778222222222222, 1e-06, {}\n".format("Bz", point))

point = magnetic.local_values(0.002778222222222222, 1e-06)["Brr"]
f.write("{}, 0.002778222222222222, 1e-06, {}\n".format("Br", point))

point = magnetic.local_values(0.002778222222222222, 0.00125075)["Brz"]
f.write("{}, 0.002778222222222222, 0.00125075, {}\n".format("Bz", point))

point = magnetic.local_values(0.002778222222222222, 0.00125075)["Brr"]
f.write("{}, 0.002778222222222222, 0.00125075, {}\n".format("Br", point))

point = magnetic.local_values(0.002778222222222222, 0.0025004999999999997)["Brz"]
f.write("{}, 0.002778222222222222, 0.0025004999999999997, {}\n".format("Bz", point))

point = magnetic.local_values(0.002778222222222222, 0.0025004999999999997)["Brr"]
f.write("{}, 0.002778222222222222, 0.0025004999999999997, {}\n".format("Br", point))

point = magnetic.local_values(0.002778222222222222, 0.00375025)["Brz"]
f.write("{}, 0.002778222222222222, 0.00375025, {}\n".format("Bz", point))

point = magnetic.local_values(0.002778222222222222, 0.00375025)["Brr"]
f.write("{}, 0.002778222222222222, 0.00375025, {}\n".format("Br", point))

point = magnetic.local_values(0.002778222222222222, 0.005)["Brz"]
f.write("{}, 0.002778222222222222, 0.005, {}\n".format("Bz", point))

point = magnetic.local_values(0.002778222222222222, 0.005)["Brr"]
f.write("{}, 0.002778222222222222, 0.005, {}\n".format("Br", point))

point = magnetic.local_values(0.003333666666666666, 1e-06)["Brz"]
f.write("{}, 0.003333666666666666, 1e-06, {}\n".format("Bz", point))

point = magnetic.local_values(0.003333666666666666, 1e-06)["Brr"]
f.write("{}, 0.003333666666666666, 1e-06, {}\n".format("Br", point))

point = magnetic.local_values(0.003333666666666666, 0.00125075)["Brz"]
f.write("{}, 0.003333666666666666, 0.00125075, {}\n".format("Bz", point))

point = magnetic.local_values(0.003333666666666666, 0.00125075)["Brr"]
f.write("{}, 0.003333666666666666, 0.00125075, {}\n".format("Br", point))

point = magnetic.local_values(0.003333666666666666, 0.0025004999999999997)["Brz"]
f.write("{}, 0.003333666666666666, 0.0025004999999999997, {}\n".format("Bz", point))

point = magnetic.local_values(0.003333666666666666, 0.0025004999999999997)["Brr"]
f.write("{}, 0.003333666666666666, 0.0025004999999999997, {}\n".format("Br", point))

point = magnetic.local_values(0.003333666666666666, 0.00375025)["Brz"]
f.write("{}, 0.003333666666666666, 0.00375025, {}\n".format("Bz", point))

point = magnetic.local_values(0.003333666666666666, 0.00375025)["Brr"]
f.write("{}, 0.003333666666666666, 0.00375025, {}\n".format("Br", point))

point = magnetic.local_values(0.003333666666666666, 0.005)["Brz"]
f.write("{}, 0.003333666666666666, 0.005, {}\n".format("Bz", point))

point = magnetic.local_values(0.003333666666666666, 0.005)["Brr"]
f.write("{}, 0.003333666666666666, 0.005, {}\n".format("Br", point))

point = magnetic.local_values(0.003889111111111111, 1e-06)["Brz"]
f.write("{}, 0.003889111111111111, 1e-06, {}\n".format("Bz", point))

point = magnetic.local_values(0.003889111111111111, 1e-06)["Brr"]
f.write("{}, 0.003889111111111111, 1e-06, {}\n".format("Br", point))

point = magnetic.local_values(0.003889111111111111, 0.00125075)["Brz"]
f.write("{}, 0.003889111111111111, 0.00125075, {}\n".format("Bz", point))

point = magnetic.local_values(0.003889111111111111, 0.00125075)["Brr"]
f.write("{}, 0.003889111111111111, 0.00125075, {}\n".format("Br", point))

point = magnetic.local_values(0.003889111111111111, 0.0025004999999999997)["Brz"]
f.write("{}, 0.003889111111111111, 0.0025004999999999997, {}\n".format("Bz", point))

point = magnetic.local_values(0.003889111111111111, 0.0025004999999999997)["Brr"]
f.write("{}, 0.003889111111111111, 0.0025004999999999997, {}\n".format("Br", point))

point = magnetic.local_values(0.003889111111111111, 0.00375025)["Brz"]
f.write("{}, 0.003889111111111111, 0.00375025, {}\n".format("Bz", point))

point = magnetic.local_values(0.003889111111111111, 0.00375025)["Brr"]
f.write("{}, 0.003889111111111111, 0.00375025, {}\n".format("Br", point))

point = magnetic.local_values(0.003889111111111111, 0.005)["Brz"]
f.write("{}, 0.003889111111111111, 0.005, {}\n".format("Bz", point))

point = magnetic.local_values(0.003889111111111111, 0.005)["Brr"]
f.write("{}, 0.003889111111111111, 0.005, {}\n".format("Br", point))

point = magnetic.local_values(0.004444555555555556, 1e-06)["Brz"]
f.write("{}, 0.004444555555555556, 1e-06, {}\n".format("Bz", point))

point = magnetic.local_values(0.004444555555555556, 1e-06)["Brr"]
f.write("{}, 0.004444555555555556, 1e-06, {}\n".format("Br", point))

point = magnetic.local_values(0.004444555555555556, 0.00125075)["Brz"]
f.write("{}, 0.004444555555555556, 0.00125075, {}\n".format("Bz", point))

point = magnetic.local_values(0.004444555555555556, 0.00125075)["Brr"]
f.write("{}, 0.004444555555555556, 0.00125075, {}\n".format("Br", point))

point = magnetic.local_values(0.004444555555555556, 0.0025004999999999997)["Brz"]
f.write("{}, 0.004444555555555556, 0.0025004999999999997, {}\n".format("Bz", point))

point = magnetic.local_values(0.004444555555555556, 0.0025004999999999997)["Brr"]
f.write("{}, 0.004444555555555556, 0.0025004999999999997, {}\n".format("Br", point))

point = magnetic.local_values(0.004444555555555556, 0.00375025)["Brz"]
f.write("{}, 0.004444555555555556, 0.00375025, {}\n".format("Bz", point))

point = magnetic.local_values(0.004444555555555556, 0.00375025)["Brr"]
f.write("{}, 0.004444555555555556, 0.00375025, {}\n".format("Br", point))

point = magnetic.local_values(0.004444555555555556, 0.005)["Brz"]
f.write("{}, 0.004444555555555556, 0.005, {}\n".format("Bz", point))

point = magnetic.local_values(0.004444555555555556, 0.005)["Brr"]
f.write("{}, 0.004444555555555556, 0.005, {}\n".format("Br", point))

point = magnetic.local_values(0.005, 1e-06)["Brz"]
f.write("{}, 0.005, 1e-06, {}\n".format("Bz", point))

point = magnetic.local_values(0.005, 1e-06)["Brr"]
f.write("{}, 0.005, 1e-06, {}\n".format("Br", point))

point = magnetic.local_values(0.005, 0.00125075)["Brz"]
f.write("{}, 0.005, 0.00125075, {}\n".format("Bz", point))

point = magnetic.local_values(0.005, 0.00125075)["Brr"]
f.write("{}, 0.005, 0.00125075, {}\n".format("Br", point))

point = magnetic.local_values(0.005, 0.0025004999999999997)["Brz"]
f.write("{}, 0.005, 0.0025004999999999997, {}\n".format("Bz", point))

point = magnetic.local_values(0.005, 0.0025004999999999997)["Brr"]
f.write("{}, 0.005, 0.0025004999999999997, {}\n".format("Br", point))

point = magnetic.local_values(0.005, 0.00375025)["Brz"]
f.write("{}, 0.005, 0.00375025, {}\n".format("Bz", point))

point = magnetic.local_values(0.005, 0.00375025)["Brr"]
f.write("{}, 0.005, 0.00375025, {}\n".format("Br", point))

point = magnetic.local_values(0.005, 0.005)["Brz"]
f.write("{}, 0.005, 0.005, {}\n".format("Bz", point))

point = magnetic.local_values(0.005, 0.005)["Brr"]
f.write("{}, 0.005, 0.005, {}\n".format("Br", point))

info = magnetic.solution_mesh_info()
f.write("{}, {}\n".format("dofs", info["dofs"]))
f.write("{}, {}\n".format("nodes", info["nodes"]))
f.write("{}, {}\n".format("elements", info["elements"]))

# CLOSING STEPS
f.close()
