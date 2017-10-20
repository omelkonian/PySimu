from abc import ABC, abstractmethod
from sortedcontainers import SortedListWithKey
from math import ceil, floor

from Constants import *
from StochasticVariables import *
from T import *


class Event(ABC):
    """Event super-class"""

    timestamp = None

    def __init__(self, timestamp):
        self.timestamp = timestamp

    def s(self, info):
        return colored('yellow', '[{0.timestamp}]\t{1}'.format(self, info))

    def __str__(self) -> str:
        return self.s("")

    @abstractmethod
    def handle(self, state, events):
        state.time = self.timestamp


class EndSim(Event):
    """End of the simulation."""

    def __init__(self, timestamp):
        super().__init__(timestamp)

    def handle(self, state, events):
        super().handle(state, events)
        state.end_simulation = True

    def __str__(self) -> str:
        return self.s("END_SIM")


class LChange(Event):
    """Change passenger arrival rate."""

    def handle(self, state, events):
        super().handle(state, events)
        state.lambdas = next_lambda()

    def __str__(self) -> str:
        return self.s("L_CHANGE")


class TramDestroy(Event):
    """Destroy a tram."""

    def __init__(self, timestamp, how_many):
        super().__init__(timestamp)
        self.how_many = how_many

    def handle(self, state, events):
        super().handle(state, events)
        state.stops[PR_DEP].to_destroy = ceil(self.how_many/2)
        state.stops[CS_DEP].to_destroy = floor(self.how_many / 2)

    def __str__(self) -> str:
        return self.s("T_DESTROY {}".format(self.how_many))


class PassengerArrival(Event):
    """Arrival of a passenger."""

    def __init__(self, timestamp, stop):
        super().__init__(timestamp)
        self.stop = stop

    def handle(self, state, events):
        super().handle(state, events)

        immediate = state.stops[self.stop].parked_tram and state.stops[self.stop].parked_tram.capacity < state.c
        # Embark parked train, if it is already there
        if immediate:
            state.stops[self.stop].parked_tram.embark(1, self.stop)
            state.statistics.update_waiting(0, self.timestamp, self.stop, state)
        # Wait at stop, otherwise
        else:
            state.stops[self.stop].arrivals.append(self.timestamp)

        # Schedule next passenger, if it is earlier than 10pm
        if self.timestamp.time < T('22:00:00').time:
            inter_time = round(gen_passenger_arrival(state, self.stop), 5)
            events.schedule(PassengerArrival(
                self.timestamp.shift(seconds=inter_time), self.stop))

    def __str__(self) -> str:
        return self.s("P_ARR\t @{1}".format(self, stop_names[self.stop]))


class Enqueue(Event):
    """Enqueue tram at entrance of stop."""

    def __init__(self, timestamp, tram, stop, nonstop=None):
        super().__init__(timestamp)
        self.tram = tram
        self.stop = stop
        self.nonstop = nonstop

    def handle(self, state, events):
        super().handle(state, events)
        state.trams[self.tram].stop = self.stop
        if end_dep(self.stop):
            assert state.trams[self.tram].capacity == 0
        if self.nonstop:
            state.trams[self.tram].nonstop = self.nonstop

        # Destroy trams at night

        if not state.stops[self.stop].parked_tram:
            events.schedule(TramArrival(self.timestamp, self.tram, self.stop))
        else:
            if end_dep(self.stop) and state.stops[self.stop].to_destroy > 0:
                state.stops[self.stop].to_destroy -= 1
                state.trams[self.tram].destroyed = True
            else:
                state.stops[self.stop].queue.append(self.tram)

    def __str__(self):
        return self.s("ENQUEUE\t Tram {0} @ {1}".format(self.tram, stop_names[self.stop]))


