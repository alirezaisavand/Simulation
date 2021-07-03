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
    def handle_event(self):