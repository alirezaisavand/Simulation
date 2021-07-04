class Department():
    def __init__(self, MUs, max_priority):
        self.servers = []
        self.max_priority = max_priority
        self.queues = []
        self.customers_in_queue = 0
        self.lengths_of_queue = []

    def add_to_queue(self, customer):
        self.queues[customer.priority].append(customer)

    def change_server_status(self, server_number, status):
        self.servers[server_number].change_status(status)

    def get_first_customer(self):
        for i in range(self.max_priority-1,-1, -1):
            if len(self.queues[i]) > 0:
                return self.queues[i][0]
    def get_available_severs(self):
        return [i for i, server in enumerate(self.servers) if server.available()]

    def modify_avg(self):
        pass

