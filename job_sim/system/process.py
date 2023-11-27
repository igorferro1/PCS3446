from ..components.io import IOProtocol, IORequest, IOFinishException, IOStartException
from ..system.job import Job


class Process:
    def __init__(
        self, name: str, arrival_time: int, operations: list, io: IOProtocol, job: Job
    ):
        self.name: str = name
        self.arrival_time: int = arrival_time

        self.io: IOProtocol = io

        self.state = "ready"

        self.operations = operations

        # TO-DO trocar esse *17 pelo que foi determinado no IOPROTOCOL
        self.execution_duration: int = (
            operations.count("op")
            + operations.count("ioo") * self.io.out_time
            + operations.count("ioi") * self.io.in_time
        )

        self.current_io_request: IORequest = None

        self.job: Job = job

    def time_left(self):
        if self.operations:
            aux = (
                self.operations.count("op")
                + self.operations.count("ioo") * self.io.out_time
                + self.operations.count("ioi") * self.io.in_time
            )
            return aux
        elif self.current_io_request:  # and self.current_io_request.time_left():
            return self.current_io_request.time_left()
        else:
            return 0

    def wait_io(self):
        if self.current_io_request:
            self.current_io_request.wait_io()

            if not self.current_io_request.time_left():
                print(f"Process from {self.name}: IO Finished")
                self.current_io_request = None
                self.state = "ready"
                raise IOFinishException

            print(f"Process from {self.name}: Waiting io")
            with open("waitingio.txt", 'a', encoding='utf-8') as file:
                            file.write(self.name[-1])

    def exec_op(self):
        if self.state == "blocked":
            self.wait_io()

        else:
            with open("processadorexec.txt", 'a', encoding='utf-8') as file:
                file.write(self.name[-1])
            if self.operations != []:
                op: str = self.operations.pop(0)
                match op:
                    case "op":
                        print(f"Process from {self.name}: Aritmetic op")
                    case "ioi":
                        print(f"Process from {self.name}: IO in op")
                        self.current_io_request = self.io.io_request(type="in")
                        self.state = "blocked"
                        raise IOStartException
                    case "ioo":
                        print(f"Process from {self.name}: IO out op")
                        self.current_io_request = self.io.io_request(type="out")
                        self.state = "blocked"
                        raise IOStartException
