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
geometry.add_edge(0.0, -0.035, 0.0, -0.005, boundaries={'magnetic': 'a0'})
geometry.add_edge(0.0, -0.005, 0.0, 0.005, boundaries={'magnetic': 'a0'})
geometry.add_edge(0.07, -0.035, 0.0, -0.035, boundaries={'magnetic': 'a0'})
geometry.add_edge(0.07, 0.035, 0.07, -0.035, boundaries={'magnetic': 'a0'})
geometry.add_edge(0.0, 0.035, 0.07, 0.035, boundaries={'magnetic': 'a0'})
geometry.add_edge(0.0, 0.005, 0.0, 0.035, boundaries={'magnetic': 'a0'})
geometry.add_edge(0.0, 0.005, 0.005, 0.005)
geometry.add_edge(0.005, 0.005, 0.005, -0.005)
geometry.add_edge(0.005, -0.005, 0.0, -0.005)
geometry.add_edge(0.00064, -0.0135, 0.0016200000000000014, -0.0135)
geometry.add_edge(0.0016200000000000014, -0.0135, 0.00164, -0.0135)
geometry.add_edge(0.00164, -0.0135, 0.00164, -0.015)
geometry.add_edge(0.00164, -0.015, 0.00064, -0.015)
geometry.add_edge(0.00064, -0.015, 0.00064, -0.0135)
geometry.add_edge(0.00062, -0.012, 0.0015100000000000007, -0.012)
geometry.add_edge(0.0015100000000000007, -0.012, 0.0016200000000000001, -0.012)
geometry.add_edge(0.0016200000000000001, -0.012, 0.0016200000000000001, -0.0135)
geometry.add_edge(0.0006399999999999985, -0.0135, 0.0006200000000000001, -0.0135)
geometry.add_edge(0.00062, -0.0135, 0.00062, -0.012)
geometry.add_edge(0.00051, -0.0105, 0.0007899999999999994, -0.0105)
geometry.add_edge(0.0007899999999999994, -0.0105, 0.00151, -0.0105)
geometry.add_edge(0.00151, -0.0105, 0.00151, -0.012)
geometry.add_edge(0.0006200000000000004, -0.012, 0.00051, -0.012)
geometry.add_edge(0.00051, -0.012, 0.00051, -0.0105)
geometry.add_edge(0.00079, -0.009000000000000001, 0.0015300000000000008, -0.009000000000000001)
geometry.add_edge(0.0015300000000000008, -0.009000000000000001, 0.0017900000000000001, -0.009000000000000001)
geometry.add_edge(0.0017900000000000001, -0.009000000000000001, 0.0017900000000000001, -0.0105)
geometry.add_edge(0.0017900000000000001, -0.0105, 0.0015100000000000007, -0.0105)
geometry.add_edge(0.00079, -0.0105, 0.00079, -0.009000000000000001)
geometry.add_edge(0.0005300000000000001, -0.0075, 0.0015300000000000001, -0.0075)
geometry.add_edge(0.0015300000000000001, -0.0075, 0.0015300000000000001, -0.009000000000000001)
geometry.add_edge(0.0007900000000000006, -0.009000000000000001, 0.0005300000000000001, -0.009000000000000001)
geometry.add_edge(0.0005300000000000001, -0.009000000000000001, 0.0005300000000000001, -0.0075)
geometry.add_edge(0.004980000000000001, -0.006, 0.005150000000000003, -0.006)
geometry.add_edge(0.005150000000000003, -0.006, 0.005980000000000001, -0.006)
geometry.add_edge(0.005980000000000001, -0.006, 0.005980000000000001, -0.0075)
geometry.add_edge(0.005980000000000001, -0.0075, 0.004980000000000001, -0.0075)
geometry.add_edge(0.004980000000000001, -0.0075, 0.004980000000000001, -0.006)
geometry.add_edge(0.00515, -0.0045000000000000005, 0.0052499999999999995, -0.0045000000000000005)
geometry.add_edge(0.0052499999999999995, -0.0045000000000000005, 0.00615, -0.0045000000000000005)
geometry.add_edge(0.00615, -0.0045000000000000005, 0.00615, -0.006)
geometry.add_edge(0.0061499999999999975, -0.006, 0.0059800000000000035, -0.006)
geometry.add_edge(0.00515, -0.006, 0.00515, -0.0045000000000000005)
geometry.add_edge(0.00525, -0.003, 0.0055299999999999985, -0.003)
geometry.add_edge(0.0055299999999999985, -0.003, 0.00625, -0.003)
geometry.add_edge(0.00625, -0.003, 0.00625, -0.0045000000000000005)
geometry.add_edge(0.00625, -0.0045000000000000005, 0.006150000000000006, -0.0045000000000000005)
geometry.add_edge(0.00525, -0.0045000000000000005, 0.00525, -0.003)
geometry.add_edge(0.00553, -0.0015, 0.0061200000000000004, -0.0015)
geometry.add_edge(0.0061200000000000004, -0.0015, 0.00653, -0.0015)
geometry.add_edge(0.00653, -0.0015, 0.00653, -0.003)
geometry.add_edge(0.006530000000000001, -0.003, 0.0062499999999999995, -0.003)
geometry.add_edge(0.00553, -0.003, 0.00553, -0.0015)
geometry.add_edge(0.0061200000000000004, 0.0, 0.00619, 0.0)
geometry.add_edge(0.00619, 0.0, 0.0071200000000000005, 0.0)
geometry.add_edge(0.0071200000000000005, 0.0, 0.0071200000000000005, -0.0015)
geometry.add_edge(0.0071200000000000005, -0.0015, 0.006529999999999999, -0.0015)
geometry.add_edge(0.0061200000000000004, -0.0015, 0.0061200000000000004, 0.0)
geometry.add_edge(0.00519, 0.0015, 0.00617, 0.0015)
geometry.add_edge(0.00617, 0.0015, 0.00619, 0.0015)
geometry.add_edge(0.00619, 0.0015, 0.00619, 0.0)
geometry.add_edge(0.0061200000000000004, 0.0, 0.00519, 0.0)
geometry.add_edge(0.00519, 0.0, 0.00519, 0.0015)
geometry.add_edge(0.005169999999999999, 0.003, 0.005230000000000002, 0.003)
geometry.add_edge(0.005230000000000002, 0.003, 0.00617, 0.003)
geometry.add_edge(0.00617, 0.003, 0.00617, 0.0015)
geometry.add_edge(0.00519, 0.0015, 0.005170000000000001, 0.0015)
geometry.add_edge(0.00517, 0.0015, 0.00517, 0.003)
geometry.add_edge(0.00523, 0.0045000000000000005, 0.006040000000000003, 0.0045000000000000005)
geometry.add_edge(0.006040000000000003, 0.0045000000000000005, 0.00623, 0.0045000000000000005)
geometry.add_edge(0.00623, 0.0045000000000000005, 0.00623, 0.003)
geometry.add_edge(0.00623, 0.003, 0.006169999999999998, 0.003)
geometry.add_edge(0.00523, 0.003, 0.00523, 0.0045000000000000005)
geometry.add_edge(0.00504, 0.006, 0.00604, 0.006)
geometry.add_edge(0.00604, 0.006, 0.00604, 0.0045000000000000005)
geometry.add_edge(0.005230000000000005, 0.0045000000000000005, 0.00504, 0.0045000000000000005)
geometry.add_edge(0.00504, 0.0045000000000000005, 0.00504, 0.006)
geometry.add_edge(0.0008100000000000001, 0.0075, 0.0008699999999999996, 0.0075)
geometry.add_edge(0.0008699999999999996, 0.0075, 0.0018100000000000002, 0.0075)
geometry.add_edge(0.0018100000000000002, 0.0075, 0.0018100000000000002, 0.006)
geometry.add_edge(0.0018100000000000002, 0.006, 0.0008100000000000001, 0.006)
geometry.add_edge(0.0008100000000000001, 0.006, 0.0008100000000000001, 0.0075)
geometry.add_edge(0.00087, 0.009000000000000001, 0.0016699999999999985, 0.009000000000000001)
geometry.add_edge(0.0016699999999999985, 0.009000000000000001, 0.0018699999999999988, 0.009000000000000001)
geometry.add_edge(0.0018700000000000001, 0.009000000000000001, 0.0018700000000000001, 0.0075)
geometry.add_edge(0.0018700000000000001, 0.0075, 0.0018100000000000015, 0.0075)
geometry.add_edge(0.00087, 0.0075, 0.00087, 0.009000000000000001)
geometry.add_edge(0.0006700000000000006, 0.0105, 0.0015700000000000009, 0.0105)
geometry.add_edge(0.0015700000000000009, 0.0105, 0.00167, 0.0105)
geometry.add_edge(0.00167, 0.0105, 0.00167, 0.009000000000000001)
geometry.add_edge(0.0008700000000000003, 0.009000000000000001, 0.00067, 0.009000000000000001)
geometry.add_edge(0.00067, 0.009000000000000001, 0.00067, 0.0105)
geometry.add_edge(0.00057, 0.012, 0.0005800000000000003, 0.012)
geometry.add_edge(0.0005800000000000003, 0.012, 0.0015699999999999998, 0.012)
geometry.add_edge(0.00157, 0.012, 0.00157, 0.0105)
geometry.add_edge(0.0006700000000000009, 0.0105, 0.0005700000000000001, 0.0105)
geometry.add_edge(0.00057, 0.0105, 0.00057, 0.012)
geometry.add_edge(0.00058, 0.0135, 0.0007600000000000009, 0.0135)
geometry.add_edge(0.0007600000000000009, 0.0135, 0.0015799999999999998, 0.0135)
geometry.add_edge(0.00158, 0.0135, 0.00158, 0.012)
geometry.add_edge(0.00158, 0.012, 0.0015699999999999996, 0.012)
geometry.add_edge(0.00058, 0.012, 0.00058, 0.0135)
geometry.add_edge(0.00076, 0.015, 0.00176, 0.015)
geometry.add_edge(0.00176, 0.015, 0.00176, 0.0135)
geometry.add_edge(0.00176, 0.0135, 0.0015800000000000007, 0.0135)
geometry.add_edge(0.00076, 0.0135, 0.00076, 0.015)

