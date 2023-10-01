class CPU:
    def __init__(self):
        self.time = 0
        self.job = None

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
