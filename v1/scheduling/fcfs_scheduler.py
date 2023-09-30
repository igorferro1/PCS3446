import time
import threading
from queue import Queue


class FCFSScheduler:
    def __init__(self, resource_manager):
        self.job_queue = Queue()
        self.current_time = 0
        self.resource_manager = resource_manager
        self.executing_job = None
        self.running_jobs = []
        self.lock = threading.Lock()

    def add_job(self, job, arrival_time):
        self.job_queue.put([job, arrival_time])

    def run(self):
        print("Running FCFS Scheduler")
        # beginning_time = time.time()
        # or self.executing_job is not None or self.running_jobs:
        while not self.job_queue.empty():
            if not self.job_queue.empty():  # and self.executing_job is None:
                # self.current_time = time.time()
                element = self.job_queue.get()
                job = element[0]
                arrival_time = element[1]
                # print(self.current_time)
                # print(list(self.job_queue.queue))

                if job.phase == "Submitted" and self.current_time >= arrival_time:
                    print(f"Job '{job.name}' arrived at time {arrival_time}")
                    job.transition_to_waiting_for_memory()
                    print(f"Job '{job.name}' is {job.phase}")
                elif job.phase == "Submitted":
                    self.add_job(job, arrival_time)

                if job.phase == "Waiting for Memory":
                    if self.resource_manager.allocate_memory(job.memory_usage):
                        job.transition_to_ready_for_execution()
                        print(f"Job '{job.name}' is {job.phase}")
                    else:
                        self.add_job(job, arrival_time)

                if job.phase == "Ready for Execution" and self.executing_job is None:
                    job.phase = "Executing"  # Transition to "Executing" phase
                    print(f"Job '{job.name} is executing")
                    self.executing_job = job

                    # Start the job in a new thread
                    job_thread = threading.Thread(
                        target=self.run_job, args=(job,))
                    job_thread.start()

                    self.running_jobs.append(job_thread)

                elif job.phase == "Ready for Execution" and self.executing_job is not None:
                    self.add_job(job, arrival_time)

                if self.executing_job is None:
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
