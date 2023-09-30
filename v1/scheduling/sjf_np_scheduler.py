import time
import threading
from queue import Queue


class SJFScheduler:
    def __init__(self, resource_manager):
        self.job_queue = Queue()
        self.current_time = 0
        self.resource_manager = resource_manager
        self.executing_job = None
        self.ready_jobs = []
        self.running_jobs = []
        self.lock = threading.Lock()

    def add_job(self, job, arrival_time):
        self.job_queue.put([job, arrival_time])

    def run(self):
        print("Running SJF Scheduler")
        while not self.job_queue.empty() or self.executing_job is not None or self.running_jobs:
            if not self.job_queue.empty():
                element = self.job_queue.get()
                job = element[0]
                arrival_time = element[1]

                if job.phase == "Submitted" and self.current_time >= arrival_time:
                    print(f"Job '{job.name}' arrived at time {arrival_time}")
                    job.transition_to_waiting_for_memory()
                    print(f"Job '{job.name}' is {job.phase}")
                elif job.phase == "Submitted":
                    self.add_job(job, arrival_time)

                if job.phase == "Waiting for Memory":
                    if self.resource_manager.allocate_memory(job.memory_usage):
                        job.transition_to_ready_for_execution()
                        self.ready_jobs.append(job)
                        print(f"Job '{job.name}' is {job.phase}")
                    else:
                        self.add_job(job, arrival_time)

            if self.ready_jobs and arrival_time > self.current_time and self.executing_job is None:
                self.ready_jobs.sort(key=lambda x: x.execution_time)

                next_job = self.ready_jobs[0]
                self.ready_jobs.remove(next_job)
                next_job.phase = "Executing"
                print(f"Job '{next_job.name}' is executing")
                self.executing_job = next_job

                job_thread = threading.Thread(
                    target=self.run_job, args=(next_job,))
                job_thread.start()
                self.running_jobs.append(job_thread)

            if self.executing_job is None and arrival_time > self.current_time:
                time.sleep(1)  # Simulate execution time
                self.current_time += 1

            with self.lock:
                self.running_jobs = [
                    job for job in self.running_jobs if job.is_alive()]

            if not self.running_jobs:
                self.executing_job = None

    def run_job(self, job):
        job_thread = threading.current_thread()
        while job.execution_time > 0:
            time.sleep(1)  # Simulate execution time
            self.current_time += 1
            job.execution_time -= 1

        # Job has finished execution
        self.resource_manager.release_memory(job.memory_usage)
        job.phase = "Completed"
        print(f"Job '{job.name}' finished execution at time {self.current_time}")
