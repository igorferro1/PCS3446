from system.os import OperationalSystem

from components import Hardware

from system.job import JobMix, Job

from system.os import Scheduler


def main():
    print("Inicio")

    hardware = Hardware(mem_size=128_000, block_size=4_000, cpu_speed=0.1, cpu_limit=25)

    os = OperationalSystem(hardware=hardware, scheduler=Scheduler(hardware))

    init = JobMix([Job("job1", 1, 1, 10), Job("job2", 3, 1, 5), Job("job3", 3, 1, 5)])

    os.boot(init)

    os.run()


if __name__ == "__main__":
    main()
