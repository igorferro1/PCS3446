from time import sleep
from system.job import Job
from .io import IORequest, IOFinishException, IOStartException


class CPU:
    def __init__(self, limit: int = 100, speed: int = None):
        self.time = 0
        self.current_job: Job = None
        self.limit = limit
        self.speed = speed

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
                    self.current_io_request = IORequest(type="in")
                    raise IOStartException
                case "ioo":
                    print(f"Job {self.current_job}: IO out op")
                    self.current_io_request = IORequest(type="out")
                    raise IOStartException
