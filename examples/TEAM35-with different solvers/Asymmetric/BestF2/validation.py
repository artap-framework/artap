import operator
from pathlib import Path
from collections import defaultdict
import math

def read_results(filename):
    results = defaultdict(list)
    if filename.exists():
        with open(filename, "r") as f:
            for line in f:
                line = line.strip().split(",")
                if len(line) == 2:
                    results[line[0]] = float(line[1])
                else:
                    results[line.pop(0)].append(tuple(float(xi) for xi in line))
    else:
        raise RuntimeError(f'{filename} is missing. Try to run the solver_scripts.')

    return results


def calculate_objective_functions(X, resn, res, resp):
    Bz = [pointvalue[2] for pointvalue in res["Bz"]]  # [x, y, Bz(x, y)]
    Br = [pointvalue[2] for pointvalue in res["Br"]]  # [x, y, Br(x, y)]
    xi = [pointvalue[0] for pointvalue in res["Br"]]  # [x, y, Br(x, y)]
    yi = [pointvalue[1] for pointvalue in res["Br"]]  # [x, y, Br(x, y)]
    nb_nodes = res["nodes"]

    # Calculate F1
    B0 = 2e-3
    F1 = max(map(lambda Bz_i: abs(Bz_i - B0), Bz))

    # Calculate F2

    Bzp = [pointvalue[2] for pointvalue in resp["Bz"]]
    Brp = [pointvalue[2] for pointvalue in resp["Br"]]

    Bzn = [pointvalue[2] for pointvalue in resn["Bz"]]
    Brn = [pointvalue[2] for pointvalue in resn["Br"]]

    deltaBpz = map(operator.abs, map(operator.sub, Bzp, Bz))
    deltaBpr = map(operator.abs, map(operator.sub, Brp, Br))
    deltaBp = map(math.sqrt, map(lambda a, b: a ** 2 + b ** 2, deltaBpz, deltaBpr))

    deltaBnz = map(operator.abs, map(operator.sub, Bzn, Bz))
    deltaBnr = map(operator.abs, map(operator.sub, Brn, Br))
    deltaBn = map(math.sqrt, map(lambda a, b: a ** 2 + b ** 2, deltaBnz, deltaBnr))

    F2 = max(map(operator.add, deltaBp, deltaBn))

    # Calcukate F3
    F3 = sum(X)

    return [F1, F2, F3]

def print_objective_funcitons(res):
    F1, F2, F3 = res
    print(f'F1: {F1:.2e}\t F2: {F2:.2e}\t F3: {F3:.0f}')
    
def main():
    X = [2.51, 3.33, 2.86, 4.44, 4.98, 6.44, 6.92, 8.97, 7.42, 10.82, 8.03, 8.18, 8.39, 7.11, 6, 5.01, 3.75, 1.5, 2.57, 1.09]

    dir_data = Path(__file__).parent / "solver_scripts"
    res_minus = read_results(dir_data/"solution_minus.csv")
    res_0 = read_results(dir_data/"solution_0.csv")
    res_plus = read_results(dir_data/"solution_plus.csv")


    print_objective_funcitons(calculate_objective_functions(X, res_minus, res_0, res_plus))

if __name__ == "__main__":
    main()
