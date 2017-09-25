from abc import ABC, abstractmethod


class Event(ABC):
    """Event super-class"""

    timestamp = 0.0

    def __init__(self, timestamp):
        self.timestamp = timestamp

    @abstractmethod
    def handle(self, state, events):
        print("NOT IMPLEMENTED! {}".format(str(self)))


class EndSim(Event):
    """End of the simulation."""

    def __init__(self, timestamp):
        super().__init__(timestamp)

    def handle(self, state, events):
        state.end_simulation = True

    def __str__(self) -> str:
        return "[{}] END_SIM".format(self.timestamp)


class FToggle(Event):
    """Toggle tram frequency."""

    def __init__(self, timestamp):
        super().__init__(timestamp)

    def handle(self, state, events):
        state.toggle_timetable()

    def __str__(self) -> str:
        return "[{}] F_TOGGLE".format(self.timestamp)


class TramArrival(Event):
    """Arrival of a tram."""

    def __init__(self, timestamp, tram, stop, nonstop=False):
        super().__init__(timestamp)
        self.tram = tram
        self.stop = stop
        self.nonstop = nonstop

    def handle(self, state, events):
        return super().handle(state, events)

    def __str__(self) -> str:
        return "[{0.timestamp}] T_ARR: Tram {0.tram}, Stop {0.stop}, Nonstop {0.nonstop}".format(self)


class TramDeparture(Event):
    """Departure of a tram."""

    def __init__(self, timestamp, tram, stop):
        super().__init__(timestamp)
        self.tram = tram
        self.stop = stop

    def handle(self, state, events):
        return super().handle(state, events)

    def __str__(self) -> str:
        return "[{0.timestamp}] T_DEP: Tram {0.tram}, Stop {0.stop}, Nonstop {0.nonstop}".format(self)


class PassengerArrival(Event):
    """Arrival of a passenger."""

    def __init__(self, timestamp, stop):
        super().__init__(timestamp)
        self.stop = stop

    def handle(self, state, events):
        return super().handle(state, events)

    def __str__(self) -> str:
        return "[{0.timestamp}] P_ARR: Stop {0.stop}".format(self)


class Events(object):
    """Event list, ordered in time."""

    event_list = []

    def schedule(self, *events):
        for event in events:
            self.event_list.append(event)
        self.event_list.sort(key=lambda e: e.timestamp)

    def next(self):
        return self.event_list.pop(0)