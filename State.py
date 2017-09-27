from Constants import *


class State(object):
    """State of the simulation"""
    def __init__(self):
        self.end_simulation = False
        self.timetable_generator = self.gen_timetable()
        self.timetable = {}
        self.toggle_timetable()
        self.tram_capacity = [0] * number_of_trams
        self.stop_capacity = [0] * number_of_stops
        self.stop_last_timestamps = [None] * number_of_stops
        self.arrivals = [[]] * number_of_stops
        self.lambda_ = initial_l

    @staticmethod
    def gen_timetable():
        while True:
            yield Timetable(6, 15)
            yield Timetable(7, 4)
            yield Timetable(19, 15)

    def toggle_timetable(self):
        next_timetable = next(self.timetable_generator)
        self.timetable = {
            PR_DEP: next_timetable,
            CS_DEP: next_timetable.generate_other_direction()
        }

    def __str__(self):
        return """
        ============ STATE ============
        Timetable: {0.timetable}
        TramCapacity: {0.tram_capacity}
        StopCapacity: {0.stop_capacity}
        Arrivals: {0.arrivals}
        ===============================
        """.format(self)


class Timetable(object):

    def __init__(self, hour, freq, offset=0):
        self.hour = hour
        self.freq = freq
        self.table = [(freq * i + offset, False) for i in range(int(60 / freq))]

    def get_next_time(self):
        for i, (minute, tagged) in enumerate(self.table):
            if not tagged:
                self.table[i] = (minute, True)
                if i == len(self.table) - 1:
                    self.hour += 1
                    self.table = [(minute, False) for minute, _ in self.table]
                return self.hour * 3600 + minute * 60

    def generate_other_direction(self):
        Timetable(self.hour, self.freq, end_to_end_time % f)

    def __str__(self):
        return "{0.hour}: {0.table}".format(self)






