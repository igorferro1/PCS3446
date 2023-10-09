# class Partition:
#     def __init__(self, base, size, job=None):
#         self.job = job
#         self.base = base
#         self.size = size


class Block:
    def __init__(self, block_size: int, block_address: int):
        self.block_address = block_address
        self.block_size = block_size
        self.block = [None] * block_size
        self.valid = False


class Memory:
    def __init__(self, size: int, block_size: int):
        self.memory = []
        for i in range((size / block_size).__ceil__()):
            self.memory.append(Block(block_size, i * block_size))

    def allocate(self, bytes: int, name: str):
        block_size = self.memory[0].block_size  # All blocks have the same size
        blocks_needed = (
            bytes + block_size - 1
        ) // block_size  # Calculate how many blocks are needed

        print(f"Blocks needed: {blocks_needed}")

        allocated_blocks = []

        for block in self.memory:
            block: Block
            if not block.valid and blocks_needed > 0:
                print(
                    f"Allocating block {self.memory.index(block)} with address {block.block_address}"
                )
                allocated_bytes = min(block.block_size, bytes)
                block.block[:allocated_bytes] = [name] * allocated_bytes
                allocated_blocks.append(block)
                block.valid = True
                bytes -= allocated_bytes
                blocks_needed -= 1

        if blocks_needed == 0:
            print("Allocation successful!")
            addresses = [i.block_address for i in allocated_blocks]
            return addresses
        else:
            for block in allocated_blocks:
                block.valid = False
            print("Insufficient memory!")

    def deallocate(self, block_addresses):
        for address in block_addresses:
            for block in self.memory:
                if block.block_address == address and block.valid:
                    block.valid = False
                    print(f"Deallocated block with address {address}")
                    break
        print("Deallocation complete!")
