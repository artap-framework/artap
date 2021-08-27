import agros2d as a2d

# PROBLEM
problem = a2d.problem(clear=True)
problem.coordinate_type = "axisymmetric"
problem.mesh_type = "triangle"

magnetic = a2d.field("magnetic")
magnetic.analysis_type = "steadystate"
magnetic.number_of_refinements = 0
magnetic.polynomial_order = 2
magnetic.solver = "linear"

geometry = a2d.geometry

magnetic.adaptivity_type = "hp-adaptivity"
magnetic.adaptivity_parameters["tolerance"] = 1
magnetic.adaptivity_parameters["steps"] = 10

# MATERIAL DEFINITIONS
magnetic.add_material("J+", {'magnetic_remanence_angle': 0.0, 'magnetic_velocity_y': 0.0, 'magnetic_current_density_external_real': 2000000.0, 'magnetic_permeability': 1.0, 'magnetic_conductivity': 0.0, 'magnetic_remanence': 0.0, 'magnetic_velocity_angular': 0.0, 'magnetic_velocity_x': 0.0})
magnetic.add_material("air", {'magnetic_remanence_angle': 0.0, 'magnetic_velocity_y': 0.0, 'magnetic_current_density_external_real': 0.0, 'magnetic_permeability': 1.0, 'magnetic_conductivity': 0.0, 'magnetic_remanence': 0.0, 'magnetic_velocity_angular': 0.0, 'magnetic_velocity_x': 0.0})
magnetic.add_material("control", {'magnetic_remanence_angle': 0.0, 'magnetic_velocity_y': 0.0, 'magnetic_current_density_external_real': 0.0, 'magnetic_permeability': 1.0, 'magnetic_conductivity': 0.0, 'magnetic_remanence': 0.0, 'magnetic_velocity_angular': 0.0, 'magnetic_velocity_x': 0.0})

# BOUNDARY DEFINITIONS
magnetic.add_boundary("a0", "magnetic_potential", {'magnetic_potential_real': 0.0})

