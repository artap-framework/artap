import textwrap
import re
import paramiko
import os
import datetime
import time
import ntpath
from string import Template
from xml.dom import minidom
from artap.environment import Enviroment

from abc import ABCMeta, abstractmethod
from .utils import ConfigDictionary
from shutil import copyfile

from logging import NullHandler, getLogger
getLogger('paramiko.transport').addHandler(NullHandler())


class Executor(metaclass=ABCMeta):

    """
    Function is a class representing objective or cost function for
    optimization problems.
    """

    def __init__(self, problem):
        self.problem = problem

        self.options = ConfigDictionary()
        # parse method
        self.parse_results = None

    @abstractmethod
    def eval(self, x):
        # set default parse method from problem (can be overridden)
        if self.parse_results is None and "parse_results" in dir(self.problem):
            self.parse_results = self.problem.parse_results

    @staticmethod
    def _join_parameters_names(parameters, sep=","):
        param_names_string = ""

        for parameter in parameters:
            param_names_string += str(parameter['name']) + sep

        # remove last sep
        if (len(parameters)) > len(sep):
            param_names_string = param_names_string[:-len(sep)]

        return param_names_string

    @staticmethod
    def _join_parameters_values(x, sep=","):
        param_values_string = ""
        for number in x:
            param_values_string += str(number) + sep

        # remove last sep
        if (len(x)) > len(sep):
            param_values_string = param_values_string[:-len(sep)]

        return param_values_string

    @staticmethod
    def _remove_dir(local_dir):
        files = os.listdir(path=local_dir)
        for f in files:
            filepath = os.path.join(local_dir, f)
            os.remove(filepath)

        os.rmdir(local_dir)


class LocalComsolExecutor(Executor):

    comsol_command = Template("comsol batch -inputfile $input_file -nosave -pname $param_names -plist $param_values")

    def __init__(self, problem, problem_file, input_files=None, output_files=None):
        super().__init__(problem)
        self.model_file = ntpath.basename(problem_file)
        copyfile(problem_file, self.problem.working_dir + self.model_file)

        self.output_files = output_files
        self.input_files = input_files

    def eval(self, individual):
        super().eval(individual)

        param_names_string = Executor._join_parameters_names(self.problem.parameters)
        param_values_string = Executor._join_parameters_values(individual.vector)

        run_string = self.comsol_command.substitute(input_file=self.model_file,
                                                    param_names=param_names_string,
                                                    param_values=param_values_string)

        # run command
        current_path = os.getcwd()
        os.chdir(self.problem.working_dir)
        os.system(run_string)
        os.chdir(current_path)
        output_files = []
        for file in self.output_files:
            output_files.append(self.problem.working_dir + file)
        result = self.parse_results(output_files, individual)
        return result

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


class RemoteExecutor(Executor):
    """
        Allows distributing of calculation of objective functions.
        """

    # ToDo: Make inheritated classes: Matlab, Comsol ...

    def __init__(self, problem, command, files_to_server, files_from_server=None):
        super().__init__(problem)

        if problem.working_dir is None:
            raise Exception('RemoteExecutor: Problem working directory must be set.')

        self.options.declare(name='hostname', default=Enviroment.ssh_host,
                             desc='Hostname')
        self.options.declare(name='username', default=Enviroment.ssh_login,
                             desc='Username')
        self.options.declare(name='port', default=22, lower=0,
                             desc='Port')
        self.options.declare(name='password', default=None,
                             desc='Password')

        # command
        self.command = command

        # files
        self.input_files = files_to_server
        self.output_files = files_from_server

    @abstractmethod
    def eval(self, individual):
        super().eval(individual)

    def _create_client(self):
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=self.options["hostname"],
                       username=self.options["username"],
                       password=self.options["password"])

        return client

    def _init_remote(self, directory):
        try:
            # create client
            client = self._create_client()
            remote_dir = self._create_dir_on_remote(directory=directory, client=client)
            client.close()
            return remote_dir
        except paramiko.ssh_exception.SSHException:
            self.problem.logger.error("Cannot create remote directory '{}' on ''".format(directory,
                                                                                         self.options["hostname"]))

    @staticmethod
    def _transfer_file_to_remote(source_file, destination_file, remote_dir, client):
        source = source_file
        dest = remote_dir + os.sep + destination_file

        sftp = paramiko.SFTPClient.from_transport(client.get_transport())
        sftp.put(source, dest)

    @staticmethod
    def _transfer_file_from_remote(source_file, destination_file, remote_dir, client):
        dest = destination_file
        source = remote_dir + os.sep + source_file
        sftp = paramiko.SFTPClient.from_transport(client.get_transport())
        sftp.get(source, dest)

    def _read_file_from_remote(self, source_file, remote_dir, client):
        try:
            source = remote_dir + os.sep + source_file
            sftp = paramiko.SFTPClient.from_transport(client.get_transport())
            remote_file = sftp.open(source)
            result = remote_file.read().decode("utf-8")
            return result
        except IOError:
            self.problem.logger.error("Remote file '{}' doesn't exists.".format(source_file))

    @staticmethod
    def _create_dir_on_remote(directory, client):
        d = datetime.datetime.now()
        ts = d.strftime("%Y-%m-%d-%H-%M-%S-%f")

        # projects directory
        client.exec_command("mkdir " + directory)

        # working directory
        wd = directory + os.sep + "artap-" + ts
        client.exec_command("mkdir " + wd)

        return wd

    @staticmethod
    def _create_file_on_remote(source_file, content, remote_dir, client):
        source = remote_dir + os.sep + source_file
        sftp = paramiko.SFTPClient.from_transport(client.get_transport())
        with sftp.open(source, 'w') as file:
            file.write(content)

    @staticmethod
    def _remove_remote_dir(remote_dir, client):
        sftp = paramiko.SFTPClient.from_transport(client.get_transport())

        files = sftp.listdir(path=remote_dir)
        for f in files:
            filepath = os.path.join(remote_dir, f)
            sftp.remove(filepath)

        sftp.rmdir(remote_dir)

    def _run_command_on_remote(self, command, remote_dir, client, suppress_stdout=True, suppress_stderr=False):
        # Run ssh command
        if remote_dir == "":
            stdin, stdout, stderr = client.exec_command(command)
        else:
            stdin, stdout, stderr = client.exec_command("cd " + remote_dir + "; " + command)

        # output
        output = ""
        for line in stdout:
            output += line.strip('\n')

        if not suppress_stdout:
            lines = ""
            for line in stdout:
                lines += line + '\n'
            self.problem.logger.info(lines)

        if not suppress_stderr:
            lines = ""
            for line in stdout:
                lines += line + '\n'
            if len(lines) > 0:
                self.problem.logger.error(lines)

        return output

    def _transfer_files_to_remote(self, remote_dir, client):
        # transfer input files
        if self.input_files:
            for file in self.input_files:
                self._transfer_file_to_remote(self.problem.working_dir + os.sep + file, "." + os.sep + file,
                                              remote_dir=remote_dir, client=client)

    def _transfer_files_from_remote(self, client):
        pass


