import os
import re
import paramiko
import tempfile
import os
import datetime
import time
import getpass

from string import Template
from xml.dom import minidom
from artap.enviroment import Enviroment

from abc import ABCMeta, abstractmethod
from .utils import ConfigDictionary

from logging import NullHandler, getLogger
getLogger('paramiko.transport').addHandler(NullHandler())


class Executor(metaclass=ABCMeta):
    """
    Function is a class representing objective or cost function for
    optimization problems.
    """

    NONE = 1
    EXECUTED = 2
    FINISHED = 3
    FAILED = 4

    def __init__(self, problem):
        self.problem = problem
        self.status = Executor.NONE

        self.options = ConfigDictionary()
        # parse method
        self.parse_results = None

    @abstractmethod
    def eval(self, x):
        # set default parse method from problem (can be overriden)
        if not self.parse_results and "parse_results" in dir(self.problem):
            self.parse_results = self.problem.parse_results

    @staticmethod
    def _join_parameters(x, sep=","):
        param_values_string = ""

        for val in x:
            param_values_string += str(val) + sep

        # remove last sep
        if (len(x)) > len(sep):
            param_values_string = param_values_string[:-len(sep)]

        return param_values_string


# TODO: not working
class ComsolExecutor(Executor):

    def __init__(self, problem, model_file, output_file):
        super().__init__(problem)

        self.model_file = model_file
        self.output_file = output_file

    def eval(self, x):
        super().eval(x)

        param_names_string = Executor._join_parameters(self.problem.parameters)
        param_values_string = Executor._join_parameters(x)

        run_string = "{} comsol batch -inputfile {} -nosave -pname {} -plist {}"\
            .format(Enviroment.comsol_path, self.model_file, param_names_string, param_values_string)

        print(run_string)
        os.system(run_string)

        with open(self.output_file) as file:
            content = file.read()
            result = self.parse_results(content)

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

    def __init__(self, problem,
                 model_file, output_file, input_file=None, supplementary_files=None, command=None):
        super().__init__(problem)

        if problem.working_dir is None:
            raise Exception('RemoteExecutor: Problem working directory must be set.')

        self.options.declare(name='hostname', default='',
                             desc='Hostname')
        self.options.declare(name='username', default=getpass.getuser(),
                             desc='Username')
        self.options.declare(name='port', default=22, lower=0,
                             desc='Port')
        self.options.declare(name='password', default='',
                             desc='Password')

        self.remote_dir = ''

        # command
        self.command = command

        # files
        self.model_file = model_file
        self.input_file = input_file
        self.output_file = output_file
        self.supplementary_files = supplementary_files

    def __exit__(self, exc_type, exc_val, exc_tb):
        # remove remote dir
        self._remove_remote_dir()
        # pass

    @abstractmethod
    def eval(self, x):
        super().eval(x)

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
            self.remote_dir = self._create_dir_on_remote(directory=directory, client=client)
            client.close()
        except:
            self.problem.logger.error("Cannot create remote directory '{}' on ''".format(directory, self.options["hostname"]))

    def _transfer_file_to_remote(self, source_file, destination_file, client):
        source = source_file
        dest = self.remote_dir + os.sep + destination_file

        sftp = paramiko.SFTPClient.from_transport(client.get_transport())
        sftp.put(source, dest)

    def _transfer_file_from_remote(self, source_file, destination_file, client):
        dest = destination_file
        source = self.remote_dir + os.sep + source_file
        sftp = paramiko.SFTPClient.from_transport(client.get_transport())
        sftp.get(source, dest)

    def _read_file_from_remote(self, source_file, client):
        try:
            source = self.remote_dir + os.sep + source_file
            sftp = paramiko.SFTPClient.from_transport(client.get_transport())
            remote_file = sftp.open(source)
            result = remote_file.read().decode("utf-8")
            return result
        except IOError as e:
            self.problem.logger.error("Remote file '{}' doesn't exists.".format(source_file))

    def _create_dir_on_remote(self, directory, client):
        d = datetime.datetime.now()
        ts = d.strftime("%Y-%m-%d-%H-%M-%S-%f")

        # projects directory
        client.exec_command("mkdir " + directory)
        # working directory
        wd = directory + os.sep + "artap-" + ts
        client.exec_command("mkdir " + wd)

        return wd

    def _create_file_on_remote(self, source_file, content, client):
        source = self.remote_dir + os.sep + source_file
        sftp = paramiko.SFTPClient.from_transport(client.get_transport())
        with sftp.open(source, 'w') as file:
            file.write(content)

    def _remove_remote_dir(self, client):
        sftp = paramiko.SFTPClient.from_transport(client.get_transport())

        files = sftp.listdir(path=self.remote_dir)
        for f in files:
            filepath = os.path.join(self.remote_dir, f)
            sftp.remove(filepath)

        sftp.rmdir(self.remote_dir)

    def _run_command_on_remote(self, command, client, suppress_stdout=True, suppress_stderr=False):
        # Run ssh command
        output = ""
        if self.remote_dir == "":
            stdin, stdout, stderr = client.exec_command(command)
        else:
            stdin, stdout, stderr = client.exec_command("cd " + self.remote_dir + "; " + command)

        for line in stdout:
            if not suppress_stdout:
                self.problem.logger.info(line.strip('\n'))
            output += line.strip('\n')
        for line in stderr:
            if not suppress_stderr:
                self.problem.logger.error(line.strip('\n'))
        return output

    def _transfer_files_to_remote(self, client):
        # transfer supplementary files
        if self.supplementary_files:
            for file in self.supplementary_files:
                self._transfer_file_to_remote(self.problem.working_dir + os.sep + file, "." + os.sep + file,
                                            client=client)

        # transfer model file
        if self.model_file:
            self._transfer_file_to_remote(self.problem.working_dir + os.sep + self.model_file, self.model_file,
                                        client=client)

    def _transfer_files_from_remote(self, client):
        pass


