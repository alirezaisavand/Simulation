import Department
import Reception
import Customer
import heapq
import Event
import Priority


class Simulator:
    time = 0
    number_of_customers = 0
    max_number_of_customers = 0
    max_priority = 0
    number_of_left_customers = 0
    system_times = {}

    def __init__(self, N, lam, alpha, mu, MUs, max_priority, max_number_of_customers):
        # definition of departures
        for i in range(max_priority + 1):
            Priority.Priority.add_priority(Priority.Priority(i))

        for i in range(N):
            Department.Department.add_department(Department.Department(MUs[i], max_priority))  # todo

        # definition of reception
        Reception.Reception.set_reception(Reception.Reception(mu))

        # set up customers
        Customer.Customer.lam = lam
        Customer.Customer.alpha = alpha

        # set constants
        Simulator.max_priority = max_priority
        Simulator.max_number_of_customers = max_number_of_customers
        # set up heap of events
        self.events = []
        heapq.heapify(self.events)

    def simulate(self):
        # todo here we have to add the start event
        # instead, firstly, we add an arrival event
        self.start_simulation()

        while len(self.events) > 0:
            event = self.get_event()

            if event.is_expired():
                continue

            self.time = event.time

            results = event.handle_event()
            for result in results:
                self.add_event(result)

        # todo demonstrate the result of this simulation

        return

    def start_simulation(self):
        customer = Customer.Customer(self.time)
        self.events.append(Event.Arrival(customer, customer.arrival_time))

    def add_event(self, event):
        heapq.heappush(self.events, event)

    def get_event(self):
        event = heapq.heappop(self.events)
        return event

    @staticmethod
    def increase_number_of_left_customers():
        Simulator.number_of_left_customers += 1

    @staticmethod
    def add_system_time(time):
        Simulator.system_times[time] += 1
