class Job:
    def __init__(self, name, arrival_time, memory_usage, execution_duration):
        self.name: str = name

        self.arrival_time: int = arrival_time
        self.memory_usage: int = memory_usage
        self.execution_duration: int = execution_duration

        self.execution_init_time: int = None

        self.execution_time: int = 0

        self.phase: str = "Submitted"  # Initial phase

    def transition_to_waiting_for_memory(self):
        self.phase = "Waiting for Memory"

    def transition_to_ready_for_execution(self):
        self.phase = "Ready for Execution"

    def transition_to_executing(self, current_cpu_cycle: int):
        self.execution_init_time = current_cpu_cycle
        self.execution_expected_finish = current_cpu_cycle + self.execution_duration
        self.phase = "Executing"

    def transition_to_finished(self):
        self.phase = "Finished"

    def transition_to_completed(self):
        self.phase = "Completed"


class JobMix:
    def __init__(self, job_list: list[Job]):
        self.job_list = job_list
