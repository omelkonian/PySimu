from State import State
from Events import *

# State
state = State()

# Events
events = Events()

# Schedule initial events
events.schedule(
    EndSim(3600 * 24),
    FToggle(7 * 3600),
    FToggle(19 * 3600),
    # TODO First trams
    TramArrival(5 * 3600 + 40 * 60, 0, 0)
    # TODO passenger arrivals
)
