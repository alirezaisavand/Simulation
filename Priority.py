class Priority():
    priorities = []
    def __init__(self, number):
        self.number = number
        self.number_of_customers = 0
        self.sum_of_system_times = 0
        self.sum_of_waiting_times = 0
        self.service_times = {}
        self.waiting_times = {}

    def add_waiting_time(self, time):
        self.waiting_times[time] += 1
        self.sum_of_waiting_times += time


    def add_service_time(self, time):
        self.service_times[time] += 1

    def add_system_time(self, time):
        self.sum_of_system_times += time

    def add_number_of_customers(self):
        self.number_of_customers += 1

    @staticmethod
    def add_priority(priority):
        Priority.priorities.append(priority)

