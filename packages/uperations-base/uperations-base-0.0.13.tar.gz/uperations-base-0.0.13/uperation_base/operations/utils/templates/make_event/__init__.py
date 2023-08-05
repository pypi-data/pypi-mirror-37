
from vendors.uperations.operations.event import Event

class EVENTNAME(Event):

    @staticmethod
    def name():
        return "EVENTNAME"

    @staticmethod
    def description():
        return "No description provided for EVENTNAME"

    def __init__(self):
        super().__init__()
        return