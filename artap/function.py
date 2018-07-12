from fabric import Connection
import sys, paramiko

class Function:
    """
    Function is a class representing objective or cost function for 
    optimization problems.
    """

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
            input_file.write('%f %f' % (x[0], x[1]))    # TODO: generalize
 
        # Parse the output file from the external code and set the value of y
        self.run_comsol()

        y = 0        
        with open(self.output_filename) as file:
            data = file.read()
            lines = data.split("\n")
            y = float(lines[5])
        return y

    
    #TODO: Add tool for automatic generating of .java files
    

class RemoteFunction(Function):   
        """
        Allowes distributing of calculation of obejctive functions. 
        """

        def __init__(self, hostname = "edison.fel.zcu.cz", 
            port = 22, username = "panek50", password = "tkditf_16_2"): #TODO: Make it safe
            self.hostname = hostname
            self.port = port
            self.username = username
            self.password = password

        def transfer_files_to_remote(self, source_file, destination_file):           
           source = source_file
           dest   = destination_file

           try:
               t = paramiko.Transport((self.hostname, self.port))
               t.connect(username=self.username, password=self.password)
               sftp = paramiko.SFTPClient.from_transport(t)
               sftp.put(source, dest)

           finally:
                t.close()            

        def transfer_files_from_remote(self, source_file, destination_file):
           dest = destination_file
           source = source_file

           try:
               t = paramiko.Transport((self.hostname, self.port))
               t.connect(username=self.username, password=self.password)
               sftp = paramiko.SFTPClient.from_transport(t)
               sftp.get(source, dest)

           finally:
                t.close()            

        def run_command_on_remote(self, command):
            # Run ssh command
            try:
                client = paramiko.SSHClient()
                client.load_system_host_keys()
                client.set_missing_host_key_policy(paramiko.WarningPolicy())
                client.connect(self.hostname, port = self.port, username = self.username, password = self.password,)

                stdin, stdout, stderr = client.exec_command(command)
                # print(stdout.read(),)

            finally:
                client.close()


        def eval(self, x):
            y = 0
            self.transfer_files_to_remote('./tests/eval.py', "eval.py")
                
            with open("./tests/parameters.txt", 'w') as input_file:
                input_file.write(str(x[0]) + " " + str(x[1]))
            
            self.transfer_files_to_remote('./tests/parameters.txt', 'parameters.txt')          
            connection = Connection('edison.fel.zcu.cz', user = 'panek50', port = 22, connect_kwargs={'password': 'tkditf_16_2'})
            connection.run("python ./tests/eval.py")                        
            connection.close()
            self.transfer_files_from_remote('output.txt', './tests/output.txt')            
            with open("./tests/output.txt") as file:
                y = float(file.read())
            
            return y

class CondorJobFunction(RemoteFunction):
    """ Allwes submit goal function calculation as a HT Condor job """
    def __init__(self, ):
        super().__init__()

    
    def eval(self, x):
            y = 0
            self.transfer_files_to_remote('./tests/eval.py', './tests/eval.py')
            self.transfer_files_to_remote('./tests/condor.job', './tests/condor.job')
                
            with open("./tests/parameters.txt", 'w') as input_file:
                input_file.write(str(x[0]) + " " + str(x[1]))
            
            self.transfer_files_to_remote('./tests/parameters.txt', './tests/parameters.txt')          
            
            connection = Connection('edison.fel.zcu.cz', user = 'panek50', port = 22, connect_kwargs={'password': 'tkditf_16_2'})            
            connection.run("condor_submit ./tests/condor.job")               
            connection.close()
            
            self.transfer_files_from_remote('./tests/output.txt', './tests/output.txt')            
            with open("./tests/output.txt") as file:
                y = file.read()
            
            return y


if __name__ == "__main__":
    function = CondorJobFunction()
    print(function.eval([1, 1]))