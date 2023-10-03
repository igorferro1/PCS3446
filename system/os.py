from components import Hardware
from .job import JobMix, Job


class Scheduler:
    def __init__(self, hardware: Hardware):
        self.hardware = hardware

        self.waiting_malloc: list[Job] = []
        self.waiting_execution: list[Job] = []

        self.executing: Job = None

        self.waiting_mfree: list[Job] = []

    def job_ingress(self, current_cpu_cycle: int, jobmix: list[Job]):
        for job in jobmix:
            if job.arrival_time == current_cpu_cycle:
                job.transition_to_waiting_for_memory()
                self.waiting_malloc.append(job)

    def job_malloc(self):
        for job in self.waiting_malloc:
            # TO-DO IMPLEMENTAR MALLOC
            self.waiting_malloc.remove(job)
            self.waiting_execution.append(job)
            job.transition_to_ready_for_execution()

    def job_execute(self, current_cpu_cycle: int):
        if self.hardware.cpu.is_available() and self.waiting_execution:
            job: Job = self.waiting_execution.pop(0)
            job.transition_to_executing(current_cpu_cycle)
            self.executing = job
            self.hardware.cpu.allocate(job)
        if self.hardware.cpu.current_job:
            self.hardware.cpu.current_job.execution_time += 1
            print(f"Executing {self.hardware.cpu.current_job.name}")
            if (
                self.hardware.cpu.current_job.execution_time
                == self.hardware.cpu.current_job.execution_duration
            ):
                self.executing = None
                self.waiting_mfree.append(self.hardware.cpu.current_job)
                self.hardware.cpu.free()

    def free_mem(self):
        for job in self.waiting_mfree:
            self.waiting_mfree.remove(job)
            # frees memory that it's using


class FCFS(Scheduler):
    def __init__(self, hardware: Hardware):
        super().__init__(hardware)


class OperationalSystem:
    def __init__(self, hardware: Hardware, scheduler: Scheduler):
        self.hardware: Hardware = hardware
        self.jobmix: list[Job] = []

        self.scheduler: Scheduler = scheduler

    def boot(self, input_jobmix: JobMix):
        self.jobmix = input_jobmix.job_list

    def run(self):
        for current_cpu_cycle in self.hardware.cpu:
            print("Ciclo {}".format(current_cpu_cycle))
            self.scheduler.job_ingress(current_cpu_cycle, self.jobmix)

            self.scheduler.job_malloc()

            self.scheduler.job_execute(current_cpu_cycle)

            self.scheduler.free_mem()
