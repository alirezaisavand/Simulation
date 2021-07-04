import numpy as np

class Customer:
    lam = 0
    alpha = 0
    def __init__(self, priority):
        self.priority = priority

    def create_customer(self, time):
        tmp = np.random.exponential(1 / Customer.lam)
        self.arrival_time = int(time + tmp)