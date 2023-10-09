from time import sleep
from system.job import Job


class CPU:
    def __init__(self, limit: int = 100, speed: int = None):
        self.time = 0
        self.current_job: Job = None
        self.limit = limit
        self.speed = speed

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
        op: str = self.current_job.operations.pop(0)
        match op:
            case "op":
                print("Aritmetich op")
            case "io":
                print("IO op")
