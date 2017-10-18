from Constants import *
from T import T


class Statistics(object):

    def __init__(self):
        self.punctuality = {
            PR_DEP: {"schedules": 0, "delays": 0, "max": 0, "big_delays": 0},
            CS_DEP: {"schedules": 0, "delays": 0, "max": 0, "big_delays": 0},
        }
        self.waiting = {"passengers": 0, "waiting_times": 0, "max": 0}

    def update_punctuality(self, state, endstation, delay):
        self.punctuality[endstation]["schedules"] += 1
        self.punctuality[endstation]["delays"] += delay
        if delay > self.punctuality[endstation]["max"]:
            self.punctuality[endstation]["max"] = delay
        if delay > state.dd:
            self.punctuality[endstation]["big_delays"] += 1

    def update_waiting(self, waiting_time):
        self.waiting["passengers"] += 1
        self.waiting["waiting_times"] += waiting_time
        if waiting_time > self.waiting["max"]:
            self.waiting["max"] = waiting_time

    @property
    def PR_max(self):
        return self.punctuality[PR_DEP]["max"]

    @property
    def PR_avg(self):
        return self.punctuality[PR_DEP]["delays"] / self.punctuality[PR_DEP]["schedules"]

    @property
    def PR_big(self):
        return self.punctuality[PR_DEP]["big_delays"] / self.punctuality[PR_DEP]["schedules"]

    @property
    def CS_max(self):
        return self.punctuality[CS_DEP]["max"]

    @property
    def CS_avg(self):
        return self.punctuality[CS_DEP]["delays"] / self.punctuality[CS_DEP]["schedules"]

    @property
    def CS_big(self):
        return self.punctuality[CS_DEP]["big_delays"] / self.punctuality[CS_DEP]["schedules"]

    @property
    def PA_max(self):
        return self.waiting["max"]

    @property
    def PA_avg(self):
        return self.waiting["waiting_times"] / self.waiting["passengers"]

    @staticmethod
    def display_time(seconds):
        return T('00:00:00').shift(seconds=seconds).time.format('HH:mm:ss')

    def __str__(self) -> str:
        return """\033[32;1m
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
             
        ************************************
        ************************************\033[0m
        """.format(self.display_time(self.PR_avg), self.display_time(self.PR_max), self.PR_big,
                   self.display_time(self.CS_avg), self.display_time(self.CS_max), self.CS_big,
                   self.display_time(self.PA_avg), self.display_time(self.PA_max))


