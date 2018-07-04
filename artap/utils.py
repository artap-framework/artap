from random import random

def gen_number(bounds, precision):
    if not((type(bounds) is list) or (type(bounds) is tuple)):
        raise TypeError
        
        
    if (len(bounds) != 2):
        raise TypeError

    output = random() * (bounds[1] - bounds[0]) + bounds[0] 
    output = round(output / precision) * precision 

    return(output)

if __name__ == "__main__":
    print(gen_number([1, 2], 0.01))