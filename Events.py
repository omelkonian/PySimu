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
        if state.stops[self.stop].predicted_until is None \
                or state.stops[self.stop].predicted_until.time < self.timestamp.time:
            state.stops[self.stop].arrivals.append(self.timestamp)

        # Stop arrivals after 22:00
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
        if end_dep(self.stop) and \
           state.stops[self.stop].to_destroy > 0 and \
           state.timetable[self.stop].peek_schedule().time > self.timestamp.shift(minutes=10).time:
            state.stops[self.stop].to_destroy -= 1
            return

        if not state.stops[self.stop].queue:
            events.schedule(TramArrival(self.timestamp, self.tram, self.stop))
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

    def handle(self, state, events):
        super().handle(state, events)
        # Reset nonstop flags
        if state.trams[self.tram].nonstop and state.trams[self.tram].nonstop == self.stop:
            state.trams[self.tram].nonstop = None
        # Check nonstop flags
        if state.trams[self.tram].nonstop:
            assert state.trams[self.tram].capacity == 0
            events.schedule(TramDeparture(self.timestamp, self.tram, self.stop))
            return

        p_out_percentage = 1 if end_arr(self.stop) else (0 if end_dep(self.stop) else
                                                         gen_passenger_exit_percentage(self.stop))
        self.po = p_out_percentage
        p_out = int(p_out_percentage * state.trams[self.tram].capacity)
        state.trams[self.tram].capacity -= p_out
        if end_arr(self.stop):
            assert state.trams[self.tram].capacity == 0
        # print("\033[31;1m - {}\033[0m".format(p_out))

        p_in = min(state.c - state.trams[self.tram].capacity, state.stops[self.stop].capacity)
        if end_arr(self.stop):
            assert p_in == 0

        for _ in range(p_in):
            passenger_arrived = state.stops[self.stop].arrivals.popleft().time
            now = self.timestamp.time
            waiting_time = 0 if now < passenger_arrived else (now - passenger_arrived).total_seconds()
            state.statistics.update_waiting(max(0, waiting_time), self.stop, self.timestamp)

        state.trams[self.tram].capacity += p_in
        if end_arr(self.stop):
            assert state.trams[self.tram].capacity == 0

        # print("\033[32;1m + {}\033[0m".format(p_in))

        wait_for_next_tram = positive(
            0 if state.stops[self.stop].last_departure is None
            else (self.timestamp.time - state.stops[self.stop].last_departure.shift(seconds=40).time).total_seconds()
        )
        dwell_time = gen_dwell_time(state, p_in, p_out)
        delay = max(wait_for_next_tram, dwell_time)
        dep_time = self.timestamp.shift(seconds=delay)

        # Intermediate passenger
        p_in_intermediate = min(state.c - state.trams[self.tram].capacity,
                                gen_passenger_arrival(state, self.stop, total=delay))
        if end_arr(self.stop):
            assert p_in_intermediate == 0

        state.trams[self.tram].capacity += p_in_intermediate
        for _ in range(p_in_intermediate):
            state.statistics.update_waiting(0, self.stop, self.timestamp)
        # print("\033[33;1m + {}\033[0m".format(p_in_intermediate))

        state.stops[self.stop].predicted_until = dep_time

        destroy_tram = False
        if end_dep(self.stop):
            # print('{}: {}'.format(self.stop, len(state.timetable[self.stop].schedules)))
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
            if end_arr(self.stop):
                assert state.trams[self.tram].capacity == 0
            events.schedule(TramDeparture(dep_time, self.tram, self.stop))

        # Deque next tram
        if state.stops[self.stop].queue:
            next_tram = state.stops[self.stop].queue.popleft()
            events.schedule(TramArrival(dep_time, next_tram, self.stop))

        # print(state.trams[self.tram].capacity)

    def __str__(self) -> str:
        if self.late is None:
            late = ''
        elif self.late == 0:
            late = colored('green', ' - 0')
        elif self.late < 0:
            late = colored('green', ' - {}'.format(tt(-self.late)))
        elif self.late > 0:
            late = colored('red', ' + {}'.format(tt(self.late)))

        po = colored('blue', '' if self.po is None else str(round(self.po, 4)) + '%')
        return self.s("T_ARR\t\tTram {0}\t\t@{1}\t\t{2}\t\t{3}".format(self.tram, stop_names[self.stop], po, late))


class TramDeparture(Event):
    """Departure of a tram."""

    def __init__(self, timestamp, tram, stop):
        super().__init__(timestamp)
        self.tram = tram
        self.stop = stop
        self.deviation = None

    def handle(self, state, events):
        super().handle(state, events)
        next_stop = (self.stop + 1) % number_of_stops
        if end_dep(next_stop):
            assert state.trams[self.tram].capacity == 0
        driving_time = (state.q * 60) if end_arr(self.stop) else gen_driving_time(self.stop)
        try:
            self.deviation = driving_time - avg_driving_times[self.stop]
        except:
            pass
        events.schedule(
            Enqueue(self.timestamp.shift(seconds=driving_time), tram=self.tram, stop=next_stop))

    def __str__(self) -> str:
        if self.deviation is None:
            t = ''
        elif self.deviation == 0:
            t = colored('green', '- 0')
        elif self.deviation < 0:
            t = colored('green', '- {}'.format(tt(-self.deviation)))
        elif self.deviation > 0:
            t = colored('red', '+ {}'.format(tt(self.deviation)))
        return self.s("T_DEP\t\tTram {0}\t\t@{1}\t\t{2}".format(self.tram, stop_names[self.stop], t))


class Events(object):
    """Event list, ordered in time."""

    event_list = SortedListWithKey(key=lambda e: e.timestamp.time)

    def schedule(self, *events: [Event]):
        self.event_list.update(events)

    def next(self):
        return self.event_list.pop(0)
