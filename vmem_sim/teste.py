from components.memory import Memory, Block
from components.mmu import MMU
from system.memory import VirtualMemorySpace

mem_size = 131_072
block_nbr = 32

mmu = MMU((mem_size / block_nbr).__ceil__())
memory = Memory(block_nbr, mem_size, mmu)
vm = VirtualMemorySpace(memory, 50, "components/memdisk", [10, 15, 20, 25], mmu)

data = vm.read(0)
data = vm.read(4096)
data = vm.read(1)

print(data)
