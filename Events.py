from abc import ABC, abstractmethod
from sortedcontainers import SortedListWithKey

from numpy.ma import ceil

from Constants import *
from StochasticVariables import *
from T import *


class Event(ABC):
    """Event super-class"""

    timestamp = None

    def __init__(self, timestamp):
        self.timestamp = timestamp

    def __str__(self):
        return "[{.timestamp}] ".format(self)

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
        return super().__str__() + "END_SIM"


class LChange(Event):
    """Change passenger arrival rate."""

    def handle(self, state, events):
        state.lambda_ = next_lambda()

    def __str__(self) -> str:
        return super().__str__() + "L_CHANGE"


class PassengerArrival(Event):
    """Arrival of a passenger."""

    def __init__(self, timestamp, stop):
        super().__init__(timestamp)
        self.stop = stop

    def handle(self, state, events):
        state.stops[self.stop].arrivals.append(self.timestamp)
        inter_time = self.timestamp.shift(seconds=gen_passenger_arrival(state))
        events.schedule(PassengerArrival(inter_time, self.stop))

    def __str__(self) -> str:
        return super().__str__() + "P_ARR, Stop: {0.stop}".format(self)


class Enqueue(Event):
    """Enqueue tram at entrance of stop."""

    def __init__(self, timestamp, tram, stop):
        super().__init__(timestamp)
        self.tram = tram
        self.stop = stop

    def handle(self, state, events):
        if not state.stops[self.stop].queue:
            events.schedule(TramArrival(self.timestamp, self.tram, self.stop))
        else:
            state.stops[self.stop].queue.append(self.tram)

    def __str__(self):
        return """{0}ENQUEUE
        Tram: {1.tram}
        Stop: {2}        
        """.format(super().__str__(), self, stop_names[self.stop])


class TramArrival(Event):
    """Arrival of a tram."""

    def __init__(self, timestamp, tram, stop):
        super().__init__(timestamp)
        self.tram = tram
        self.stop = stop

    def handle(self, state, events):
        if self.stop == CS_DEP:  # reset nonstop flags at CS
            state.trams[self.tram].remove_nonstop()

        if state.trams[self.tram].nonstop:
            assert state.trams[self.tram].capacity == 0
            events.schedule(TramDeparture(self.timestamp, self.tram, self.stop))
            return

        p_out = int(ceil(
            (1 if end_arr(self.stop) else gen_passenger_exit_percentage()) * state.trams[self.tram].capacity))
        state.trams[self.tram].capacity -= p_out
        p_in = min(state.c - state.stops[self.tram].capacity, state.stops[self.stop].capacity)
        for _ in range(p_in):
            passenger_enters = state.stops[self.stop].arrivals.popleft()
            state.statistics.update_waiting((self.timestamp.time - passenger_enters.time).total_seconds())

        state.trams[self.tram].capacity += p_in

        wait_for_next_tram = positive(
            0 if state.stops[self.stop].last_departure is None
            else (self.timestamp.time - state.stops[self.stop].last_departure.shift(seconds=40).time).total_seconds()
        )
        dwell_time = gen_dwell_time(state, p_in, p_out)

        delay = max(wait_for_next_tram, dwell_time)

        # TODO turnaround -- if end_arr(self.stop)

        dep_time = self.timestamp.shift(seconds=delay)
        if end_dep(self.stop):
            try:
                next_schedule = state.timetable[self.stop].next_schedule()
            except IndexError:
                state.toggle_timetables()
                next_schedule = state.timetable[self.stop].next_schedule()
            seconds_late = (self.timestamp.time - next_schedule.time).total_seconds()
            state.statistics.update_punctuality(state, self.stop, max(0, seconds_late))
            if seconds_late < 0:
                dep_time = self.timestamp.shift(seconds=max(delay, -seconds_late))

        events.schedule(TramDeparture(dep_time, self.tram, self.stop))

        # Deque next tram
        if state.stops[self.stop].queue:
            next_tram = state.stops[self.stop].queue.popleft()
            events.schedule(TramArrival(dep_time, next_tram, self.stop))

    def __str__(self) -> str:
        return """{0}T_ARR
        Tram: {1.tram}
        Stop: {2}
        """.format(super().__str__(), self, stop_names[self.stop])


class TramDeparture(Event):
    """Departure of a tram."""

    def __init__(self, timestamp, tram, stop):
        super().__init__(timestamp)
        self.tram = tram
        self.stop = stop

    def handle(self, state, events):
        next_stop = (self.stop + 1) % number_of_stops
        driving_time = state.q if end_arr(self.stop) else gen_driving_time(self.stop)
        events.schedule(
            Enqueue(self.timestamp.shift(seconds=driving_time), tram=self.tram, stop=next_stop))

    def __str__(self) -> str:
        return """{0}T_DEP
        Tram: {1.tram}
        Stop: {2}
        """.format(super().__str__(), self, stop_names[self.stop])


class Events(object):
    """Event list, ordered in time."""

    event_list = SortedListWithKey(key=lambda e: e.timestamp.time.timestamp)

    def schedule(self, *events: [Event]):
        self.event_list.update(events)

    def next(self):
        return self.event_list.pop(0)
