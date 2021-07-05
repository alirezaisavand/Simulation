import Simulator
import numpy as np
import Department
import Customer
import Reception


class Event:
    def __init__(self, customer, time):
        # todo we have to add an attribute to show if a customer has left the system and its event is expired
        # we can find out from customer exit time: exit_time != -1 -> expired
        # self.expired = False
        self.time = time
        self.customer = customer

    def handle_event(self):
        pass

    def __lt__(self, other):
        return self.time < other.time

    def is_expired(self):
        return self.customer.exit_time != -1


class Arrival(Event):
    def handle_event(self):
        Simulator.Simulator.number_of_customers += 1

        results = []

        if Simulator.Simulator.number_of_customers < Simulator.Simulator.max_number_of_customers:
            results.append(Event.Arrival(Customer.Customer(Simulator.Simulator.time), Simulator.Simulator.time))

        res = Reception.Reception.reception.add_customer(self.customer)
        if res is not None:
            results.append(res)

        results.append(LeaveSystem(self.customer, Simulator.Simulator.time + self.customer.patience))

        return results


class EndReception(Event):
    def handle_event(self):
        Reception.Reception.reception.set_available(True)

        department = np.random.choice(Department.Department.departments)
        self.customer.set_departmnet(department)

        results = []

        res = department.add_to_department(self.customer)
        if res is not None:
            results.append(res)

        res2 = Reception.Reception.reception.process()
        if res2 is not None:
            results.append(res2)

        return results


class EndService(Event):
    def handle_event(self):
        self.customer.exit_time = self.time
        self.customer.server.set_available(True)
        results = []
        res = self.customer.department.process()
        if res is not None:
            results.append(res)
        return results


class LeaveSystem(Event):
    def handle_event(self):
        self.customer.exit_time = self.time
        if not self.customer.started_reception:
            Reception.Reception.change_capacity(-1)
        elif self.customer.department == None:
            Reception.Reception.reception.set_available(True)
            return Reception.Reception.reception.process()
        elif self.customer.server == None:
            self.customer.department.change_capacity(-1)
        else:
            self.customer.server.set_available(True)
            return self.customer.department.process()
        return None
