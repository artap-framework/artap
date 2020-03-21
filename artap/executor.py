import textwrap
import re
import tempfile
import os
import subprocess
import datetime
import time
import ntpath
from string import Template

import rpyc
from rpyc.core.async_ import AsyncResultTimeout
from rpyc.utils.classic import upload_file, download_file

from abc import ABCMeta, abstractmethod
from .utils import ConfigDictionary
from shutil import copyfile

from artap.config import config


# parse ip address
def parse_address(address):
    regex_match = re.compile(r'<(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}):.*').match(address)
    if regex_match is not None:
        return regex_match.group(1)
    return ""


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

        cmd_string = self.comsol_command.substitute(input_file=self.model_file,
                                                    param_names=param_names_string,
                                                    param_values=param_values_string)

        try:
            # run command
            current_path = os.getcwd()
            os.chdir(self.problem.working_dir)

            out = subprocess.run(cmd_string, shell=True)
            os.chdir(current_path)

            if out.returncode != 0:
                err = "Unknown error"
                if out.stderr is not None:
                    err = "Cannot run COMSOL Multiphysics.\n\n {}".format(out.stderr)

                self.problem.logger.error(err)
                raise RuntimeError(err)

            output_files = []
            for file in self.output_files:
                output_files.append(self.problem.working_dir + file)
            result = self.parse_results(output_files, individual)

            return result
        except Exception as e:
            err = "Cannot run COMSOL Multiphysics.\n\n {}".format(e)
            self.problem.logger.error(err)
            raise RuntimeError(err)


