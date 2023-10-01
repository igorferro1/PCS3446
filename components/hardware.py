from .cpu import CPU
from .memory import Memory


class Hardware:
    def __init__(self, mem_size: int, cpu_speed: int = None, cpu_limit=100):
        self.cpu = CPU(limit=cpu_limit, speed=cpu_speed)
        self.mem = Memory(size=mem_size)
