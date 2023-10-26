from ..components.io import IOProtocol, IORequest, IOFinishException, IOStartException


class Process:
    def __ini__(
        self,
        name: str,
        arrival_time: int,
        memory_usage: int,
        operations: list,
    ):
        self.name: str = name
        self.arrival_time: int = arrival_time

        self.memory_usage: int = memory_usage
        self.mem_addresses: list[int] = []

        self.state = "ready"

        self.operations = operations

        self.execution_duration: int = (
            operations.count("op") + operations.count("io") * 17
        )

        self.current_io_request: IORequest = None

    def time_left(self):
        if self.operations:
            return self.operations.count("op") + self.operations.count("io") * 17
        else:
            return 0

    def wait_io(self):
        if self.current_io_request:
            self.current_io_request.wait_io()

            if not self.current_io_request.time_left:
                print(f"Job {self.current_process}: IO Finished")
                self.current_io_request = None
                raise IOFinishException

            print(f"Process {self.current_process}: Waiting io")

    def exec_op(self):
        op: str = self.operations.pop(0)
        match op:
            case "op":
                print(f"Job {self.current_process}: Aritmetic op")
            case "ioi":
                print(f"Job {self.current_process}: IO in op")
                self.current_io_request = self.io.io_request(type="in")
                raise IOStartException
            case "ioo":
                print(f"Job {self.current_process}: IO out op")
                self.current_io_request = self.io.io_request(type="out")
                raise IOStartException
