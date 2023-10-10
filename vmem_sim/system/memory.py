import os
from components.memory import Block, Memory
from components.mmu import MMU

# from components.mmu import MMU


class PageTableEntry:
    def __init__(self, tag, valid=False):
        self.tag = tag
        self.block_address = 0
        self.valid = valid
        self.present = False


class PageTable:
    def __init__(self, page_table_size, initial_addresses):
        self.page_table_size = page_table_size
        self.entries = [PageTableEntry(i) for i in range(page_table_size)]

        for i in range(len(initial_addresses)):
            self.entries[i].block_address = initial_addresses[i]

    def is_valid(self, tag):
        entry = self.entries[tag]
        return entry.valid

    def get_block_address(self, tag):
        entry = self.entries[tag]
        return entry.block_address

    def set_block_address(self, tag, block_address, valid):
        self.entries[tag].block_address = block_address
        self.entries[tag].valid = valid
        self.entries[tag].present = valid

    def unset_block_address(self, old_block_address, disk_block_address):
        for entry in self.entries:
            if entry.block_address == old_block_address:
                entry.block_address = disk_block_address
                entry.valid = False
                entry.present = False


class VirtualMemorySpace:
    def __init__(self, mem, page_table_size, disk_dir, initial_addresses, mmu):
        self.page_table_size: int = page_table_size
        self.disk_dir: str = disk_dir
        self.page_table: PageTable = PageTable(page_table_size, initial_addresses)
        self.mem: Memory = mem
        self.mmu = mmu

    def read(self, virtual_address):
        tag, offset = self.mmu.translate(virtual_address)
        present = self.page_table.is_valid(tag)
        block_address = self.page_table.get_block_address(tag)

        if present:
            memory_position = self.mem.memory_addresses.index(block_address)
            block: Block = self.mem.memory[memory_position]
            data = block.data[offset]
        else:
            block = self.bring_from_memory(block_address)
            data = block.data[offset]
            new_address, removed_block = self.raisePageFault(self.mem, block)

            if removed_block:
                self.page_table.unset_block_address(new_address, removed_block.block_id)

            self.page_table.set_block_address(tag, new_address, True)

            self.read(virtual_address)

        return data

    def write(self, virtual_address, value):
        tag, offset = self.mmu.translate(virtual_address)
        block_address = self.page_table.get_block_address(tag)

        for x in self.mem:
            x: Block
            if x.block_address == block_address:
                x.block[offset] = value
                break

    def bring_from_memory(self, address):
        with open(self.disk_dir + "/" + str(address) + ".txt", "r") as f:
            block_data = [line.rstrip() for line in f]
        block = Block(self.mem.block_size, address)
        block.data = block_data
        return block

    def raisePageFault(self, memory: Memory, block: Block):
        return memory.allocate(block)
