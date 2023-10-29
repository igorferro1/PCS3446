from job_sim.system.os import OperatingSystem
from job_sim.components import Hardware, IOProtocol
from job_sim.system.job import JobMix, Job
from job_sim.system.scheduler import Scheduler, FCFS, SJF
from job_sim.system.process_scheduler import ProcessScheduler

from vmem_sim.components.memory import Memory, Block
from vmem_sim.components.mmu import MMU
from vmem_sim.system.memory import VirtualMemorySpace
from vmem_sim.system.memory import TLB

import questionary


def main():
    print("OS Simulator")
    print(" ")
    input("Identiifcador do teste: ")
    print(" ")

    # print(" ")
    sim = questionary.select(
        message="Choose Simulation to Run: ",
        choices=["Job Simulation", "Virtual Memory Simulation"],
    ).ask()
    print(" ")

    match sim:
        case "Job Simulation":
            hardware = Hardware(
                mem_size=300,
                block_size=5,
                cpu_speed=0.01,
                cpu_limit=200,
                cpu_cores=4,
                io=IOProtocol(in_time=20, out_time=25),
            )

            os = OperatingSystem(
                hardware=hardware, scheduler=FCFS(hardware, ProcessScheduler())
            )

            # init = JobMix(
            #     [
            #         Job("job1", 1, 6, 50),
            #         Job("job2", 1, 1, 5),
            #         Job("job3", 1, 1, 7),
            #     ],
            # )

            os.boot()

            os.run()

        case "Virtual Memory Simulation":
            mem_size = 131_072
            block_nbr = 32

            mmu = MMU((mem_size / block_nbr).__ceil__())
            memory = Memory(block_nbr, mem_size, mmu)
            tlb = TLB(8)

            choice = questionary.select(
                message="Choose script file: ",
                choices=["script1.txt", "script2.txt"],
            ).ask()
            print(" ")

            with open("vmem_sim/scripts/" + choice, "r") as f:
                addresses = f.readline().split()
                addresses = [int(x) for x in addresses]

                vm = VirtualMemorySpace(
                    memory, 64, "vmem_sim/components/memdisk", addresses, mmu, tlb
                )

                instructions = filter(None, (line.rstrip().split() for line in f))

                data_buffer = ""

                for inst in instructions:
                    match inst[0]:
                        case "read":
                            data_buffer = vm.read(inst[1])
                        case "write":
                            vm.write(inst[1], data_buffer)
                        case "print":
                            if len(inst) > 1:
                                print(vm.read(inst[1]))
                            else:
                                print(data_buffer)
                        case "dump":
                            match inst[1]:
                                case "mem":
                                    print(memory)
                                case "pt":
                                    print(vm.page_table)
                                case "tlb":
                                    print(tlb)
                        case "input":
                            data_buffer = input("Insert the input: ")

                        case _:
                            pass

                vm.finish()


if __name__ == "__main__":
    main()
