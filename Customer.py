import numpy as np


class Customer:
    lam = 0
    alpha = 0
    priority_CDF = [0.50, 0.70, 0.85, 0.95, 1.0]

    def __init__(self, time):
        self.patience = int(np.random.exponential(Customer.alpha))
        self.arrival_time = int(time + np.random.exponential(Customer.lam))
        self.priority = Customer.generate_priority()
        self.exit_time = -1
        self.server = None
        self.department = None
        self.started_reception = False

    def set_server(self, server):
        self.server = server

    def set_department(self, department):
        self.department = department

    def set_started_reception(self):
        self.started_reception = True

    def set_exit_time(self, time):
        self.exit_time = time

    def get_system_time(self):
        return self.exit_time - self.arrival_time

    @staticmethod
    def generate_priority():
        r = np.random.rand()
        for i, p in enumerate(Customer.priority_CDF):
            if r < p:
                return i
        return -1
