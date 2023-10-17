import os
from components.memory import Block, Memory
from components.mmu import MMU

# from components.mmu import MMU


class PageTableEntry:
    def __init__(self, tag, valid=False):
        self.tag = tag
        self.block_address = 0
        self.valid = valid
        self.dirty = False
        self.present = False

    def __repr__(self) -> str:
        return f"Tag: {self.tag}, B_add: {self.block_address}, Present: {self.present}"


class PageTable:
    def __init__(self, page_table_size, initial_addresses):
        self.page_table_size = page_table_size
        self.entries = [PageTableEntry(i) for i in range(page_table_size)]

        for i in range(len(initial_addresses)):
            self.entries[i].block_address = initial_addresses[i]

    def __repr__(self):
        return "\n".join(map(str, self.entries))

    def is_present(self, tag):
        entry = self.entries[tag]
        return entry.present

    def get_block_address(self, tag):
        entry = self.entries[tag]
        return entry.block_address

    def set_block_address(self, tag, block_address, valid):
        self.entries[tag].block_address = block_address
        self.entries[tag].valid = valid
        self.entries[tag].present = valid

    def unset_block_address(self, old_block_address, removed_block, disk_dir):
        disk_block_address = removed_block.block_id
        for entry in self.entries:
            if entry.block_address == old_block_address:
                entry.block_address = disk_block_address
                entry.valid = False
                entry.present = False
                if entry.dirty:
                    with open(
                        disk_dir + "/" + str(disk_block_address) + ".txt", "w"
                    ) as f:
                        f.write("\n".join(str(line) for line in removed_block.data))
                break

    def set_dirty(self, tag):
        self.entries[tag].dirty = True

    def unset_dirty(self, tag):
        self.entries[tag].dirty = False


class TLBEntry:
    def __init__(self, tag, valid=False):
        self.tag = tag
        self.block_address = 0
        self.valid = valid
        self.present = False
        self.dirty = False

    def __repr__(self) -> str:
        return f"Entry tag: {self.tag}, add: {self.block_address}"


class TLB:
    def __init__(self, tlb_size):
        self.tlb_size = tlb_size
        self.table = []
        self.last_accesses = []

    def __repr__(self) -> str:
        return f"Translation Lookaside Buffer table: {self.table}"

    def is_present(self, tag):
        for entry in self.table:
            if tag == entry.tag:
                return entry.present
        return False

    def get_block_address(self, tag):
        for entry in self.table:
            if tag == entry.tag and entry.valid:
                return entry.block_address
        return None

    def set_block_address(self, tag, block_address):
        for entry in self.table:
            if tag == entry.tag:
                entry.block_address = block_address

    def set_valid(self, tag, valid):
        for entry in self.table:
            if tag == entry.tag:
                entry.valid = valid

    def set_present(self, tag, present):
        for entry in self.table:
            if tag == entry.tag:
                entry.present = present

    def insert_in_tlb(self, tag, block_address):
        new_entry = TLBEntry(tag)
        removed_block_tag = None

        if tag in self.last_accesses:
            self.last_accesses.remove(tag)
            self.last_accesses.append(tag)

        elif len(self.last_accesses) < self.tlb_size and tag not in self.last_accesses:
            self.last_accesses.append(tag)
            self.table.append(new_entry)

        elif len(self.last_accesses) == self.tlb_size and tag not in self.last_accesses:
            removed_block_tag = self.last_accesses.pop(0)
            self.last_accesses.append(tag)

        if removed_block_tag:
            self.table = [
                new_entry if x.tag == removed_block_tag else x for x in self.table
            ]

        self.set_block_address(tag, block_address)
        self.set_present(tag, True)
        self.set_valid(tag, True)

    def remove_from_tlb(self, block_address):
        for entry in self.table:
            if block_address == entry.block_address:
                self.table.remove(entry)
                self.last_accesses.remove(entry.tag)
                break


class VirtualMemorySpace:
    def __init__(self, mem, page_table_size, disk_dir, initial_addresses, mmu, tlb):
        self.page_table_size: int = page_table_size
        self.disk_dir: str = disk_dir
        self.page_table: PageTable = PageTable(page_table_size, initial_addresses)
        self.mem: Memory = mem
        self.mmu: MMU = mmu
        self.tlb: TLB = tlb

    def read(self, virtual_address):
        tag, offset = self.mmu.translate(virtual_address)
        present_in_tlb = self.tlb.is_present(tag)

        if present_in_tlb:
            block_address = self.tlb.get_block_address(tag)
        else:
            present = self.page_table.is_present(tag)
            block_address = self.page_table.get_block_address(tag)

        if present_in_tlb or present:
            memory_position = self.mem.memory_addresses.index(block_address)
            block = self.mem.memory[memory_position]
            data = block.data[offset]
        else:
            block = self.bring_from_disk(block_address)
            data = block.data[offset]
            new_address, removed_block = self.raisePageFault(self.mem, block)

            if removed_block:
                self.page_table.unset_block_address(
                    new_address, removed_block, self.disk_dir
                )
                self.tlb.remove_from_tlb(new_address)

            self.page_table.set_block_address(tag, new_address, True)
            self.read(virtual_address)
            present_in_tlb = True

        if not present_in_tlb:
            self.tlb.insert_in_tlb(tag, block_address if present else new_address)

        return data

    def write(self, virtual_address, value):
        tag, offset = self.mmu.translate(virtual_address)
        present_in_tlb = self.tlb.is_present(tag)

        if present_in_tlb:
            block_address = self.tlb.get_block_address(tag)
        else:
            present = self.page_table.is_present(tag)
            block_address = self.page_table.get_block_address(tag)

        if present_in_tlb or present:
            memory_position = self.mem.memory_addresses.index(block_address)
            block: Block = self.mem.memory[memory_position]
            block.data[offset] = value
            self.page_table.set_dirty(tag)

        else:
            block = self.bring_from_disk(block_address)
            block.data[offset] = value
            new_address, removed_block = self.raisePageFault(self.mem, block)
            self.page_table.set_dirty(tag)

            if removed_block:
                self.page_table.unset_block_address(
                    new_address, removed_block, self.disk_dir
                )
                self.tlb.remove_from_tlb(new_address)

            self.page_table.set_block_address(tag, new_address, True)

            self.write(virtual_address, value)
            present_in_tlb = True
            self.tlb.set_valid(tag, True)

        if not present_in_tlb:
            self.tlb.insert_in_tlb(tag, block_address if present else new_address)

    def bring_from_disk(self, address):
        with open(self.disk_dir + "/" + str(address) + ".txt", "r") as f:
            block_data = [line.rstrip() for line in f]
        block = Block(self.mem.block_size, address)
        block.data = block_data
        return block

    def raisePageFault(self, memory: Memory, block: Block):
        return memory.allocate(block)

    def finish(self):
        for page in self.page_table.entries:
            page: PageTableEntry
            if page.present:
                self.tlb.remove_from_tlb(page.block_address)
                self.page_table.unset_block_address(
                    page.block_address,
                    self.mem.memory[
                        self.mem.memory_addresses.index(page.block_address)
                    ],
                    self.disk_dir,
                )
