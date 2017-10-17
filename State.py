from Constants import *
from T import *
from Statistics import Statistics


class Tram(object):
    """Representation of a tram."""
    def __init__(self, id_, nonstop=False):
        self.id = id_
        self.capacity = 0
        self.nonstop = nonstop

    def remove_nonstop(self):
        self.nonstop = False

    def __str__(self):
        return "Tram {0.id} [{0.capacity}] {1}".format(self, "!NONSTOP" if self.nonstop else "")


class Stop(object):
    """Representation of a tram stop."""
    def __init__(self, index):
        self.name = stop_names[index]
        self.last_departure = None
        self.arrivals = deque()
        self.queue = deque()

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
        self.total = q + (17 * 60)

        # State variables
        self.end_simulation = False
        self.lambda_ = next_lambda()
        self.timetable_generator = self.gen_timetable()
        self.timetable = {}
        self.toggle_timetables()
        self.stops = [Stop(i) for i in range(number_of_stops)]
        self.trams = [Tram(i, nonstop=True) for i in range(0, 4)] + [Tram(i) for i in range(4, number_of_trams)]
        self.statistics = Statistics()

    @staticmethod
    def gen_timetable():
        while True:
            yield Timetable(T('06:00:00'), T('07:00:00'), freq=15)
            yield Timetable(T('07:00:00'), T('19:00:00'), freq=4)
            yield Timetable(T('19:00:00'), T('21:30:00'), freq=15)

    def toggle_timetables(self):
        next_timetable = next(self.timetable_generator)
        self.timetable = {
            PR_DEP: next_timetable,
            CS_DEP: next_timetable.generate_other_direction(self.total, self.f)
        }

    def __str__(self):
        ret = "============ STATE ============\nTRAMS:\n"
        for i, tr in enumerate(self.trams):
            ret += "\t{0}. {1}\n".format(i, str(tr))
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
        return ret
