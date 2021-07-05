import Department
import Reception
import Customer
import heapq
import Event

class Simulator:
    time = 0
    number_of_customers = 0
    max_number_of_customers = 0
    max_priority = 0
    def __init__(self, N, lam, alpha, mu, MUs, max_priority, max_number_of_customers):
        # definition of departures
        for i in range(N):
            Department.Department.add_department(Department(MUs[i], max_priority)) # todo

        # definition of reception
        Reception.set_reception(Reception.Reception(mu))

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
            results = event.handle_event()
            for result in results:
                self.add_event(result)

        # todo demonstrate the result of this simulation

        return

    def start_simulation(self):
        self.events.append(Event.Arrival(Customer.Customer(self.time), self.time))

    def add_event(self, event):
        heapq.heappush(self.events, event)

    def get_event(self):
        event = heapq.heappop(self.events)
        return event
