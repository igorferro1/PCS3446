import time
from job import Job
from resource_manager import ResourceManager
from fcfs_scheduler import FCFSScheduler
from sjf_np_scheduler import SJFScheduler

# maximum memory size
resource_manager = ResourceManager(max_memory=300)

# Create an FCFS scheduler with the resource manager
fcfs_scheduler = FCFSScheduler(resource_manager)
sjf_scheduler = SJFScheduler(resource_manager)

# Create some sample jobs
job1 = Job("Job A", 100, 5)
job2 = Job("Job B", 200, 2)
job3 = Job("Job C", 50, 3)
job4 = Job("Job D", 150, 4)

# Add jobs to the scheduler

starttime = time.time()
fcfs_scheduler.add_job(job1, 0)
# time.sleep(6)
fcfs_scheduler.add_job(job2, 7)
# time.sleep(1)
fcfs_scheduler.add_job(job3, 15)
# time.sleep(3)
fcfs_scheduler.add_job(job4, 20)

sjf_scheduler.add_job(job1, 0)
# time.sleep(6)
sjf_scheduler.add_job(job2, 0)
# time.sleep(1)
sjf_scheduler.add_job(job3, 15)
# time.sleep(3)
sjf_scheduler.add_job(job4, 20)

# Run the FCFS scheduler
sjf_scheduler.run()
