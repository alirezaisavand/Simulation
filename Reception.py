import Simulator
import heapq
import numpy as np
from collections import deque
import Event


class Reception:
    reception = None

    def __init__(self, mu):
        self.mu = mu

        self.queue = deque()
        self.lengths_of_queue = []
        self.waiting_customers = 0
        self.last_time = 0
        self.available = True
        self.customers_in_queue = 0

    def add_customer(self, customer):
        self.add_to_queue(customer)
        return self.process()

    def add_to_queue(self, customer):
        self.change_capacity(1)
        self.queue.append(customer)

    def pop_from_queue(self):
        self.change_capacity(-1)
        customer = self.queue.popleft()
        while customer.exit_time != -1:
            customer = self.queue.popleft()
        return customer

    def change_capacity(self, value):
        # warning: pay attention to zero-length intervals
        self.lengths_of_queue.append((self.customers_in_queue, Simulator.Simulator.time - self.last_time))
        self.last_time = Simulator.Simulator.time
        self.customers_in_queue += value

    def process(self):
        if (not self.available) or (self.customers_in_queue == 0):
            return None

        self.available = False

        customer = self.pop_from_queue()
        customer.set_started_reception()

        service_time = self.get_service_time()
        # variables needed for customers service times
        customer.change_sum_of_service_times(service_time)
        customer.set_end_of_current_service(Simulator.Simulator.time + service_time)

        return Event.EndReception(customer, Simulator.Simulator.time + service_time)

    def set_available(self, is_available):
        self.available = is_available

    def get_service_time(self):
        # todo correct the rates and scales of exponential random numbers
        return int(np.random.exponential(self.mu))

    def modify_average_of_lengths(self):
        sum_of_lengths = 0
        for queue_len, time_len in self.lengths_of_queue:
            sum_of_lengths += queue_len * time_len
        return sum_of_lengths / Simulator.Simulator.time

    @staticmethod
    def set_reception(reception):
        Reception.reception = reception
