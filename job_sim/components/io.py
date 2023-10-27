from typing import Literal

IN_TIME = 20
OUT_TIME = 25


class IOProtocol:
    def __init__(self, in_time: int, out_time: int):
        self.in_time = in_time
        self.out_time = out_time

        self.global_time: int = 0

    def io_request(self, type: Literal["in", "out"]):
        match type:
            case "in":
                return IORequest(io_protocol=self, t=self.in_time)
            case "out":
                return IORequest(io_protocol=self, t=self.in_time)

    def pass_1time(self):
        self.global_time += 1


class IORequest:
    def __init__(self, io_protocol: IOProtocol, t):
        self.arrival_time = io_protocol.global_time
        self.expected_finish_time = io_protocol.global_time + t
        self.io_protocol = io_protocol

        # self.time_left = t

    def wait_io(self):
        self.time_left()  # -= 1

    def time_left(self):
        aux = self.expected_finish_time - self.io_protocol.global_time
        if aux > 0:
            return aux
        else:
            return 0


# class IORequest_old:
#     def __init__(self, type: Literal["in", "out"]):
#         match type:
#             case "in":
#                 self.time_left = IN_TIME
#             case "out":
#                 self.time_left = OUT_TIME

#     def wait_io(self):
#         self.time_left -= 1


class IOStartException(Exception):
    pass


class IOFinishException(Exception):
    pass
