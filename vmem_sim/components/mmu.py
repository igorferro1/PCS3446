class MMU:
    def __init__(self, block_size):
        self.last_accesses = []
        self.block_size = block_size

    def __repr__(self) -> str:
        return "Last accesses on MMU: {}".format(self.last_accesses)

    def translate(self, v_address):
        # Considering 32 bit addresses with pages of 4kiB
        v_address = str(format(int(v_address), "032b"))
        tag = int(v_address[0:20], base=2)
        offset = int(v_address[20:32], base=2)

        return tag, offset

    def track_accesses(self, block_id):
        # casos:
        # acesso recente: só coloca no final
        # tem espaço, novo acesso: só add
        # sem espaço e novo acesso: tira o mais longe e poe o novo
        if block_id in self.last_accesses:
            self.last_accesses.remove(block_id)
            self.last_accesses.append(block_id)

        elif len(self.last_accesses) < 32 and block_id not in self.last_accesses:
            self.last_accesses.append(block_id)

        elif len(self.last_accesses) == 32 and block_id not in self.last_accesses:
            removed_block_id = self.last_accesses.pop(0)
            self.last_accesses.append(block_id)
            return removed_block_id
        return None
