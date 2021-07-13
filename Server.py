import numpy as np
import Simulator


class Server:
    def __init__(self, mu):
        self.mu = mu
        self.available = True

    def set_available(self, is_available):
        self.available = is_available

    def get_service_time(self):
        return int(np.random.exponential(1 / self.mu) * Simulator.Simulator.unit)

    @staticmethod
    def reset():
        pass
