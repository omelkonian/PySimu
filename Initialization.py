from State import State
from Events import *

# Parameters
q = 5  # Turnaround time
f = 4  # Tram frequency
c = 420  # Tram capacity
t = 13  # Number of trams

number_of_trams = 13
number_of_stops = 18

# State
state = State(number_of_trams, number_of_stops)

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

# Stochastic variables
