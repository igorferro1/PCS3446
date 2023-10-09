from components import Hardware
from .job import JobMix, Job

from .scheduler import Scheduler

import os

from seedir import seedir
import questionary


class OperatingSystem:
    def __init__(self, hardware: Hardware, scheduler: Scheduler):
        self.hardware: Hardware = hardware
        self.jobmix: list[Job] = []

        self.scheduler: Scheduler = scheduler

    def print_files(self):
        seedir(self.hardware.disk)

    def ask_jobmix(self):
        files = [f.name for f in self.hardware.disk.iterdir() if f.is_file()]

        print(" ")
        jobmix_name = questionary.select(
            message="Choose jobmix file: ", choices=files
        ).ask()
        print(" ")
        jobmix_file = self.hardware.disk.joinpath(jobmix_name)
        if jobmix_file.is_file():
            self.read_jobmix(jobmix_file)
        else:
            print("Invalid file")

    def read_jobmix(self, jobmix_file):
        self.jobmix = JobMix(file=jobmix_file).job_list

    def boot(self, input_jobmix: JobMix = None):
        if input_jobmix:
            self.jobmix = input_jobmix.job_list

    def run(self):
        while not self.jobmix:
            # print("Choose jobmix from disk")
            self.print_files()
            self.ask_jobmix()

        print(" ")
        print("Running Jobs")
        for current_cpu_cycle in self.hardware.cpu:
            print(f"Cycle {current_cpu_cycle}")
            self.scheduler.job_ingress(current_cpu_cycle, self.jobmix)

            self.scheduler.job_malloc()

            self.scheduler.job_execute(current_cpu_cycle)

            self.scheduler.free_mem()
