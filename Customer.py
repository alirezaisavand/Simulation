import numpy as np
import State


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
        self.sum_of_service_times = 0
        self.end_of_current_service = -1

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

    def get_service_time(self):
        return self.sum_of_service_times

    def get_waiting_time(self):
        return self.get_system_time() - self.get_service_time()

    def change_sum_of_service_times(self, value):
        self.sum_of_service_times += value

    def set_end_of_current_service(self, time):
        self.end_of_current_service = time

    def get_state(self):
        if not self.started_reception:
            return State.State.in_reception_queue
        elif self.department is None:
            return State.State.reception
        elif self.server is None:
            return State.State.in_department_queue
        return State.State.preparing_order

    @staticmethod
    def generate_priority():
        r = np.random.rand()
        for i, p in enumerate(Customer.priority_CDF):
            if r < p:
                return i
        return -1
