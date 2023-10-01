from .cpu import CPU
from .memory import Memory


class Struct:
    def __init__(self, mem_size):
        self.cpu = CPU()
        self.mem = Memory(size=mem_size)
