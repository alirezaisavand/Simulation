class Department():
    def __init__(self, MUs, max_priority):
        self.servers = []
        self.max_priority = max_priority
        self.queues = []
        self.customers_in_queue = 0
        self.lengths_of_queue = []

    def add(self, event):
        pass

    def depart(self):
        pass

    def modify_avg(self):
        pass