# BLOCK LABELS
geometry.add_label(0.00139, -0.01425, materials = {'magnetic' : 'J+'})
geometry.add_label(0.0013700000000000001, -0.012750000000000001, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00126, -0.01125, materials = {'magnetic' : 'J+'})
geometry.add_label(0.0015400000000000001, -0.00975, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00128, -0.00825, materials = {'magnetic' : 'J+'})
geometry.add_label(0.005730000000000001, -0.00675, materials = {'magnetic' : 'J+'})
geometry.add_label(0.005900000000000001, -0.00525, materials = {'magnetic' : 'J+'})
geometry.add_label(0.006, -0.00375, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00628, -0.0022500000000000003, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00687, -0.00075, materials = {'magnetic' : 'J+'})
geometry.add_label(0.005940000000000001, 0.00075, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00592, 0.0022500000000000003, materials = {'magnetic' : 'J+'})
geometry.add_label(0.005980000000000001, 0.00375, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00579, 0.00525, materials = {'magnetic' : 'J+'})
geometry.add_label(0.0015600000000000002, 0.00675, materials = {'magnetic' : 'J+'})
geometry.add_label(0.0016200000000000001, 0.00825, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00142, 0.00975, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00132, 0.01125, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00133, 0.012750000000000001, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00151, 0.01425, materials = {'magnetic' : 'J+'})
geometry.add_label(0.03, 0.03, materials = {'magnetic' : 'air'})
geometry.add_label(0.003, 0.0, materials = {'magnetic' : 'control'})

# SOLVE
problem.solve()
a2d.view.zoom_best_fit()
f = open("solution_minus.csv", "w")

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
