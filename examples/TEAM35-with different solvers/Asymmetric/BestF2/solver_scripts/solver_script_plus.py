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
geometry.add_edge(0.07, -0.035, 0.0, -0.035, boundaries={'magnetic': 'a0'})
geometry.add_edge(0.0, 0.005, 0.0, 0.035, boundaries={'magnetic': 'a0'})
geometry.add_edge(0.0, -0.005, 0.0, 0.005, boundaries={'magnetic': 'a0'})
geometry.add_edge(0.07, 0.035, 0.07, -0.035, boundaries={'magnetic': 'a0'})
geometry.add_edge(0.0, -0.035, 0.0, -0.005, boundaries={'magnetic': 'a0'})
geometry.add_edge(0.0, 0.035, 0.07, 0.035, boundaries={'magnetic': 'a0'})
geometry.add_edge(0.0, 0.005, 0.005, 0.005)
geometry.add_edge(0.005, 0.005, 0.005, -0.005)
geometry.add_edge(0.005, -0.005, 0.0, -0.005)
geometry.add_edge(0.0030099999999999997, -0.0135, 0.003829999999999998, -0.0135)
geometry.add_edge(0.003829999999999998, -0.0135, 0.00401, -0.0135)
geometry.add_edge(0.00401, -0.0135, 0.00401, -0.015)
geometry.add_edge(0.004010000000000004, -0.015, 0.0030099999999999997, -0.015)
geometry.add_edge(0.0030099999999999997, -0.015, 0.0030099999999999997, -0.0135)
geometry.add_edge(0.00383, -0.012, 0.004360000000000005, -0.012)
geometry.add_edge(0.004360000000000005, -0.012, 0.00483, -0.012)
geometry.add_edge(0.00483, -0.012, 0.00483, -0.0135)
geometry.add_edge(0.004830000000000004, -0.0135, 0.004009999999999997, -0.0135)
geometry.add_edge(0.00383, -0.0135, 0.00383, -0.012)
geometry.add_edge(0.00336, -0.0105, 0.00436, -0.0105)
geometry.add_edge(0.00436, -0.0105, 0.00436, -0.012)
geometry.add_edge(0.003829999999999999, -0.012, 0.00336, -0.012)
geometry.add_edge(0.00336, -0.012, 0.00336, -0.0105)
geometry.add_edge(0.004940000000000001, -0.009000000000000001, 0.005480000000000007, -0.009000000000000001)
geometry.add_edge(0.005480000000000007, -0.009000000000000001, 0.005940000000000001, -0.009000000000000001)
geometry.add_edge(0.005940000000000001, -0.009000000000000001, 0.005940000000000001, -0.0105)
geometry.add_edge(0.005940000000000005, -0.0105, 0.004940000000000001, -0.0105)
geometry.add_edge(0.004940000000000001, -0.0105, 0.004940000000000001, -0.009000000000000001)
geometry.add_edge(0.0054800000000000005, -0.0075, 0.0064800000000000005, -0.0075)
geometry.add_edge(0.0064800000000000005, -0.0075, 0.0064800000000000005, -0.009000000000000001)
geometry.add_edge(0.006479999999999996, -0.009000000000000001, 0.005940000000000004, -0.009000000000000001)
geometry.add_edge(0.0054800000000000005, -0.009000000000000001, 0.0054800000000000005, -0.0075)
geometry.add_edge(0.006940000000000001, -0.006, 0.00742, -0.006)
geometry.add_edge(0.00742, -0.006, 0.007940000000000001, -0.006)
geometry.add_edge(0.007940000000000001, -0.006, 0.007940000000000001, -0.0075)
geometry.add_edge(0.007940000000000001, -0.0075, 0.006940000000000001, -0.0075)
geometry.add_edge(0.006940000000000001, -0.0075, 0.006940000000000001, -0.006)
geometry.add_edge(0.00742, -0.0045000000000000005, 0.00842, -0.0045000000000000005)
geometry.add_edge(0.00842, -0.0045000000000000005, 0.00842, -0.006)
geometry.add_edge(0.00842, -0.006, 0.007940000000000001, -0.006)
geometry.add_edge(0.00742, -0.006, 0.00742, -0.0045000000000000005)
geometry.add_edge(0.009470000000000001, -0.003, 0.01047, -0.003)
geometry.add_edge(0.01047, -0.003, 0.01047, -0.0045000000000000005)
geometry.add_edge(0.01047, -0.0045000000000000005, 0.009470000000000001, -0.0045000000000000005)
geometry.add_edge(0.009470000000000001, -0.0045000000000000005, 0.009470000000000001, -0.003)
geometry.add_edge(0.00792, -0.0015, 0.00892, -0.0015)
geometry.add_edge(0.00892, -0.0015, 0.00892, -0.003)
geometry.add_edge(0.008919999999999999, -0.003, 0.00792, -0.003)
geometry.add_edge(0.00792, -0.003, 0.00792, -0.0015)
geometry.add_edge(0.01132, 0.0, 0.012320000000000001, 0.0)
geometry.add_edge(0.012320000000000001, 0.0, 0.012320000000000001, -0.0015)
geometry.add_edge(0.012320000000000001, -0.0015, 0.01132, -0.0015)
geometry.add_edge(0.01132, -0.0015, 0.01132, 0.0)
geometry.add_edge(0.00853, 0.0015, 0.00868, 0.0015)
geometry.add_edge(0.00868, 0.0015, 0.00953, 0.0015)
geometry.add_edge(0.00953, 0.0015, 0.00953, 0.0)
geometry.add_edge(0.00953, 0.0, 0.00853, 0.0)
geometry.add_edge(0.00853, 0.0, 0.00853, 0.0015)
geometry.add_edge(0.008679999999999998, 0.003, 0.008889999999999999, 0.003)
geometry.add_edge(0.008889999999999999, 0.003, 0.00968, 0.003)
geometry.add_edge(0.00968, 0.003, 0.00968, 0.0015)
geometry.add_edge(0.00968, 0.0015, 0.00953, 0.0015)
geometry.add_edge(0.00868, 0.0015, 0.00868, 0.003)
geometry.add_edge(0.00889, 0.0045000000000000005, 0.009890000000000001, 0.0045000000000000005)
geometry.add_edge(0.009890000000000001, 0.0045000000000000005, 0.009890000000000001, 0.003)
geometry.add_edge(0.009890000000000001, 0.003, 0.00968, 0.003)
geometry.add_edge(0.00889, 0.003, 0.00889, 0.0045000000000000005)
geometry.add_edge(0.0076100000000000004, 0.006, 0.00861, 0.006)
geometry.add_edge(0.00861, 0.006, 0.00861, 0.0045000000000000005)
geometry.add_edge(0.00861, 0.0045000000000000005, 0.0076100000000000004, 0.0045000000000000005)
geometry.add_edge(0.0076100000000000004, 0.0045000000000000005, 0.0076100000000000004, 0.006)
geometry.add_edge(0.006500000000000001, 0.0075, 0.006510000000000001, 0.0075)
geometry.add_edge(0.006510000000000001, 0.0075, 0.0075, 0.0075)
geometry.add_edge(0.0075, 0.0075, 0.0075, 0.006)
geometry.add_edge(0.0075, 0.006, 0.006500000000000001, 0.006)
geometry.add_edge(0.006500000000000001, 0.006, 0.006500000000000001, 0.0075)
geometry.add_edge(0.00551, 0.009000000000000001, 0.00651, 0.009000000000000001)
geometry.add_edge(0.00651, 0.009000000000000001, 0.00651, 0.0075)
geometry.add_edge(0.006500000000000005, 0.0075, 0.00551, 0.0075)
geometry.add_edge(0.00551, 0.0075, 0.00551, 0.009000000000000001)
geometry.add_edge(0.00425, 0.0105, 0.00525, 0.0105)
geometry.add_edge(0.00525, 0.0105, 0.00525, 0.009000000000000001)
geometry.add_edge(0.00525, 0.009000000000000001, 0.00425, 0.009000000000000001)
geometry.add_edge(0.00425, 0.009000000000000001, 0.00425, 0.0105)
geometry.add_edge(0.002, 0.012, 0.003, 0.012)
geometry.add_edge(0.003, 0.012, 0.003, 0.0105)
geometry.add_edge(0.003, 0.0105, 0.002, 0.0105)
geometry.add_edge(0.002, 0.0105, 0.002, 0.012)
geometry.add_edge(0.00307, 0.0135, 0.004070000000000001, 0.0135)
geometry.add_edge(0.004070000000000001, 0.0135, 0.004070000000000001, 0.012)
geometry.add_edge(0.004070000000000001, 0.012, 0.00307, 0.012)
geometry.add_edge(0.00307, 0.012, 0.00307, 0.0135)
geometry.add_edge(0.00159, 0.015, 0.00259, 0.015)
geometry.add_edge(0.00259, 0.015, 0.00259, 0.0135)
geometry.add_edge(0.00259, 0.0135, 0.00159, 0.0135)
geometry.add_edge(0.00159, 0.0135, 0.00159, 0.015)

