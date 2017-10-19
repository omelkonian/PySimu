from math import floor, ceil

from Constants import *
from T import *
from StochasticVariables import next_lambda
from Statistics import Statistics


class Tram(object):
    """Representation of a tram."""
    def __init__(self, id_, nonstop=None):
        self.id = id_
        self.capacity = 0
        self.nonstop = nonstop
        self.destroy = []
        self.stop = None

    def __str__(self):
        return "Tram {0.id} [{0.capacity}] {1} @{2}".format(
            self, "!NONSTOP" if self.nonstop else "", stop_names[self.stop] if self.stop else '-')


class Stop(object):
    """Representation of a tram stop."""
    def __init__(self, index):
        self.name = stop_names[index]
        self.last_departure = None
        self.arrivals = deque()
        self.queue = deque()
        self.predicted_until = None
        self.to_destroy = 0

    @property
    def capacity(self):
        return len(self.arrivals)

    def __str__(self):
        return """{0.name} [{0.capacity}] @{0.last_departure} Arr: {1} Queue: {2}""".format(
            self, ', '.join(map(str, self.arrivals)), ', '.join(map(str, self.queue)))


class State(object):
    """State of the simulation"""
    def __init__(self, q, f, c, dd, db):
        # Parameters
        self.q = q
        self.f = f
        self.c = c
        self.dd = dd
        self.db = db

        # State variables
        self.end_simulation = False
        self.lambdas = next_lambda()
        pr_tt = Timetable(starts=[T('06:00:00'), T('07:04:00'), T('19:15:00')],
                          ends=[T('07:00:00'), T('19:00:00'), T('21:30:00')],
                          freqs=[15, f, 15])
        self.timetable = {PR_DEP: pr_tt, CS_DEP: pr_tt.generate_other_direction((q + end_to_end_time) % f)}
        self.time = None
        self.statistics = Statistics()
        self.stops = [Stop(i) for i in range(number_of_stops)]
        self.initial_trams = floor(number_of_trams / floor(15/f))
        if self.initial_trams % 2 != 0:
            self.initial_trams = ceil(self.initial_trams)
        it = int(self.initial_trams/2)
        self.trams = [Tram(i, nonstop=CS_DEP) for i in range(it)] + [Tram(i) for i in range(it, number_of_trams)]

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
