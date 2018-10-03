import re
import paramiko
import sys
import tempfile
import traceback
import os
import datetime
from string import Template
from xml.dom import minidom

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
            run_string += parameter + ","
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

    def __del__(self):
        # close connection
        self.client.close()

    def create_remote_dir(self, directory="htcondor"):
        try:
            d = datetime.datetime.now()
            ts = d.strftime("%Y-%m-%d-%H-%M-%S-%f")

            # projects directory
            self.client.exec_command("mkdir " + directory)
            # working directory
            wd = directory + "/" + "artap-" + ts
            self.client.exec_command("mkdir " + wd)

            return wd

        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
            try:
                self.client.close()
            except IOError:
                pass
            sys.exit(1)

    def transfer_files_to_remote(self, source_file, destination_file):
        source = source_file
        dest = self.remote_dir + "/" + destination_file

        try:
            sftp = paramiko.SFTPClient.from_transport(self.client.get_transport())
            sftp.put(source, dest)

        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
            try:
                self.client.close()
            except IOError:
                pass
            sys.exit(1)

    def transfer_files_from_remote(self, source_file, destination_file):
        dest = destination_file
        source = self.remote_dir + "/" + source_file

        try:
            sftp = paramiko.SFTPClient.from_transport(self.client.get_transport())
            sftp.get(source, dest)

        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
            try:
                self.client.close()
            except IOError:
                pass
            sys.exit(1)

    def read_file_from_remote(self, source_file):
        source = self.remote_dir + "/" + source_file

        try:
            sftp = paramiko.SFTPClient.from_transport(self.client.get_transport())
            remote_file = sftp.open(source)
            return remote_file.read().decode("utf-8")

        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
            try:
                self.client.close()
            except IOError:
                pass
            sys.exit(1)

    def create_file_on_remote(self, source_file):
        source = self.remote_dir + "/" + source_file

        try:
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

    def remove_remote_dir(self):
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

    def run_command_on_remote(self, command, suppress_stdout=True, suppress_stderr=False):
        # Run ssh command
        output = ""
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

        self.parameters = parameters
        self.output_filename = output_filename
        self.model_name = model_name
        self.time_out = time_out

        if supplementary_files is None:
            supplementary_files = []
        supplementary_files.append(self.model_name)

        super().__init__(hostname, username, password, port, working_dir=working_dir,
                         supplementary_files=supplementary_files)

    # TODO: Internal use
    # def eval_batch(self, table):
    #
    #     self.transfer_files_to_remote(self.working_dir + '/' + self.model_name, './' + self.model_name)
    #
    #     # add parameters
    #     param_names_string = ""
    #     for parameter in self.parameters:
    #         param_names_string += parameter + ","
    #     # remove last comma
    #     if (len(self.parameters)) > 1:
    #         param_names_string = param_names_string[:-1]
    #
    #     ids = []
    #     i = 0
    #     for x in table:
    #         # add values
    #         param_values_string = ""
    #         for val in x:
    #             param_values_string += str(val) + ","
    #         # remove last comma
    #         if (len(x)) > 1:
    #             param_values_string = param_values_string[:-1]
    #
    #         i += 1
    #         with open(self.working_dir + "/remote.tp", 'r') as job_file:
    #             job_file = Template(job_file.read())
    #
    #         output_filename = os.path.basename(self.output_filename)
    #
    #         job_file = job_file.substitute(model_name=os.path.basename(self.model_name),
    #                                        output_file="{0}{1}{2}".format(os.path.splitext(output_filename)[0], ts,
    #                                                                       os.path.splitext(output_filename)[1]),
    #                                        log_file="comsol%d.log" % i, run_file="run%d.sh" % i,
    #                                        param_names=param_names_string,
    #                                        param_values=param_values_string)
    #
    #         job_remote_file = self.create_file_on_remote("remote%d.job" % i)
    #         job_remote_file.write(job_file)
    #
    #         with open(self.working_dir + "/run.tp", 'r') as run_file:
    #             run_file = Template(run_file.read())
    #
    #         output_file = os.path.splitext(output_filename)[0] + str(i) + os.path.splitext(output_filename)[1]
    #         run_file = run_file.substitute(output_base_file=output_filename, output_file=output_file)
    #
    #         job_run_file = self.create_file_on_remote("run%d.sh" % i)
    #         job_run_file.write(run_file)
    #
    #         # run
    #         output = self.run_command_on_remote("condor_submit remote%d.job" % i)
    #         process_id = re.search('cluster \d+', output).group().split(" ")[1]
    #         ids.append(process_id)
    #
    #     event = dict()
    #
    #     for process_id in ids:
    #         event[process_id] = ""
    #
    #     while any((e != "Completed" and e != "Held") for e in event.values()):
    #         for process_id in ids:
    #             content = self.read_file_from_remote("%s.condor_log" % process_id)
    #             state = RemoteCondorExecutor.parse_condor_log(content)
    #
    #             if state[1] != event[process_id]:
    #                 print(state)
    #             event[process_id] = state[1]
    #
    #     result = []
    #     for j in range(len(table)):
    #         index = j + 1
    #         if event[ids[j]] == "Completed":
    #             content = self.read_file_from_remote('./max%d.txt' % index)
    #             y = float(content.split("\n")[5])
    #             result.append(y)
    #         else:
    #             result.append(0)
    #             assert 0
    #
    #     # remove remote dir
    #     self.remove_remote_dir()
    #
    #     return result

    def eval(self, x):
        self.transfer_files_to_remote(self.working_dir + '/' + self.model_name, './' + self.model_name)
        param_names_string = ""
        for parameter in self.parameters:
            param_names_string += parameter + ","  # remove last comma
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

        job_remote_file = self.create_file_on_remote("remote%s.job" % ts)
        job_remote_file.write(job_file)

        with open(self.working_dir + "/run.tp", 'r') as run_file:
            run_file = Template(run_file.read())

        output_file = os.path.splitext(output_filename)[0] + ts + os.path.splitext(output_filename)[1]
        run_file = run_file.substitute(output_base_file=output_filename, output_file=output_file)

        job_run_file = self.create_file_on_remote("run%s.sh" % ts)
        job_run_file.write(run_file)

        # run
        output = self.run_command_on_remote("condor_submit remote%s.job" % ts)
        process_id = re.search('cluster \d+', output).group().split(" ")[1]

        event = ""

        while event != "Completed":
            content = self.read_file_from_remote("%s.condor_log" % process_id)
            state = RemoteCondorExecutor.parse_condor_log(content)

            if state[1] != event:
                print(state)
                event = state[1]

        if state[1] == "Completed":
            content = self.read_file_from_remote('./max%s.txt' % ts)
            result = float(content.split("\n")[5])
        else:
            assert 0

        # remove remote dir
        self.remove_remote_dir()

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

        parameters_file = self.create_file_on_remote("parameters.txt")
        parameters_file.write(str(x[0]) + " " + str(x[1]))
        parameters_file.close()

        for file in self.supplementary_files:
            self.transfer_files_to_remote(self.working_dir + '/' + file, './' + file)
        output = self.run_command_on_remote("condor_submit ./remote.job")
        print("output:", output)
        process_id = re.search('cluster \d+', output).group().split(" ")[1]

        event = ""
        while event != "Completed":  # If the job is complete it disappears from que
            content = self.read_file_from_remote("%s.condor_log" % process_id)
            state = RemoteCondorExecutor.parse_condor_log(content)

            if state[1] != event:
                print(state)
            event = state[1]

        content = self.read_file_from_remote(self.output_filename)
        y = float(content[0])

        # remove remote dir
        self.remove_remote_dir()

        return y
