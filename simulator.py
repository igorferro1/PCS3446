from system.os import OperationalSystem

from components import Struct

from system.job import JobMix, Job


def main():
    print("Inicio")

    struct = Struct(mem_size=128_000)

    os = OperationalSystem(struct=struct)

    init = JobMix([Job("job1", 1, 1)])

    os.boot(init)

    os.run()


if __name__ == "__main__":
    main()