class TramArrival(Event):
    """Arrival of a tram."""

    def __init__(self, timestamp, tram, stop):
        super().__init__(timestamp)
        self.tram = tram
        self.stop = stop
        self.late = None
        self.po = None
        self.pin = None
        self.pout = None
        self.pinter = None

    def handle(self, state, events):
        super().handle(state, events)
        # Reset nonstop flags
        if state.trams[self.tram].nonstop and state.trams[self.tram].nonstop == self.stop:
            state.trams[self.tram].nonstop = None
        # Check nonstop flags
        if state.trams[self.tram].nonstop:
            assert state.trams[self.tram].capacity == 0
            events.schedule(TramExpectedDeparture(self.timestamp, self.tram, self.stop, 0))
            return

        state.stops[self.stop].parked_tram = state.trams[self.tram]
        p_out_percentage = 1 if end_arr(self.stop) else (0 if end_dep(self.stop) else
                                                         gen_passenger_exit_percentage(self.stop))
        self.po = p_out_percentage
        p_out = int(p_out_percentage * state.trams[self.tram].capacity)
        self.pout = p_out
        state.trams[self.tram].disembark(p_out, self.stop)
        assert (not end_arr(self.stop)) or state.trams[self.tram].capacity == 0

        p_in = min(state.c - state.trams[self.tram].capacity, state.stops[self.stop].capacity)
        self.pin = p_in
        assert (not end_arr(self.stop)) or p_in == 0

        for _ in range(p_in):
            passenger_arrived = state.stops[self.stop].arrivals.popleft().time
            now = self.timestamp.time
            waiting_time = 0 if now < passenger_arrived else (now - passenger_arrived).total_seconds()
            state.statistics.update_waiting(max(0, waiting_time), self.timestamp, self.stop, state)

        state.trams[self.tram].embark(p_in, self.stop)
        assert (not end_arr(self.stop)) or state.trams[self.tram].capacity == 0

        ld = state.stops[self.stop].last_departure
        safe = (ld is None) or (ld.shift(seconds=safety_time).time < self.timestamp.time)
        wait_for_next_tram = positive(
            0 if safe else (self.timestamp.time - ld.shift(seconds=safety_time).time).total_seconds())
        dwell_time = gen_dwell_time(state, p_in, p_out)

        delay = max(wait_for_next_tram, dwell_time)
        dep_time = self.timestamp.shift(seconds=delay)

        destroy_tram = False
        if end_dep(self.stop):
            try:
                next_schedule = state.timetable[self.stop].next_schedule()
                seconds_late = (self.timestamp.time - next_schedule.time).total_seconds()
                state.statistics.update_punctuality(state, self.stop, max(0, seconds_late))
                if seconds_late < 0:
                    dep_time = self.timestamp.shift(seconds=max(delay, -seconds_late))
                self.late = seconds_late
            except IndexError:
                destroy_tram = True

        if not destroy_tram:
            assert (not end_arr(self.stop)) or state.trams[self.tram].capacity == 0
            events.schedule(TramExpectedDeparture(dep_time, self.tram, self.stop, state.trams[self.tram].capacity))

    def __str__(self) -> str:
        return self.s("T_ARR\t\tTram {0}\t\t@{1}\t\t{2}\t{3}\t{4}\t{5}\t{6}".format(
            self.tram,
            stop_names[self.stop],
            colored('blue', '' if self.po is None else '{:.1f}%'.format(self.po * 100)),
            '' if self.pin is None or self.pin == 0 else colored('green', '+{}'.format(self.pin)),
            '' if self.pout is None or self.pout == 0 else colored('red', '-{}'.format(self.pout)),
            '' if self.pinter is None or self.pinter == 0 else colored('yellow', '(+{})'.format(self.pinter)),
            '' if self.late is None or self.late == 0 else (
                colored('green', ' -{}'.format(tt(-self.late))) if self.late < 0 else
                colored('red', ' +{}'.format(tt(self.late)))
            ),
        ))


class TramExpectedDeparture(Event):
    """Expected departure of a tram."""

    def __init__(self, timestamp, tram, stop, cap):
        super().__init__(timestamp)
        self.tram = tram
        self.stop = stop
        self.cap = cap
        self.pinter = 0

    def handle(self, state, events):
        super().handle(state, events)
        state.stops[self.stop].parked_tram = None

        # Add delay of intermediate passengers
        p_inter = state.trams[self.tram].capacity - self.cap
        self.pinter = p_inter
        dwell_inter = gen_intermediate_dwell_time(p_inter)

        # Extra delay at endstops
        dwell_switch = state.q * 60 if end_arr(self.stop) else 0
        # dwell_switch = state.use_switches(self.timestamp, self.stop) if end_stop(self.stop) else 0

        events.schedule(TramDeparture(self.timestamp.shift(seconds=dwell_inter + dwell_switch),
                                      tram=self.tram, stop=self.stop))

    def __str__(self) -> str:
        return self.s("T_E_DEP\t\tTram {0}\t\t@{1}\t{2}".format(
            self.tram, stop_names[self.stop], colored('green', '+ {}'.format(self.pinter))))


class TramDeparture(Event):
    """Departure of a tram."""

    def __init__(self, timestamp, tram, stop):
        super().__init__(timestamp)
        self.tram = tram
        self.stop = stop

    def handle(self, state, events):
        super().handle(state, events)
        state.stops[self.stop].last_departure = self.timestamp
        next_stop = (self.stop + 1) % number_of_stops
        if end_dep(next_stop):
            assert state.trams[self.tram].capacity == 0
        driving_time = 0 if end_arr(self.stop) else gen_driving_time(self.stop)
        events.schedule(
            Enqueue(self.timestamp.shift(seconds=driving_time), tram=self.tram, stop=next_stop))

        # Deque next tram
        if state.stops[self.stop].queue:
            next_tram = state.stops[self.stop].queue.popleft()
            arrival_time = max(self.timestamp.time, state.timetable[self.stop].peek_schedule().time) \
                if end_dep(self.stop) else 0
            events.schedule(TramArrival(T(time=arrival_time), next_tram, self.stop))

    def __str__(self) -> str:
        return self.s("T_DEP\t\tTram {0}\t\t@{1}".format(self.tram, stop_names[self.stop]))


class Events(object):
    """Event list, ordered in time."""

    event_list = SortedListWithKey(key=lambda e: e.timestamp.time)

    def schedule(self, *events: [Event]):
        self.event_list.update(events)

    def next(self):
        return self.event_list.pop(0)
