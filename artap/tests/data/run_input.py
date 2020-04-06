def eval(x):
    return x[0]**2 + x[1]**2     

if __name__ == "__main__":
    # parameters    
    x = []
    with open("input.txt", 'r') as file:
        params = file.read().split("\n")
        
        for val in params:
            x.append(float(val))

    # eval
    out = eval(x)
    
    with open("output.txt", 'w') as file:
        file.write(str(out))