# GEOMETRY
geometry.add_edge(0.0, 0.035, 0.07, 0.035, boundaries={'magnetic': 'a0'})
geometry.add_edge(0.0, -0.035, 0.0, -0.005, boundaries={'magnetic': 'a0'})
geometry.add_edge(0.07, -0.035, 0.0, -0.035, boundaries={'magnetic': 'a0'})
geometry.add_edge(0.0, 0.005, 0.0, 0.035, boundaries={'magnetic': 'a0'})
geometry.add_edge(0.0, -0.005, 0.0, 0.005, boundaries={'magnetic': 'a0'})
geometry.add_edge(0.07, 0.035, 0.07, -0.035, boundaries={'magnetic': 'a0'})
geometry.add_edge(0.0, 0.005, 0.005, 0.005)
geometry.add_edge(0.005, 0.005, 0.005, -0.005)
geometry.add_edge(0.005, -0.005, 0.0, -0.005)
geometry.add_edge(0.00116, -0.0135, 0.0021200000000000012, -0.0135)
geometry.add_edge(0.0021200000000000012, -0.0135, 0.00216, -0.0135)
geometry.add_edge(0.00216, -0.0135, 0.00216, -0.015)
geometry.add_edge(0.00216, -0.015, 0.00116, -0.015)
geometry.add_edge(0.00116, -0.015, 0.00116, -0.0135)
geometry.add_edge(0.0011200000000000001, -0.012, 0.0020100000000000005, -0.012)
geometry.add_edge(0.0020100000000000005, -0.012, 0.0021200000000000004, -0.012)
geometry.add_edge(0.0021200000000000004, -0.012, 0.0021200000000000004, -0.0135)
geometry.add_edge(0.0011600000000000007, -0.0135, 0.0011200000000000001, -0.0135)
geometry.add_edge(0.0011200000000000001, -0.0135, 0.0011200000000000001, -0.012)
geometry.add_edge(0.00101, -0.0105, 0.001669999999999999, -0.0105)
geometry.add_edge(0.001669999999999999, -0.0105, 0.0020099999999999996, -0.0105)
geometry.add_edge(0.0020099999999999996, -0.0105, 0.0020099999999999996, -0.012)
geometry.add_edge(0.0011200000000000006, -0.012, 0.00101, -0.012)
geometry.add_edge(0.00101, -0.012, 0.00101, -0.0105)
geometry.add_edge(0.00167, -0.009000000000000001, 0.002149999999999999, -0.009000000000000001)
geometry.add_edge(0.002149999999999999, -0.009000000000000001, 0.00267, -0.009000000000000001)
geometry.add_edge(0.00267, -0.009000000000000001, 0.00267, -0.0105)
geometry.add_edge(0.00267, -0.0105, 0.0020100000000000014, -0.0105)
geometry.add_edge(0.00167, -0.0105, 0.00167, -0.009000000000000001)
geometry.add_edge(0.00115, -0.0075, 0.00215, -0.0075)
geometry.add_edge(0.00215, -0.0075, 0.00215, -0.009000000000000001)
geometry.add_edge(0.001669999999999999, -0.009000000000000001, 0.00115, -0.009000000000000001)
geometry.add_edge(0.00115, -0.009000000000000001, 0.00115, -0.0075)
geometry.add_edge(0.00435, -0.006, 0.00535, -0.006)
geometry.add_edge(0.00535, -0.006, 0.00535, -0.0075)
geometry.add_edge(0.00535, -0.0075, 0.00435, -0.0075)
geometry.add_edge(0.00435, -0.0075, 0.00435, -0.006)
geometry.add_edge(0.00584, -0.0045000000000000005, 0.00607, -0.0045000000000000005)
geometry.add_edge(0.00607, -0.0045000000000000005, 0.00684, -0.0045000000000000005)
geometry.add_edge(0.00684, -0.0045000000000000005, 0.00684, -0.006)
geometry.add_edge(0.00684, -0.006, 0.00584, -0.006)
geometry.add_edge(0.00584, -0.006, 0.00584, -0.0045000000000000005)
geometry.add_edge(0.006070000000000001, -0.003, 0.00696, -0.003)
geometry.add_edge(0.00696, -0.003, 0.007070000000000001, -0.003)
geometry.add_edge(0.007070000000000001, -0.003, 0.007070000000000001, -0.0045000000000000005)
geometry.add_edge(0.007070000000000001, -0.0045000000000000005, 0.006839999999999996, -0.0045000000000000005)
geometry.add_edge(0.006070000000000001, -0.0045000000000000005, 0.006070000000000001, -0.003)
geometry.add_edge(0.00596, -0.0015, 0.00671, -0.0015)
geometry.add_edge(0.00671, -0.0015, 0.00696, -0.0015)
geometry.add_edge(0.00696, -0.0015, 0.00696, -0.003)
geometry.add_edge(0.00607, -0.003, 0.00596, -0.003)
geometry.add_edge(0.00596, -0.003, 0.00596, -0.0015)
geometry.add_edge(0.00671, 0.0, 0.007080000000000001, 0.0)
geometry.add_edge(0.007080000000000001, 0.0, 0.00771, 0.0)
geometry.add_edge(0.00771, 0.0, 0.00771, -0.0015)
geometry.add_edge(0.00771, -0.0015, 0.00696, -0.0015)
geometry.add_edge(0.00671, -0.0015, 0.00671, 0.0)
geometry.add_edge(0.00608, 0.0015, 0.006489999999999999, 0.0015)
geometry.add_edge(0.006489999999999999, 0.0015, 0.00708, 0.0015)
geometry.add_edge(0.00708, 0.0015, 0.00708, 0.0)
geometry.add_edge(0.006709999999999999, 0.0, 0.00608, 0.0)
geometry.add_edge(0.00608, 0.0, 0.00608, 0.0015)
geometry.add_edge(0.00649, 0.003, 0.007380000000000001, 0.003)
geometry.add_edge(0.007380000000000001, 0.003, 0.00749, 0.003)
geometry.add_edge(0.00749, 0.003, 0.00749, 0.0015)
geometry.add_edge(0.00749, 0.0015, 0.007080000000000001, 0.0015)
geometry.add_edge(0.00649, 0.0015, 0.00649, 0.003)
geometry.add_edge(0.00638, 0.0045000000000000005, 0.006940000000000002, 0.0045000000000000005)
geometry.add_edge(0.006940000000000002, 0.0045000000000000005, 0.00738, 0.0045000000000000005)
geometry.add_edge(0.00738, 0.0045000000000000005, 0.00738, 0.003)
geometry.add_edge(0.006489999999999999, 0.003, 0.00638, 0.003)
geometry.add_edge(0.00638, 0.003, 0.00638, 0.0045000000000000005)
geometry.add_edge(0.0059400000000000034, 0.006, 0.006940000000000001, 0.006)
geometry.add_edge(0.006940000000000001, 0.006, 0.006940000000000001, 0.0045000000000000005)
geometry.add_edge(0.0063799999999999985, 0.0045000000000000005, 0.005940000000000001, 0.0045000000000000005)
geometry.add_edge(0.005940000000000001, 0.0045000000000000005, 0.005940000000000001, 0.006)
geometry.add_edge(0.0013000000000000002, 0.0075, 0.002300000000000001, 0.0075)
geometry.add_edge(0.0023, 0.0075, 0.0023, 0.006)
geometry.add_edge(0.0023, 0.006, 0.0013000000000000002, 0.006)
geometry.add_edge(0.0013000000000000002, 0.006, 0.0013000000000000002, 0.0075)
geometry.add_edge(0.00315, 0.009000000000000001, 0.00415, 0.009000000000000001)
geometry.add_edge(0.00415, 0.009000000000000001, 0.00415, 0.0075)
geometry.add_edge(0.00415, 0.0075, 0.00315, 0.0075)
geometry.add_edge(0.00315, 0.0075, 0.00315, 0.009000000000000001)
geometry.add_edge(0.00117, 0.0105, 0.0020800000000000016, 0.0105)
geometry.add_edge(0.0020800000000000016, 0.0105, 0.00217, 0.0105)
geometry.add_edge(0.00217, 0.0105, 0.00217, 0.009000000000000001)
geometry.add_edge(0.00217, 0.009000000000000001, 0.00117, 0.009000000000000001)
geometry.add_edge(0.00117, 0.009000000000000001, 0.00117, 0.0105)
geometry.add_edge(0.00108, 0.012, 0.002029999999999998, 0.012)
geometry.add_edge(0.002029999999999998, 0.012, 0.0020800000000000003, 0.012)
geometry.add_edge(0.0020800000000000003, 0.012, 0.0020800000000000003, 0.0105)
geometry.add_edge(0.0011700000000000011, 0.0105, 0.00108, 0.0105)
geometry.add_edge(0.00108, 0.0105, 0.00108, 0.012)
geometry.add_edge(0.00103, 0.0135, 0.002000000000000001, 0.0135)
geometry.add_edge(0.002000000000000001, 0.0135, 0.0020299999999999997, 0.0135)
geometry.add_edge(0.0020299999999999997, 0.0135, 0.0020299999999999997, 0.012)
geometry.add_edge(0.0010800000000000004, 0.012, 0.00103, 0.012)
geometry.add_edge(0.00103, 0.012, 0.00103, 0.0135)
geometry.add_edge(0.001, 0.015, 0.002, 0.015)
geometry.add_edge(0.002, 0.015, 0.002, 0.0135)
geometry.add_edge(0.0010300000000000012, 0.0135, 0.001, 0.0135)
geometry.add_edge(0.001, 0.0135, 0.001, 0.015)

# BLOCK LABELS
geometry.add_label(0.00191, -0.01425, materials = {'magnetic' : 'J+'})
geometry.add_label(0.0018700000000000001, -0.012750000000000001, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00176, -0.01125, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00242, -0.00975, materials = {'magnetic' : 'J+'})
geometry.add_label(0.0019, -0.00825, materials = {'magnetic' : 'J+'})
geometry.add_label(0.0050999999999999995, -0.00675, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00659, -0.00525, materials = {'magnetic' : 'J+'})
geometry.add_label(0.0068200000000000005, -0.00375, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00671, -0.0022500000000000003, materials = {'magnetic' : 'J+'})
geometry.add_label(0.0074600000000000005, -0.00075, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00683, 0.00075, materials = {'magnetic' : 'J+'})
geometry.add_label(0.007240000000000001, 0.0022500000000000003, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00713, 0.00375, materials = {'magnetic' : 'J+'})
geometry.add_label(0.006690000000000001, 0.00525, materials = {'magnetic' : 'J+'})
geometry.add_label(0.0020499999999999997, 0.00675, materials = {'magnetic' : 'J+'})
geometry.add_label(0.0039, 0.00825, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00192, 0.00975, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00183, 0.01125, materials = {'magnetic' : 'J+'})
geometry.add_label(0.0017800000000000001, 0.012750000000000001, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00175, 0.01425, materials = {'magnetic' : 'J+'})
geometry.add_label(0.03, 0.03, materials = {'magnetic' : 'air'})
geometry.add_label(0.003, 0.0, materials = {'magnetic' : 'control'})

