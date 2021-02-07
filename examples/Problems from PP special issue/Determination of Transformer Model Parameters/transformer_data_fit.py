from artap.problem import Problem
from artap.algorithm_genetic import NSGAII, EpsMOEA
from artap.algorithm_swarm import SMPSO
from artap.results import Results
import cmath, math


class TransformerDataFit(Problem):

    def set(self):
        # Not mandatory to give a name for the test problem
        self.name = 'Transformer'
        self.working_dir = '.'
        self.parameters = [{'name': 'R1', 'bounds': [0.1, 100]},
                           {'name': 'X1', 'bounds': [0.1, 100]},
                           {'name': 'Rm', 'bounds': [2000, 12000]},
                           {'name': 'Xm', 'bounds': [1000, 4000]}]
        self.costs = [{'name': 'F', 'criteria': 'minimize'}]

    def evaluate(self, individual):
        # Five measured data
        U1 = [230.34,   229.36, 229.02,  228.13, 48.634]
        I1 = [0.116,    0.3485, 0.57078, 1.2748, 1.1055]
        pF = [0.2136,   0.9267, 0.9693,  0.9921, 0.9922]
        U2 = [13.026,   12.414, 11.951,  10.95,  0.0]
        RL = [math.inf, 2.3448, 1.2745,  0.4992, 0.0]

        # Model parameters
        R1 = individual.vector[0]
        R2 = R1
        X1 = individual.vector[1]
        X2 = X1
        Rm = individual.vector[2]
        Xm = individual.vector[3]
        a  = U1[0]/U2[0]

        # Objective function
        F = 0.0
        for i in range(len(U1)):
            if i == 0:
                Zp = 1.0 / (1.0 / Rm + 1.0 / (1j * Xm))
            else:
                Zp = 1.0 / (1.0 / Rm + 1.0 / (1j * Xm) + 1.0 / (a*a*RL[i] + R2 + 1j * X2))
            Ze  = R1 + 1j * X1 + Zp
            aZe = abs(Ze)
            fZe = cmath.phase(Ze)
            F   = F + (U1[i] / aZe / I1[i] - 1.0) ** 2.0 + (math.cos(fZe) / pF[i] - 1.0) ** 2.0

            if i < len(U1)-1:
                if i == 0:
                    U2c = U1[i] * Zp / Ze
                else:
                    U2c = U1[i] * Zp / Ze * a*a*RL[i] / (a*a*RL[i] + R2 + 1j * X2)
                U2c = abs(U2c) / a
                F   = F + (U2c / U2[i] - 1.0) ** 2.0
        return [F]


# Initialization of the problem
problem = TransformerDataFit()

# Perform the optimization
algorithm  = NSGAII(problem)
#algorithm = EpsMOEA(problem)
#algorithm = SMPSO(problem)
algorithm.options['max_population_number'] = 500
algorithm.options['max_population_size'] = 100
algorithm.run()

# Post - processing the results
results = Results(problem)
# results.pareto_values()

res_individual = results.find_optimum()
print(res_individual.vector)
for i in range(len(problem.parameters)):
    print("{} : {}".format(problem.parameters[i].get("name"), res_individual.vector[i]))

R1 = res_individual.vector[0]
R2 = R1
X1 = res_individual.vector[1]
X2 = X1
Rm = res_individual.vector[2]
Xm = res_individual.vector[3]

# Check by measurement
U1 = [230.34,   229.36, 229.02,  228.13, 48.634]
I1 = [0.116,    0.3485, 0.57078, 1.2748, 1.1055]
pF = [0.2136,   0.9267, 0.9693,  0.9921, 0.9922]
U2 = [13.026,   12.414, 11.951,  10.95,  0.0]
RL = [math.inf, 2.3448, 1.2745,  0.4992, 0.0]
a  = U1[0]/U2[0]

for i in range(len(U1)):
    if i == 0:
        Zp = 1.0 / (1.0 / Rm + 1.0 / (1j * Xm))
    else:
        Zp = 1.0 / (1.0 / Rm + 1.0 / (1j * Xm) + 1.0 / (a*a*RL[i] + R2 + 1j * X2))
    Ze  = R1 + 1j * X1 + Zp
    aZe = abs(Ze)
    fZe = cmath.phase(Ze)

    if i == 0:
        U2c = U1[i] * Zp / Ze
    else:
        U2c = U1[i] * Zp / Ze * a*a*RL[i] / (a*a*RL[i] + R2 + 1j * X2)
    U2c = abs(U2c)/a
    print(I1[i],U1[i]/aZe,pF[i],math.cos(fZe),U2[i],U2c)