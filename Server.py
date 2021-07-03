import numpy as np

class Server():
    def __init__(self, miu):
        self.miu = miu
        self.available = True
    def get_service_time(self):
        return int(np.random.exponential(self.miu))