# SOLVE
problem.solve()
a2d.view.zoom_best_fit()
f = open("solution_0.csv", "w")

# POSTPROCESSING AND EXPORTING
point = magnetic.local_values(1e-06, -0.005)["Brz"]
f.write("{}, 1e-06, -0.005, {}\n".format("Bz", point))

point = magnetic.local_values(1e-06, -0.005)["Brr"]
f.write("{}, 1e-06, -0.005, {}\n".format("Br", point))

point = magnetic.local_values(1e-06, -0.0038888888888888888)["Brz"]
f.write("{}, 1e-06, -0.0038888888888888888, {}\n".format("Bz", point))

point = magnetic.local_values(1e-06, -0.0038888888888888888)["Brr"]
f.write("{}, 1e-06, -0.0038888888888888888, {}\n".format("Br", point))

point = magnetic.local_values(1e-06, -0.002777777777777778)["Brz"]
f.write("{}, 1e-06, -0.002777777777777778, {}\n".format("Bz", point))

point = magnetic.local_values(1e-06, -0.002777777777777778)["Brr"]
f.write("{}, 1e-06, -0.002777777777777778, {}\n".format("Br", point))

point = magnetic.local_values(1e-06, -0.0016666666666666666)["Brz"]
f.write("{}, 1e-06, -0.0016666666666666666, {}\n".format("Bz", point))

point = magnetic.local_values(1e-06, -0.0016666666666666666)["Brr"]
f.write("{}, 1e-06, -0.0016666666666666666, {}\n".format("Br", point))

point = magnetic.local_values(1e-06, -0.0005555555555555553)["Brz"]
f.write("{}, 1e-06, -0.0005555555555555553, {}\n".format("Bz", point))

point = magnetic.local_values(1e-06, -0.0005555555555555553)["Brr"]
f.write("{}, 1e-06, -0.0005555555555555553, {}\n".format("Br", point))

point = magnetic.local_values(1e-06, 0.0005555555555555553)["Brz"]
f.write("{}, 1e-06, 0.0005555555555555553, {}\n".format("Bz", point))

point = magnetic.local_values(1e-06, 0.0005555555555555553)["Brr"]
f.write("{}, 1e-06, 0.0005555555555555553, {}\n".format("Br", point))

point = magnetic.local_values(1e-06, 0.001666666666666667)["Brz"]
f.write("{}, 1e-06, 0.001666666666666667, {}\n".format("Bz", point))

point = magnetic.local_values(1e-06, 0.001666666666666667)["Brr"]
f.write("{}, 1e-06, 0.001666666666666667, {}\n".format("Br", point))

point = magnetic.local_values(1e-06, 0.0027777777777777788)["Brz"]
f.write("{}, 1e-06, 0.0027777777777777788, {}\n".format("Bz", point))

point = magnetic.local_values(1e-06, 0.0027777777777777788)["Brr"]
f.write("{}, 1e-06, 0.0027777777777777788, {}\n".format("Br", point))

point = magnetic.local_values(1e-06, 0.003888888888888889)["Brz"]
f.write("{}, 1e-06, 0.003888888888888889, {}\n".format("Bz", point))

point = magnetic.local_values(1e-06, 0.003888888888888889)["Brr"]
f.write("{}, 1e-06, 0.003888888888888889, {}\n".format("Br", point))

point = magnetic.local_values(1e-06, 0.005)["Brz"]
f.write("{}, 1e-06, 0.005, {}\n".format("Bz", point))

point = magnetic.local_values(1e-06, 0.005)["Brr"]
f.write("{}, 1e-06, 0.005, {}\n".format("Br", point))

point = magnetic.local_values(0.0005564444444444444, -0.005)["Brz"]
f.write("{}, 0.0005564444444444444, -0.005, {}\n".format("Bz", point))

point = magnetic.local_values(0.0005564444444444444, -0.005)["Brr"]
f.write("{}, 0.0005564444444444444, -0.005, {}\n".format("Br", point))

point = magnetic.local_values(0.0005564444444444444, -0.0038888888888888888)["Brz"]
f.write("{}, 0.0005564444444444444, -0.0038888888888888888, {}\n".format("Bz", point))

point = magnetic.local_values(0.0005564444444444444, -0.0038888888888888888)["Brr"]
f.write("{}, 0.0005564444444444444, -0.0038888888888888888, {}\n".format("Br", point))

point = magnetic.local_values(0.0005564444444444444, -0.002777777777777778)["Brz"]
f.write("{}, 0.0005564444444444444, -0.002777777777777778, {}\n".format("Bz", point))

point = magnetic.local_values(0.0005564444444444444, -0.002777777777777778)["Brr"]
f.write("{}, 0.0005564444444444444, -0.002777777777777778, {}\n".format("Br", point))

point = magnetic.local_values(0.0005564444444444444, -0.0016666666666666666)["Brz"]
f.write("{}, 0.0005564444444444444, -0.0016666666666666666, {}\n".format("Bz", point))

point = magnetic.local_values(0.0005564444444444444, -0.0016666666666666666)["Brr"]
f.write("{}, 0.0005564444444444444, -0.0016666666666666666, {}\n".format("Br", point))

point = magnetic.local_values(0.0005564444444444444, -0.0005555555555555553)["Brz"]
f.write("{}, 0.0005564444444444444, -0.0005555555555555553, {}\n".format("Bz", point))

point = magnetic.local_values(0.0005564444444444444, -0.0005555555555555553)["Brr"]
f.write("{}, 0.0005564444444444444, -0.0005555555555555553, {}\n".format("Br", point))

point = magnetic.local_values(0.0005564444444444444, 0.0005555555555555553)["Brz"]
f.write("{}, 0.0005564444444444444, 0.0005555555555555553, {}\n".format("Bz", point))

