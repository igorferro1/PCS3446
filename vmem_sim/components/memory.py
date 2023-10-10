from mmu import MMU


class Block:
    def __init__(self, block_size: int, block_address: int):
        self.block_address = block_address
        self.block_size = block_size


class Memory:
    def __init__(self, nbr_blocks: int, memory_size: int, block_size: int):
        self.memory: list[Block] = []
        self.memory_addresses = [i for i in range(0, memory_size, block_size)]
        self.nbr_blocks: int = nbr_blocks
        self.mmu = MMU()

    def allocate(self, block: Block):
        remove_address = self.mmu.track_accesses(block.block_address)

        if remove_address:
            self.deallocate([remove_address])

        self.memory.append(block)

        return self.memory.index(block)

    def deallocate(self, block_addresses):
        for address in block_addresses:
            for block in self.memory:
                if block.block_address == address and block.valid:
                    block.valid = False
                    break


class InstructionMemory(Memory):
    def __init__(self, nbr_blocks: int):
        super().__init__(nbr_blocks)
