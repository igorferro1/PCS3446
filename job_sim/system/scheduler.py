from ..components import Hardware
from .job import JobMix, Job

from ..components.io import IOStartException, IOFinishException


class Scheduler:
    def __init__(self, hardware: Hardware):
        self.hardware = hardware

        self.waiting_malloc: list[Job] = []
        self.waiting_execution: list[Job] = []

        self.executing: Job = None

        self.waiting_io: list[Job] = []

        self.waiting_mfree: list[Job] = []

    def job_ingress(self, current_cpu_cycle: int, jobmix: list[Job]):
        for job in jobmix:
            if job.arrival_time == current_cpu_cycle:
                print(f"Job {job}: arrived, moved to waiting mem")
                job.transition_to_waiting_for_memory()
                self.waiting_malloc.append(job)

    def job_malloc(self):
        raise Exception(
            "Default Scheduler do not implement job_malloc, use a scheduler type to allocate jobs"
        )

    def job_execute(self, current_cpu_cycle: int):
        if self.hardware.cpu.is_available() and self.waiting_execution:
            job: Job = self.waiting_execution.pop(0)
            job.transition_to_executing(current_cpu_cycle)
            self.executing = job
            # job.time_left = job.execution_duration
            self.hardware.cpu.allocate(job)

        if self.hardware.cpu.current_job:
            try:
                self.hardware.cpu.execute()
            except IOStartException:
                self.waiting_io.append(self.executing)
            except IOFinishException:
                self.waiting_io.remove(self.executing)

            # print(f"Executing {self.hardware.cpu.current_job.name}")
            if not self.hardware.cpu.current_job.time_left():
                self.executing = None
                self.waiting_mfree.append(self.hardware.cpu.current_job)
                self.hardware.cpu.free()

    def free_mem(self):
        for job in self.waiting_mfree:
            self.hardware.mem.deallocate(job.mem_addresses)
            self.waiting_mfree.remove(job)
            print(f"Finished execution of job {job.name}")


class FCFS(Scheduler):
    def __init__(self, hardware: Hardware):
        super().__init__(hardware)

    def job_malloc(self):
        for _ in range(len(self.waiting_malloc)):
            print(f"Waiting malloc: {self.waiting_malloc}")
            job = self.waiting_malloc.pop(0)
            print(f"Malloc Job: {job}")
            job.mem_addresses = self.hardware.mem.allocate(job.memory_usage, job.name)
            self.waiting_execution.append(job)
            job.transition_to_ready_for_execution()


class SJF(Scheduler):
    def __init__(self, hardware: Hardware):
        super().__init__(hardware)
        self.scheduler = "SJF"

    def job_malloc(self):
        for _ in range(len(self.waiting_malloc)):
            print(f"Waiting malloc: {self.waiting_malloc}")
            job = self.waiting_malloc.pop(0)
            print(f"Malloc Job: {job}")
            job.mem_addresses = self.hardware.mem.allocate(job.memory_usage, job.name)
            self.waiting_execution.append(job)
            job.transition_to_ready_for_execution()

            self.waiting_execution.sort(key=lambda x: x.execution_duration)
