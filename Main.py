import click

from State import State
from Events import *
from T import T


def initial_events(state):
    it = int(state.initial_trams/2)
    return [
        # Simulation end
        EndSim(T('23:00:00')),
    ] + [
        # Rate changes
        LChange(T('06:15:00').shift(minutes=15 * i))
        for i in range(4 * 15)
    ] + [
        # Initial CS trams
        Enqueue(T('05:40:00').shift(minutes=15 * tr), tram=tr, stop=PR_DEP)
        for tr in range(it)
    ] + [
        # Initial PR trams
        Enqueue(T('06:00:00').shift(minutes=15 * tr), tram=tr + it, stop=PR_DEP)
        for tr in range(it)
    ] + [
        # Peak trams
        Enqueue(T('07:00:00').shift(minutes=-(state.q + end_to_end_time) if tr % 2 else 0),
                tram=tr + state.initial_trams, stop=PR_DEP, nonstop=(CS_DEP if tr % 2 else None))
        for tr in range(number_of_trams - (2 * it))
    ] + [
        # Tram destruction
        TramDestroy(T('18:50:00'), number_of_trams - state.initial_trams)
    ] + [
        # Initial passengers
        PassengerArrival(T('06:00:00'), st)
        for st in range(number_of_stops)
        if not end_arr(st)
    ]


@click.command()
@click.option('-edr', default=1, help='Event display rate.')
@click.option('-sdr', default=None, help='State display rate.')
@click.option('-q', default=5, help='Turnaround time.')
@click.option('-f', default=4, help='Tram frequency.')
@click.option('-c', default=420, help='Tram capacity.')
@click.option('-dd', default=60, help='Big departure delay.')
@click.option('-db', default=.05, help='Door block percentage.')
@click.option('--track_tram', '-tt', default=None, help="Track specific tram's events.")
@click.option('--track_stop', '-ts', default=None, help="Track specific stop's events.")
@click.option('--only_passengers', '-p', type=bool, default=False, help="Display only passengers' events.")
@click.option('--start', '-s', default=None, help="Start simulation later.")
@click.option('--end', '-e', default=None, help="End simulation earlier.")
@click.option('--show_all', '-A', default=None, help="Show all events.")
@click.option('--etype', '-t', default=None, help="Filter on event type.")
def run(edr, sdr, q, f, c, dd, db, track_tram, track_stop, only_passengers, start, end, show_all, etype):
    """Run simulation with given parameters (in seconds). """
    state = State(q, f, c, dd, db)
    events = Events()
    events.schedule(*initial_events(state))

    if end:
        events.schedule(EndSim(T(end)))

    i = 0
    while not state.end_simulation:
        event = events.next()
        state.time = event.timestamp
        event.handle(state, events)

        constraints = [i % edr == 0]
        if track_tram:
            constraints.append((any([isinstance(event, t) for t in [TramArrival, TramDeparture, Enqueue]]))
                               and (event.tram == int(track_tram)))
        if track_stop:
            constraints.append(not any([isinstance(event, t) for t in [EndSim, LChange, TramDestroy]])
                               and (event.stop == int(track_stop)))
        if only_passengers:
            constraints.append(isinstance(event, PassengerArrival))

        if start:
            constraints.append(event.timestamp.time >= T(start).time)

        if etype:
            constraints.append(type(event).__name__ == etype)

        if all(constraints) or show_all:
            print(event)

        if sdr and i % int(sdr) == 0:
            print(state)

        i += 1
    print(state.statistics)


if __name__ == '__main__':
    run()
