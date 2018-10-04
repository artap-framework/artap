import re
import paramiko
import sys
import tempfile
import traceback
import os
import datetime
import time
from string import Template
from xml.dom import minidom
from multiprocessing import Lock
from artap.enviroment import Enviroment


class Executor:
    """
    Function is a class representing objective or cost function for
    optimization problems.
    """

    def __init__(self):
        pass

    def exec(self, x):
        pass


# TODO: For internal use
# class LocalBatchExecutor(Executor):
#
#     def __init__(self, evaluate):
#         self.evaluate = evaluate
#         super().__init__()
#
#     def exec(self, x: list):
#         return self.evaluate(x)
#
#     def exec_batch(self, table: list):
#         n = len(table)
#         results = [0]*n
#         for i in range(len(table)):
#             results[i] = self.evaluate(table[i])
#         return results


class ComsolExecutor(Executor):

    def __init__(self, parameters, model_name, output_filename):
        super().__init__()
        self.parameters = parameters
        self.output_filename = output_filename
        self.model_name = model_name

    def run_comsol(self, x):
        """ Function compile model_name.java file and run Comsol in a batch mode."""
        import os
        comsol_path = Enviroment.comsol_path
        run_string = comsol_path + "comsol batch -inputfile " + self.model_name + " -nosave -pname "

        # add parameters
        for parameter in self.parameters:
            run_string += parameter + ", "

        # remove last comma
        if (len(self.parameters)) > 1:
            run_string = run_string[:-1]

        run_string += " -plist "

        # add values
        for val in x:
            run_string += str(val) + ","

        # remove last comma
        if (len(x)) > 1:
            run_string = run_string[:-1]

        # print(run_string)
        os.system(run_string)

    def eval(self, x):
        # Parse the output file from the external code and set the value of y
        self.run_comsol(x)

        with open(self.output_filename) as file:
            data = file.read()
            lines = data.split("\n")
            y = float(lines[5])
        return y


class RemoteExecutor(Executor):
    """
        Allows distributing of calculation of objective functions.
        """

    def __init__(self, hostname=None,
                 username=None, password=None, port=22, working_dir=None, supplementary_files=None):
        super().__init__()
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.working_dir = working_dir
        self.supplementary_files = supplementary_files
        self.script = ""
        self.lock = Lock()
        try:
            self.client = paramiko.SSHClient()
            self.client.load_system_host_keys()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(hostname=self.hostname, username=self.username, password=self.password)

            self.status = "None"
            self.host = ""

            self.remote_dir = self.create_remote_dir()

        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
            try:
                self.client.close()
            except IOError:
                pass
            sys.exit(1)

    def create_remote_dir(self, directory="htcondor", client=None):
        if client is not None:
            self.client = client
        try:
            d = datetime.datetime.now()
            ts = d.strftime("%Y-%m-%d-%H-%M-%S-%f")

            # projects directory
            self.client.exec_command("mkdir " + directory)
            # working directory
            wd = directory + "/" + "artap-" + ts
            self.lock.acquire()
            self.client.exec_command("mkdir " + wd)
            self.lock.release()

            return wd

        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
            try:
                self.client.close()
            except IOError:
                pass
            sys.exit(1)

    def transfer_files_to_remote(self, source_file, destination_file, client=None):
        if client is not None:
            self.client = client
        source = source_file
        dest = self.remote_dir + "/" + destination_file

        try:
            self.lock.acquire()
            sftp = paramiko.SFTPClient.from_transport(self.client.get_transport())
            sftp.put(source, dest)
            self.lock.release()

        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
            try:
                self.client.close()
            except IOError:
                pass
            sys.exit(1)

    def transfer_files_from_remote(self, source_file, destination_file, client=None):
        if client is not None:
            self.client = client
        dest = destination_file
        source = self.remote_dir + "/" + source_file

        try:
            self.lock.acquire()
            sftp = paramiko.SFTPClient.from_transport(self.client.get_transport())
            sftp.get(source, dest)
            self.lock.release()

        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
            try:
                self.client.close()
            except IOError:
                pass
            sys.exit(1)

    def read_file_from_remote(self, source_file, client):
        if client is not None:
            self.client = client
        source = self.remote_dir + "/" + source_file

        try:
            self.lock.acquire()
            sftp = paramiko.SFTPClient.from_transport(self.client.get_transport())
            remote_file = sftp.open(source)
            result = remote_file.read().decode("utf-8")
            self.lock.release()
            return result

        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
            try:
                self.client.close()
            except IOError:
                pass
            sys.exit(1)

    def create_file_on_remote(self, source_file, client):
        if client is not None:
            self.client = client
        source = self.remote_dir + "/" + source_file

        try:
            self.lock.acquire()
            sftp = paramiko.SFTPClient.from_transport(self.client.get_transport())
            return sftp.open(source, 'w')

        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
            try:
                self.client.close()
            except IOError:
                pass
            sys.exit(1)

        finally:
            self.lock.release()

    def remove_remote_dir(self, client):
        if client is not None:
            self.client = client

        try:
            sftp = paramiko.SFTPClient.from_transport(self.client.get_transport())

            files = sftp.listdir(path=self.remote_dir)
            for f in files:
                filepath = os.path.join(self.remote_dir, f)
                sftp.remove(filepath)

            sftp.rmdir(self.remote_dir)

        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
            try:
                self.client.close()
            except IOError:
                pass
            sys.exit(1)

    def run_command_on_remote(self, command, suppress_stdout=True, suppress_stderr=False, client=None):
        if client is not None:
            self.client = client
        # Run ssh command
        output = ""

        self.lock.acquire()
        try:
            if self.remote_dir == "":
                stdin, stdout, stderr = self.client.exec_command(command)
            else:
                stdin, stdout, stderr = self.client.exec_command("cd " + self.remote_dir + "; " + command)

            for line in stdout:
                if not suppress_stdout:
                    print(line.strip('\n'))
                output += line.strip('\n')
            for line in stderr:
                if not suppress_stderr:
                    print(line.strip('\n'))

        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
            try:
                self.client.close()
            except IOError:
                pass
            sys.exit(1)

        finally:
            self.lock.release()
        return output

    def eval(self, x):

        for file in self.supplementary_files:
            self.transfer_files_to_remote(self.working_dir + '/' + file, './' + file)

        parameters_file = tempfile.NamedTemporaryFile(mode="w", delete=False)
        parameters_file.write(str(x[0]) + " " + str(x[1]))
        parameters_file.close()

        output_file = tempfile.NamedTemporaryFile(mode="w", delete=False)
        output_file.close()

        self.transfer_files_to_remote(parameters_file.name, 'parameters.txt')
        self.run_command_on_remote("python3 remote.py")

        self.transfer_files_from_remote('output.txt', output_file.name)
        with open(output_file.name) as file:
            y = float(file.read())

        os.remove(parameters_file.name)
        os.remove(output_file.name)

        return y


