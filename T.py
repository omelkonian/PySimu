from collections import deque
from dateutil.relativedelta import relativedelta as rd
import arrow
from arrow import Arrow
from functools import partial

positive = partial(max, 0)


class T(object):

    def __init__(self, time_string='', time=None):
        self.time = time or arrow.get('2017-01-01T' + time_string)

    def copy(self):
        return T(time=Arrow(
            self.time.year, self.time.month, self.time.day, self.time.hour, self.time.minute, self.time.second))

    def shift(self, days=0, hours=0, minutes=0, seconds=0):
        return T(time=self.copy().time.shift(days=days, hours=hours, minutes=minutes, seconds=seconds))

    def __str__(self) -> str:
        return self.time.format('HH:mm:ss')


class Timetable(object):

    def __init__(self, starts, ends, freqs, offset=0):
        self.starts = starts
        self.ends = ends
        self.freqs = freqs
        self.schedules = deque([])

        for start, end, freq in zip(starts, ends, freqs):
            between = int((end.time - start.time).total_seconds() / 60 / freq)
            self.schedules.extend([start.shift(minutes=offset + (freq * i)) for i in range(between + 1)])

    def peek_schedule(self):
        return self.schedules[0]

    def next_schedule(self):
        return self.schedules.popleft()

    def generate_other_direction(self, offset):
        return Timetable(self.starts, self.ends, self.freqs, offset=offset)

    def __str__(self):
        return ', '.join(map(str, self.schedules))


def tt(secs):
    x = rd(seconds=secs)
    return ' '.join('{0:.0f} {1}'.format(
        getattr(x, k), k) for k in ['hours', 'minutes', 'seconds'] if getattr(x, k))


if __name__ == '__main__':
    from pprint import pprint
    pprint([
         (i, str(T('06:00:00').shift(minutes=15 * i)))
         for i in range(4 * 16)
     ])

