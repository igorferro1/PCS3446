class Job:
    def __init__(
        self,
        name: str,
        arrival_time: int,
        memory_usage: int,
        execution_duration: int,
        io_except: list[int] = [0, 0],
    ):
        self.name: str = name
        self.arrival_time: int = arrival_time

        self.memory_usage: int = memory_usage
        self.mem_addresses: list[int] = []

        self.execution_duration: int = execution_duration
        self.time_left: int = 0

        self.inputs = io_except[0]
        self.outputs = io_except[1]

        self.phase: str = "Submitted"  # Initial phase

    def __repr__(self):
        return self.name

    def transition_to_waiting_for_memory(self):
        self.phase = "Waiting for Memory"

    def transition_to_ready_for_execution(self):
        self.phase = "Ready for Execution"

    def transition_to_executing(self, current_cpu_cycle: int):
        for _ in range(self.inputs):
            self.execution_duration += 10

        for _ in range(self.outputs):
            self.execution_duration += 15

        self.phase = "Executing"

    def transition_to_finished(self):
        self.phase = "Finished"

    def transition_to_completed(self):
        self.phase = "Completed"


class JobMix:
    def __init__(self, job_list: list[Job]):
        self.job_list = job_list
