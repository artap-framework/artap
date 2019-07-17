import sys


def evaluate(x):
    return x[0]**2 + x[1]**2     


if __name__ == "__main__":
    # parameters    
    
    params = sys.argv[1].split(",")
    print(params)
    x = []
    for val in params:
        x.append(float(val))

    # eval
    out = evaluate(x)
    
    # write
    with open("output.txt", 'w') as file:
        file.write(str(out))
