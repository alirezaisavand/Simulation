import Simulator
import numpy as np
import Department
import Customer
import Reception
import Priority


class Event:
    def __init__(self, customer, time):
        # todo we have to add an attribute to show if a customer has left the system and its event is expired
        # we can find out from customer exit time: exit_time != -1 -> expired
        self.customer = customer
        self.time = time

    def handle_event(self):
        pass

    def __lt__(self, other):
        return self.time < other.time

    def is_expired(self):
        return self.customer.exit_time != -1


class Arrival(Event):
    def handle_event(self):
        self.update_simulation_variables()

        return self.get_results()

    def update_simulation_variables(self):
        # todo waiting times still remain
        Simulator.Simulator.number_of_customers += 1

    def get_results(self):
        results = []

        if Simulator.Simulator.number_of_customers < Simulator.Simulator.max_number_of_customers:
            customer = Customer.Customer(Simulator.Simulator.time)
            results.append(Arrival(customer, customer.arrival_time))

        res = Reception.Reception.reception.add_customer(self.customer)
        if res is not None:
            results.append(res)

        results.append(LeaveSystem(self.customer, Simulator.Simulator.time + self.customer.patience))

        return results


class EndReception(Event):
    def handle_event(self):
        Reception.Reception.reception.set_available(True)

        department = np.random.choice(Department.Department.departments)
        self.customer.set_department(department)

        return self.get_results()

    def get_results(self):
        results = []

        res = self.customer.add_to_department(self.customer)
        if res is not None:
            results.append(res)

        res2 = Reception.Reception.reception.process()
        if res2 is not None:
            results.append(res2)

        return results

    def update_simulation_variables(self):
        pass


class EndService(Event):
    def handle_event(self):
        self.customer.set_exit_time(self.time)
        self.customer.server.set_available(True)

        return self.get_results()

    def get_results(self):
        results = []
        res = self.customer.department.process()
        if res is not None:
            results.append(res)
        return results

    def update_simulation_variables(self):
        Priority.Priority.get_priority_by_number(self.customer.priority).add_system_time(
            self.customer.get_system_time())
        Priority.Priority.get_priority_by_number(self.customer.priority).add_number_of_customers()
        Simulator.Simulator.add_system_time(self.customer.get_system_time())


class LeaveSystem(Event):
    def handle_event(self):
        self.customer.set_exit_time(self.time)

        # updating simulations variables
        self.update_simulation_variables()

        # return results of event
        return self.get_results()

    def update_simulation_variables(self):
        Simulator.Simulator.increase_number_of_left_customers()
        Priority.Priority.get_priority_by_number(self.customer.priority).add_system_time(
            self.customer.get_system_time())
        Priority.Priority.get_priority_by_number(self.customer.priority).add_number_of_customers()
        Simulator.Simulator.add_system_time(self.customer.get_system_time())

    def get_results(self):
        results = []
        if not self.customer.started_reception:
            Reception.Reception.reception.change_capacity(-1)
        elif self.customer.department is None:
            Reception.Reception.reception.set_available(True)
            res = Reception.Reception.reception.process()
            if res is not None:
                results.append(res)
        elif self.customer.server is None:
            self.customer.department.change_capacity(-1)
        else:
            self.customer.server.set_available(True)
            res2 = self.customer.department.process()
            if res2 is not None:
                results.append(res2)
        return results
