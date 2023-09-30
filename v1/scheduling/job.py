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
