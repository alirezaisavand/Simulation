class Event:
    def __init__(self, time):

        # todo we have to add an attribute to show if a customer has left the system and its event is expired
        self.expired = False
        self.time = time

    def handle_event(self):
        pass

    def __lt__(self, other):
        return self.time < other.time

class Arrival(Event):
    def handle_event(self):

class Reception(Event):
    def handle_event(self):

class End_service(Event):
    def __init__(self, part, server, time):
        self.part = part
        self.server = server
        Event.__init__(self, time=time)
    def handle_event(self):