from system.os import OperationalSystem

from components import Hardware

from system.job import JobMix, Job


def main():
    print("Inicio")

    hardware = Hardware(mem_size=128_000, cpu_speed=1, cpu_limit=10)

    os = OperationalSystem(hardware=hardware)

    init = JobMix([Job("job1", 1, 1)])

    os.boot(init)

    os.run()


if __name__ == "__main__":
    main()