class RemoteSSHExecutor(RemoteExecutor):
    """
    Allows distributing of calculation of objective functions.
    """

    def __init__(self, problem, command, model_file, output_file, input_file=None, supplementary_files=None):
        super().__init__(problem, model_file, output_file, input_file, supplementary_files, command)

        # set default host
        self.options["hostname"] = Enviroment.ssh_host

        # init remote
        self._init_remote(directory="remote")

    def eval(self, x):
        super().eval(x)

        # create client
        client = self._create_client()

        # transfer supplementary files, input and model file
        self._transfer_files_to_remote(client)

        #  run command on remote
        if self.input_file:
            # parameters
            param_values_string = Executor._join_parameters(x, "\n")
            # create remote file
            self._create_file_on_remote(self.input_file, param_values_string, client=client)
            # execute command on remote
            self._run_command_on_remote("{} {}".format(self.command, self.model_file), client=client)
        else:
            # parameters
            param_values_string = Executor._join_parameters(x)
            # execute command on remote
            self._run_command_on_remote("{} {} {}".format(self.command, self.model_file, param_values_string), client=client)

        # read and parse output file
        content = self._read_file_from_remote(self.output_file, client=client)
        result = self.parse_results(content)

        client.close()

        return result


class CondorJobExecutor(RemoteExecutor):
    """
    Allows distributing of calculation of objective functions.
    """

    def __init__(self, problem,
                 model_file, output_file, input_file=None, supplementary_files=None):
        super().__init__(problem, model_file, output_file, input_file, supplementary_files)

        # set default host
        self.options["hostname"] = Enviroment.condor_host

        # init remote
        self._init_remote(directory="htcondor")

    def _create_job_file(self, ts, x, client):
        # create job file
        with open(self.problem.working_dir + os.sep + "remote.tp", 'r') as job_file:
            job_file = Template(job_file.read())

        # parameters
        param_names_string = Executor._join_parameters(self.problem.parameters)
        param_values_string = Executor._join_parameters(x)
        # file
        job_file = job_file.substitute(model_name=os.path.basename(self.model_file),
                                       output_file="{}_{}".format(ts, self.output_file),
                                       log_file="{}.log".format(ts),
                                       run_file="{}_run.sh".format(ts),
                                       param_names=param_names_string,
                                       param_values=param_values_string)

        self._create_file_on_remote("{}_remote.job".format(ts), job_file, client)

        # create input file with parameters
        if self.input_file:
            # parameters
            param_values_string = Executor._join_parameters(x, "\n")
            # create remote file
            self._create_file_on_remote("{}_{}".format(ts, self.input_file), param_values_string, client=client)

    def _create_run_file(self, ts, client):
        with open(self.problem.working_dir + os.sep + "run.tp", 'r') as run_file:
            run_file = run_file.read()

        # add move command
        substitute = "mv {0} {1} \n".format(self.output_file,
                                            "{}_{}".format(ts, self.output_file))
        run_file += substitute

        self._create_file_on_remote("{}_run.sh".format(ts), run_file, client)

    def eval(self, x):
        super().eval(x)

        success = False
        while not success:
            try:
                # create client
                client = self._create_client()

                # transfer supplementary files, input and model file
                self._transfer_files_to_remote(client)

                d = datetime.datetime.now()
                ts = d.strftime("%Y-%m-%d-%H-%M-%S-%f")

                # apply template for remote.job
                self._create_job_file(ts, x, client)

                # apply template for run.sh
                self._create_run_file(ts, client)

                # submit job
                output = self._run_command_on_remote("condor_submit {}_remote.job".format(ts), client=client)

                # process id
                process_id = re.search('cluster \d+', output).group().split(" ")[1]

                event = ""
                while (event != "Completed") and (event != "Held"):
                    content = self._read_file_from_remote("{}.condor_log".format(process_id), client=client)
                    state = ComsolExecutor.parse_condor_log(content)

                    if state[1] != event:
                        self.problem.logger.info("Job {} is '{}' at {}".format(state[2], state[1], state[3]))
                        event = state[1]

                    if event == "Completed":
                        # stop while cycle
                        break

                    if event == "Held":
                        self.problem.logger.error("Job {} is '{}' at {}".format(state[2], state[1], state[3]))
                        # TODO: remove job?
                        # TODO: abort computation - no success?

                    time.sleep(1.0)

                if event == "Completed":
                    out_file = "{}_{}{}".format(ts,
                                           os.path.splitext(self.output_file)[0],
                                           os.path.splitext(self.output_file)[1])
                    content = self._read_file_from_remote("." + os.sep + out_file, client=client)
                    success = True
                    result = self.parse_results(content)
                else:
                    assert 0

                client.close()
                
                return result

            except Exception as e:
                print(e)
                time.sleep(1)
                continue
