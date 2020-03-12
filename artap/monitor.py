import rpyc
from rpyc.core.service import ClassicService


class ArtapMonitorService(ClassicService):
    def __init__(self, problem):
        super().__init__()
        self.problem = problem

        # self.artap_dir = "/var/lib/artap/"

    def on_connect(self, conn):
        super().on_connect(conn)
        # print("Connected (ArtapMonitorService): ", self, conn)

    def populations(self):
        return self.problem.data_store.populations


class MonitorService:
    def __init__(self, problem):
        self.problem = problem
        self.port = 0

        self.server = rpyc.utils.server.ThreadedServer(ArtapMonitorService(self.problem), port=0, auto_register=False)
        self.port = self.server.port
        self.server.logger.quiet = False
        self.server._start_in_thread()

    def __del__(self):
        self.server.close()



