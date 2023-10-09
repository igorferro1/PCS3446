from typing import Literal

IN_TIME = 2
OUT_TIME = 5


class IORequest:
    def __init__(self, type: Literal["in", "out"]):
        match type:
            case "in":
                self.time_left = IN_TIME
            case "out":
                self.time_left = OUT_TIME

    def wait_io(self):
        self.time_left -= 1


class IOStartException(Exception):
    pass


class IOFinishException(Exception):
    pass
