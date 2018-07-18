""" Module cares about generating pseudo-random numbers, vectors and populations"""
#TODO: Latin Hypercube, differend kind of probability distribution etc.
#TODO: Decide if add to problem or make own class


from random import random

def gen_population(population_size, vector_length, parameters):
    population = []
    
    for i in range(population_size):    
        population.append(gen_vector(vector_length, parameters))
    return population

def gen_vector(vector_length, parameters: dict):    
        
    vector = []
    for parameter in parameters.items():
                
        if not('bounds' in parameter[1]):
            bounds = None
        else:
            bounds = parameter[1]['bounds']

        if not('precision' in parameter[1]):
            precision = None
        else:
            precision = parameter[1]['precision']
        
        if (precision == None) and (bounds == None):
            vector.append(gen_number())
            continue
        
        if (precision == None):
            vector.append(gen_number(bounds=bounds))
            continue

        if (bounds == None):
            vector.append(gen_number(precision=precision))
            continue

        vector.append(gen_number(bounds, precision))

    return vector

def gen_number(bounds = [], precision = 0):

    if bounds == []:
        bounds = [0, 1]
    
    if precision == 0:
        precision = 1e-12
        
    number = random() * (bounds[1] - bounds[0]) + bounds[0] 
    number = round(number / precision) * precision 

    return number

if __name__ == "__main__":
    print(gen_population(3,3,{'x_1': { 'initial_value': 10, 'bounds': [0, 5], 'precision': 0.01},
                           'x_2': { 'initial_value': 10, 'bounds': [0, 5], 'precision': 0.01}, 
                           'x_3': { 'initial_value': 10, 'bounds': [0, 5], 'precision': 0.01}}))
        
    print(gen_population(3,3,{'x_1': { 'initial_value': 10, 'precision': 0.01},
                        'x_2': { 'initial_value': 10, 'bounds': [0, 5], 'precision': 0.01}, 
                        'x_3': { 'initial_value': 10, 'bounds': [0, 5], 'precision': 0.01}}))
                
    print(gen_population(3,3,{'x_1': { 'initial_value': 10},
                        'x_2': { 'initial_value': 10, 'bounds': [0, 5], 'precision': 0.01}, 
                        'x_3': { 'initial_value': 10, 'bounds': [0, 5], 'precision': 0.01}}))