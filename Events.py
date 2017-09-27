from abc import ABC, abstractmethod
from Constants import *
from StochasticVariables import *


class Event(ABC):
    """Event super-class"""

    timestamp = None

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
        state.toggle_timetables()

    def __str__(self) -> str:
        return "[{}] F_TOGGLE".format(self.timestamp)


class LChange(Event):
    """Change passenger arrival rate."""

    def __init__(self, timestamp, new_l):
        super().__init__(timestamp)
        self.new_l = new_l

    def handle(self, state, events):
        state.lambda_ = self.new_l

    def __str__(self) -> str:
        return "[{}] L_CHANGE".format(self.timestamp)


class TramArrival(Event):
    """Arrival of a tram."""

    def __init__(self, timestamp, tram, stop, nonstop=False):
        super().__init__(timestamp)
        self.tram = tram
        self.stop = stop
        self.nonstop = nonstop

    def handle(self, state, events):
        end_dep = self.stop in [PR_DEP, CS_DEP]
        end_arr = self.stop in [PR_ARR, CS_ARR]

        p_out = 100 if end_arr else np.random.uniform(0, 100)  # TODO percentage
        p_in = state.stop_capacity[self.stop + 1 if end_arr else self.stop]
        next_stop = self.stop + 1 if end_arr else self.stop

        state.tram_capacity[self.tram] -= p_out

        # last_tram = state.stop_last_timestamps[next_stop]
        wait_for_next_tram = 0  # TODO fast/slow speeds
        extra_time = q if end_arr else gen_dwell_time(p_in, p_out)
        minutes_late = (state.timetable[self.stop].next_schedule().time - self.timestamp.time).total_seconds()
        time_until_scheduled = max(0, minutes_late) if end_dep else 0

        events.schedule(
            TramDeparture(
                self.timestamp.shift(seconds=max(max(extra_time, wait_for_next_tram), time_until_scheduled)),
                self.tram,
                next_stop
            )
        )
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
        return "[{0.timestamp}] T_DEP: Tram {0.tram}, Stop {0.stop}".format(self)


class PassengerArrival(Event):
    """Arrival of a passenger."""

    def __init__(self, timestamp, stop):
        super().__init__(timestamp)
        self.stop = stop

    def handle(self, state, events):
        state.stop_capacity[self.stop] += 1
        inter_time = gen_passenger_arrival(state)
        events.schedule(PassengerArrival(inter_time, self.stop))
        return super().handle(state, events)

    def __str__(self) -> str:
        return "[{0.timestamp}] P_ARR: Stop {0.stop}".format(self)


class Events(object):
    """Event list, ordered in time."""

    event_list = []

    def schedule(self, *events):
        for event in events:
            self.event_list.append(event)
        self.event_list.sort(key=lambda e: e.timestamp.time.timestamp)

    def next(self):
        return self.event_list.pop(0)
