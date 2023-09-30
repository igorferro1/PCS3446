import time
import threading
from queue import Queue


class Job:
    def __init__(self, name, memory_usage, execution_time):
        self.name = name
        self.memory_usage = memory_usage
        self.execution_time = execution_time
        self.phase = "Submitted"  # Initial phase

    def transition_to_waiting_for_memory(self):
        self.phase = "Waiting for Memory"

    def transition_to_ready_for_execution(self):
        self.phase = "Ready for Execution"

    def transition_to_executing(self):
        self.phase = "Executing"

    def transition_to_finished(self):
        self.phase = "Finished"

    def transition_to_completed(self):
        self.phase = "Completed"

class ResourceManager:
    def __init__(self, max_memory):
        self.max_memory = max_memory
        self.available_memory = max_memory
        self.lock = threading.Lock()

    def allocate_memory(self, memory):
        with self.lock:
            if memory <= self.available_memory:
                self.available_memory -= memory
                return True
            else:
                return False

    def release_memory(self, memory):
        with self.lock:
            self.available_memory += memory


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
        while not self.job_queue.empty():# or self.executing_job is not None or self.running_jobs:
            if not self.job_queue.empty():# and self.executing_job is None:
                # self.current_time = time.time()
                element = self.job_queue.get()
                job = element[0]
                arrival_time = element[1]

                if job.phase == "Submitted": # and self.current_time >= arrival_time:
                    print(f"ENtrou '{(self.current_time)}'")
                    print(f"Job '{job.name}' arrived at time {arrival_time}")    
                    job.transition_to_waiting_for_memory()
                    print(f"Job '{job.name}' is {job.phase}")
                # elif job.phase == "Submitted":
                #     time.sleep(1)
                #     self.current_time += 1
                #     self.add_job(job, arrival_time)

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

                # Attempt to allocate memory
                # while job.phase != "Executing":
                #     if self.resource_manager.allocate_memory(job.memory_usage):
                #         job.phase = "Executing"  # Transition to "Executing" phase
                #         print(f"Job '{job.name} is executing")
                #         self.executing_job = job

                #         # Start the job in a new thread
                #         job_thread = threading.Thread(
                #             target=self.run_job, args=(job,))
                #         job_thread.start()

                #         self.running_jobs.append(job_thread)
                #     else:
                #         job.phase = "Waiting for Memory"  # Transition to "Waiting for Memory" phase
                #         print(f"Job '{job.name}' is waiting for memory")

            # if self.executing_job is not None:
            #     print(
            #         f"Job '{self.executing_job.name}' is {self.executing_job.phase}")

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


# maximum memory size
resource_manager = ResourceManager(max_memory=300)

# Create an FCFS scheduler with the resource manager
fcfs_scheduler = FCFSScheduler(resource_manager)

# Create some sample jobs
job1 = Job("Job A", 100, 5)
job2 = Job("Job B", 200, 2)
job3 = Job("Job C", 50, 3)
job4 = Job("Job D", 150, 4)


# Add jobs to the scheduler

starttime = time.time()
fcfs_scheduler.add_job(job1, 0)
# time.sleep(6)
fcfs_scheduler.add_job(job2, 6)
# time.sleep(1)
fcfs_scheduler.add_job(job3, 7)
# time.sleep(3)
fcfs_scheduler.add_job(job4, 10)
# Run the FCFS scheduler
fcfs_scheduler.run()