class RemoteCondorExecutor(RemoteExecutor):
    """
        Allows distributing of calculation of obejctive functions.
        """

    def __init__(self, hostname=None,
                 username=None, password=None, port=22, working_dir=None, supplementary_files=None):
        super().__init__(hostname, username, password, port, working_dir=working_dir,
                         supplementary_files=supplementary_files)

    @staticmethod
    def parse_condor_log(content):
        pre_hack = '<?xml version="1.0"?><!DOCTYPE classads SYSTEM "classads.dtd"><classads>'
        post_hack = "</classads>"

        xml_doc = minidom.parseString(pre_hack + content + post_hack)
        event_time = ""
        state = ""
        cluster = 0

        class_ads = xml_doc.getElementsByTagName('c')
        execute_host = ""  # only in "ExecuteEvent"
        for c in class_ads:
            ads = c.getElementsByTagName('a')

            state = ""
            event_time = ""
            cluster = 0
            for a in ads:
                n = a.attributes['n'].value

                if n == "MyType":
                    s = a.getElementsByTagName('s')[0].firstChild.nodeValue

                    if s == "JobTerminatedEvent":
                        state = "Completed"
                    elif s == "SubmitEvent":
                        state = "Submitted"
                    elif s == "ExecuteEvent":
                        state = "Executed"
                    elif s == "JobImageSizeEvent":
                        state = "Running"
                    elif s == "JobDisconnectedEvent":
                        state = "Disconnected"
                    elif s == "JobAbortedEvent":
                        state = "JobAbortedEvent"
                    elif s == "JobHeldEvent":
                        state = "Held"

                if n == "EventTime":
                    s = a.getElementsByTagName('s')[0].firstChild.nodeValue
                    event_time = s.replace("T", " ")

                if n == "ExecuteHost":
                    s = a.getElementsByTagName('s')[0].firstChild.nodeValue
                    execute_host = s.split(":")[0][1:]

                if n == "Cluster":
                    s = a.getElementsByTagName('i')[0].firstChild.nodeValue
                    cluster = int(s)

            # print(event_time + ": " + state + "\t" + execute_host)

        return [event_time, state, cluster, execute_host]


