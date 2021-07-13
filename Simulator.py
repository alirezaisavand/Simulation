import Department
import Reception
import Customer
import heapq
import Event
import Priority
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import Server


class Simulator:
    time = 0
    number_of_customers = 0
    max_number_of_customers = 0
    max_priority = 0
    number_of_left_customers = 0
    system_times = {}
    unit = 100
    online_customers = [(0, 0)]
    number_of_online_customers = 0

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

            Simulator.time = event.time

            results = event.handle_event()
            for result in results:
                self.add_event(result)

        self.report_results()
        # todo demonstrate the result of this simulation

        return

    def start_simulation(self):
        customer = Customer.Customer(Simulator.time)
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
    def report_results():
        Simulator.report_system_time_results()
        Simulator.report_waiting_time_results()
        Simulator.report_left_customers()
        Simulator.report_lengths_of_queues()
        Simulator.draw_service_time_frequency()
        Simulator.draw_waiting_time_frequency()

        Simulator.draw_number_of_online_customers()
        Simulator.draw_lengths_of_queues()

    @staticmethod
    def report_lengths_of_queues():
        print("average length of main queue:")
        print(Reception.Reception.reception.modify_average_of_lengths())

        for i, department in enumerate(Department.Department.departments):
            print("average length of department " + str(i + 1) + ":")
            print(department.modify_average_of_lengths())

    @staticmethod
    def report_left_customers():
        print("number of customers who left the system:")
        print(Simulator.number_of_left_customers)

    @staticmethod
    def report_waiting_time_results():
        sum_of_all_waiting_times = 0
        for priority in Priority.Priority.priorities:
            print("average waiting time in queues for priority " + str(priority.number) + ":")
            print(Simulator.normalize_time(priority.sum_of_waiting_times / priority.number_of_customers))

            sum_of_all_waiting_times += priority.sum_of_waiting_times

        print("average waiting time in queue for all customers:")
        print(Simulator.normalize_time(sum_of_all_waiting_times / Simulator.number_of_customers))

    @staticmethod
    def report_system_time_results():
        sum_of_all_system_times = 0
        for priority in Priority.Priority.priorities:
            print("average system time for priority " + str(priority.number) + ":")
            print(Simulator.normalize_time(priority.sum_of_system_times / priority.number_of_customers))

            sum_of_all_system_times += priority.sum_of_system_times

        print("average system times for all customers:")
        print(Simulator.normalize_time(sum_of_all_system_times / Simulator.number_of_customers))

    @staticmethod
    def add_system_time(time):
        if time not in Simulator.system_times:
            Simulator.system_times[time] = 0
        Simulator.system_times[time] += 1

    @staticmethod
    def normalize_time(time):
        return time / Simulator.unit

    @staticmethod
    def draw_plot(X, Y, kind, number):
        plt.title(kind + ' time for priority = ' + number)
        plt.ylabel('frequency')
        plt.xlabel(kind + ' time (Unit)')
        plt.hist(x=X, weights=Y, bins=100, edgecolor='w')
        plt.show()

    @staticmethod
    def draw_service_time_frequency():
        for priority in Priority.Priority.priorities:
            X = np.array(list(priority.service_times.keys())) / Simulator.unit
            Y = list(priority.service_times.values())
            Simulator.draw_plot(X, Y, 'service', str(priority.number))

    @staticmethod
    def draw_waiting_time_frequency():
        for priority in Priority.Priority.priorities:
            X = np.array(list(priority.waiting_times.keys())) / Simulator.unit
            Y = list(priority.waiting_times.values())
            Simulator.draw_plot(X, Y, 'waiting', str(priority.number))

    @staticmethod
    def change_number_of_online_customers(value):
        Simulator.number_of_online_customers += value
        # only consider last value for each time
        last_time = Simulator.online_customers[-1][0]
        if last_time == Simulator.time:
            Simulator.online_customers[-1] = (Simulator.time, Simulator.number_of_online_customers)
        else:
            Simulator.online_customers.append((Simulator.time, Simulator.number_of_online_customers))

    @staticmethod
    def draw_time_plot(points, bins, title, xlabel, ylabel):
        X = [Simulator.normalize_time(time) for time, cnt in points]
        Y = [cnt for time, cnt in points]
        plt.hist(x=X, weights=Y, bins=bins, edgecolor='w')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

    @staticmethod
    def draw_number_of_online_customers():
        title = "Number of customers in system during time"
        xlabel = "time(unit)"
        ylabel = "number of customers"
        Simulator.draw_time_plot(Simulator.online_customers, 100, title, xlabel, ylabel)

    @staticmethod
    def draw_lengths_of_queues():
        xlabel = "time(unit)"
        ylabel = "length of queue"

        title = "length of main queue"
        Simulator.draw_time_plot(Reception.Reception.reception.get_lengths_points(), 100, title, xlabel, ylabel)

        for i, department in enumerate(Department.Department.departments):
            title = "length of queue in partition " + str(i + 1)
            Simulator.draw_time_plot(department.get_lengths_points(), 100, title, xlabel, ylabel)

    @staticmethod
    def reset():
        Simulator.time = 0
        Simulator.number_of_customers = 0
        Simulator.max_number_of_customers = 0
        Simulator.max_priority = 0
        Simulator.number_of_left_customers = 0
        Simulator.system_times = {}
        Simulator.unit = 100
        Simulator.online_customers = [(0, 0)]
        Simulator.number_of_online_customers = 0

        Customer.Customer.reset()
        Department.Department.reset()
        Priority.Priority.reset()
        Reception.Reception.reset()
        Server.Server.reset()

