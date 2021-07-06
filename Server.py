import numpy as np


class Server:
    def __init__(self, mu):
        self.mu = mu
        self.available = True

    def set_available(self, is_available):
        self.available = is_available

    def get_service_time(self):
        return int(np.random.exponential(self.mu))