class CondorJobExecutor(RemoteExecutor):
    """
    Allows distributing of calculation of objective functions.
    """

    condor_command = """condor_submit remote.job"""

    condor_job_template = Template(textwrap.dedent("""\
        universe = vanilla
        initialdir = ./
        executable = $run_file
        arguments = $arguments
        requirements = (OpSys == "LINUX" && Arch == "X86_64")

        input = $input_file
        output = $log_file
        log = $$(cluster).condor_log
        error = $$(cluster)_$$(process).condor_err

        request_cpus = 10
        request_memory = 10 GB
        log_xml = true
        should_transfer_files = yes
        when_to_transfer_output = ON_EXIT
        transfer_input_files = $input_files
        transfer_output_files = $output_files
        transfer_executable = true
        queue"""))

    def __init__(self, problem, files_to_condor, files_from_condor=None):
        super().__init__(problem, self.condor_command, files_to_condor, files_from_condor)

        # set default host
        self.options["hostname"] = Enviroment.condor_host
        self.job_file = None
        self.condor_executable = None

    @abstractmethod
    def _create_job_file(self, remote_dir, individual, client):
        pass

    def eval(self, individual):
        super().eval(individual)

        # init remote
        remote_dir = self._init_remote(directory="htcondor")

        success = False
        while not success:
            try:
                # create client
                client = self._create_client()

                # apply template for remote.job
                self._create_job_file(remote_dir, individual, client)

                # Create
                self._create_file_on_remote("remote.job", self.job_file, remote_dir=remote_dir, client=client)
                self._create_file_on_remote("run.sh", self.condor_executable, remote_dir=remote_dir,
                                            client=client)

                # transfer supplementary files, input and model file
                self._transfer_files_to_remote(remote_dir, client)

                # submit job
                output = self._run_command_on_remote("condor_submit remote.job", remote_dir=remote_dir, client=client)

                # process id
                process_id = re.search(r'cluster \d+', output).group().split(" ")[1]

                event = ""
                start = time.time()
                while (event != "Completed") and (event != "Held"):
                    content = self._read_file_from_remote("{}.condor_log".format(process_id),
                                                          remote_dir=remote_dir, client=client)
                    state = LocalComsolExecutor.parse_condor_log(content)

                    if state[1] != event:
                        self.problem.logger.info("Job {} is '{}' at {}".format(state[2], state[1], state[3]))
                        event = state[1]

                    if event == "Completed":
                        # stop while cycle
                        break

                    if (event == "Held") or (event == "JobAbortedEvent"):
                        self.problem.logger.error("Job {} is '{}' at {}".format(state[2], state[1], state[3]))
                        # read log
                        content_log = self._read_file_from_remote("{}.log".format(self.output_files[0]),
                                                                  remote_dir=remote_dir, client=client)
                        self.problem.logger.error(content_log)
                        # remove job
                        self._run_command_on_remote("condor_rm {}".format(process_id),
                                                    remote_dir=remote_dir, client=client)
                        # TODO: abort computation - no success?
                        raise RuntimeError

                    end = time.time()
                    if (end - start) > self.problem.options["time_out"]:
                        raise TimeoutError

                if event == "Completed":
                    output_files = []
                    d = datetime.datetime.now()
                    ts = d.strftime("%Y-%m-%d-%H-%M-%S-%f")
                    path = self.problem.working_dir + 'artap' + ts
                    os.system("mkdir {0}".format(path))

                    for file in self.output_files:
                        self._transfer_file_from_remote(source_file=file, destination_file=path + os.sep + file,
                                                        remote_dir=remote_dir, client=client)
                        output_files.append(path + os.sep + file)
                    success = True
                    result = self.parse_results(output_files, individual)
                    self._remove_remote_dir(remote_dir, client=client)

                    if self.problem.options['save_data_files'] is False:
                        self._remove_dir(path)
                else:
                    assert 0

                # self._remove_remote_dir(remote_dir=remote_dir, client=client)

                client.close()

                return result

            except ConnectionError as e:
                print(e)
                time.sleep(1.0)
                continue