point = magnetic.local_values(0.0005564444444444444, 0.0005555555555555553)["Brr"]
f.write("{}, 0.0005564444444444444, 0.0005555555555555553, {}\n".format("Br", point))

point = magnetic.local_values(0.0005564444444444444, 0.001666666666666667)["Brz"]
f.write("{}, 0.0005564444444444444, 0.001666666666666667, {}\n".format("Bz", point))

point = magnetic.local_values(0.0005564444444444444, 0.001666666666666667)["Brr"]
f.write("{}, 0.0005564444444444444, 0.001666666666666667, {}\n".format("Br", point))

point = magnetic.local_values(0.0005564444444444444, 0.0027777777777777788)["Brz"]
f.write("{}, 0.0005564444444444444, 0.0027777777777777788, {}\n".format("Bz", point))

point = magnetic.local_values(0.0005564444444444444, 0.0027777777777777788)["Brr"]
f.write("{}, 0.0005564444444444444, 0.0027777777777777788, {}\n".format("Br", point))

point = magnetic.local_values(0.0005564444444444444, 0.003888888888888889)["Brz"]
f.write("{}, 0.0005564444444444444, 0.003888888888888889, {}\n".format("Bz", point))

point = magnetic.local_values(0.0005564444444444444, 0.003888888888888889)["Brr"]
f.write("{}, 0.0005564444444444444, 0.003888888888888889, {}\n".format("Br", point))

point = magnetic.local_values(0.0005564444444444444, 0.005)["Brz"]
f.write("{}, 0.0005564444444444444, 0.005, {}\n".format("Bz", point))

point = magnetic.local_values(0.0005564444444444444, 0.005)["Brr"]
f.write("{}, 0.0005564444444444444, 0.005, {}\n".format("Br", point))

point = magnetic.local_values(0.0011118888888888888, -0.005)["Brz"]
f.write("{}, 0.0011118888888888888, -0.005, {}\n".format("Bz", point))

point = magnetic.local_values(0.0011118888888888888, -0.005)["Brr"]
f.write("{}, 0.0011118888888888888, -0.005, {}\n".format("Br", point))

point = magnetic.local_values(0.0011118888888888888, -0.0038888888888888888)["Brz"]
f.write("{}, 0.0011118888888888888, -0.0038888888888888888, {}\n".format("Bz", point))

point = magnetic.local_values(0.0011118888888888888, -0.0038888888888888888)["Brr"]
f.write("{}, 0.0011118888888888888, -0.0038888888888888888, {}\n".format("Br", point))

point = magnetic.local_values(0.0011118888888888888, -0.002777777777777778)["Brz"]
f.write("{}, 0.0011118888888888888, -0.002777777777777778, {}\n".format("Bz", point))

point = magnetic.local_values(0.0011118888888888888, -0.002777777777777778)["Brr"]
f.write("{}, 0.0011118888888888888, -0.002777777777777778, {}\n".format("Br", point))

point = magnetic.local_values(0.0011118888888888888, -0.0016666666666666666)["Brz"]
f.write("{}, 0.0011118888888888888, -0.0016666666666666666, {}\n".format("Bz", point))

point = magnetic.local_values(0.0011118888888888888, -0.0016666666666666666)["Brr"]
f.write("{}, 0.0011118888888888888, -0.0016666666666666666, {}\n".format("Br", point))

point = magnetic.local_values(0.0011118888888888888, -0.0005555555555555553)["Brz"]
f.write("{}, 0.0011118888888888888, -0.0005555555555555553, {}\n".format("Bz", point))

point = magnetic.local_values(0.0011118888888888888, -0.0005555555555555553)["Brr"]
f.write("{}, 0.0011118888888888888, -0.0005555555555555553, {}\n".format("Br", point))

point = magnetic.local_values(0.0011118888888888888, 0.0005555555555555553)["Brz"]
f.write("{}, 0.0011118888888888888, 0.0005555555555555553, {}\n".format("Bz", point))

point = magnetic.local_values(0.0011118888888888888, 0.0005555555555555553)["Brr"]
f.write("{}, 0.0011118888888888888, 0.0005555555555555553, {}\n".format("Br", point))

point = magnetic.local_values(0.0011118888888888888, 0.001666666666666667)["Brz"]
f.write("{}, 0.0011118888888888888, 0.001666666666666667, {}\n".format("Bz", point))

point = magnetic.local_values(0.0011118888888888888, 0.001666666666666667)["Brr"]
f.write("{}, 0.0011118888888888888, 0.001666666666666667, {}\n".format("Br", point))

point = magnetic.local_values(0.0011118888888888888, 0.0027777777777777788)["Brz"]
f.write("{}, 0.0011118888888888888, 0.0027777777777777788, {}\n".format("Bz", point))

point = magnetic.local_values(0.0011118888888888888, 0.0027777777777777788)["Brr"]
f.write("{}, 0.0011118888888888888, 0.0027777777777777788, {}\n".format("Br", point))

point = magnetic.local_values(0.0011118888888888888, 0.003888888888888889)["Brz"]
f.write("{}, 0.0011118888888888888, 0.003888888888888889, {}\n".format("Bz", point))

point = magnetic.local_values(0.0011118888888888888, 0.003888888888888889)["Brr"]
f.write("{}, 0.0011118888888888888, 0.003888888888888889, {}\n".format("Br", point))

point = magnetic.local_values(0.0011118888888888888, 0.005)["Brz"]
f.write("{}, 0.0011118888888888888, 0.005, {}\n".format("Bz", point))

point = magnetic.local_values(0.0011118888888888888, 0.005)["Brr"]
f.write("{}, 0.0011118888888888888, 0.005, {}\n".format("Br", point))

point = magnetic.local_values(0.0016673333333333332, -0.005)["Brz"]
f.write("{}, 0.0016673333333333332, -0.005, {}\n".format("Bz", point))

point = magnetic.local_values(0.0016673333333333332, -0.005)["Brr"]
f.write("{}, 0.0016673333333333332, -0.005, {}\n".format("Br", point))

point = magnetic.local_values(0.0016673333333333332, -0.0038888888888888888)["Brz"]
f.write("{}, 0.0016673333333333332, -0.0038888888888888888, {}\n".format("Bz", point))

point = magnetic.local_values(0.0016673333333333332, -0.0038888888888888888)["Brr"]
f.write("{}, 0.0016673333333333332, -0.0038888888888888888, {}\n".format("Br", point))

