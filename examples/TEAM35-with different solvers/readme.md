# TEAM Benchmark 35

This project proposes a different approach for the original DC problem than the papers mentioned earlier. 
The goal of this analyis was to resolve the original three-objective problem as two separate two-objective problems.
During this analysis the proposed task handled as a three-objective optimization task because this form of the problem 
fits better for a real-life design task. 
The previous papers excluded asymmetrical solutions from the optimization. However, 
due to the non-linearity of the optimization problem, some asymmetrical solutions can be competitive with some symmetrical solutions.

This 3D solution space is analyzed in this example, and the analysis made two other modifications on the parameter space of the problem. 
Firstly, the boundaries of the radii-s changed. Secondly, the number of turns varied and the results of these three separate analyses were compared .

# Results

| Best F1    | F1       | F2       | F3  | R1   | R2   | R3   | R4   | R5   | R6   | R7   | R8  | R9   | R10  | R11  | R12  | R13  | R14  | R15  | R16  | R17  | R18  | R19  | R20  |
|------------|----------|----------|-----|------|------|------|------|------|------|------|-----|------|------|------|------|------|------|------|------|------|------|------|------|
| Symmetric  | 1.02E-05 | 5.60E-05 | 118 | 3.55 | 6.09 | 1.29 | 5.16 | 5.76 | 7.22 | 7    | 7.5 | 7.5  | 7.9  | 7.9  | 7.5  | 7.5  | 7    | 7.22 | 5.76 | 5.16 | 1.29 | 6.09 | 3.55 |
| Asymmetric | 2.07E-05 | 6.16E-05 | 100 | 1.29 | 1.47 | 2.43 | 5.02 | 6.42 | 5.43 | 6.54 | 6.8 | 6.99 | 7.14 | 7.18 | 6.92 | 6.69 | 6.67 | 5.82 | 5.55 | 4.47 | 1.47 | 4.61 | 1.06 |


| Best F2    | F1       | F2       | F3  | R1   | R2   | R3   | R4   | R5   | R6   | R7   | R8   | R9   | R10   | R11  | R12  | R13  | R14  | R15  | R16  | R17  | R18  | R19  | R20  |
|------------|----------|----------|-----|------|------|------|------|------|------|------|------|------|-------|------|------|------|------|------|------|------|------|------|------|
| Symmetric  | 0.000249 | 1.53E-05 | 137 | 6.82 | 6.42 | 3.55 | 1.97 | 5.33 | 7.07 | 8.99 | 8.69 | 9.76 | 9.99  | 9.99 | 9.76 | 8.69 | 8.99 | 7.07 | 5.33 | 1.97 | 3.55 | 6.42 | 6.82 |
| Asymmetric | 0.000234 | 2.55E-05 | 110 | 2.51 | 3.33 | 2.86 | 4.44 | 4.98 | 6.44 | 6.92 | 8.97 | 7.42 | 10.82 | 8.03 | 8.18 | 8.39 | 7.11 | 6    | 5.01 | 3.75 | 1.5  | 2.57 | 1.09 |


| Best F3    | F1       | F2       | F3   | R1   | R2   | R3   | R4   | R5   | R6   | R7   | R8   | R9   | R10  | R11  | R12  | R13  | R14  | R15  | R16  | R17  | R18  | R19  | R20  |
|------------|----------|----------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| Symmetric  | 0.000575 | 0.000326 | 56.2 | 1.01 | 1.01 | 1    | 1.01 | 1    | 1.02 | 5.51 | 5.5  | 5.55 | 5.51 | 5.51 | 5.55 | 5.5  | 5.51 | 1.02 | 1    | 1.01 | 1    | 1.01 | 1.01 |
| Asymmetric | 0.000531 | 0.000359 | 65   | 1.14 | 1.12 | 1.01 | 1.29 | 1.03 | 5.48 | 5.65 | 5.75 | 6.03 | 6.62 | 5.69 | 5.67 | 5.73 | 5.54 | 1.31 | 1.37 | 1.17 | 1.07 | 1.08 | 1.26 |


| Last       | F1       | F2       | F3   | R1   | R2   | R3   | R4   | R5   | R6   | R7   | R8   | R9   | R10  | R11  | R12  | R13  | R14  | R15  | R16  | R17  | R18  | R19  | R20  |
|------------|----------|----------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| Symmetric  | 0.000583 | 0.000322 | 56.7 | 1.01 | 1    | 1.01 | 1.01 | 1.04 | 1.15 | 5.61 | 5.5  | 5.5  | 5.54 | 5.54 | 5.5  | 5.5  | 5.61 | 1.15 | 1.04 | 1.01 | 1.01 | 1    | 1.01 |
| Asymmetric | 0.000541 | 0.000279 | 68.6 | 1.16 | 1.12 | 1.01 | 1.67 | 1.15 | 4.35 | 5.84 | 6.07 | 5.96 | 6.71 | 6.08 | 6.49 | 6.38 | 5.94 | 1.3  | 3.15 | 1.17 | 1.08 | 1.03 | 1    |

# Namings

## File naming and structure

Every case has the following file structure:
```
Asymmetric/
├── BestF1
│   ├── solver_scripts
│   │   ├── solution_0.csv
│   │   ├── solution_minus.csv
│   │   ├── solution_plus.csv
│   │   ├── solver_script_0.py
│   │   ├── solver_script_minus.py
│   │   └── solver_script_plus.py
│   └── validation.py
```

```solver_scripts/``` contains the necessary scripts that can be executed by Agros2D.  

- ```solver_scripts_0.py``` solves the problem for the input **X**,
- ```solver_scripts_minus.py``` solves the problem for the input **X**-0.5 mm,
- ```solver_script_plus.py``` solves the problem for the input **X** + 0.5 mm,

where ***X*** is the result from the paper for that case.

```solver_scripts_0.py``` is need for the calculation of the F1 objective function, meanwhile  ```solver_scripts_minus.py```, ```solver_script_plus.py``` are necessary to compute the F2 objective function. After executing the scripts they export the results into the csv files.

- ```validation.py```:
This script reads the csv files for a case and computes the objective functions for the particular ***X*** vector nad prints out the results. **Small differences are expected**

## CSV Structure

```csv
Bz, 1e-06, -0.005, 0.00199194915183
Br, 1e-06, -0.005, -5.83269719979e-09
Bz, 1e-06, -0.0038888888888888888, 0.00199812358553
...
dofs, 4136
nodes, 4222
elements, 2089
```

All *.csv files have the same structure: ```Variable, x, y, Value```. ```Bz``` is the z component of the magnetic flux density, ```Br``` is the radial component of the magnetic flux density, ```x, y``` is the coordinates of the measurement and ```Value``` is the actual measurement value. For example:
|Variable| x | y | Value |
|-|-|-|-|
|Bz| 1e-06| -0.005| 0.00199194915183|
|Br| 1e-06| -0.005| -5.83269719979e-09|

The last 3 rows give information about the mesh. ```dofs``` means the number of degrees, ```nodes``` means the number of node and ```elements``` means the number of elements.

# How to validate

1. Open a terminal and ```cd``` to the desired directory.
2. You can run the simulations if you have Agros2D installed.
2.a Make sure Agros2D is reachable with the Path environmental variable. 
2.b If you are on linux use ```agros2d_solver -s solver_script_0.py```
2.c If you are on windows use ```Solver.exe -s solver_script_0.py```
3. After the you ran all the ```solver_scripts``` run the ```validation.py``` file. You don't have to install any library.
