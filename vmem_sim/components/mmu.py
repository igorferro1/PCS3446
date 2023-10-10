class MMU:
    def __init__(self):
        self.last_accesses = []

    def translate(self, v_address):
        # Considering 32 bit addresses
        tag = v_address[0:19]
        offset = v_address[20:31]

        return tag, offset

    def track_accesses(self, address):
        # casos:
        # acesso recente: só coloca no final
        # tem espaço, novo acesso: só add
        # sem espaço e novo acesso: tira o mais longe e poe o novo
        if address in self.last_accesses:
            self.last_accesses.remove(address)
            self.last_accesses.append(address)

        elif len(self.last_accesses) < 32 and address not in self.last_accesses:
            self.last_accesses.append(address)

        elif len(self.last_accesses) == 32 and address not in self.last_accesses:
            removed_block = self.last_accesses.pop(0)
            self.last_accesses.append(address)
            return removed_block
        return None
