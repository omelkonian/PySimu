from Constants import *
import arrow
from arrow import Arrow


class T(object):

    def __init__(self, time_string='', time=None):
        self.time = time or arrow.get('2017-01-01T' + time_string)

    def copy(self):
        return T(time=Arrow(self.time.year, self.time.month, self.time.day, self.time.hour, self.time.second))

    def shift(self, days=0, hours=0, minutes=0, seconds=0):
        return T(time=self.copy().time.shift(days=days, hours=hours, minutes=minutes, seconds=seconds))

    def __str__(self) -> str:
        return self.time.format('HH:mm:ss')


class Timetable(object):

    def __init__(self, start, end, freq, offset=0):
        self.start = start
        self.end = end
        self.freq = freq
        minutes_between = int((end.time - start.time).total_seconds() / 60 / freq)
        self.schedules = [start.shift(minutes=offset + freq * i) for i in range(minutes_between + 1)]

    def next_schedule(self):
        return self.schedules.pop(0)

    def generate_other_direction(self):
        return Timetable(self.start, self.end, self.freq, offset=end_to_end_time % f)

    def __str__(self):
        ret = ''
        for schedule in self.schedules:
            ret += str(schedule) + "\n"
        return ret
