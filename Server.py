import numpy as np


class Server():
    def __init__(self, mu):
        self.mu = mu
        self.available = True

    def get_service_time(self):
        return int(np.random.exponential(self.miu))
