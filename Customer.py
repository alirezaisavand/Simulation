import numpy as np

class Customer:
    lam = 0
    alpha = 0
    def __init__(self):
        pass

    def create_customer(self, time):
        tmp = np.random.exponential(1 / Customer.lam)