point = magnetic.local_values(0.0016673333333333332, -0.002777777777777778)["Brz"]
f.write("{}, 0.0016673333333333332, -0.002777777777777778, {}\n".format("Bz", point))

point = magnetic.local_values(0.0016673333333333332, -0.002777777777777778)["Brr"]
f.write("{}, 0.0016673333333333332, -0.002777777777777778, {}\n".format("Br", point))

point = magnetic.local_values(0.0016673333333333332, -0.0016666666666666666)["Brz"]
f.write("{}, 0.0016673333333333332, -0.0016666666666666666, {}\n".format("Bz", point))

point = magnetic.local_values(0.0016673333333333332, -0.0016666666666666666)["Brr"]
f.write("{}, 0.0016673333333333332, -0.0016666666666666666, {}\n".format("Br", point))

point = magnetic.local_values(0.0016673333333333332, -0.0005555555555555553)["Brz"]
f.write("{}, 0.0016673333333333332, -0.0005555555555555553, {}\n".format("Bz", point))

point = magnetic.local_values(0.0016673333333333332, -0.0005555555555555553)["Brr"]
f.write("{}, 0.0016673333333333332, -0.0005555555555555553, {}\n".format("Br", point))

point = magnetic.local_values(0.0016673333333333332, 0.0005555555555555553)["Brz"]
f.write("{}, 0.0016673333333333332, 0.0005555555555555553, {}\n".format("Bz", point))

point = magnetic.local_values(0.0016673333333333332, 0.0005555555555555553)["Brr"]
f.write("{}, 0.0016673333333333332, 0.0005555555555555553, {}\n".format("Br", point))

point = magnetic.local_values(0.0016673333333333332, 0.001666666666666667)["Brz"]
f.write("{}, 0.0016673333333333332, 0.001666666666666667, {}\n".format("Bz", point))

point = magnetic.local_values(0.0016673333333333332, 0.001666666666666667)["Brr"]
f.write("{}, 0.0016673333333333332, 0.001666666666666667, {}\n".format("Br", point))

point = magnetic.local_values(0.0016673333333333332, 0.0027777777777777788)["Brz"]
f.write("{}, 0.0016673333333333332, 0.0027777777777777788, {}\n".format("Bz", point))

point = magnetic.local_values(0.0016673333333333332, 0.0027777777777777788)["Brr"]
f.write("{}, 0.0016673333333333332, 0.0027777777777777788, {}\n".format("Br", point))

point = magnetic.local_values(0.0016673333333333332, 0.003888888888888889)["Brz"]
f.write("{}, 0.0016673333333333332, 0.003888888888888889, {}\n".format("Bz", point))

point = magnetic.local_values(0.0016673333333333332, 0.003888888888888889)["Brr"]
f.write("{}, 0.0016673333333333332, 0.003888888888888889, {}\n".format("Br", point))

point = magnetic.local_values(0.0016673333333333332, 0.005)["Brz"]
f.write("{}, 0.0016673333333333332, 0.005, {}\n".format("Bz", point))

point = magnetic.local_values(0.0016673333333333332, 0.005)["Brr"]
f.write("{}, 0.0016673333333333332, 0.005, {}\n".format("Br", point))

point = magnetic.local_values(0.0022227777777777775, -0.005)["Brz"]
f.write("{}, 0.0022227777777777775, -0.005, {}\n".format("Bz", point))

point = magnetic.local_values(0.0022227777777777775, -0.005)["Brr"]
f.write("{}, 0.0022227777777777775, -0.005, {}\n".format("Br", point))

point = magnetic.local_values(0.0022227777777777775, -0.0038888888888888888)["Brz"]
f.write("{}, 0.0022227777777777775, -0.0038888888888888888, {}\n".format("Bz", point))

point = magnetic.local_values(0.0022227777777777775, -0.0038888888888888888)["Brr"]
f.write("{}, 0.0022227777777777775, -0.0038888888888888888, {}\n".format("Br", point))

point = magnetic.local_values(0.0022227777777777775, -0.002777777777777778)["Brz"]
f.write("{}, 0.0022227777777777775, -0.002777777777777778, {}\n".format("Bz", point))

point = magnetic.local_values(0.0022227777777777775, -0.002777777777777778)["Brr"]
f.write("{}, 0.0022227777777777775, -0.002777777777777778, {}\n".format("Br", point))

point = magnetic.local_values(0.0022227777777777775, -0.0016666666666666666)["Brz"]
f.write("{}, 0.0022227777777777775, -0.0016666666666666666, {}\n".format("Bz", point))

point = magnetic.local_values(0.0022227777777777775, -0.0016666666666666666)["Brr"]
f.write("{}, 0.0022227777777777775, -0.0016666666666666666, {}\n".format("Br", point))

point = magnetic.local_values(0.0022227777777777775, -0.0005555555555555553)["Brz"]
f.write("{}, 0.0022227777777777775, -0.0005555555555555553, {}\n".format("Bz", point))

point = magnetic.local_values(0.0022227777777777775, -0.0005555555555555553)["Brr"]
f.write("{}, 0.0022227777777777775, -0.0005555555555555553, {}\n".format("Br", point))

point = magnetic.local_values(0.0022227777777777775, 0.0005555555555555553)["Brz"]
f.write("{}, 0.0022227777777777775, 0.0005555555555555553, {}\n".format("Bz", point))

point = magnetic.local_values(0.0022227777777777775, 0.0005555555555555553)["Brr"]
f.write("{}, 0.0022227777777777775, 0.0005555555555555553, {}\n".format("Br", point))

point = magnetic.local_values(0.0022227777777777775, 0.001666666666666667)["Brz"]
f.write("{}, 0.0022227777777777775, 0.001666666666666667, {}\n".format("Bz", point))

point = magnetic.local_values(0.0022227777777777775, 0.001666666666666667)["Brr"]
f.write("{}, 0.0022227777777777775, 0.001666666666666667, {}\n".format("Br", point))

point = magnetic.local_values(0.0022227777777777775, 0.0027777777777777788)["Brz"]
f.write("{}, 0.0022227777777777775, 0.0027777777777777788, {}\n".format("Bz", point))

point = magnetic.local_values(0.0022227777777777775, 0.0027777777777777788)["Brr"]
f.write("{}, 0.0022227777777777775, 0.0027777777777777788, {}\n".format("Br", point))

