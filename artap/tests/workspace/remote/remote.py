def eval():
    """ Generate the input file for the external code. """    
    with open("parameters.txt") as input_file:
        data = input_file.read().split()
        x = []
        y = 0
        for number in data:
            x.append(float(number))
            y += float(number) * float(number)
 
    with open("output.txt", 'w') as file:
        file.write(str(y))
       

if __name__ == "__main__":
    eval()
