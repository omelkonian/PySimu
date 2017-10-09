from Events import *
from T import *
from State import State

# State
state = State()

# Events
events = Events()

# Schedule initial events
events.schedule(*(
    [   # Simulation end
        EndSim(T('00:00').shift(days=1)),
    ] +
    [   # Rate changes
        LChange(T('06:15:00').shift(minutes=15 * i), 10)
        for i in range(int((T('21:30:00').time - T('06:15:00').time).total_seconds() / 60 * 15))
    ] +
    [   # Initial CS trams
        Enqueue(T('05:40:00').shift(minutes=2 * tr), tram=tr, stop=PR_DEP)
        for tr in range(4)
    ] +
    [   # Initial PR trams
        Enqueue(T('06:00:00').shift(minutes=2 * tr), tram=tr + 4, stop=PR_DEP)
        for tr in range(4)
    ] +
    [   # Peak trams
        Enqueue(T('07:00:00').shift(minutes=2 * tr), tram=tr + 8, stop=PR_DEP)
        for tr in range(number_of_trams - 8)
    ] +
    [   # Initial passengers
        PassengerArrival(T('06:00:00').shift(seconds=gen_passenger_arrival(state)), st)
        for st in range(number_of_stops)
    ]
))