class RemoteExecutor(Executor):
    """
        Allows distributing of calculation of objective functions.
        """

    def __init__(self, problem, command, files_to_server, files_from_server=None):
        super().__init__(problem)

        if problem.working_dir is None:
            raise Exception('RemoteExecutor: Problem working directory must be set.')

        self.options.declare(name='hostname', default=config["condor_host"],
                             desc='Hostname')
        self.options.declare(name='username', default=config["condor_login"],
                             desc='Username')
        self.options.declare(name='port', default=15900, lower=0,
                             desc='Port')

        # command
        self.command = command

        # files
        self.input_files = files_to_server
        self.output_files = files_from_server

    @abstractmethod
    def eval(self, individual):
        super().eval(individual)

    def _create_client(self):
        # key = os.path.join(os.path.dirname(__file__), "cert/artap.key")
        # cert = os.path.join(os.path.dirname(__file__), "cert/artap.crt")

        channel = rpyc.Channel(rpyc.SocketStream.connect(self.options["hostname"], self.options["port"]))
        channel.send(self.options["username"].encode('utf-8'))
        response = channel.recv()
        AUTH_ERROR = b'error'
        if response == AUTH_ERROR:
            raise rpyc.utils.authenticators.AuthenticationError('Invalid username for daemon')

        return rpyc.utils.factory.connect_channel(channel, service=rpyc.core.ClassicService)
        # return rpyc.classic.connect(self.options["hostname"], self.options["port"])
        # return rpyc.classic.ssl_connect(self.options["hostname"], self.options["port"], keyfile=key, certfile=cert)

    def _init_remote(self, client):
        try:
            # create client
            remote_dir = client.root.create_job_dir()
            return remote_dir
        except RuntimeError as e:
            #self.problem.logger.error("Cannot create remote directory '{}' on ''".format(directory,
            #                                                                             self.options["hostname"]))
            print("ERROR --------------------------------")
            pass

    @staticmethod
    def _create_file_on_remote(destination_file, content, remote_dir, client):
        fp = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
        fp.write(content)
        fp.close()

        RemoteExecutor._transfer_file_to_remote(fp.name, destination_file, remote_dir, client)

        os.unlink(fp.name)

    @staticmethod
    def _transfer_file_to_remote(source_file, destination_file, remote_dir, client):
        source = source_file
        dest = remote_dir + os.sep + destination_file

        upload_file(client, localpath=source, remotepath=client.root.artap_dir + os.sep + dest)

    @staticmethod
    def _transfer_file_from_remote(source_file, destination_file, remote_dir, client):
        dest = destination_file
        source = remote_dir + os.sep + source_file

        download_file(client, remotepath=client.root.artap_dir + os.sep + source, localpath=dest)

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
    def __init__(self, problem, files_to_condor, files_from_condor=None):
        super().__init__(problem, "", files_to_condor, files_from_condor)

        # set default host
        self.options["hostname"] = config["condor_host"]

        # set default requirements
        self.requirements = ""
        self.request_cpus = -1
        self.request_memory = -1
        self.hold_on_start = False

    @abstractmethod
    def _create_job_file(self, remote_dir, individual, client):
        pass

    def eval(self, individual):
        if config["condor_host"] is None:
            raise Exception("Condor host is not defined.")

        super().eval(individual)

        success = False
        while not success:
            try:
                # create client
                client = self._create_client()

                # init remote
                remote_dir = self._init_remote(client=client)
                # self.problem.logger.info("RemoteDir {}".format(remote_dir))

                # transfer supplementary files, input and model file
                self._transfer_files_to_remote(remote_dir, client)

                # submit job
                try:
                    self._create_job_file(remote_dir, individual, client)
                except AsyncResultTimeout as e:
                    print("ERROR - {} - try again ({})".format(e, remote_dir))
                    # remove job dir
                    client.root.remove_job_dir(remote_dir)
                    client.close()
                    # resubmit
                    return self.eval(individual)

                start = time.time()

                events = []
                cnt = 0
                return_value = -1
                delay = 0.5

                run = True
                while run:
                    eventlog = client.root.eventlog(remote_dir)
                    for e in eventlog:
                        if {e["timestamp"], e["type"]} not in events:
                            events.append({e["timestamp"], e["type"]})

                    # print("len(events) = {}".format(len(events)))
                    if len(events) > 0:
                        for i in range(cnt, len(events)):
                            event = eventlog[i]
                            tp = event["type"]

                            args = ""

                            if tp == "submit":
                                # SUBMIT
                                if "ReturnValue" in event["info"]:
                                    return_value = event["info"]["ReturnValue"]
                            elif tp == "execute":
                                # EXECUTE
                                if "ExecuteHost" in event["info"]:
                                    args += "ExecuteHost: {}, ".format(parse_address(event["info"]["ExecuteHost"]))
                            elif tp == "image_size":
                                # IMAGE_SIZE
                                pass
                            elif tp == "job_terminated":
                                # JOB_TERMINATED
                                if "ReturnValue" in event["info"]:
                                    return_value = event["info"]["ReturnValue"]
                                run = False
                            elif tp == "job_held":
                                # JOB_HELD
                                if "ReturnValue" in event["info"]:
                                    return_value = event["info"]["ReturnValue"]

                                self.problem.logger.error("Job {}.{} is '{}' at {}".format(event["cluster"], event["proc"], event["type"], ""))
                                run = False
                                # read log
                                #content_log = self._read_file_from_remote("{}.log".format(self.output_files[0]),
                                #                                          remote_dir=remote_dir, client=client)
                                #self.problem.logger.error(content_log)
                                # remove job
                                # self._run_command_on_remote("condor_rm {}".format(process_id),
                                #                            remote_dir=remote_dir, client=client)
                                raise RuntimeError

                            if len(args) > 0:
                                args = args[:-2]

                            self.problem.logger.info("Job {}.{} ({}) is '{}' at {}".format(event["cluster"], event["proc"], remote_dir, event["type"], args))
                            # print("{}: {} ({})".format(eventlog[i].timestamp, eventlog[i].type, args))

                    if run:
                        cnt = len(events)
                        time.sleep(delay)

                end = time.time()
                if (end - start) > self.problem.options["time_out"]:
                    raise TimeoutError

                # successfull
                if return_value == 0:
                    if len(self.output_files) > 0:
                        output_files = []
                        d = datetime.datetime.now()
                        ts = d.strftime("%Y-%m-%d-%H-%M-%S-%f")
                        path = self.problem.working_dir + 'artap' + ts
                        os.mkdir(path)

                        for file in self.output_files:
                            self._transfer_file_from_remote(source_file=file, destination_file=path + os.sep + file,
                                                            remote_dir=remote_dir, client=client)
                            output_files.append(path + os.sep + file)
                        success = True
                        result = self.parse_results(output_files, individual)

                    # remove job dir
                    if result is not None:
                        client.root.remove_job_dir(remote_dir)

                    if self.problem.options['save_data_files'] is False:
                        self._remove_dir(path)
                else:
                    assert 0

                # remove job dir
                # client.root.remove_job_dir(remote_dir)

                client.close()

                return result

            except ConnectionError as e:
                print(e)
                time.sleep(1.0)
                continue