class CondorComsolJobExecutor(RemoteCondorExecutor):
    """ Allows submit goal function calculation as a HT Condor job """

    def __init__(self, parameters, model_name, output_filename, hostname=None,
                 username=None, password=None, port=22, working_dir=None, supplementary_files=None, time_out=None):

        super().__init__(hostname, username, password, port, working_dir=working_dir)

        self.parameters = parameters
        self.output_filename = output_filename
        self.model_name = model_name
        self.time_out = time_out

        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=self.hostname, username=self.username, password=self.password)
        self.transfer_files_to_remote(self.working_dir + '/' + self.model_name, './' + self.model_name, client)
        client.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        # remove remote dir
        self.remove_remote_dir()

    def eval(self, x):
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=self.hostname, username=self.username, password=self.password)

        param_names_string = ""
        for parameter in self.parameters:
            param_names_string += parameter + ","
        if (len(self.parameters)) > 1:
           param_names_string = param_names_string[:-1]

        param_values_string = ""
        for val in x:
            param_values_string += str(val) + ","
        # remove last comma
        if (len(x)) > 1:
            param_values_string = param_values_string[:-1]

        with open(self.working_dir + "/remote.tp", 'r') as job_file:
            job_file = Template(job_file.read())

        output_filename = os.path.basename(self.output_filename)
        d = datetime.datetime.now()
        ts = d.strftime("%Y-%m-%d-%H-%M-%S-%f")

        job_file = job_file.substitute(model_name=os.path.basename(self.model_name),
                                       output_file="{0}{1}{2}".format(os.path.splitext(output_filename)[0], ts,
                                                                      os.path.splitext(output_filename)[1]),
                                       log_file="comsol%s.log" % ts, run_file="run%s.sh" % ts,
                                       param_names=param_names_string,
                                       param_values=param_values_string)

        job_config_file = self.create_file_on_remote("remote%s.job" % ts, client)
        job_config_file.write(job_file)
        job_config_file.close()

        with open(self.working_dir + "/run.tp", 'r') as run_file:
            run_file = Template(run_file.read())

        output_file = os.path.splitext(output_filename)[0] + ts + os.path.splitext(output_filename)[1]
        run_file = run_file.substitute(output_base_file=output_filename, output_file=output_file)

        job_run_file = self.create_file_on_remote("run%s.sh" % ts, client)
        job_run_file.write(run_file)
        job_run_file.close()

        # run
        output = self.run_command_on_remote("condor_submit remote%s.job" % ts, client)

        process_id = re.search('cluster \d+', output).group().split(" ")[1]

        event = ""

        while event != "Completed":
            content = self.read_file_from_remote("%s.condor_log" % process_id, client)
            state = RemoteCondorExecutor.parse_condor_log(content)
            time.sleep(2)
            if state[1] != event:
                print(state)
                event = state[1]

        if state[1] == "Completed":
            content = self.read_file_from_remote('./max%s.txt' % ts, client)
            result = float(content.split("\n")[5])
        else:
            assert 0
        client.close()
        return result


class CondorPythonJobExecutor(RemoteCondorExecutor):
    """ Allows submit goal function calculation as a HT Condor job """

    def __init__(self, parameters, model_name, output_filename, hostname=None,
                 username=None, password=None, port=22, working_dir=None, supplementary_files=None):

        self.parameters = parameters
        self.output_filename = output_filename
        self.model_name = model_name

        super().__init__(hostname, username, password, port, working_dir=working_dir,
                         supplementary_files=supplementary_files)

    def eval(self, x):

        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=self.hostname, username=self.username, password=self.password)

        parameters_file = self.create_file_on_remote("parameters.txt", client)
        parameters_file.write(str(x[0]) + " " + str(x[1]))
        parameters_file.close()

        for file in self.supplementary_files:
            self.transfer_files_to_remote(self.working_dir + '/' + file, './' + file, client)
        output = self.run_command_on_remote("condor_submit ./remote.job")
        print("output:", output)
        process_id = re.search('cluster \d+', output).group().split(" ")[1]

        event = ""
        while event != "Completed":  # If the job is complete it disappears from que
            content = self.read_file_from_remote("%s.condor_log" % process_id, client)
            state = RemoteCondorExecutor.parse_condor_log(content)

            if state[1] != event:
                print(state)
            event = state[1]

        content = self.read_file_from_remote(self.output_filename, client)
        y = float(content[0])

        # remove remote dir
        self.remove_remote_dir(client)
        client.close()
        return y