# BLOCK LABELS
geometry.add_label(0.00376, -0.01425, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00458, -0.012750000000000001, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00411, -0.01125, materials = {'magnetic' : 'J+'})
geometry.add_label(0.005690000000000001, -0.00975, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00623, -0.00825, materials = {'magnetic' : 'J+'})
geometry.add_label(0.007690000000000001, -0.00675, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00817, -0.00525, materials = {'magnetic' : 'J+'})
geometry.add_label(0.010220000000000002, -0.00375, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00867, -0.0022500000000000003, materials = {'magnetic' : 'J+'})
geometry.add_label(0.01207, -0.00075, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00928, 0.00075, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00943, 0.0022500000000000003, materials = {'magnetic' : 'J+'})
geometry.add_label(0.009640000000000001, 0.00375, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00836, 0.00525, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00725, 0.00675, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00626, 0.00825, materials = {'magnetic' : 'J+'})
geometry.add_label(0.005, 0.00975, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00275, 0.01125, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00382, 0.012750000000000001, materials = {'magnetic' : 'J+'})
geometry.add_label(0.00234, 0.01425, materials = {'magnetic' : 'J+'})
geometry.add_label(0.03, 0.03, materials = {'magnetic' : 'air'})
geometry.add_label(0.003, 0.0, materials = {'magnetic' : 'control'})

# SOLVE
problem.solve()
a2d.view.zoom_best_fit()
f = open("solution_plus.csv", "w")

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
