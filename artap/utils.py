""" Module cares about generating pseudo-random numbers, vectors and populations"""
#TODO: Latin Hypercube, differend kind of probability distribution etc.
#TODO: Decide if add to problem or make own class


from random import random

def gen_population(population_size, vector_length, bounds = [], precisions = []):
    population = []
    for i in range(population_size):
        population.append(gen_vector(vector_length, bounds, precisions))
    return population

def gen_vector(vector_length, bounds = [], precisions = []):
    
    vector = []
    if (len(bounds) == 0) and (len(precisions) == 0):     
        for i in range(vector_length):
            vector.append(gen_number())
        return vector
    
    if (len(bounds) == 0):     
        for i in range(vector_length):
            vector.append(gen_number(precision=precisions[i]))
        return vector

    if (len(precisions) == 0):     
        for i in range(vector_length):
            vector.append(gen_number(bounds=bounds[i]))
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
    print(gen_number([1, 2], 0.01))
    print(gen_number())
    print(gen_vector(10))
    print(gen_vector(3, precisions=[0.1, 0.1, 0.1]))
    print(gen_population(3,3,precisions=[0.1, 0.1, 0.1]))
