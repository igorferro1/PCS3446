from components.memory import Memory, Block
from components.mmu import MMU
from system.memory import VirtualMemorySpace
from system.memory import TLB

mem_size = 131_072
block_nbr = 32

mmu = MMU((mem_size / block_nbr).__ceil__())
memory = Memory(block_nbr, mem_size, mmu)
tlb = TLB(8)
vm = VirtualMemorySpace(memory, 64, "components/memdisk", [10, 15, 20, 25], mmu, tlb)

with open("script.txt", "r") as f:
    instructions = [line.rstrip().split() for line in f]


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
print(instructions)

vm.finish()

# print(data)
