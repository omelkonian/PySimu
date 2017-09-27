from Constants import *
from T import *


class State(object):
    """State of the simulation"""
    def __init__(self):
        self.end_simulation = False
        self.timetable_generator = self.gen_timetable()
        self.timetable = {}
        self.toggle_timetables()
        self.tram_capacity = [0] * number_of_trams
        self.stop_capacity = [0] * number_of_stops
        self.stop_last_timestamps = [None] * number_of_stops
        self.arrivals = [[]] * number_of_stops
        self.lambda_ = initial_l

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