point = magnetic.local_values(0.0022227777777777775, 0.003888888888888889)["Brz"]
f.write("{}, 0.0022227777777777775, 0.003888888888888889, {}\n".format("Bz", point))

point = magnetic.local_values(0.0022227777777777775, 0.003888888888888889)["Brr"]
f.write("{}, 0.0022227777777777775, 0.003888888888888889, {}\n".format("Br", point))

point = magnetic.local_values(0.0022227777777777775, 0.005)["Brz"]
f.write("{}, 0.0022227777777777775, 0.005, {}\n".format("Bz", point))

point = magnetic.local_values(0.0022227777777777775, 0.005)["Brr"]
f.write("{}, 0.0022227777777777775, 0.005, {}\n".format("Br", point))

point = magnetic.local_values(0.002778222222222222, -0.005)["Brz"]
f.write("{}, 0.002778222222222222, -0.005, {}\n".format("Bz", point))

point = magnetic.local_values(0.002778222222222222, -0.005)["Brr"]
f.write("{}, 0.002778222222222222, -0.005, {}\n".format("Br", point))

point = magnetic.local_values(0.002778222222222222, -0.0038888888888888888)["Brz"]
f.write("{}, 0.002778222222222222, -0.0038888888888888888, {}\n".format("Bz", point))

point = magnetic.local_values(0.002778222222222222, -0.0038888888888888888)["Brr"]
f.write("{}, 0.002778222222222222, -0.0038888888888888888, {}\n".format("Br", point))

point = magnetic.local_values(0.002778222222222222, -0.002777777777777778)["Brz"]
f.write("{}, 0.002778222222222222, -0.002777777777777778, {}\n".format("Bz", point))

point = magnetic.local_values(0.002778222222222222, -0.002777777777777778)["Brr"]
f.write("{}, 0.002778222222222222, -0.002777777777777778, {}\n".format("Br", point))

point = magnetic.local_values(0.002778222222222222, -0.0016666666666666666)["Brz"]
f.write("{}, 0.002778222222222222, -0.0016666666666666666, {}\n".format("Bz", point))

point = magnetic.local_values(0.002778222222222222, -0.0016666666666666666)["Brr"]
f.write("{}, 0.002778222222222222, -0.0016666666666666666, {}\n".format("Br", point))

point = magnetic.local_values(0.002778222222222222, -0.0005555555555555553)["Brz"]
f.write("{}, 0.002778222222222222, -0.0005555555555555553, {}\n".format("Bz", point))

point = magnetic.local_values(0.002778222222222222, -0.0005555555555555553)["Brr"]
f.write("{}, 0.002778222222222222, -0.0005555555555555553, {}\n".format("Br", point))

point = magnetic.local_values(0.002778222222222222, 0.0005555555555555553)["Brz"]
f.write("{}, 0.002778222222222222, 0.0005555555555555553, {}\n".format("Bz", point))

point = magnetic.local_values(0.002778222222222222, 0.0005555555555555553)["Brr"]
f.write("{}, 0.002778222222222222, 0.0005555555555555553, {}\n".format("Br", point))

point = magnetic.local_values(0.002778222222222222, 0.001666666666666667)["Brz"]
f.write("{}, 0.002778222222222222, 0.001666666666666667, {}\n".format("Bz", point))

point = magnetic.local_values(0.002778222222222222, 0.001666666666666667)["Brr"]
f.write("{}, 0.002778222222222222, 0.001666666666666667, {}\n".format("Br", point))

point = magnetic.local_values(0.002778222222222222, 0.0027777777777777788)["Brz"]
f.write("{}, 0.002778222222222222, 0.0027777777777777788, {}\n".format("Bz", point))

point = magnetic.local_values(0.002778222222222222, 0.0027777777777777788)["Brr"]
f.write("{}, 0.002778222222222222, 0.0027777777777777788, {}\n".format("Br", point))

point = magnetic.local_values(0.002778222222222222, 0.003888888888888889)["Brz"]
f.write("{}, 0.002778222222222222, 0.003888888888888889, {}\n".format("Bz", point))

point = magnetic.local_values(0.002778222222222222, 0.003888888888888889)["Brr"]
f.write("{}, 0.002778222222222222, 0.003888888888888889, {}\n".format("Br", point))

point = magnetic.local_values(0.002778222222222222, 0.005)["Brz"]
f.write("{}, 0.002778222222222222, 0.005, {}\n".format("Bz", point))

point = magnetic.local_values(0.002778222222222222, 0.005)["Brr"]
f.write("{}, 0.002778222222222222, 0.005, {}\n".format("Br", point))

point = magnetic.local_values(0.003333666666666666, -0.005)["Brz"]
f.write("{}, 0.003333666666666666, -0.005, {}\n".format("Bz", point))

point = magnetic.local_values(0.003333666666666666, -0.005)["Brr"]
f.write("{}, 0.003333666666666666, -0.005, {}\n".format("Br", point))

point = magnetic.local_values(0.003333666666666666, -0.0038888888888888888)["Brz"]
f.write("{}, 0.003333666666666666, -0.0038888888888888888, {}\n".format("Bz", point))

point = magnetic.local_values(0.003333666666666666, -0.0038888888888888888)["Brr"]
f.write("{}, 0.003333666666666666, -0.0038888888888888888, {}\n".format("Br", point))

point = magnetic.local_values(0.003333666666666666, -0.002777777777777778)["Brz"]
f.write("{}, 0.003333666666666666, -0.002777777777777778, {}\n".format("Bz", point))

point = magnetic.local_values(0.003333666666666666, -0.002777777777777778)["Brr"]
f.write("{}, 0.003333666666666666, -0.002777777777777778, {}\n".format("Br", point))

point = magnetic.local_values(0.003333666666666666, -0.0016666666666666666)["Brz"]
f.write("{}, 0.003333666666666666, -0.0016666666666666666, {}\n".format("Bz", point))

point = magnetic.local_values(0.003333666666666666, -0.0016666666666666666)["Brr"]
f.write("{}, 0.003333666666666666, -0.0016666666666666666, {}\n".format("Br", point))

point = magnetic.local_values(0.003333666666666666, -0.0005555555555555553)["Brz"]
f.write("{}, 0.003333666666666666, -0.0005555555555555553, {}\n".format("Bz", point))

