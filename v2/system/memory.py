class AddressSpace:
    def __init__(self, size, page_size):
        self.size = size
        self.page_size = page_size
        self.num_pages = size // page_size
        self.page_table = PageTable(self.num_pages)

    def get_num_pages(self):
        return self.num_pages

    def get_page_table(self):
        return self.page_table

    def get_page_size(self):
        return self.page_size

    def get_virtual_size(self):
        return self.size


class PageTableEntry:
    def __init__(self):
        self.valid_bit = False
        self.dirty_bit = False
        self.physical_frame = None

    def set_valid(self):
        self.valid_bit = True

    def set_invalid(self):
        self.valid_bit = False

    def set_dirty(self):
        self.dirty_bit = True

    def set_clean(self):
        self.dirty_bit = False

    def is_valid(self):
        return self.valid_bit

    def is_dirty(self):
        return self.dirty_bit

    def set_physical_frame(self, frame):
        self.physical_frame = frame

    def get_physical_frame(self):
        return self.physical_frame


class PageTable:
    def __init__(self, num_pages):
        self.page_table = [PageTableEntry() for _ in range(num_pages)]

    def map_page(self, virtual_page, physical_frame):
        if 0 <= virtual_page < len(self.page_table):
            self.page_table[virtual_page].set_valid()
            self.page_table[virtual_page].set_physical_frame(physical_frame)

    def unmap_page(self, virtual_page):
        if 0 <= virtual_page < len(self.page_table):
            self.page_table[virtual_page].set_invalid()

    def is_page_mapped(self, virtual_page):
        if 0 <= virtual_page < len(self.page_table):
            return self.page_table[virtual_page].is_valid()
        else:
            return False

    def get_physical_frame(self, virtual_page):
        if 0 <= virtual_page < len(self.page_table):
            return self.page_table[virtual_page].get_physical_frame()
        else:
            return None

    def set_dirty(self, virtual_page):
        if 0 <= virtual_page < len(self.page_table):
            self.page_table[virtual_page].set_dirty()

    def is_dirty(self, virtual_page):
        if 0 <= virtual_page < len(self.page_table):
            return self.page_table[virtual_page].is_dirty()
        else:
            return False
