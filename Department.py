import Server
import Simulator
import numpy as np
import Event
from collections import deque

class Department():
    departments = []
    def __init__(self, MUs, max_priority):
        self.last_time = 0
        self.servers = []
        for mu in MUs:
            self.servers.append(Server.Server(mu))

        self.max_priority = max_priority
        self.queues = []
        for i in range(max_priority):
            self.queues.append(deque())

        self.customers_in_queue = 0
        self.lengths_of_queue = []

    def change_capacity(self, value):
        self.lengths_of_queue.append((self.customers_in_queue, Simulator.Simulator.time - self.last_time))
        self.customers_in_queue += value
        self.last_time = Simulator.Simulator.time


    def add_to_queue(self, customer):
        self.change_capacity(1)
        self.queues[customer.priority].append(customer)

    def get_first_customer(self):
        self.change_capacity(-1)

        for i in range(self.max_priority-1,-1, -1):
            if len(self.queues[i]) == 0:
                continue

            customer = self.queues[i].popleft()

            while len(self.queues[i]) > 0 and customer.exit_time != -1:
                customer = self.queues[i].popleft()

            if customer.exit_time == -1:
                return customer

        return None

    def get_available_severs(self):
        return [server for server in self.servers if server.available()]

    def add_to_department(self, customer):
        self.add_to_queue(customer)
        return self.process()


    def process(self):
        available_servers = self.get_available_severs()
        if len(available_servers) == 0 or self.customers_in_queue == 0:
            return None

        server = np.random.choice(available_servers)
        server.set_available(False)

        customer = self.get_first_customer()
        customer.set_server(server)

        return Event.EndService(self, server, self.time + server.get_service_time())

    def modify_avg(self):
        return

    @staticmethod
    def add_department(department):
        Department.departments.append(department)


