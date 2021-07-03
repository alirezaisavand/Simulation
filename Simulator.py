import Department
import Reception
import Customer
import heapq


class Simulator:
    def __init__(self, N, lam, alpha, mu, MUs, max_priority):
        # definition of departures
        self.Departments = []
        for i in range(N):
            self.Departments.add(Department.Department(MUs[i], max_priority))  # todo

        # definition of reception
        self.reception = Reception.Reception(mu)

        # set up customers
        Customer.Customer.lam = lam
        Customer.Customer.alpha = alpha

        # set constants
        self.max_priority = max_priority

        # set up heap of events
        self.events = []
        heapq.heapify(self.events)

    def simulate(self):
        # todo here we have to add the start event

        while len(self.events) > 0:
            event = self.get_event()
            result = event.handle_event()
            if result is not None:
                self.add_event(result)

        # todo demonstrate the result of this simulation

        return

    def add_event(self, event):
        heapq.heappush(self.events, event)

    def get_event(self):
        event = heapq.heappop(self.events)
        return event
