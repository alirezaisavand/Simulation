import Simulator
import heapq
import queue


class Reception:

    def __init__(self, mu):
        self.mu = mu

        self.queue = [(0, 0)] # (length, time)

        self.waiting_customers = 0
        self.last_time = 0

        self.events = queue.Queue()

    def add_customer(self, event):
        self.throw_expired()
        self.change_capacity(1)
        heapq.heappush(self.events, event)
        if self.waiting_customers == 1:
            self.process()
        return

    def depart_customer(self):
        self.throw_expired()
        self.change_capacity(-1)
        heapq.heappop(self.events)
        self.throw_expired()
        if self.waiting_customers > 0:
            self.process()
        return

    def throw_expired(self):
        while len(self.events) > 0:
            event = self.events[0]
            if event.expired:
                heapq.heappop(self.events)
                continue
            break
        return

    def change_capacity(self, value):
        self.queue.append((self.waiting_customers, Simulator.Simulator.time - self.last_time))
        self.last_time = Simulator.Simulator.time
        self.waiting_customers += value

    def process(self):
        event = heapq.heappop(self.events)
        self.change_capacity(-1)
        # todo prepare a new event for departments
        return