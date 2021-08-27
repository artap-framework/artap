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
geometry.add_edge(0.07, 0.035, 0.07, -0.035, boundaries={'magnetic': 'a0'})
geometry.add_edge(0.0, 0.005, 0.0, 0.035, boundaries={'magnetic': 'a0'})
geometry.add_edge(0.0, -0.005, 0.0, 0.005, boundaries={'magnetic': 'a0'})
geometry.add_edge(0.07, -0.035, 0.0, -0.035, boundaries={'magnetic': 'a0'})
geometry.add_edge(0.0, 0.035, 0.07, 0.035, boundaries={'magnetic': 'a0'})
geometry.add_edge(0.0, -0.035, 0.0, -0.005, boundaries={'magnetic': 'a0'})
geometry.add_edge(0.0, 0.005, 0.005, 0.005)
geometry.add_edge(0.005, 0.005, 0.005, -0.005)
geometry.add_edge(0.005, -0.005, 0.0, -0.005)
geometry.add_edge(0.0025099999999999996, -0.0135, 0.003329999999999998, -0.0135)
geometry.add_edge(0.003329999999999998, -0.0135, 0.0035099999999999997, -0.0135)
geometry.add_edge(0.0035099999999999997, -0.0135, 0.0035099999999999997, -0.015)
geometry.add_edge(0.0035099999999999997, -0.015, 0.0025099999999999996, -0.015)
geometry.add_edge(0.0025099999999999996, -0.015, 0.0025099999999999996, -0.0135)
geometry.add_edge(0.00333, -0.012, 0.0038600000000000015, -0.012)
geometry.add_edge(0.0038600000000000015, -0.012, 0.0043300000000000005, -0.012)
geometry.add_edge(0.0043300000000000005, -0.012, 0.0043300000000000005, -0.0135)
geometry.add_edge(0.004330000000000005, -0.0135, 0.0035099999999999975, -0.0135)
geometry.add_edge(0.00333, -0.0135, 0.00333, -0.012)
geometry.add_edge(0.00286, -0.0105, 0.00386, -0.0105)
geometry.add_edge(0.00386, -0.0105, 0.00386, -0.012)
geometry.add_edge(0.0033299999999999988, -0.012, 0.00286, -0.012)
geometry.add_edge(0.00286, -0.012, 0.00286, -0.0105)
geometry.add_edge(0.00444, -0.009000000000000001, 0.004980000000000007, -0.009000000000000001)
geometry.add_edge(0.004980000000000007, -0.009000000000000001, 0.00544, -0.009000000000000001)
geometry.add_edge(0.00544, -0.009000000000000001, 0.00544, -0.0105)
geometry.add_edge(0.005440000000000005, -0.0105, 0.00444, -0.0105)
geometry.add_edge(0.00444, -0.0105, 0.00444, -0.009000000000000001)
geometry.add_edge(0.004980000000000001, -0.0075, 0.005980000000000001, -0.0075)
geometry.add_edge(0.005980000000000001, -0.0075, 0.005980000000000001, -0.009000000000000001)
geometry.add_edge(0.005980000000000001, -0.009000000000000001, 0.005440000000000004, -0.009000000000000001)
geometry.add_edge(0.004980000000000001, -0.009000000000000001, 0.004980000000000001, -0.0075)
geometry.add_edge(0.00644, -0.006, 0.00692, -0.006)
geometry.add_edge(0.00692, -0.006, 0.00744, -0.006)
geometry.add_edge(0.00744, -0.006, 0.00744, -0.0075)
geometry.add_edge(0.00744, -0.0075, 0.00644, -0.0075)
geometry.add_edge(0.00644, -0.0075, 0.00644, -0.006)
geometry.add_edge(0.00692, -0.0045000000000000005, 0.00792, -0.0045000000000000005)
geometry.add_edge(0.00792, -0.0045000000000000005, 0.00792, -0.006)
geometry.add_edge(0.00792, -0.006, 0.00744, -0.006)
geometry.add_edge(0.00692, -0.006, 0.00692, -0.0045000000000000005)
geometry.add_edge(0.00897, -0.003, 0.009970000000000001, -0.003)
geometry.add_edge(0.009970000000000001, -0.003, 0.009970000000000001, -0.0045000000000000005)
geometry.add_edge(0.009970000000000001, -0.0045000000000000005, 0.00897, -0.0045000000000000005)
geometry.add_edge(0.00897, -0.0045000000000000005, 0.00897, -0.003)
geometry.add_edge(0.00742, -0.0015, 0.00842, -0.0015)
geometry.add_edge(0.00842, -0.0015, 0.00842, -0.003)
geometry.add_edge(0.008419999999999999, -0.003, 0.00742, -0.003)
geometry.add_edge(0.00742, -0.003, 0.00742, -0.0015)
geometry.add_edge(0.01082, 0.0, 0.01182, 0.0)
geometry.add_edge(0.01182, 0.0, 0.01182, -0.0015)
geometry.add_edge(0.01182, -0.0015, 0.01082, -0.0015)
geometry.add_edge(0.01082, -0.0015, 0.01082, 0.0)
geometry.add_edge(0.008029999999999999, 0.0015, 0.00818, 0.0015)
geometry.add_edge(0.00818, 0.0015, 0.00903, 0.0015)
geometry.add_edge(0.00903, 0.0015, 0.00903, 0.0)
geometry.add_edge(0.00903, 0.0, 0.008029999999999999, 0.0)
geometry.add_edge(0.008029999999999999, 0.0, 0.008029999999999999, 0.0015)
geometry.add_edge(0.008179999999999998, 0.003, 0.008389999999999998, 0.003)
geometry.add_edge(0.008389999999999998, 0.003, 0.00918, 0.003)
geometry.add_edge(0.00918, 0.003, 0.00918, 0.0015)
geometry.add_edge(0.00918, 0.0015, 0.00903, 0.0015)
geometry.add_edge(0.00818, 0.0015, 0.00818, 0.003)
geometry.add_edge(0.00839, 0.0045000000000000005, 0.00939, 0.0045000000000000005)
geometry.add_edge(0.00939, 0.0045000000000000005, 0.00939, 0.003)
geometry.add_edge(0.00939, 0.003, 0.00918, 0.003)
geometry.add_edge(0.00839, 0.003, 0.00839, 0.0045000000000000005)
geometry.add_edge(0.0071100000000000035, 0.006, 0.00811, 0.006)
geometry.add_edge(0.00811, 0.006, 0.00811, 0.0045000000000000005)
geometry.add_edge(0.00811, 0.0045000000000000005, 0.007109999999999997, 0.0045000000000000005)
geometry.add_edge(0.007110000000000001, 0.0045000000000000005, 0.007110000000000001, 0.006)
geometry.add_edge(0.006, 0.0075, 0.006010000000000001, 0.0075)
geometry.add_edge(0.006010000000000001, 0.0075, 0.007, 0.0075)
geometry.add_edge(0.007, 0.0075, 0.007, 0.006)
geometry.add_edge(0.007, 0.006, 0.006, 0.006)
geometry.add_edge(0.006, 0.006, 0.006, 0.0075)
geometry.add_edge(0.00501, 0.009000000000000001, 0.00601, 0.009000000000000001)
geometry.add_edge(0.00601, 0.009000000000000001, 0.00601, 0.0075)
geometry.add_edge(0.0060000000000000045, 0.0075, 0.00501, 0.0075)
geometry.add_edge(0.00501, 0.0075, 0.00501, 0.009000000000000001)
geometry.add_edge(0.00375, 0.0105, 0.00475, 0.0105)
geometry.add_edge(0.00475, 0.0105, 0.00475, 0.009000000000000001)
geometry.add_edge(0.00475, 0.009000000000000001, 0.00375, 0.009000000000000001)
geometry.add_edge(0.00375, 0.009000000000000001, 0.00375, 0.0105)
geometry.add_edge(0.0015, 0.012, 0.0025, 0.012)
geometry.add_edge(0.0025, 0.012, 0.0025, 0.0105)
geometry.add_edge(0.0025, 0.0105, 0.0015, 0.0105)
geometry.add_edge(0.0015, 0.0105, 0.0015, 0.012)
geometry.add_edge(0.00257, 0.0135, 0.00357, 0.0135)
geometry.add_edge(0.00357, 0.0135, 0.00357, 0.012)
geometry.add_edge(0.00357, 0.012, 0.00257, 0.012)
geometry.add_edge(0.00257, 0.012, 0.00257, 0.0135)
geometry.add_edge(0.0010900000000000011, 0.015, 0.0020900000000000024, 0.015)
geometry.add_edge(0.00209, 0.015, 0.00209, 0.0135)
geometry.add_edge(0.00209, 0.0135, 0.0010900000000000011, 0.0135)
geometry.add_edge(0.00109, 0.0135, 0.00109, 0.015)

# BLOCK LABELS
geometry.add_label(0.00326, -0.01425, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00408, -0.012750000000000001, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00361, -0.01125, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00519, -0.00975, materials = {'magnetic' : 'J+'})
geometry.add_label(0.005730000000000001, -0.00825, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00719, -0.00675, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00767, -0.00525, materials = {'magnetic' : 'J+'})
geometry.add_label(0.009720000000000001, -0.00375, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00817, -0.0022500000000000003, materials = {'magnetic' : 'J+'})
geometry.add_label(0.01157, -0.00075, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00878, 0.00075, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00893, 0.0022500000000000003, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00914, 0.00375, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00786, 0.00525, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00675, 0.00675, materials = {'magnetic' : 'J+'})
geometry.add_label(0.0057599999999999995, 0.00825, materials = {'magnetic' : 'J+'})
geometry.add_label(0.0045000000000000005, 0.00975, materials = {'magnetic' : 'J+'})
geometry.add_label(0.0022500000000000003, 0.01125, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00332, 0.012750000000000001, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00184, 0.01425, materials = {'magnetic' : 'J+'})
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