class CondorPythonJobExecutor(CondorJobExecutor):
    def __init__(self, problem, script, parameter_file, output_files=None, python_path="python3"):
        self.script = ntpath.basename(script)
        super().__init__(problem, [self.script], output_files)

        self.parameter_file = parameter_file
        copyfile(script, self.problem.working_dir + self.script)

        self.executable = textwrap.dedent("""\
            #!/bin/sh
            # args

            """ + python_path + """  $@""")

    def _create_job_file(self, remote_dir, individual, client):
        condor_output_files = self.output_files

        condor_input_files = [self.script]
        # create input file with parameters

        if self.parameter_file:
            # parameters
            # create remote file
            param_values_string = Executor._join_parameters_values(individual.vector, "\n")
            condor_input_files.append(self.parameter_file)
            arguments = self.script + " " + self.parameter_file
            self._create_file_on_remote(self.parameter_file, param_values_string, remote_dir=remote_dir,
                                        client=client)
        else:
            param_values_string = Executor._join_parameters_values(individual.vector, ",")
            arguments = self.script + " " + param_values_string

        # create executable
        self._create_file_on_remote("run.sh", self.executable, remote_dir=remote_dir, client=client)

        # desc
        desc = {}
        desc["type"] = "python"
        desc["extension"] = ".py"
        desc["editor"] = True
        desc["name"] = "Python"

        client.root.submit_job(remote_dir=remote_dir,
                               executable=client.root.artap_dir + os.sep + remote_dir + os.sep + "run.sh",
                               arguments=arguments,
                               input_files=condor_input_files,
                               output_files=condor_output_files,
                               requirements=self.requirements,
                               request_cpus=self.request_cpus,
                               request_memory=self.request_memory,
                               hold_on_start=self.hold_on_start,
                               desc=desc)


class CondorMatlabJobExecutor(CondorJobExecutor):
    def __init__(self, problem, script, parameter_file, files_from_condor=None, matlab_path="/opt/matlab-R2018b/bin/matlab"):
        self.script = ntpath.basename(script)
        super().__init__(problem, [self.script], files_from_condor)
        self.parameter_file = parameter_file
        copyfile(script, self.problem.working_dir + self.script)

        self.executable = textwrap.dedent("""\
            #!/bin/sh
            # args
            s=$@

            """ + matlab_path + """ -nodisplay -nosplash -nodesktop -r ${s%.m}""")

    def _create_job_file(self, remote_dir, individual, client):
        condor_output_files = self.output_files
        condor_input_files = [self.parameter_file, self.input_files[0]]

        # create input file with parameters
        if self.parameter_file:
            # parameters
            param_values_string = Executor._join_parameters_values(individual.vector, "\n")
            # create remote file
            self._create_file_on_remote(self.parameter_file, param_values_string, remote_dir=remote_dir, client=client)

        # create executable
        self._create_file_on_remote("run.sh", self.executable, remote_dir=remote_dir, client=client)

        # desc
        desc = {}
        desc["type"] = "matlab"
        desc["extension"] = ".m"
        desc["editor"] = False
        desc["name"] = "Matlab"

        client.root.submit_job(remote_dir=remote_dir,
                               executable=client.root.artap_dir + os.sep + remote_dir + os.sep + "run.sh",
                               arguments=self.script,
                               input_files=condor_input_files,
                               output_files=condor_output_files,
                               requirements=self.requirements,
                               request_cpus=self.request_cpus,
                               request_memory=self.request_memory,
                               hold_on_start=self.hold_on_start,
                               desc=desc)


class CondorComsolJobExecutor(CondorJobExecutor):
    def __init__(self, problem, model_file, files_from_condor=None, comsol_path="/opt/comsol-5.4/bin/comsol"):
        self.model_file = ntpath.basename(model_file)
        super().__init__(problem, [self.model_file], files_from_condor)
        copyfile(model_file, self.problem.working_dir + self.model_file)

        self.arguments = Template("-inputfile $input_file -nosave -pname $param_names -plist $param_values")
        self.executable = textwrap.dedent("""\
                #!/bin/sh
                """ + comsol_path + """ batch $@
                """)

        self.request_cpus = 3
        self.request_memory = 30

    def _create_job_file(self, remote_dir, individual, client):
        condor_output_files = self.output_files

        param_names_string = Executor._join_parameters_names(self.problem.parameters)
        param_values_string = Executor._join_parameters_values(individual.vector)
        arguments = self.arguments.substitute(input_file=os.path.basename(self.model_file),
                                              param_names=param_names_string,
                                              param_values=param_values_string)

        # create executable
        self._create_file_on_remote("run.sh", self.executable, remote_dir=remote_dir, client=client)

        # desc
        desc = {}
        desc["type"] = "comsol"
        desc["extension"] = ".mph"
        desc["editor"] = False
        desc["name"] = "Comsol Multiphysics"

        client.root.submit_job(remote_dir=remote_dir,
                               executable=client.root.artap_dir + os.sep + remote_dir + os.sep + "run.sh",
                               arguments=arguments,
                               input_files=[self.model_file],
                               output_files=condor_output_files,
                               requirements=self.requirements,
                               request_cpus=self.request_cpus,
                               request_memory=self.request_memory,
                               hold_on_start=self.hold_on_start,
                               desc=desc)
