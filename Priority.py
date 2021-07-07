class Priority:
    priorities = []

    def __init__(self, number):
        self.number = number
        self.number_of_customers = 0
        self.sum_of_system_times = 0
        self.sum_of_waiting_times = 0
        self.service_times = {}
        self.waiting_times = {}

    def add_customer_results(self, customer):
        self.add_system_time(customer.get_system_time())
        self.add_service_time(customer.get_service_time())
        self.add_waiting_time(customer.get_waiting_time())
        self.add_number_of_customers()

    def add_waiting_time(self, time):
        if time not in self.waiting_times:
            self.waiting_times[time] = 0
        self.waiting_times[time] += 1
        self.sum_of_waiting_times += time

    def add_service_time(self, time):
        if time not in self.service_times:
            self.service_times[time] = 0
        self.service_times[time] += 1

    def add_system_time(self, time):
        self.sum_of_system_times += time

    def add_number_of_customers(self):
        self.number_of_customers += 1

    @staticmethod
    def add_priority(priority):
        Priority.priorities.append(priority)

    @staticmethod
    def get_priority_by_number(priority_number):
        return Priority.priorities[priority_number]
