# class Partition:
#     def __init__(self, base, size, job=None):
#         self.job = job
#         self.base = base
#         self.size = size


class Block:
    def __init__(self, block_size):
        self.block = [None] * block_size


class Memory:
    def __init__(self, size, block_size):
        self.memory = [Block(block_size)] * (
            (size / block_size).__ceil__()
        )  # ceil or floor
