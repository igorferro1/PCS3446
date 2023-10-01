class Partition:
    def __init__(self, base, size, job=None):
        self.job = job
        self.base = base
        self.size = size


class Memory:
    def __init__(self):
        self.memory = []


class PhysicalMemory:
    def __init__(self, num_blocks):
        self.num_blocks = num_blocks
        self.blocks = [None] * num_blocks  # Initialize empty memory blocks
        # Set of available free blocks
        self.free_blocks = set(range(num_blocks))

    def allocate_block(self):
        # Allocate a free block
        if not self.free_blocks:
            return None  # No free blocks available
        block = self.free_blocks.pop()
        return block

    def deallocate_block(self, block):
        # Deallocate a block and mark it as free
        if 0 <= block < self.num_blocks:
            self.free_blocks.add(block)
            self.blocks[block] = None

    def read_block(self, block):
        # Read the contents of a physical block
        if 0 <= block < self.num_blocks:
            return self.blocks[block]
        return None

    def write_block(self, block, data):
        # Write data to a physical block
        if 0 <= block < self.num_blocks:
            self.blocks[block] = data
