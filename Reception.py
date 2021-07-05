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
        #warning: pay attention to zero-lengh intervals
        self.queue.append((self.customers_in_queue, Simulator.Simulator.time - self.last_time))
        self.last_time = Simulator.Simulator.time
        self.customers_in_queue += value

    def process(self):
        if (not self.available) or (self.customers_in_queue == 0):
            return None

        customer = self.pop_from_queue()
        customer.set_started_reception()

        self.available = False

        return Event.EndReception(customer, self.get_service_time() + Simulator.Simulator.time)


    def set_available(self, is_available):
        self.available = is_available

    def get_service_time(self):
        return int(np.random.exponential(self.mu))

    @staticmethod
    def set_reception(reception):
        Reception.reception = reception