point = magnetic.local_values(0.003333666666666666, -0.0005555555555555553)["Brr"]
f.write("{}, 0.003333666666666666, -0.0005555555555555553, {}\n".format("Br", point))

point = magnetic.local_values(0.003333666666666666, 0.0005555555555555553)["Brz"]
f.write("{}, 0.003333666666666666, 0.0005555555555555553, {}\n".format("Bz", point))

point = magnetic.local_values(0.003333666666666666, 0.0005555555555555553)["Brr"]
f.write("{}, 0.003333666666666666, 0.0005555555555555553, {}\n".format("Br", point))

point = magnetic.local_values(0.003333666666666666, 0.001666666666666667)["Brz"]
f.write("{}, 0.003333666666666666, 0.001666666666666667, {}\n".format("Bz", point))

point = magnetic.local_values(0.003333666666666666, 0.001666666666666667)["Brr"]
f.write("{}, 0.003333666666666666, 0.001666666666666667, {}\n".format("Br", point))

point = magnetic.local_values(0.003333666666666666, 0.0027777777777777788)["Brz"]
f.write("{}, 0.003333666666666666, 0.0027777777777777788, {}\n".format("Bz", point))

point = magnetic.local_values(0.003333666666666666, 0.0027777777777777788)["Brr"]
f.write("{}, 0.003333666666666666, 0.0027777777777777788, {}\n".format("Br", point))

point = magnetic.local_values(0.003333666666666666, 0.003888888888888889)["Brz"]
f.write("{}, 0.003333666666666666, 0.003888888888888889, {}\n".format("Bz", point))

point = magnetic.local_values(0.003333666666666666, 0.003888888888888889)["Brr"]
f.write("{}, 0.003333666666666666, 0.003888888888888889, {}\n".format("Br", point))

point = magnetic.local_values(0.003333666666666666, 0.005)["Brz"]
f.write("{}, 0.003333666666666666, 0.005, {}\n".format("Bz", point))

point = magnetic.local_values(0.003333666666666666, 0.005)["Brr"]
f.write("{}, 0.003333666666666666, 0.005, {}\n".format("Br", point))

point = magnetic.local_values(0.003889111111111111, -0.005)["Brz"]
f.write("{}, 0.003889111111111111, -0.005, {}\n".format("Bz", point))

point = magnetic.local_values(0.003889111111111111, -0.005)["Brr"]
f.write("{}, 0.003889111111111111, -0.005, {}\n".format("Br", point))

point = magnetic.local_values(0.003889111111111111, -0.0038888888888888888)["Brz"]
f.write("{}, 0.003889111111111111, -0.0038888888888888888, {}\n".format("Bz", point))

point = magnetic.local_values(0.003889111111111111, -0.0038888888888888888)["Brr"]
f.write("{}, 0.003889111111111111, -0.0038888888888888888, {}\n".format("Br", point))

point = magnetic.local_values(0.003889111111111111, -0.002777777777777778)["Brz"]
f.write("{}, 0.003889111111111111, -0.002777777777777778, {}\n".format("Bz", point))

point = magnetic.local_values(0.003889111111111111, -0.002777777777777778)["Brr"]
f.write("{}, 0.003889111111111111, -0.002777777777777778, {}\n".format("Br", point))

point = magnetic.local_values(0.003889111111111111, -0.0016666666666666666)["Brz"]
f.write("{}, 0.003889111111111111, -0.0016666666666666666, {}\n".format("Bz", point))

point = magnetic.local_values(0.003889111111111111, -0.0016666666666666666)["Brr"]
f.write("{}, 0.003889111111111111, -0.0016666666666666666, {}\n".format("Br", point))

point = magnetic.local_values(0.003889111111111111, -0.0005555555555555553)["Brz"]
f.write("{}, 0.003889111111111111, -0.0005555555555555553, {}\n".format("Bz", point))

point = magnetic.local_values(0.003889111111111111, -0.0005555555555555553)["Brr"]
f.write("{}, 0.003889111111111111, -0.0005555555555555553, {}\n".format("Br", point))

point = magnetic.local_values(0.003889111111111111, 0.0005555555555555553)["Brz"]
f.write("{}, 0.003889111111111111, 0.0005555555555555553, {}\n".format("Bz", point))

point = magnetic.local_values(0.003889111111111111, 0.0005555555555555553)["Brr"]
f.write("{}, 0.003889111111111111, 0.0005555555555555553, {}\n".format("Br", point))

point = magnetic.local_values(0.003889111111111111, 0.001666666666666667)["Brz"]
f.write("{}, 0.003889111111111111, 0.001666666666666667, {}\n".format("Bz", point))

point = magnetic.local_values(0.003889111111111111, 0.001666666666666667)["Brr"]
f.write("{}, 0.003889111111111111, 0.001666666666666667, {}\n".format("Br", point))

point = magnetic.local_values(0.003889111111111111, 0.0027777777777777788)["Brz"]
f.write("{}, 0.003889111111111111, 0.0027777777777777788, {}\n".format("Bz", point))

point = magnetic.local_values(0.003889111111111111, 0.0027777777777777788)["Brr"]
f.write("{}, 0.003889111111111111, 0.0027777777777777788, {}\n".format("Br", point))

point = magnetic.local_values(0.003889111111111111, 0.003888888888888889)["Brz"]
f.write("{}, 0.003889111111111111, 0.003888888888888889, {}\n".format("Bz", point))

point = magnetic.local_values(0.003889111111111111, 0.003888888888888889)["Brr"]
f.write("{}, 0.003889111111111111, 0.003888888888888889, {}\n".format("Br", point))

point = magnetic.local_values(0.003889111111111111, 0.005)["Brz"]
f.write("{}, 0.003889111111111111, 0.005, {}\n".format("Bz", point))

point = magnetic.local_values(0.003889111111111111, 0.005)["Brr"]
f.write("{}, 0.003889111111111111, 0.005, {}\n".format("Br", point))

point = magnetic.local_values(0.004444555555555556, -0.005)["Brz"]
f.write("{}, 0.004444555555555556, -0.005, {}\n".format("Bz", point))

point = magnetic.local_values(0.004444555555555556, -0.005)["Brr"]
f.write("{}, 0.004444555555555556, -0.005, {}\n".format("Br", point))

point = magnetic.local_values(0.004444555555555556, -0.0038888888888888888)["Brz"]
f.write("{}, 0.004444555555555556, -0.0038888888888888888, {}\n".format("Bz", point))

