from typing import Literal

IN_TIME = 2
OUT_TIME = 5


class IOProtocol:
    def __init__(self, in_time: int, out_time: int):
        self.in_time = in_time
        self.out_time = out_time

    def io_request(self, type: Literal["in", "out"]):
        match type:
            case "in":
                return IORequest(t=self.in_time)
            case "out":
                return IORequest(t=self.in_time)


class IORequest:
    def __init__(self, t):
        self.time_left = t

    def wait_io(self):
        self.time_left -= 1


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
