class Event:
    def __init__(self, time):
        self.time = time
    def handle_event(self):
        pass

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