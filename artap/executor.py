import time
import re
import paramiko
import sys
import tempfile
import traceback
import os

class Executor:
    """
    Function is a class representing objective or cost function for 
    optimization problems.
    """

    def __init__(self, inputs = 1, outputs = 1):
        self.number_inputs  = inputs
        self.number_outputs = outputs
    
    def exec(self, x):
        pass

class ComsolExecutor(Executor):
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
    
class RemoteExecutor(Executor):   
        """
        Allowes distributing of calculation of obejctive functions. 
        """

        def __init__(self, hostname = None, 
            username = None, password = None, port = 22): 
            self.hostname = hostname
            self.port = port
            self.username = username
            self.password = password

            self.script = ""

            try:              
                self.client = paramiko.SSHClient()
                self.client.load_system_host_keys()
                self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())            
                self.client.connect(hostname=self.hostname, username=self.username, password=self.password)
        
                self.status = "None"
                self.host = ""

            except Exception as e:
                print('*** Caught exception: %s: %s' % (e.__class__, e))
                traceback.print_exc()
                try:
                    self.client.close()
                except:
                    pass
                sys.exit(1)

        def __del__(self):
            # close connection
            self.client.close()

        def transfer_files_to_remote(self, source_file, destination_file):           
           source = source_file
           dest = destination_file

           try:
                sftp = paramiko.SFTPClient.from_transport(self.client.get_transport())
                sftp.put(source, dest)

           except Exception as e:
                print('*** Caught exception: %s: %s' % (e.__class__, e))
                traceback.print_exc()
                try:
                    self.client.close()
                except:
                    pass
                sys.exit(1)

        def transfer_files_from_remote(self, source_file, destination_file):
            dest = destination_file
            source = source_file

            try:
                sftp = paramiko.SFTPClient.from_transport(self.client.get_transport())
                sftp.get(source, dest)

            except Exception as e:
                print('*** Caught exception: %s: %s' % (e.__class__, e))
                traceback.print_exc()
                try:
                    self.client.close()
                except:
                    pass
                sys.exit(1)                         

        def run_command_on_remote(self, command):
            # Run ssh command
            output = ""
            try:
                stdin, stdout, stderr = self.client.exec_command(command)                
                for line in stdout:
                    print(line.strip('\n'))
                    output += line.strip('\n')
                for line in stderr:
                    print(line.strip('\n'))            

            except Exception as e:
                print('*** Caught exception: %s: %s' % (e.__class__, e))
                traceback.print_exc()
                try:
                    self.client.close()
                except:
                    pass
                sys.exit(1)
            
            return output

        def eval(self, x):
            y = 0
            self.transfer_files_to_remote(self.script, "remote_eval.py")
                
            parameters_file = tempfile.NamedTemporaryFile(mode = "w", delete=False)
            parameters_file.write(str(x[0]) + " " + str(x[1]))
            parameters_file.close()
            
            output_file = tempfile.NamedTemporaryFile(mode = "w", delete=False)
            output_file.close()

            self.transfer_files_to_remote(parameters_file.name, 'parameters.txt')          
            self.run_command_on_remote("python3 remote_eval.py")
            
            self.transfer_files_from_remote('output.txt', output_file.name)            
            with open(output_file.name) as file:
                y = float(file.read())
            
            os.remove(parameters_file.name)
            os.remove(output_file.name)

            return y

class CondorJobExecutor(RemoteExecutor):
    """ Allwes submit goal function calculation as a HT Condor job """
    def __init__(self, hostname = None, 
            username = None, password = None, port = 22):

            super().__init__(hostname, username, password, port)

    
    def eval(self, x):
            y = 0
            self.transfer_files_to_remote('./remote_eval.py', './tests/remote_eval.py')
            self.transfer_files_to_remote('./tests/condor.job', './tests/condor.job')
                
            with open("./parameters.txt", 'w') as input_file:
                input_file.write(str(x[0]) + " " + str(x[1]))
            
            self.transfer_files_to_remote('./tests/parameters.txt', './tests/parameters.txt')                              
            output = self.run_command_on_remote("condor_submit ./tests/condor.job")                                   
            id = re.search('cluster \d+', output).group().split(" ")[1]                        
            output = "run"
            start =  time.time()
            while (output != ""):      # If the job is complete it disappears from que
                output = self.run_command_on_remote("condor_q -l " + str(id))                
                if (time.time() - start) > 1:   # Time out is 5 seconds 
                    print(time.time() - start)
                    # break
            
            self.transfer_files_from_remote('./tests/output.txt', './tests/output.txt')            
            with open("./tests/output.txt") as file:
                y = file.read()            
            return y

if __name__ == "__main__":
    function = CondorJobExecutor()
    print(function.eval([1, 1]))