point = magnetic.local_values(0.004444555555555556, -0.0038888888888888888)["Brr"]
f.write("{}, 0.004444555555555556, -0.0038888888888888888, {}\n".format("Br", point))

point = magnetic.local_values(0.004444555555555556, -0.002777777777777778)["Brz"]
f.write("{}, 0.004444555555555556, -0.002777777777777778, {}\n".format("Bz", point))

point = magnetic.local_values(0.004444555555555556, -0.002777777777777778)["Brr"]
f.write("{}, 0.004444555555555556, -0.002777777777777778, {}\n".format("Br", point))

point = magnetic.local_values(0.004444555555555556, -0.0016666666666666666)["Brz"]
f.write("{}, 0.004444555555555556, -0.0016666666666666666, {}\n".format("Bz", point))

point = magnetic.local_values(0.004444555555555556, -0.0016666666666666666)["Brr"]
f.write("{}, 0.004444555555555556, -0.0016666666666666666, {}\n".format("Br", point))

point = magnetic.local_values(0.004444555555555556, -0.0005555555555555553)["Brz"]
f.write("{}, 0.004444555555555556, -0.0005555555555555553, {}\n".format("Bz", point))

point = magnetic.local_values(0.004444555555555556, -0.0005555555555555553)["Brr"]
f.write("{}, 0.004444555555555556, -0.0005555555555555553, {}\n".format("Br", point))

point = magnetic.local_values(0.004444555555555556, 0.0005555555555555553)["Brz"]
f.write("{}, 0.004444555555555556, 0.0005555555555555553, {}\n".format("Bz", point))

point = magnetic.local_values(0.004444555555555556, 0.0005555555555555553)["Brr"]
f.write("{}, 0.004444555555555556, 0.0005555555555555553, {}\n".format("Br", point))

point = magnetic.local_values(0.004444555555555556, 0.001666666666666667)["Brz"]
f.write("{}, 0.004444555555555556, 0.001666666666666667, {}\n".format("Bz", point))

point = magnetic.local_values(0.004444555555555556, 0.001666666666666667)["Brr"]
f.write("{}, 0.004444555555555556, 0.001666666666666667, {}\n".format("Br", point))

point = magnetic.local_values(0.004444555555555556, 0.0027777777777777788)["Brz"]
f.write("{}, 0.004444555555555556, 0.0027777777777777788, {}\n".format("Bz", point))

point = magnetic.local_values(0.004444555555555556, 0.0027777777777777788)["Brr"]
f.write("{}, 0.004444555555555556, 0.0027777777777777788, {}\n".format("Br", point))

point = magnetic.local_values(0.004444555555555556, 0.003888888888888889)["Brz"]
f.write("{}, 0.004444555555555556, 0.003888888888888889, {}\n".format("Bz", point))

point = magnetic.local_values(0.004444555555555556, 0.003888888888888889)["Brr"]
f.write("{}, 0.004444555555555556, 0.003888888888888889, {}\n".format("Br", point))

point = magnetic.local_values(0.004444555555555556, 0.005)["Brz"]
f.write("{}, 0.004444555555555556, 0.005, {}\n".format("Bz", point))

point = magnetic.local_values(0.004444555555555556, 0.005)["Brr"]
f.write("{}, 0.004444555555555556, 0.005, {}\n".format("Br", point))

point = magnetic.local_values(0.005, -0.005)["Brz"]
f.write("{}, 0.005, -0.005, {}\n".format("Bz", point))

point = magnetic.local_values(0.005, -0.005)["Brr"]
f.write("{}, 0.005, -0.005, {}\n".format("Br", point))

point = magnetic.local_values(0.005, -0.0038888888888888888)["Brz"]
f.write("{}, 0.005, -0.0038888888888888888, {}\n".format("Bz", point))

point = magnetic.local_values(0.005, -0.0038888888888888888)["Brr"]
f.write("{}, 0.005, -0.0038888888888888888, {}\n".format("Br", point))

point = magnetic.local_values(0.005, -0.002777777777777778)["Brz"]
f.write("{}, 0.005, -0.002777777777777778, {}\n".format("Bz", point))

point = magnetic.local_values(0.005, -0.002777777777777778)["Brr"]
f.write("{}, 0.005, -0.002777777777777778, {}\n".format("Br", point))

point = magnetic.local_values(0.005, -0.0016666666666666666)["Brz"]
f.write("{}, 0.005, -0.0016666666666666666, {}\n".format("Bz", point))

point = magnetic.local_values(0.005, -0.0016666666666666666)["Brr"]
f.write("{}, 0.005, -0.0016666666666666666, {}\n".format("Br", point))

point = magnetic.local_values(0.005, -0.0005555555555555553)["Brz"]
f.write("{}, 0.005, -0.0005555555555555553, {}\n".format("Bz", point))

point = magnetic.local_values(0.005, -0.0005555555555555553)["Brr"]
f.write("{}, 0.005, -0.0005555555555555553, {}\n".format("Br", point))

point = magnetic.local_values(0.005, 0.0005555555555555553)["Brz"]
f.write("{}, 0.005, 0.0005555555555555553, {}\n".format("Bz", point))

point = magnetic.local_values(0.005, 0.0005555555555555553)["Brr"]
f.write("{}, 0.005, 0.0005555555555555553, {}\n".format("Br", point))

point = magnetic.local_values(0.005, 0.001666666666666667)["Brz"]
f.write("{}, 0.005, 0.001666666666666667, {}\n".format("Bz", point))

point = magnetic.local_values(0.005, 0.001666666666666667)["Brr"]
f.write("{}, 0.005, 0.001666666666666667, {}\n".format("Br", point))

point = magnetic.local_values(0.005, 0.0027777777777777788)["Brz"]
f.write("{}, 0.005, 0.0027777777777777788, {}\n".format("Bz", point))

point = magnetic.local_values(0.005, 0.0027777777777777788)["Brr"]
f.write("{}, 0.005, 0.0027777777777777788, {}\n".format("Br", point))

point = magnetic.local_values(0.005, 0.003888888888888889)["Brz"]
f.write("{}, 0.005, 0.003888888888888889, {}\n".format("Bz", point))

point = magnetic.local_values(0.005, 0.003888888888888889)["Brr"]
f.write("{}, 0.005, 0.003888888888888889, {}\n".format("Br", point))

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
