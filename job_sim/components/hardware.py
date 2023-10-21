from .cpu import CPU
from .memory import Memory

from .io import IOProtocol

from pathlib import Path


class Hardware:
    def __init__(
        self,
        mem_size: int,
        block_size: int,
        cpu_speed: int,
        cpu_limit: int,
        io: IOProtocol,
    ):
        self.cpu = CPU(
            limit=cpu_limit,
            speed=cpu_speed,
            io=io,
        )
        self.mem = Memory(size=mem_size, block_size=block_size)

        self.disk = (
            Path.cwd().joinpath("job_sim").joinpath("components").joinpath("disk")
        )
