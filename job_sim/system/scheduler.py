from ..components import Hardware
from .job import JobMix, Job
from .process import Process
from .process_scheduler import ProcessScheduler

from ..components.io import IOStartException, IOFinishException


class Scheduler:
    def __init__(self, hardware: Hardware, p_scheduler: ProcessScheduler):
        self.hardware = hardware

        self.waiting_malloc: list[Job] = []
        self.waiting_execution: list[Job] = []

        self.executing: Job = None

        self.waiting_io: list[Process] = []

        self.waiting_mfree: list[Job] = []

        self.p_scheduler = p_scheduler

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
        # process ingress (passar CPU, a lista toda de jobs waiting execution e ai o process scheduler vai verificar os cores disponiveis e alocar os jobs prioritários encapsulando eles em um processo)
        self.p_scheduler.ingress(
            self.hardware.cpu, self.waiting_execution, self.scheduler
        )

        # process execute ( passar a CPU e chama o cpu.execute() )
        self.p_scheduler.execute(self.hardware.cpu, self.waiting_mfree)

    def free_mem(self):
        for job in self.waiting_mfree:
            self.hardware.mem.deallocate(job.mem_addresses)
            self.waiting_mfree.remove(job)
            print(f"Finished execution of job {job.name}")


class FCFS(Scheduler):
    def __init__(self, hardware: Hardware, p_scheduler: ProcessScheduler):
        super().__init__(hardware, p_scheduler)
        self.scheduler = "FCFS"

    def job_malloc(self):
        for _ in range(len(self.waiting_malloc)):
            print(f"Waiting malloc: {self.waiting_malloc}")
            job = self.waiting_malloc.pop(0)
            print(f"Malloc Job: {job}")
            job.mem_addresses = self.hardware.mem.allocate(job.memory_usage, job.name)
            self.waiting_execution.append(job)
            job.transition_to_ready_for_execution()


class SJF(Scheduler):
    def __init__(self, hardware: Hardware, p_scheduler: ProcessScheduler):
        super().__init__(hardware, p_scheduler)
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
