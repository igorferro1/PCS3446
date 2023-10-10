from .mmu import MMU


class Block:
    def __init__(self, block_size: int, block_id: int):
        self.block_id = block_id
        self.block_size = block_size
        self.data = []

    def __repr__(self):
        return "Block with ID {}, Size {}, Data {}".format(
            self.block_id, self.block_size, self.data
        )


class Memory:
    def __init__(self, nbr_blocks: int, memory_size: int, mmu: MMU):
        self.memory: list[Block] = []
        self.block_size = (memory_size / nbr_blocks).__ceil__()
        self.memory_addresses = [i for i in range(0, memory_size, self.block_size)]
        self.nbr_blocks: int = nbr_blocks
        self.block_size
        self.mmu = mmu

    def __repr__(self):
        return "Data {}".format(self.memory)

    def allocate(self, block: Block):
        remove_id = self.mmu.track_accesses(block.block_id)

        removed_block = None

        if remove_id:
            removed_block = self.deallocate([remove_id])

        self.memory.append(block)

        return self.memory_addresses[self.memory.index(block)], removed_block

    def deallocate(self, block_ids):
        for id in block_ids:
            for block in self.memory:
                if block.block_id == id:
                    self.memory.remove(block)
                    return block


class InstructionMemory(Memory):
    def __init__(self, nbr_blocks: int):
        super().__init__(nbr_blocks)
