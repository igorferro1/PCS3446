class CPU:
    def __init__(self, limit: int = 100):
        self.time = 0
        self.job = None
        self.limit = limit

    def __iter__(self):
        self.cycle = 1
        return self

    def __next__(self):
        x = self.cycle

        if x == self.limit:
            raise Exception("Fim da execução")

        self.cycle += 1
        return x

    def free(self):
        self.job = None

    def is_available(self):
        if self.current_job == None:
            return True
        return False

    def allocate(self, job):
        if self.is_available():
            self.current_job = job
            return True
        return False
