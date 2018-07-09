class Function:
    def __init__(self, inputs = 1, outputs = 1):
        self.number_inputs  = inputs
        self.number_outputs = outputs
    
    def eval(self, x):
        result = 0
        for i in x:
            result += i*i
        return result

class ComsolFunction(Function):
    def __init__(self, inputs, outputs, input_filename, output_filename, model_name):
        
        self.input_filename = input_filename
        self.output_filename = output_filename
        self.model_name = model_name
        

    def run_comsol(self):
        """ Funtion compile model_name.java file and run Comsol in a batch mode."""
        import os        
        file_name = self.model_name[:-5]        
        comsol_path = "/home/david/Apps/comsol53/multiphysics/bin/"
        compile_string =comsol_path +  "comsol compile " +  file_name + ".java"
        run_string = comsol_path + "comsol batch -inputfile " + file_name + ".class"
        
        os.system(compile_string)  # it is necessary only when .java file is changed
        os.system(run_string)
    
    def eval(self, x):      
        # Generate the input file for the external code
        with open(self.input_filename, 'w') as input_file:
            input_file.write('%f %f' % (x[0], x[1]))    # ToDo: generalize
 
                # Parse the output file from the external code and set the value of f_xy
        self.run_comsol()

        y = 0        
        with open(self.output_filename) as file:
            data = file.read()
            lines = data.split("\n")
            y = float(lines[5])
        return y
