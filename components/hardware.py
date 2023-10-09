from .cpu import CPU
from .memory import Memory

from pathlib import Path


class Hardware:
    def __init__(
        self, mem_size: int, block_size: int, cpu_speed: int = None, cpu_limit=100
    ):
        self.cpu = CPU(limit=cpu_limit, speed=cpu_speed)
        self.mem = Memory(size=mem_size, block_size=block_size)

        self.disk = Path.cwd().joinpath("components").joinpath("disk")
