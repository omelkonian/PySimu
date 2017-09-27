from Events import *
from T import *
from State import State

# State
state = State()

# Events
events = Events()

# Schedule initial events
events.schedule(
    EndSim(T('00:00').shift(days=1)),
    FToggle(T('07:00:00')),
    FToggle(T('19:00:00')),
    # TODO First trams
    TramArrival(T('05:40:00'), 0, 0)
    # TODO passenger arrivals
)