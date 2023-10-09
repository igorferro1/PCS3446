from pathlib import Path


class Job:
    def __init__(
        self,
        name: str,
        arrival_time: int,
        memory_usage: int,
        operations: list,
        # execution_duration: int = None,
    ):
        self.name: str = name
        self.arrival_time: int = arrival_time

        self.memory_usage: int = memory_usage
        self.mem_addresses: list[int] = []

        self.operations = operations

        self.execution_duration: int = operations.count("op")

        self.time_left: int = 0

        self.phase: str = "Submitted"  # Initial phase

    def __repr__(self):
        return self.name

    def transition_to_waiting_for_memory(self):
        self.phase = "Waiting for Memory"

    def transition_to_ready_for_execution(self):
        self.phase = "Ready for Execution"

    def transition_to_executing(self, current_cpu_cycle: int):
        self.execution_init_time = current_cpu_cycle

        self.phase = "Executing"

    def transition_to_finished(self):
        self.phase = "Finished"

    def transition_to_completed(self):
        self.phase = "Completed"


class JobMix:
    def __init__(self, job_list: list[Job] = [], file: Path = None):
        if job_list and file:
            raise Exception("File and joblist not allowed")

        self.job_list = job_list

        if file:
            self.from_file(file)

    def from_file(self, file: Path):
        with open(file, mode="r") as f:
            lines = f.readlines()
            job_name = None
            job_arrival_time = None
            job_memory = None
            job_ops = []
            for line in lines:
                if job_name is None:
                    if line[0] == "#":
                        tokens = [t for t in line.split(" ") if t != ""]
                        job_name = tokens[-1].removesuffix("\n")
                else:
                    match line[0]:
                        case "\n":
                            if (
                                job_arrival_time is None
                                or job_memory is None
                                or job_ops is []
                            ):
                                raise ValueError("Wrong file structure")

                            self.job_list.append(
                                Job(
                                    name=job_name,
                                    arrival_time=job_arrival_time,
                                    memory_usage=job_memory,
                                    operations=job_ops,
                                )
                            )
                        case "t":
                            tokens = [t for t in line.split(" ") if t != ""]
                            job_arrival_time = int(tokens[-1].removesuffix("\n"))
                        case "m":
                            tokens = [t for t in line.split(" ") if t != ""]
                            job_memory = int(tokens[-1].removesuffix("\n"))
                        case _:
                            tokens = [t for t in line.split(" ") if t != ""]
                            job_ops.append(tokens[-1].removesuffix("\n"))

        self.job_list
