import threading


class ResourceManager:
    def __init__(self, max_memory):
        self.max_memory = max_memory
        self.available_memory = max_memory
        self.lock = threading.Lock()

    def allocate_memory(self, memory):
        with self.lock:
            if memory <= self.available_memory:
                self.available_memory -= memory
                return True
            else:
                return False

    def release_memory(self, memory):
        with self.lock:
            self.available_memory += memory
