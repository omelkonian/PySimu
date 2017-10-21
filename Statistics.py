from Constants import *
from T import T


def filter_time(func):
    def inner(self, *args, **kwargs):
        if self.start is None or args[0].time.time > self.start.time:
            func(self, *args, **kwargs)
    return inner


class Statistics(object):

    def __init__(self, start):
        self.start = start
        self.punctuality = {
            PR_DEP: {"count": 0, "sum": 0, "max": 0, "big": 0},
            CS_DEP: {"count": 0, "sum": 0, "max": 0, "big": 0},
        }
        self.waiting = {"count": 0, "sum": 0, "max": 0, "big": 0}
        self.stops = {"count": 0, "sum": 0}

    @filter_time
    def update_punctuality(self, state, endstation, delay):
        self.punctuality[endstation]["count"] += 1
        self.punctuality[endstation]["sum"] += delay
        if delay > self.punctuality[endstation]["max"]:
            self.punctuality[endstation]["max"] = delay
        if delay > state.dd:
            self.punctuality[endstation]["big"] += 1

    @filter_time
    def update_waiting(self, state, waiting_time):
        self.waiting["count"] += 1
        self.waiting["sum"] += waiting_time
        if waiting_time > self.waiting["max"]:
            print(state.time)
            print(self.start)
            self.waiting["max"] = waiting_time
        if waiting_time > state.wt:
            self.waiting["big"] += 1

    @filter_time
    def update_stop_capacity(self, state, current_cap):
        self.stops["count"] += 1
        self.stops["sum"] += current_cap

    @property
    def PR_max(self):
        return self.punctuality[PR_DEP]["max"]

    @property
    def PR_avg(self):
        return self.punctuality[PR_DEP]["sum"] / self.punctuality[PR_DEP]["count"]

    @property
    def PR_big(self):
        return self.punctuality[PR_DEP]["big"] / self.punctuality[PR_DEP]["count"]

    @property
    def CS_max(self):
        return self.punctuality[CS_DEP]["max"]

    @property
    def CS_avg(self):
        return self.punctuality[CS_DEP]["sum"] / self.punctuality[CS_DEP]["count"]

    @property
    def CS_big(self):
        return self.punctuality[CS_DEP]["big"] / self.punctuality[CS_DEP]["count"]

    @property
    def PA_max(self):
        return self.waiting["max"]

    @property
    def PA_avg(self):
        return self.waiting["sum"] / self.waiting["count"]

    @property
    def PA_big(self):
        return self.waiting["big"] / self.waiting["count"]

    @property
    def ST_avg(self):
        return self.stops["sum"] / self.stops["count"]

    @staticmethod
    def dt(seconds):
        return T('00:00:00').shift(seconds=seconds).time.format('HH:mm:ss')

    def __str__(self) -> str:
        return colored('green', """
        ************************************
        ************ STATISTICS ************
        ************************************
             
             ---------------------------
             ------- PUNCTUALITY -------
             ---------------------------
             
             PR: avg {0}
                 max {1}
                 big {2:.2%}
            
             CS: avg {3}
                 max {4}
                 big {5:.2%}
             
             ---------------------------
             --------- WAITING ---------
             ---------------------------
        
             AVG: {6}
             MAX: {7}
             BIG: {8:.2%}
             
             ---------------------------
             --------- STOP_CAP --------
             ---------------------------
             
             AVG: {9:.2f}
             
        ************************************
        ************************************
        """.format(self.dt(self.PR_avg), self.dt(self.PR_max), self.PR_big,
                   self.dt(self.CS_avg), self.dt(self.CS_max), self.CS_big,
                   self.dt(self.PA_avg), self.dt(self.PA_max), self.PA_big,
                   self.ST_avg))
