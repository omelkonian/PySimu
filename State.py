import numpy as np
from math import floor, ceil

from Constants import *
from T import *
from Statistics import Statistics


class Tram(object):
    """Representation of a tram."""
    def __init__(self, id_, nonstop=None, destroyed=False):
        self.id = id_
        self.capacity = 0
        self.debug = []
        self.nonstop = nonstop
        self.destroyed = destroyed
        self.stop = None

    def embark(self, pin, st):
        self.capacity += pin
        # self.debug.append((stop_names[st], '+{}={}'.format(pin, self.capacity)))

    def disembark(self, pout, st):
        self.capacity -= pout
        # self.debug.append((stop_names[st], '-{}={}'.format(pout, self.capacity)))

    def __str__(self):
        return "{0} Tram#{1} [{2}:{3}] {4} @{5}".format(
            "xxx" if self.destroyed else "",
            self.id, self.capacity,
            '\n' + '\n'.join(list(reversed(self.debug[len(self.debug)-10:]))) + '\n',
            "!NONSTOP" if self.nonstop else "",
            stop_names[self.stop] if self.stop else '-')


class Stop(object):
    """Representation of a tram stop."""
    def __init__(self, index):
        self.id = index
        self.name = stop_names[index]
        self.last_departure = None
        self.arrivals = deque()
        self.capacity = 0
        self.queue = deque()
        self.to_destroy = 0
        self.parked_tram = None

    def enter(self, timestamp, state):
        self.arrivals.append(timestamp)
        self.capacity += 1
        state.statistics.update_stop_capacity(state, self.capacity)

    def leave(self, state):
        self.capacity -= 1
        state.statistics.update_stop_capacity(state, self.capacity)
        return self.arrivals.popleft()

    def __str__(self):
        return """{0.name} [{0.capacity}] @{0.last_departure} Arr: {1} Queue: {2}""".format(
            self, ', '.join(map(str, self.arrivals)), ', '.join(map(str, self.queue)))


class State(object):
    """State of the simulation"""
    def __init__(self, nt, q, f, db, start=None):
        # Parameters
        self.pin_lambdas = deque(np.loadtxt('matlab/pin_lambdas.csv', delimiter=',').tolist())
        self.lambdas = None
        self.next_lambda()
        self.nt = nt
        self.q = q
        self.f = f
        self.db = db

        # State variables
        self.end_simulation = False
        pr_tt = Timetable(starts=[T('06:00:00'), T('07:04:00'), T('19:15:00')],
                          ends=[T('07:00:00'), T('19:00:00'), T('21:30:00')],
                          freqs=[offpeak_f, f, offpeak_f])
        self.timetable = {PR_DEP: pr_tt, CS_DEP: pr_tt.generate_other_direction((q + end_to_end_time) % f)}
        self.time = None
        self.statistics = Statistics(start)
        self.stops = [Stop(i) for i in range(number_of_stops)]
        self.trams = [Tram(i) for i in range(self.nt)]
        self.initial_trams = int(floor(self.nt / (offpeak_f/f)))
        if self.initial_trams % 2 != 0:
            self.initial_trams = ceil(self.initial_trams)
        self.switches = {'P+R': None, 'CS': None}

    def next_lambda(self):
        self.lambdas = self.pin_lambdas.popleft()

    def use_switches(self, timestamp, st):
        est = {0: 'P+R', 8: 'CS', 9: 'CS', 17: 'P+R'}[st]
        if self.switches[est] is None:
            self.switches[est] = timestamp
            return 0
        else:
            allow = self.switches[est].shift(seconds=switch_delay)
            if timestamp.time > allow.time:
                self.switches[est] = timestamp
                return 0
            else:
                wait = (allow.time - timestamp.time).total_seconds()
                self.switches[est] = timestamp.shift(seconds=wait)
                return wait

    def __str__(self):
        ret = "============ [{}] STATE ============\nTRAMS:\n".format(self.time)
        for tr in self.trams:
            ret += "\t{0}\n".format(str(tr))
        ret += "STOPS:\n"
        for st in self.stops:
            ret += "\t{}\n".format(str(st))
        try:
            ret += "TimetablePR: {}".format(self.timetable[PR_DEP].schedules[0])
        except IndexError:
            ret += "TimetablePR -"
        try:
            ret += "\nTimetableCS: {}".format(self.timetable[CS_DEP].schedules[0])
        except IndexError:
            ret += "\nTimetableCS -"
        return colored('blue', ret)


if __name__ == '__main__':
    timetable = Timetable(starts=[T('06:00:00'), T('07:04:00'), T('19:15:00')],
                          ends=[T('07:00:00'), T('19:00:00'), T('21:30:00')],
                          freqs=[15, 4, 15])
    timetable = {
        PR_DEP: str(timetable),
        CS_DEP: str(timetable.generate_other_direction((5 + 17) % 4))
    }
    import pprint
    pprint.pprint(timetable)