class CondorComsolJobExecutor(CondorJobExecutor):
    """

    """
    arguments = Template("-inputfile $input_file -nosave -pname $param_names -plist $param_values")
    executable = textwrap.dedent("""\
        #!/bin/sh
        /opt/comsol-5.4/bin/comsol batch $@
        """)

    def __init__(self, problem, model_file, files_from_condor=None):
        self.model_file = ntpath.basename(model_file)
        super().__init__(problem, [self.model_file], files_from_condor)
        copyfile(model_file, self.problem.working_dir + self.model_file)

    def _create_job_file(self, remote_dir, individual, client):
        output_files_str = ",".join(self.output_files)
        param_names_string = Executor._join_parameters_names(self.problem.parameters)
        param_values_string = Executor._join_parameters_values(individual.vector)
        arguments = self.arguments.substitute(input_file=os.path.basename(self.model_file),
                                              param_names=param_names_string,
                                              param_values=param_values_string)

        self.job_file = self.condor_job_template.substitute(input_file=os.path.basename(self.model_file),
                                                            run_file="run.sh",
                                                            arguments=arguments,
                                                            input_files=self.model_file,
                                                            output_files=output_files_str,
                                                            log_file="{}.log".format(self.output_files[0]))
        self.condor_executable = self.executable


class CondorMatlabJobExecutor(CondorJobExecutor):

    executable = textwrap.dedent("""\
    #!/bin/sh
    # args
    s=$@

    /opt/matlab-R2018b/bin/matlab -nodisplay -nosplash -nodesktop -r ${s%.m}""")

    def __init__(self, problem, script, parameter_file, files_from_condor=None):
        self.script = ntpath.basename(script)
        super().__init__(problem, [self.script], files_from_condor)
        self.parameter_file = parameter_file
        copyfile(script, self.problem.working_dir + self.script)

    def _create_job_file(self, remote_dir, individual, client):
        condor_output_files = ",".join(self.output_files)
        condor_input_files = self.parameter_file + ", " + self.input_files[0]
        # create input file with parameters

        if self.parameter_file:
            # parameters
            param_values_string = Executor._join_parameters_values(individual.vector, "\n")
            # create remote file
            self._create_file_on_remote(self.parameter_file, param_values_string, remote_dir=remote_dir, client=client)

        self.job_file = self.condor_job_template.substitute(input_file=os.path.basename(self.script),
                                                            run_file="run.sh",
                                                            arguments=self.script,
                                                            input_files=condor_input_files,
                                                            output_files=condor_output_files,
                                                            log_file="{}.log".format(self.output_files[0]))
        self.condor_executable = self.executable


class CondorPythonJobExecutor(CondorJobExecutor):

    executable = textwrap.dedent("""\
        #!/bin/sh
        # args
                      
        python3 $@""")

    def __init__(self, problem, script, parameter_file, output_files=None):
        self.script = ntpath.basename(script)
        super().__init__(problem, [self.script], output_files)
        self.parameter_file = parameter_file
        copyfile(script, self.problem.working_dir + self.script)

    def _create_job_file(self, remote_dir, individual, client):
        condor_output_files = ",".join(self.output_files)
        condor_input_files = self.script
        # create input file with parameters

        if self.parameter_file:
            # parameters
            # create remote file
            param_values_string = Executor._join_parameters_values(individual.vector, "\n")
            condor_input_files += ", " + self.parameter_file
            self.arguments = self.script + " " + self.parameter_file
            self._create_file_on_remote(self.parameter_file, param_values_string, remote_dir=remote_dir,
                                        client=client)
        else:
            param_values_string = Executor._join_parameters_values(individual.vector, ",")
            self.arguments = self.script + " " + param_values_string

        self.job_file = self.condor_job_template.substitute(input_file=os.path.basename(self.script),
                                                            run_file="run.sh",
                                                            arguments=self.arguments,
                                                            input_files=condor_input_files,
                                                            output_files=condor_output_files,
                                                            log_file="{}.log".format(self.output_files[0]))
        self.condor_executable = self.executable
