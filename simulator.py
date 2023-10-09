from system.os import OperatingSystem

from components import Hardware

from system.job import JobMix, Job

from system.scheduler import Scheduler, FCFS, SJF


def main():
    print("Inicio")

    hardware = Hardware(mem_size=200, block_size=5, cpu_speed=0.1, cpu_limit=100)

    os = OperatingSystem(hardware=hardware, scheduler=SJF(hardware))

    # init = JobMix(
    #     [
    #         Job("job1", 1, 6, 50),
    #         Job("job2", 1, 1, 5),
    #         Job("job3", 1, 1, 7),
    #     ],
    # )

    os.boot()

    os.run()


if __name__ == "__main__":
    main()
