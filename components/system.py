from .cpu import CPU
from .memory import Memory


class Sys:
    def __init__(self, mem_size):
        cpu = CPU()
        mem = Memory(size=mem_size)
