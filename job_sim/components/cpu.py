from time import sleep
from ..system.job import Job
from ..system.process import Process
from .io import IOProtocol, IORequest, IOFinishException, IOStartException


class CPUCore:
    def __ini__(self):
        self.current_process: Process = None

    def execute(self):
        if self.current_process.status != "blocked":
            self.current_process.exec_op()
        else:
            print(f"Process {self.current_process} blocked!")


class CPU:
    def __init__(self, limit: int, speed: int, io: IOProtocol):
        self.time = 0
        self.current_job: Job = None
        self.limit = limit
        self.speed = speed

        self.io = io
        self.current_io_request: IORequest = None

    def __iter__(self):
        self.cycle = 1
        return self

    def __next__(self):
        if self.speed:
            sleep(self.speed)

        x = self.cycle
        if x > self.limit:
            raise StopIteration

        self.cycle += 1
        return x

    def free(self):
        self.current_job = None

    def is_available(self):
        if self.current_job == None:
            return True
        return False

    def allocate(self, job: Job):
        if self.is_available():
            self.current_job = job
            return True
        return False

    def execute(self):
        if self.current_io_request:
            self.current_io_request.wait_io()
            if not self.current_io_request.time_left:
                print(f"Job {self.current_job}: IO Finished")
                self.current_io_request = None
                raise IOFinishException

            print(f"Job {self.current_job}: Waiting io")
        else:
            op: str = self.current_job.operations.pop(0)
            match op:
                case "op":
                    print(f"Job {self.current_job}: Aritmetic op")
                case "ioi":
                    print(f"Job {self.current_job}: IO in op")
                    self.current_io_request = self.io.io_request(type="in")
                    raise IOStartException
                case "ioo":
                    print(f"Job {self.current_job}: IO out op")
                    self.current_io_request = self.io.io_request(type="out")
                    raise IOStartException
