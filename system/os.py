from components import Struct
from .job import JobMix


class OperationalSystem:
    def __init__(self, struct: Struct):
        self.struct = struct
        self.queue = []

    def boot(self, jobmix: JobMix):
        for job in jobmix.job_list:
            self.queue.insert(0, job)

    def run(self):
        for cpu_cycle in self.struct.cpu:
            print(cpu_cycle)
