import atexit
import rpyc
from rpyc.core.service import ClassicService

from .individual import Individual

MONITOR_PORT = 16000


class ArtapMonitorService(ClassicService):
    def __init__(self, problem):
        super().__init__()
        self.problem = problem

        # self.artap_dir = "/var/lib/artap/"

    def on_connect(self, conn):
        super().on_connect(conn)
        # print("Connected (ArtapMonitorService): ", self, conn)

    def on_disconnect(self, conn):
        super().on_disconnect(conn)
        # print("Disconnected (ArtapMonitorService): ", self, conn)

    def stats(self):
        st = {}
        st["populations_count"] = len(self.problem.populations)
        st["individuals_count"] = 0
        st["individuals_stats"] = { "empty": 0, "in_progress": 0, "evaluated": 0, "failed": 0 }
        for population in self.problem.populations:
            st["individuals_count"] += len(population.individuals)
            for individual in population.individuals:
                if individual.state == Individual.State.EMPTY:
                    st["individuals_stats"]["empty"] += 1
                elif individual.state == Individual.State.IN_PROGRESS:
                    st["individuals_stats"]["in_progress"] += 1
                elif individual.state == Individual.State.EVALUATED:
                    st["individuals_stats"]["evaluated"] += 1
                elif individual.state == Individual.State.FAILED:
                    st["individuals_stats"]["failed"] += 1

        return st

    def populations(self):
        return self.problem.populations

    def problem(self):
        return self.problem


class MonitorService:
    def __init__(self, problem):
        self.problem = problem
        self.server = None
        self.port = 0

        self.start_server()

    def start_server(self):
        port = MONITOR_PORT
        while True:
            try:
                self.server = rpyc.utils.server.ThreadedServer(ArtapMonitorService(self.problem), port=port, auto_register=False)
                break
            except OSError as e:
                # print("Error: {}, port = {}".format(e.strerror, port))
                if e.strerror == "Address already in use":
                    port = port + 1
                    continue

        self.port = self.server.port
        self.problem.logger.info("Problem monitor created at {} port {}".format(self.server.host, self.port))
        self.server.logger.quiet = False
        self.server._start_in_thread()

