from Initialization import *

while not state.end_simulation:
    event = events.next()
    print(event)
    event.handle(state, events)
