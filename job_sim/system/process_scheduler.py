from ..components.cpu import CPU, CPUCore
from .process import Process
from .job import Job
from ..components.io import IOFinishException, IOStartException


class ProcessScheduler:
    def __init__(self):
        self.processes_to_run = []
        self.allocated_processes = []
        pass

    def ingress(self, cpu: CPU, job_list: list):
        for job in job_list:
            job: Job
            process = Process(job.name, job.arrival_time, job.operations, cpu.io, job)
            if process not in self.processes_to_run:
                self.processes_to_run.append(process)
                job_list.remove(job)

        self.distribute(cpu)

    def distribute(self, cpu: CPU):
        for ncore, core in cpu.cores.items():
            core: CPUCore
            if (
                not core.current_process or core.current_process.state == "blocked"
            ):  # se nao tem processo ou se esta bloqueado
                for process in self.processes_to_run:
                    process: Process
                    if (
                        process.state == "ready"
                        and process not in self.allocated_processes
                    ):
                        if core.current_process:
                            self.allocated_processes.remove(core.current_process)
                        self.allocated_processes.append(process)
                        core.current_process = process
                        core.current_process.state = "executing"
                        print(
                            f"Process from {process.name} has been allocated to core {ncore}"
                        )
                        break

    def execute(self, cpu: CPU, waiting_mfree: list):
        try:
            cpu.execute()

            for process in self.processes_to_run:
                if process not in self.allocated_processes:
                    process: Process
                    if process.state == "blocked":
                        process.wait_io()
        except IOStartException:
            self.distribute(cpu)
        except IOFinishException:
            self.distribute(cpu)

        for core in cpu.cores.values():
            core: CPUCore
            if core.current_process and not core.current_process.time_left():
                waiting_mfree.append(core.current_process.job)
                self.processes_to_run.remove(core.current_process)
                core.free()