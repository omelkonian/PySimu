from Initialization import *

event_display_rate = 25
state_display_rate = 50

i, j = 0, 0
while not state.end_simulation:
    event = events.next()
    event.handle(state, events)
    if i % 15 == 0:
        if not isinstance(event, PassengerArrival):
            print(event)
    if j % 30 == 0:
        print(state)
    i += 1
    j += 1
