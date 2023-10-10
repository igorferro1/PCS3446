import os
from components.memory import Block, Memory

# from components.mmu import MMU


class PageTableEntry:
    def __init__(self, tag, valid=False):
        self.tag = tag
        self.block_address = 0
        self.valid = valid
        self.present = False


class PageTable:
    def __init__(self, page_table_size, initial_addresses):
        self.page_size = page_table_size
        self.entries = [PageTableEntry(i) for i in range(page_table_size)]

        for i in range(initial_addresses):
            self.entries[i].block_address = initial_addresses[i]

    def is_valid(self, tag):
        entry = self.entries[tag]
        return entry.valid

    def get_block_address(self, tag):
        entry = self.entries[tag]
        if not entry.valid:
            raise PageFaultError(entry, tag)
        return entry.block_address

    def set_block_address(self, tag, block_address):
        self.entries[tag].block_address = block_address
        self.entries[tag].valid = True

    def unset_block_address(self, tag):
        pass


class VirtualMemorySpace:
    def __init__(self, mem, page_size, disk_dir, initial_addresses, mmu):
        self.page_size: int = page_size
        self.disk_dir: str = disk_dir
        self.page_table: PageTable = PageTable(page_size, initial_addresses)
        self.mem: Memory = mem
        self.mmu = mmu

    def read(self, virtual_address):
        tag, offset = self.mmu.translate(virtual_address)
        block_address = self.page_table.get_block_address(tag)

        for x in self.mem:
            x: Block
            if x.block_address == block_address:
                data = x.block[offset]
                break

        else:
            self.raisePageFault(self.mem, block_address)

        return data

    def write(self, virtual_address, value):
        tag, offset = self.mmu.translate(virtual_address)
        block_address = self.page_table.get_block_address(tag)

        for x in self.mem:
            x: Block
            if x.block_address == block_address:
                x.block[offset] = value
                break

    def raisePageFault(self, memory: Memory, block: Block):
        memory.allocate(block)
